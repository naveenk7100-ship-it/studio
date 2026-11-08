import os
import sys
import subprocess
import numpy as np
import scipy.signal as signal
import soundfile as sf

def analyze_acoustics_pure(audio_path: str):
    # Convert audio to wav if mp3 using ffmpeg
    wav_path = audio_path.replace(".mp3", "_temp.wav")
    cmd = ["ffmpeg", "-y", "-i", audio_path, "-ar", "24000", "-ac", "1", wav_path]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    y, sr = sf.read(wav_path)
    if os.path.exists(wav_path):
        os.remove(wav_path)
        
    dur = float(len(y) / sr)
    
    # 1. RMS & Pauses (20ms frames)
    frame_len = int(sr * 0.02) # 20ms
    num_frames = len(y) // frame_len
    rms = np.array([np.sqrt(np.mean(y[i*frame_len:(i+1)*frame_len]**2)) for i in range(num_frames)])
    
    max_rms = np.max(rms) if len(rms) > 0 else 1e-6
    # Silence: frame RMS < 6% of peak RMS (-24 dB)
    is_silent = rms < (0.06 * max_rms)
    pause_time = np.sum(is_silent) * 0.02
    pause_pct = (pause_time / dur) * 100.0 if dur > 0 else 0.0
    speech_time = max(0.1, dur - pause_time)
    
    # 2. Syllable Nuclei via Bandpass (300 - 3200 Hz) + Envelope Peaks
    b, a = signal.butter(4, [300 / (sr/2), 3200 / (sr/2)], btype='bandpass')
    y_band = signal.filtfilt(b, a, y)
    env = np.abs(y_band)
    
    # Smooth envelope (35ms window)
    win_len = int(sr * 0.035)
    kernel = np.hanning(win_len)
    kernel /= kernel.sum()
    env_smooth = signal.convolve(env, kernel, mode='same')
    
    # Detect peaks with minimum 140ms spacing (typical syllable rate limit)
    min_dist = int(sr * 0.14)
    threshold = np.mean(env_smooth) * 0.6
    peaks, _ = signal.find_peaks(env_smooth, distance=min_dist, height=threshold)
    syllable_rate = len(peaks) / speech_time
    
    # 3. Fundamental Frequency (F0) & Pitch Variation via Autocorrelation
    voiced_f0 = []
    hop_len = int(sr * 0.01) # 10ms hop
    win_len = int(sr * 0.03) # 30ms window
    # Pitch bounds: 75 Hz to 350 Hz
    min_lag = int(sr / 350)
    max_lag = int(sr / 75)
    
    for start in range(0, len(y) - win_len, hop_len):
        chunk = y[start:start+win_len]
        chunk_rms = np.sqrt(np.mean(chunk**2))
        if chunk_rms < 0.08 * max_rms:
            continue # skip unvoiced/quiet
        # Autocorrelation
        corr = signal.correlate(chunk, chunk, mode='full')
        corr = corr[len(chunk)-1:]
        if max_lag < len(corr):
            lag_region = corr[min_lag:max_lag]
            peak_lag = min_lag + np.argmax(lag_region)
            peak_val = corr[peak_lag]
            if peak_val > 0.4 * corr[0]: # voiced
                f0 = sr / peak_lag
                voiced_f0.append(f0)
                
    if len(voiced_f0) > 15:
        med_f0 = np.median(voiced_f0)
        semitones = 12.0 * np.log2(np.array(voiced_f0) / med_f0)
        pitch_variation = float(np.std(semitones))
    else:
        pitch_variation = 0.0
        
    return {
        "duration_s": round(dur, 2),
        "speech_s": round(speech_time, 2),
        "pause_pct": round(pause_pct, 1),
        "num_syllables": int(len(peaks)),
        "syllable_rate": round(syllable_rate, 2),
        "pitch_variation_st": round(pitch_variation, 2)
    }

if __name__ == "__main__":
    test_file = r"C:\Users\navee\OneDrive\Desktop\studio\cache\shootout\Sadaltager_mastered.mp3"
    res = analyze_acoustics_pure(test_file)
    print("Sadaltager analysis:", res)
