"""
FLASH Content OS - 30s Speech Synthesis & Forced Alignment
Synthesizes natural Tenglish speech using Gemini TTS Sadachbia (with te-IN/en-IN fallback)
and generates word-level timestamps.
"""

import os
import sys
import json
from dotenv import load_dotenv

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
sys.path.insert(0, ROOT)
load_dotenv(os.path.join(ROOT, ".env"))

import tts

CACHE_DIR = os.path.join(ROOT, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

NEW_REELS = [
    {
        "id": "reel_new_1_superagent",
        "title": "DeepSeek SuperAgent: Autonomous Hierarchy",
        "script": (
            "Mama, autonomous AI agents ki next-gen breakthrough idi: deepseek-ai nunchi SuperAgent Prototype release ayyindi. "
            "Idi complex coding tasks ni planning mariyu execution sub-agents ga divide chesthundi. "
            "Single prompt tho direct codebase edits mariyu verification steps run chesthundi. "
            "GitHub lo 18,000 stars cross chesina viral rising repo idi. "
            "Terminal lo python run_agent.py command tho local ga test cheyochu. "
            "Production lo max-step limits petadam marchipokandi. "
            "Daily fresh tech intelligence kosam FLASH ni FOLLOW cheyandi!"
        ),
        "voice_out": os.path.join(CACHE_DIR, "voice_superagent.mp3"),
        "words_out": os.path.join(CACHE_DIR, "words_superagent.json"),
    },
    {
        "id": "reel_new_2_ollama",
        "title": "Ollama v0.40.14: Local LLM Unified Runtime",
        "script": (
            "Mama, mee local laptop lo LLMs run cheyalante Ollama fresh v0.40.14 update release ayyindi. "
            "Deenilo automated GPU layer offloading mariyu multi-model routing chala smooth ga pani chesthundhi. "
            "Kevalam single command ollama run qwen2.5 tho 7B model seconds lo load avthundi. "
            "Cloud APIs lekunda, 100% private ga complete AI server mee machine lone run avthundi. "
            "Large context ki VRAM allocate avthundi kabatti memory check cheskondi. "
            "Daily top developer tools kosam FLASH ni FOLLOW cheyandi!"
        ),
        "voice_out": os.path.join(CACHE_DIR, "voice_ollama.mp3"),
        "words_out": os.path.join(CACHE_DIR, "words_ollama.json"),
    },
    {
        "id": "reel_new_3_qwen_news",
        "title": "Qwen 27B: Local Model Weight Interpretability",
        "script": (
            "Mama, నిన్నటి viral Hacker News top discussion idi: Qwen 27B model local laptop lone model weights interpret chesthundi. "
            "656 points tho trending unna ee research lo, cloud clusters avasaram lekunda local hardware medha neural activation vectors inspect cheyochu. "
            "Developer laptops lo direct model weight analysis cheyatam idi first time. "
            "Run cheyalante 16GB unified memory leda 24GB VRAM undali. "
            "Daily verified AI news mariyu practical insights kosam FLASH ni FOLLOW cheyandi!"
        ),
        "voice_out": os.path.join(CACHE_DIR, "voice_qwen_news.mp3"),
        "words_out": os.path.join(CACHE_DIR, "words_qwen_news.json"),
    },
]

def synthesize_all():
    print("================ SYNTHESIZING VOICES FOR 3 NEW REELS ================")
    for item in NEW_REELS:
        print(f"\n>>> Generating voice for {item['id']}: {item['title']}...")
        aligned_words = tts.make_voice(
            display_text=item["script"],
            path=item["voice_out"],
            voice_override="Sadachbia"
        )
        with open(item["words_out"], "w", encoding="utf-8") as f:
            json.dump(aligned_words, f, indent=2)
        duration = tts.get_audio_duration(item["voice_out"])
        print(f"  [SYNTHESIZED] Audio: {item['voice_out']} ({duration:.2f}s, {len(aligned_words)} aligned words)")

if __name__ == "__main__":
    synthesize_all()
