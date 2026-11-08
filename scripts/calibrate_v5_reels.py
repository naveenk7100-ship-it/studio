import os
import sys
import json
import time
import base64
import requests
import subprocess
import numpy as np
import soundfile as sf
import scipy.signal as signal
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# Calibrated scripts (45 - 55 words) to hit ~24.5s speech at 5.0 syl/s (Bunty pace)
SCRIPT_PILLAR_A = (
    "Ever wondered how ChatGPT actually answers? "
    "It does not search a database. "
    "Your question is sliced into numerical tokens. "
    "Each token enters a three-dimensional embedding space, finding related concepts. "
    "Attention beams calculate context, while transformer layers predict the next most probable word. "
    "Patterns, not magic."
)

SCRIPT_PILLAR_B = (
    "Summarizing research papers with AI? "
    "Never paste messy PDFs directly into chat. "
    "We benchmarked pypdf, pdfminer, and pypdfium2. "
    "Pure Python parsers took nearly 400 milliseconds and scrambled multi-column text. "
    "The winner is pypdfium2, powered by Google's C++ PDFium engine. "
    "It parsed five pages in just 59 milliseconds—over six times faster. "
    "Clean context, zero bloat."
)

STYLE_PROMPT = (
    "Speak as a warm, confident friend explaining something fascinating. "
    "Relaxed, conversational pace, small natural pauses at commas and periods, "
    "clear emphasis on key technical words, not rushed."
)

CHOSEN_VOICE = "Sadaltager"

def synthesize(text: str, pcm_path: str):
    models = ["gemini-2.5-flash-preview-tts", "gemini-3.8-flash-lite-tts", "gemini-3.8-flash-tts"]
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}"
        payload = {
            "contents": [{"parts": [{"text": f"{STYLE_PROMPT}\nScript: {text}"}]}],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": CHOSEN_VOICE}}
                }
            }
        }
        r = requests.post(url, json=payload, timeout=40)
        if r.status_code == 200:
            data = r.json()
            for cand in data.get("candidates", []):
                for part in cand.get("content", {}).get("parts", []):
                    inline = part.get("inlineData", {})
                    if "audio" in inline.get("mimeType", ""):
                        with open(pcm_path, "wb") as f:
                            f.write(base64.b64decode(inline["data"]))
                        return True
    return False

def pcm_to_mp3(pcm_path: str, mp3_path: str):
    af = "highpass=f=80,equalizer=f=3000:width_type=q:width=1.0:g=1.5,loudnorm=I=-14.0:TP=-1.5:LRA=7"
    cmd = [
        "ffmpeg", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1",
        "-i", pcm_path,
        "-af", af,
        "-ar", "48000", "-b:a", "192k", mp3_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def align_captions(audio_path: str):
    from faster_whisper import WhisperModel
    print(f"[WHISPER] Aligning word timestamps for {audio_path}...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, _ = model.transcribe(audio_path, word_timestamps=True)
    
    captions = []
    current_phrase = []
    phrase_start = None
    
    for seg in segments:
        for w in seg.words:
            clean_word = w.word.strip()
            if not clean_word:
                continue
            if phrase_start is None:
                phrase_start = w.start
            current_phrase.append(clean_word)
            
            is_break = any(p in clean_word for p in [".", ",", "?", "!"]) or len(current_phrase) >= 4
            if is_break:
                captions.append({
                    "start": round(phrase_start, 2),
                    "end": round(w.end, 2),
                    "text": " ".join(current_phrase)
                })
                current_phrase = []
                phrase_start = None
                
    if current_phrase and phrase_start is not None:
        captions.append({
            "start": round(phrase_start, 2),
            "end": round(w.end, 2),
            "text": " ".join(current_phrase)
        })
        
    return captions

def main():
    os.makedirs("cache/v5", exist_ok=True)
    from procedural_music_engine import render_procedural_track
    
    # --- REEL 1: PILLAR A ---
    print("\n--- PROCESSING PILLAR A: HOW CHATGPT WORKS (CALIBRATED) ---")
    pcm_a = "cache/v5/voice_a_raw.pcm"
    mp3_a = "cache/v5/voice_a.mp3"
    mix_a = "cache/v5/master_pillar_a.mp3"
    meta_a = "cache/v5/music_meta_a.json"
    cap_a = "cache/v5/captions_pillar_a.json"
    
    synthesize(SCRIPT_PILLAR_A, pcm_a)
    pcm_to_mp3(pcm_a, mp3_a)
    render_procedural_track(mp3_a, mix_a, meta_a)
    caps_a = align_captions(mp3_a)
    with open(cap_a, "w", encoding="utf-8") as f:
        json.dump(caps_a, f, indent=2)
    last_word_a = caps_a[-1]["end"] if caps_a else 0
    print(f"Pillar A captions: {len(caps_a)} phrases. Last word ends at {last_word_a}s")

    # --- REEL 2: PILLAR B ---
    print("\n--- PROCESSING PILLAR B: BEST TOOL FOR JOB (CALIBRATED) ---")
    pcm_b = "cache/v5/voice_b_raw.pcm"
    mp3_b = "cache/v5/voice_b.mp3"
    mix_b = "cache/v5/master_pillar_b.mp3"
    meta_b = "cache/v5/music_meta_b.json"
    cap_b = "cache/v5/captions_pillar_b.json"
    
    synthesize(SCRIPT_PILLAR_B, pcm_b)
    pcm_to_mp3(pcm_b, mp3_b)
    render_procedural_track(mp3_b, mix_b, meta_b)
    caps_b = align_captions(mp3_b)
    with open(cap_b, "w", encoding="utf-8") as f:
        json.dump(caps_b, f, indent=2)
    last_word_b = caps_b[-1]["end"] if caps_b else 0
    print(f"Pillar B captions: {len(caps_b)} phrases. Last word ends at {last_word_b}s")

if __name__ == "__main__":
    main()
