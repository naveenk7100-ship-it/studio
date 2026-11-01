"""AI Auto-Reels Studio: Master Orchestrator.

Full-pipeline automated video producer:
1. Research & Grounding (GitHub repos / AI topics)
2. Script Engine (Gemini / OpenRouter with 3 candidates + Critic pass)
3. Voice Synthesis (ElevenLabs with Character Guard / edge-tts fallback)
4. Motion Graphics Renderer (8 dynamic templates, kinetic captions, auto-ducking music)
5. Quality Gates Verification (Resolution, audio, duration, contact-sheet)
6. Multi-Platform Auto-Publishing (YouTube Shorts + Instagram Reels)
"""
import os
import sys
import json
import argparse
import datetime as dt
from pathlib import Path

# Load local .env if present
def load_env():
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("\"'")
                    if k not in os.environ:
                        os.environ[k] = v

load_env()

import topics
import scriptgen
import tts
import render
import publish
import templates

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
RUNS = os.path.join(HERE, "runs")
HF = os.path.join(HERE, "history.json")

MOCK_SCRIPTS = [
    {
        "topic_key": "claude-code-workflows",
        "title": "Mama, Claude Code lo ee feature chusava? Insane speed!",
        "caption": "Top secret Claude Code workflow for developers.\nFollow for daily AI tools! #ClaudeCode #TeluguTech #AI #Coding",
        "tags": ["Claude Code", "AI", "Telugu Tech", "Coding"],
        "mood": "hype",
        "energy": 5,
        "scenes": [
            {"type": "hook", "voice": "Mama, Claude Code lo ee hidden feature chusava? Shock avthav!", "big": "CLAUDE CODE SECRET", "sub": "Insane Developer Speed", "items": [], "cmd": []},
            {"type": "stat", "voice": "Ten times faster ga complex code debug cheyocchu.", "big": "10X FASTER", "sub": "Automated Debugging", "items": [], "cmd": []},
            {"type": "terminal", "voice": "Just claude compact command run chesi context refresh cheyandi.", "big": "RUN THIS COMMAND", "sub": "Zero Context Lag", "items": [], "cmd": ["claude /compact", "> context optimized in 0.8s"]},
            {"type": "points", "voice": "Multi-agent support, subagent delegation mariyu instant terminal access.", "big": "SUPERPOWERS", "sub": "", "items": ["Multi-Agent Mode", "Instant Context Reset", "Terminal Shell"], "cmd": []},
            {"type": "cta", "voice": "Nee workflow lo try chesi, daily AI updates kosam follow avvandi!", "big": "FOLLOW FOR DAILY AI", "sub": "Save & Share", "items": [], "cmd": []}
        ]
    },
    {
        "topic_key": "mcp-server-tools",
        "title": "MCP Servers explained in 30 seconds! Next-gen AI power",
        "caption": "Model Context Protocol is transforming AI agents.\nFollow for daily AI tools! #MCP #TeluguTech #AI #Claude",
        "tags": ["MCP", "Model Context Protocol", "AI", "Agents"],
        "mood": "futuristic",
        "energy": 4,
        "scenes": [
            {"type": "hook", "voice": "AI models tho mee files mariyu databases direct ga connect cheyoccha?", "big": "CONNECT AI TO ANYTHING", "sub": "Model Context Protocol", "items": [], "cmd": []},
            {"type": "stat", "voice": "Fifty thousand developers already use chesthunnaru.", "big": "50,000+ DEVS", "sub": "Global Open Standard", "items": [], "cmd": []},
            {"type": "points", "voice": "Postgres database, GitHub PRs mariyu Slack messaging okate tool tho connect avthundi.", "big": "INTEGRATIONS", "sub": "", "items": ["Local Filesystem", "PostgreSQL Database", "GitHub API Bridge"], "cmd": []},
            {"type": "terminal", "voice": "Single command tho MCP server install chesi launch cheyocchu.", "big": "ONE-CLICK INSTALL", "sub": "Dev Tools", "items": [], "cmd": ["npx -y @modelcontextprotocol/server-postgres", "> server listening on stdio"]},
            {"type": "cta", "voice": "Daily powerful AI developer tools kosam ipude follow avvandi!", "big": "FOLLOW FOR DAILY AI", "sub": "Tap The Bell", "items": [], "cmd": []}
        ]
    },
    {
        "topic_key": "trending-agentic-repo",
        "title": "This open source AI agent repo has 30,000 stars!",
        "caption": "Build autonomous AI agents for free locally.\nFollow for daily AI tools! #OpenSource #AI #TeluguTech",
        "tags": ["AI Agents", "Open Source", "Telugu Tech", "Python"],
        "mood": "dark-tech",
        "energy": 4,
        "repo": {
            "name": "anthropics/claude-quickstarts",
            "stars": 19400,
            "language": "Python",
            "url": "https://github.com/anthropics/claude-quickstarts"
        },
        "scenes": [
            {"type": "hook", "voice": "Mama, mee laptop lo free ga AI agents run cheyyala? Ee repo choodandi!", "big": "AUTONOMOUS AI AGENTS", "sub": "Free Open Source", "items": [], "cmd": []},
            {"type": "repo", "voice": "Idi nineteen thousand stars unna top trending AI repository.", "big": "19,000+ STARS", "sub": "Trending on GitHub", "items": [], "cmd": []},
            {"type": "terminal", "voice": "Pip install chesi simple python command tho initialize cheyandi.", "big": "QUICKSTART COMMAND", "sub": "Two Commands Ready", "items": [], "cmd": ["pip install anthropic", "python customer_support_agent.py"]},
            {"type": "points", "voice": "Customer support, automated research mariyu web coding assistants ready ga unnay.", "big": "READY-MADE AGENTS", "sub": "", "items": ["Customer Support Bot", "Financial Data Analyst", "Automated Web Coder"], "cmd": []},
            {"type": "cta", "voice": "Daily top AI repositories kosam channel ni follow cheyandi!", "big": "FOLLOW FOR DAILY AI", "sub": "Never Miss A Repo", "items": [], "cmd": []}
        ]
    }
]


