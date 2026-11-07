"""
FLASH Content OS - Render and Master Today's 2 Fresh Daily Reels:
1. TodayReel-Anatomy (wheresryan22/anatomy)
2. TodayReel-BrowserUse (browser-use/browser-use)
"""

import os
import sys
import json
import subprocess
import time
import re
import imageio_ffmpeg

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
ENG_DIR = os.path.join(ROOT, "engine")
OUT_DIR = os.path.join(ROOT, "out")
CACHE_DIR = os.path.join(ROOT, "cache")
MUSIC_DIR = os.path.join(ROOT, "assets", "music")
DOCS_VIDEOS_DIR = os.path.join(ROOT, "docs", "videos")
REMOTION_BIN = os.path.join(ENG_DIR, "node_modules", ".bin", "remotion.cmd")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(DOCS_VIDEOS_DIR, exist_ok=True)

REELS = [
    {
        "id": "today_1_anatomy",
        "comp_id": "TodayReel-Anatomy",
        "raw_mp4": os.path.join(OUT_DIR, "raw_today_1_anatomy.mp4"),
        "voice_mp3": os.path.join(CACHE_DIR, "voice_final_today_1_anatomy.mp3"),
        "music_mp3": os.path.join(MUSIC_DIR, "futuristic", "futuristic_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "reel_today_1_anatomy.mp4"),
        "web_mp4": os.path.join(DOCS_VIDEOS_DIR, "reel_today_1_anatomy_720p.mp4"),
        "target_lufs": -13.8,
    },
    {
        "id": "today_2_browseruse",
        "comp_id": "TodayReel-BrowserUse",
        "raw_mp4": os.path.join(OUT_DIR, "raw_today_2_browseruse.mp4"),
        "voice_mp3": os.path.join(CACHE_DIR, "voice_final_today_2_browseruse.mp3"),
        "music_mp3": os.path.join(MUSIC_DIR, "dark-tech", "dark-tech_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "reel_today_2_browseruse.mp4"),
        "web_mp4": os.path.join(DOCS_VIDEOS_DIR, "reel_today_2_browseruse_720p.mp4"),
        "target_lufs": -13.8,
    },
]

def render_comp(comp_id, out_mp4):
    if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 5 * 1024 * 1024:
        print(f">>> REUSING EXISTING RENDER: {comp_id} -> {out_mp4} ({os.path.getsize(out_mp4)/(1024*1024):.2f} MB)", flush=True)
        return True

    print(f"\n=======================================================", flush=True)
    print(f">>> STARTING REMOTION RENDER: {comp_id} -> {out_mp4}", flush=True)
    print(f"=======================================================", flush=True)
    t0 = time.time()
    cmd = [
        REMOTION_BIN, "render",
        comp_id,
        out_mp4,
        "--gl=angle",
        "--concurrency=4",
    ]
    res = subprocess.run(cmd, cwd=ENG_DIR, capture_output=True, text=True)
    dt = time.time() - t0
    if res.returncode == 0:
        size_mb = os.path.getsize(out_mp4) / (1024 * 1024) if os.path.exists(out_mp4) else 0
        print(f">>> SUCCESS: {comp_id} rendered in {dt:.1f}s ({size_mb:.2f} MB)", flush=True)
        return True
    else:
        print(f">>> FAILED: {comp_id} (code {res.returncode}):", flush=True)
        print(res.stderr or res.stdout, flush=True)
        return False

def mux_and_master(cfg):
    reel_id = cfg["id"]
    raw_mp4 = cfg["raw_mp4"]
    voice_mp3 = cfg["voice_mp3"]
    music_mp3 = cfg["music_mp3"]
    final_mp4 = cfg["final_mp4"]
    web_mp4 = cfg["web_mp4"]
    t_lufs = cfg["target_lufs"]

    print(f"\n================ Muxing & Mastering {reel_id} (Target I={t_lufs}) ================", flush=True)
    padded_voice_wav = os.path.join(CACHE_DIR, f"voice_padded_{reel_id}.wav")
    temp_mix_wav = os.path.join(CACHE_DIR, f"temp_mix_{reel_id}.wav")

    # Step A: Pad voice audio out to 27.95s so the end card has music and loudness stays calibrated
    pad_cmd = [
        FFMPEG, "-y",
        "-i", voice_mp3,
        "-af", "apad=whole_dur=27.95",
        "-ar", "48000",
        padded_voice_wav
    ]
    subprocess.run(pad_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Step B: Pre-mix compressed voice + music
    premix_filter = (
        "[0:a]volume=1.2,acompressor=threshold=-18dB:ratio=4.5:attack=5:release=50[v];"
        "[1:a]volume=0.040[m];"
        "[v][m]amix=inputs=2:duration=first:dropout_transition=2[aout]"
    )
    premix_cmd = [
        FFMPEG, "-y",
        "-i", padded_voice_wav,
        "-stream_loop", "-1", "-i", music_mp3,
        "-filter_complex", premix_filter,
        "-map", "[aout]",
        "-c:a", "pcm_s16le",
        "-ar", "48000",
        temp_mix_wav
    ]
    subprocess.run(premix_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Step C: Pass 1 - Measure loudnorm parameters
    meas_cmd = [
        FFMPEG, "-i", temp_mix_wav,
        "-af", f"loudnorm=I={t_lufs}:TP=-1.6:LRA=7.0:print_format=json",
        "-f", "null", "-"
    ]
    res1 = subprocess.run(meas_cmd, capture_output=True, text=True, errors="ignore")
    json_str = res1.stderr[res1.stderr.find('{'):res1.stderr.rfind('}')+1]
    stats = json.loads(json_str)

    # Step D: Pass 2 - Precision Linear Mastering into final master MP4
    ln_filter = (
        f"loudnorm=I={t_lufs}:TP=-1.6:LRA=7.0:"
        f"measured_I={stats['input_i']}:"
        f"measured_TP={stats['input_tp']}:"
        f"measured_LRA={stats['input_lra']}:"
        f"measured_thresh={stats['input_thresh']}:"
        f"offset={stats['target_offset']}:linear=true"
    )
    
    cmd_pass2 = [
        FFMPEG, "-y",
        "-i", raw_mp4,
        "-i", temp_mix_wav,
        "-af", ln_filter,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",
        "-shortest",
        final_mp4
    ]
    subprocess.run(cmd_pass2, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Step E: Produce 720p web copy with faststart
    cmd_web = [
        FFMPEG, "-y",
        "-i", final_mp4,
        "-vf", "scale=720:1280",
        "-c:v", "libx264",
        "-crf", "22",
        "-preset", "fast",
        "-c:a", "copy",
        "-movflags", "+faststart",
        web_mp4
    ]
    subprocess.run(cmd_web, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Step F: Measure final audio on both master and web
    def measure_lufs(path):
        meas_cmd = [FFMPEG, "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"]
        r = subprocess.run(meas_cmd, capture_output=True, text=True)
        i_val, tp_val = None, None
        for line in r.stderr.splitlines()[-25:]:
            if "I:" in line and "LUFS" in line and i_val is None:
                m = re.search(r"I:\s+([-\d.]+)\s+LUFS", line)
                if m: i_val = float(m.group(1))
            if "Peak:" in line and "dBFS" in line and tp_val is None:
                m = re.search(r"Peak:\s+([-\d.]+)\s+dBFS", line)
                if m: tp_val = float(m.group(1))
        return i_val, tp_val

    m_i, m_tp = measure_lufs(final_mp4)
    w_i, w_tp = measure_lufs(web_mp4)

    print(f"  Master MP4: {final_mp4}")
    print(f"    Integrated: {m_i} LUFS | True Peak: {m_tp} dBTP")
    print(f"  Web 720p MP4: {web_mp4}")
    print(f"    Integrated: {w_i} LUFS | True Peak: {w_tp} dBTP")

    m_pass = (abs(m_i - (-14.0)) <= 0.5) and (m_tp <= -1.5)
    w_pass = (abs(w_i - (-14.0)) <= 0.5) and (w_tp <= -1.5)
    print(f"  Quality Gate Verdict: Master {'PASS' if m_pass else 'FAIL'} | Web {'PASS' if w_pass else 'FAIL'}")
    return m_pass and w_pass

if __name__ == "__main__":
    t_start = time.time()
    for cfg in REELS:
        ok = render_comp(cfg["comp_id"], cfg["raw_mp4"])
        if not ok:
            print(f"FATAL: Remotion render failed for {cfg['comp_id']}", flush=True)
            sys.exit(1)
        ok_m = mux_and_master(cfg)
        if not ok_m:
            print(f"FATAL: Mux & Mastering failed for {cfg['id']}", flush=True)
            sys.exit(1)
    print(f"\n[ALL RENDERS & MASTERING COMPLETED IN {time.time() - t_start:.1f}s]")
