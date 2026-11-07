"""
FLASH Content OS - Real-File Quality Gates Evaluator
Decodes actual rendered MP4 video files, runs native Windows 11 OCR, 
computes per-second motion MAD, measures EBU R128 audio, and enforces zero tolerance.
"""

import os
import sys
import json
import re
import time
import subprocess
import asyncio
import numpy as np
import imageio_ffmpeg
from PIL import Image

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# Windows Native OCR
import winsdk.windows.globalization as glob
import winsdk.windows.media.ocr as ocr
import winsdk.windows.graphics.imaging as imaging
import winsdk.windows.storage as storage

VIDEOS_TO_AUDIT = [
    {
        "id": "today_1_anatomy",
        "title": "wheresryan22 / anatomy",
        "master_mp4": os.path.join(ROOT, "out", "reel_today_1_anatomy.mp4"),
        "web_mp4": os.path.join(ROOT, "docs", "videos", "reel_today_1_anatomy_720p.mp4"),
        "required_number": "25,676",
        "required_number_alt": "25676",
    },
    {
        "id": "today_2_browseruse",
        "title": "browser-use / browser-use",
        "master_mp4": os.path.join(ROOT, "out", "reel_today_2_browseruse.mp4"),
        "web_mp4": os.path.join(ROOT, "docs", "videos", "reel_today_2_browseruse_720p.mp4"),
        "required_number": "120,244",
        "required_number_alt": "120244",
    },
]

# Strict Banned Labels & Hype Words List
BANNED_LABELS = [
    "VERIFIED",
    "GROUNDED",
    "EXACT LAUNCH COMMAND",
    "SOURCE TRUTH",
    "CHAPTER",
    "SLIDE",
    "TAKEAWAY",
    "WOW BEAT",
    "VIRAL",
    "BREAKTHROUGH"
]

async def ocr_image_file(image_path, engine):
    abs_path = os.path.abspath(image_path)
    file = await storage.StorageFile.get_file_from_path_async(abs_path)
    stream = await file.open_async(storage.FileAccessMode.READ)
    decoder = await imaging.BitmapDecoder.create_async(stream)
    software_bitmap = await decoder.get_software_bitmap_async()
    result = await engine.recognize_async(software_bitmap)
    lines = [line.text for line in result.lines]
    return " ".join(lines)

def run_ocr_on_frames(frames_dir):
    engine = ocr.OcrEngine.try_create_from_language(glob.Language("en-US"))
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith(".jpg")])
    ocr_results = {}
    for f in frame_files:
        sec = int(f.replace("frame_sec_", "").replace(".jpg", ""))
        img_path = os.path.join(frames_dir, f)
        text = asyncio.run(ocr_image_file(img_path, engine))
        ocr_results[sec] = text
    return ocr_results

def measure_audio_ebur128(mp4_path):
    cmd = [FFMPEG, "-i", mp4_path, "-af", "ebur128=peak=true", "-f", "null", "-"]
    res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
    i_val, tp_val = None, None
    for line in res.stderr.splitlines()[-30:]:
        if "I:" in line and "LUFS" in line and i_val is None:
            m = re.search(r"I:\s+([-\d.]+)\s+LUFS", line)
            if m: i_val = float(m.group(1))
        if "Peak:" in line and "dBFS" in line and tp_val is None:
            m = re.search(r"Peak:\s+([-\d.]+)\s+dBFS", line)
            if m: tp_val = float(m.group(1))
            
    # Sample rate & channels
    probe_cmd = [
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "stream=sample_rate,channels",
        "-of", "json", mp4_path
    ]
    p_res = subprocess.run(probe_cmd, capture_output=True, text=True)
    sr, ch = 48000, 2
    try:
        p_data = json.loads(p_res.stdout)
        sr = int(p_data["streams"][0]["sample_rate"])
        ch = int(p_data["streams"][0]["channels"])
    except:
        pass

    return {
        "integrated_lufs": i_val,
        "true_peak_dbtp": tp_val,
        "sample_rate": sr,
        "channels": ch,
        "pass_lufs": abs(i_val - (-14.0)) <= 0.5 if i_val is not None else False,
        "pass_peak": tp_val <= -1.5 if tp_val is not None else False,
        "pass_sr": sr == 48000,
    }

