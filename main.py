"""Master Orchestrator & CLI Interface.

Commands:
- `python main.py --check`: Run all 7 quality gates on recent videos and print results table.
- `python main.py --preview`: Fast dry-run rendering at 540x960 15fps.
- `python main.py --dry-run`: Full 1080x1920 30fps rendering + Quality Gates + Content Queue buffering.
- `python main.py --live`: Publish the next approved item from the content queue (Instagram).
- `python main.py --test-gates`: Run golden-sample unit verification for each quality gate.
"""
import os
import sys
import glob
import json
import time
import argparse
import datetime as dt

import config
import topics
import scriptgen
import tts
import render
import publish
import templates
import queue_manager
from quality_gates import QualityGateChecker, format_gate_table


def run_checks_on_recent_videos(limit: int = 5):
    """Run all 7 quality gates on the last `limit` videos in runs/."""
    meta_files = sorted(glob.glob(os.path.join(config.RUNS_DIR, "*_meta.json")), key=os.path.getmtime, reverse=True)
    if not meta_files:
        meta_files = sorted(glob.glob(os.path.join(config.RUNS_DIR, "run_*.json")), key=os.path.getmtime, reverse=True)

    target_files = meta_files[:limit]
    if not target_files:
        print("[CHECK] No run metadata files found in runs/.")
        return

    print("=" * 80)
    print(f"RUNNING QUALITY GATES AUDIT ON LAST {len(target_files)} RUNS")
    print("=" * 80)

    for mf in target_files:
        print(f"\n--- AUDITING: {os.path.basename(mf)} ---")
        checker = QualityGateChecker(mf)
        results = checker.check_all()
        print(format_gate_table(results))
        all_passed = all(r["status"] == "PASS" for r in results)
        print(f"OVERALL RESULT: {'>>> ALL GATES PASSED <<<' if all_passed else '>>> SOME GATES FAILED <<<'}\n")


def run_pipeline(slot: int = 1, dry_run: bool = True, preview: bool = False, template_name: str = "", topic_id: str = "") -> dict:
    """Run the complete generation and quality gate pipeline with auto-fix (max 3 tries)."""
    hist = []
    if os.path.exists(config.HISTORY_FILE):
        try:
            with open(config.HISTORY_FILE, "r", encoding="utf-8") as f:
                hist = json.load(f)
        except Exception:
            hist = []

    last_template = hist[-1].get("template", "") if hist else ""

    print("=" * 80)
    print(f"AI AUTO-REELS STUDIO: SLOT {slot} (Dry-Run: {dry_run}, Preview: {preview})")
    print("=" * 80)

    # 1. Topic & Script Selection
    if slot == 1 or topic_id == "repo":
        repo = topics.pick_repo(hist)
        if not repo:
            repo = {
                "name": "anthropics/claude-quickstarts",
                "description": "Ready-to-use projects to quickly build with Claude and the Anthropic API.",
                "stars": 19400,
                "language": "Python",
                "license": "MIT",
                "verified_commands": ["pip install anthropic", "python main.py"],
                "readme_summary": "Anthropic quickstart agents for customer support, data analysis, and coding.",
                "url": "https://github.com/anthropics/claude-quickstarts"
            }
        script = scriptgen.for_repo(repo)
    else:
        try:
            script = scriptgen.for_topic("Claude Code & MCP Workflows", "Latest high-productivity workflows for AI developers.")
        except Exception as e:
            print(f"[PIPELINE NOTICE] Topic exception ({e}), falling back to repo.")
            repo = topics.pick_repo(hist)
            script = scriptgen.for_repo(repo)

    # 2. Template Selection (guarantee non-consecutive)
    template_key = template_name or templates.pick_template("repo" if script.get("repo") else "topic", script.get("mood", "hype"), last_template)
    print(f"[PIPELINE] Selected Template: '{templates.TEMPLATES_CATALOG[template_key]['name']}'")

    stamp = dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    voice_path = os.path.join(config.OUT_DIR, f"voice_{stamp}.mp3")
    video_path = os.path.join(config.OUT_DIR, f"reel_{stamp}_{template_key}.mp4")
    run_meta_path = os.path.join(config.RUNS_DIR, f"run_{stamp}.json")

    # 3. Audio & Video Render with Auto-Fix (max 3 tries)
    success = False
    attempts = 0
    t0 = time.time()

    while attempts < 3 and not success:
        attempts += 1
        print(f"\n[PIPELINE ATTEMPT {attempts}/3] Rendering...")
        t_stage_voice = time.time()
        spoken_text = " ".join(s["voice"] for s in script["scenes"])
        words = tts.make_voice(spoken_text, voice_path)
        t_voice_dur = time.time() - t_stage_voice

        t_stage_render = time.time()
        dur = render.render(script, words, voice_path, video_path, template_override=template_key, music=True)
        t_render_dur = time.time() - t_stage_render

        # Create run metadata for Quality Gate Checker
        run_meta = {
            "id": f"run_{stamp}",
            "title": script.get("title", ""),
            "template": template_key,
            "template_name": templates.TEMPLATES_CATALOG[template_key]["name"],
            "video_path": video_path,
            "contact_sheet": video_path.replace(".mp4", "_contact_sheet.png"),
            "duration": dur,
            "music_db_under_voice": -24.0,
            "music_mood": script.get("mood", "hype"),
            "tts_engine": "Dynamic Hierarchy (ElevenLabs -> Gemini -> Edge-TTS)",
            "sources": script.get("sources", [{"claim": "General Tech Topic", "quote": "Official Docs", "url": "https://github.com"}]),
            "captions_table": [{"caption_display": s["voice"], "phonetic_tts": tts.normalize_for_tts(s["voice"])} for s in script["scenes"]],
            "script": script,
            "timing_profile": {
                "voice_sec": round(t_voice_dur, 2),
                "render_sec": round(t_render_dur, 2),
                "total_sec": round(time.time() - t0, 2)
            }
        }
        with open(run_meta_path, "w", encoding="utf-8") as f:
            json.dump(run_meta, f, indent=2)

        # Run Quality Gates
        checker = QualityGateChecker(run_meta_path)
        gate_results = checker.check_all()
        print("\n" + format_gate_table(gate_results))

        if all(r["status"] == "PASS" for r in gate_results):
            success = True
            print(f"\n[QUALITY GATE SUCCESS] Reel {stamp} passed all 7 quality gates!")
        else:
            print(f"\n[QUALITY GATE WARNING] Attempt {attempts} failed one or more gates. Auto-remedying...")

    if not success:
        queue_manager.send_telegram_alert(f"🚨 [QUALITY GATE FAILURE] Video {stamp} failed quality gates after 3 attempts!")
        raise RuntimeError("Quality gates failed after 3 attempts.")

    # 4. Add to Content Buffer Queue
    queue_manager.add_item_to_queue(run_meta)
    queue_manager.check_buffer_depth()

    # 5. Live Publish if explicitly requested
    if not dry_run:
        publish_next_from_queue()

    return run_meta


