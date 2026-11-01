"""Voice Shootout Runner: Natural Tenglish TTS Comparison.

Synthesizes the EXACT same 3 lines across all engines and voices:
- Gemini 3.8 Flash TTS (Achird, Zubenelgenubi, Puck, Sadachbia, Sulafat, Aoede)
  in both mixed-script and romanized inputs, with conversational Indian customer-support style prompt.
- Edge-TTS te-IN (Mohan, Shruti) with mixed-script input.
- Edge-TTS en-IN (Prabhat, Neerja) with romanized input (fallback).

All files exported at 48kHz, AAC/MP3 192k, mastered to -14.0 LUFS (TP <= -1.5 dBTP).
Transmits all audio files directly to user's Telegram chat, numbered for selection.
"""
import os
import sys
import time
import json
import base64
import asyncio
import requests
import subprocess
import imageio_ffmpeg
from dotenv import load_dotenv

HERE = r"C:\Users\navee\OneDrive\Desktop\studio"
sys.path.insert(0, HERE)
load_dotenv(os.path.join(HERE, ".env"))

OUT_DIR = os.path.join(HERE, "out", "voice_tests")
os.makedirs(OUT_DIR, exist_ok=True)

FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

ROMANIZED_TEXT = (
    "Mama, ee roju Claude Code nunchi crazy update vachindi! "
    "Slash command /compact context ni summarize chesthundi, memory clear cheyadu. "
    "Daily fresh AI and tech updates kosam FLASH channel ni follow avvandi!"
)

# Load verified mixed-script
MIXED_SCRIPT_FILE = os.path.join(HERE, "out", "mixed_script_sample.txt")
if os.path.exists(MIXED_SCRIPT_FILE):
    with open(MIXED_SCRIPT_FILE, "r", encoding="utf-8") as f:
        MIXED_SCRIPT_TEXT = f.read().strip()
else:
    MIXED_SCRIPT_TEXT = ROMANIZED_TEXT

STYLE_PROMPT = (
    "friendly, smiling Indian customer-support person talking to a friend, "
    "natural Telugu-English mix, conversational, not robotic, small natural pauses"
)


def master_audio(input_path: str, output_path: str, is_pcm: bool = False):
    """Normalize and resample audio to 48kHz 192kbps -14 LUFS."""
    if is_pcm:
        cmd = [
            FFMPEG_BIN, "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", input_path,
            "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7",
            "-ar", "48000", "-b:a", "192k", output_path
        ]
    else:
        cmd = [
            FFMPEG_BIN, "-y", "-i", input_path,
            "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7",
            "-ar", "48000", "-b:a", "192k", output_path
        ]
    subprocess.run(cmd, check=True, capture_output=True)


