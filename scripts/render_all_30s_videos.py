"""
Render all 3 Golden 30s Explainer compositions via Remotion CLI.
1. Golden30s-vLLM (840 frames) -> out/raw_golden_30s_1.mp4
2. Golden30s-ClaudeCode (840 frames) -> out/raw_golden_30s_2.mp4
3. Golden30s-MCP (840 frames) -> out/raw_golden_30s_3.mp4
"""

import os
import subprocess
import time

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
ENG_DIR = os.path.join(ROOT, "engine")
OUT_DIR = os.path.join(ROOT, "out")

RENDERS = [
    ("Golden30s-vLLM", os.path.join(OUT_DIR, "raw_golden_30s_1.mp4")),
    ("Golden30s-ClaudeCode", os.path.join(OUT_DIR, "raw_golden_30s_2.mp4")),
    ("Golden30s-MCP", os.path.join(OUT_DIR, "raw_golden_30s_3.mp4")),
]

def render_comp(comp_id, out_mp4):
    print(f"\n>>> Starting render for {comp_id} -> {out_mp4}")
    t0 = time.time()
    cmd = [
        "npx.cmd", "remotion", "render",
        comp_id,
        out_mp4,
        "--gl=angle",
        "--concurrency=4",
    ]
    res = subprocess.run(cmd, cwd=ENG_DIR, capture_output=True, text=True)
    dt = time.time() - t0
    if res.returncode == 0:
        print(f">>> Render succeeded for {comp_id} in {dt:.1f}s")
        return True
    else:
        print(f">>> FAILED to render {comp_id} (code {res.returncode}):")
        print(res.stderr or res.stdout)
        return False

if __name__ == "__main__":
    for comp_id, out_mp4 in RENDERS:
        ok = render_comp(comp_id, out_mp4)
        if not ok:
            print(f"Aborting sequence due to error in {comp_id}")
            break