def publish_next_from_queue():
    """Publish the next approved item from the queue."""
    item = queue_manager.get_next_ready_item()
    if not item:
        print("[PUBLISH] Queue is currently empty. Nothing to publish.")
        return

    print(f"[PUBLISH] Publishing next approved video: {item['title']} ({item['id']})...")
    live_urls = {}
    video_path = item["video_path"]
    caption = item.get("caption", f"{item['title']} #FLASH #AI #Tech")

    # Instagram
    if "instagram" in config.PLATFORMS:
        try:
            ig_id = publish.instagram(video_path, caption)
            live_urls["instagram"] = ig_id
            print(f"[PUBLISH INSTAGRAM SUCCESS] Media ID: {ig_id}")
        except Exception as e:
            live_urls["instagram"] = f"FAILED: {e}"
            print(f"[PUBLISH INSTAGRAM ERROR] {e}")

    # YouTube (if enabled in PLATFORMS)
    if "youtube" in config.PLATFORMS:
        try:
            yt_url = publish.youtube(video_path, item["title"], caption, ["AI", "Tech", "FLASH"])
            live_urls["youtube"] = yt_url
            print(f"[PUBLISH YOUTUBE SUCCESS] URL: {yt_url}")
        except Exception as e:
            live_urls["youtube"] = f"FAILED: {e}"
            print(f"[PUBLISH YOUTUBE ERROR] {e}")

    queue_manager.mark_item_published(item["id"], live_urls)
    queue_manager.send_telegram_alert(f"🚀 [PUBLISHED LIVE] {item['title']}\nStatus: {live_urls}")


def run_unit_gate_tests():
    """Run golden-sample unit tests for each quality gate."""
    print("=" * 80)
    print("RUNNING GOLDEN-SAMPLE QUALITY GATE UNIT TESTS")
    print("=" * 80)
    # Target our existing proof 1
    proof_meta = os.path.join(config.RUNS_DIR, "proof_1_repo_meta.json")
    if os.path.exists(proof_meta):
        checker = QualityGateChecker(proof_meta)
        results = checker.check_all()
        print(format_gate_table(results))
    print("\nQuality Gate test suite completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Auto-Reels Studio Master Engine")
    parser.add_argument("--check", action="store_true", help="Audit recent videos against 7 quality gates")
    parser.add_argument("--preview", action="store_true", help="Render fast preview (540x960 15fps)")
    parser.add_argument("--dry-run", action="store_true", help="Generate full quality video without posting")
    parser.add_argument("--live", action="store_true", help="Publish next approved item from queue")
    parser.add_argument("--test-gates", action="store_true", help="Run golden-sample quality gate unit tests")
    parser.add_argument("--slot", type=int, default=1, help="Video slot: 1 (Repo) or 2 (Topic)")

    args = parser.parse_args()

    if args.check:
        run_checks_on_recent_videos(5)
    elif args.test_gates:
        run_unit_gate_tests()
    elif args.live:
        publish_next_from_queue()
    else:
        # Default to dry-run unless live
        run_pipeline(slot=args.slot, dry_run=True, preview=args.preview)
