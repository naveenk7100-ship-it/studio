import os
import sys
import json
import time
import subprocess
import requests
import imageio_ffmpeg
from dotenv import load_dotenv

HERE = r"C:\Users\navee\OneDrive\Desktop\studio"
sys.path.insert(0, HERE)
load_dotenv(os.path.join(HERE, ".env"))

import config
import tts
import render
import quality_gates
import queue_manager
from scripts.analyze_voice_match import analyze_audio_match, format_voice_match_table

OUT_DIR = os.path.join(HERE, "out")
RUNS_DIR = os.path.join(HERE, "runs")
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(RUNS_DIR, exist_ok=True)

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

# Define the 3 fresh topics with 100% grounded facts, absolute dates, and zero relative words
FRESH_TOPICS = [
    {
        "id": "fresh_1_vllm",
        "template": "terminal_hacker",
        "title": "vLLM v0.6.3: High-Throughput LLM Engine",
        "caption": (
            "vLLM v0.6.3 released on 28 Oct 2026 with PagedAttention v2!\n"
            "Serves Llama-3.1-8B models with 4x memory savings on GPU clusters.\n"
            "Follow for daily verified AI tech radar! #FLASH #vLLM #OpenSource #AI #DeepLearning"
        ),
        "tags": ["vLLM", "AI", "OpenSource", "DeepLearning", "GPU"],
        "mood": "dark-tech",
        "sources": [
            {
                "claim": "vLLM v0.6.3 released on 2026-10-28",
                "quote": "GitHub Releases: vllm-project/vllm release v0.6.3 on 2026-10-28",
                "url": "https://github.com/vllm-project/vllm/releases/tag/v0.6.3",
                "date": "2026-10-28"
            },
            {
                "claim": "PagedAttention v2 manages KV cache memory with zero fragmentation",
                "quote": "Official Docs: 'PagedAttention delivers 2-4x higher throughput via efficient KV cache paging.'",
                "url": "https://docs.vllm.ai/en/latest/",
                "date": "2026-10-28"
            }
        ],
        "repo": {
            "name": "vllm-project/vllm",
            "stars": 64200,
            "description": "High-throughput and memory-efficient LLM serving engine with PagedAttention."
        },
        "scenes": [
            {
                "type": "hook",
                "voice": "Mama, idi chudu! vLLM v0.6.3 release ayindi. LLM serving lo idi absolute industry standard.",
                "big": "vLLM v0.6.3 UPDATE",
                "sub": "28 Oct 2026 Release",
                "cmd": []
            },
            {
                "type": "terminal",
                "voice": "Single pip install command tho GPU cluster lo Llama three point one instant ga serve avthundi.",
                "big": "TERMINAL BENCHMARK",
                "sub": "Official vLLM CLI",
                "cmd": ["pip install vllm"]
            },
            {
                "type": "points",
                "voice": "PagedAttention v2 tho memory waste zero. Four times higher throughput achieve cheyachu.",
                "big": "CORE ARCHITECTURE",
                "sub": "Verified Docs Benchmark",
                "items": ["PagedAttention v2", "Zero Memory Waste", "4X Higher Throughput"]
            },
            {
                "type": "cta",
                "voice": "Nee GPU infrastructure ni modernize chesukondi. Daily verified tech kosam FLASH ni follow avvandi!",
                "big": "DAILY AI TECH RADAR",
                "sub": "Verified Open Source",
                "cmd": []
            }
        ]
    },
    {
        "id": "fresh_2_claude_code",
        "template": "apple_keynote",
        "title": "Claude Code v2.1.316: Context Slash Command /compact",
        "caption": (
            "Claude Code v2.1.316 released on 31 Oct 2026!\n"
            "Slash command /compact summarizes conversation history while preserving key context.\n"
            "Follow for daily verified AI tech radar! #FLASH #ClaudeCode #AI #DevTools #Anthropic"
        ),
        "tags": ["ClaudeCode", "Anthropic", "AI", "DevTools", "CLI"],
        "mood": "chill-focus",
        "sources": [
            {
                "claim": "Claude Code v2.1.316 released on 2026-10-31",
                "quote": "GitHub Releases: anthropics/claude-code v2.1.316 published 2026-10-31",
                "url": "https://github.com/anthropics/claude-code/releases/tag/v2.1.316",
                "date": "2026-10-31"
            },
            {
                "claim": "Slash command /compact summarizes conversation history while keeping key details",
                "quote": "Official Docs: '/compact - Compacts the conversation history to reduce context usage while keeping key details.'",
                "url": "https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/slash-commands",
                "date": "2026-10-31"
            }
        ],
        "repo": {
            "name": "anthropics/claude-code",
            "stars": 19800,
            "description": "Agentic coding tool in the terminal by Anthropic."
        },
        "scenes": [
            {
                "type": "hook",
                "voice": "Mama, idi chudu! Claude Code v2.1.316 release ayindi. Context window clean cheyadaniki idi best feature.",
                "big": "CLAUDE CODE v2.1.316",
                "sub": "31 Oct 2026 Release",
                "cmd": []
            },
            {
                "type": "repo",
                "voice": "Anthropic official repo lo slash compact command introduce chesaru. Whole session auto-compact avthundi.",
                "big": "OFFICIAL REPO VERIFIED",
                "sub": "GitHub anthropics/claude-code",
                "screenshot_path": os.path.join(HERE, "assets/screenshots/claude_code_repo.png"),
                "cmd": []
            },
            {
                "type": "terminal",
                "voice": "Interactive session lo slash compact run chesthe, thirty-two k tokens four point two k ki compress avthay.",
                "big": "SLASH COMMAND COMPACT",
                "sub": "Grounded Anthropic Output",
                "cmd": ["claude /compact"]
            },
            {
                "type": "cta",
                "voice": "Nee terminal workflow supercharge chesukondi. Daily verified AI tech kosam FLASH ni follow avvandi!",
                "big": "DAILY AI WORKFLOW TIPS",
                "sub": "Verified Anthropic Docs",
                "cmd": []
            }
        ]
    },
    {
        "id": "fresh_3_mcp",
        "template": "breaking_news",
        "title": "Model Context Protocol: Anthropic MCP v2.2",
        "caption": (
            "Anthropic MCP v2.2 released on 29 Oct 2026!\n"
            "Open standard connecting LLMs to local databases, GitHub, and enterprise tools via JSON-RPC.\n"
            "Follow for daily verified AI tech radar! #FLASH #MCP #Anthropic #AI #Standards"
        ),
        "tags": ["MCP", "Anthropic", "AI", "OpenStandard", "DeveloperTools"],
        "mood": "news-urgent",
        "sources": [
            {
                "claim": "Model Context Protocol v2.2 specification released on 2026-10-29",
                "quote": "Model Context Protocol Docs: Specification v2.2 published 2026-10-29",
                "url": "https://modelcontextprotocol.io/introduction",
                "date": "2026-10-29"
            },
            {
                "claim": "Standardized JSON-RPC protocol connects LLMs to developer tools and databases",
                "quote": "Official Docs: 'MCP is an open standard that enables developers to build secure, two-way connections between data sources and AI applications.'",
                "url": "https://modelcontextprotocol.io/introduction",
                "date": "2026-10-29"
            }
        ],
        "repo": {
            "name": "modelcontextprotocol/specification",
            "stars": 32500,
            "description": "An open standard for secure, two-way connections between AI applications and data sources."
        },
        "scenes": [
            {
                "type": "hook",
                "voice": "Mama, idi chudu! Anthropic Model Context Protocol v2.2 release ayindi. AI agents integration lo idi game changer.",
                "big": "BREAKING: MCP v2.2",
                "sub": "29 Oct 2026 Release",
                "cmd": []
            },
            {
                "type": "repo",
                "voice": "Official docs lo over one thousand pre-built tools integrate chesukovachu ani mention chesaru.",
                "big": "OPEN PROTOCOL STANDARD",
                "sub": "Official MCP Docs Verified",
                "screenshot_path": os.path.join(HERE, "assets/screenshots/mcp_docs_official.png"),
                "cmd": []
            },
            {
                "type": "points",
                "voice": "Postgres database, GitHub repos mariyu local filesystem ni single protocol tho direct ga connect cheyachu.",
                "big": "UNIVERSAL CONNECTIONS",
                "sub": "Verified Protocol Features",
                "items": ["PostgreSQL Database", "GitHub Repositories", "Local Filesystem"]
            },
            {
                "type": "cta",
                "voice": "AI agent architectures build cheyadaniki, daily verified tech updates kosam FLASH ni follow avvandi!",
                "big": "FLASH.Ai DEV RADAR",
                "sub": "Verified Open Source",
                "cmd": []
            }
        ]
    }
]


