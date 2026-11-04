"""
Calibrate 30s Audio Duration and Timestamps to strictly fit 25-30s gate (Target 28.00s = 840 frames @ 30 fps).
Speed adjustment preserves pitch via atempo filter.
Word timestamps are scaled by 1/speed to maintain 1:1 sync precision.
"""

import os
import sys
import json
import re
import subprocess
import imageio_ffmpeg

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
CACHE_DIR = os.path.join(ROOT, "cache")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

TARGET_DURATION = 28.0 # seconds (strictly between 25 and 30s)

ITEMS = [
    {
        "id": "reel_new_1_superagent",
        "audio_in": os.path.join(CACHE_DIR, "voice_superagent.mp3"),
        "words_in": os.path.join(CACHE_DIR, "words_superagent.json"),
        "audio_out": os.path.join(CACHE_DIR, "voice_28s_superagent.mp3"),
        "words_out": os.path.join(CACHE_DIR, "words_28s_superagent.json"),
    },
    {
        "id": "reel_new_2_ollama",
        "audio_in": os.path.join(CACHE_DIR, "voice_ollama.mp3"),
        "words_in": os.path.join(CACHE_DIR, "words_ollama.json"),
        "audio_out": os.path.join(CACHE_DIR, "voice_28s_ollama.mp3"),
        "words_out": os.path.join(CACHE_DIR, "words_28s_ollama.json"),
    },
    {
        "id": "reel_new_3_qwen_news",
        "audio_in": os.path.join(CACHE_DIR, "voice_qwen_news.mp3"),
        "words_in": os.path.join(CACHE_DIR, "words_qwen_news.json"),
        "audio_out": os.path.join(CACHE_DIR, "voice_28s_qwen_news.mp3"),
        "words_out": os.path.join(CACHE_DIR, "words_28s_qwen_news.json"),
    }
]

def get_duration(path: str) -> float:
    cmd = [FFMPEG, "-i", path]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
    m = re.search(r"Duration:\s+(\d+):(\d+):([\d.]+)", res.stderr)
    if m:
        h, mi, s = m.groups()
        return int(h) * 3600 + int(mi) * 60 + float(s)
    return 30.0

def calibrate():
    print("================ CALIBRATING AUDIO TO STRICT 28.00s WINDOW ================")
    for it in ITEMS:
        orig_dur = get_duration(it["audio_in"])
        speed = orig_dur / TARGET_DURATION
        print(f"\nProcessing {it['id']}: Original {orig_dur:.2f}s -> Target {TARGET_DURATION}s (Speed Factor: {speed:.3f})")
        
        # Audio atempo filter
        cmd = [
            FFMPEG, "-y",
            "-i", it["audio_in"],
            "-filter:a", f"atempo={speed}",
            "-ar", "48000",
            it["audio_out"]
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        final_dur = get_duration(it["audio_out"])
        
        # Scale word timestamps
        with open(it["words_in"], "r", encoding="utf-8") as f:
            words = json.load(f)
            
        scaled_words = []
        for w in words:
            # Handle both formats: [word, start, end] or dict
            if isinstance(w, list):
                scaled_words.append([w[0], round(w[1] / speed, 3), round(w[2] / speed, 3)])
            elif isinstance(w, dict):
                scaled_words.append([w.get("word", ""), round(w.get("start", 0) / speed, 3), round(w.get("end", 0) / speed, 3)])
                
        with open(it["words_out"], "w", encoding="utf-8") as f:
            json.dump(scaled_words, f, indent=2)
            
        print(f"  [SAVED] {it['audio_out']} ({final_dur:.2f}s) | Scaled {len(scaled_words)} words to {it['words_out']}")

if __name__ == "__main__":
    calibrate()
