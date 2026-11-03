"""
Synthesize 28-30s Voiceover Tracks for 3 Golden Explainer Videos:
1. vLLM High-Throughput Serving (Prompt ID 164)
2. Claude Code CLI /compact Session (Prompt ID 274)
3. Anthropic Model Context Protocol (MCP) (Prompt ID 242)
Mastered to 48kHz, -14.0 LUFS, with Whisper forced alignment.
"""

import os
import sys
import json
import re
from dotenv import load_dotenv

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
sys.path.insert(0, ROOT)
load_dotenv(os.path.join(ROOT, ".env"))

import tts

CACHE_DIR = os.path.join(ROOT, "cache")

VIDEOS_30S = [
    {
        "id": "vllm_30s",
        "title": "vLLM High-Throughput Serving Engine",
        "script": (
            "Mama, mee local GPU lo LLMs high-speed serve cheyalani anukuntunnara? "
            "Idi vLLM v0.32.0. Idi oka open-source high-throughput inference engine. "
            "Deeni PagedAttention algorithm KV-cache memory waste ni zero chesthundi. "
            "Single GPU lo 4x ekuva concurrent requests handle chesthundi. "
            "Terminal lo vllm serve meta-llama type chesi direct ga deploy cheyochu. "
            "Gated model kabatti HuggingFace token kavali, leda direct ga Qwen vadachu. "
            "Daily top tech tools kosam FLASH ni FOLLOW cheyandi!"
        ),
        "voice_out": os.path.join(CACHE_DIR, "voice_30s_vllm.mp3"),
        "words_out": os.path.join(CACHE_DIR, "words_30s_vllm.json")
    },
    {
        "id": "claude_30s",
        "title": "Claude Code CLI /compact Session",
        "script": (
            "Mama, Claude Code terminal lo daily coding chesthunnara? "
            "Pedda codebases lo work chesthunappudu context limit fill aypothundi. "
            "Daaniki official solution /compact slash command. "
            "Idi conversation history ni condense chesthundi, key file paths mariyu decisions retain chesthundi. "
            "Idi session reset cheyadhu, kevalam context token load thagginchuthundi. "
            "Reset cheyalante /clear vadali, context preserve cheyalante /compact matrame vadali. "
            "Daily pro developer tips kosam FLASH ni FOLLOW cheyandi!"
        ),
        "voice_out": os.path.join(CACHE_DIR, "voice_30s_claude.mp3"),
        "words_out": os.path.join(CACHE_DIR, "words_30s_claude.json")
    },
    {
        "id": "mcp_30s",
        "title": "Anthropic Model Context Protocol (MCP)",
        "script": (
            "Mama, AI agents ki local databases mariyu APIs connect cheyatam kastam anukuntunnara? "
            "Idi Anthropic launch chesina Model Context Protocol, aka MCP open standard. "
            "Custom wrappers lekunda, oke standard protocol tho LLMs tools ni access chesthayi. "
            "Local Postgres, GitHub repos, leda Google Drive ni direct secure connection ivvochu. "
            "Terminal lo npx mcp-server run chesi Mee agent ki powers ivvandi. "
            "Next-gen agentic workflows kosam FLASH ni FOLLOW cheyandi!"
        ),
        "voice_out": os.path.join(CACHE_DIR, "voice_30s_mcp.mp3"),
        "words_out": os.path.join(CACHE_DIR, "words_30s_mcp.json")
    }
]

def main():
    print("\n=======================================================")
    print("SYNTHESIZING 30S VOICE TRACKS (SADACHBIA TTS)")
    print("=======================================================")
    
    for v in VIDEOS_30S:
        print(f"\n>>> Synthesizing: {v['title']} ({v['id']})...")
        words = [w for w in re.split(r"\s+", v["script"].strip()) if w]
        
        # Check if already cached
        if os.path.exists(v["voice_out"]) and os.path.exists(v["words_out"]):
            print(f"Using cached audio: {v['voice_out']}")
            continue
            
        aligned_words = tts.make_voice(
            display_text=v["script"],
            path=v["voice_out"],
            voice_override="Sadachbia"
        )
        
        with open(v["words_out"], "w", encoding="utf-8") as f:
            json.dump(aligned_words, f, indent=2)
            
        dur = tts.get_audio_duration(v["voice_out"])
        print(f"Generated {v['voice_out']}: {dur:.2f}s ({len(aligned_words)} aligned words)")

if __name__ == "__main__":
    main()
