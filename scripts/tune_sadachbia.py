import os
import json
import base64
import requests
import subprocess
import soundfile as sf
import numpy as np
import scipy.signal as signal
from dotenv import load_dotenv
import imageio_ffmpeg

load_dotenv(r"C:\Users\navee\OneDrive\Desktop\studio\.env")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

gemini_key = os.getenv("GEMINI_API_KEY")

sample_mixed_script = (
    "Mama! Claude Code v2.1.316 release ayyindi. "
    "Mundu slash compact kodithe summary matrame vachedi, context reset ayyedi kaadu. "
    "Kaani ee kotha update lo automatic compression chala fast ga jaruguthundi. "
    "Official docs lo chusthe memory usage fourty percent thaggindi ani rasaru. "
    "Terminal lo single command tho direct ga run cheyyachu. "
    "Idi dev workflow ni chala clean ga marchuthundi. "
    "Mee coding speed ni double cheyyadaniki FLASH ni follow avvandi!"
)

# Test prompts
prompts = [
    (
        "prompt_v1",
        "friendly, engaging Telugu tech creator talking to a friend, natural Telugu-English mix, lively intonation, slightly slower pace with clear pronunciation, brief natural pauses between ideas"
    ),
    (
        "prompt_v2",
        "natural Telugu tech creator, warm conversational tone, slightly slower deliberate rhythm, rich intonation, brief natural pauses, engaging and confident"
    )
]

for p_name, style_prompt in prompts:
    print(f"\n--- Testing {p_name} ---")
    models = [
        "gemini-3.8-flash-lite-tts",
        "gemini-2.5-flash-preview-tts",
        "gemini-3.1-flash-tts-preview",
        "gemini-3.8-flash-tts"
    ]
    res_data = None
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{style_prompt}\nScript: {sample_mixed_script}"
                }]
            }],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {
                            "voiceName": "Sadachbia"
                        }
                    }
                }
            }
        }
        r = requests.post(url, json=payload, timeout=35)
        if r.status_code == 200:
            print(f"Success with model {model}!")
            res_data = r.json()
            break
        elif r.status_code == 429:
            print(f"Model {model} 429 Quota Exceeded, trying next...")
            continue
        else:
            print(f"Model {model} returned {r.status_code}: {r.text[:120]}")

    pcm_bytes = None
    for cand in res_data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData", {})
            if "audio" in inline.get("mimeType", ""):
                pcm_bytes = base64.b64decode(inline["data"])
                break
                
    if not pcm_bytes:
        print("No audio returned")
        continue
        
    raw_pcm = f"scratch/test_{p_name}.pcm"
    wav_out = f"scratch/test_{p_name}.wav"
    with open(raw_pcm, "wb") as f:
        f.write(pcm_bytes)
        
    cmd = [
        FFMPEG, "-y", "-f", "s16le", "-ar", "24000", "-ac", "1",
        "-i", raw_pcm,
        "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7",
        "-ar", "16000", wav_out
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    if os.path.exists(raw_pcm):
        os.remove(raw_pcm)
        
    # Analyze metrics
    data, sr = sf.read(wav_out)
    total_dur = len(data) / sr
    
    frame_len = int(sr * 0.02)
    step = int(sr * 0.01)
    frames = [data[i:i + frame_len] for i in range(0, len(data) - frame_len, step)]
    frame_rms = np.array([np.sqrt(np.mean(f**2) + 1e-12) for f in frames])
    max_rms = np.max(frame_rms)
    
    silent = (frame_rms < (max_rms * 0.04)).astype(int)
    diffs = np.diff(np.pad(silent, (1, 1), 'constant'))
    starts = np.where(diffs == 1)[0]
    ends = np.where(diffs == -1)[0]
    durations = (ends - starts) * 0.01
    pause_dur = np.sum(durations[durations >= 0.15])
    pause_pct = (pause_dur / total_dur) * 100
    speech_dur = total_dur - pause_dur
    
    # Pitch
    pitches = []
    min_lag = int(sr / 380)
    max_lag = int(sr / 75)
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
    pitch_med = float(np.median(pitches)) if len(pitches) > 0 else 0.0
    semitones = 12 * np.log2(pitches / pitch_med) if len(pitches) > 0 else np.array([0])
    expressiveness = float(np.std(semitones))
    
    # Syllable energy peaks
    analytic = signal.hilbert(data)
    env = np.abs(analytic)
    b, a = signal.butter(2, 8.0 / (sr / 2), btype='low')
    s_env = signal.filtfilt(b, a, env)
    peaks, _ = signal.find_peaks(s_env, distance=int(sr * 0.11), prominence=0.03 * np.max(s_env))
    peaks_per_sec = len(peaks) / speech_dur
    
    print(f"Results for {p_name}:")
    print(f"Total Dur: {total_dur:.2f}s | Speech Dur: {speech_dur:.2f}s")
    print(f"Pitch Median: {pitch_med:.1f} Hz (Ref: 188 Hz)")
    print(f"Expressiveness: {expressiveness:.2f} st (Target: >= 4.5)")
    print(f"Syllable Peaks/sec: {peaks_per_sec:.2f} (Target: 4.6 - 5.6)")
    print(f"Pause Percentage: {pause_pct:.1f}% (Target: 12.0 - 22.0%)")
    
    gate_expressive = expressiveness >= 4.5
    gate_pace = 4.6 <= peaks_per_sec <= 5.6
    gate_pause = 12.0 <= pause_pct <= 22.0
    all_pass = gate_expressive and gate_pace and gate_pause
    print(f"GATE PASS: {all_pass} (Expressive: {gate_expressive}, Pace: {gate_pace}, Pause: {gate_pause})")
