"""
Reference Reel Frame & Audio Analyzer
Extracts:
1. Cut rate (mean shot duration, shots per 15s/30s) via scene-boundary frame difference.
2. Motion score (frame-difference per second, optical flow proxy) in 1.0s windows.
3. Music BPM and beat grid via Librosa.
4. Updates target ranges in brand_kit.json.
"""

import os
import sys
import json
import cv2
import numpy as np
import librosa

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND_KIT_PATH = os.path.join(HERE, "brand_kit.json")

def analyze_video(video_path: str):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / fps

    print(f"\nAnalyzing: {os.path.basename(video_path)} ({duration_sec:.1f}s @ {fps:.1f} fps)")

    prev_gray = None
    frame_diffs = []
    cuts = [0.0]  # Timestamps of cuts in seconds
    per_second_motion = []
    current_sec_diffs = []

    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize for fast analysis
        small = cv2.resize(frame, (270, 480))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

        if prev_gray is not None:
            # Absolute difference
            diff = cv2.absdiff(gray, prev_gray)
            mean_diff = float(np.mean(diff))
            frame_diffs.append(mean_diff)
            current_sec_diffs.append(mean_diff)

            # Scene cut detection threshold
            if mean_diff > 35.0:
                t = frame_idx / fps
                if len(cuts) == 0 or (t - cuts[-1]) >= 0.5:
                    cuts.append(t)
        else:
            frame_diffs.append(0.0)
            current_sec_diffs.append(0.0)

        prev_gray = gray
        frame_idx += 1

        if frame_idx % int(fps) == 0:
            per_second_motion.append(float(np.mean(current_sec_diffs)) if current_sec_diffs else 0.0)
            current_sec_diffs = []

    cap.release()
    if current_sec_diffs:
        per_second_motion.append(float(np.mean(current_sec_diffs)))

    cuts.append(duration_sec)
    shot_durations = [cuts[i+1] - cuts[i] for i in range(len(cuts)-1)]
    mean_shot_len = float(np.mean(shot_durations)) if shot_durations else duration_sec
    shot_count = len(shot_durations)
    shots_per_30s = (shot_count / duration_sec) * 30.0 if duration_sec > 0 else 0

    # Audio analysis with librosa
    try:
        y, sr = librosa.load(video_path, sr=22050)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        bpm = float(np.atleast_1d(tempo)[0])
    except Exception as e:
        print(f"Audio analysis note: {e}")
        bpm = 120.0

    return {
        "duration_sec": round(duration_sec, 2),
        "total_shots": shot_count,
        "mean_shot_length_sec": round(mean_shot_len, 2),
        "shots_per_30s": round(shots_per_30s, 1),
        "music_bpm": round(bpm, 1),
        "mean_motion_score": round(float(np.mean(per_second_motion)), 2),
        "min_motion_score_1s": round(float(np.min(per_second_motion)) if per_second_motion else 0.0, 2),
        "per_second_motion": [round(x, 2) for x in per_second_motion]
    }

def update_brand_kit_with_references(ref_results: list):
    with open(BRAND_KIT_PATH, "r", encoding="utf-8") as f:
        bk = json.load(f)

    mean_shots = [r["shots_per_30s"] for r in ref_results]
    shot_lens = [r["mean_shot_length_sec"] for r in ref_results]
    bpms = [r["music_bpm"] for r in ref_results]
    motion_means = [r["mean_motion_score"] for r in ref_results]
    motion_mins = [r["min_motion_score_1s"] for r in ref_results]

    bk["reference_benchmarks"] = {
        "target_shots_per_30s": [int(np.min(mean_shots)), int(np.max(mean_shots))],
        "target_mean_shot_duration_sec": [round(float(np.min(shot_lens)), 2), round(float(np.max(shot_lens)), 2)],
        "target_music_bpm": [round(float(np.min(bpms)), 1), round(float(np.max(bpms)), 1)],
        "min_motion_threshold_1s": round(float(np.min(motion_mins)) * 0.8, 2),
        "target_motion_mean": round(float(np.mean(motion_means)), 2)
    }

    with open(BRAND_KIT_PATH, "w", encoding="utf-8") as f:
        json.dump(bk, f, indent=2)

    print("\nUpdated brand_kit.json with reference benchmark target ranges!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_reference_reels.py <reel1.mp4> [reel2.mp4] [reel3.mp4]")
        sys.exit(1)

    results = []
    for path in sys.argv[1:]:
        res = analyze_video(path)
        print(f"Result for {os.path.basename(path)}: {json.dumps(res, indent=2)}")
        results.append(res)

    if results:
        update_brand_kit_with_references(results)
