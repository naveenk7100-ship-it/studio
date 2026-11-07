"""
FLASH Content OS - 8-Beat Contact Sheet Generator for Today's 2 Fresh Reels:
1. wheresryan22/anatomy
2. browser-use/browser-use
"""

import os
import cv2
import numpy as np

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
OUT_DIR = os.path.join(ROOT, "out")
DOCS_DIR = os.path.join(ROOT, "docs")

REELS = [
    {
        "id": "today_1_anatomy",
        "title": "wheresryan22 / anatomy",
        "mp4": os.path.join(OUT_DIR, "reel_today_1_anatomy.mp4"),
        "contact_sheet": os.path.join(OUT_DIR, "reel_today_1_anatomy_contact_sheet.png"),
        "docs_sheet": os.path.join(DOCS_DIR, "reel_today_1_anatomy_contact_sheet.png"),
        "beat_frames": [49, 144, 265, 406, 528, 623, 703, 792],
        "beat_labels": [
            "01 Cover Hook (1.6s)",
            "02 Install (4.8s)",
            "03 Raptor Engine (8.8s)",
            "04 Slash Command (13.5s)",
            "05 Assemblies (17.6s)",
            "06 Stars 25,676 (20.8s)",
            "07 Author Ryan (23.4s)",
            "08 Brand End Card (26.4s)",
        ],
    },
    {
        "id": "today_2_browseruse",
        "title": "browser-use / browser-use",
        "mp4": os.path.join(OUT_DIR, "reel_today_2_browseruse.mp4"),
        "contact_sheet": os.path.join(OUT_DIR, "reel_today_2_browseruse_contact_sheet.png"),
        "docs_sheet": os.path.join(DOCS_DIR, "reel_today_2_browseruse_contact_sheet.png"),
        "beat_frames": [76, 188, 293, 418, 511, 609, 707, 792],
        "beat_labels": [
            "01 Cover Hook (2.5s)",
            "02 Architecture (6.3s)",
            "03 Quickstart uv (9.8s)",
            "04 Python Controller (13.9s)",
            "05 Benchmark (17.0s)",
            "06 Stars 120,244 (20.3s)",
            "07 browser-use Team (23.6s)",
            "08 Brand End Card (26.4s)",
        ],
    },
]

def generate_contact_sheet(cfg):
    mp4_path = cfg["mp4"]
    out_sheet = cfg["contact_sheet"]
    docs_sheet = cfg["docs_sheet"]
    title = cfg["title"]
    beat_frames = cfg["beat_frames"]
    beat_labels = cfg["beat_labels"]

    print(f">>> Generating 8-Beat Contact Sheet for {title}...", flush=True)
    cap = cv2.VideoCapture(mp4_path)
    if not cap.isOpened():
        print(f"ERROR: Cannot open {mp4_path}")
        return False

    thumbnails = []
    cell_w, cell_h = 270, 480

    for idx, fnum in enumerate(beat_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, fnum)
        ret, frame = cap.read()
        if not ret or frame is None:
            frame = np.zeros((1920, 1080, 3), dtype=np.uint8)
        
        resized = cv2.resize(frame, (cell_w, cell_h), interpolation=cv2.INTER_AREA)

        # Overlay beat label
        label = beat_labels[idx]
        cv2.rectangle(resized, (0, cell_h - 36), (cell_w, cell_h), (7, 9, 14), -1)
        cv2.putText(
            resized, label, (8, cell_h - 12),
            cv2.FONT_HERSHEY_SIMPLEX, 0.40, (0, 229, 255), 1, cv2.LINE_AA
        )
        thumbnails.append(resized)

    cap.release()

    # 4 columns x 2 rows
    row1 = np.hstack(thumbnails[0:4])
    row2 = np.hstack(thumbnails[4:8])
    grid = np.vstack([row1, row2]) # 1080w x 960h

    # Add header bar
    header = np.zeros((60, 1080, 3), dtype=np.uint8)
    header[:] = (7, 9, 14)
    cv2.putText(
        header, f"FLASH.Ai CINEMATIC PROOF -- {title.upper()}",
        (20, 38), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA
    )
    cv2.line(header, (0, 59), (1080, 59), (0, 229, 255), 1)

    final_sheet = np.vstack([header, grid])

    cv2.imwrite(out_sheet, final_sheet)
    cv2.imwrite(docs_sheet, final_sheet)
    print(f"    Saved: {out_sheet} and {docs_sheet}")
    return True

if __name__ == "__main__":
    for c in REELS:
        generate_contact_sheet(c)
    print("[CONTACT SHEETS GENERATION COMPLETE]")
