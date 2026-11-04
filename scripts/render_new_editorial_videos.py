"""
Render all 3 New Editorial Clean Explainer compositions via Remotion CLI.
1. NewEditorial-SuperAgent (840 frames) -> out/raw_new_1_superagent.mp4
2. NewEditorial-Ollama (840 frames) -> out/raw_new_2_ollama.mp4
3. NewEditorial-QwenNews (840 frames) -> out/raw_new_3_qwen_news.mp4
"""

import os
import subprocess
import time

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
ENG_DIR = os.path.join(ROOT, "engine")
OUT_DIR = os.path.join(ROOT, "out")
REMOTION_BIN = os.path.join(ENG_DIR, "node_modules", ".bin", "remotion.cmd")

RENDERS = [
    ("NewEditorial-SuperAgent", os.path.join(OUT_DIR, "raw_new_1_superagent.mp4")),
    ("NewEditorial-Ollama", os.path.join(OUT_DIR, "raw_new_2_ollama.mp4")),
    ("NewEditorial-QwenNews", os.path.join(OUT_DIR, "raw_new_3_qwen_news.mp4")),
]

def render_comp(comp_id, out_mp4):
    print(f"\n>>> Starting render for {comp_id} -> {out_mp4}", flush=True)
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
        print(f">>> Render succeeded for {comp_id} in {dt:.1f}s", flush=True)
        return True
    else:
        print(f">>> FAILED to render {comp_id} (code {res.returncode}):", flush=True)
        print(res.stderr or res.stdout, flush=True)
        return False

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for comp_id, out_mp4 in RENDERS:
        ok = render_comp(comp_id, out_mp4)
        if not ok:
            print(f"Aborting sequence due to error in {comp_id}", flush=True)
            exit(1)
    print("\nAll 3 New Editorial videos rendered successfully!")
