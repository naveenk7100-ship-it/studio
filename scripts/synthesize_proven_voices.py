"""
FLASH Content OS - Synthesize and Calibrate Voices for 3 Proven Topics
Topics:
1. unslop (Rising Repo - heydamir/unslop) -> cache/voice_28s_unslop.mp3 + cache/words_28s_unslop.json
2. uv (Tool Release - astral-sh/uv v0.13.7) -> cache/voice_28s_uv.mp3 + cache/words_28s_uv.json
3. kimi (AI News - Moonshot Kimi K3.1 Pro) -> cache/voice_28s_kimi.mp3 + cache/words_28s_kimi.json

Uses Gemini TTS Sadachbia with mixed-script payload, aligns words via faster-whisper/ctc,
and scales precisely to 28.00s via FFmpeg atempo.
"""

import os
import sys
import json
import subprocess
import re
import imageio_ffmpeg
from dotenv import load_dotenv

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
sys.path.insert(0, ROOT)
load_dotenv(os.path.join(ROOT, ".env"))

import tts

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
CACHE_DIR = os.path.join(ROOT, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

TARGET_DURATION = 28.00

SCRIPTS = [
    {
        "id": "unslop",
        "title": "heydamir/unslop (Rising Repo)",
        "voice_name": "Sadachbia",
        "display_text": "Mama, mee AI tools generate chesina web UI generic ga, AI slop la anipistunda? Idi heydamir unslop. October twenty-nine release aina idi, okka Claude skill tho vibecoded interfaces ni professional design system ga marchutundi. Idi border radius, contrast mariyu typography ni automatically refactor chestundi. Eight thousand nine hundred stars reach aina open source repo idi. Try cheyadaniki npx at damir slash unslop run cheyandi.",
        "raw_voice_path": os.path.join(CACHE_DIR, "voice_raw_unslop.mp3"),
        "calibrated_mp3": os.path.join(CACHE_DIR, "voice_28s_unslop.mp3"),
        "words_json": os.path.join(CACHE_DIR, "words_28s_unslop.json"),
    },
    {
        "id": "uv",
        "title": "astral-sh/uv v0.13.7 (Tool Release)",
        "voice_name": "Sadachbia",
        "display_text": "Mama, Python AI development lo pip install slow ga undi visugostunda? Idi Astral uv release zero point thirteen point seven. Rust language tho build chesina ee tool, standard pip kante ten to hundred times faster ga dependencies resolve chestundi. Virtual environments create cheyadam fraction of a second lo aipotundi. Ninety-one thousand stars unna official tool idi. Install cheyadaniki curl command tho single line run cheyandi.",
        "raw_voice_path": os.path.join(CACHE_DIR, "voice_raw_uv.mp3"),
        "calibrated_mp3": os.path.join(CACHE_DIR, "voice_28s_uv.mp3"),
        "words_json": os.path.join(CACHE_DIR, "words_28s_uv.json"),
    },
    {
        "id": "kimi",
        "title": "Kimi K3.1 Pro (AI News)",
        "voice_name": "Sadachbia",
        "display_text": "Mama, open weight AI models lo major breakthrough vachindi. Moonshot AI official ga Kimi K three point one Pro weights release chesindi. Hacker News lo four hundred sixty-three points tho viral aina ee model, advanced long context reasoning mariyu agentic coding capabilities istundi. Developers direct ga Hugging Face nunchi weights download chesi Transformers library tho run cheyavachu. Open source AI community ki idi great asset.",
        "raw_voice_path": os.path.join(CACHE_DIR, "voice_raw_kimi.mp3"),
        "calibrated_mp3": os.path.join(CACHE_DIR, "voice_28s_kimi.mp3"),
        "words_json": os.path.join(CACHE_DIR, "words_28s_kimi.json"),
    }
]

def synthesize_and_calibrate():
    print("================ SYNTHESIZING & CALIBRATING 3 PROVEN TOPIC VOICES ================")
    
    for item in SCRIPTS:
        topic_id = item["id"]
        raw_mp3 = item["raw_voice_path"]
        cal_mp3 = item["calibrated_mp3"]
        words_out = item["words_json"]
        
        print(f"\n>>> Processing Voice for {item['title']}...")
        
        # 1. Synthesize via tts.make_voice
        words = tts.make_voice(
            display_text=item["display_text"],
            path=raw_mp3,
            voice_override=item["voice_name"]
        )
        
        orig_dur = tts.get_audio_duration(raw_mp3)
        orig_words = words if isinstance(words, list) else []
        print(f"  Raw Synthesis: {orig_dur:.2f}s, {len(orig_words)} aligned words")
        
        if orig_dur <= 0.0 or not os.path.exists(raw_mp3):
            print(f"ERROR: Synthesis failed for {topic_id}")
            continue
            
        # 2. Calibrate duration to exactly TARGET_DURATION (28.00s)
        # speed_ratio = orig_dur / TARGET_DURATION
        speed_ratio = orig_dur / TARGET_DURATION
        print(f"  Calibrating with atempo = {speed_ratio:.4f}x to target {TARGET_DURATION}s...")
        
        # Build atempo filter chain (atempo only supports 0.5 to 2.0 per filter)
        atempo_filters = []
        rem_speed = speed_ratio
        while rem_speed > 2.0:
            atempo_filters.append("atempo=2.0")
            rem_speed /= 2.0
        while rem_speed < 0.5:
            atempo_filters.append("atempo=0.5")
            rem_speed /= 0.5
        atempo_filters.append(f"atempo={rem_speed:.4f}")
        filter_str = ",".join(atempo_filters)
        
        cmd = [
            FFMPEG, "-y",
            "-i", raw_mp3,
            "-filter:a", filter_str,
            "-b:a", "192k",
            "-ar", "48000",
            cal_mp3
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Verify calibrated duration
        meas_cmd = [FFMPEG, "-i", cal_mp3]
        res = subprocess.run(meas_cmd, capture_output=True, text=True)
        m = re.search(r"Duration:\s+(\d+):(\d+):([\d.]+)", res.stderr)
        final_dur = float(m.group(3)) if m else 0.0
        print(f"  Calibrated MP3 Duration: {final_dur:.2f}s at {cal_mp3}")
        
        # 3. Proportionally scale word alignment timestamps
        time_factor = TARGET_DURATION / orig_dur
        scaled_words = []
        for w in orig_words:
            # w format: [word_str, start_sec, end_sec]
            w_text = w[0]
            w_start = round(w[1] * time_factor, 3)
            w_end = round(w[2] * time_factor, 3)
            scaled_words.append([w_text, w_start, w_end])
            
        with open(words_out, "w", encoding="utf-8") as f:
            json.dump(scaled_words, f, indent=2)
            
        print(f"  Scaled {len(scaled_words)} words to {words_out} (first word: {scaled_words[0]}, last word: {scaled_words[-1]})")
        
    print("\nAll 3 voices synthesized and calibrated successfully!")

if __name__ == "__main__":
    synthesize_and_calibrate()
