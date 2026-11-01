"""Voice synthesis and word-timestamp alignment.

Engine Hierarchy:
1. ElevenLabs (voice Bunty / library voice; speed 0.95, stability 0.60, similarity 0.30; handles 402 gracefully)
2. Gemini TTS (gemini-2.5-flash-preview-tts; warm Indian customer-support Tenglish) aligned via faster-whisper
3. Edge-TTS (en-IN-PrabhatNeural / en-IN-NeerjaNeural) with native boundary timestamps
"""
import os
import re
import sys
import json
import base64
import asyncio
import subprocess
import requests
import imageio_ffmpeg
import config

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

# Load editable lexicon
LEXICON = {}
if os.path.exists(config.LEXICON_FILE):
    try:
        with open(config.LEXICON_FILE, "r", encoding="utf-8") as f:
            lex_data = json.load(f)
            LEXICON = lex_data.get("terms", {})
    except Exception as e:
        print(f"[LEXICON NOTICE] Failed loading lexicon: {e}")


def normalize_for_tts(text: str) -> str:
    """Apply pronunciation adjustments from config/lexicon.json for TTS audio only."""
    out = text
    for term, phon in LEXICON.items():
        pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
        out = pattern.sub(phon, out)
    return out


def get_audio_duration(path: str) -> float:
    """Extract audio duration via ffmpeg."""
    try:
        cmd = [FFMPEG_BIN, "-i", path]
        res = subprocess.run(cmd, capture_output=True, text=True)
        m = re.search(r"Duration:\s+(\d+):(\d+):([\d.]+)", res.stderr)
        if m:
            h, mi, s = m.groups()
            return int(h) * 3600 + int(mi) * 60 + float(s)
    except Exception:
        pass
    return 5.0


def _align(words, bounds, total_dur):
    """Align display words with word boundaries, linearly interpolating if needed."""
    n = len(words)
    if n == 0:
        return []
    if bounds and len(bounds) >= 2:
        nb = len(bounds)
        out = []
        for i, w in enumerate(words):
            b = bounds[min(nb - 1, int(i * nb / n))] if nb != n else bounds[i]
            out.append([w, float(b[1]), float(b[2])])
    else:
        total_len = sum(len(w) + 1 for w in words) or 1
        t = 0.0
        out = []
        for w in words:
            d = total_dur * (len(w) + 1) / total_len
            out.append([w, round(t, 3), round(t + d, 3)])
            t += d

    for i in range(n - 1):
        out[i][2] = max(out[i][2], out[i][1] + 0.05)
    return out


# --- ENGINE 1: ELEVENLABS ---

def synthesize_elevenlabs(spoken_text: str, path: str, display_words: list):
    """ElevenLabs voice synthesis with custom settings."""
    cfg = config.VOICE_CONFIG["elevenlabs"]
    api_key = os.getenv("ELEVEN_API_KEY", "").strip()
    voice_id = cfg["voice_id"]

    print(f"[ELEVENLABS] Attempting synthesis with voice {voice_id}...")
    headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
    payload = {
        "text": spoken_text,
        "model_id": cfg["model_id"],
        "voice_settings": {
            "stability": cfg["stability"],
            "similarity_boost": cfg["similarity_boost"],
            "speed": cfg.get("speed", 0.95)
        }
    }
    
    # Try with-timestamps first
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
    r = requests.post(url, headers=headers, json=payload, timeout=20)
    if r.status_code == 200:
        data = r.json()
        with open(path, "wb") as f:
            f.write(base64.b64decode(data["audio_base64"]))
        dur = get_audio_duration(path)
        # Parse alignment
        alignment = data.get("alignment", {})
        chars = alignment.get("characters", [])
        starts = alignment.get("character_start_times_seconds", [])
        ends = alignment.get("character_end_times_seconds", [])
        bounds = []
        cur_w, st, et = "", None, 0.0
        for c, s, e in zip(chars, starts, ends):
            if c.isspace():
                if cur_w:
                    bounds.append((cur_w, st, et))
                    cur_w = ""
            else:
                if not cur_w:
                    st = s
                cur_w += c
                et = e
        if cur_w:
            bounds.append((cur_w, st, et))
        print(f"[ELEVENLABS SUCCESS] {dur:.2f}s audio generated.")
        return _align(display_words, bounds, dur)
    else:
        raise RuntimeError(f"ElevenLabs HTTP {r.status_code}: {r.text[:200]}")


# --- ENGINE 2: GEMINI TTS + FASTER-WHISPER ALIGNMENT ---

