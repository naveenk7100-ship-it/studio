"""
FLASH Content OS - Telegram Morning Briefing Engine
Dispatches the Top 8 Intelligence candidates to Telegram with interactive buttons:
- Pick: marks for production
- Skip: dismisses candidate
- Make video: immediately triggers resource pack creation & queueing
Auto-picks top 2 candidates if no response is received.
"""

import os
import sys
import json
import requests
import datetime as dt
from dotenv import load_dotenv
from intelligence import collect_and_rank_intelligence

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
load_dotenv(os.path.join(ROOT, ".env"))

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BRIEFING_STATE_PATH = os.path.join(ROOT, "queue", "briefing_state.json")

def send_telegram_briefing(top_candidates: list = None):
    if not BOT_TOKEN or not CHAT_ID:
        print("[BRIEFING] ERROR: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured.")
        return False

    if not top_candidates:
        top_candidates = collect_and_rank_intelligence()

    today_str = dt.date.today().strftime("%d %b %Y")
    
    # 1. Send Main Briefing Header Message
    header_text = (
        f"⚡ <b>FLASH DAILY INTELLIGENCE BRIEFING</b> • {today_str}\n"
        f"<i>Scanned from GitHub, Hacker News & Official AI Blogs</i>\n\n"
        f"Top 8 builder-relevant topics scored for impact, freshness & relevance.\n"
        f"💡 <i>Click <b>[Make Video]</b> or <b>[Pick]</b>. Auto-picks top 2 if unreviewed.</i>"
    )
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    res = requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": header_text,
        "parse_mode": "HTML"
    }, timeout=20)
    print(f"[BRIEFING] Header sent: status {res.status_code}")

    # 2. Send Each Candidate with Actions
    briefing_state = {
        "date": dt.date.today().isoformat(),
        "candidates": top_candidates,
        "picked": [],
        "skipped": [],
        "auto_picked": []
    }

    for idx, cand in enumerate(top_candidates, 1):
        cid = cand["id"]
        score = cand["score"]
        title = cand["title"]
        src = cand["source_type"]
        why = cand["why_it_matters"]
        link = cand["source_url"]
        p_date = cand.get("published_date", "")

        msg = (
            f"<b>#{idx} [{score}/100] {title}</b>\n"
            f"🏷️ <i>{src} • {p_date}</i>\n\n"
            f"📌 <b>Why It Matters:</b> {why}\n"
            f"🔗 <a href='{link}'>{link}</a>"
        )

        inline_keyboard = {
            "inline_keyboard": [
                [
                    {"text": "🎬 Make Video", "callback_data": f"make:{cid}"},
                    {"text": "⭐ Pick", "callback_data": f"pick:{cid}"},
                    {"text": "⏭️ Skip", "callback_data": f"skip:{cid}"}
                ]
            ]
        }

        r = requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "HTML",
            "reply_markup": inline_keyboard,
            "disable_web_page_preview": False
        }, timeout=20)
        print(f"[BRIEFING] Candidate #{idx} sent: status {r.status_code}")

    # Save briefing state
    os.makedirs(os.path.dirname(BRIEFING_STATE_PATH), exist_ok=True)
    with open(BRIEFING_STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(briefing_state, f, indent=2)

    return True

def auto_pick_top_two(briefing_state_path: str = BRIEFING_STATE_PATH):
    """Fallback mechanism: auto-picks top 2 candidates if user has not picked."""
    if not os.path.exists(briefing_state_path):
        return []

    with open(briefing_state_path, "r", encoding="utf-8") as f:
        state = json.load(f)

    picked = state.get("picked", [])
    if len(picked) >= 2:
        print(f"[BRIEFING] User already picked {len(picked)} candidates: {picked}")
        return picked

    candidates = state.get("candidates", [])
    needed = 2 - len(picked)
    auto_picked = []
    
    for c in candidates:
        if c["id"] not in picked and c["id"] not in state.get("skipped", []):
            auto_picked.append(c["id"])
            if len(auto_picked) == needed:
                break

    state["auto_picked"] = auto_picked
    state["picked"].extend(auto_picked)

    with open(briefing_state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

    print(f"[BRIEFING] Auto-picked {len(auto_picked)} candidates: {auto_picked}")
    
    # Notify user on Telegram
    if BOT_TOKEN and CHAT_ID and auto_picked:
        msg = f"⚡ <b>FLASH AUTO-PICK</b>\nAuto-selected top {len(auto_picked)} topics for today's production:\n"
        for ap in auto_picked:
            title = next((c["title"] for c in candidates if c["id"] == ap), ap)
            msg += f"• <b>{title}</b>\n"
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={
            "chat_id": CHAT_ID,
            "text": msg,
            "parse_mode": "HTML"
        }, timeout=15)

    return state["picked"]

if __name__ == "__main__":
    send_telegram_briefing()
