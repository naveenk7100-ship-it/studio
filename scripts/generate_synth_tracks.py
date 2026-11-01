"""Procedural Royalty-Free Audio Synthesizer & Music Library Generator.

Generates custom high-fidelity stereo backing tracks (BPM synced, ambient synth chords,
percussion pulses, basslines) for each mood so the studio is 100% self-contained and zero-copyright-risk.
"""
import os
import math
import json
import wave
import struct
import numpy as np
import subprocess

try:
    import imageio_ffmpeg
    FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_BIN = "ffmpeg"

SAMPLE_RATE = 44100

MOOD_CONFIGS = {
    "hype": {"bpm": 130, "root": 60, "scale": [0, 3, 5, 7, 10], "energy": 5, "style": "punchy"},
    "futuristic": {"bpm": 124, "root": 57, "scale": [0, 2, 3, 7, 9], "energy": 4, "style": "cyber"},
    "chill-focus": {"bpm": 92, "root": 62, "scale": [0, 2, 4, 7, 9], "energy": 2, "style": "lofi"},
    "dark-tech": {"bpm": 120, "root": 55, "scale": [0, 1, 5, 7, 8], "energy": 4, "style": "drone"},
    "inspiring": {"bpm": 118, "root": 65, "scale": [0, 2, 4, 5, 7, 9, 11], "energy": 4, "style": "uplifting"},
    "news-urgent": {"bpm": 135, "root": 58, "scale": [0, 3, 5, 6, 7], "energy": 5, "style": "ticker"},
    "playful": {"bpm": 110, "root": 64, "scale": [0, 2, 4, 7, 9], "energy": 3, "style": "bouncy"}
}

def midi_to_freq(m):
    return 440.0 * (2.0 ** ((m - 69.0) / 12.0))

def generate_track(mood: str, duration_sec: float = 45.0) -> np.ndarray:
    cfg = MOOD_CONFIGS[mood]
    bpm = cfg["bpm"]
    beat_dur = 60.0 / bpm
    n_samples = int(SAMPLE_RATE * duration_sec)
    t = np.linspace(0, duration_sec, n_samples, endpoint=False)

    left = np.zeros(n_samples)
    right = np.zeros(n_samples)

    # 1. Bass / Pad Chords
    chord_dur = beat_dur * 4
    n_chords = int(math.ceil(duration_sec / chord_dur))
    for c_idx in range(n_chords):
        c_start = int(c_idx * chord_dur * SAMPLE_RATE)
        c_end = min(n_samples, int((c_idx + 1) * chord_dur * SAMPLE_RATE))
        if c_start >= n_samples:
            break
        c_len = c_end - c_start
        c_t = np.linspace(0, c_len / SAMPLE_RATE, c_len, endpoint=False)

        # Scale degree progression
        deg = cfg["scale"][c_idx % len(cfg["scale"])]
        base_freq = midi_to_freq(cfg["root"] + deg - 12)

        # Soft envelope with low attack and decay
        env = np.sin(np.pi * np.clip(c_t / (chord_dur), 0, 1)) ** 0.5

        # Sub-bass + detuned stereo pads
        left[c_start:c_end] += 0.22 * np.sin(2 * np.pi * base_freq * c_t) * env
        right[c_start:c_end] += 0.22 * np.sin(2 * np.pi * (base_freq * 1.004) * c_t) * env

        # Mid pad harmony
        mid_freq = midi_to_freq(cfg["root"] + deg + 7)
        left[c_start:c_end] += 0.12 * np.sin(2 * np.pi * mid_freq * c_t) * env
        right[c_start:c_end] += 0.12 * np.sin(2 * np.pi * (mid_freq * 0.996) * c_t) * env

    # 2. Rhythm & Beat pulse
    beat_samples = int(beat_dur * SAMPLE_RATE)
    for b in range(int(duration_sec / beat_dur)):
        b_pos = int(b * beat_dur * SAMPLE_RATE)
        p_len = min(int(0.12 * SAMPLE_RATE), n_samples - b_pos)
        if p_len <= 0 or b_pos >= n_samples:
            continue
        p_t = np.linspace(0, p_len / SAMPLE_RATE, p_len, endpoint=False)

        # Soft filtered kick on quarter notes
        if b % 2 == 0 or cfg["style"] == "punchy":
            kick = np.sin(2 * np.pi * (80.0 * np.exp(-35 * p_t)) * p_t) * np.exp(-18 * p_t)
            left[b_pos:b_pos + p_len] += 0.35 * kick
            right[b_pos:b_pos + p_len] += 0.35 * kick

        # Subtle hi-hat / shaker tick on offbeats
        if b % 2 == 1 or cfg["style"] == "cyber":
            noise = (np.random.rand(p_len) * 2 - 1) * np.exp(-55 * p_t)
            left[b_pos:b_pos + p_len] += 0.08 * noise
            right[b_pos:b_pos + p_len] += 0.08 * noise

    # 3. Master normalization & soft limit
    mix = np.vstack([left, right])
    peak = np.max(np.abs(mix)) or 1.0
    mix = (mix / peak) * 0.82  # Target ~ -1.8dB true peak

    # 4. Fade in (1.5s) and fade out (2.0s)
    fade_in_len = int(1.5 * SAMPLE_RATE)
    fade_out_len = int(2.0 * SAMPLE_RATE)
    mix[:, :fade_in_len] *= np.linspace(0, 1, fade_in_len)
    mix[:, -fade_out_len:] *= np.linspace(1, 0, fade_out_len)

    return mix


