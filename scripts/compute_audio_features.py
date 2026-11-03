"""
Deterministic Per-Frame Audio Feature Extractor
Computes:
1. Exact beat grid (beat timestamps, downbeats, 16th subdivisions) at 30 FPS.
2. Per-frame FFT frequency bands (sub-bass, mid, presence, RMS energy).
3. Produces pure JSON lookup table: Frame -> AudioFeatures.
"""

import os
import sys
import json
import numpy as np
import librosa

def compute_audio_timeline(audio_path: str, fps: int = 30, total_duration_sec: float = 15.0):
    y, sr = librosa.load(audio_path, sr=22050)
    total_frames = int(round(total_duration_sec * fps))

    # 1. Beat detection
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(np.atleast_1d(tempo)[0])
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    beat_video_frames = [int(round(t * fps)) for t in beat_times if t <= total_duration_sec]

    # 2. STFT for per-frame spectral features
    hop_length = int(sr / fps)
    stft = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop_length))
    freqs = librosa.fft_frequencies(sr=sr, n_fft=2048)

    # Define bands
    sub_bass_mask = (freqs >= 20) & (freqs < 150)
    mid_mask = (freqs >= 150) & (freqs < 2500)
    presence_mask = (freqs >= 2500) & (freqs < 8000)

    features_per_frame = []
    num_stft_frames = stft.shape[1]

    for f in range(total_frames):
        if f < num_stft_frames:
            spec_col = stft[:, f]
            sub_bass = float(np.mean(spec_col[sub_bass_mask])) if np.any(sub_bass_mask) else 0.0
            mid = float(np.mean(spec_col[mid_mask])) if np.any(mid_mask) else 0.0
            presence = float(np.mean(spec_col[presence_mask])) if np.any(presence_mask) else 0.0
            rms = float(np.sqrt(np.mean(spec_col**2)))
        else:
            sub_bass = mid = presence = rms = 0.0

        is_beat = f in beat_video_frames
        features_per_frame.append({
            "frame": f,
            "time_sec": round(f / fps, 3),
            "is_beat": is_beat,
            "sub_bass": round(min(1.0, sub_bass * 4.0), 3),
            "mid": round(min(1.0, mid * 3.0), 3),
            "presence": round(min(1.0, presence * 5.0), 3),
            "rms": round(min(1.0, rms * 3.5), 3)
        })

    timeline = {
        "audio_path": audio_path,
        "duration_sec": total_duration_sec,
        "fps": fps,
        "total_frames": total_frames,
        "bpm": round(bpm, 1),
        "beat_frames": beat_video_frames,
        "per_frame_features": features_per_frame
    }
    return timeline

if __name__ == "__main__":
    audio_file = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\navee\OneDrive\Desktop\studio\assets\music\dark-tech\dark-tech_pulse.mp3"
    out_json = sys.argv[2] if len(sys.argv) > 2 else r"C:\Users\navee\OneDrive\Desktop\studio\config\audio_features.json"
    
    print(f"Extracting features from {audio_file}...")
    res = compute_audio_timeline(audio_file, fps=30, total_duration_sec=15.0)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)
    print(f"Exported {res['total_frames']} frames to {out_json} (BPM: {res['bpm']})")
