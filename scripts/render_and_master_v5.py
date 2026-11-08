import os
import sys
import json
import subprocess
import cv2
import numpy as np

def run_cmd(cmd, cwd=None):
    print(f"[CMD] {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    res = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[STDERR] {res.stderr[:400]}")
        raise RuntimeError(f"Command failed with code {res.returncode}")
    return res.stdout

def create_contact_sheet(video_path: str, out_sheet_path: str, rows=4, cols=3):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    num_samples = rows * cols
    step = total_frames // num_samples
    
    frames = []
    for i in range(num_samples):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * step)
        ret, frame = cap.read()
        if ret:
            # Resize frame to 240x426 for grid
            thumb = cv2.resize(frame, (240, 426))
            # Add timecode badge
            sec = round((i * step) / 30.0, 1)
            cv2.putText(thumb, f"{sec}s", (12, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 0), 4)
            cv2.putText(thumb, f"{sec}s", (12, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 240, 255), 2)
            frames.append(thumb)
            
    cap.release()
    
    # Assemble grid
    grid_rows = []
    for r in range(rows):
        row_frames = frames[r * cols:(r + 1) * cols]
        grid_rows.append(np.hstack(row_frames))
    sheet = np.vstack(grid_rows)
    cv2.imwrite(out_sheet_path, sheet)
    print(f"[SHEET] Saved contact sheet: {out_sheet_path}")

def main():
    engine_dir = r"C:\Users\navee\OneDrive\Desktop\studio\engine"
    out_dir = r"C:\Users\navee\OneDrive\Desktop\studio\out"
    docs_dir = r"C:\Users\navee\OneDrive\Desktop\studio\docs"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(docs_dir, exist_ok=True)
    
    # 1. Render Pillar A
    print("\n=== RENDERING PILLAR A: HOW CHATGPT WORKS (30.0s) ===")
    raw_a = os.path.join(out_dir, "raw_pillar_a.mp4")
    final_a = os.path.join(out_dir, "reel_pillar_a_how_chatgpt_works_720p.mp4")
    run_cmd(f'npx remotion render PillarA-HowChatGPTWorks "{raw_a}" --concurrency=4', cwd=engine_dir)
    
    # Master audio to strict -14.0 LUFS
    audio_a = r"C:\Users\navee\OneDrive\Desktop\studio\cache\v5\master_pillar_a.mp3"
    run_cmd([
        "ffmpeg", "-y", "-i", raw_a, "-i", audio_a,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy",
        "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7",
        "-c:a", "aac", "-b:a", "192k",
        final_a
    ])
    if os.path.exists(raw_a):
        os.remove(raw_a)
    create_contact_sheet(final_a, os.path.join(docs_dir, "pillar_a_contact_sheet.png"))
    
    # 2. Render Pillar B
    print("\n=== RENDERING PILLAR B: BEST TOOL FOR THE JOB (30.0s) ===")
    raw_b = os.path.join(out_dir, "raw_pillar_b.mp4")
    final_b = os.path.join(out_dir, "reel_pillar_b_best_tool_for_job_720p.mp4")
    run_cmd(f'npx remotion render PillarB-BestToolForJob "{raw_b}" --concurrency=4', cwd=engine_dir)
    
    audio_b = r"C:\Users\navee\OneDrive\Desktop\studio\cache\v5\master_pillar_b.mp3"
    run_cmd([
        "ffmpeg", "-y", "-i", raw_b, "-i", audio_b,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "copy",
        "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7",
        "-c:a", "aac", "-b:a", "192k",
        final_b
    ])
    if os.path.exists(raw_b):
        os.remove(raw_b)
    create_contact_sheet(final_b, os.path.join(docs_dir, "pillar_b_contact_sheet.png"))
    
    print("\n=== RENDERING & AUDIO MASTERING COMPLETE ===")

if __name__ == "__main__":
    main()
