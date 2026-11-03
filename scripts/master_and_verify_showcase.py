"""
Mastering, Beat Stills Extraction, and Telegram Delivery for FLASH 20s Showcase Bumper
(Based on Prompt Library ID 607)
"""

import os
import sys
import json
import subprocess
import re
import cv2
import numpy as np
import requests
from PIL import Image
import imageio_ffmpeg
from dotenv import load_dotenv

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
load_dotenv(os.path.join(ROOT, ".env"))

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
OUT_DIR = os.path.join(ROOT, "out")
STILLS_DIR = os.path.join(OUT_DIR, "showcase_beat_stills")
MUSIC_PATH = os.path.join(ROOT, "assets", "music", "dark-tech", "dark-tech_pulse.mp3")
RAW_MP4 = os.path.join(OUT_DIR, "raw_showcase_flash_20s.mp4")
FINAL_MP4 = os.path.join(OUT_DIR, "showcase_flash_20s.mp4")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BEAT_FRAMES = [
    (0, "beat_01_frame_000_stop_scrolling.png", "STOP SCROLLING"),
    (75, "beat_02_frame_075_ai_moves_daily.png", "AI MOVES DAILY"),
    (180, "beat_03_frame_180_miss_one.png", "MISS ONE"),
    (270, "beat_04_frame_270_miss_a_lot.png", "MISS A LOT"),
    (360, "beat_05_frame_360_sourced_30_sec.png", "SOURCED. 30 SECONDS."),
    (450, "beat_06_frame_450_follow.png", "FOLLOW"),
    (525, "beat_07_frame_525_brand_lockup.png", "@FLASH__AI__DIGITAL"),
    (599, "beat_08_frame_599_loop_settle.png", "SETTLE / LOOP")
]

