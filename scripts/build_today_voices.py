"""
FLASH Content OS - Today's 2 Fresh Daily Videos Voice Synthesizer & Word Aligner
Uses edge-tts with precise word boundaries.
"""

import os
import sys
import json
import re
import asyncio
import subprocess
import imageio_ffmpeg
import edge_tts
# from pydub import AudioSegment
from dotenv import load_dotenv

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
CACHE_DIR = os.path.join(ROOT, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

SCRIPTS = [
    {
        "id": "today_1_anatomy",
        "title": "wheresryan22 / anatomy",
        "script": "Mama, complex software architectures explain cheyadaniki kastam ga unda? Idi Anatomy, Claude Code open skill. System code ni inspect chesi, real machine parts la interactive isometric diagrams build chestundi. Slash anatomy preview run chesi SVG and 3D lo visual inspect cheyandi. GitHub lo 25395 stars reach aindi. MIT license tho open-source ga undi. Link in bio check cheyandi.",
        "target_speech_dur": 24.2,
    },
    {
        "id": "today_2_browseruse",
        "title": "browser-use / browser-use 0.13.14",
        "script": "Mama, AI agents websites browse chesi workflows automate cheyala? Idi Browser Use 0.13.14 open-source library. Playwright integration tho LLMs direct ga buttons click chesi, forms fill chesi, multi-step browser tasks execute chestundi. Pip install browser use chesi agent script run cheyandi. GitHub lo 120179 stars tho viral ga undi. MIT license tho available ga undi. Full setup guide bio link lo undi.",
        "target_speech_dur": 24.2,
    }
]

async def synthesize_voice_with_words(text, raw_mp3):
    communicate = edge_tts.Communicate(text, "te-IN-MohanNeural", rate="+6%")
    submaker = edge_tts.SubMaker()
    
    with open(raw_mp3, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])
                
    return submaker.cues

def process_item(item):
    item_id = item["id"]
    text = item["script"]
    target_dur = item["target_speech_dur"]
    
    raw_mp3 = os.path.join(CACHE_DIR, f"voice_raw_{item_id}.mp3")
    calibrated_mp3 = os.path.join(CACHE_DIR, f"voice_calibrated_{item_id}.mp3")
    final_voice_mp3 = os.path.join(CACHE_DIR, f"voice_final_{item_id}.mp3")
    words_json = os.path.join(CACHE_DIR, f"words_final_{item_id}.json")
    
    print(f"\n================ Synthesizing Voice for {item_id} ================", flush=True)
    print(f"Script ({len(text.split())} words):\n\"{text}\"", flush=True)
    
    cues = asyncio.run(synthesize_voice_with_words(text, raw_mp3))
    
    # Get duration
    probe = subprocess.run([FFMPEG, "-i", raw_mp3], capture_output=True, text=True, errors="ignore")
    dur = 24.0
    m = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", probe.stderr)
    if m:
        dur = int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))
    print(f"  Raw Speech Duration: {dur:.2f} s (Target: {target_dur:.2f} s)", flush=True)
    
    # Speed calibration factor
    speech_space = target_dur - 0.45
    speed = dur / speech_space
    speed = max(0.85, min(1.25, speed))
    tempo_str = f"atempo={speed:.4f}"
    
    # Apply tempo, 150ms head silence, and pad to 28.00s exactly
    cmd = [
        FFMPEG, "-y",
        "-i", raw_mp3,
        "-filter_complex",
        f"[0:a]{tempo_str},adelay=150|150,apad=pad_dur=4.0[a]",
        "-map", "[a]",
        "-c:a", "mp3",
        "-b:a", "192k",
        "-ar", "48000",
        "-t", "28.00",
        calibrated_mp3
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    import shutil
    shutil.copy2(calibrated_mp3, final_voice_mp3)
    
    # Calculate word timestamps scaled by speed + 150ms offset
    words = []
    text_words = [w.strip() for w in text.split()]
    
    # Extract cues to words
    for idx, cue in enumerate(cues):
        # cue.start is timedelta
        st = cue.start.total_seconds() / speed + 0.150
        et = cue.end.total_seconds() / speed + 0.150
        w_text = cue.content.strip()
        words.append({
            "word": w_text,
            "start": round(st, 3),
            "end": round(et, 3)
        })
        
    with open(words_json, "w", encoding="utf-8") as f:
        json.dump(words, f, indent=2)
        
    print(f"  Saved {len(words)} aligned words to {words_json}", flush=True)
    if words:
        print(f"  First word: '{words[0]['word']}' at {words[0]['start']}s | Last word: '{words[-1]['word']}' at {words[-1]['end']}s", flush=True)
    return True

if __name__ == "__main__":
    for s in SCRIPTS:
        process_item(s)
    print("\n[ALL TODAY VOICES READY]")