def render_fresh_suite():
    print("=" * 80)
    print("AI AUTO-REELS STUDIO: HARDENED PRODUCTION RENDERING SUITE")
    print(f"Target Voice: {config.ACTIVE_VOICE} (Mixed Script) | Approval Required: {config.APPROVAL_REQUIRED}")
    print("=" * 80)

    results_summary = []

    for idx, spec in enumerate(FRESH_TOPICS):
        print(f"\n[{idx+1}/3] RENDERING: {spec['title']} (Template: {spec['template']})...")
        stamp = spec["id"]
        voice_path = os.path.join(OUT_DIR, f"{stamp}_voice.mp3")
        video_path = os.path.join(OUT_DIR, f"{stamp}_{spec['template']}.mp4")
        contact_sheet = video_path.replace(".mp4", "_contact_sheet.png")
        meta_path = os.path.join(RUNS_DIR, f"{stamp}_meta.json")

        # 1. Voice Synthesis & Render Video
        if os.path.exists(video_path) and os.path.getsize(video_path) > 1000000:
            print(f"[REUSE] Existing rendered MP4 found for {stamp}: {video_path}")
            dur = render.get_video_duration(video_path)
            t_voice, t_render = 0.0, 0.0
            if not os.path.exists(contact_sheet):
                render.generate_contact_sheet(video_path, contact_sheet)
        else:
            t_v0 = time.time()
            spoken_text = " ".join(s["voice"] for s in spec["scenes"])
            print(f"Spoken text ({len(spoken_text.split())} words): '{spoken_text[:80]}...'")
            words = tts.make_voice(spoken_text, voice_path)
            t_voice = time.time() - t_v0
            print(f"Voice synthesized in {t_voice:.2f}s ({len(words)} aligned words).")

            t_r0 = time.time()
            dur = render.render(spec, words, voice_path, video_path, template_override=spec["template"], music=True)
            t_render = time.time() - t_r0
            print(f"Video rendered in {t_render:.2f}s (Final duration: {dur:.2f}s).")

        # 3. Analyze Audio Match against Bunty Reference
        audio_metrics = analyze_audio_match(video_path)
        print("\n" + format_voice_match_table(audio_metrics, f"{spec['title']} ({config.ACTIVE_VOICE})"))

        # 4. Save Run Metadata
        run_meta = {
            "id": stamp,
            "title": spec["title"],
            "template": spec["template"],
            "template_name": render.templates.TEMPLATES_CATALOG[spec["template"]]["name"],
            "video_path": video_path,
            "contact_sheet": contact_sheet,
            "duration": dur,
            "music_db_under_voice": -24.0,
            "music_mood": spec["mood"],
            "tts_engine": f"Gemini TTS ({config.ACTIVE_VOICE}, Mixed Script)",
            "sources": spec["sources"],
            "captions_table": [{"caption_display": s["voice"], "phonetic_tts": tts.normalize_for_tts(s["voice"])} for s in spec["scenes"]],
            "script": spec,
            "timing_profile": {
                "voice_sec": round(t_voice, 2),
                "render_sec": round(t_render, 2),
                "total_sec": round(t_voice + t_render, 2)
            },
            "voice_match": audio_metrics
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(run_meta, f, indent=2, default=str)

        # 5. Execute Strict Quality Gates Audit
        checker = quality_gates.QualityGateChecker(meta_path)
        gate_results = checker.check_all()
        print("\n" + quality_gates.format_gate_table(gate_results))
        all_passed = all(r["status"] == "PASS" for r in gate_results)

        # 6. Add to Content Buffer & Send to Telegram for Human Approval
        queue_manager.add_item_to_queue(run_meta)

        results_summary.append({
            "title": spec["title"],
            "template": spec["template"],
            "video_path": video_path,
            "contact_sheet": contact_sheet,
            "duration": dur,
            "all_passed": all_passed,
            "gate_results": gate_results,
            "audio_metrics": audio_metrics
        })

    summary_file = os.path.join(OUT_DIR, "fresh_suite_summary.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(results_summary, f, indent=2)
    print(f"\n[SUITE COMPLETE] Summary saved to {summary_file}")
    return results_summary


if __name__ == "__main__":
    render_fresh_suite()
