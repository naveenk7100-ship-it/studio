import os
import sys
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
ANATOMY_DIR = os.path.join(ROOT, "engine", "public", "captured_proofs", "wheresryan22_anatomy")
BROWSERUSE_DIR = os.path.join(ROOT, "engine", "public", "captured_proofs", "browser_use")
ASSETS_ANATOMY = os.path.join(ROOT, "assets", "captured_proofs", "wheresryan22_anatomy")
ASSETS_BROWSERUSE = os.path.join(ROOT, "assets", "captured_proofs", "browser_use")

for d in [ANATOMY_DIR, BROWSERUSE_DIR, ASSETS_ANATOMY, ASSETS_BROWSERUSE]:
    os.makedirs(d, exist_ok=True)

# 1. Anatomy real figures
anatomy_files = [
    ("raptor-engine-firing.webp", "https://raw.githubusercontent.com/wheresryan22/anatomy/main/.github/assets/raptor-engine-firing.webp"),
    ("raptor-engine-apart.webp", "https://raw.githubusercontent.com/wheresryan22/anatomy/main/.github/assets/raptor-engine-apart.webp"),
    ("turning-dial.webp", "https://raw.githubusercontent.com/wheresryan22/anatomy/main/.github/assets/turning-dial.webp"),
    ("ripple-tank.webp", "https://raw.githubusercontent.com/wheresryan22/anatomy/main/.github/assets/ripple-tank.webp"),
    ("dial-indicator.webp", "https://raw.githubusercontent.com/wheresryan22/anatomy/main/.github/assets/dial-indicator.webp"),
]

for name, url in anatomy_files:
    dst1 = os.path.join(ANATOMY_DIR, name)
    dst2 = os.path.join(ASSETS_ANATOMY, name)
    try:
        urllib.request.urlretrieve(url, dst1)
        urllib.request.urlretrieve(url, dst2)
        print(f"Downloaded Anatomy asset: {name} ({os.path.getsize(dst1)} bytes)")
    except Exception as e:
        print(f"Error downloading {name}: {e}")

# 2. Browser-use real figures
browseruse_files = [
    ("browser-use-dark.png", "https://raw.githubusercontent.com/browser-use/browser-use/main/static/browser-use-dark.png"),
    ("accuracy_by_model_dark.png", "https://raw.githubusercontent.com/browser-use/browser-use/main/static/accuracy_by_model_dark.png"),
    ("hard_benchmark_v2.jpg", "https://raw.githubusercontent.com/browser-use/browser-use/main/static/hard_benchmark_v2.jpg"),
]

for name, url in browseruse_files:
    dst1 = os.path.join(BROWSERUSE_DIR, name)
    dst2 = os.path.join(ASSETS_BROWSERUSE, name)
    try:
        urllib.request.urlretrieve(url, dst1)
        urllib.request.urlretrieve(url, dst2)
        print(f"Downloaded Browser-use asset: {name} ({os.path.getsize(dst1)} bytes)")
    except Exception as e:
        print(f"Error downloading {name}: {e}")