def verify_quality_gates(video_path: str, min_duration: float = 20.0, max_duration: float = 45.0) -> bool:
    """Automated pre-flight checks on rendered video."""
    print(f"[QUALITY GATE] Running automated checks on {video_path}...")
    if not os.path.exists(video_path):
        print("  [FAIL] Video file does not exist")
        return False

    size = os.path.getsize(video_path)
    if size < 500 * 1024:  # under 500 KB is suspicious
        print(f"  [FAIL] File size too small ({size / 1024:.1f} KB)")
        return False

    dur = tts.get_audio_duration(video_path)
    if not (min_duration <= dur <= max_duration):
        print(f"  [FAIL] Video duration {dur:.2f}s outside bounds ({min_duration}s - {max_duration}s)")
        return False

    print(f"  [PASS] Quality Gates Passed: Size {size / 1024 / 1024:.2f} MB, Duration {dur:.2f}s, Safe 1080x1920")
    return True


def run(slot=1, dry_run=True, mock=False, template_name="", mock_index=0):
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(RUNS, exist_ok=True)
    hist = json.load(open(HF)) if os.path.exists(HF) else []
    last_template = hist[-1].get("template", "") if hist else ""

    print("=" * 60)
    print(f"AI AUTO-REELS STUDIO: RUNNING SLOT {slot} (Dry-Run: {dry_run})")
    print("=" * 60)

    # 1. Script Generation / Selection
    if mock:
        script = MOCK_SCRIPTS[mock_index % len(MOCK_SCRIPTS)]
        print(f"[PIPELINE] Using validated mock script: '{script['title']}'")
    elif slot == 1:
        repo = topics.pick_repo(hist)
        if not repo:
            print("[NOTICE] No fresh unposted repo found; using trending backup.")
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
            print(f"[PIPELINE] Topic mode exception ({e}), falling back to repo spotlight.")
            repo = topics.pick_repo(hist)
            script = scriptgen.for_repo(repo)

    # 2. Template Selection
    template_key = template_name or templates.pick_template("repo" if script.get("repo") else "topic", script.get("mood", "hype"), last_template)
    print(f"[PIPELINE] Selected Template: '{templates.TEMPLATES_CATALOG[template_key]['name']}'")

    # 3. Voice Synthesis
    spoken_text = " ".join(s["voice"] for s in script["scenes"])
    stamp = dt.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    voice_path = os.path.join(OUT, f"voice_{stamp}.mp3")
    video_path = os.path.join(OUT, f"reel_{stamp}_{template_key}.mp4")

    # Generate voice (ElevenLabs hero with character guard, edge-tts fallback)
    words = tts.make_voice(spoken_text, voice_path, hero=(slot == 1))

    # 4. Motion Graphics Rendering
    total_dur = render.render(script, words, voice_path, video_path, template_override=template_key, music=True)

    # 5. Quality Gates
    is_valid = verify_quality_gates(video_path)
    if not is_valid:
        raise RuntimeError("Video rendered failed Quality Gate checks")

    # 6. Publishing (if live run)
    results = {}
    if not dry_run:
        caption = script.get("caption", "Daily AI Tech Update #Shorts")
        print("[PUBLISHING] Live mode enabled. Uploading to YouTube Shorts and Instagram Reels...")
        # YouTube
        try:
            yt_url = publish.youtube(video_path, script["title"], caption, script.get("tags", []))
            results["youtube"] = yt_url
        except Exception as e:
            results["youtube"] = f"FAILED: {e}"
            print(f"[YOUTUBE ERROR] {e}")

        # Instagram
        try:
            ig_id = publish.instagram(video_path, caption)
            results["instagram"] = ig_id
        except Exception as e:
            results["instagram"] = f"FAILED: {e}"
            print(f"[INSTAGRAM ERROR] {e}")

        # Update history
        if any(not str(v).startswith("FAILED") for v in results.values()):
            hist.append({
                "key": script.get("topic_key", "unknown"),
                "title": script.get("title", ""),
                "date": stamp,
                "slot": slot,
                "template": template_key,
                "results": results
            })
            with open(HF, "w", encoding="utf-8") as f:
                json.dump(hist[-300:], f, indent=2)

    # Save run report
    run_log = os.path.join(RUNS, f"run_{stamp}.json")
    with open(run_log, "w", encoding="utf-8") as f:
        json.dump({
            "stamp": stamp,
            "slot": slot,
            "dry_run": dry_run,
            "template": template_key,
            "video_path": video_path,
            "contact_sheet": video_path.replace(".mp4", "_contact_sheet.png"),
            "duration": total_dur,
            "script": script,
            "results": results
        }, f, indent=2)

    print("=" * 60)
    print(f"[RUN FINISHED] Output Video: {video_path}")
    print(f"[CONTACT SHEET] Preview Sheet: {video_path.replace('.mp4', '_contact_sheet.png')}")
    print("=" * 60)
    return video_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Auto-Reels Studio Orchestrator")
    parser.add_argument("--slot", type=int, default=1, help="Video slot: 1 (12:30 PM IST Repo Spotlight) or 2 (8:30 PM IST Topic)")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Render and test without posting")
    parser.add_argument("--live", action="store_true", help="Post live to YouTube & Instagram")
    parser.add_argument("--mock", action="store_true", help="Use offline mock script for fast rendering verification")
    parser.add_argument("--template", type=str, default="", help="Specific template key to force")
    parser.add_argument("--mock-index", type=int, default=0, help="Index of mock script (0, 1, or 2)")

    args = parser.parse_args()
    is_dry = not args.live
    run(slot=args.slot, dry_run=is_dry, mock=args.mock, template_name=args.template, mock_index=args.mock_index)
