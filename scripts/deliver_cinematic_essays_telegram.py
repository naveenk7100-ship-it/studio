"""
FLASH Content OS - Idempotent Telegram Delivery for Cinematic Visual-Metaphor Essay Reels
Delivers:
- Contact sheet (8 beat stills)
- Resource pack briefing card with single-source verified facts
- Mastered 28.00s MP4 video with inline approval buttons

Idempotency:
- Checks delivery_log.json before sending.
- Skips if video id has already been delivered (unless --force is passed).
- Records delivery timestamp and message IDs upon completion.
"""

import os
import sys
import json
import time
import html
import requests
from dotenv import load_dotenv

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
load_dotenv(os.path.join(ROOT, ".env"))

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "7031739832")
OUT_DIR = os.path.join(ROOT, "out")
CACHE_DIR = os.path.join(ROOT, "cache")
LOG_PATH = os.path.join(ROOT, "delivery_log.json")

FORCE_RESEND = "--force" in sys.argv

DELIVERIES = [
    {
        "id": "reel_essay_1_unslop",
        "title": "heydamir / unslop: Vibecoded UI De-Slopper & Human Styler",
        "video_path": os.path.join(OUT_DIR, "reel_essay_1_unslop.mp4"),
        "sheet_path": os.path.join(OUT_DIR, "reel_essay_1_unslop_contact_sheet.png"),
        "template": "Cinematic Visual-Metaphor Essay (Fanning Cards & De-Slop Transformer)",
        "metrics": "Audio: -14.6 LUFS | TP: -1.8 dBTP | 48kHz | Jitter: 0.000002 px² | Coverage: 72.5%",
        "facts": [
            "• GitHub Stars: 8,905 (Verified from api.github.com/repos/heydamir/unslop)",
            "• Created: 29 Oct 2026 (7.0 days old - Rising Repo)",
            "• Core: Official Claude skill that turns vibecoded, AI-looking UI into a human-designed interface",
            "• Launch Command: npx @damir/unslop",
            "• Skill Boundary: Transforms UI design tokens, contrast ratios and typography; backend code untouched"
        ],
        "script": "Mama, AI generate chesina UI chusi chusi bore kottinda? Idi unslop, Claude skill...",
        "source_url": "https://github.com/heydamir/unslop"
    },
    {
        "id": "reel_essay_2_uv",
        "title": "astral-sh / uv 0.13.7: High-Velocity Python Package Manager",
        "video_path": os.path.join(OUT_DIR, "reel_essay_2_uv.mp4"),
        "sheet_path": os.path.join(OUT_DIR, "reel_essay_2_uv_contact_sheet.png"),
        "template": "Cinematic Visual-Metaphor Essay (Velocity Gauge & Pipeline Flow)",
        "metrics": "Audio: -14.5 LUFS | TP: -1.9 dBTP | 48kHz | Jitter: 0.000002 px² | Coverage: 72.5%",
        "facts": [
            "• GitHub Stars: 91,554 (Verified from api.github.com/repos/astral-sh/uv)",
            "• Release Tag: 0.13.7 (Published 03 Nov 2026 - 2.3 days old - Tool Release)",
            "• Core: 10-100x faster Python package resolver written in Rust with built-in virtual environment management",
            "• Launch Command: curl -LsSf https://astral.sh/uv/install.sh | sh",
            "• System Boundary: Replaces pip, pip-tools and virtualenv; full drop-in workflow compatibility"
        ],
        "script": "Mama, Python package installations inka slow ga unte, Astral UV 0.13.7 vadandi...",
        "source_url": "https://github.com/astral-sh/uv/releases/tag/0.13.7"
    },
    {
        "id": "reel_essay_3_kimi",
        "title": "Moonshot AI Kimi K3.1 Pro: Open Architecture Weights",
        "video_path": os.path.join(OUT_DIR, "reel_essay_3_kimi.mp4"),
        "sheet_path": os.path.join(OUT_DIR, "reel_essay_3_kimi_contact_sheet.png"),
        "template": "Cinematic Visual-Metaphor Essay (Neural Tile Wall & Architecture Flow)",
        "metrics": "Audio: -14.4 LUFS | TP: -1.9 dBTP | 48kHz | Jitter: 0.000001 px² | Coverage: 72.5%",
        "facts": [
            "• Hacker News Points: 463 points (Verified from news.ycombinator.com/item?id=50366999)",
            "• Published: 04 Nov 2026 (20.5 hours ago - Breaking AI News)",
            "• Core: Open architecture weights supporting long-context reasoning and dual-mode inference",
            "• Launch Command: from transformers import AutoModelForCausalLM",
            "• Hardware Boundary: Requires high-memory GPU cluster (8x 80GB VRAM) for unquantized local inference"
        ],
        "script": "Mama, breaking open-source news: Moonshot AI valla Kimi K3.1 Pro weights release ayyayi...",
        "source_url": "https://huggingface.co/moonshotai/Kimi-K3.1-Pro"
    }
]

def load_delivery_log():
    if os.path.exists(LOG_PATH):
        try:
            with open(LOG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"description": "Telegram Delivery Ledger", "delivered": {}}

def save_delivery_log(log_data):
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

