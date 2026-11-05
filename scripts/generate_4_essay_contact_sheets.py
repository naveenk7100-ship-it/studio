"""
FLASH Content OS - 8-Beat Cinematic Essay Contact Sheet Generator (All 4 Reels)
Extracts 8 distinct beat stills across each 28.00s explainer reel:
Shot 1 (Radar & Signal Field): frame 45 (1.5s)
Shot 2 (Sonar Proof Card): frame 135 (4.5s)
Shot 3 (Fanning Cards Proof): frame 225 (7.5s)
Shot 4 (High-DPI Docs Deep-Dive): frame 330 (11.0s)
Shot 5 (Interactive Step Flow): frame 435 (14.5s)
Shot 6 (Motion Burst Spike): frame 555 (18.5s)
Shot 7 (Command Blueprint): frame 675 (22.5s)
Shot 8 (Follow End Card): frame 795 (26.5s)

Arranges into a 4x2 grid contact sheet (1080x1920 scaled down to 270x480 each, grid 1080x960).
"""

import os
import sys
import shutil
import cv2
import numpy as np

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
OUT_DIR = os.path.join(ROOT, "out")
DOCS_DIR = os.path.join(ROOT, "docs")
BRAIN_DIR = r"C:\Users\navee\.gemini\antigravity\brain\8b5ef5ec-ac96-4092-ba21-368a898ca77f"

VIDEOS = [
    {
        "id": "reel_essay_1_unslop",
        "mp4": os.path.join(OUT_DIR, "reel_essay_1_unslop.mp4"),
        "raw_mp4": os.path.join(OUT_DIR, "raw_essay_1_unslop.mp4"),
        "contact_sheet": os.path.join(OUT_DIR, "reel_essay_1_unslop_contact_sheet.png"),
        "title": "heydamir / unslop (Fanning Cards & Clean-Room De-Slop)",
    },
    {
        "id": "reel_essay_2_uv",
        "mp4": os.path.join(OUT_DIR, "reel_essay_2_uv.mp4"),
        "raw_mp4": os.path.join(OUT_DIR, "raw_essay_2_uv.mp4"),
        "contact_sheet": os.path.join(OUT_DIR, "reel_essay_2_uv_contact_sheet.png"),
        "title": "astral-sh / uv 0.13.7 (High-Velocity Package Manager)",
    },
    {
        "id": "reel_essay_3_kimi",
        "mp4": os.path.join(OUT_DIR, "reel_essay_3_kimi.mp4"),
        "raw_mp4": os.path.join(OUT_DIR, "raw_essay_3_kimi.mp4"),
        "contact_sheet": os.path.join(OUT_DIR, "reel_essay_3_kimi_contact_sheet.png"),
        "title": "Moonshot AI Kimi K3.1 Pro (Reasoning Model Weights)",
    },
    {
        "id": "reel_essay_4_craft",
        "mp4": os.path.join(OUT_DIR, "reel_essay_4_craft.mp4"),
        "raw_mp4": os.path.join(OUT_DIR, "raw_essay_4_craft.mp4"),
        "contact_sheet": os.path.join(OUT_DIR, "reel_essay_4_craft_contact_sheet.png"),
        "title": "storytold / craft-anything (Rust Clean-Room Voxel Engine)",
    },
]

BEAT_FRAMES = [45, 135, 225, 330, 435, 555, 675, 795]
BEAT_LABELS = [
    "01 Signal Field (1.5s)",
    "02 Sonar Proof (4.5s)",
    "03 Fanning Cards (7.5s)",
    "04 Deep-Dive (11.0s)",
    "05 Step Flow (14.5s)",
    "06 Burst Spike (18.5s)",
    "07 Blueprint (22.5s)",
    "08 Follow Card (26.5s)",
]

def make_contact_sheet(vid):
    vid_id = vid["id"]
    mp4_path = vid["mp4"] if os.path.exists(vid["mp4"]) else vid["raw_mp4"]
    sheet_out = vid["contact_sheet"]
    
    print(f"\n>>> Generating Contact Sheet for {vid_id} from {mp4_path}...", flush=True)
    if not os.path.exists(mp4_path):
        print(f"ERROR: MP4 not found at {mp4_path}", flush=True)
        return False
        
    cap = cv2.VideoCapture(mp4_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    stills = []
    
    for f_idx in BEAT_FRAMES:
        cap.set(cv2.CAP_PROP_POS_FRAMES, min(f_idx, total_frames - 1))
        ret, frame = cap.read()
        if ret:
            thumb = cv2.resize(frame, (270, 480), interpolation=cv2.INTER_AREA)
            stills.append(thumb)
        else:
            print(f"Warning: could not read frame {f_idx}")
            blank = np.zeros((480, 270, 3), dtype=np.uint8)
            stills.append(blank)
    cap.release()
    
    row1 = np.hstack(stills[:4])
    row2 = np.hstack(stills[4:])
    grid = np.vstack([row1, row2])
    
    # Add header banner (60px high)
    header = np.full((60, 1080, 3), 18, dtype=np.uint8)
    cv2.putText(header, f"FLASH.Ai Cinematic Essay: {vid['title']}", (24, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(header, "840 Frames @ 30fps (28.00s)", (780, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 229, 255), 1, cv2.LINE_AA)
    
    final_img = np.vstack([header, grid])
    
    # Draw badges for each beat on row 1 & row 2
    for i, label in enumerate(BEAT_LABELS):
        r = 0 if i < 4 else 1
        c = i if i < 4 else i - 4
        x = c * 270 + 8
        y = 60 + r * 480 + 24
        cv2.rectangle(final_img, (x - 2, y - 18), (x + len(label) * 8 + 4, y + 6), (0, 0, 0), -1)
        cv2.putText(final_img, label, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 229, 255), 1, cv2.LINE_AA)
        
    cv2.imwrite(sheet_out, final_img)
    print(f"  Saved contact sheet: {sheet_out} ({os.path.getsize(sheet_out)} bytes)", flush=True)
    
    # Copy to docs/ and brain
    docs_out = os.path.join(DOCS_DIR, f"{vid_id}_contact_sheet.png")
    brain_out = os.path.join(BRAIN_DIR, f"{vid_id}_contact_sheet.png")
    shutil.copy2(sheet_out, docs_out)
    shutil.copy2(sheet_out, brain_out)
    return True

if __name__ == "__main__":
    for v in VIDEOS:
        make_contact_sheet(v)
    print("\n[ALL 4 CONTACT SHEETS GENERATED]")
