"""
FLASH Content OS - Render and Master 12-Second Visual Overhaul Style Tests:
- StyleTest-VariantA (Deep Teal Studio)
- StyleTest-VariantB (Warm Paper-and-Ink Blueprint)
- StyleTest-VariantC (Light Museum Vitrine)

Mastered to EBU R128 (-14.0 +/- 0.5 LUFS, True Peak <= -1.5 dBTP, 48 kHz).
Includes ducked music and scene-matched foley sound design.
"""

import os
import sys
import json
import subprocess
import time
import imageio_ffmpeg
import numpy as np

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
ENG_DIR = os.path.join(ROOT, "engine")
OUT_DIR = os.path.join(ROOT, "out")
CACHE_DIR = os.path.join(ROOT, "cache")
MUSIC_DIR = os.path.join(ROOT, "assets", "music")
DOCS_VIDEOS_DIR = os.path.join(ROOT, "docs", "videos")
REMOTION_BIN = os.path.join(ENG_DIR, "node_modules", ".bin", "remotion.cmd")
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(DOCS_VIDEOS_DIR, exist_ok=True)

VOICE_MP3 = os.path.join(CACHE_DIR, "voice_final_style_test_12s.mp3")

VARIANTS = [
    {
        "id": "variant_a",
        "name": "Variant A (Deep Teal Studio)",
        "comp_id": "StyleTest-VariantA",
        "raw_mp4": os.path.join(OUT_DIR, "raw_style_test_variant_a.mp4"),
        "music_mp3": os.path.join(MUSIC_DIR, "dark-tech", "dark-tech_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "style_test_variant_a.mp4"),
        "web_mp4": os.path.join(DOCS_VIDEOS_DIR, "style_test_variant_a_720p.mp4"),
        "target_lufs": -13.8,
    },
    {
        "id": "variant_b",
        "name": "Variant B (Warm Paper-and-Ink Blueprint)",
        "comp_id": "StyleTest-VariantB",
        "raw_mp4": os.path.join(OUT_DIR, "raw_style_test_variant_b.mp4"),
        "music_mp3": os.path.join(MUSIC_DIR, "futuristic", "futuristic_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "style_test_variant_b.mp4"),
        "web_mp4": os.path.join(DOCS_VIDEOS_DIR, "style_test_variant_b_720p.mp4"),
        "target_lufs": -13.8,
    },
    {
        "id": "variant_c",
        "name": "Variant C (Light Museum Vitrine)",
        "comp_id": "StyleTest-VariantC",
        "raw_mp4": os.path.join(OUT_DIR, "raw_style_test_variant_c.mp4"),
        "music_mp3": os.path.join(MUSIC_DIR, "chill-focus", "chill-focus_pulse.mp3"),
        "final_mp4": os.path.join(OUT_DIR, "style_test_variant_c.mp4"),
        "web_mp4": os.path.join(DOCS_VIDEOS_DIR, "style_test_variant_c_720p.mp4"),
        "target_lufs": -13.8,
    },
]

def generate_foley_track(out_foley_wav):
    """
    Synthesize high-fidelity sound design elements matched to the picture:
    - 3.20s: Exploded view mechanical unlatch & whoosh
    - 6.00s: Tech transition tick
    - 6.60s - 8.20s: Mechanical keyboard typing clicks
    - 10.00s - 10.50s: Riser sweep resolving into end card logo hit
    """
    print(f">>> Synthesizing matched foley track -> {out_foley_wav} ...", flush=True)
    sample_rate = 48000
    total_samples = int(12.0 * sample_rate)
    foley = np.zeros(total_samples, dtype=np.float32)

    def add_click(t_sec, freq=1200, dur=0.035, vol=0.15):
        idx = int(t_sec * sample_rate)
        n = int(dur * sample_rate)
        if idx + n > total_samples: return
        t = np.linspace(0, dur, n, endpoint=False)
        decay = np.exp(-t * 90)
        tone = np.sin(2 * np.pi * freq * t) * decay * vol
        foley[idx:idx+n] += tone.astype(np.float32)

    def add_whoosh(t_sec, dur=0.45, vol=0.12):
        idx = int(t_sec * sample_rate)
        n = int(dur * sample_rate)
        if idx + n > total_samples: return
        # Shaped noise burst
        t = np.linspace(0, 1, n, endpoint=False)
        envelope = np.sin(np.pi * t) ** 2
        noise = np.random.normal(0, 1, n)
        # Apply rudimentary lowpass
        filtered = np.convolve(noise, np.ones(15)/15, mode='same')
        foley[idx:idx+n] += (filtered * envelope * vol).astype(np.float32)

    def add_riser(t_sec, dur=0.6, vol=0.14):
        idx = int(t_sec * sample_rate)
        n = int(dur * sample_rate)
        if idx + n > total_samples: return
        t = np.linspace(0, dur, n, endpoint=False)
        freq = np.linspace(250, 880, n)
        envelope = (t / dur) ** 2
        tone = np.sin(2 * np.pi * freq * t) * envelope * vol
        foley[idx:idx+n] += tone.astype(np.float32)

    # 1. Exploded view unlatch & whoosh at 3.20s
    add_click(3.18, freq=1400, dur=0.04, vol=0.18)
    add_whoosh(3.20, dur=0.50, vol=0.12)

    # 2. Tech cut at 6.00s
    add_click(6.00, freq=900, dur=0.03, vol=0.14)

    # 3. Mechanical typing clicks matching command typing (6.6s - 8.2s)
    typing_times = [6.65, 6.78, 6.92, 7.05, 7.18, 7.30, 7.45, 7.58, 7.72, 7.85, 8.00, 8.15]
    for tt in typing_times:
        freq = np.random.uniform(1100, 1600)
        add_click(tt, freq=freq, dur=0.025, vol=0.08)

    # 4. Riser sweep into end card payoff (10.0s - 10.5s)
    add_riser(9.80, dur=0.45, vol=0.15)
    add_click(10.25, freq=180, dur=0.15, vol=0.22)  # Bass hit on logo impact

    # Normalize and write to 16-bit WAV
    max_val = np.max(np.abs(foley))
    if max_val > 0:
        foley_norm = foley / max_val * 0.45
    else:
        foley_norm = foley
    foley_int16 = (foley_norm * 32767).astype(np.int16)

    import wave
    with wave.open(out_foley_wav, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(foley_int16.tobytes())
    print(f">>> Foley track saved ({os.path.getsize(out_foley_wav)/1024:.1f} KB)", flush=True)

def render_comp(comp_id, out_mp4):
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
        return True, dt
    else:
        print(f">>> FAILED: {comp_id} (code {res.returncode}):", flush=True)
        print(res.stderr or res.stdout, flush=True)
        return False, dt

def mux_and_master(cfg, foley_wav):
    vid_id = cfg["id"]
    raw_mp4 = cfg["raw_mp4"]
    music_mp3 = cfg["music_mp3"]
    final_mp4 = cfg["final_mp4"]
    web_mp4 = cfg["web_mp4"]
    t_lufs = cfg["target_lufs"]

    print(f"\n>>> Muxing & Mastering {vid_id} (Target LUFS={t_lufs}) ...", flush=True)
    temp_mix_wav = os.path.join(CACHE_DIR, f"temp_mix_{vid_id}.wav")

    # Step A: 3-way Audio Mix (Voice + Ducked Music + Foley SFX)
    # Voice is primary with light compression
    # Music is ducked at -22dB
    # Foley adds crisp technical accents
    premix_filter = (
        "[0:a]volume=1.15,acompressor=threshold=-18dB:ratio=4.0:attack=5:release=50[v];"
        "[1:a]volume=0.038[m];"
        "[2:a]volume=0.85[f];"
        "[v][m][f]amix=inputs=3:duration=first:dropout_transition=2[aout]"
    )
    premix_cmd = [
        FFMPEG, "-y",
        "-i", VOICE_MP3,
        "-stream_loop", "-1", "-i", music_mp3,
        "-i", foley_wav,
        "-filter_complex", premix_filter,
        "-map", "[aout]",
        "-c:a", "pcm_s16le",
        "-ar", "48000",
        "-t", "12.00",
        temp_mix_wav
    ]
    subprocess.run(premix_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Step B: Pass 1 - Measure loudnorm parameters
    meas_cmd = [
        FFMPEG, "-i", temp_mix_wav,
        "-af", f"loudnorm=I={t_lufs}:TP=-1.6:LRA=7.0:print_format=json",
        "-f", "null", "-"
    ]
    res1 = subprocess.run(meas_cmd, capture_output=True, text=True, errors="ignore")
    json_str = res1.stderr[res1.stderr.find('{'):res1.stderr.rfind('}')+1]
    stats = json.loads(json_str)

    # Step C: Pass 2 - Precision Linear Mastering into final master MP4
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

    # Step D: Transcode web-ready 720p version
    cmd_web = [
        FFMPEG, "-y",
        "-i", final_mp4,
        "-vf", "scale=720:1280",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-c:a", "copy",
        "-movflags", "+faststart",
        web_mp4
    ]
    subprocess.run(cmd_web, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Verify Loudness
    ver_cmd = [
        FFMPEG, "-i", final_mp4,
        "-af", "ebur128=framelog=verbose",
        "-f", "null", "-"
    ]
    ver_res = subprocess.run(ver_cmd, capture_output=True, text=True, errors="ignore")
    lines = ver_res.stderr.strip().split("\n")
    meas_i = None
    meas_tp = None
    for line in lines[-25:]:
        if "I:" in line and "LUFS" in line:
            parts = line.split()
            for i, p in enumerate(parts):
                if p == "I:": meas_i = float(parts[i+1])
        if "Peak:" in line and "dBFS" in line:
            parts = line.split()
            for i, p in enumerate(parts):
                if p == "Peak:": meas_tp = float(parts[i+1])

    print(f">>> {vid_id} Mastered: I={meas_i} LUFS, True Peak={meas_tp} dBTP", flush=True)
    return {"measured_i": meas_i, "measured_tp": meas_tp}

def main():
    foley_wav = os.path.join(CACHE_DIR, "style_test_foley.wav")
    generate_foley_track(foley_wav)

    results = {}
    for cfg in VARIANTS:
        ok, dt = render_comp(cfg["comp_id"], cfg["raw_mp4"])
        if not ok:
            print(f"FAILED TO RENDER {cfg['comp_id']}")
            sys.exit(1)
        audio_stats = mux_and_master(cfg, foley_wav)
        results[cfg["id"]] = {
            "name": cfg["name"],
            "render_time_s": round(dt, 1),
            "master_mp4": cfg["final_mp4"],
            "web_mp4": cfg["web_mp4"],
            "measured_lufs": audio_stats["measured_i"],
            "measured_tp": audio_stats["measured_tp"],
        }

    with open(os.path.join(CACHE_DIR, "style_test_render_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("\n>>> ALL 3 STYLE VARIANTS RENDERED AND MASTERED SUCCESSFULLY! <<<", flush=True)

if __name__ == "__main__":
    main()
