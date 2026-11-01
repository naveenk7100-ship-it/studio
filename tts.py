"""Voice synthesis and word-timestamp alignment.

Features:
- ElevenLabs (multilingual v2) with word-level timestamps as primary hero voice.
- ElevenLabs Character Guard: queries subscription quota and auto-fails over to edge-tts if low.
- edge-tts (free, en-IN voice) as zero-cost fallback with simulated / boundary timings.
- Tenglish pronunciation normalizer: phonetically spells romanized Telugu and tech acronyms
  for speech synthesis while preserving clean text for subtitles and on-screen cards.
- Self-contained audio duration measurement via imageio-ffmpeg.
"""
import os
import re
import sys
import json
import base64
import asyncio
import subprocess
import requests

try:
    import imageio_ffmpeg
    FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_BIN = "ffmpeg"


# --- TENGLISH & TECH PRONUNCIATION NORMALIZER ---
# Only applied to the text fed into TTS engines; subtitles retain clean orthography.
PHONETIC_REPLACEMENTS = [
    # Common Tenglish conversational markers
    (r"\bMama\b", "Maama"),
    (r"\bmama\b", "maama"),
    (r"\bBhayya\b", "Bhayyaa"),
    (r"\bbhayya\b", "bhayyaa"),
    (r"\bchusava\b", "choosaavaa"),
    (r"\bchusthe\b", "choosthey"),
    (r"\bavthav\b", "av-thaavu"),
    (r"\bavthundi\b", "av-thundhi"),
    (r"\bcheyandi\b", "cheyandee"),
    (r"\bcheyocchu\b", "cheyochhu"),
    (r"\bchudandi\b", "choodandee"),
    (r"\bikkada\b", "ik-kada"),
    (r"\bchaala\b", "chaalaa"),
    (r"\bpedda\b", "ped-dha"),
    (r"\bkada\b", "kadhaa"),
    (r"\bkadu\b", "kaadhu"),
    (r"\banthe\b", "anthey"),
    (r"\bmariyu\b", "mariyoo"),
    (r"\bandariki\b", "andharikee"),
    (r"\bkani\b", "kaanee"),
    (r"\blopala\b", "lopalaa"),
    (r"\bkothaga\b", "koth-thagaa"),
    (r"\bchesuko\b", "chesukoo"),

    # Tech terms & acronyms phonetic tuning
    (r"\brepo\b", "ray-poh"),
    (r"\bRepo\b", "Ray-poh"),
    (r"\brepos\b", "ray-pohs"),
    (r"\bRepos\b", "Ray-pohs"),
    (r"\bgithub\b", "git hub"),
    (r"\bGitHub\b", "Git Hub"),
    (r"\bREADME\b", "read me"),
    (r"\bLLM\b", "L L M"),
    (r"\bLLMs\b", "L L Ms"),
    (r"\bAPI\b", "A P I"),
    (r"\bAPIs\b", "A P Is"),
    (r"\bMCP\b", "M C P"),
    (r"\bCLI\b", "C L I"),
    (r"\bUI\b", "U I"),
    (r"\bPR\b", "P R"),
    (r"\bSDK\b", "S D K"),
    (r"\bClaude\b", "Clawd"),
    (r"\bclaude\b", "clawd"),
    (r"\bpip install\b", "pip in-stall"),
    (r"\bnpx\b", "N P X"),
]

def normalize_for_tts(text: str) -> str:
    """Transform text for optimal phonetics in TTS models."""
    normalized = text
    for pattern, replacement in PHONETIC_REPLACEMENTS:
        normalized = re.sub(pattern, replacement, normalized)
    return normalized


def get_audio_duration(path: str) -> float:
    """Measure duration of audio file using ffmpeg without ffprobe dependency."""
    try:
        proc = subprocess.run([FFMPEG_BIN, "-i", path], stderr=subprocess.PIPE, stdout=subprocess.DEVNULL, text=True, errors="replace")
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", proc.stderr)
        if m:
            hours, mins, secs = m.groups()
            return int(hours) * 3600 + int(mins) * 60 + float(secs)
    except Exception as e:
        print(f"[AUDIO] Duration detection fallback error: {e}")
    # Rough estimate fallback: 16KB/sec for 128kbps mp3
    try:
        size = os.path.getsize(path)
        return max(1.0, size / 16000.0)
    except Exception:
        return 5.0


def _align(words, bounds, total_dur):
    """Align word list with timestamp boundaries, linearly interpolating if needed."""
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
        # Linear distribution based on word lengths
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


