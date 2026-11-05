"""
Render all 3 Cinematic Visual-Metaphor Essay compositions + Showcase Bumper via Remotion CLI.
1. CinematicEssay-Unslop (840 frames) -> out/raw_essay_1_unslop.mp4
2. CinematicEssay-UV (840 frames) -> out/raw_essay_2_uv.mp4
3. CinematicEssay-Kimi (840 frames) -> out/raw_essay_3_kimi.mp4
4. ShowcaseBumper (600 frames) -> out/raw_showcase_bumper.mp4
"""

import os
import subprocess
import time
import sys

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
ENG_DIR = os.path.join(ROOT, "engine")
OUT_DIR = os.path.join(ROOT, "out")
REMOTION_BIN = os.path.join(ENG_DIR, "node_modules", ".bin", "remotion.cmd")

RENDERS = [
    ("CinematicEssay-Unslop", os.path.join(OUT_DIR, "raw_essay_1_unslop.mp4")),
    ("CinematicEssay-UV", os.path.join(OUT_DIR, "raw_essay_2_uv.mp4")),
    ("CinematicEssay-Kimi", os.path.join(OUT_DIR, "raw_essay_3_kimi.mp4")),
    ("ShowcaseBumper", os.path.join(OUT_DIR, "raw_showcase_bumper.mp4")),
]

def render_comp(comp_id, out_mp4):
    print(f"\n=======================================================", flush=True)
    print(f">>> STARTING RENDER: {comp_id} -> {out_mp4}", flush=True)
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
        return True
    else:
        print(f">>> FAILED: {comp_id} (code {res.returncode}):", flush=True)
        print(res.stderr or res.stdout, flush=True)
        return False

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for comp_id, out_mp4 in RENDERS:
        ok = render_comp(comp_id, out_mp4)
        if not ok:
            print(f"FATAL: Render failed for {comp_id}", flush=True)
            sys.exit(1)
    print("\n[ALL 4 RENDERS COMPLETED SUCCESSFULLY]")
