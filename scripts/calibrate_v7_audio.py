"""
Calibrate Master Audio for both v7_tools and v7_discovery to ensure:
- Integrated Loudness: -14.0 +/- 0.5 LUFS
- True Peak: <= -1.5 dBTP
- Sample Rate: exactly 48000 Hz
"""
import subprocess
import json
import os

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"

def calibrate(reel_id: str, dur: float, voice_boost_db: float = 0.0):
    mix_wav = os.path.join(ROOT, "cache", "v7", f"{reel_id}_mix.wav")
    master_mp3 = os.path.join(ROOT, "cache", "v7", f"{reel_id}_master_48k.mp3")
    voice_wav = os.path.join(ROOT, "cache", "v7", f"{reel_id}_voice_calibrated.wav")
    music_wav = os.path.join(ROOT, "cache", "v7", f"{reel_id}_music.wav")
    
    # 1. Mix voice + music
    af_voice = f"[0:a]volume={voice_boost_db:.2f}dB[v];[v][1:a]" if voice_boost_db != 0 else "[0:a][1:a]"
    cmd_mix = [
        "ffmpeg", "-y",
        "-i", voice_wav,
        "-i", music_wav,
        "-filter_complex",
        f"{af_voice}amix=inputs=2:duration=first:dropout_transition=2[mix];[mix]apad=pad_dur=3.0,atrim=0:{dur}[out]",
        "-map", "[out]",
        "-ar", "48000",
        mix_wav
    ]
    subprocess.run(cmd_mix, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. Pass 1: Measure
    cmd_p1 = [
        "ffmpeg", "-y", "-i", mix_wav,
        "-af", "loudnorm=I=-14.0:TP=-1.9:LRA=7:print_format=json",
        "-f", "null", "-"
    ]
    p1 = subprocess.run(cmd_p1, capture_output=True, text=True)
    raw = p1.stderr
    stats = json.loads(raw[raw.rfind("{"):raw.rfind("}")+1])
    
    # 3. Pass 2: Render 48k MP3
    af_p2 = (
        f"loudnorm=I=-14.0:TP=-1.9:LRA=7:"
        f"measured_I={stats['input_i']}:"
        f"measured_TP={stats['input_tp']}:"
        f"measured_LRA={stats['input_lra']}:"
        f"measured_thresh={stats['input_thresh']}:"
        f"offset={stats['target_offset']}"
    )
    cmd_p2 = [
        "ffmpeg", "-y", "-i", mix_wav,
        "-af", af_p2,
        "-ar", "48000",
        "-c:a", "mp3",
        "-b:a", "192k",
        master_mp3
    ]
    subprocess.run(cmd_p2, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 4. Verify
    cmd_v = [
        "ffmpeg", "-i", master_mp3,
        "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7:print_format=json",
        "-f", "null", "-"
    ]
    pv = subprocess.run(cmd_v, capture_output=True, text=True)
    v_raw = pv.stderr
    vstats = json.loads(v_raw[v_raw.rfind("{"):v_raw.rfind("}")+1])
    
    # Check sample rate
    cmd_pr = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", master_mp3]
    pr = subprocess.run(cmd_pr, capture_output=True, text=True)
    pr_json = json.loads(pr.stdout)
    sr = int(pr_json["streams"][0]["sample_rate"])
    
    print(f"[{reel_id}] Final I: {vstats['input_i']} LUFS, True Peak: {vstats['input_tp']} dBTP, Sample Rate: {sr} Hz")
    return {
        "integrated_lufs": float(vstats["input_i"]),
        "true_peak_dbtp": float(vstats["input_tp"]),
        "lra": float(vstats["input_lra"]),
        "sample_rate": sr
    }

if __name__ == "__main__":
    t_res = calibrate("v7_tools", 48.0, voice_boost_db=0.0)
    d_res = calibrate("v7_discovery", 50.0, voice_boost_db=2.5)
