import subprocess, re, imageio_ffmpeg, json, os

exe = imageio_ffmpeg.get_ffmpeg_exe()
in_audio = r"C:\Users\navee\OneDrive\Desktop\studio\out\voice_tests\gemini_aoede_mixed.mp3"
bg_music = r"C:\Users\navee\OneDrive\Desktop\studio\assets\music\chill-focus\chill-focus_pulse.mp3"

tmp_mix = r"C:\Users\navee\OneDrive\Desktop\studio\out\voice_tests\tmp_raw_mix.wav"
cmd_mix = [
    exe, "-y", "-i", in_audio, "-stream_loop", "-1", "-i", bg_music,
    "-filter_complex", "[1:a]volume=0.063[m];[0:a][m]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[aout]",
    "-map", "[aout]", "-ar", "48000", tmp_mix
]
subprocess.run(cmd_mix, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

# Pass 1: Measure raw mix
cmd_p1 = [exe, "-i", tmp_mix, "-af", "loudnorm=I=-14.0:TP=-1.7:LRA=7:print_format=json", "-f", "null", "-"]
res1 = subprocess.run(cmd_p1, capture_output=True, text=True, errors="ignore")
json_str = res1.stderr[res1.stderr.rfind("{"):res1.stderr.rfind("}")+1]
p1 = json.loads(json_str)
print("PASS 1 RAW MIX STATS:")
print(f"  input_i: {p1['input_i']} LUFS (offset needed: {p1['target_offset']} dB)")
print(f"  input_tp: {p1['input_tp']} dBTP")

# Pass 2: Two-pass linear correction with limiter
out_mp4 = r"C:\Users\navee\OneDrive\Desktop\studio\out\voice_tests\tmp_two_pass_mastered.mp4"
p2_filter = (
    f"loudnorm=I=-14.0:TP=-1.5:LRA=7:"
    f"measured_I={p1['input_i']}:measured_TP={p1['input_tp']}:"
    f"measured_LRA={p1['input_lra']}:measured_thresh={p1['input_thresh']}:"
    f"offset={p1['target_offset']}:linear=true,"
    f"alimiter=limit=-1.7dB"
)
cmd_p2 = [
    exe, "-y", "-f", "lavfi", "-i", "color=c=black:s=1080x1920:d=13.4",
    "-i", tmp_mix, "-filter_complex", f"[1:a]{p2_filter}[aout]",
    "-map", "0:v", "-map", "[aout]", "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
    out_mp4
]
subprocess.run(cmd_p2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

# Pass 3: Final EBU R128 re-measurement
cmd_m = [exe, "-i", out_mp4, "-af", "ebur128=peak=true", "-f", "null", "-"]
res_m = subprocess.run(cmd_m, capture_output=True, text=True, errors="ignore")

summary_lines = []
capturing = False
for line in res_m.stderr.splitlines():
    if "Summary:" in line:
        capturing = True
    if capturing:
        summary_lines.append(line)

print("\nPASS 2 FINAL MP4 MEASUREMENT:")
print("\n".join(summary_lines[:15]))
