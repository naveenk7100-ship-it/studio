"""
FLASH Content OS - 8-Beat Editorial Contact Sheet Generator
Extracts 8 distinct beat stills across each 28.00s explainer reel:
Shot 1 (Hook): frame 30 (1.0s)
Shot 2 (What is it): frame 120 (4.0s)
Shot 3 (Architecture): frame 240 (8.0s)
Shot 4 (Code/Config): frame 360 (12.0s)
Shot 5 (Benchmark): frame 480 (16.0s)
Shot 6 (Indian Builder Context): frame 600 (20.0s)
Shot 7 (Actionable Takeaway): frame 720 (24.0s)
Shot 8 (CTA): frame 810 (27.0s)

Arranges into a 4x2 grid contact sheet (1080x1920 scaled down to 270x480 each, grid 1080x960).
"""

import os
import sys
import subprocess
import cv2
import numpy as np
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
OUT_DIR = os.path.join(ROOT, "out")

VIDEOS = [
    {
        "id": "reel_new_1_superagent",
        "mp4": os.path.join(OUT_DIR, "reel_new_1_superagent.mp4"),
        "raw_mp4": os.path.join(OUT_DIR, "raw_new_1_superagent.mp4"),
        "contact_sheet": os.path.join(OUT_DIR, "reel_new_1_superagent_contact_sheet.png"),
        "title": "DeepSeek SuperAgent (Editorial Zoom)",
    },
    {
        "id": "reel_new_2_ollama",
        "mp4": os.path.join(OUT_DIR, "reel_new_2_ollama.mp4"),
        "raw_mp4": os.path.join(OUT_DIR, "raw_new_2_ollama.mp4"),
        "contact_sheet": os.path.join(OUT_DIR, "reel_new_2_ollama_contact_sheet.png"),
        "title": "Ollama v0.40.14 (Screen-Studio Demo)",
    },
    {
        "id": "reel_new_3_qwen_news",
        "mp4": os.path.join(OUT_DIR, "reel_new_3_qwen_news.mp4"),
        "raw_mp4": os.path.join(OUT_DIR, "raw_new_3_qwen_news.mp4"),
        "contact_sheet": os.path.join(OUT_DIR, "reel_new_3_qwen_news_contact_sheet.png"),
        "title": "Qwen 27B Interpretability (Data Story)",
    },
]

BEAT_FRAMES = [30, 120, 240, 360, 480, 600, 720, 810]
BEAT_LABELS = [
    "01 Hook (1.0s)",
    "02 Problem (4.0s)",
    "03 Architecture (8.0s)",
    "04 Deep-Dive (12.0s)",
    "05 Metrics (16.0s)",
    "06 Indian Builders (20.0s)",
    "07 Action Item (24.0s)",
    "08 CTA (27.0s)",
]

def make_contact_sheet(vid):
    vid_id = vid["id"]
    mp4_path = vid["mp4"] if os.path.exists(vid["mp4"]) else vid["raw_mp4"]
    sheet_out = vid["contact_sheet"]
    
    print(f"\n>>> Generating Contact Sheet for {vid_id} from {mp4_path}...")
    if not os.path.exists(mp4_path):
        print(f"ERROR: MP4 not found at {mp4_path}")
        return False
        
    cap = cv2.VideoCapture(mp4_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    stills = []
    
    for f_idx in BEAT_FRAMES:
        cap.set(cv2.CAP_PROP_POS_FRAMES, min(f_idx, total_frames - 1))
        ret, frame = cap.read()
        if ret:
            # Resize from 1080x1920 to 270x480
            thumb = cv2.resize(frame, (270, 480), interpolation=cv2.INTER_AREA)
            stills.append(thumb)
        else:
            print(f"Warning: could not read frame {f_idx}")
            blank = np.zeros((480, 270, 3), dtype=np.uint8)
            stills.append(blank)
    cap.release()
    
    # 4 columns, 2 rows: Row 1 = shots 1..4 (width 1080, height 480), Row 2 = shots 5..8 (width 1080, height 480)
    # Total grid: 1080 x 960
    row1 = np.hstack(stills[:4])
    row2 = np.hstack(stills[4:])
    grid = np.vstack([row1, row2])
    
    # Add header banner (60px high)
    header = np.full((60, 1080, 3), 18, dtype=np.uint8)
    cv2.putText(header, f"FLASH.Ai Editorial Contact Sheet: {vid['title']}", (24, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(header, "840 Frames @ 30fps (28.00s)", (780, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 229, 255), 1, cv2.LINE_AA)
    
    final_sheet = np.vstack([header, grid])
    cv2.imwrite(sheet_out, final_sheet)
    print(f"Saved contact sheet to {sheet_out} ({final_sheet.shape[1]}x{final_sheet.shape[0]})")
    return True

if __name__ == "__main__":
    for v in VIDEOS:
        make_contact_sheet(v)
