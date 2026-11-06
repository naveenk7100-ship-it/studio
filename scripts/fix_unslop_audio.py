import os
import subprocess
import re
import json
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
OUT_DIR = os.path.join(ROOT, "out")
CACHE_DIR = os.path.join(ROOT, "cache")
MUSIC_DIR = os.path.join(ROOT, "assets", "music")

voice_mp3 = os.path.join(CACHE_DIR, "voice_final_unslop.mp3")
norm_voice = os.path.join(CACHE_DIR, "voice_norm_unslop.wav")

# Pre-normalize voice to -13.8 LUFS
subprocess.run([FFMPEG, "-y", "-i", voice_mp3, "-af", "loudnorm=I=-13.8:TP=-1.5:LRA=7.0", norm_voice], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

music_mp3 = os.path.join(MUSIC_DIR, "dark-tech", "dark-tech_pulse.mp3")
raw_mp4 = os.path.join(OUT_DIR, "raw_essay_1_unslop.mp4")
temp_wav = os.path.join(CACHE_DIR, "temp_unslop_pass1.wav")
final_mp4 = os.path.join(OUT_DIR, "reel_essay_1_unslop.mp4")

premix_filter = "[0:a]volume=1.0,acompressor=threshold=-15dB:ratio=3.5:attack=5:release=50[v];[1:a]volume=0.040[m];[v][m]amix=inputs=2:duration=first:dropout_transition=2[aout]"
subprocess.run([
    FFMPEG, "-y", "-i", norm_voice, "-stream_loop", "-1", "-i", music_mp3,
    "-filter_complex", premix_filter, "-map", "[aout]", "-c:a", "pcm_s16le", "-ar", "48000", temp_wav
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

meas_cmd = [FFMPEG, "-i", temp_wav, "-af", "loudnorm=I=-14.0:TP=-1.8:LRA=7.0:print_format=json", "-f", "null", "-"]
res1 = subprocess.run(meas_cmd, capture_output=True, text=True, errors="ignore")
lines = res1.stderr.splitlines()
json_lines = []
cap = False
for l in lines:
    if "{" in l: cap = True
    if cap: json_lines.append(l)
    if "}" in l and cap: break
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
    FFMPEG, "-y", "-i", raw_mp4, "-i", temp_wav,
    "-af", ln_filter, "-map", "0:v:0", "-map", "1:a:0",
    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
    final_mp4
]
subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

res = subprocess.run([FFMPEG, "-i", final_mp4, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True, errors="ignore")
summary_lines = res.stderr.split("Summary:")[-1]
m_i = re.search(r"I:\s+([-\d.]+)\s+LUFS", summary_lines)
m_tp = re.search(r"Peak:\s+([-\d.]+)\s+dBFS", summary_lines)
i_val = float(m_i.group(1)) if m_i else None
tp_val = float(m_tp.group(1)) if m_tp else None
is_pass = (abs(i_val - (-14.0)) <= 0.5) and (tp_val <= -1.5)
print(f"PRE-NORM VOICE UNSLOP: Integrated = {i_val} LUFS, Peak = {tp_val} dBTP -> PASS: {is_pass}")

if os.path.exists(temp_wav):
    try: os.remove(temp_wav)
    except: pass
if os.path.exists(norm_voice):
    try: os.remove(norm_voice)
    except: pass
