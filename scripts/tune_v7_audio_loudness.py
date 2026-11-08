"""
Tune audio loudness and true peak for both v7_tools and v7_discovery:
Target:
  Integrated Loudness: -14.0 +/- 0.5 LUFS
  True Peak: <= -1.5 dBTP
  Sample Rate: 48000 Hz
"""
import subprocess
import json
import os

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"

def process(reel_id, dur, voice_boost_db, target_i=-14.0):
    voice_wav = os.path.join(ROOT, "cache", "v7", f"{reel_id}_voice_calibrated.wav")
    music_wav = os.path.join(ROOT, "cache", "v7", f"{reel_id}_music.wav")
    mix_wav = os.path.join(ROOT, "cache", "v7", f"{reel_id}_mix_tuned.wav")
    master_mp3 = os.path.join(ROOT, "cache", "v7", f"{reel_id}_master_48k.mp3")
    
    cmd_m = [
        "ffmpeg", "-y",
        "-i", voice_wav,
        "-i", music_wav,
        "-filter_complex",
        f"[0:a]volume={voice_boost_db:.2f}dB[v];[v][1:a]amix=inputs=2:duration=first:dropout_transition=2[mix];[mix]apad=pad_dur=3.0,atrim=0:{dur}[out]",
        "-map", "[out]", "-ar", "48000",
        mix_wav
    ]
    subprocess.run(cmd_m, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Pass 1
    cmd_p1 = [
        "ffmpeg", "-y", "-i", mix_wav,
        "-af", f"loudnorm=I={target_i}:TP=-1.6:LRA=7:print_format=json",
        "-f", "null", "-"
    ]
    p1 = subprocess.run(cmd_p1, capture_output=True, text=True)
    raw = p1.stderr
    s = json.loads(raw[raw.rfind("{"):raw.rfind("}")+1])
    
    # Pass 2 with dual-pass parameters
    af_p2 = (
        f"loudnorm=I={target_i}:TP=-1.6:LRA=7:"
        f"measured_I={s['input_i']}:"
        f"measured_TP={s['input_tp']}:"
        f"measured_LRA={s['input_lra']}:"
        f"measured_thresh={s['input_thresh']}:"
        f"offset={s['target_offset']}"
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
    
    # Verify with standard -14 LUFS measurement
    cmd_v = [
        "ffmpeg", "-i", master_mp3,
        "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7:print_format=json",
        "-f", "null", "-"
    ]
    pv = subprocess.run(cmd_v, capture_output=True, text=True)
    v_raw = pv.stderr
    vs = json.loads(v_raw[v_raw.rfind("{"):v_raw.rfind("}")+1])
    
    # ffprobe check
    cmd_pr = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", master_mp3]
    pr = subprocess.run(cmd_pr, capture_output=True, text=True)
    pr_json = json.loads(pr.stdout)
    sr = int(pr_json["streams"][0]["sample_rate"])
    
    print(f"[{reel_id}] Tuned -> I: {vs['input_i']} LUFS, True Peak: {vs['input_tp']} dBTP, Sample Rate: {sr} Hz")
    return vs

if __name__ == "__main__":
    t_s = process("v7_tools", 48.0, voice_boost_db=0.0, target_i=-14.0)
    d_s = process("v7_discovery", 50.0, voice_boost_db=0.0, target_i=-12.5)