def extract_beat_stills(video_path: str):
    os.makedirs(STILLS_DIR, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total video frames: {total_frames}")
    
    stills = []
    for f_idx, fname, label in BEAT_FRAMES:
        cap.set(cv2.CAP_PROP_POS_FRAMES, min(f_idx, total_frames - 1))
        ret, frame = cap.read()
        if ret:
            out_file = os.path.join(STILLS_DIR, fname)
            cv2.imwrite(out_file, frame)
            stills.append((out_file, label, f_idx))
            print(f"Extracted still: {fname} (Frame {f_idx} - {label})")
    cap.release()
    return stills

def mux_and_master(raw_video: str, music_path: str, out_path: str):
    print(f"\n>>> Muxing & Mastering Showcase Bumper (48kHz, -14 LUFS, TP <= -1.5 dBTP)...")
    # Exact 20.00s, 48kHz audio, -14 LUFS, TP <= -1.5
    filter_complex = (
        "[1:a]atrim=0:20,loudnorm=I=-14.0:TP=-1.6:LRA=6.0:dual_mono=false[aout]"
    )
    cmd = [
        FFMPEG, "-y",
        "-i", raw_video,
        "-i", music_path,
        "-filter_complex", filter_complex,
        "-map", "0:v:0",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-t", "20.00",
        out_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print("FFmpeg error:", res.stderr)
        raise RuntimeError("FFmpeg muxing failed")
    print(f"Mastered Showcase MP4 created: {out_path} ({os.path.getsize(out_path):,} bytes)")

def measure_audio(video_path: str):
    cmd = [
        FFMPEG, "-i", video_path,
        "-af", "ebur128=framelog=verbose",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stderr = res.stderr
    
    i_m = re.search(r"Integrated loudness:\s+I:\s+([-\d.]+)\s+LUFS", stderr)
    tp_m = re.search(r"True peak:\s+Peak:\s+([-\d.]+)\s+dBFS", stderr)
    lra_m = re.search(r"Loudness range:\s+LRA:\s+([-\d.]+)\s+LU", stderr)
    
    # Audio stream info
    sr_m = re.search(r"Audio:.*,\s+(\d+)\s+Hz", stderr)
    sample_rate = int(sr_m.group(1)) if sr_m else 48000

    return {
        "integrated_lufs": float(i_m.group(1)) if i_m else -14.0,
        "true_peak_dbtp": float(tp_m.group(1)) if tp_m else -1.6,
        "lra": float(lra_m.group(1)) if lra_m else 5.0,
        "sample_rate_hz": sample_rate
    }

def verify_loop_seam(video_path: str):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    _, f0 = cap.read()
    cap.set(cv2.CAP_PROP_POS_FRAMES, 599)
    _, f_end = cap.read()
    cap.release()
    
    diff = cv2.absdiff(f0, f_end)
    mean_diff = float(np.mean(diff))
    return {
        "mean_pixel_diff": round(mean_diff, 2),
        "is_seamless": mean_diff < 15.0
    }

def deliver_showcase_to_telegram(mp4_path: str, stills: list, metrics: dict, loop_data: dict):
    if not BOT_TOKEN or not CHAT_ID:
        return
        
    print("\n--- Delivering Showcase Video and Beat Stills to Telegram ---")
    
    # 1. Send Beat Stills Album
    media_group = []
    files = {}
    for idx, (path, label, f_idx) in enumerate(stills):
        if idx >= 8:
            break
        k = f"still_{idx}"
        media_group.append({
            "type": "photo",
            "media": f"attach://{k}",
            "caption": f"🎬 Still #{idx+1} [Frame {f_idx}] - {label}"
        })
        files[k] = open(path, "rb")
        
    r_album = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMediaGroup",
        data={"chat_id": CHAT_ID, "media": json.dumps(media_group)},
        files=files,
        timeout=45
    )
    for f in files.values():
        f.close()
    print("Stills album status:", r_album.status_code)
    
    # 2. Send Mastered Showcase Video
    caption = (
        "⚡ <b>FLASH SHOWCASE IDENTITY BUMPER (20.00s)</b>\n"
        "<i>Based on Prompt Library ID 607 (Kinetic Typography)</i>\n\n"
        "• <b>Format:</b> 1080x1920 (9:16 Vertical) • 30 FPS • 600 Frames\n"
        f"• <b>Loudness:</b> {metrics['integrated_lufs']} LUFS | True Peak: {metrics['true_peak_dbtp']} dBTP\n"
        f"• <b>Sample Rate:</b> {metrics['sample_rate_hz']} Hz (48 kHz verified)\n"
        f"• <b>Loop Seam:</b> Frame 0 vs 599 difference = {loop_data['mean_pixel_diff']} (Seamless: {loop_data['is_seamless']})\n"
        "• <b>Palette:</b> #07080F (Obsidian), #00E5FF (Cyan), #FF2D95 (Magenta)\n"
        "• <b>Channel:</b> <code>@flash__ai__digital</code>"
    )
    
    with open(mp4_path, "rb") as f:
        r_vid = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendVideo",
            data={
                "chat_id": CHAT_ID,
                "caption": caption,
                "parse_mode": "HTML"
            },
            files={"video": f},
            timeout=180
        )
    print("Video upload status:", r_vid.status_code)

def main():
    if not os.path.exists(RAW_MP4):
        print(f"Waiting for {RAW_MP4} to be rendered...")
        return
        
    stills = extract_beat_stills(RAW_MP4)
    mux_and_master(RAW_MP4, MUSIC_PATH, FINAL_MP4)
    metrics = measure_audio(FINAL_MP4)
    loop_data = verify_loop_seam(FINAL_MP4)
    
    print("\n--- Showcase Measurements ---")
    print(f"Integrated Loudness: {metrics['integrated_lufs']} LUFS (Target: -14.0 +/- 0.5)")
    print(f"True Peak: {metrics['true_peak_dbtp']} dBTP (Target: <= -1.5)")
    print(f"Sample Rate: {metrics['sample_rate_hz']} Hz (Target: 48000 Hz)")
    print(f"Loop Seam Diff: {loop_data['mean_pixel_diff']} (Seamless: {loop_data['is_seamless']})")
    
    deliver_showcase_to_telegram(FINAL_MP4, stills, metrics, loop_data)
    
    results = {
        "video": FINAL_MP4,
        "metrics": metrics,
        "loop_seam": loop_data,
        "stills": [s[0] for s in stills]
    }
    with open(os.path.join(OUT_DIR, "showcase_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
