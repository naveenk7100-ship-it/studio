"""
FLASH Content OS - Playwright Headless Verification of GitHub Pages & Review Dashboard
1. Starts a lightweight local HTTP server serving docs/
2. Navigates to http://localhost:8089/index.html:
   - Verifies all 5 HTML5 <video> elements are present (4 reels + showcase bumper)
   - Verifies the single-source telemetry numbers appear in the DOM:
     - "9,054 Stars" (heydamir / unslop)
     - "91,559 Stars" (astral-sh / uv 0.13.7)
     - "532 HN Points" (Moonshot AI Kimi K3.1 Pro)
     - "13,530 Stars" (storytold / craft-anything)
3. Navigates to http://localhost:8089/review/index.html:
   - Verifies mobile viewport (390x844 iPhone 14)
   - Verifies 5 tabs: Today, Queue, Analytics, Health, Settings
   - Verifies playable HTML5 video element
   - Verifies Approve, Post Now, Reject, Regenerate, Edit Caption action buttons
   - Verifies 8-gate quality checklist
   - Verifies 1-tap copy buttons (Caption, Comment, Description, Tags)
   - Verifies license attribution and exact verified command blocks
"""

import os
import sys
import time
import http.server
import socketserver
import threading
from playwright.sync_api import sync_playwright

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
DOCS_DIR = os.path.join(ROOT, "docs")
PORT = 8089

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DOCS_DIR, **kwargs)

def run_test():
    print(f"\n================ PLAYWRIGHT HEADLESS VERIFICATION OF GITHUB PAGES ================", flush=True)
    
    httpd = socketserver.TCPServer(("", PORT), Handler)
    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()
    print(f"Local HTTP server started at http://localhost:{PORT}/", flush=True)
    
    time.sleep(1)
    
    summary = {
        "index_passed": False,
        "review_passed": False,
        "overall_pass": False,
    }
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            
            # --- Test 1: Public Portal index.html ---
            print("\n>>> Testing Public Portal (index.html)...", flush=True)
            page = browser.new_page(viewport={"width": 1280, "height": 900})
            url = f"http://localhost:{PORT}/index.html"
            page.goto(url, wait_until="networkidle")
            
            title = page.title()
            print(f"  Page Title: {title}", flush=True)
            page_content = page.content()
            
            expected_numbers = [
                ("9,054 Stars", "heydamir / unslop"),
                ("91,559 Stars", "astral-sh / uv"),
                ("532 HN Points", "Kimi K3.1 Pro"),
                ("13,530 Stars", "storytold / craft-anything"),
            ]
            
            num_ok = True
            for expected_num, label in expected_numbers:
                if expected_num in page_content:
                    print(f"  [PASS] Single-Source Data Verified in DOM: '{expected_num}' for {label}", flush=True)
                else:
                    print(f"  [FAIL] Missing expected number '{expected_num}' for {label}", flush=True)
                    num_ok = False
                    
            video_elements = page.query_selector_all("video")
            print(f"  Found {len(video_elements)} video elements on index.html (Expected: 5).", flush=True)
            videos_ok = len(video_elements) == 5
            for idx, vid in enumerate(video_elements):
                src = page.evaluate("(v) => v.currentSrc || v.querySelector('source')?.src", vid)
                print(f"    Video #{idx+1}: src={src}", flush=True)
                
            summary["index_passed"] = num_ok and videos_ok
            page.close()
            
            # --- Test 2: Mobile Review Dashboard review/index.html ---
            print("\n>>> Testing Mobile Review Dashboard (review/index.html)...", flush=True)
            mobile_page = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
            review_url = f"http://localhost:{PORT}/review/index.html"
            mobile_page.goto(review_url, wait_until="networkidle")
            
            rev_title = mobile_page.title()
            print(f"  Review Page Title: {rev_title}", flush=True)
            
            # Check 5 tabs in navigation
            nav_buttons = mobile_page.query_selector_all(".nav-btn")
            print(f"  Found {len(nav_buttons)} bottom navigation tabs (Expected: 5).", flush=True)
            tabs_ok = len(nav_buttons) == 5
            
            # Check video element
            rev_videos = mobile_page.query_selector_all("video")
            print(f"  Found {len(rev_videos)} active video elements on review dashboard.", flush=True)
            rev_vids_ok = len(rev_videos) >= 1
            
            # Check action buttons (Approve, Post Now, Reject, Regenerate, Edit Caption)
            actions_ok = True
            for btn_text in ["APPROVE", "POST NOW", "Reject", "Regenerate", "Edit Caption"]:
                btn = mobile_page.query_selector(f"button:has-text('{btn_text}')")
                if btn:
                    print(f"  [PASS] Found Action Button: '{btn_text}'", flush=True)
                else:
                    print(f"  [FAIL] Missing Action Button: '{btn_text}'", flush=True)
                    actions_ok = False
            
            # Check 8-gate quality checklist presence
            gate_elements = mobile_page.query_selector_all(".gate-cell")
            print(f"  Found {len(gate_elements)} quality gate audit cells (Expected: >= 8).", flush=True)
            gates_ok = len(gate_elements) >= 8
            
            # Check copy buttons
            copy_pills = mobile_page.query_selector_all(".copy-pill")
            print(f"  Found {len(copy_pills)} 1-tap copy buttons.", flush=True)
            copy_ok = len(copy_pills) >= 4
            
            # Check license credits in DOM
            rev_content = mobile_page.content()
            lic_ok = True
            for lic_sub in ["CC BY 4.0", "MIT / Apache-2.0"]:
                if lic_sub in rev_content:
                    print(f"  [PASS] Verified License in DOM: '{lic_sub}'", flush=True)
                else:
                    print(f"  [FAIL] Missing license string '{lic_sub}'", flush=True)
                    lic_ok = False
                    
            # Check exact commands in DOM
            cmd_ok = True
            for cmd_sub in ["git clone https://github.com/heydamir/unslop", "curl -LsSf https://astral.sh/uv/install.sh"]:
                if cmd_sub in rev_content:
                    print(f"  [PASS] Verified Exact Command in DOM: '{cmd_sub}'", flush=True)
                else:
                    print(f"  [FAIL] Missing exact command '{cmd_sub}'", flush=True)
                    cmd_ok = False
                    
            summary["review_passed"] = tabs_ok and rev_vids_ok and actions_ok and gates_ok and copy_ok and lic_ok and cmd_ok
            mobile_page.close()
            browser.close()
            
        summary["overall_pass"] = summary["index_passed"] and summary["review_passed"]
        print(f"\n================ PLAYWRIGHT VERIFICATION SUMMARY ================", flush=True)
        print(f"  Public Portal index.html: {'PASS' if summary['index_passed'] else 'FAIL'}", flush=True)
        print(f"  Mobile Review Dashboard:   {'PASS' if summary['review_passed'] else 'FAIL'}", flush=True)
        print(f"  OVERALL PLAYWRIGHT SUITE:  {'PASS (ALL CHECKS PASSED)' if summary['overall_pass'] else 'FAIL'}", flush=True)
    finally:
        httpd.shutdown()
        print("Local HTTP server shutdown completed.", flush=True)
        
    return summary

if __name__ == "__main__":
    res = run_test()
    if not res["overall_pass"]:
        sys.exit(1)
