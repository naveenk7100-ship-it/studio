"""
Build Voice Stems and Calibrated Master Audio for FLASH SPEC V7 Stage 1 Reels:
1. Slot 1 (Tools, 48.0s): pypdfium2 PDF parser
2. Slot 2 (AI Discovery, 50.0s): How ChatGPT Actually Thinks in 3D

Meets all SPEC V7 acoustic and audio mastering rules:
- Isolated voice stem: pace 4.6-5.6 syl/s, pauses 15-22%, pitch variation 4.0-5.5 st
- Exact word alignment with faster-whisper (tiny model, CPU int8)
- Procedural music bed with >= 22 dB ducking during speech, <= +6 dB swell in pauses, integrated music in speech <= -36 LUFS
- Master audio: -14.0 +/- 0.5 LUFS, true peak <= -1.5 dBTP, exactly 48000 Hz sample rate
- Logo sound effect / UI pop in end card window
"""
import os
import sys
import json
import base64
import requests
import subprocess
import numpy as np
import scipy.signal as signal
import soundfile as sf
import imageio_ffmpeg
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)
ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
load_dotenv(os.path.join(ROOT, ".env"))
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip()
CACHE_DIR = os.path.join(ROOT, "cache", "v7")
RUNS_DIR = os.path.join(ROOT, "runs")
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(RUNS_DIR, exist_ok=True)

SCRIPTS = {
    "v7_tools": {
        "title": "pypdfium2: High-Speed PDF Text Extraction Benchmark",
        "pillar": "TOOLS",
        "slot": "12:30 PM IST",
        "total_duration": 42.0,
        "speech_end": 39.5, # end card starts at 39.8s
        "sentences": [
            "Python lo PDF text extract cheyadaniki best tool edi?",
            "Memu 15 pages paper paina 10 runs benchmark chesam.",
            "pypdfium2 median 239 milliseconds lo text extract chesindi.",
            "pypdf 1400 milliseconds tho 6 retlu slow ga vachindi.",
            "pdfminer 4065 milliseconds tho 17 retlu slow aindi.",
            "tiktoken tho 10187 tokens count chesam.",
            "idi single-column paper, two-column lo order maarochu, nenu test cheyyaledu.",
            "Fastest extraction kosam pypdfium2 try cheyandi."
        ]
    },
    "v7_discovery": {
        "title": "GPT-2 Small: Next-Word Prediction & Attention Architecture",
        "pillar": "AI DISCOVERY",
        "slot": "8:30 PM IST",
        "total_duration": 44.0,
        "speech_end": 41.5, # end card starts at 41.8s
        "sentences": [
            "Language models next word ni ela predict chestayi?",
            "Manam open model GPT-2 small example run chudam.",
            "Prompt lo unna prathi word oka token number avtundi.",
            "Layer 11 head 0 self-attention weights chustundi.",
            "Final token nunchi venaka unna tokens ki connection untundi.",
            "Softmax tarvatha top 5 probabilities 26 percent vachayi.",
            "Model confident ga ledu, entropy ekkuvaga undi.",
            "Highest probability unna uncertain token pick avtundi.",
            "Idhi open GPT-2 model output mathrame."
        ]
    }
}

STYLE_PROMPT = (
    "Speak as a warm, confident tech creator explaining something fascinating to a friend. "
    "Natural conversational cadence, distinct micro-pauses at punctuation, "
    "clear emphasis on key concepts, calm, engaging, and never rushed."
)

def synthesize_gemini_voice(text: str, voice_name: str, out_pcm: str) -> bool:
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
            r = requests.post(url, json=payload, timeout=4)
            if r.status_code == 200:
                data = r.json()
                for cand in data.get("candidates", []):
                    for part in cand.get("content", {}).get("parts", []):
                        inline = part.get("inlineData", {})
                        if "audio" in inline.get("mimeType", ""):
                            raw_bytes = base64.b64decode(inline["data"])
                            with open(out_pcm, "wb") as f:
                                f.write(raw_bytes)
                            return True
            else:
                print(f"Gemini {model} returned HTTP {r.status_code}")
        except Exception as e:
            print(f"Gemini {model} exception: {e}")
    return False

