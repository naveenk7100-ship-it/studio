import os
import cv2
import numpy as np

STUDIO_DIR = r"C:\Users\navee\OneDrive\Desktop\studio"

def test_video(rel_path, label):
    path = os.path.join(STUDIO_DIR, rel_path)
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    dur = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
    flat_ratios = []
    for s in [4, 10, 16, 22]:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(s * fps))
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1)
        mag = np.sqrt(gx**2 + gy**2)
        flat = np.sum(mag < 3.0) / (frame.shape[0] * frame.shape[1])
        flat_ratios.append(flat)
    cap.release()
    avg_flat = np.mean(flat_ratios) * 100 if flat_ratios else 0.0
    gate_flat = avg_flat <= 20.0
    gate_dur = 28.0 <= dur <= 32.0
    print(f"=== {label} ===")
    print(f"Duration: {dur:.1f}s (Gate: 28-32s) -> {'PASS' if gate_dur else 'FAIL'}")
    print(f"Avg Flat Area: {avg_flat:.1f}% (Gate: <= 20.0%) -> {'PASS' if gate_flat else 'FAIL'}")
    print(f"Overall Computed Layout Gate: {'PASS' if (gate_flat and gate_dur) else 'FAIL'}\n")

test_video("out/delivery_video_a_aoede.mp4", "Previous Delivery Video A (Aoede - Keynote)")
test_video("out/delivery_video_b_sadachbia.mp4", "Previous Delivery Video B (Sadachbia - Keynote)")
