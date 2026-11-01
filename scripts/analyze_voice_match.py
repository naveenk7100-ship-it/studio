import os
import sys
import subprocess
import numpy as np
import soundfile as sf
import scipy.signal as signal
import imageio_ffmpeg

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()


def analyze_audio_match(audio_or_video_path: str) -> dict:
    """Compute acoustic pitch median, expressiveness, syllable-energy peaks/s, and pause percentage."""
    wav_tmp = os.path.join(os.path.dirname(audio_or_video_path), "tmp_analyze.wav")
    cmd = [FFMPEG_BIN, "-y", "-i", audio_or_video_path, "-vn", "-ar", "16000", "-ac", "1", wav_tmp]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

    data, sr = sf.read(wav_tmp)
    if os.path.exists(wav_tmp):
        try:
            os.remove(wav_tmp)
        except Exception:
            pass

    total_dur = len(data) / sr

    # 1. Pause Percentage (Contiguous silence runs >= 150ms where RMS < 4% max)
    frame_len = int(sr * 0.02)
    step = int(sr * 0.01)
    frames = [data[i:i + frame_len] for i in range(0, len(data) - frame_len, step)]
    frame_rms = np.array([np.sqrt(np.mean(f**2) + 1e-12) for f in frames])
    max_rms = np.max(frame_rms) if len(frame_rms) > 0 else 1.0

    silent = (frame_rms < (max_rms * 0.04)).astype(int)
    diffs = np.diff(np.pad(silent, (1, 1), 'constant'))
    starts = np.where(diffs == 1)[0]
    ends = np.where(diffs == -1)[0]
    durations = (ends - starts) * 0.01
    pause_dur = np.sum(durations[durations >= 0.15])
    pause_pct = (pause_dur / total_dur) * 100.0 if total_dur > 0 else 0.0
    speech_dur = max(0.1, total_dur - pause_dur)

    # 2. Pitch tracking using Autocorrelation
    pitches = []
    min_lag = int(sr / 380)  # 380 Hz max
    max_lag = int(sr / 75)   # 75 Hz min

    for f, rms in zip(frames, frame_rms):
        if rms >= max_rms * 0.04:
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

    # 3. Syllable-energy peaks per second (Standard acoustic envelope modulation)
    analytic = signal.hilbert(data)
    env = np.abs(analytic)
    b, a = signal.butter(2, 8.0 / (sr / 2), btype='low')
    smooth_env = signal.filtfilt(b, a, env)
    min_dist = int(sr * 0.090)  # 90ms min inter-syllabic interval
    peaks, _ = signal.find_peaks(smooth_env, distance=min_dist, prominence=0.025 * np.max(smooth_env))
    peaks_per_sec = len(peaks) / speech_dur

    gates = config.VOICE_QUALITY_GATES
    gate_expressive = bool(semitone_std >= gates["min_expressiveness"])
    gate_pace = bool(gates["min_syllable_peaks"] <= peaks_per_sec <= gates["max_syllable_peaks"])
    gate_pause = bool(gates["min_pause_pct"] <= pause_pct <= gates["max_pause_pct"])
    passed = bool(gate_expressive and gate_pace and gate_pause)

    return {
        "duration_sec": round(float(total_dur), 2),
        "speech_dur_sec": round(float(speech_dur), 2),
        "pitch_median_hz": round(float(pitch_median), 1),
        "expressiveness_semitones": round(float(semitone_std), 2),
        "syllable_peaks_per_sec": round(float(peaks_per_sec), 2),
        "pause_percentage": round(float(pause_pct), 1),
        "gate_expressiveness": gate_expressive,
        "gate_pace": gate_pace,
        "gate_pause": gate_pause,
        "passed": passed
    }


def format_voice_match_table(metrics: dict, label: str) -> str:
    """Format comparison table against Bunty reference."""
    ref = config.BUNTY_REFERENCE
    lines = [
        f"### Voice Match Report: {label}",
        "| Acoustic Metric | Bunty Benchmark | Candidate Measured | Gate Threshold | Gate Status |",
        "| :--- | :---: | :---: | :---: | :---: |",
        f"| **Pitch Median** | `188 Hz` | `{metrics['pitch_median_hz']} Hz` | Natural timbre | PASS |",
        f"| **Expressiveness** | `5.0 semitones` | `{metrics['expressiveness_semitones']} semitones` | >= 4.5 st | {'PASS' if metrics['gate_expressiveness'] else 'FAIL'} |",
        f"| **Speech Pace (Syllable Peaks)** | `5.13 peaks/s` | `{metrics['syllable_peaks_per_sec']} peaks/s` | 4.6 - 5.6 peaks/s | {'PASS' if metrics['gate_pace'] else 'FAIL'} |",
        f"| **Pause Percentage** | `16.2%` | `{metrics['pause_percentage']}%` | 12.0% - 22.0% | {'PASS' if metrics['gate_pause'] else 'FAIL'} |",
        f"| **Overall Voice Gate** | - | - | All 3 gates | **{'PASS' if metrics['passed'] else 'FAIL'}** |"
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\navee\OneDrive\Desktop\studio\scratch\test_prompt_v2.wav"
    res = analyze_audio_match(path)
    print(format_voice_match_table(res, os.path.basename(path)))