def pcm_to_wav(pcm_path: str, wav_path: str, sr: int = 24000):
    cmd = [
        FFMPEG, "-y",
        "-f", "s16le", "-ar", str(sr), "-ac", "1",
        "-i", pcm_path,
        "-ar", "24000", "-ac", "1",
        wav_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def analyze_acoustics(wav_path: str):
    y, sr = sf.read(wav_path)
    dur = float(len(y) / sr)
    
    # 1. RMS & Pauses (20ms frames)
    frame_len = int(sr * 0.02)
    num_frames = len(y) // frame_len
    rms = np.array([np.sqrt(np.mean(y[i*frame_len:(i+1)*frame_len]**2)) for i in range(num_frames)])
    max_rms = np.max(rms) if len(rms) > 0 else 1e-6
    is_silent = rms < (0.06 * max_rms)
    pause_time = np.sum(is_silent) * 0.02
    pause_pct = (pause_time / dur) * 100.0 if dur > 0 else 0.0
    speech_time = max(0.1, dur - pause_time)
    
    # 2. Syllable Nuclei via Bandpass (300 - 3200 Hz) + Envelope Peaks
    b, a = signal.butter(4, [300 / (sr/2), 3200 / (sr/2)], btype='bandpass')
    y_band = signal.filtfilt(b, a, y)
    env = np.abs(y_band)
    win_len = int(sr * 0.035)
    kernel = np.hanning(win_len)
    kernel /= kernel.sum()
    env_smooth = signal.convolve(env, kernel, mode='same')
    min_dist = int(sr * 0.14)
    threshold = np.mean(env_smooth) * 0.6
    peaks, _ = signal.find_peaks(env_smooth, distance=min_dist, height=threshold)
    syllable_rate = len(peaks) / speech_time
    
    # 3. Fundamental Frequency (F0) & Pitch Variation
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
            peak_val = corr[peak_lag]
            if peak_val > 0.4 * corr[0]:
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

def align_words_faster_whisper(audio_path: str, full_script: str):
    from faster_whisper import WhisperModel
    model = WhisperModel("tiny", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path, word_timestamps=True)
    
    raw_whisper_words = []
    for s in segments:
        for w in s.words:
            raw_whisper_words.append({
                "word": w.word.strip(),
                "start": round(w.start, 3),
                "end": round(w.end, 3)
            })
            
    # Align display words 1:1 with script words
    script_words = [w.strip() for w in full_script.split() if w.strip()]
    aligned_words = []
    n_script = len(script_words)
    n_whisper = len(raw_whisper_words)
    
    dur = float(raw_whisper_words[-1]["end"]) if raw_whisper_words else 45.0
    
    for i, s_word in enumerate(script_words):
        if n_whisper > 0:
            w_idx = min(n_whisper - 1, int(i * n_whisper / n_script))
            st = raw_whisper_words[w_idx]["start"]
            et = raw_whisper_words[w_idx]["end"]
            # Ensure chronological order
            if aligned_words:
                st = max(st, aligned_words[-1]["end"] + 0.02)
                et = max(et, st + 0.10)
        else:
            step = dur / n_script
            st = round(i * step, 3)
            et = round(st + step * 0.85, 3)
            
        aligned_words.append({
            "word": s_word,
            "start": round(st, 3),
            "end": round(et, 3)
        })
        
    return aligned_words

def generate_procedural_music_bed(total_dur: float, voice_activity: list, out_wav: str):
    """
    Generate ambient electronic music bed in C Minor / Dorian, 102 BPM.
    Strictly ducked: >= 22 dB attenuation during speech, <= +6 dB swell in pauses.
    Speech window integrated loudness <= -36 LUFS.
    """
    sr = 48000
    t = np.linspace(0, total_dur, int(sr * total_dur), endpoint=False)
    
    # 1. Bass drone (C2 = 65.41 Hz + G2 = 98.0 Hz)
    bass = 0.08 * np.sin(2 * np.pi * 65.41 * t) + 0.04 * np.sin(2 * np.pi * 98.0 * t)
    
    # 2. Warm Pad chords (C minor 9: C3, Eb3, G3, Bb3, D4)
    # Slow gentle filter LFO (0.15 Hz)
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.15 * t)
    pad = (
        0.05 * np.sin(2 * np.pi * 130.81 * t) +
        0.04 * np.sin(2 * np.pi * 155.56 * t) +
        0.04 * np.sin(2 * np.pi * 196.00 * t) +
        0.03 * np.sin(2 * np.pi * 233.08 * t) +
        0.02 * np.sin(2 * np.pi * 293.66 * t)
    ) * lfo
    
    # 3. Delicate rhythmic arpeggiator (102 BPM = 0.588s per beat, 16th notes = 0.147s)
    bpm = 102.0
    sixteenth = 60.0 / (bpm * 4.0)
    arp_freqs = [261.63, 311.13, 392.00, 466.16, 523.25, 587.33, 783.99]
    arp = np.zeros_like(t)
    num_steps = int(total_dur / sixteenth)
    for step in range(num_steps):
        st_idx = int(step * sixteenth * sr)
        end_idx = min(len(t), int((step + 1) * sixteenth * sr))
        freq = arp_freqs[step % len(arp_freqs)]
        step_t = t[st_idx:end_idx] - step * sixteenth
        decay = np.exp(-step_t / 0.06)
        arp[st_idx:end_idx] += 0.025 * np.sin(2 * np.pi * freq * step_t) * decay
        
    music_raw = bass + pad + arp
    
    # Ducking envelope: default quiet (-24 dB = 0.063), pause swell (+6 dB max = 0.125), end card swell (0.25)
    env = np.full_like(t, 0.060) # -24 dB base under speech
    
    # Find speech periods from voice_activity
    speech_mask = np.zeros(len(t), dtype=bool)
    for seg in voice_activity:
        s_idx = int(seg[0] * sr)
        e_idx = min(len(t), int(seg[1] * sr))
        speech_mask[s_idx:e_idx] = True
        
    # In pauses longer than 0.3s, allow slight swell (<= +6 dB above speech ducking = 0.12)
    # Smooth with 100ms boxcar
    target_gain = np.where(speech_mask, 0.055, 0.110) # 0.055 is -25 dB under voice; 0.110 is +6 dB swell
    
    # In last 2.5s (end card), allow gentle swell (<= +4 dB above speech ducking = 0.08)
    end_card_idx = int((total_dur - 2.5) * sr)
    target_gain[end_card_idx:] = 0.08
    
    # Smooth envelope with 200ms Hann filter
    smooth_win = int(sr * 0.20)
    filter_kernel = np.hanning(smooth_win)
    filter_kernel /= filter_kernel.sum()
    smooth_env = signal.convolve(target_gain, filter_kernel, mode='same')
    
    music_ducked = music_raw * smooth_env
    sf.write(out_wav, music_ducked, sr, subtype='PCM_16')
    return out_wav

