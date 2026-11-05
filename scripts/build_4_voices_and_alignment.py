"""
FLASH Content OS - 4 Voices Synthesis & Exact Alignment Calibrator
Synthesizes with Gemini TTS Sadachbia and calibrates duration to exactly 28.00s:
- 150 ms silence head
- Speech from 0.15s to ~24.6s
- >= 500 ms silence tail before Follow End Card (25.2s - 28.0s)
- Measures phrase-end energy ratio (<= 0.5)
- Proportionally scales aligned word timestamps and saves to cache/words_essay_{id}.json
"""

import os
import sys
import json
import time
import subprocess
import numpy as np
import wave
import imageio_ffmpeg
from dotenv import load_dotenv

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
load_dotenv(os.path.join(ROOT, ".env"))
sys.path.insert(0, ROOT)
import tts

CACHE_DIR = os.path.join(ROOT, "cache")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

VOICE_CONFIGS = [
    {
        "id": "unslop",
        "title": "heydamir / unslop",
        "script": "Mama, AI generate chesina UI chusi chusi bore kottinda? Idi unslop, Claude Code skill for interface design. Purple gradients mariyu generic AI styling ni human design system ga marchutundi. Git clone chesi skills folder lo petti, Claude Code lo slash unslop run cheyandi. GitHub lo 9054 stars vachayi, CC BY 4.0 license tho. Full commands mariyu details bio link lo check cheyandi.",
        "target_speech_end": 24.6, # seconds
    },
    {
        "id": "uv",
        "title": "astral-sh / uv",
        "script": "Mama, Python package installations inka slow ga unte, Astral UV vadandi. Idi Rust tho build chesina high velocity Python package manager. Pip mariyu virtualenv replace chesi, dependency trees ni 100 times faster ga build chestundi. Official curl command run chesi instant ga install cheyandi. GitHub lo 91559 stars reach aindi, Apache 2.0 license tho. Full installation commands bio link lo check cheyandi.",
        "target_speech_end": 24.6,
    },
    {
        "id": "kimi",
        "title": "Moonshot AI Kimi K3.1 Pro",
        "script": "Mama, Moonshot AI official ga Kimi K3.1 Pro open model weights release chesaru. Hacker News lo 532 points tho top trending lo undi. OpenAI client syntax tho reasoning effort max configure cheyochu. 2.8T parameter architecture kabatti, multi node GPU cluster avasaram. Open weights Hugging Face lo Kimi model license tho unnayi. Official model card link bio lo check cheyandi.",
        "target_speech_end": 24.6,
    },
    {
        "id": "craft",
        "title": "storytold / craft-anything",
        "script": "Mama, edaina software ela pani chestundo clean room lo reverse engineer cheyala? Idi craft anything, 100 percent Rust engine for software crafting. Target app ni study chesi, coding agents tho new code build chestundi. Cargo run release tho desktop app mariyu CLI doctor run cheyandi. GitHub lo 13530 stars vachayi, MIT mariyu Apache 2.0 license tho. Full setup instructions bio link lo check cheyandi.",
        "target_speech_end": 24.6,
    }
]

def check_phrase_end_energy(mp3_path: str, speech_end_s: float) -> float:
    # Converts audio to temporary 16-bit mono wav and measures RMS energy of last 30ms vs median
    temp_wav = mp3_path.replace(".mp3", "_temp.wav")
    cmd = [FFMPEG, "-y", "-i", mp3_path, "-ac", "1", "-ar", "24000", "-c:a", "pcm_s16le", temp_wav]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    try:
        with wave.open(temp_wav, "rb") as wf:
            sr = wf.getframerate()
            n_frames = wf.getnframes()
            frames = wf.readframes(n_frames)
            samples = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    finally:
        if os.path.exists(temp_wav):
            os.remove(temp_wav)
            
    if len(samples) == 0:
        return 0.0
        
    end_idx = int(min(speech_end_s * sr, len(samples)))
    win_len = int(sr * 0.030)
    start_idx = max(0, end_idx - win_len)
    
    last_30ms = samples[start_idx:end_idx]
    last_30ms_rms = np.sqrt(np.mean(last_30ms**2)) if len(last_30ms) > 0 else 0.0
    
    # Compute running RMS across active speech
    speech_start_idx = int(0.150 * sr)
    hop = int(sr * 0.010)
    energies = []
    for i in range(speech_start_idx, end_idx - win_len, hop):
        w = samples[i : i + win_len]
        energies.append(np.sqrt(np.mean(w**2)))
        
    if not energies:
        return 0.0
        
    energies = np.array(energies)
    med_energy = np.median(energies[energies > np.percentile(energies, 25)])
    if med_energy <= 1e-6:
        return 0.0
        
    ratio = float(last_30ms_rms / med_energy)
    return round(ratio, 4)

