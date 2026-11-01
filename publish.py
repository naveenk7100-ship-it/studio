"""Auto-post to YouTube Shorts + Instagram Reels (official APIs, zero/low cost).

Supports:
- YouTube Shorts via Google YouTube Data API v3 (resumable upload)
- Instagram Reels via Instagram Login API (graph.instagram.com) & Meta Graph API (graph.facebook.com)
- Public video hosting via Cloudinary with automatic tmpfiles.org zero-config fallback
"""
import os
import sys
import time
import json
import hashlib
import requests
from pathlib import Path

# Ensure stdout handles utf-8 safely on Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def get_youtube_service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    cred = Credentials(
        None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )
    return build("youtube", "v3", credentials=cred)


def youtube(path, title, desc, tags=None):
    """Upload vertical video to YouTube Shorts using resumable upload."""
    from googleapiclient.http import MediaFileUpload

    tags = tags or ["Shorts", "AI", "Tech", "Coding"]
    yt = get_youtube_service()

    t = title if "#shorts" in title.lower() else (title[:90].strip() + " #Shorts")
    body = {
        "snippet": {
            "title": t[:100],
            "description": (desc.strip() + "\n\n#Shorts #Tech #AI")[:5000],
            "tags": tags[:15],
            "categoryId": "28"  # Science & Technology
        },
        "status": {
            "privacyStatus": os.getenv("YT_PRIVACY", "public"),
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(path, mimetype="video/mp4", chunksize=1024 * 1024 * 4, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)

    print(f"[YOUTUBE] Uploading {path} as '{t}'...")
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"  [YOUTUBE] Progress: {int(status.progress() * 100)}%")

    video_id = resp.get("id")
    url = f"https://youtube.com/shorts/{video_id}"
    print(f"[YOUTUBE SUCCESS] Published: {url}")
    return url


def _upload_tmpfiles(path):
    """Upload video to tmpfiles.org for a free temporary direct download link."""
    print("[IG HOST] Uploading video to tmpfiles.org...")
    with open(path, "rb") as f:
        r = requests.post("https://tmpfiles.org/api/v1/upload", files={"file": f}, timeout=60)
    r.raise_for_status()
    data = r.json()
    raw_url = data["data"]["url"]
    direct_url = raw_url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
    print(f"[IG HOST] Video hosted temporarily at: {direct_url}")
    return direct_url


def _upload_cloudinary(path):
    """Upload video to Cloudinary free tier for an HTTPS secure URL."""
    c_url = os.environ.get("CLOUDINARY_URL", "").replace("cloudinary://", "")
    cred, cloud = c_url.split("@")
    key, sec = cred.split(":")
    ts = str(int(time.time()))
    sig = hashlib.sha1(f"timestamp={ts}{sec}".encode()).hexdigest()
    with open(path, "rb") as f:
        r = requests.post(
            f"https://api.cloudinary.com/v1_1/{cloud}/video/upload",
            data={"api_key": key, "timestamp": ts, "signature": sig},
            files={"file": f},
            timeout=180
        )
    r.raise_for_status()
    secure_url = r.json()["secure_url"]
    print(f"[IG HOST] Video hosted on Cloudinary: {secure_url}")
    return secure_url


def get_public_video_url(path):
    """Get a public HTTPS video URL for Instagram media crawler."""
    if os.getenv("CLOUDINARY_URL"):
        try:
            return _upload_cloudinary(path)
        except Exception as e:
            print(f"[WARNING] Cloudinary upload failed ({e}), falling back to tmpfiles.org")
    return _upload_tmpfiles(path)


def instagram(path, caption):
    """Upload vertical reel to Instagram via Instagram Login API or Meta Graph API."""
    uid = os.environ.get("IG_USER_ID", "").strip()
    tok = os.environ.get("IG_ACCESS_TOKEN", "").strip()

    if not uid or not tok:
        raise ValueError("Missing IG_USER_ID or IG_ACCESS_TOKEN in environment")

    # Select base API URL based on token type
    if tok.startswith("IGAA"):
        api_base = "https://graph.instagram.com/v21.0"
        print("[INSTAGRAM] Using Instagram Login API (graph.instagram.com)")
    else:
        api_base = "https://graph.facebook.com/v21.0"
        print("[INSTAGRAM] Using Facebook Graph API (graph.facebook.com)")

    # 1. Host video publicly
    video_url = get_public_video_url(path)

    # 2. Create Instagram Media Container
    print(f"[INSTAGRAM] Creating Reels media container for user {uid}...")
    create_url = f"{api_base}/{uid}/media"
    payload = {
        "media_type": "REELS",
        "video_url": video_url,
        "caption": caption,
        "share_to_feed": "true",
        "access_token": tok
    }

    res = requests.post(create_url, data=payload, timeout=60)
    if res.status_code != 200:
        raise RuntimeError(f"Failed to create Instagram container: {res.text}")

    container_id = res.json().get("id")
    print(f"[INSTAGRAM] Media container created: ID {container_id}")

    # 3. Poll container processing status until FINISHED
    print("[INSTAGRAM] Waiting for video processing...")
    status_url = f"{api_base}/{container_id}"
    ready = False
    for attempt in range(45):
        time.sleep(6)
        s_res = requests.get(status_url, params={"fields": "status_code", "access_token": tok}, timeout=30)
        status_data = s_res.json()
        status_code = status_data.get("status_code")
        print(f"  [INSTAGRAM] Processing status ({attempt+1}/45): {status_code}")

        if status_code == "FINISHED":
            ready = True
            break
        elif status_code == "ERROR":
            raise RuntimeError(f"Instagram media processing failed: {status_data}")

    if not ready:
        raise TimeoutError("Timed out waiting for Instagram to process video container")

    # 4. Publish Reels Container
    print(f"[INSTAGRAM] Publishing media container {container_id}...")
    publish_url = f"{api_base}/{uid}/media_publish"
    p_res = requests.post(publish_url, data={"creation_id": container_id, "access_token": tok}, timeout=60)
    if p_res.status_code != 200:
        raise RuntimeError(f"Failed to publish Instagram reel: {p_res.text}")

    post_id = p_res.json().get("id")
    print(f"[INSTAGRAM SUCCESS] Reel published! Post ID: {post_id}")
    return post_id
