"""
FLASH Content OS - 4 Cinematic Essay Reels Audio Muxer & EBU R128 Masterer
Performs calibrated 2-pass broadcast-grade mastering:
Target: Integrated Loudness = -14.0 LUFS ± 0.5, True Peak <= -1.5 dBTP, 48,000 Hz, stereo AAC 192 kbps
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
        "id": "reel_essay_1_unslop",
        "raw_mp4": os.path.join(OUT_DIR, "raw_essay_1_unslop.mp4"),
        "voice_mp3": os.path.join(CACHE_DIR, "voice_final_unslop.mp3"),
        "music_mp3": os.path.join(MUSIC_DIR, "futuristic", "futuristic_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "reel_essay_1_unslop.mp4"),
        "threshold": "-14dB",
        "ratio": "3.0",
        "target_lufs": -13.1,
    },
    {
        "id": "reel_essay_2_uv",
        "raw_mp4": os.path.join(OUT_DIR, "raw_essay_2_uv.mp4"),
        "voice_mp3": os.path.join(CACHE_DIR, "voice_final_uv.mp3"),
        "music_mp3": os.path.join(MUSIC_DIR, "dark-tech", "dark-tech_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "reel_essay_2_uv.mp4"),
        "threshold": "-15dB",
        "ratio": "3.5",
        "target_lufs": -13.8,
    },
    {
        "id": "reel_essay_3_kimi",
        "raw_mp4": os.path.join(OUT_DIR, "raw_essay_3_kimi.mp4"),
        "voice_mp3": os.path.join(CACHE_DIR, "voice_final_kimi.mp3"),
        "music_mp3": os.path.join(MUSIC_DIR, "news-urgent", "news-urgent_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "reel_essay_3_kimi.mp4"),
        "threshold": "-14dB",
        "ratio": "3.0",
        "target_lufs": -13.5,
    },
    {
        "id": "reel_essay_4_craft",
        "raw_mp4": os.path.join(OUT_DIR, "raw_essay_4_craft.mp4"),
        "voice_mp3": os.path.join(CACHE_DIR, "voice_final_craft.mp3"),
        "music_mp3": os.path.join(MUSIC_DIR, "futuristic", "futuristic_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "reel_essay_4_craft.mp4"),
        "threshold": "-15dB",
        "ratio": "3.5",
        "target_lufs": -13.6,
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
    t_lufs = video_conf.get("target_lufs", -13.5)
    
    print(f"\n================ Processing {vid_id} (Target I={t_lufs}) ================", flush=True)
    if not os.path.exists(raw_mp4):
        print(f"ERROR: Raw MP4 not found at {raw_mp4}", flush=True)
        return False

    temp_mix_wav = os.path.join(CACHE_DIR, f"temp_mix_{vid_id}.wav")

    # Step A: Pre-mix voice + compressed music to intermediate 48k wav
    premix_filter = (
        f"[0:a]volume=1.0,acompressor=threshold={thresh}:ratio={ratio}:attack=5:release=50[v];"
        f"[1:a]volume=0.038[m];"
        f"[v][m]amix=inputs=2:duration=first:dropout_transition=2[aout]"
    )
    premix_cmd = [
        FFMPEG, "-y",
        "-i", voice_mp3,
        "-stream_loop", "-1", "-i", music_mp3,
        "-filter_complex", premix_filter,
        "-map", "[aout]",
        "-c:a", "pcm_s16le",
        "-ar", "48000",
        temp_mix_wav
    ]
    subprocess.run(premix_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Step B: Pass 1 - Measure loudnorm parameters
    meas_cmd = [
        FFMPEG, "-i", temp_mix_wav,
        "-af", f"loudnorm=I={t_lufs}:TP=-1.8:LRA=7.0:print_format=json",
        "-f", "null", "-"
    ]
    res1 = subprocess.run(meas_cmd, capture_output=True, text=True, errors="ignore")
    json_lines = []
    capturing = False
    for line in res1.stderr.splitlines():
        if "{" in line:
            capturing = True
        if capturing:
            json_lines.append(line)
        if "}" in line and capturing:
            break
            
    stats = json.loads("\n".join(json_lines))

    # Step C: Pass 2 - Precision Linear Mastering into final MP4 with video stream copy
    ln_filter = (
        f"loudnorm=I={t_lufs}:TP=-1.8:LRA=7.0:"
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
    
    # Step D: Final EBU R128 verification measurement
    meas_cmd2 = [FFMPEG, "-i", final_mp4, "-af", "ebur128=peak=true", "-f", "null", "-"]
    res2 = subprocess.run(meas_cmd2, capture_output=True, text=True)
    
    i_val, tp_val = None, None
    for line in res2.stderr.splitlines()[-25:]:
        if "I:" in line and "LUFS" in line and i_val is None:
            m = re.search(r"I:\s+([-\d.]+)\s+LUFS", line)
            if m: i_val = float(m.group(1))
        if "Peak:" in line and "dBFS" in line and tp_val is None:
            m = re.search(r"Peak:\s+([-\d.]+)\s+dBFS", line)
            if m: tp_val = float(m.group(1))

    # Clean temp file
    if os.path.exists(temp_mix_wav):
        try: os.remove(temp_mix_wav)
        except: pass

    print(f"  Final Mastered File: {final_mp4}")
    print(f"  Measured Integrated Loudness: {i_val} LUFS (Target: -14.0 LUFS ± 0.5)")
    print(f"  Measured True Peak: {tp_val} dBTP (Target: <= -1.5 dBTP)")
    
    # Strict Quality gate checks (tolerance ±0.5 LUFS)
    lufs_pass = abs(i_val - (-14.0)) <= 0.5 if i_val is not None else False
    tp_pass = (tp_val <= -1.5) if tp_val is not None else False
    
    print(f"  Gate Verdict: Loudness {'PASS' if lufs_pass else 'FAIL'} | True Peak {'PASS' if tp_pass else 'FAIL'}")
    return lufs_pass and tp_pass

def mux_bumper():
    raw_mp4 = os.path.join(OUT_DIR, "raw_showcase_bumper.mp4")
    final_mp4 = os.path.join(OUT_DIR, "showcase_bumper.mp4")
    music_mp3 = os.path.join(MUSIC_DIR, "futuristic", "futuristic_pulse.mp3")
    if not os.path.exists(raw_mp4):
        print(f"ERROR: Raw bumper not found at {raw_mp4}")
        return False
    print(f"\n================ Processing Showcase Bumper ================", flush=True)
    
    temp_music = os.path.join(CACHE_DIR, "temp_music_bumper.wav")
    subprocess.run([
        FFMPEG, "-y", "-i", music_mp3, "-t", "15.0", "-c:a", "pcm_s16le", "-ar", "48000", temp_music
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    meas_cmd = [FFMPEG, "-i", temp_music, "-af", "loudnorm=I=-14.0:TP=-1.8:LRA=7.0:print_format=json", "-f", "null", "-"]
    res1 = subprocess.run(meas_cmd, capture_output=True, text=True, errors="ignore")
    json_lines = []
    capturing = False
    for line in res1.stderr.splitlines():
        if "{" in line: capturing = True
        if capturing: json_lines.append(line)
        if "}" in line and capturing: break
    stats = json.loads("\n".join(json_lines))
    
    ln_filter = (
        f"loudnorm=I=-14.0:TP=-1.8:LRA=7.0:"
        f"measured_I={stats['input_i']}:"
        f"measured_TP={stats['input_tp']}:"
        f"measured_LRA={stats['input_lra']}:"
        f"measured_thresh={stats['input_thresh']}:"
        f"offset={stats['target_offset']}:linear=true"
    )
    
    cmd = [
        FFMPEG, "-y",
        "-i", raw_mp4,
        "-i", temp_music,
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
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(temp_music):
        try: os.remove(temp_music)
        except: pass
    print(f"  Showcase Bumper mastered -> {final_mp4}")
    return True

if __name__ == "__main__":
    results = []
    for v in VIDEOS:
        ok = mux_and_master(v)
        results.append(ok)
    mux_bumper()
    all_ok = all(results)
    print(f"\n[MASTERING FINISHED] All 4 reels passed strict -14.0 ±0.5 LUFS: {all_ok}")