def save_track_mp3(audio_data: np.ndarray, wav_path: str, mp3_path: str):
    """Save audio array as WAV then transcode to MP3 via ffmpeg."""
    n_samples = audio_data.shape[1]
    int16_data = np.clip(audio_data * 32767.0, -32768, 32767).astype(np.int16)
    interleaved = np.empty((n_samples * 2,), dtype=np.int16)
    interleaved[0::2] = int16_data[0]
    interleaved[1::2] = int16_data[1]

    os.makedirs(os.path.dirname(wav_path), exist_ok=True)
    with wave.open(wav_path, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(interleaved.tobytes())

    # Transcode to high quality 192kbps MP3
    os.makedirs(os.path.dirname(mp3_path), exist_ok=True)
    subprocess.run(
        [FFMPEG_BIN, "-y", "-i", wav_path, "-codec:a", "libmp3lame", "-b:a", "192k", mp3_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )
    if os.path.exists(wav_path):
        os.remove(wav_path)


def build_music_library(output_dir: str):
    """Generate all 7 mood tracks and create music.json catalog."""
    music_dir = os.path.join(output_dir, "assets", "music")
    index = []

    print("[MUSIC] Building royalty-free procedural music library...")
    for mood, cfg in MOOD_CONFIGS.items():
        mood_folder = os.path.join(music_dir, mood)
        os.makedirs(mood_folder, exist_ok=True)

        track_filename = f"{mood}_pulse.mp3"
        mp3_path = os.path.join(mood_folder, track_filename)
        wav_path = os.path.join(mood_folder, f"{mood}_temp.wav")

        print(f"  [MUSIC] Synthesizing '{mood}' track ({cfg['bpm']} BPM, style: {cfg['style']})...")
        audio = generate_track(mood, duration_sec=45.0)
        save_track_mp3(audio, wav_path, mp3_path)

        meta = {
            "track_id": f"{mood}_01",
            "title": f"CyberPulse: {mood.capitalize()}",
            "mood": mood,
            "energy": cfg["energy"],
            "bpm": cfg["bpm"],
            "duration": 45.0,
            "file": f"assets/music/{mood}/{track_filename}",
            "license": "Royalty-Free / Generated Studio CC0",
            "source_url": "studio://internal-synth",
            "attribution": "Music: AI Auto-Reels Studio"
        }
        index.append(meta)

    # Save music.json
    index_file = os.path.join(music_dir, "music.json")
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    print(f"[MUSIC SUCCESS] Generated {len(index)} royalty-free tracks in {music_dir}/music.json")
    return index

if __name__ == "__main__":
    studio_root = r"C:\Users\navee\OneDrive\Desktop\studio"
    build_music_library(studio_root)
