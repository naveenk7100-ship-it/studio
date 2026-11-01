import os
import subprocess
import numpy as np
import soundfile as sf
import scipy.signal as signal
import imageio_ffmpeg

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

STUDIO_DIR = r"C:\Users\navee\OneDrive\Desktop\studio"
AOEDE_PATH = os.path.join(STUDIO_DIR, "out", "delivery_video_a_aoede_voice.mp3")
SADACHBIA_PATH = os.path.join(STUDIO_DIR, "out", "delivery_video_b_sadachbia_voice.mp3")

def analyze_voice(audio_path):
    wav_tmp = os.path.join(STUDIO_DIR, "scratch", "tmp_metric.wav")
    os.makedirs(os.path.dirname(wav_tmp), exist_ok=True)
    subprocess.run([FFMPEG_BIN, "-y", "-i", audio_path, "-vn", "-ar", "16000", "-ac", "1", wav_tmp],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    data, sr = sf.read(wav_tmp)
    if os.path.exists(wav_tmp):
        try: os.remove(wav_tmp)
        except Exception: pass

    total_dur = len(data) / sr

    # 1. Pitch median and semitone std
    frame_len = int(sr * 0.02)  # 20ms
    frames = [data[i:i + frame_len] for i in range(0, len(data) - frame_len, frame_len)]
    frame_rms = np.array([np.sqrt(np.mean(f**2) + 1e-12) for f in frames])
    max_rms = np.max(frame_rms) if len(frame_rms) > 0 else 1.0

    # Pause calculation
    # Speech vs pause: frames with rms < threshold
    silence_thresh = max_rms * 0.05
    silent_frames = np.sum(frame_rms < silence_thresh)
    pause_pct = (silent_frames / len(frames)) * 100.0 if len(frames) > 0 else 0.0

    # Pitch tracking using Autocorrelation
    pitches = []
    min_lag = int(sr / 380)  # 380 Hz max
    max_lag = int(sr / 75)   # 75 Hz min

    for f, rms in zip(frames, frame_rms):
        if rms >= silence_thresh:
            norm_f = f - np.mean(f)
            corr = np.correlate(norm_f, norm_f, mode="full")
            corr = corr[len(corr) // 2:]
            if len(corr) > max_lag:
                peak_lag = min_lag + np.argmax(corr[min_lag:max_lag])
                if corr[peak_lag] > 0.35 * corr[0]:
                    pitch = sr / peak_lag
                    if 80 <= pitch <= 350:
                        pitches.append(pitch)

    pitches = np.array(pitches)
    if len(pitches) > 0:
        pitch_median = float(np.median(pitches))
        semitones = 12 * np.log2(pitches / pitch_median)
        semitone_std = float(np.std(semitones))
    else:
        pitch_median = 0.0
        semitone_std = 0.0

    # 2. Syllable-energy peaks per second:
    # Envelope extraction: Hilbert transform or lowpass filtered rectified signal
    # Syllables typically occur at 3-7 Hz modulation rate (prominence ~ 150-250 ms apart)
    speech_dur = total_dur * (1.0 - (pause_pct / 100.0))
    analytic = signal.hilbert(data)
    envelope = np.abs(analytic)
    # Lowpass filter the envelope at 10 Hz
    b, a = signal.butter(2, 10.0 / (sr / 2), btype='low')
    smooth_env = signal.filtfilt(b, a, envelope)
    
    # Find peaks on smoothed envelope
    # Min distance between peaks ~ 120ms (sr * 0.12)
    # Prominence relative to max
    min_dist = int(sr * 0.12)
    peaks, _ = signal.find_peaks(smooth_env, distance=min_dist, prominence=0.03 * np.max(smooth_env))
    num_peaks = len(peaks)
    peaks_per_sec = num_peaks / max(0.1, speech_dur)

    print(f"File: {os.path.basename(audio_path)}")
    print(f"Total Dur: {total_dur:.2f}s, Speech Dur: {speech_dur:.2f}s")
    print(f"Pitch Median: {pitch_median:.1f} Hz")
    print(f"Expressiveness (semitone std): {semitone_std:.2f} st")
    print(f"Pause Pct: {pause_pct:.1f}%")
    print(f"Syllable Peaks: {num_peaks}, Peaks/sec (over speech time): {peaks_per_sec:.2f}")
    print("---")

analyze_voice(AOEDE_PATH)
analyze_voice(SADACHBIA_PATH)