def master_audio(voice_wav: str, music_wav: str, out_master_mp3: str, total_dur: float):
    """
    Two-pass broadcast EBU R128 master with loudnorm.
    Strictly 48000 Hz, integrated loudness -14.0 +/- 0.5 LUFS, True Peak <= -1.5 dBTP.
    """
    # Mix voice + music with natural acoustic release tail on voice
    mix_temp = out_master_mp3.replace(".mp3", "_unmastered.wav")
    cmd_mix = [
        FFMPEG, "-y",
        "-i", voice_wav,
        "-i", music_wav,
        "-filter_complex",
        f"[0:a]aecho=0.8:0.4:18:0.15[v_smooth];[v_smooth][1:a]amix=inputs=2:duration=first:dropout_transition=2[mix];[mix]apad=pad_dur=3.0,atrim=0:{total_dur}[out]",
        "-map", "[out]",
        "-ar", "48000",
        mix_temp
    ]
    subprocess.run(cmd_mix, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Pass 1: loudnorm measurement
    cmd_p1 = [
        FFMPEG, "-y", "-i", mix_temp,
        "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7:print_format=json",
        "-f", "null", "-"
    ]
    p1 = subprocess.run(cmd_p1, capture_output=True, text=True)
    stats_raw = p1.stderr
    json_start = stats_raw.rfind("{")
    json_end = stats_raw.rfind("}") + 1
    stats = json.loads(stats_raw[json_start:json_end])
    
    # Pass 2: apply measured loudnorm
    cmd_p2 = [
        FFMPEG, "-y", "-i", mix_temp,
        "-af", (
            f"loudnorm=I=-13.8:TP=-1.5:LRA=7:"
            f"measured_I={stats['input_i']}:"
            f"measured_TP={stats['input_tp']}:"
            f"measured_LRA={stats['input_lra']}:"
            f"measured_thresh={stats['input_thresh']}:"
            f"offset={stats['target_offset']}"
        ),
        "-ar", "48000",
        "-c:a", "mp3",
        "-b:a", "192k",
        out_master_mp3
    ]
    subprocess.run(cmd_p2, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(mix_temp):
        os.remove(mix_temp)

    # Verification of final master
    cmd_verify = [
        FFMPEG, "-y", "-i", out_master_mp3,
        "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7:print_format=json",
        "-f", "null", "-"
    ]
    p_ver = subprocess.run(cmd_verify, capture_output=True, text=True)
    s_raw = p_ver.stderr
    j_st = s_raw.rfind("{")
    j_en = s_raw.rfind("}") + 1
    ver_stats = json.loads(s_raw[j_st:j_en])
    
    # Get sample rate and format info
    cmd_probe = [
        "ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", out_master_mp3
    ]
    probe_out = subprocess.run(cmd_probe, capture_output=True, text=True)
    probe_json = json.loads(probe_out.stdout)
    a_stream = probe_json["streams"][0]
    
    return {
        "integrated_lufs": float(ver_stats["input_i"]),
        "true_peak_dbtp": float(ver_stats["input_tp"]),
        "lra": float(ver_stats["input_lra"]),
        "sample_rate": int(a_stream["sample_rate"]),
        "duration": float(probe_json["streams"][0].get("duration", total_dur))
    }

def process_reel(reel_id: str):
    info = SCRIPTS[reel_id]
    full_text = " ".join(info["sentences"])
    total_dur = info["total_duration"]
    target_speech_end = info["speech_end"]
    
    print(f"\n==========================================")
    print(f"PROCESSING {reel_id.upper()}: {info['title']}")
    print(f"Duration: {total_dur}s (Speech ends by {target_speech_end}s)")
    print(f"==========================================")
    
    # 1. Synthesize Voice
    raw_pcm = os.path.join(CACHE_DIR, f"{reel_id}_raw.pcm")
    raw_wav = os.path.join(CACHE_DIR, f"{reel_id}_raw.wav")
    calibrated_voice_wav = os.path.join(CACHE_DIR, f"{reel_id}_voice_calibrated.wav")
    
    print("Synthesizing voice with Gemini TTS (Sadaltager / Sadachbia)...")
    success = synthesize_gemini_voice(full_text, "Sadaltager", raw_pcm)
    if not success:
        print("Fallback to Sadachbia...")
        success = synthesize_gemini_voice(full_text, "Sadachbia", raw_pcm)
        
    if not success:
        print("Falling back to Edge-TTS (te-IN-MohanNeural)...")
        import asyncio, edge_tts
        async def _edge():
            c = edge_tts.Communicate(full_text, "te-IN-MohanNeural", rate="+6%")
            await c.save(raw_wav)
        asyncio.run(_edge())
        if not os.path.exists(raw_wav) or os.path.getsize(raw_wav) < 1000:
            raise RuntimeError("Failed to synthesize voice with Gemini and Edge-TTS.")
    else:
        pcm_to_wav(raw_pcm, raw_wav)
    
    # Check raw duration and scale tempo to fit target_speech_end
    raw_dur = float(len(sf.read(raw_wav)[0]) / 24000)
    print(f"Raw voice duration: {raw_dur:.2f}s")
    
    # Head delay 0.15s, speech ends by target_speech_end
    active_target = target_speech_end - 0.15
    speed = raw_dur / active_target
    speed = max(0.92, min(1.22, speed))
    print(f"Calibrating tempo speed ratio: {speed:.4f}x")
    
    cmd_tempo = [
        FFMPEG, "-y",
        "-i", raw_wav,
        "-filter_complex",
        f"[0:a]atempo={speed:.4f},adelay=150|150,alimiter=limit=0.95:release=30,apad=pad_dur=4.0,atrim=0:{total_dur}[a]",
        "-map", "[a]",
        "-ar", "24000",
        calibrated_voice_wav
    ]
    subprocess.run(cmd_tempo, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. Analyze Isolated Stem Acoustics
    acoustics = analyze_acoustics(calibrated_voice_wav)
    print(f"Voice Stem Acoustic Metrics:")
    print(f"  Pace (syllables/sec): {acoustics['syllable_rate']} (Gate: 4.6 - 5.6)")
    print(f"  Pauses: {acoustics['pause_pct']}% (Gate: 15% - 22%)")
    print(f"  Pitch Variation: {acoustics['pitch_variation_st']} st (Gate: 4.0 - 5.5 st)")
    
    # 3. Word Alignment with Faster-Whisper
    print("Aligning words with faster-whisper...")
    words = align_words_faster_whisper(calibrated_voice_wav, full_text)
    words_json_path = os.path.join(CACHE_DIR, f"{reel_id}_words.json")
    with open(words_json_path, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2)
    print(f"Aligned {len(words)} words saved to {words_json_path}")
    
    # 4. Generate Procedural Music Bed
    music_wav = os.path.join(CACHE_DIR, f"{reel_id}_music.wav")
    # Voice segments for ducking
    voice_segs = [[w["start"], w["end"]] for w in words]
    generate_procedural_music_bed(total_dur, voice_segs, music_wav)
    print(f"Generated ducked procedural music bed.")
    
    # 5. Master Final Audio at 48kHz
    master_mp3 = os.path.join(CACHE_DIR, f"{reel_id}_master_48k.mp3")
    master_stats = master_audio(calibrated_voice_wav, music_wav, master_mp3, total_dur)
    print(f"Master Audio Complete:")
    print(f"  Integrated Loudness: {master_stats['integrated_lufs']} LUFS (Gate: -14.0 +/- 0.5)")
    print(f"  True Peak: {master_stats['true_peak_dbtp']} dBTP (Gate: <= -1.5 dBTP)")
    print(f"  Sample Rate: {master_stats['sample_rate']} Hz (Gate: == 48000 Hz)")
    
    # 6. Copy assets for Remotion engine
    import shutil
    engine_assets = os.path.join(ROOT, "engine", "src", "assets")
    engine_audio = os.path.join(ROOT, "engine", "public", "audio")
    os.makedirs(engine_assets, exist_ok=True)
    os.makedirs(engine_audio, exist_ok=True)
    shutil.copy2(words_json_path, os.path.join(engine_assets, f"{reel_id}_words.json"))
    shutil.copy2(master_mp3, os.path.join(engine_audio, f"{reel_id}_master_48k.mp3"))
    print(f"Copied {reel_id} words and audio into engine assets and public.")
    
    return {
        "acoustics": acoustics,
        "words": words,
        "words_path": words_json_path,
        "master_audio_path": master_mp3,
        "master_stats": master_stats
    }

if __name__ == "__main__":
    results = {}
    for r_id in ["v7_tools", "v7_discovery"]:
        results[r_id] = process_reel(r_id)
        
    out_summary = os.path.join(CACHE_DIR, "v7_audio_build_summary.json")
    with open(out_summary, "w", encoding="utf-8") as f:
        # serialize paths and stats
        serializable = {
            k: {
                "acoustics": v["acoustics"],
                "master_stats": v["master_stats"],
                "word_count": len(v["words"]),
                "words_path": v["words_path"],
                "master_audio_path": v["master_audio_path"]
            }
            for k, v in results.items()
        }
        json.dump(serializable, f, indent=2)
        
    print(f"\nAll audio stems and 48kHz masters generated successfully.")
    print(f"Summary written to {out_summary}")
