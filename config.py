"""AI Auto-Reels Studio: Unified Configuration Management.
Central source of truth for branding, loudness, safe zones, templates, voice, and quality gates.
No hardcoded values are allowed in render or script logic.
"""
import os
import json
import requests
from dotenv import load_dotenv

# Load .env
load_dotenv(r"C:\Users\navee\OneDrive\Desktop\studio\.env")

# ---------------------------------------------------------
# BRANDING & SOCIAL CONFIG
# ---------------------------------------------------------
BRAND_NAME = os.getenv("BRAND_NAME", "FLASH")
BRAND_TAGLINE = os.getenv("BRAND_TAGLINE", "FLASH.Ai")

# Dynamically fetch Instagram handle via Graph API if available
def get_instagram_handle() -> str:
    cached_handle = os.getenv("IG_HANDLE")
    if cached_handle:
        return cached_handle.strip()
    
    token = os.getenv("IG_ACCESS_TOKEN", "").strip()
    if token:
        try:
            r = requests.get(
                "https://graph.instagram.com/v21.0/me",
                params={"fields": "username", "access_token": token},
                timeout=5
            )
            if r.status_code == 200:
                uname = r.json().get("username")
                if uname:
                    return f"@{uname}"
        except Exception:
            pass
    return "@flash__ai__digital"

IG_HANDLE = get_instagram_handle()

# Active platforms: currently 'instagram'
_platforms_str = os.getenv("PLATFORMS", "instagram")
PLATFORMS = [p.strip().lower() for p in _platforms_str.split(",") if p.strip()]

# ---------------------------------------------------------
# AUDIO & LOUDNESS CONFIG (EBU R128 Standards)
# ---------------------------------------------------------
AUDIO_CONFIG = {
    "target_lufs": -14.0,           # EBU R128 integrated loudness target
    "lufs_tolerance": 1.5,          # Broadcast dynamic tolerance: -12.5 to -15.5 LUFS
    "max_true_peak": -1.5,          # dBTP ceiling to prevent inter-sample distortion
    "music_ducking_min": 22.0,      # Min dB attenuation under voice
    "music_ducking_max": 26.0,      # Max dB attenuation under voice
    "music_ducking_target": 24.0,   # Default ducking attenuation
    "max_silence_sec": 0.6,         # Max contiguous dead air allowed
    "audio_sample_rate": 44100
}

# ---------------------------------------------------------
# VIDEO SPECIFICATIONS & SAFE ZONES
# ---------------------------------------------------------
VIDEO_CONFIG = {
    "width": 1080,
    "height": 1920,
    "fps": 30,
    "min_duration": 20.0,
    "max_duration": 35.0,
    "safe_zone_top": 250,           # Top 250px clear of primary elements
    "safe_zone_bottom": 380,        # Bottom 380px clear except captions
    "min_font_size": 36,            # Minimum text size for mobile readability
    "max_empty_ratio": 0.35,        # Maximum allowable flat background fraction
    "preview_width": 540,
    "preview_height": 960,
    "preview_fps": 15
}

# ---------------------------------------------------------
# VOICE & TTS CONFIG
# ---------------------------------------------------------
VOICE_CONFIG = {
    "engine_order": ["elevenlabs", "gemini", "edge_tts"],
    "elevenlabs": {
        "voice_id": os.getenv("ELEVEN_VOICE_ID", "7qBNUtXRGP0jPi0H4r8k"),
        "model_id": "eleven_multilingual_v2",
        "speed": 0.95,
        "stability": 0.60,
        "similarity_boost": 0.30
    },
    "gemini": {
        "model": "gemini-2.5-flash-preview-tts",
        "prompt": "Read the following script aloud with a warm, smiling, friendly Indian customer-support Tenglish tone."
    },
    "edge_tts": {
        "voice": "en-IN-PrabhatNeural",
        "alt_voice": "en-IN-NeerjaNeural",
        "rate": "+0%"
    }
}

# ---------------------------------------------------------
# TEMPLATE WEIGHTS (Equal distribution, non-repeating)
# ---------------------------------------------------------
TEMPLATE_WEIGHTS = {
    "terminal_hacker": 1.0,
    "apple_keynote": 1.0,
    "breaking_news": 1.0,
    "neon_cyberpunk": 1.0,
    "blueprint_cad": 1.0,
    "brutalist_bold": 1.0,
    "glassmorphism": 1.0,
    "cinematic_letterbox": 1.0
}

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
BASE_DIR = r"C:\Users\navee\OneDrive\Desktop\studio"
OUT_DIR = os.path.join(BASE_DIR, "out")
RUNS_DIR = os.path.join(BASE_DIR, "runs")
QUEUE_DIR = os.path.join(BASE_DIR, "queue")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")
LEXICON_FILE = os.path.join(CONFIG_DIR, "lexicon.json")

for d in [OUT_DIR, RUNS_DIR, QUEUE_DIR, CONFIG_DIR, ASSETS_DIR]:
    os.makedirs(d, exist_ok=True)
