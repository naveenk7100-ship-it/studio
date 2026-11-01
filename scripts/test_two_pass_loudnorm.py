import subprocess, json, re, imageio_ffmpeg, os

exe = imageio_ffmpeg.get_ffmpeg_exe()
in_audio = r"C:\Users\navee\OneDrive\Desktop\studio\out\voice_tests\gemini_aoede_mixed.mp3"

# 1. Pass 1: Measure
cmd1 = [exe, "-i", in_audio, "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7:print_format=json", "-f", "null", "-"]
res1 = subprocess.run(cmd1, capture_output=True, text=True, errors="ignore")
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
print("PASS 1 MEASURED STATS:")
for k in ["input_i", "input_tp", "input_lra", "input_thresh", "target_offset"]:
    print(f"  {k}: {stats.get(k)}")

# 2. Pass 2: Apply linear true loudnorm + limiter at -1.7 dB
out_mastered = r"C:\Users\navee\OneDrive\Desktop\studio\out\voice_tests\test_mastered_aoede.mp3"
ln_filter = (
    f"loudnorm=I=-14.0:TP=-1.5:LRA=7:"
    f"measured_I={stats['input_i']}:"
    f"measured_TP={stats['input_tp']}:"
    f"measured_LRA={stats['input_lra']}:"
    f"measured_thresh={stats['input_thresh']}:"
    f"offset={stats['target_offset']}:linear=true,"
    f"alimiter=limit=-1.7dB"
)
cmd2 = [exe, "-y", "-i", in_audio, "-af", ln_filter, "-ar", "48000", "-b:a", "192k", out_mastered]
subprocess.run(cmd2, capture_output=True, check=True)

# 3. Re-measure the mastered audio
cmd3 = [exe, "-i", out_mastered, "-af", "ebur128=peak=true", "-f", "null", "-"]
res3 = subprocess.run(cmd3, capture_output=True, text=True, errors="ignore")
print("\nPASS 2 RE-MEASURED EBUR128 VERIFICATION:")
for line in res3.stderr.splitlines()[-15:]:
    print(" ", line)