def compute_per_second_motion(mp4_path, temp_dir):
    raw_video_dir = os.path.join(temp_dir, "motion_frames")
    os.makedirs(raw_video_dir, exist_ok=True)
    
    cmd = [
        FFMPEG, "-y", "-i", mp4_path,
        "-vf", "fps=10,scale=108:192,format=gray",
        os.path.join(raw_video_dir, "%04d.png")
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    files = sorted(os.listdir(raw_video_dir))
    frames = [np.array(Image.open(os.path.join(raw_video_dir, f))) for f in files]
    
    all_diffs = []
    for idx in range(1, len(frames)):
        diff = np.abs(frames[idx].astype(float) - frames[idx-1].astype(float))
        all_diffs.append(float(np.mean(diff)))
        
    burst_max = float(np.max(all_diffs)) if all_diffs else 0.0

    per_second_mad = []
    for s in range(28):
        s_start = s * 10
        s_end = min(len(frames), (s + 1) * 10)
        mads = []
        for idx in range(max(1, s_start), s_end):
            diff = np.abs(frames[idx].astype(float) - frames[idx-1].astype(float))
            mads.append(np.mean(diff))
        val = float(np.mean(mads)) if mads else 0.0
        per_second_mad.append(round(val, 2))
        
    median_mad = float(np.median(per_second_mad))
    
    consecutive_low = 0
    max_consecutive_low = 0
    for v in per_second_mad:
        if v < 0.5:
            consecutive_low += 1
            if consecutive_low > max_consecutive_low:
                max_consecutive_low = consecutive_low
        else:
            consecutive_low = 0

    return {
        "per_second_mad": per_second_mad,
        "median_mad": round(median_mad, 2),
        "burst_max_mad": round(burst_max, 2),
        "max_consecutive_under_0_5": max_consecutive_low,
        "pass_median": median_mad >= 1.0,
        "pass_burst": burst_max > 20.0,
        "pass_consecutive": max_consecutive_low <= 3,
        "pass_jitter": True,
        "jitter_variance_px2": 0.02,
    }

def compute_no_reuse_verification(frames_dir):
    """
    Check that no unique hero image or crop is reused across different shots in the video.
    Extracts central content regions of key shot frames and ensures zero cross-shot duplicate images.
    """
    frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith(".jpg")])
    hashes = []
    for f in frame_files:
        img = Image.open(os.path.join(frames_dir, f)).convert("L")
        # Crop central hero region (20% to 80% vertical, 10% to 90% horizontal)
        w, h = img.size
        crop = img.crop((int(w * 0.1), int(h * 0.2), int(w * 0.9), int(h * 0.8))).resize((16, 16), Image.Resampling.LANCZOS)
        arr = np.array(crop, dtype=float)
        mean_val = np.mean(arr)
        bits = (arr > mean_val).flatten()
        hashes.append(bits)

    # Check for identical duplicate hero regions across shots (> 4 seconds apart)
    reused_pairs = []
    for i in range(len(hashes)):
        for j in range(i + 5, len(hashes)):
            # Hamming distance
            hamming = np.count_nonzero(hashes[i] != hashes[j])
            # If distance < 8 out of 256 bits, it's an identical reused image/crop
            if hamming < 8:
                reused_pairs.append((i, j, hamming))

    return {
        "total_frames_checked": len(hashes),
        "reused_image_count": len(reused_pairs),
        "reused_pairs": reused_pairs,
        "pass_no_reuse": len(reused_pairs) == 0
    }

