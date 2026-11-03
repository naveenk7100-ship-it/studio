import os
import sys
import json
import requests
from dotenv import load_dotenv

HERE = r"C:\Users\navee\OneDrive\Desktop\studio"
load_dotenv(os.path.join(HERE, ".env"))

BOT = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT = os.getenv("TELEGRAM_CHAT_ID")
OUT_DIR = os.path.join(HERE, "out")

reels = [
    {
        "id": "golden_reel_1_vllm",
        "video": os.path.join(OUT_DIR, "golden_reel_1_vllm.mp4"),
        "sheet": os.path.join(OUT_DIR, "golden_reel_1_vllm_contact_sheet.png"),
        "title": "Golden Reel 1: vLLM High-Throughput LLM Serving",
        "caption": "⚡ FLASH Golden Reel 1 (vLLM)\n• Audio: Sadachbia TTS + ducked dark-tech BGM\n• Loudness: -14.3 LUFS | True Peak: -1.6 dBTP\n• Word Sync Median: 6.7 ms (p95: 13.3 ms)\n• Hero Visual: 53.1% canvas height\n• Pop captions + 3D Browser mockup (perspective 1200px)\n• Live Stars: 96,121 (GitHub API verified)\n• Caveat: Gated Llama-3.1-8B needs HF_TOKEN"
    },
    {
        "id": "golden_reel_2_claude_code",
        "video": os.path.join(OUT_DIR, "golden_reel_2_claude_code.mp4"),
        "sheet": os.path.join(OUT_DIR, "golden_reel_2_claude_code_contact_sheet.png"),
        "title": "Golden Reel 2: Claude Code CLI /compact Session",
        "caption": "⚡ FLASH Golden Reel 2 (Claude Code)\n• Audio: Sadachbia TTS + ducked dark-tech BGM\n• Loudness: -14.7 LUFS | True Peak: -1.6 dBTP\n• Word Sync Median: 10.0 ms (p95: 13.3 ms)\n• Hero Visual: 53.1% canvas height\n• Pop captions + 3D Anthropic Docs mockup\n• Motion min window: 0.599 (Sec 8-11 motion floor resolved)\n• Clean truth: /compact summarizes vs /clear resets (no unsourced numbers)"
    }
]

for r_item in reels:
    print(f"\n--- Sending {r_item['id']} to Telegram ---")
    inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": "✅ Approve", "callback_data": f"approve:{r_item['id']}"},
                {"text": "❌ Reject", "callback_data": f"reject:{r_item['id']}"}
            ]
        ]
    }
    
    if os.path.exists(r_item["sheet"]):
        with open(r_item["sheet"], "rb") as f:
            r = requests.post(
                f"https://api.telegram.org/bot{BOT}/sendPhoto",
                data={"chat_id": CHAT, "caption": f"🎬 Contact Sheet: {r_item['title']}\n{r_item['caption'][:200]}"},
                files={"photo": f},
                timeout=45
            )
            print("Contact Sheet status:", r.status_code)

    if os.path.exists(r_item["video"]):
        with open(r_item["video"], "rb") as f:
            r = requests.post(
                f"https://api.telegram.org/bot{BOT}/sendVideo",
                data={
                    "chat_id": CHAT,
                    "caption": f"⚡ {r_item['title']}\n{r_item['caption']}",
                    "reply_markup": json.dumps(inline_keyboard)
                },
                files={"video": f},
                timeout=180
            )
            print("Video upload status:", r.status_code)

print("\nGolden reels and contact sheets sent to Telegram successfully!")
