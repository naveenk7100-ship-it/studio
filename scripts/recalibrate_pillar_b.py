import os
import sys
import json
import base64
import requests
import subprocess
from dotenv import load_dotenv

load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# 39-word punchy script for 22.5s speech
SCRIPT_PILLAR_B = (
    "Summarizing research papers with AI? "
    "Never paste messy PDFs directly. "
    "We benchmarked pypdf vs pypdfium2. "
    "Pure Python took 386 milliseconds and scrambled multi-column text. "
    "Google's C++ PDFium parsed it in just 59 milliseconds. "
    "Over six times faster. "
    "Clean context, zero bloat."
)

STYLE_PROMPT = (
    "Speak as a warm, confident friend explaining something fascinating. "
    "Relaxed, conversational pace, small natural pauses at commas and periods, "
    "clear emphasis on key technical words, not rushed."
)

CHOSEN_VOICE = "Sadaltager"

pcm_b = "cache/v5/voice_b_raw.pcm"
mp3_b = "cache/v5/voice_b.mp3"
mix_b = "cache/v5/master_pillar_b.mp3"
meta_b = "cache/v5/music_meta_b.json"
cap_b = "cache/v5/captions_pillar_b.json"

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key={GEMINI_KEY}"
payload = {
    "contents": [{"parts": [{"text": f"{STYLE_PROMPT}\nScript: {SCRIPT_PILLAR_B}"}]}],
    "generationConfig": {
        "responseModalities": ["AUDIO"],
        "speechConfig": {
            "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": CHOSEN_VOICE}}
        }
    }
}
r = requests.post(url, json=payload, timeout=40)
data = r.json()
for cand in data.get("candidates", []):
    for part in cand.get("content", {}).get("parts", []):
        inline = part.get("inlineData", {})
        if "audio" in inline.get("mimeType", ""):
            with open(pcm_b, "wb") as f:
                f.write(base64.b64decode(inline["data"]))
            break

# Convert to MP3 with mastering
af = "highpass=f=80,equalizer=f=3000:width_type=q:width=1.0:g=1.5,loudnorm=I=-14.0:TP=-1.5:LRA=7"
cmd = [
    "ffmpeg", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1",
    "-i", pcm_b,
    "-af", af,
    "-ar", "48000", "-b:a", "192k", mp3_b
]
subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Procedural music mix
from procedural_music_engine import render_procedural_track
render_procedural_track(mp3_b, mix_b, meta_b)

# Word timestamps
from faster_whisper import WhisperModel
model = WhisperModel("base", device="cpu", compute_type="int8")
segments, _ = model.transcribe(mp3_b, word_timestamps=True)

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

with open(cap_b, "w", encoding="utf-8") as f:
    json.dump(captions, f, indent=2)

print(f"Pillar B calibrated! Final word ends at: {captions[-1]['end']}s")
