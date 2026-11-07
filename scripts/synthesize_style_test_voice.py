"""
Synthesize 12-second style test voice track for Anatomy topic with exact word timestamps.
"""
import os
import sys
import json
import subprocess
import imageio_ffmpeg
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
load_dotenv(os.path.join(ROOT, ".env"))
sys.path.insert(0, ROOT)
import tts

CACHE_DIR = os.path.join(ROOT, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

STYLE_TEST_SCRIPT = "Mama, technical idea explain cheyadaniki machine blueprint kavala? Idi Anatomy Claude skill. Single line idea iste working isometric diagrams SVG and 3D lo build chestundi."
TARGET_SPEECH_END = 10.20  # Ends at 10.2s, 10.5-12.0s is end card

raw_mp3 = os.path.join(CACHE_DIR, "voice_raw_style_test_12s.mp3")
calibrated_mp3 = os.path.join(CACHE_DIR, "voice_final_style_test_12s.mp3")
words_json = os.path.join(CACHE_DIR, "words_final_style_test_12s.json")

print(f"Synthesizing 12s voice: \"{STYLE_TEST_SCRIPT}\"")

words_raw = tts.make_voice(
    display_text=STYLE_TEST_SCRIPT,
    path=raw_mp3,
    voice_override="Sadachbia"
)

dur_raw = tts.get_audio_duration(raw_mp3)
print(f"Raw duration: {dur_raw:.2f}s")

target_active = TARGET_SPEECH_END - 0.15
speed = dur_raw / target_active
speed = max(0.90, min(1.25, speed))
print(f"Speed ratio: {speed:.4f}x")

cmd = [
    FFMPEG, "-y",
    "-i", raw_mp3,
    "-filter_complex",
    f"[0:a]atempo={speed:.4f},adelay=150|150,apad=pad_dur=3.0[a]",
    "-map", "[a]",
    "-c:a", "mp3",
    "-b:a", "192k",
    "-ar", "48000",
    "-t", "12.00",
    calibrated_mp3
]
subprocess.run(cmd, check=True)

# Build words
text_words = [w.strip() for w in STYLE_TEST_SCRIPT.split()]
scaled_words = []
if words_raw and isinstance(words_raw, list):
    for idx, item in enumerate(words_raw):
        w_text = item.get("word", "") if isinstance(item, dict) else (item[0] if len(item) > 0 else "")
        w_start = item.get("start", 0.0) if isinstance(item, dict) else (item[1] if len(item) > 1 else 0.0)
        w_end = item.get("end", 0.0) if isinstance(item, dict) else (item[2] if len(item) > 2 else 0.0)
        
        cal_start = round(0.15 + (w_start / speed), 3)
        cal_end = round(0.15 + (w_end / speed), 3)
        display_word = text_words[idx] if idx < len(text_words) else w_text
        scaled_words.append({
            "word": display_word,
            "start": cal_start,
            "end": min(cal_end, TARGET_SPEECH_END)
        })
else:
    step = (TARGET_SPEECH_END - 0.15) / len(text_words)
    for idx, w in enumerate(text_words):
        st = round(0.15 + idx * step, 3)
        et = round(st + step * 0.85, 3)
        scaled_words.append({
            "word": w,
            "start": st,
            "end": et
        })

with open(words_json, "w", encoding="utf-8") as f:
    json.dump(scaled_words, f, indent=2)

print(f"Saved {len(scaled_words)} words to {words_json}")
print(f"Voice calibrated to {calibrated_mp3} ({tts.get_audio_duration(calibrated_mp3):.2f}s)")
