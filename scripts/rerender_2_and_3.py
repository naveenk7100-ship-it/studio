import os
import sys
import json
import time

HERE = r"C:\Users\navee\OneDrive\Desktop\studio"
sys.path.insert(0, HERE)

import config
import tts
import render
import quality_gates
import queue_manager
from scripts.analyze_voice_match import analyze_audio_match, format_voice_match_table
from scripts.render_fresh_hardened_videos import FRESH_TOPICS

OUT_DIR = os.path.join(HERE, "out")
RUNS_DIR = os.path.join(HERE, "runs")

for spec in FRESH_TOPICS[1:]:  # Video 2 (Keynote) and Video 3 (Breaking News)
    stamp = spec["id"]
    print(f"\nRE-RENDERING WITH GRAIN NOISE & AUTO-TRIM: {spec['title']} ({spec['template']})...")
    voice_path = os.path.join(OUT_DIR, f"{stamp}_voice.mp3")
    video_path = os.path.join(OUT_DIR, f"{stamp}_{spec['template']}.mp4")
    contact_sheet = video_path.replace(".mp4", "_contact_sheet.png")
    meta_path = os.path.join(RUNS_DIR, f"{stamp}_meta.json")

    spoken_text = " ".join(s["voice"] for s in spec["scenes"])
    words = tts.make_voice(spoken_text, voice_path)
    dur = render.render(spec, words, voice_path, video_path, template_override=spec["template"], music=True)
    print(f"Rendered in {dur:.2f}s: {video_path}")

    audio_metrics = analyze_audio_match(video_path)
    print("\n" + format_voice_match_table(audio_metrics, spec["title"]))

    run_meta = {
        "id": stamp,
        "title": spec["title"],
        "template": spec["template"],
        "template_name": render.templates.TEMPLATES_CATALOG[spec["template"]]["name"],
        "video_path": video_path,
        "contact_sheet": contact_sheet,
        "duration": dur,
        "music_db_under_voice": -24.0,
        "music_mood": spec["mood"],
        "tts_engine": f"Gemini TTS ({config.ACTIVE_VOICE}, Mixed Script)",
        "sources": spec["sources"],
        "captions_table": [{"caption_display": s["voice"], "phonetic_tts": tts.normalize_for_tts(s["voice"])} for s in spec["scenes"]],
        "script": spec,
        "voice_match": audio_metrics
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(run_meta, f, indent=2, default=str)

    checker = quality_gates.QualityGateChecker(meta_path)
    gate_results = checker.check_all()
    print("\n" + quality_gates.format_gate_table(gate_results))
    queue_manager.add_item_to_queue(run_meta)

print("Re-render of videos 2 and 3 complete!")