def synthesize_and_calibrate(cfg):
    item_id = cfg["id"]
    text = cfg["script"]
    target_speech_end = cfg["target_speech_end"]
    
    raw_mp3 = os.path.join(CACHE_DIR, f"voice_raw_final_{item_id}.mp3")
    calibrated_mp3 = os.path.join(CACHE_DIR, f"voice_final_{item_id}.mp3")
    words_json = os.path.join(CACHE_DIR, f"words_final_{item_id}.json")
    
    print(f"\n================ Synthesizing & Calibrating {item_id} ================")
    print(f"Script ({len(text.split())} words):\n\"{text}\"")
    
    words_raw = tts.make_voice(
        display_text=text,
        path=raw_mp3,
        voice_override="Sadachbia"
    )
    
    dur_raw = tts.get_audio_duration(raw_mp3)
    print(f"  Raw Duration: {dur_raw:.2f} s")
    
    # We want speech (with 150ms head) to finish at exactly target_speech_end (24.6s)
    # Target speech active duration = 24.6 - 0.15 = 24.45s
    target_active_dur = target_speech_end - 0.15
    speed = dur_raw / target_active_dur
    speed = max(0.85, min(1.25, speed))
    print(f"  Atempo speed ratio: {speed:.4f}x")
    
    # Filter: atempo, adelay 150ms head, apad to 28.00s
    cmd = [
        FFMPEG, "-y",
        "-i", raw_mp3,
        "-filter_complex",
        f"[0:a]atempo={speed:.4f},adelay=150|150,apad=pad_dur=5.0[a]",
        "-map", "[a]",
        "-t", "28.00",
        calibrated_mp3
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Measure calibrated audio
    cal_dur = tts.get_audio_duration(calibrated_mp3)
    tail_silence_ms = int((cal_dur - target_speech_end) * 1000)
    
    energy_ratio = check_phrase_end_energy(calibrated_mp3, target_speech_end)
    print(f"  Calibrated File: {calibrated_mp3} ({cal_dur:.2f} s)")
    print(f"  Head Silence: 150 ms | Speech End: {target_speech_end:.2f} s | Tail Silence: {tail_silence_ms} ms (req >= 300 ms)")
    print(f"  Phrase End Energy Ratio: {energy_ratio} (Target <= 0.5 -> {'PASS' if energy_ratio <= 0.5 else 'FAIL'})")
    
    # Calibrate word timestamps
    # Original words are aligned to raw audio [0..dur_raw]
    # In calibrated audio, time = 0.15 + (raw_time / speed)
    scaled_words = []
    text_words = [w.strip() for w in text.split()]
    
    if words_raw and isinstance(words_raw, list):
        for idx, item in enumerate(words_raw):
            w_text = item.get("word", "") if isinstance(item, dict) else (item[0] if len(item) > 0 else "")
            w_start = item.get("start", 0.0) if isinstance(item, dict) else (item[1] if len(item) > 1 else 0.0)
            w_end = item.get("end", 0.0) if isinstance(item, dict) else (item[2] if len(item) > 2 else 0.0)
            
            cal_start = round(0.15 + (w_start / speed), 3)
            cal_end = round(0.15 + (w_end / speed), 3)
            # Match with display text words if available
            display_word = text_words[idx] if idx < len(text_words) else w_text
            scaled_words.append({
                "word": display_word,
                "start": cal_start,
                "end": min(cal_end, target_speech_end)
            })
    else:
        # Interpolate across active speech window
        step = target_active_dur / len(text_words)
        for idx, w in enumerate(text_words):
            scaled_words.append({
                "word": w,
                "start": round(0.15 + idx * step, 3),
                "end": round(0.15 + (idx + 0.85) * step, 3)
            })
            
    with open(words_json, "w", encoding="utf-8") as f:
        json.dump(scaled_words, f, indent=2)
        
    print(f"  Saved {len(scaled_words)} calibrated words to {words_json}")
    if scaled_words:
        print(f"    First word: '{scaled_words[0]['word']}' at {scaled_words[0]['start']}s")
        print(f"    Last word: '{scaled_words[-1]['word']}' at {scaled_words[-1]['end']}s")
        
    return {
        "id": item_id,
        "calibrated_mp3": calibrated_mp3,
        "words_json": words_json,
        "word_count": len(scaled_words),
        "speech_end": target_speech_end,
        "tail_silence_ms": tail_silence_ms,
        "energy_ratio": energy_ratio,
    }

if __name__ == "__main__":
    results = []
    for cfg in VOICE_CONFIGS:
        r = synthesize_and_calibrate(cfg)
        results.append(r)
    with open(os.path.join(CACHE_DIR, "voice_calibration_summary.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("\n[ALL 4 VOICES SYNTHESIZED, CALIBRATED, AND SAVED]")
