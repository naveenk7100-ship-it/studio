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


# --- TRANSLITERATION: MIXED-SCRIPT BUILDER ---

TRANSLIT_CACHE_FILE = os.path.join(os.path.dirname(__file__), "cache", "translit_cache.json")

def build_mixed_script(romanized_tenglish: str) -> str:
    """Build TTS input as mixed-script:
    Telugu words written in native Telugu script, English and tech words kept in Latin letters,
    punctuation added for natural pauses.
    Native script exists ONLY inside the TTS call and its cache, never in display captions or logs."""
    os.makedirs(os.path.dirname(TRANSLIT_CACHE_FILE), exist_ok=True)
    cache = {}
    if os.path.exists(TRANSLIT_CACHE_FILE):
        try:
            with open(TRANSLIT_CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except Exception:
            cache = {}

    norm_key = romanized_tenglish.strip()
    if norm_key in cache:
        return cache[norm_key]

    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not gemini_key:
        return romanized_tenglish

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
        prompt = (
            "You are a specialized transliterator for Tenglish (Telugu + English). "
            "Convert the following romanized Tenglish into mixed-script for high-quality TTS: "
            "1. Convert ALL Telugu words into native Telugu script (Telugu unicode characters). "
            "2. Keep ALL English and tech terms, brand names, slash commands, repo names, and numbers in clean Latin letters/digits. "
            "3. Attach Telugu case suffixes like ni, tho, lo, kosam appropriately in Telugu script. "
            "4. Add natural punctuation (commas, exclamation marks) for natural speaking rhythm and pauses. "
            "Return ONLY the converted mixed-script string without markdown, quotes, or preamble.\n\n"
            f"Input: {norm_key}"
        )
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        r = requests.post(url, json=payload, timeout=20)
        if r.status_code == 200:
            res = r.json()
            mixed = res["candidates"][0]["content"]["parts"][0]["text"].strip()
            cache[norm_key] = mixed
            with open(TRANSLIT_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
            print(f"[TRANSLITERATION] Built natural mixed-script for TTS ({len(mixed)} chars).")
            return mixed
    except Exception as e:
        print(f"[TRANSLITERATION NOTICE] LLM transliteration fallback: {e}")

    return romanized_tenglish


# --- ENGINE 1: ELEVENLABS ---

def synthesize_elevenlabs(spoken_text: str, path: str, display_words: list):
    """ElevenLabs voice synthesis (Reserved strictly for manual hero lane)."""
    cfg = config.VOICE_CONFIG["elevenlabs"]
    api_key = os.getenv("ELEVEN_API_KEY", "").strip()
    voice_id = cfg["voice_id"]

    print(f"[ELEVENLABS] Manual hero lane synthesis with voice {voice_id}...")
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
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
    r = requests.post(url, headers=headers, json=payload, timeout=20)
    if r.status_code == 200:
        data = r.json()
        with open(path, "wb") as f:
            f.write(base64.b64decode(data["audio_base64"]))
        dur = get_audio_duration(path)
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

def synthesize_gemini_tts(spoken_text: str, path: str, display_words: list, voice_name: str = None, use_mixed_script: bool = True):
    """Gemini TTS synthesis (gemini-3.8-flash-tts) with style prompt and faster-whisper word alignment."""
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not gemini_key:
        raise RuntimeError("GEMINI_API_KEY is not set.")

    chosen_voice = voice_name or config.VOICE_CONFIG.get("gemini", {}).get("voice_name", "Puck")
    tts_input = build_mixed_script(spoken_text) if use_mixed_script else spoken_text

    style_prompt = config.VOICE_CONFIG.get("gemini", {}).get(
        "style_prompt",
        "natural Telugu tech creator, warm conversational tone, slightly slower deliberate rhythm, rich intonation, brief natural pauses, engaging and confident"
    )

    # Try models: gemini-3.8-flash-lite-tts, gemini-3.8-flash-tts, gemini-2.5-flash-preview-tts
    models = ["gemini-3.8-flash-lite-tts", "gemini-3.8-flash-tts", "gemini-2.5-flash-preview-tts", "gemini-3.1-flash-tts-preview"]
    res_data = None
    for model_name in models:
        print(f"[GEMINI-TTS] Synthesizing speech via {model_name} (Voice: {chosen_voice}, Mixed: {use_mixed_script})...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={gemini_key}"
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{style_prompt}\nScript: {tts_input}"
                }]
            }],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {
                            "voiceName": chosen_voice
                        }
                    }
                }
            }
        }
        r = requests.post(url, json=payload, timeout=35)
        if r.status_code == 200:
            res_data = r.json()
            break
        elif r.status_code == 429:
            print(f"[GEMINI-TTS NOTICE] {model_name} quota 429, trying next model...")
            continue
        else:
            raise RuntimeError(f"Gemini TTS HTTP {r.status_code}: {r.text[:200]}")

    if not res_data:
        raise RuntimeError(f"All Gemini TTS models ({models}) returned 429 Quota Exceeded.")
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

    # Convert PCM to 48kHz MP3 with loudnorm
    cmd = [
        FFMPEG_BIN, "-y", "-f", "s16le", "-ar", "24000", "-ac", "1",
        "-i", raw_pcm_path,
        "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7",
        "-ar", "48000", "-b:a", "192k", path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    if os.path.exists(raw_pcm_path):
        os.remove(raw_pcm_path)

    dur = get_audio_duration(path)
    print(f"[GEMINI-TTS] Audio generated ({dur:.2f}s). Aligning romanized captions with faster-whisper...")

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
    temp_edge = path.replace(".mp3", "_edge_raw.mp3")
    with open(temp_edge, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                st = chunk["offset"] / 1e7
                d = chunk["duration"] / 1e7
                bounds.append((chunk["text"], round(st, 2), round(st + d, 2)))

    # Re-encode to 48kHz with broadcast loudnorm
    cmd = [
        FFMPEG_BIN, "-y", "-i", temp_edge,
        "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7",
        "-ar", "48000", "-b:a", "192k", path
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    if os.path.exists(temp_edge):
        os.remove(temp_edge)

    return bounds


def synthesize_edge_tts(spoken_text: str, path: str, display_words: list, voice: str = None):
    """Edge-TTS synthesis with automatic mixed-script for te-IN and romanized for en-IN."""
    target_voice = voice or config.VOICE_CONFIG["edge_tts"]["voice"]
    if target_voice.startswith("te-IN"):
        tts_input = build_mixed_script(spoken_text)
    else:
        tts_input = spoken_text

    print(f"[EDGE-TTS] Synthesizing speech with {target_voice} (48kHz, loudnorm -14 LUFS)...")
    bounds = asyncio.run(_edge_async(tts_input, target_voice, path))
    dur = get_audio_duration(path)
    print(f"[EDGE-TTS SUCCESS] {dur:.2f}s audio generated with {len(bounds)} boundary markers.")
    return _align(display_words, bounds, dur)


# --- UNIFIED VOICE PIPELINE & CACHING ---

TTS_CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache", "tts_audio")
QUOTA_TRACKER_FILE = os.path.join(os.path.dirname(__file__), "cache", "quota_tracker.json")


def notify_telegram_fallback(message: str):
    """Alert user on Telegram whenever an engine falls back."""
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if token and chat_id:
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data={"chat_id": chat_id, "text": f"⚠️ [VOICE FALLBACK ALERT]\n{message}"},
                timeout=5
            )
        except Exception:
            pass


def record_quota_attempt(model_or_engine: str):
    """Track API calls against daily free-tier cap (10 RPD observed on Gemini TTS)."""
    os.makedirs(os.path.dirname(QUOTA_TRACKER_FILE), exist_ok=True)
    today = str(config.dt.date.today()) if hasattr(config, "dt") else "today"
    data = {}
    if os.path.exists(QUOTA_TRACKER_FILE):
        try:
            with open(QUOTA_TRACKER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    day_counts = data.get(today, {})
    day_counts[model_or_engine] = day_counts.get(model_or_engine, 0) + 1
    data[today] = day_counts
    try:
        with open(QUOTA_TRACKER_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass


def make_voice(display_text: str, path: str, phonetic_text: str = None, hero: bool = False, engine_override: str = None, voice_override: str = None) -> list:
    """Generate voice audio following the user-configured natural Tenglish hierarchy:
    1. Gemini TTS (Aoede, mixed-script input)
    2. Gemini TTS (Sadachbia, mixed-script input)
    3. Edge-TTS (te-IN-ShrutiNeural, mixed-script input)
    4. Edge-TTS (en-IN-NeerjaNeural, romanized input fallback)

    - Exactly ONE TTS request per video, strictly cached by script hash.
    - Automatic fallback with immediate Telegram notification.
    - Display captions are strictly romanized with authentic word-level sync.
    """
    import hashlib
    import shutil

    os.makedirs(os.path.dirname(path), exist_ok=True)
    os.makedirs(TTS_CACHE_DIR, exist_ok=True)

    spoken = phonetic_text if phonetic_text else normalize_for_tts(display_text)
    display_words = display_text.split()

    chosen_voice = voice_override or getattr(config, "ACTIVE_VOICE", "Aoede")
    script_hash = hashlib.sha256(f"{spoken}_{chosen_voice}".encode("utf-8")).hexdigest()[:16]
    cached_audio_path = os.path.join(TTS_CACHE_DIR, f"{script_hash}_{chosen_voice}.mp3")

    # 1. Cache Check: Instant zero-cost reuse if identical script already synthesized
    if os.path.exists(cached_audio_path) and os.path.getsize(cached_audio_path) > 10000:
        print(f"[TTS CACHE HIT] Reusing cached audio ({script_hash}_{chosen_voice}.mp3). Zero API quota consumed.")
        shutil.copyfile(cached_audio_path, path)
        dur = get_audio_duration(path)
        # Fast align display words
        bounds = []
        try:
            from faster_whisper import WhisperModel
            model = WhisperModel("tiny", device="cpu", compute_type="int8")
            segments, _ = model.transcribe(path, word_timestamps=True)
            for s in segments:
                for w in s.words:
                    bounds.append((w.word.strip(), round(w.start, 2), round(w.end, 2)))
        except Exception:
            pass
        return _align(display_words, bounds, dur)

    # Manual Hero Lane (ElevenLabs)
    if hero and os.getenv("ELEVEN_API_KEY") and os.getenv("ELEVEN_VOICE_ID"):
        try:
            return synthesize_elevenlabs(spoken, path, display_words)
        except Exception as e:
            notify_telegram_fallback(f"ElevenLabs hero lane failed: {e}. Falling back to Gemini TTS.")

    # Build fallback order starting from active voice
    hierarchy = [
        {"engine": "gemini", "voice": chosen_voice, "mixed": True},
        {"engine": "gemini", "voice": "Sadachbia" if chosen_voice != "Sadachbia" else "Aoede", "mixed": True},
        {"engine": "edge_tts", "voice": "te-IN-ShrutiNeural", "mixed": True},
        {"engine": "edge_tts", "voice": "en-IN-NeerjaNeural", "mixed": False}
    ]

    last_err = None
    for step in hierarchy:
        eng = step["engine"]
        vname = step["voice"]
        use_mixed = step["mixed"]

        if eng == "gemini":
            if not os.getenv("GEMINI_API_KEY"):
                continue
            record_quota_attempt("gemini_tts")
            try:
                words = synthesize_gemini_tts(spoken, path, display_words, voice_name=vname, use_mixed_script=use_mixed)
                shutil.copyfile(path, cached_audio_path)
                return words
            except Exception as e:
                last_err = str(e)
                print(f"[VOICE NOTICE] Gemini TTS ({vname}) error: {e}")
                notify_telegram_fallback(f"Gemini TTS ({vname}) failed ({str(e)[:120]}). Auto-advancing down hierarchy.")

        elif eng == "edge_tts":
            try:
                record_quota_attempt(f"edge_{vname}")
                words = synthesize_edge_tts(spoken, path, display_words, voice=vname)
                shutil.copyfile(path, cached_audio_path)
                return words
            except Exception as e:
                last_err = str(e)
                print(f"[VOICE NOTICE] Edge-TTS ({vname}) error: {e}")

    raise RuntimeError(f"All voices in hierarchy exhausted. Last error: {last_err}")
