"""
FLASH Content OS - New Editorial 30s Explainer Reel Audio Muxer & EBU R128 Masterer
Muxes raw 28.00s MP4 renders with calibrated voiceover and ducked background music.
Performs broadcast-grade mastering:
- Gentle dynamic compressor (threshold -15dB, ratio 3.5:1, attack 5ms, release 50ms)
- Loudnorm targeting: Integrated Loudness = -14.0 LUFS, True Peak = -1.6 dBTP, LRA = 7.0
- Audio Sample Rate: 48,000 Hz
"""

import os
import sys
import json
import subprocess
import re
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
OUT_DIR = os.path.join(ROOT, "out")
CACHE_DIR = os.path.join(ROOT, "cache")
MUSIC_DIR = os.path.join(ROOT, "assets", "music")

VIDEOS = [
    {
        "id": "reel_new_1_superagent",
        "raw_mp4": os.path.join(OUT_DIR, "raw_new_1_superagent.mp4"),
        "voice_mp3": os.path.join(CACHE_DIR, "voice_28s_superagent.mp3"),
        "music_mp3": os.path.join(MUSIC_DIR, "futuristic", "futuristic_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "reel_new_1_superagent.mp4"),
        "threshold": "-14dB",
        "ratio": "3.0",
    },
    {
        "id": "reel_new_2_ollama",
        "raw_mp4": os.path.join(OUT_DIR, "raw_new_2_ollama.mp4"),
        "voice_mp3": os.path.join(CACHE_DIR, "voice_28s_ollama.mp3"),
        "music_mp3": os.path.join(MUSIC_DIR, "dark-tech", "dark-tech_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "reel_new_2_ollama.mp4"),
        "threshold": "-15dB",
        "ratio": "3.5",
    },
    {
        "id": "reel_new_3_qwen_news",
        "raw_mp4": os.path.join(OUT_DIR, "raw_new_3_qwen_news.mp4"),
        "voice_mp3": os.path.join(CACHE_DIR, "voice_28s_qwen_news.mp3"),
        "music_mp3": os.path.join(MUSIC_DIR, "news-urgent", "news-urgent_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "reel_new_3_qwen_news.mp4"),
        "threshold": "-14dB",
        "ratio": "3.0",
    },
]

def mux_and_master(video_conf):
    vid_id = video_conf["id"]
    raw_mp4 = video_conf["raw_mp4"]
    voice_mp3 = video_conf["voice_mp3"]
    music_mp3 = video_conf["music_mp3"]
    final_mp4 = video_conf["final_mp4"]
    thresh = video_conf.get("threshold", "-14dB")
    ratio = video_conf.get("ratio", "3.0")
    
    print(f"\n================ Processing {vid_id} ================", flush=True)
    if not os.path.exists(raw_mp4):
        print(f"ERROR: Raw MP4 not found at {raw_mp4}", flush=True)
        return False

    filter_complex = (
        f"[1:a]volume=1.0,acompressor=threshold={thresh}:ratio={ratio}:attack=5:release=50[v];"
        f"[2:a]volume=0.045[m];"
        f"[v][m]amix=inputs=2:duration=first:dropout_transition=2,"
        f"loudnorm=I=-14.0:TP=-1.6:LRA=7.0:dual_mono=false[aout]"
    )
    
    cmd = [
        FFMPEG, "-y",
        "-i", raw_mp4,
        "-i", voice_mp3,
        "-stream_loop", "-1", "-i", music_mp3,
        "-filter_complex", filter_complex,
        "-map", "0:v:0",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-shortest",
        final_mp4
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Measure with ebur128
    meas_cmd = [FFMPEG, "-i", final_mp4, "-af", "ebur128=peak=true", "-f", "null", "-"]
    res = subprocess.run(meas_cmd, capture_output=True, text=True)
    
    i_val, tp_val = None, None
    for line in res.stderr.splitlines()[-25:]:
        if "I:" in line and "LUFS" in line and i_val is None:
            m = re.search(r"I:\s+([-\d.]+)\s+LUFS", line)
            if m: i_val = float(m.group(1))
        if "Peak:" in line and "dBFS" in line and tp_val is None:
            m = re.search(r"Peak:\s+([-\d.]+)\s+dBFS", line)
            if m: tp_val = float(m.group(1))
            
    print(f"[{vid_id}] Final Broadcast Audio Mastered: Integrated Loudness = {i_val} LUFS, True Peak = {tp_val} dBTP", flush=True)
    return {
        "id": vid_id,
        "final_mp4": final_mp4,
        "lufs": i_val,
        "true_peak": tp_val,
        "passed": (i_val is not None and -15.0 <= i_val <= -13.0 and tp_val is not None and tp_val <= -1.5)
    }

if __name__ == "__main__":
    results = []
    for conf in VIDEOS:
        res = mux_and_master(conf)
        if res:
            results.append(res)
    
    summary_path = os.path.join(OUT_DIR, "mastering_new_summary.json")
    with open(summary_path, "w") as f:
        json.dump(results, f, indent=2)
    print("\nMastering complete! Summary saved to:", summary_path, flush=True)
