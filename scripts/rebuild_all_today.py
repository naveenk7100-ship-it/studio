import os
import sys
import shutil
import subprocess
import json
import time

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
OUT_DIR = os.path.join(ROOT, "out")
DOCS_VIDEOS = os.path.join(ROOT, "docs", "videos")

print("================ STEP 1: CLEANING STALE ASSETS ================")
stale_files = [
    os.path.join(OUT_DIR, "raw_today_1_anatomy.mp4"),
    os.path.join(OUT_DIR, "raw_today_2_browseruse.mp4"),
    os.path.join(OUT_DIR, "reel_today_1_anatomy.mp4"),
    os.path.join(OUT_DIR, "reel_today_2_browseruse.mp4"),
    os.path.join(DOCS_VIDEOS, "reel_today_1_anatomy_720p.mp4"),
    os.path.join(DOCS_VIDEOS, "reel_today_2_browseruse_720p.mp4"),
]
for f in stale_files:
    if os.path.exists(f):
        os.remove(f)
        print(f"Removed stale file: {f}")

print("\n================ STEP 2: RENDERING & MASTERING REELS ================")
render_script = os.path.join(ROOT, "scripts", "render_and_master_today_reels.py")
subprocess.run([sys.executable, render_script], check=True, cwd=ROOT)

print("\n================ STEP 3: GENERATING 8-BEAT CONTACT SHEETS ================")
sheets_script = os.path.join(ROOT, "scripts", "generate_today_contact_sheets.py")
subprocess.run([sys.executable, sheets_script], check=True, cwd=ROOT)

print("\n================ STEP 4: RUNNING REAL-FILE GATES ================")
gates_script = os.path.join(ROOT, "scripts", "run_real_file_gates.py")
subprocess.run([sys.executable, gates_script], check=True, cwd=ROOT)

print("\n================ STEP 5: BUILDING REVIEW DASHBOARD & DOCS ================")
dash_script = os.path.join(ROOT, "scripts", "build_today_dashboard.py")
subprocess.run([sys.executable, dash_script], check=True, cwd=ROOT)

print("\n================ STEP 6: RUNNING REGRESSION TESTS ================")
test_script = os.path.join(ROOT, "tests", "regression", "run_all_regression.py")
subprocess.run([sys.executable, test_script], check=True, cwd=ROOT)

print("\n>>> ALL TODAY PRODUCTION STEPS COMPLETED!")
