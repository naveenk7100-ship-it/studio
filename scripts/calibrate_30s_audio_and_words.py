"""
Calibrate 30s Audio Duration and Timestamps to strictly fit 25-30s gate.
Speed adjustment preserves pitch via atempo filter.
Word timestamps are scaled by 1/speed to maintain 1:1 sync precision.
Mastered to 48kHz, -14.0 LUFS, TP <= -1.5 dBTP.
"""

import os
import sys
import json
import subprocess
import imageio_ffmpeg

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
CACHE_DIR = os.path.join(ROOT, "cache")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

TARGET_DURATION = 28.0 # seconds (strictly between 25 and 30s)

ITEMS = [
    {
        "id": "vllm_30s",
        "audio_in": os.path.join(CACHE_DIR, "voice_30s_vllm.mp3"),
        "words_in": os.path.join(CACHE_DIR, "words_30s_vllm.json"),
        "audio_out": os.path.join(CACHE_DIR, "voice_28s_vllm.mp3"),
        "words_out": os.path.join(CACHE_DIR, "words_28s_vllm.json"),
    },
    {
        "id": "claude_30s",
        "audio_in": os.path.join(CACHE_DIR, "voice_30s_claude.mp3"),
        "words_in": os.path.join(CACHE_DIR, "words_30s_claude.json"),
        "audio_out": os.path.join(CACHE_DIR, "voice_28s_claude.mp3"),
        "words_out": os.path.join(CACHE_DIR, "words_28s_claude.json"),
    },
    {
        "id": "mcp_30s",
        "audio_in": os.path.join(CACHE_DIR, "voice_30s_mcp.mp3"),
        "words_in": os.path.join(CACHE_DIR, "words_30s_mcp.json"),
        "audio_out": os.path.join(CACHE_DIR, "voice_28s_mcp.mp3"),
        "words_out": os.path.join(CACHE_DIR, "words_28s_mcp.json"),
    }
]

def get_duration(path: str) -> float:
    cmd = [FFMPEG, "-i", path]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True)
    import re
    m = re.search(r"Duration:\s+(\d+):(\d+):([\d.]+)", res.stderr)
    if m:
        h, mi, s = m.groups()
        return int(h) * 3600 + int(mi) * 60 + float(s)
    return 30.0

def calibrate():
    print("\n=======================================================")
    print("CALIBRATING AUDIO TO STRICT 25-30s WINDOW (Target 28.0s)")
    print("=======================================================")
    
    for it in ITEMS:
        orig_dur = get_duration(it["audio_in"])
        speed = round(orig_dur / TARGET_DURATION, 3)
        print(f"\n>>> {it['id']}: Original {orig_dur:.2f}s -> Target {TARGET_DURATION}s (Speed Factor: {speed}x)")
        
        # Apply atempo and loudnorm
        filter_str = f"atempo={speed},loudnorm=I=-14.0:TP=-1.6:LRA=6.0"
        cmd = [
            FFMPEG, "-y",
            "-i", it["audio_in"],
            "-af", filter_str,
            "-ar", "48000",
            "-b:a", "192k",
            it["audio_out"]
        ]
        subprocess.run(cmd, check=True)
        final_dur = get_duration(it["audio_out"])
        print(f"Calibrated audio generated: {it['audio_out']} ({final_dur:.2f}s, 48kHz)")
        
        # Scale word timestamps
        with open(it["words_in"], "r", encoding="utf-8") as f:
            words = json.load(f)
            
        scaled_words = []
        for w, s, e in words:
            scaled_words.append([w, round(s / speed, 3), round(e / speed, 3)])
            
        with open(it["words_out"], "w", encoding="utf-8") as f:
            json.dump(scaled_words, f, indent=2)
            
        print(f"Scaled word timestamps saved: {it['words_out']} ({len(scaled_words)} words, last word end {scaled_words[-1][2]}s)")

if __name__ == "__main__":
    calibrate()
