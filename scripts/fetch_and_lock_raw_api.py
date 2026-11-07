import urllib.request
import json
import os
import sys
from datetime import datetime, timezone

sys.stdout.reconfigure(encoding='utf-8')

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
CACHE_DIR = os.path.join(ROOT, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

REPOS = {
    "today_1_anatomy": {
        "repo": "wheresryan22/anatomy",
        "raw_file": "raw_api_anatomy.json"
    },
    "today_2_browseruse": {
        "repo": "browser-use/browser-use",
        "raw_file": "raw_api_browseruse.json"
    }
}

now_utc = datetime.now(timezone.utc).isoformat()

for key, item in REPOS.items():
    repo = item["repo"]
    url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        data["_fetched_at_utc"] = now_utc
        
        # If browser-use, also fetch latest release
        if "browser-use" in repo:
            rel_url = f"https://api.github.com/repos/{repo}/releases/latest"
            rel_req = urllib.request.Request(rel_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(rel_req) as rel_resp:
                data["_latest_release"] = json.loads(rel_resp.read().decode("utf-8"))
        
        dst = os.path.join(CACHE_DIR, item["raw_file"])
        with open(dst, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Locked {repo} raw API data to {dst} at {now_utc}")
        print(f"  Stars: {data.get('stargazers_count'):,}")
        if "_latest_release" in data:
            print(f"  Release Tag: {data['_latest_release'].get('tag_name')} at {data['_latest_release'].get('published_at')}")