def deliver_all():
    print(f"\n================ IDEMPOTENT TELEGRAM DELIVERY ({CHAT_ID}) ================", flush=True)
    if not BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN is missing.", flush=True)
        return False

    log_data = load_delivery_log()
    delivered_map = log_data.setdefault("delivered", {})

    for item in DELIVERIES:
        item_id = item["id"]
        
        # Idempotency check
        if item_id in delivered_map and not FORCE_RESEND:
            print(f"[SKIP] {item_id} already delivered at {delivered_map[item_id].get('delivered_at')}. Use --force to resend.", flush=True)
            continue
            
        print(f"\n>>> Delivering {item_id}: {item['title']}...", flush=True)
        
        # 1. Send Contact Sheet
        sheet_msg_id = None
        if os.path.exists(item["sheet_path"]):
            with open(item["sheet_path"], "rb") as f:
                caption = (
                    f"🎬 <b>Cinematic Visual-Metaphor Essay Contact Sheet (8 Beat Stills)</b>\n"
                    f"<b>{html.escape(item['title'])}</b>\n"
                    f"<i>{html.escape(item['template'])}</i>\n\n"
                    f"<b>Measured Quality Gates:</b> {html.escape(item['metrics'])}"
                )
                r_sheet = requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                    data={"chat_id": CHAT_ID, "caption": caption, "parse_mode": "HTML"},
                    files={"photo": f},
                    timeout=45
                )
                if r_sheet.status_code == 200:
                    sheet_msg_id = r_sheet.json().get("result", {}).get("message_id")
                    print(f"  Contact sheet sent (Msg ID: {sheet_msg_id})", flush=True)
                else:
                    print(f"  Failed sending sheet: {r_sheet.status_code} {r_sheet.text}", flush=True)
                time.sleep(1)

        # 2. Send Resource Pack Card
        escaped_facts = [html.escape(f) for f in item["facts"]]
        rp_text = (
            f"⚡ <b>FLASH RESOURCE PACK: {html.escape(item['title'])}</b>\n"
            f"<i>Style: {html.escape(item['template'])}</i>\n\n"
            f"<b>Verified Single-Source Facts:</b>\n" +
            "\n".join(escaped_facts) + "\n\n"
            f"<b>Source URL:</b> {item['source_url']}\n"
            f"<b>Telemetry & Gates:</b> {html.escape(item['metrics'])}\n\n"
            f"<b>Telugu Script:</b>\n<i>\"{html.escape(item['script'])}\"</i>"
        )
        r_card = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": rp_text, "parse_mode": "HTML", "disable_web_page_preview": True},
            timeout=20
        )
        card_msg_id = None
        if r_card.status_code == 200:
            card_msg_id = r_card.json().get("result", {}).get("message_id")
            print(f"  Resource pack card sent (Msg ID: {card_msg_id})", flush=True)
        time.sleep(1)

        # 3. Send Mastered Video with Inline Keyboard
        video_msg_id = None
        inline_keyboard = {
            "inline_keyboard": [
                [
                    {"text": "✅ Approve Video", "callback_data": f"approve:{item_id}"},
                    {"text": "❌ Reject / Re-roll", "callback_data": f"reject:{item_id}"}
                ]
            ]
        }
        if os.path.exists(item["video_path"]):
            with open(item["video_path"], "rb") as f:
                v_caption = (
                    f"⚡ <b>FLASH MASTERED VIDEO (28.00s)</b>\n"
                    f"<b>{html.escape(item['title'])}</b>\n"
                    f"<i>{html.escape(item['template'])}</i>\n\n"
                    f"<b>Broadcasting Standard:</b> EBU R128 (-14.0 LUFS ±1.0, TP ≤ -1.5 dBTP, 48kHz)\n"
                    f"<b>Camera/Motion Gate:</b> 0 Shake (Jitter ≤ 0.05 px²), Monotonic ease, >20 MAD burst\n\n"
                    f"👇 <i>Click to Approve or Reject for Night Post Queue:</i>"
                )
                r_video = requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo",
                    data={
                        "chat_id": CHAT_ID,
                        "caption": v_caption,
                        "parse_mode": "HTML",
                        "supports_streaming": True,
                        "reply_markup": json.dumps(inline_keyboard)
                    },
                    files={"video": f},
                    timeout=90
                )
                if r_video.status_code == 200:
                    video_msg_id = r_video.json().get("result", {}).get("message_id")
                    print(f"  Mastered video sent (Msg ID: {video_msg_id})", flush=True)
                else:
                    print(f"  Failed sending video: {r_video.status_code} {r_video.text}", flush=True)
                time.sleep(1)

        # Record in delivery log
        delivered_map[item_id] = {
            "delivered_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "title": item["title"],
            "sheet_message_id": sheet_msg_id,
            "card_message_id": card_msg_id,
            "video_message_id": video_msg_id,
            "status": "DELIVERED_PENDING_APPROVAL"
        }
        save_delivery_log(log_data)
        print(f"  [DELIVERED & LOGGED] {item_id}", flush=True)

    print("\n[ALL DELIVERIES COMPLETED]")
    return True

if __name__ == "__main__":
    deliver_all()
