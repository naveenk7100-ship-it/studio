import os
from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = r"C:\Users\navee\OneDrive\Desktop\studio\assets\screenshots"
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

targets = [
    {
        "url": "https://github.com/anthropics/claude-code",
        "output": os.path.join(SCREENSHOTS_DIR, "claude_code_repo.png"),
        "wait_for": "article"
    },
    {
        "url": "https://modelcontextprotocol.io/introduction",
        "output": os.path.join(SCREENSHOTS_DIR, "mcp_docs_official.png"),
        "wait_for": "main"
    },
    {
        "url": "https://github.com/anthropics/claude-quickstarts",
        "output": os.path.join(SCREENSHOTS_DIR, "claude_quickstarts_repo.png"),
        "wait_for": "article"
    }
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for target in targets:
        try:
            print(f"Capturing: {target['url']} -> {target['output']}...")
            page = browser.new_page(viewport={"width": 1280, "height": 820})
            page.goto(target["url"], timeout=20000, wait_until="domcontentloaded")
            page.wait_for_timeout(1500)
            page.screenshot(path=target["output"])
            page.close()
            print(f"Saved: {target['output']}")
        except Exception as e:
            print(f"Failed to capture {target['url']}: {e}")
    browser.close()

print("All Playwright captures complete!")
