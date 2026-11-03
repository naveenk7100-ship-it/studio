import os
import cv2
import numpy as np
from PIL import Image

HERE = r"C:\Users\navee\OneDrive\Desktop\studio"
OUT = os.path.join(HERE, "out")

reels = [
    {
        "video": os.path.join(OUT, "golden_reel_1_vllm.mp4"),
        "sheet": os.path.join(OUT, "golden_reel_1_vllm_contact_sheet.png"),
        "name": "Golden Reel 1: vLLM (Repo Spotlight)"
    },
    {
        "video": os.path.join(OUT, "golden_reel_2_claude_code.mp4"),
        "sheet": os.path.join(OUT, "golden_reel_2_claude_code_contact_sheet.png"),
        "name": "Golden Reel 2: Claude Code (Tech Tip)"
    }
]

for r in reels:
    cap = cv2.VideoCapture(r["video"])
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    
    # Sample 8 equidistant frames across the 15 seconds
    sample_indices = [int(i * (total_frames - 1) / 7) for i in range(8)]
    frames = []
    
    for idx in sample_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            # Resize for contact sheet
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(rgb).resize((270, 480))
            frames.append(pil_img)
    cap.release()

    if len(frames) == 8:
        # 2 rows of 4 columns
        sheet = Image.new("RGB", (1080, 960), (7, 11, 20))
        for i, img in enumerate(frames):
            row = i // 4
            col = i % 4
            sheet.paste(img, (col * 270, row * 480))
        sheet.save(r["sheet"])
        print(f"Generated contact sheet: {r['sheet']}")

print("All golden contact sheets created!")
