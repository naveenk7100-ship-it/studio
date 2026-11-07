"""
Capture Mobile-First Dashboard Screenshots via Playwright (iPhone 14 Emulation: 390x844)
"""
import os
import shutil
from playwright.sync_api import sync_playwright

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
DOCS_DIR = os.path.join(ROOT, "docs")
REVIEW_HTML = os.path.join(DOCS_DIR, "review", "index.html")
ARTIFACT_DIR = r"C:\Users\navee\.gemini\antigravity\brain\8b5ef5ec-ac96-4092-ba21-368a898ca77f"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

def capture_screenshots():
    with sync_playwright() as p:
        iphone = p.devices["iPhone 14"]
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(**iphone)
        page = context.new_page()

        file_url = f"file:///{REVIEW_HTML.replace(os.sep, '/')}"
        print(f"Loading {file_url} with iPhone 14 emulation...", flush=True)
        page.goto(file_url, wait_until="networkidle")
        page.wait_for_timeout(1000)

        # 1. Viewport (Above the Fold)
        vp_path = os.path.join(DOCS_DIR, "review-mobile-viewport.png")
        page.screenshot(path=vp_path, full_page=False)
        print(f"Captured above-the-fold screenshot -> {vp_path}")

        # 2. Full Page
        fp_path = os.path.join(DOCS_DIR, "review-mobile-iphone14.png")
        page.screenshot(path=fp_path, full_page=True)
        print(f"Captured full-page screenshot -> {fp_path}")

        # Copy to artifact directory for presentation
        art_vp = os.path.join(ARTIFACT_DIR, "review_mobile_viewport.png")
        art_fp = os.path.join(ARTIFACT_DIR, "review_mobile_iphone14.png")
        shutil.copy2(vp_path, art_vp)
        shutil.copy2(fp_path, art_fp)

        browser.close()

if __name__ == "__main__":
    capture_screenshots()
    print("[MOBILE SCREENSHOTS CAPTURED SUCCESSFULLY]")
