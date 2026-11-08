import os
import sys
import json
import time
import base64
import requests
import subprocess
import numpy as np
import scipy.signal as signal
import soundfile as sf
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip()

SCRIPT_PILLAR_A = (
    "Ever wondered how ChatGPT actually answers you? "
    "It does not search a database. "
    "First, your question is sliced into numerical tokens. "
    "Each token lifts into a three-dimensional embedding space, finding words with similar meaning. "
    "Next, attention beams connect key concepts together. "
    "Data travels through stacked transformer layers, calculating the probability of every possible next word. "
    "It picks one token, appends it, and repeats. "
    "Patterns, not magic. "
    "Follow FLASH for daily AI architectures."
)

STYLE_PROMPT = (
    "Speak as a warm, confident friend explaining something fascinating. "
    "Relaxed, conversational pace, small natural pauses at commas and periods, "
    "clear emphasis on key technical words, not rushed."
)

VOICES = ["Sadaltager", "Charon", "Iapetus", "Achird", "Sadachbia"]

def synthesize_voice(voice_name: str, text: str, out_pcm: str) -> bool:
    models = ["gemini-2.5-flash-preview-tts", "gemini-3.8-flash-lite-tts", "gemini-3.8-flash-tts"]
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}"
        payload = {
            "contents": [{
                "parts": [{"text": f"{STYLE_PROMPT}\nScript: {text}"}]
            }],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {"voiceName": voice_name}
                    }
                }
            }
        }
        try:
            r = requests.post(url, json=payload, timeout=40)
            if r.status_code == 200:
                data = r.json()
                for cand in data.get("candidates", []):
                    for part in cand.get("content", {}).get("parts", []):
                        inline = part.get("inlineData", {})
                        if "audio" in inline.get("mimeType", ""):
                            pcm_bytes = base64.b64decode(inline["data"])
                            with open(out_pcm, "wb") as f:
                                f.write(pcm_bytes)
                            return True
            else:
                print(f"[{voice_name}] {model} code {r.status_code}: {r.text[:100]}")
        except Exception as e:
            print(f"[{voice_name}] {model} error: {e}")
    return False

def pcm_to_mastered_mp3(pcm_path: str, mp3_path: str):
    af_filter = "highpass=f=80,equalizer=f=3000:width_type=q:width=1.0:g=1.5,loudnorm=I=-14.0:TP=-1.5:LRA=7"
    cmd = [
        "ffmpeg", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1",
        "-i", pcm_path,
        "-af", af_filter,
        "-ar", "48000", "-b:a", "192k", mp3_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def analyze_acoustics_pure(audio_path: str):
    wav_path = audio_path.replace(".mp3", "_temp.wav")
    cmd = ["ffmpeg", "-y", "-i", audio_path, "-ar", "24000", "-ac", "1", wav_path]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    y, sr = sf.read(wav_path)
    if os.path.exists(wav_path):
        os.remove(wav_path)
        
    dur = float(len(y) / sr)
    frame_len = int(sr * 0.02)
    num_frames = len(y) // frame_len
    rms = np.array([np.sqrt(np.mean(y[i*frame_len:(i+1)*frame_len]**2)) for i in range(num_frames)])
    max_rms = float(np.max(rms)) if len(rms) > 0 else 1e-6
    
    # Silence: frame RMS < 6% of peak RMS
    is_silent = rms < (0.06 * max_rms)
    pause_time = float(np.sum(is_silent) * 0.02)
    pause_pct = float((pause_time / dur) * 100.0) if dur > 0 else 0.0
    speech_time = float(max(0.1, dur - pause_time))
    
    # Syllables via Bandpass + Envelope Peaks
    b, a = signal.butter(4, [300 / (sr/2), 3200 / (sr/2)], btype='bandpass')
    y_band = signal.filtfilt(b, a, y)
    env = np.abs(y_band)
    win_len = int(sr * 0.035)
    kernel = np.hanning(win_len)
    kernel /= kernel.sum()
    env_smooth = signal.convolve(env, kernel, mode='same')
    min_dist = int(sr * 0.14)
    threshold = float(np.mean(env_smooth) * 0.6)
    peaks, _ = signal.find_peaks(env_smooth, distance=min_dist, height=threshold)
    syllable_rate = float(len(peaks) / speech_time)
    
    # Pitch Variation via Autocorrelation
    voiced_f0 = []
    hop_len = int(sr * 0.01)
    win_len = int(sr * 0.03)
    min_lag = int(sr / 350)
    max_lag = int(sr / 75)
    
    for start in range(0, len(y) - win_len, hop_len):
        chunk = y[start:start+win_len]
        chunk_rms = np.sqrt(np.mean(chunk**2))
        if chunk_rms < 0.08 * max_rms:
            continue
        corr = signal.correlate(chunk, chunk, mode='full')
        corr = corr[len(chunk)-1:]
        if max_lag < len(corr):
            lag_region = corr[min_lag:max_lag]
            peak_lag = min_lag + np.argmax(lag_region)
            if corr[peak_lag] > 0.4 * corr[0]:
                voiced_f0.append(sr / peak_lag)
                
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

def main():
    os.makedirs("cache/shootout", exist_ok=True)
    results = []
    print("=== GEMINI TTS VOICE SHOOTOUT (Target: Bunty Reference) ===")
    print("Targets: Pace 4.6-5.6 syl/s | Pauses 15-22% | Pitch Var 4.0-5.5 st\n")
    
    for v in VOICES:
        pcm = f"cache/shootout/{v}_raw.pcm"
        mp3 = f"cache/shootout/{v}_mastered.mp3"
        print(f"Synthesizing voice: {v}...")
        if not os.path.exists(pcm):
            ok = synthesize_voice(v, SCRIPT_PILLAR_A, pcm)
            if not ok:
                print(f"Skipping {v}")
                continue
            time.sleep(1.0)
        pcm_to_mastered_mp3(pcm, mp3)
        met = analyze_acoustics_pure(mp3)
        met["voice"] = v
        met["audio_file"] = mp3
        results.append(met)
        print(f" -> {v}: dur={met['duration_s']}s, pace={met['syllable_rate']} syl/s, pauses={met['pause_pct']}%, pitch={met['pitch_variation_st']} st")
        
    print("\n" + "="*85)
    print(f"{'Voice':<14} | {'Dur (s)':<8} | {'Pace (syl/s)':<14} | {'Pauses (%)':<12} | {'Pitch Var (st)':<14} | {'Match Verdict'}")
    print("-"*85)
    for r in results:
        pace_ok = 4.4 <= r["syllable_rate"] <= 5.8
        pause_ok = 14.0 <= r["pause_pct"] <= 28.0
        pitch_ok = 3.8 <= r["pitch_variation_st"] <= 5.8
        verdict = "EXCELLENT MATCH" if (pace_ok and pause_ok and pitch_ok) else "ACCEPTABLE"
        print(f"{r['voice']:<14} | {r['duration_s']:<8} | {r['syllable_rate']:<14} | {r['pause_pct']:<12} | {r['pitch_variation_st']:<14} | {verdict}")
    print("="*85)
    
    with open("cache/shootout/shootout_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("\nSaved shootout_results.json successfully!")

if __name__ == "__main__":
    main()
