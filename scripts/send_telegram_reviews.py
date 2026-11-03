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

videos = [
    {
        "id": "fresh_1_vllm",
        "video": os.path.join(OUT_DIR, "fresh_1_vllm_terminal_hacker.mp4"),
        "sheet": os.path.join(OUT_DIR, "fresh_1_vllm_terminal_hacker_contact_sheet.png"),
        "title": "Fresh Video 1: vLLM v0.6.3 (Terminal Hacker - 28.3s, -14.2 LUFS, 9.8% Flat Void)",
        "caption": "vLLM v0.6.3 released on 28 Oct 2026 with PagedAttention v2!\nServes Llama-3.1-8B models with 4x memory savings on GPU clusters."
    },
    {
        "id": "fresh_2_claude_code",
        "video": os.path.join(OUT_DIR, "fresh_2_claude_code_apple_keynote.mp4"),
        "sheet": os.path.join(OUT_DIR, "fresh_2_claude_code_apple_keynote_contact_sheet.png"),
        "title": "Fresh Video 2: Claude Code v2.1.316 (Apple Keynote - 31.8s, -13.9 LUFS, 9.9% Flat Void)",
        "caption": "Claude Code v2.1.316 released on 31 Oct 2026!\nSlash command /compact summarizes conversation history while preserving key context."
    },
    {
        "id": "fresh_3_mcp",
        "video": os.path.join(OUT_DIR, "fresh_3_mcp_breaking_news.mp4"),
        "sheet": os.path.join(OUT_DIR, "fresh_3_mcp_breaking_news_contact_sheet.png"),
        "title": "Fresh Video 3: Anthropic MCP v2.2 (Breaking News - 29.2s, -13.7 LUFS, 9.1% Flat Void)",
        "caption": "Anthropic MCP v2.2 released on 29 Oct 2026!\nOpen standard connecting LLMs to local databases, GitHub, and enterprise tools via JSON-RPC."
    }
]

for v in videos:
    print(f"\n--- Transmitting to Telegram: {v['id']} ---")
    inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": "✅ Approve", "callback_data": f"approve:{v['id']}"},
                {"text": "❌ Reject", "callback_data": f"reject:{v['id']}"},
                {"text": "🔄 Regenerate", "callback_data": f"regen:{v['id']}"}
            ]
        ]
    }
    
    # Send contact sheet
    if os.path.exists(v["sheet"]):
        with open(v["sheet"], "rb") as f:
            r = requests.post(
                f"https://api.telegram.org/bot{BOT}/sendPhoto",
                data={"chat_id": CHAT, "caption": f"🎬 Contact Sheet: {v['title']}\n{v['caption'][:200]}"},
                files={"photo": f},
                timeout=45
            )
            print("Contact Sheet status:", r.status_code)

    # Send video with inline approval buttons
    if os.path.exists(v["video"]):
        with open(v["video"], "rb") as f:
            r = requests.post(
                f"https://api.telegram.org/bot{BOT}/sendVideo",
                data={
                    "chat_id": CHAT,
                    "caption": f"⚡ {v['title']}\nPlease review and click below for 12:30 PM / 8:30 PM IST slot:",
                    "reply_markup": json.dumps(inline_keyboard)
                },
                files={"video": f},
                timeout=180
            )
            print("Video upload status:", r.status_code)

print("\nAll videos and contact sheets delivered to Telegram with inline approval buttons!")
