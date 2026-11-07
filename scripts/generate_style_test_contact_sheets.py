"""
Generate 8-frame contact sheets for the 3 Style Test Variants:
- StyleTest-VariantA (Deep Teal Studio)
- StyleTest-VariantB (Warm Paper-and-Ink Blueprint)
- StyleTest-VariantC (Light Museum Vitrine)

Sampled frames: [20, 70, 120, 160, 210, 260, 310, 345] (12s @ 30fps = 360 frames).
"""

import os
import sys
import shutil
import cv2
import numpy as np

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
OUT_DIR = os.path.join(ROOT, "out")
DOCS_DIR = os.path.join(ROOT, "docs")
ARTIFACT_DIR = r"C:\Users\navee\.gemini\antigravity\brain\8b5ef5ec-ac96-4092-ba21-368a898ca77f"

FRAMES_TO_EXTRACT = [20, 70, 120, 160, 210, 260, 310, 345]

VARIANTS = [
    {
        "id": "variant_a",
        "title": "Style Test Variant A - Deep Teal Studio",
        "mp4": os.path.join(OUT_DIR, "style_test_variant_a.mp4"),
        "contact_sheet": os.path.join(OUT_DIR, "style_test_variant_a_contact_sheet.png"),
        "art_sheet": os.path.join(ARTIFACT_DIR, "style_test_variant_a_contact_sheet.png"),
        "docs_sheet": os.path.join(DOCS_DIR, "style_test_variant_a_contact_sheet.png"),
        "frames_dir": os.path.join(OUT_DIR, "frames_variant_a"),
    },
    {
        "id": "variant_b",
        "title": "Style Test Variant B - Warm Paper-and-Ink Blueprint",
        "mp4": os.path.join(OUT_DIR, "style_test_variant_b.mp4"),
        "contact_sheet": os.path.join(OUT_DIR, "style_test_variant_b_contact_sheet.png"),
        "art_sheet": os.path.join(ARTIFACT_DIR, "style_test_variant_b_contact_sheet.png"),
        "docs_sheet": os.path.join(DOCS_DIR, "style_test_variant_b_contact_sheet.png"),
        "frames_dir": os.path.join(OUT_DIR, "frames_variant_b"),
    },
    {
        "id": "variant_c",
        "title": "Style Test Variant C - Light Museum Vitrine",
        "mp4": os.path.join(OUT_DIR, "style_test_variant_c.mp4"),
        "contact_sheet": os.path.join(OUT_DIR, "style_test_variant_c_contact_sheet.png"),
        "art_sheet": os.path.join(ARTIFACT_DIR, "style_test_variant_c_contact_sheet.png"),
        "docs_sheet": os.path.join(DOCS_DIR, "style_test_variant_c_contact_sheet.png"),
        "frames_dir": os.path.join(OUT_DIR, "frames_variant_c"),
    },
]

def make_contact_sheet(cfg):
    mp4_path = cfg["mp4"]
    if not os.path.exists(mp4_path):
        print(f"Error: {mp4_path} not found!")
        return False

    os.makedirs(cfg["frames_dir"], exist_ok=True)
    cap = cv2.VideoCapture(mp4_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    extracted_imgs = []
    for f_idx in FRAMES_TO_EXTRACT:
        target = min(f_idx, total_frames - 1)
        cap.set(cv2.CAP_PROP_POS_FRAMES, target)
        ret, frame = cap.read()
        if not ret:
            print(f"Failed to read frame {target} from {mp4_path}")
            continue

        # Save single frame
        frame_file = os.path.join(cfg["frames_dir"], f"frame_{target:04d}.png")
        cv2.imwrite(frame_file, frame)

        # Annotate with timecode & frame number
        annotated = frame.copy()
        t_sec = target / fps
        label = f"Frame {target:03d} | {t_sec:.2f}s"
        cv2.rectangle(annotated, (20, 20), (440, 80), (0, 0, 0), -1)
        cv2.putText(annotated, label, (30, 62), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2, cv2.LINE_AA)

        # Scale down for 2x4 grid thumbnail (width: 360, height: 640)
        thumb = cv2.resize(annotated, (360, 640), interpolation=cv2.INTER_AREA)
        extracted_imgs.append(thumb)

    cap.release()

    if len(extracted_imgs) != 8:
        print(f"Expected 8 frames, got {len(extracted_imgs)}")
        return False

    # Arrange 2 rows of 4 images: Total size = (4 * 360) x (2 * 640) = 1440 x 1280
    row1 = np.hstack(extracted_imgs[0:4])
    row2 = np.hstack(extracted_imgs[4:8])
    grid = np.vstack([row1, row2])

    # Add Title Banner Header (1440 x 90)
    banner = np.zeros((90, 1440, 3), dtype=np.uint8)
    banner[:] = (15, 23, 42)  # Dark slate background
    cv2.putText(banner, cfg["title"], (40, 58), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 229, 255) if "Teal" in cfg["title"] else (226, 184, 120) if "Blueprint" in cfg["title"] else (16, 185, 129), 3, cv2.LINE_AA)

    final_sheet = np.vstack([banner, grid])
    cv2.imwrite(cfg["contact_sheet"], final_sheet)
    print(f">>> Contact sheet saved: {cfg['contact_sheet']} ({os.path.getsize(cfg['contact_sheet'])/1024:.1f} KB)")

    if os.path.exists(ARTIFACT_DIR):
        shutil.copy2(cfg["contact_sheet"], cfg["art_sheet"])
    if os.path.exists(DOCS_DIR):
        shutil.copy2(cfg["contact_sheet"], cfg["docs_sheet"])
    return True

def main():
    for cfg in VARIANTS:
        make_contact_sheet(cfg)

if __name__ == "__main__":
    main()
