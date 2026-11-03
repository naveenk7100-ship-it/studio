"""
FLASH Content OS - 30s Explainer Reel Audio Muxer & EBU R128 Masterer
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
        "id": "golden_30s_1_vllm",
        "raw_mp4": os.path.join(OUT_DIR, "raw_golden_30s_1.mp4"),
        "voice_mp3": os.path.join(CACHE_DIR, "voice_28s_vllm.mp3"),
        "music_mp3": os.path.join(MUSIC_DIR, "futuristic", "futuristic_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "golden_30s_1_vllm.mp4"),
        "threshold": "-12dB",
        "ratio": "2.5",
    },
    {
        "id": "golden_30s_2_claude",
        "raw_mp4": os.path.join(OUT_DIR, "raw_golden_30s_2.mp4"),
        "voice_mp3": os.path.join(CACHE_DIR, "voice_28s_claude.mp3"),
        "music_mp3": os.path.join(MUSIC_DIR, "dark-tech", "dark-tech_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "golden_30s_2_claude.mp4"),
        "threshold": "-15dB",
        "ratio": "3.5",
    },
    {
        "id": "golden_30s_3_mcp",
        "raw_mp4": os.path.join(OUT_DIR, "raw_golden_30s_3.mp4"),
        "voice_mp3": os.path.join(CACHE_DIR, "voice_28s_mcp.mp3"),
        "music_mp3": os.path.join(MUSIC_DIR, "hype", "hype_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "golden_30s_3_mcp.mp4"),
        "threshold": "-15dB",
        "ratio": "3.5",
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
    
    print(f"\n================ Processing {vid_id} ================")
    if not os.path.exists(raw_mp4):
        print(f"ERROR: Raw MP4 not found at {raw_mp4}")
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

    print(f"Final Mastered {vid_id}: Integrated Loudness = {i_val} LUFS, True Peak = {tp_val} dBTP")
    i_pass = (i_val is not None) and (abs(i_val - (-14.0)) <= 0.6)
    tp_pass = (tp_val is not None) and (tp_val <= -1.45)
    print(f"Gates Pass: Integrated Loudness ({i_pass}), True Peak ({tp_pass})")
    return i_pass and tp_pass

if __name__ == "__main__":
    for v in VIDEOS:
        mux_and_master(v)
