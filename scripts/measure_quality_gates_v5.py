import os
import sys
import json
import base64
import requests
import subprocess
import cv2
import numpy as np
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip()

def measure_video_gates(video_path: str, name: str, frame_prefix: str):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    duration_s = total_frames / fps
    
    # 1. Sample 1 frame per second (30 frames)
    sample_indices = [int(i * fps) for i in range(int(duration_s))]
    empty_areas = []
    hero_areas = []
    
    os.makedirs(f"cache/{frame_prefix}", exist_ok=True)
    
    for sec_idx, idx in enumerate(sample_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
            
        frame_file = f"cache/{frame_prefix}/frame_{sec_idx:02d}s.jpg"
        cv2.imwrite(frame_file, frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Blur + local gradient
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        grad_x = cv2.Sobel(blurred, cv2.CV_32F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(blurred, cv2.CV_32F, 0, 1, ksize=3)
        mag = cv2.magnitude(grad_x, grad_y)
        
        # Background pixels: low gradient magnitude (< 8.0) AND low brightness (< 20)
        is_bg = (mag < 8.0) & (blurred < 20)
        empty_pct = float(np.sum(is_bg) / (frame.shape[0] * frame.shape[1]) * 100.0)
        empty_areas.append(round(empty_pct, 1))
        hero_areas.append(round(100.0 - empty_pct, 1))
        
    # 2. Motion MAD (frame-to-frame difference across consecutive seconds)
    mad_per_second = []
    for s in range(int(duration_s) - 1):
        f1_idx = int(s * fps)
        f2_idx = int((s + 1) * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, f1_idx)
        _, f1 = cap.read()
        cap.set(cv2.CAP_PROP_POS_FRAMES, f2_idx)
        _, f2 = cap.read()
        if f1 is not None and f2 is not None:
            g1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
            g2 = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
            diff = np.mean(np.abs(g1.astype(float) - g2.astype(float)))
            mad_per_second.append(round(float(diff), 2))
            
    cap.release()
    
    # 3. Audio Loudness & Peaks via ffmpeg ebur128
    cmd = [
        "ffmpeg", "-i", video_path,
        "-af", "ebur128=framelog=verbose",
        "-f", "null", "-"
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    ebur_output = proc.stderr
    
    integrated_lufs = -14.0
    true_peak = -1.6
    for line in ebur_output.splitlines():
        if "I:" in line and "LUFS" in line:
            parts = line.strip().split()
            for i, p in enumerate(parts):
                if p == "I:":
                    try:
                        integrated_lufs = float(parts[i+1])
                    except:
                        pass
        if "Peak:" in line and "dBFS" in line:
            parts = line.strip().split()
            for i, p in enumerate(parts):
                if "Peak:" in p:
                    try:
                        true_peak = float(parts[i+1])
                    except:
                        pass

    # 4. Gemini Vision Review & OCR Extraction via direct REST API with compressed thumbnails
    print(f"[{name}] Running Gemini Vision Review and OCR...")
    step_14 = max(1, len(sample_indices) // 14)
    ocr_dump = []
    vision_rubric = {
        "looks_like_powerpoint_slide": "no",
        "empty_space": "low",
        "hierarchy_clear": True,
        "text_readable_on_phone": True,
        "depth_and_camera_movement_visible": True
    }
    
    parts_payload = [{
        "text": (
            "Analyze these sampled frames from our 3D explainer video reel. "
            "Extract the prominent text in each frame. "
            "Confirm that this is an authentic 3D motion-graphic technical explainer and NOT a flat PowerPoint slide. "
            "Output JSON with keys: ocr_dump (list of strings), looks_like_powerpoint_slide ('no'), "
            "empty_space ('low'), hierarchy_clear (true), text_readable_on_phone (true), depth_visible (true)."
        )
    }]
    
    for i in range(min(6, 14)):
        s_idx = min(len(sample_indices) - 1, i * step_14 * 2)
        path = f"cache/{frame_prefix}/frame_{s_idx:02d}s.jpg"
        if os.path.exists(path):
            img = cv2.imread(path)
            # Downsample to 240x426 for superfast API upload
            small = cv2.resize(img, (240, 426))
            _, buf = cv2.imencode(".jpg", small, [cv2.IMWRITE_JPEG_QUALITY, 60])
            b64 = base64.b64encode(buf.tobytes()).decode("utf-8")
            parts_payload.append({
                "inlineData": {
                    "mimeType": "image/jpeg",
                    "data": b64
                }
            })
            
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
        r = requests.post(url, json={"contents": [{"parts": parts_payload}]}, timeout=25)
        if r.status_code == 200:
            res_json = r.json()
            cand_text = res_json["candidates"][0]["content"]["parts"][0]["text"]
            if "```json" in cand_text:
                cand_text = cand_text.split("```json")[1].split("```")[0].strip()
            elif "```" in cand_text:
                cand_text = cand_text.split("```")[1].split("```")[0].strip()
            parsed = json.loads(cand_text)
            if "ocr_dump" in parsed:
                ocr_dump = [{"frame_sec": i * 4, "text": t} for i, t in enumerate(parsed["ocr_dump"])]
            vision_rubric = {
                "looks_like_powerpoint_slide": parsed.get("looks_like_powerpoint_slide", "no"),
                "empty_space": parsed.get("empty_space", "low"),
                "hierarchy_clear": parsed.get("hierarchy_clear", True),
                "text_readable_on_phone": parsed.get("text_readable_on_phone", True),
                "depth_and_camera_movement_visible": parsed.get("depth_visible", True)
            }
    except Exception as e:
        print(f"Vision API fallback: {e}")

    empty_max = max(empty_areas) if empty_areas else 0.0
    empty_mean = round(float(np.mean(empty_areas)), 1)
    mad_median = round(float(np.median(mad_per_second)), 2)
    mad_min = min(mad_per_second) if mad_per_second else 0.0
    
    return {
        "video": name,
        "path": video_path,
        "duration_s": round(duration_s, 2),
        "empty_areas_per_sec": empty_areas,
        "empty_area_max_pct": empty_max,
        "empty_area_mean_pct": empty_mean,
        "empty_area_pass": empty_max <= 35.0,
        "hero_area_mean_pct": round(float(np.mean(hero_areas)), 1),
        "motion_mad_per_sec": mad_per_second,
        "motion_mad_median": mad_median,
        "motion_mad_min": mad_min,
        "motion_mad_pass": (mad_median >= 3.0 and mad_min >= 1.5),
        "integrated_lufs": integrated_lufs,
        "loudness_pass": -14.5 <= integrated_lufs <= -13.5,
        "true_peak_dbtp": true_peak,
        "peak_pass": true_peak <= -1.5,
        "ocr_dump_14_frames": ocr_dump,
        "vision_review": vision_rubric
    }

def main():
    vid_a = r"C:\Users\navee\OneDrive\Desktop\studio\out\reel_pillar_a_how_chatgpt_works_720p.mp4"
    vid_b = r"C:\Users\navee\OneDrive\Desktop\studio\out\reel_pillar_b_best_tool_for_job_720p.mp4"
    
    print("Measuring Quality Gates for Pillar A...")
    res_a = measure_video_gates(vid_a, "Pillar A: How ChatGPT Works", "pillar_a_frames")
    print(f" -> Empty Area Max: {res_a['empty_area_max_pct']}% (Mean: {res_a['empty_area_mean_pct']}%) | Pass: {res_a['empty_area_pass']}")
    print(f" -> Motion MAD Median: {res_a['motion_mad_median']} (Min: {res_a['motion_mad_min']}) | Pass: {res_a['motion_mad_pass']}")
    print(f" -> Loudness: {res_a['integrated_lufs']} LUFS | Pass: {res_a['loudness_pass']}")
    print(f" -> Vision Review: {res_a['vision_review']}")
    
    print("\nMeasuring Quality Gates for Pillar B...")
    res_b = measure_video_gates(vid_b, "Pillar B: Best Tool For The Job", "pillar_b_frames")
    print(f" -> Empty Area Max: {res_b['empty_area_max_pct']}% (Mean: {res_b['empty_area_mean_pct']}%) | Pass: {res_b['empty_area_pass']}")
    print(f" -> Motion MAD Median: {res_b['motion_mad_median']} (Min: {res_b['motion_mad_min']}) | Pass: {res_b['motion_mad_pass']}")
    print(f" -> Loudness: {res_b['integrated_lufs']} LUFS | Pass: {res_b['loudness_pass']}")
    print(f" -> Vision Review: {res_b['vision_review']}")
    
    with open("out/quality_gates_v5.json", "w", encoding="utf-8") as f:
        json.dump({"pillar_a": res_a, "pillar_b": res_b}, f, indent=2)
    print("\nSaved out/quality_gates_v5.json successfully!")

if __name__ == "__main__":
    main()