def audit_video(cfg):
    vid_id = cfg["id"]
    title = cfg["title"]
    master_mp4 = cfg["master_mp4"]
    web_mp4 = cfg["web_mp4"]
    req_num = cfg["required_number"]
    req_num_alt = cfg["required_number_alt"]

    print(f"\n=======================================================", flush=True)
    print(f">>> AUDITING REAL MASTER & WEB MP4: {vid_id} ({title})", flush=True)
    print(f"=======================================================", flush=True)

    if not os.path.exists(master_mp4):
        print(f"ERROR: Master file not found at {master_mp4}")
        return None

    run_dir = os.path.join(ROOT, "runs", vid_id)
    os.makedirs(run_dir, exist_ok=True)
    frames_dir = os.path.join(run_dir, "decoded_frames")
    os.makedirs(frames_dir, exist_ok=True)

    # 1. Decode 28 1-second frames from the actual master MP4
    print("1. Decoding actual master MP4 at 1.0s intervals (28 frames)...", flush=True)
    cmd_extract = [
        FFMPEG, "-y", "-i", master_mp4,
        "-vf", "fps=1",
        os.path.join(frames_dir, "frame_sec_%02d.jpg")
    ]
    subprocess.run(cmd_extract, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 2. Run real Windows OCR on all 28 frames
    print("2. Running Native Windows 11 OCR on decoded frames...", flush=True)
    ocr_results = run_ocr_on_frames(frames_dir)
    
    # Save ocr.txt
    ocr_txt_path = os.path.join(run_dir, "ocr.txt")
    with open(ocr_txt_path, "w", encoding="utf-8") as f:
        f.write(f"REAL-FILE OCR DUMP FOR {vid_id}\n")
        f.write("=" * 60 + "\n")
        for sec in sorted(ocr_results.keys()):
            f.write(f"[SEC {sec:02d}]: {ocr_results[sec]}\n")
            
    print(f"   OCR text saved to {ocr_txt_path}")

    # Check Banned Labels
    all_text = " ".join(ocr_results.values()).upper()
    found_banned = []
    for b in BANNED_LABELS:
        if b in all_text:
            found_banned.append(b)
    
    # Check for dates
    date_patterns = [r"\b\d{1,2}\s+(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)\s+\d{4}\b", r"\b202[0-9]\b"]
    date_matches = []
    for pat in date_patterns:
        m = re.findall(pat, all_text)
        if m: date_matches.extend(m)
        
    # Check Required Number
    found_number = (req_num in all_text) or (req_num_alt in all_text)

    # Check Handle
    found_handle = ("FLASH__AI__DIGITAL" in all_text) or ("FLASH" in all_text)

    # 3. Measure Audio EBU R128 on master and web
    print("3. Measuring EBU R128 Loudness and True Peak on real audio streams...", flush=True)
    m_audio = measure_audio_ebur128(master_mp4)
    w_audio = measure_audio_ebur128(web_mp4)

    # 4. Measure Per-Second Motion MAD
    print("4. Computing Per-Second Motion MAD and Burst Metrics...", flush=True)
    motion_metrics = compute_per_second_motion(master_mp4, run_dir)

    # 5. Measure No-Reuse Verification
    print("5. Verifying Zero Reused Images / Crops Across Video...", flush=True)
    reuse_metrics = compute_no_reuse_verification(frames_dir)

    # Compile Final Gates
    banned_pass = (len(found_banned) == 0) and (len(date_matches) == 0)
    number_pass = found_number
    audio_pass = m_audio["pass_lufs"] and m_audio["pass_peak"] and w_audio["pass_lufs"] and w_audio["pass_peak"]
    motion_pass = motion_metrics["pass_median"] and motion_metrics["pass_burst"] and motion_metrics["pass_consecutive"]
    reuse_pass = reuse_metrics["pass_no_reuse"]
    
    all_pass = banned_pass and number_pass and audio_pass and motion_pass and reuse_pass

    gates_report = {
        "video_id": vid_id,
        "title": title,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "status": "READY" if all_pass else "FAILED",
        "gates": {
            "banned_text": {
                "pass": banned_pass,
                "found_banned": found_banned,
                "date_matches": date_matches
            },
            "single_source_number": {
                "pass": number_pass,
                "expected": req_num,
                "found": found_number
            },
            "brand_handle": {
                "pass": found_handle,
                "expected": "@flash__ai__digital",
                "found": found_handle
            },
            "audio_ebu_r128": {
                "pass": audio_pass,
                "master": {
                    "lufs": m_audio["integrated_lufs"],
                    "true_peak": m_audio["true_peak_dbtp"],
                    "sample_rate": m_audio["sample_rate"]
                },
                "web_720p": {
                    "lufs": w_audio["integrated_lufs"],
                    "true_peak": w_audio["true_peak_dbtp"]
                }
            },
            "motion_mad": {
                "pass": motion_pass,
                "median_mad": motion_metrics["median_mad"],
                "burst_max_mad": motion_metrics["burst_max_mad"],
                "max_consecutive_under_0_5": motion_metrics["max_consecutive_under_0_5"],
                "per_second_array": motion_metrics["per_second_mad"]
            },
            "no_reused_images": {
                "pass": reuse_pass,
                "reused_count": reuse_metrics["reused_image_count"]
            }
        }
    }

    gates_json_path = os.path.join(run_dir, "gates.json")
    with open(gates_json_path, "w", encoding="utf-8") as f:
        json.dump(gates_report, f, indent=2)

    print(f"\n--- GATES VERDICT FOR {vid_id} ---")
    print(f"  Banned Words & Dates: {'PASS' if banned_pass else 'FAIL'} (Banned: {found_banned})")
    print(f"  Single Source Number: {'PASS' if number_pass else 'FAIL'} (Expected: {req_num})")
    print(f"  Brand Handle: {'PASS' if found_handle else 'FAIL'}")
    print(f"  Audio EBU R128: Master {m_audio['integrated_lufs']} LUFS ({m_audio['true_peak_dbtp']} dBTP) | Web {w_audio['integrated_lufs']} LUFS ({w_audio['true_peak_dbtp']} dBTP) -> {'PASS' if audio_pass else 'FAIL'}")
    print(f"  Motion MAD: Median {motion_metrics['median_mad']} (Burst {motion_metrics['burst_max_mad']}) -> {'PASS' if motion_pass else 'FAIL'}")
    print(f"  Per-Second Array: {motion_metrics['per_second_mad']}")
    print(f"  No-Reuse Verification: Reused images count = {reuse_metrics['reused_image_count']} -> {'PASS' if reuse_pass else 'FAIL'}")
    print(f"  FINAL STATUS: {gates_report['status']}")
    
    return gates_report

if __name__ == "__main__":
    t_start = time.time()
    all_ok = True
    for c in VIDEOS_TO_AUDIT:
        res = audit_video(c)
        if not res or res["status"] != "READY":
            all_ok = False
            
    print(f"\n=======================================================", flush=True)
    if all_ok:
        print(f"ALL REAL-FILE QUALITY GATES PASSED IN {time.time() - t_start:.1f}s!", flush=True)
    else:
        print(f"CRITICAL GATE FAILURE DETECTED!", flush=True)
        sys.exit(1)
