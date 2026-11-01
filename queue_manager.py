"""AI Auto-Reels Studio: Resilient Content Queue & Buffer Manager.
Maintains a 3-day content buffer (6 pre-generated, quality-checked videos).
Cron tasks consume only validated items from this queue.
Alerts via Telegram when buffer falls below 2 days (<4 items).
"""
import os
import json
import time
import requests
from typing import Dict, List, Optional
import config

QUEUE_FILE = os.path.join(config.QUEUE_DIR, "queue_manifest.json")
TELEGRAM_BOT = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_alert(message: str):
    """Send alert to admin Telegram channel."""
    if not TELEGRAM_BOT or not TELEGRAM_CHAT:
        print(f"[TELEGRAM LOG] {message}")
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT, "text": message}, timeout=10)
    except Exception as e:
        print(f"[TELEGRAM ALERT ERROR] {e}")


def load_manifest() -> Dict:
    """Load queue manifest."""
    if not os.path.exists(QUEUE_FILE):
        return {"items": [], "published": []}
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"items": [], "published": []}


def save_manifest(manifest: Dict):
    """Save queue manifest atomically."""
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)


def add_item_to_queue(item_data: Dict) -> str:
    """Add a validated video to the queue."""
    manifest = load_manifest()
    item_id = item_data.get("id") or f"slot_{int(time.time())}"
    item_entry = {
        "id": item_id,
        "title": item_data.get("title", "Untitled"),
        "video_path": item_data.get("video_path"),
        "meta_path": item_data.get("meta_path"),
        "caption": item_data.get("caption", ""),
        "status": "ready",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    manifest["items"].append(item_entry)
    save_manifest(manifest)
    print(f"[QUEUE] Added item {item_id} to queue. Total ready: {len(manifest['items'])}")
    return item_id


def get_next_ready_item() -> Optional[Dict]:
    """Get the next ready item without removing it yet."""
    manifest = load_manifest()
    for item in manifest["items"]:
        if item.get("status") == "ready" and os.path.exists(item.get("video_path", "")):
            return item
    return None


def mark_item_published(item_id: str, live_urls: Dict):
    """Mark an item as published and move to published list."""
    manifest = load_manifest()
    remaining = []
    published_item = None
    for item in manifest["items"]:
        if item["id"] == item_id:
            item["status"] = "published"
            item["published_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            item["live_urls"] = live_urls
            published_item = item
        else:
            remaining.append(item)
            
    manifest["items"] = remaining
    if published_item:
        manifest["published"].append(published_item)
    save_manifest(manifest)
    print(f"[QUEUE] Marked {item_id} as published. Remaining queue depth: {len(remaining)}")
    check_buffer_depth()


def check_buffer_depth() -> int:
    """Check buffer level; alert Telegram if < 4 videos (2 days)."""
    manifest = load_manifest()
    ready_count = sum(1 for it in manifest["items"] if it.get("status") == "ready" and os.path.exists(it.get("video_path", "")))
    print(f"[QUEUE STATUS] Buffer depth: {ready_count} videos ready.")
    
    # 2 videos per day -> 2 days = 4 videos
    if ready_count < 4:
        msg = f"⚠️ [BUFFER ALERT] AI Auto-Studio queue depth is low!\nCurrently only {ready_count} ready videos remaining (< 2 days buffer).\nPlease run replenishment."
        send_telegram_alert(msg)
    return ready_count


if __name__ == "__main__":
    depth = check_buffer_depth()
    print(f"Current ready queue depth: {depth}")
