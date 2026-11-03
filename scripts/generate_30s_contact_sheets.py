"""
Generate 2x4 contact sheets and 8 beat stills for each of the 3 Golden 30s explainer reels.
Stills extracted at frames: 0, 60, 180, 240, 360, 540, 660, 800 (at 30 fps: 0s, 2s, 6s, 8s, 12s, 18s, 22s, 26.6s).
"""

import os
import subprocess
from PIL import Image
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
OUT_DIR = os.path.join(ROOT, "out")

VIDEOS = [
    ("golden_30s_1_vllm", os.path.join(OUT_DIR, "golden_30s_1_vllm.mp4")),
    ("golden_30s_2_claude", os.path.join(OUT_DIR, "golden_30s_2_claude.mp4")),
    ("golden_30s_3_mcp", os.path.join(OUT_DIR, "golden_30s_3_mcp.mp4")),
]

FRAMES = [0, 60, 180, 240, 360, 540, 660, 800]

def make_contact_sheet(vid_id, mp4_path):
    if not os.path.exists(mp4_path):
        print(f"Skipping {vid_id}, {mp4_path} does not exist yet.")
        return
        
    stills_dir = os.path.join(OUT_DIR, f"{vid_id}_stills")
    os.makedirs(stills_dir, exist_ok=True)
    
    still_files = []
    for f in FRAMES:
        t_sec = f / 30.0
        out_jpg = os.path.join(stills_dir, f"frame_{f:04d}_{t_sec:.2f}s.jpg")
        cmd = [
            FFMPEG, "-y",
            "-ss", f"{t_sec:.3f}",
            "-i", mp4_path,
            "-vframes", "1",
            "-q:v", "2",
            out_jpg
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(out_jpg):
            still_files.append(out_jpg)
            
    print(f"Extracted {len(still_files)} stills for {vid_id}")
    
    # Build 2x4 contact sheet (2 rows, 4 columns)
    # Thumbnail size: 270x480 (maintaining 9:16 aspect ratio)
    thumb_w, thumb_h = 270, 480
    sheet_w, sheet_h = thumb_w * 4, thumb_h * 2
    sheet = Image.new("RGB", (sheet_w, sheet_h), "#070b14")
    
    for idx, fpath in enumerate(still_files[:8]):
        im = Image.open(fpath)
        im_resized = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        row = idx // 4
        col = idx % 4
        sheet.paste(im_resized, (col * thumb_w, row * thumb_h))
        
    sheet_path = os.path.join(OUT_DIR, f"{vid_id}_contact_sheet.png")
    sheet.save(sheet_path)
    print(f"Saved contact sheet to {sheet_path}")

if __name__ == "__main__":
    for vid_id, mp4_path in VIDEOS:
        make_contact_sheet(vid_id, mp4_path)
