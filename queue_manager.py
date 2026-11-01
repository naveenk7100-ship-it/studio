"""AI Auto-Reels Studio: Resilient Content Queue & Human Approval Manager.
Maintains a 3-day content buffer (6 pre-generated, quality-checked videos).
Sends finished videos to Telegram with inline approval buttons: [Approve], [Reject], [Regenerate].
When APPROVAL_REQUIRED=True, posts ONLY approved videos at slot times (12:30 PM & 8:30 PM IST).
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
    """Send text alert to admin Telegram channel."""
    if not TELEGRAM_BOT or not TELEGRAM_CHAT:
        print(f"[TELEGRAM LOG] {message}")
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendMessage"
        requests.post(url, json={"chat_id": TELEGRAM_CHAT, "text": message}, timeout=10)
    except Exception as e:
        print(f"[TELEGRAM ALERT ERROR] {e}")


def send_telegram_review(video_path: str, contact_sheet_path: str, caption: str, item_id: str):
    """Send finished video and contact sheet to Telegram with inline approval buttons."""
    if not TELEGRAM_BOT or not TELEGRAM_CHAT:
        print(f"[TELEGRAM LOG] Review for {item_id}: {video_path}")
        return

    # Inline Keyboard for Human Approval
    inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": "✅ Approve", "callback_data": f"approve:{item_id}"},
                {"text": "❌ Reject", "callback_data": f"reject:{item_id}"},
                {"text": "🔄 Regenerate", "callback_data": f"regen:{item_id}"}
            ]
        ]
    }

    # 1. Send Contact Sheet First
    if contact_sheet_path and os.path.exists(contact_sheet_path):
        try:
            with open(contact_sheet_path, "rb") as f:
                requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendPhoto",
                    data={"chat_id": TELEGRAM_CHAT, "caption": f"🎬 Review Sheet: {item_id}\n{caption[:200]}"},
                    files={"photo": f},
                    timeout=20
                )
        except Exception as e:
            print(f"[TELEGRAM PHOTO NOTICE] {e}")

    # 2. Send Video with Inline Approval Buttons
    if video_path and os.path.exists(video_path):
        try:
            with open(video_path, "rb") as f:
                r = requests.post(
                    f"https://api.telegram.org/bot{TELEGRAM_BOT}/sendVideo",
                    data={
                        "chat_id": TELEGRAM_CHAT,
                        "caption": f"⚡ Video Ready for Review: {item_id}\nPlease approve for 12:30 PM / 8:30 PM IST slot:",
                        "reply_markup": json.dumps(inline_keyboard)
                    },
                    files={"video": f},
                    timeout=60
                )
            if r.status_code == 200:
                print(f"[TELEGRAM] Sent review video with approval buttons for {item_id}")
            else:
                print(f"[TELEGRAM NOTICE] SendVideo returned {r.status_code}: {r.text[:120]}")
        except Exception as e:
            print(f"[TELEGRAM VIDEO NOTICE] {e}")


def sync_telegram_approvals():
    """Poll Telegram for callback query button clicks (Approve, Reject, Regenerate)."""
    if not TELEGRAM_BOT:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT}/getUpdates"
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return
        data = r.json()
        manifest = load_manifest()
        modified = False

        for update in data.get("result", []):
            cb = update.get("callback_query")
            if not cb:
                continue
            cb_id = cb.get("id")
            cb_data = cb.get("data", "")
            
            action = None
            target_id = None
            if cb_data.startswith("approve:"):
                action = "approved"
                target_id = cb_data.replace("approve:", "")
            elif cb_data.startswith("reject:"):
                action = "rejected"
                target_id = cb_data.replace("reject:", "")
            elif cb_data.startswith("regen:"):
                action = "regenerate"
                target_id = cb_data.replace("regen:", "")

            if action and target_id:
                for item in manifest["items"]:
                    if item["id"] == target_id and item.get("status") != action:
                        item["status"] = action
                        item["status_updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        modified = True
                        print(f"[APPROVAL] Item {target_id} updated to status: '{action}' by user on Telegram.")
                        # Acknowledge callback to stop loading spinner
                        try:
                            requests.post(
                                f"https://api.telegram.org/bot{TELEGRAM_BOT}/answerCallbackQuery",
                                json={"callback_query_id": cb_id, "text": f"Marked as {action.upper()}!"},
                                timeout=5
                            )
                        except Exception:
                            pass

        if modified:
            save_manifest(manifest)
    except Exception as e:
        print(f"[APPROVAL SYNC NOTICE] {e}")


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
    """Add a validated video to the queue and dispatch for human review."""
    manifest = load_manifest()
    item_id = item_data.get("id") or f"slot_{int(time.time())}"
    item_entry = {
        "id": item_id,
        "title": item_data.get("title", "Untitled"),
        "video_path": item_data.get("video_path"),
        "contact_sheet": item_data.get("contact_sheet"),
        "meta_path": item_data.get("meta_path"),
        "caption": item_data.get("caption", ""),
        "status": "pending_approval" if config.APPROVAL_REQUIRED else "ready",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    manifest["items"].append(item_entry)
    save_manifest(manifest)
    print(f"[QUEUE] Added item {item_id} to queue (Status: {item_entry['status']}).")

    # Send review message to Telegram with Approve / Reject / Regenerate buttons
    send_telegram_review(
        item_entry.get("video_path"),
        item_entry.get("contact_sheet"),
        item_entry.get("caption"),
        item_id
    )

    return item_id


def get_next_publishable_item() -> Optional[Dict]:
    """Get the next item ready for publishing, enforcing human approval if configured."""
    sync_telegram_approvals()
    manifest = load_manifest()
    
    for item in manifest["items"]:
        if not os.path.exists(item.get("video_path", "")):
            continue
        if config.APPROVAL_REQUIRED:
            if item.get("status") == "approved":
                return item
        else:
            if item.get("status") in ["ready", "approved"]:
                return item
                
    if config.APPROVAL_REQUIRED:
        print("[APPROVAL GATE] No approved videos found in queue. Skipping slot (APPROVAL_REQUIRED=True).")
    return None


def mark_item_published(item_id: str, live_urls: Dict):
    """Mark an item as published and move to published archive."""
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
    ready_count = sum(1 for it in manifest["items"] if it.get("status") in ["ready", "approved", "pending_approval"] and os.path.exists(it.get("video_path", "")))
    print(f"[QUEUE STATUS] Buffer depth: {ready_count} videos in queue.")
    
    if ready_count < 4:
        msg = f"⚠️ [BUFFER ALERT] FLASH (FLASH.Ai) queue depth is low!\nCurrently only {ready_count} videos remaining in queue (< 2 days buffer).\nPlease run replenishment."
        send_telegram_alert(msg)
    return ready_count


if __name__ == "__main__":
    sync_telegram_approvals()
    depth = check_buffer_depth()
    print(f"Current queue buffer: {depth} items")
