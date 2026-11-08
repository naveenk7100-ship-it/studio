import subprocess
import json

mix_wav = 'cache/v7/v7_disc_mix_new.wav'
out_mp3 = 'cache/v7/v7_discovery_master_48k.mp3'

# Clamp peak transients to 0.45 (-7 dBFS) and boost by +2.2 dB
cmd_clamp = [
    'ffmpeg', '-y', '-i', 'cache/v7/v7_disc_boosted.wav',
    '-af', 'alimiter=limit=0.45:attack=3:release=30:asc=true,volume=2.2dB',
    'cache/v7/v7_disc_clamped.wav'
]
subprocess.run(cmd_clamp, check=True)

mix_wav = 'cache/v7/v7_disc_clamped.wav'

# Pass 1
cmd_p1 = ['ffmpeg', '-y', '-i', mix_wav, '-af', 'loudnorm=I=-14.0:TP=-1.6:LRA=7:print_format=json', '-f', 'null', '-']
p1 = subprocess.run(cmd_p1, capture_output=True, text=True)
s = json.loads(p1.stderr[p1.stderr.rfind('{'):p1.stderr.rfind('}')+1])

# Pass 2
m_i = s["input_i"]
m_tp = s["input_tp"]
m_lra = s["input_lra"]
m_thresh = s["input_thresh"]
offset = s["target_offset"]

af_p2 = f"loudnorm=I=-14.0:TP=-1.5:LRA=7:measured_I={m_i}:measured_TP={m_tp}:measured_LRA={m_lra}:measured_thresh={m_thresh}:offset={offset}:linear=true"
cmd_p2 = ['ffmpeg', '-y', '-i', mix_wav, '-af', af_p2, '-ar', '48000', '-c:a', 'mp3', '-b:a', '192k', out_mp3]
subprocess.run(cmd_p2, check=True)

# Verify
p = subprocess.run(['ffmpeg', '-i', out_mp3, '-af', 'loudnorm=I=-14.0:TP=-1.5:LRA=7:print_format=json', '-f', 'null', '-'], capture_output=True, text=True)
vs = json.loads(p.stderr[p.stderr.rfind('{'):p.stderr.rfind('}')+1])
print('TWO-PASS DISCOVERY RESULT -> I:', vs['input_i'], 'LUFS, Peak:', vs['input_tp'], 'dBTP')