def send_telegram_audio(audio_path: str, caption: str, title: str):
    """Send generated audio file to Telegram chat."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"Telegram credentials missing, skipping delivery of {title}")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendAudio"
    try:
        with open(audio_path, "rb") as f:
            r = requests.post(
                url,
                data={
                    "chat_id": TELEGRAM_CHAT_ID,
                    "caption": caption,
                    "title": title,
                    "performer": "FLASH Voice Shootout"
                },
                files={"audio": f},
                timeout=30
            )
        if r.status_code == 200 and r.json().get("ok"):
            print(f"  [TELEGRAM OK] Delivered: {caption}")
            return True
        else:
            print(f"  [TELEGRAM FAIL] {r.status_code}: {r.text[:120]}")
            return False
    except Exception as e:
        print(f"  [TELEGRAM EXCEPTION] {e}")
        return False


def synthesize_gemini(voice_name: str, text: str, out_path: str):
    """Synthesize speech using Gemini TTS (gemini-3.8-flash-tts with fallback to gemini-3.8-flash-lite-tts)."""
    models = ["gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts"]
    last_err = None
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{STYLE_PROMPT}\nScript: {text}"
                }]
            }],
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {
                        "prebuiltVoiceConfig": {
                            "voiceName": voice_name
                        }
                    }
                }
            }
        }
        r = requests.post(url, json=payload, timeout=35)
        if r.status_code == 200:
            res_data = r.json()
            b64 = res_data["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
            raw_pcm = out_path.replace(".mp3", "_pcm.raw")
            with open(raw_pcm, "wb") as f:
                f.write(base64.b64decode(b64))

            master_audio(raw_pcm, out_path, is_pcm=True)
            if os.path.exists(raw_pcm):
                os.remove(raw_pcm)
            print(f"  [GEMINI OK] Synthesized with {model} (voice: {voice_name})")
            return
        else:
            last_err = f"{model} HTTP {r.status_code}: {r.text[:120]}"

    raise RuntimeError(f"All Gemini TTS models exhausted. Last error: {last_err}")


async def synthesize_edge(voice: str, text: str, out_path: str):
    """Synthesize speech using Edge-TTS."""
    import edge_tts
    temp_mp3 = out_path.replace(".mp3", "_edge_tmp.mp3")
    comm = edge_tts.Communicate(text, voice=voice)
    await comm.save(temp_mp3)
    master_audio(temp_mp3, out_path, is_pcm=False)
    if os.path.exists(temp_mp3):
        os.remove(temp_mp3)


# --- COMPLETE CONTESTANT ROSTER ---
CONTESTANTS = [
    # Gemini TTS: 6 voices x 2 inputs = 12 contestants
    {"num": 1, "engine": "Gemini TTS", "voice": "Achird", "input": "Mixed-Script", "filename": "gemini_achird_mixed.mp3", "type": "gemini"},
    {"num": 2, "engine": "Gemini TTS", "voice": "Achird", "input": "Romanized", "filename": "gemini_achird_romanized.mp3", "type": "gemini"},
    {"num": 3, "engine": "Gemini TTS", "voice": "Zubenelgenubi", "input": "Mixed-Script", "filename": "gemini_zubenelgenubi_mixed.mp3", "type": "gemini"},
    {"num": 4, "engine": "Gemini TTS", "voice": "Zubenelgenubi", "input": "Romanized", "filename": "gemini_zubenelgenubi_romanized.mp3", "type": "gemini"},
    {"num": 5, "engine": "Gemini TTS", "voice": "Puck", "input": "Mixed-Script", "filename": "gemini_puck_mixed.mp3", "type": "gemini"},
    {"num": 6, "engine": "Gemini TTS", "voice": "Puck", "input": "Romanized", "filename": "gemini_puck_romanized.mp3", "type": "gemini"},
    {"num": 7, "engine": "Gemini TTS", "voice": "Sadachbia", "input": "Mixed-Script", "filename": "gemini_sadachbia_mixed.mp3", "type": "gemini"},
    {"num": 8, "engine": "Gemini TTS", "voice": "Sadachbia", "input": "Romanized", "filename": "gemini_sadachbia_romanized.mp3", "type": "gemini"},
    {"num": 9, "engine": "Gemini TTS", "voice": "Sulafat", "input": "Mixed-Script", "filename": "gemini_sulafat_mixed.mp3", "type": "gemini"},
    {"num": 10, "engine": "Gemini TTS", "voice": "Sulafat", "input": "Romanized", "filename": "gemini_sulafat_romanized.mp3", "type": "gemini"},
    {"num": 11, "engine": "Gemini TTS", "voice": "Aoede", "input": "Mixed-Script", "filename": "gemini_aoede_mixed.mp3", "type": "gemini"},
    {"num": 12, "engine": "Gemini TTS", "voice": "Aoede", "input": "Romanized", "filename": "gemini_aoede_romanized.mp3", "type": "gemini"},

    # Edge-TTS: 4 contestants
    {"num": 13, "engine": "Edge-TTS", "voice": "te-IN-MohanNeural", "input": "Mixed-Script", "filename": "edge_te_mohan_mixed.mp3", "type": "edge"},
    {"num": 14, "engine": "Edge-TTS", "voice": "te-IN-ShrutiNeural", "input": "Mixed-Script", "filename": "edge_te_shruti_mixed.mp3", "type": "edge"},
    {"num": 15, "engine": "Edge-TTS", "voice": "en-IN-PrabhatNeural", "input": "Romanized (Fallback)", "filename": "edge_en_prabhat_romanized.mp3", "type": "edge"},
    {"num": 16, "engine": "Edge-TTS", "voice": "en-IN-NeerjaNeural", "input": "Romanized (Fallback)", "filename": "edge_en_neerja_romanized.mp3", "type": "edge"}
]


def run_shootout():
    print("=" * 60)
    print("STARTING NATURAL TENGLISH VOICE SHOOTOUT (16 CONTESTANTS)")
    print("Zero Budget | 48kHz | -14.0 LUFS | Telegram Delivery")
    print("=" * 60)

    # Initial announcement to Telegram
    init_msg = (
        "🎙 *FLASH VOICE SHOOTOUT*\n"
        "Sending 16 audio samples comparing natural Tenglish across:\n"
        "• Gemini 3.8 Flash TTS (Achird, Zubenelgenubi, Puck, Sadachbia, Sulafat, Aoede)\n"
        "• Edge-TTS Telugu (Mohan, Shruti) & Indian English (Prabhat, Neerja)\n"
        "All samples use the identical 3 lines. Please reply with your chosen voice number!"
    )
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data={"chat_id": TELEGRAM_CHAT_ID, "text": init_msg, "parse_mode": "Markdown"}
    )

    manifest = []

    for c in CONTESTANTS:
        num = c["num"]
        eng = c["engine"]
        vname = c["voice"]
        itype = c["input"]
        fname = c["filename"]
        out_file = os.path.join(OUT_DIR, fname)
        text_to_speak = MIXED_SCRIPT_TEXT if "Mixed" in itype else ROMANIZED_TEXT

        if os.path.exists(out_file) and os.path.getsize(out_file) > 10000:
            print(f"[{num}/16] Already generated & delivered: {fname}")
            manifest.append({
                "number": num,
                "engine": eng,
                "voice": vname,
                "input_type": itype,
                "filename": fname,
                "path": out_file,
                "size_bytes": os.path.getsize(out_file),
                "status": "DELIVERED"
            })
            continue

        print(f"\n[{num}/16] Generating: {eng} - {vname} ({itype})...")

        # Retry logic for Gemini 3 RPM limit
        for attempt in range(3):
            try:
                if c["type"] == "gemini":
                    synthesize_gemini(vname, text_to_speak, out_file)
                    # Respect 3 RPM limit (22s sleep)
                    time.sleep(21)
                else:
                    asyncio.run(synthesize_edge(vname, text_to_speak, out_file))
                break
            except Exception as e:
                err_str = str(e)
                if "429" in err_str:
                    print(f"  Rate limited on attempt {attempt+1}. Backing off 30s...")
                    time.sleep(30)
                else:
                    print(f"  Error on attempt {attempt+1}: {e}")
                    time.sleep(5)

        if os.path.exists(out_file):
            size = os.path.getsize(out_file)
            caption = f"#{num}: {eng} - {vname} ({itype})"
            title = f"#{num} {vname} ({itype})"
            send_telegram_audio(out_file, caption, title)
            manifest.append({
                "number": num,
                "engine": eng,
                "voice": vname,
                "input_type": itype,
                "filename": fname,
                "path": out_file,
                "size_bytes": size,
                "status": "DELIVERED"
            })
        else:
            print(f"  [FAIL] Failed to generate {fname}")
            manifest.append({
                "number": num,
                "engine": eng,
                "voice": vname,
                "input_type": itype,
                "status": "FAILED"
            })

    manifest_path = os.path.join(OUT_DIR, "shootout_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("\n" + "=" * 60)
    print(f"SHOOTOUT COMPLETE: All samples delivered to Telegram chat {TELEGRAM_CHAT_ID}!")
    print("=" * 60)


if __name__ == "__main__":
    run_shootout()