# --- ELEVENLABS CHARACTER GUARD & SYNTHESIS ---

def check_elevenlabs_quota(text_len: int) -> bool:
    """Check if ElevenLabs has sufficient quota for text_len characters."""
    api_key = os.getenv("ELEVEN_API_KEY", "").strip()
    if not api_key:
        return False
    try:
        r = requests.get("https://api.elevenlabs.io/v1/user/subscription", headers={"xi-api-key": api_key}, timeout=10)
        if r.status_code != 200:
            print(f"[ELEVENLABS] Quota check HTTP {r.status_code}")
            return False
        sub = r.json()
        count = sub.get("character_count", 0)
        limit = sub.get("character_limit", 0)
        remaining = max(0, limit - count)
        tier = sub.get("tier", "free")
        print(f"[ELEVENLABS QUOTA] Tier: {tier} | Used: {count}/{limit} | Remaining: {remaining} chars")

        if remaining < text_len + 10:
            print(f"[ELEVENLABS GUARD TRIGGERED] Need {text_len} chars but only {remaining} left. Falling back to edge-tts!")
            return False
        return True
    except Exception as e:
        print(f"[ELEVENLABS] Quota check failed: {e}")
        return False


def eleven(text, path):
    """Generate audio via ElevenLabs with exact character timestamps."""
    voice_id = os.environ["ELEVEN_VOICE_ID"].strip()
    api_key = os.environ["ELEVEN_API_KEY"].strip()
    spoken_text = normalize_for_tts(text)

    print(f"[ELEVENLABS] Synthesizing {len(spoken_text)} characters using voice {voice_id}...")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
    payload = {
        "text": spoken_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.85,
            "style": 0.35,
            "use_speaker_boost": True
        }
    }
    r = requests.post(url, params={"output_format": "mp3_44100_128"}, headers={"xi-api-key": api_key}, json=payload, timeout=180)
    r.raise_for_status()
    data = r.json()

    with open(path, "wb") as f:
        f.write(base64.b64decode(data["audio_base64"]))

    alignment = data.get("alignment", {})
    chars = alignment.get("characters", [])
    starts = alignment.get("character_start_times_seconds", [])
    ends = alignment.get("character_end_times_seconds", [])

    bounds = []
    curr_word = ""
    start_time = None
    end_time = 0.0

    for c, s, e in zip(chars, starts, ends):
        if c.isspace():
            if curr_word:
                bounds.append((curr_word, start_time, end_time))
                curr_word = ""
        else:
            if not curr_word:
                start_time = s
            curr_word += c
            end_time = e
    if curr_word:
        bounds.append((curr_word, start_time, end_time))

    duration = get_audio_duration(path)
    print(f"[ELEVENLABS SUCCESS] Audio generated: {duration:.2f}s, {len(bounds)} timed words.")
    return _align(text.split(), bounds, duration)


# --- EDGE-TTS (FREE FALLBACK) ---

async def _edge_async(text, voice, path):
    import edge_tts
    spoken_text = normalize_for_tts(text)
    try:
        communicate = edge_tts.Communicate(spoken_text, voice, rate="+6%", boundary="WordBoundary")
    except TypeError:
        communicate = edge_tts.Communicate(spoken_text, voice, rate="+6%")

    bounds = []
    with open(path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                # offset is in 100ns units -> convert to seconds
                st = chunk["offset"] / 1e7
                dur = chunk["duration"] / 1e7
                bounds.append((chunk["text"], st, st + dur))
    return bounds


def edge(text, path):
    """Generate audio using Microsoft Edge TTS (100% free, Indian English accent)."""
    voice = os.getenv("EDGE_VOICE", "en-IN-PrabhatNeural")
    print(f"[EDGE-TTS] Generating voice with {voice}...")
    bounds = asyncio.run(_edge_async(text, voice, path))
    duration = get_audio_duration(path)
    print(f"[EDGE-TTS SUCCESS] Audio generated: {duration:.2f}s, {len(bounds)} boundary markers.")
    return _align(text.split(), bounds, duration)


def make_voice(text, path, hero=True):
    """Voice generator with automatic Character Guard and fallback."""
    if hero and os.getenv("ELEVEN_API_KEY") and os.getenv("ELEVEN_VOICE_ID"):
        if check_elevenlabs_quota(len(text)):
            try:
                return eleven(text, path)
            except Exception as e:
                print(f"[WARNING] ElevenLabs synthesis failed ({e}). Auto-falling back to edge-tts.")
    return edge(text, path)