def synthesize_gemini_tts(spoken_text: str, path: str, display_words: list):
    """Gemini TTS synthesis with faster-whisper word-level timestamp alignment."""
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not gemini_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    print("[GEMINI-TTS] Synthesizing speech via gemini-2.5-flash-preview-tts...")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{config.VOICE_CONFIG['gemini']['model']}:generateContent?key={gemini_key}"
    payload = {
        "contents": [{
            "parts": [{
                "text": f"{config.VOICE_CONFIG['gemini']['prompt']} Script: {spoken_text}"
            }]
        }],
        "generationConfig": {
            "responseModalities": ["AUDIO"]
        }
    }
    r = requests.post(url, json=payload, timeout=30)
    if r.status_code != 200:
        raise RuntimeError(f"Gemini TTS HTTP {r.status_code}: {r.text[:200]}")

    res_data = r.json()
    raw_pcm_path = path.replace(".mp3", "_raw.pcm")
    audio_found = False
    for cand in res_data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline_data = part.get("inlineData", {})
            if "audio" in inline_data.get("mimeType", ""):
                pcm_bytes = base64.b64decode(inline_data["data"])
                with open(raw_pcm_path, "wb") as f:
                    f.write(pcm_bytes)
                audio_found = True
                break
    if not audio_found:
        raise RuntimeError("No audio data returned by Gemini TTS.")

    # Convert PCM to MP3
    cmd = [
        FFMPEG_BIN, "-y", "-f", "s16le", "-ar", "24000", "-ac", "1",
        "-i", raw_pcm_path, "-b:a", "192k", path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    if os.path.exists(raw_pcm_path):
        os.remove(raw_pcm_path)

    dur = get_audio_duration(path)
    print(f"[GEMINI-TTS] Audio generated ({dur:.2f}s). Aligning words with faster-whisper...")

    bounds = []
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("tiny", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(path, word_timestamps=True)
        for s in segments:
            for w in s.words:
                bounds.append((w.word.strip(), round(w.start, 2), round(w.end, 2)))
    except Exception as e:
        print(f"[WHISPER ALIGN NOTICE] {e}")

    print(f"[GEMINI-TTS SUCCESS] {dur:.2f}s audio aligned with {len(bounds)} word markers.")
    return _align(display_words, bounds, dur)


# --- ENGINE 3: EDGE-TTS ---

async def _edge_async(spoken_text: str, voice: str, path: str):
    import edge_tts
    try:
        communicate = edge_tts.Communicate(spoken_text, voice=voice, rate=config.VOICE_CONFIG["edge_tts"]["rate"], boundary="WordBoundary")
    except TypeError:
        communicate = edge_tts.Communicate(spoken_text, voice=voice, rate=config.VOICE_CONFIG["edge_tts"]["rate"])

    bounds = []
    with open(path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                st = chunk["offset"] / 1e7
                d = chunk["duration"] / 1e7
                bounds.append((chunk["text"], round(st, 2), round(st + d, 2)))
    return bounds


def synthesize_edge_tts(spoken_text: str, path: str, display_words: list):
    """Edge-TTS fallback."""
    voice = config.VOICE_CONFIG["edge_tts"]["voice"]
    print(f"[EDGE-TTS] Synthesizing speech with {voice}...")
    bounds = asyncio.run(_edge_async(spoken_text, voice, path))
    dur = get_audio_duration(path)
    print(f"[EDGE-TTS SUCCESS] {dur:.2f}s audio generated with {len(bounds)} boundary markers.")
    return _align(display_words, bounds, dur)


# --- UNIFIED VOICE PIPELINE ---

def make_voice(display_text: str, path: str, phonetic_text: str = None, hero: bool = True) -> list:
    """Generate voice audio following the strict priority order:
    1. ElevenLabs -> 2. Gemini TTS -> 3. Edge-TTS
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    spoken = phonetic_text if phonetic_text else normalize_for_tts(display_text)
    display_words = display_text.split()

    # 1. ElevenLabs
    if os.getenv("ELEVEN_API_KEY") and os.getenv("ELEVEN_VOICE_ID"):
        try:
            return synthesize_elevenlabs(spoken, path, display_words)
        except Exception as e:
            print(f"[VOICE NOTICE] ElevenLabs unavailable: {e}. Auto-advancing to Gemini TTS.")

    # 2. Gemini TTS
    if os.getenv("GEMINI_API_KEY"):
        try:
            return synthesize_gemini_tts(spoken, path, display_words)
        except Exception as e:
            print(f"[VOICE NOTICE] Gemini TTS unavailable: {e}. Auto-advancing to Edge-TTS.")

    # 3. Edge-TTS Fallback
    return synthesize_edge_tts(spoken, path, display_words)
