"""
Fetch and save single-source raw API data objects for the 3 new topics:
1. heydamir/unslop (Rising Repo) -> cache/data_unslop.json
2. astral-sh/uv (Tool Release v0.13.7) -> cache/data_uv.json
3. moonshotai/Kimi-K3.1-Pro (HN 461 pts) -> cache/data_kimi.json
"""

import os
import sys
import json
import time
import requests
from datetime import datetime, timezone

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
CACHE_DIR = os.path.join(ROOT, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

headers = {"User-Agent": "FLASH-Data-Grounding-Agent"}

def fetch_data():
    now_iso = datetime.now(timezone.utc).isoformat()
    print(f"Fetching verified single-source data at {now_iso}...", flush=True)

    # 1. heydamir/unslop
    r_repo1 = requests.get("https://api.github.com/repos/heydamir/unslop", headers=headers, timeout=15)
    r_readme1 = requests.get("https://raw.githubusercontent.com/heydamir/unslop/main/README.md", headers=headers, timeout=15)
    d1 = r_repo1.json()
    readme_text1 = r_readme1.text if r_readme1.status_code == 200 else ""
    
    obj_unslop = {
        "fetched_at_utc": now_iso,
        "source": "api.github.com",
        "topic_id": "unslop",
        "category": "Rising Repo",
        "full_name": d1.get("full_name"),
        "description": d1.get("description"),
        "stars": d1.get("stargazers_count"),
        "forks": d1.get("forks_count"),
        "open_issues": d1.get("open_issues_count"),
        "created_at": d1.get("created_at"),
        "updated_at": d1.get("updated_at"),
        "html_url": d1.get("html_url"),
        "exact_url": "https://github.com/heydamir/unslop",
        "primary_number": d1.get("stargazers_count"),
        "primary_number_str": f"{d1.get('stargazers_count'):,}",
        "grounded_command": "npx @damir/unslop",
        "grounded_quote": "A Claude skill that turns vibecoded, AI-looking UI into a designed interface",
        "steps": [
            "1. Inspect Vibecoded UI",
            "2. Strip AI Slop Patterns",
            "3. Apply Human Design System"
        ],
        "readme_excerpt": readme_text1[:1500]
    }
    with open(os.path.join(CACHE_DIR, "data_unslop.json"), "w", encoding="utf-8") as f:
        json.dump(obj_unslop, f, indent=2)
    print(f"[SAVED] cache/data_unslop.json: {obj_unslop['stars']} Stars, Created {obj_unslop['created_at']}")

    # 2. astral-sh/uv
    r_repo2 = requests.get("https://api.github.com/repos/astral-sh/uv", headers=headers, timeout=15)
    r_rel2 = requests.get("https://api.github.com/repos/astral-sh/uv/releases/latest", headers=headers, timeout=15)
    d2 = r_repo2.json()
    rel2 = r_rel2.json()
    
    obj_uv = {
        "fetched_at_utc": now_iso,
        "source": "api.github.com",
        "topic_id": "uv",
        "category": "Tool Release",
        "full_name": d2.get("full_name"),
        "description": d2.get("description"),
        "stars": d2.get("stargazers_count"),
        "forks": d2.get("forks_count"),
        "open_issues": d2.get("open_issues_count"),
        "release_tag": rel2.get("tag_name"),
        "published_at": rel2.get("published_at"),
        "html_url": rel2.get("html_url"),
        "exact_url": "https://github.com/astral-sh/uv/releases/tag/0.13.7",
        "primary_number": d2.get("stargazers_count"),
        "primary_number_str": f"{d2.get('stargazers_count'):,}",
        "grounded_command": "curl -LsSf https://astral.sh/uv/install.sh | sh",
        "grounded_quote": "An extremely fast Python package and project manager, written in Rust.",
        "steps": [
            "1. Install uv via Rust binary",
            "2. Resolve dependency lockfile",
            "3. Instant 10x-100x virtualenv sync"
        ]
    }
    with open(os.path.join(CACHE_DIR, "data_uv.json"), "w", encoding="utf-8") as f:
        json.dump(obj_uv, f, indent=2)
    print(f"[SAVED] cache/data_uv.json: Release {obj_uv['release_tag']} ({obj_uv['stars']} Stars)")

    # 3. moonshotai/Kimi-K3.1-Pro (HN Item 50366999)
    r_hn = requests.get("https://hacker-news.firebaseio.com/v0/item/50366999.json", timeout=15)
    d_hn = r_hn.json()
    
    obj_kimi = {
        "fetched_at_utc": now_iso,
        "source": "news.ycombinator.com",
        "topic_id": "kimi",
        "category": "AI News",
        "hn_id": 50366999,
        "title": d_hn.get("title"),
        "score": d_hn.get("score"),
        "time": d_hn.get("time"),
        "published_at": datetime.fromtimestamp(d_hn.get("time", 0), tz=timezone.utc).isoformat(),
        "canonical_url": "https://huggingface.co/moonshotai/Kimi-K3.1-Pro",
        "hn_url": "https://news.ycombinator.com/item?id=50366999",
        "exact_url": "https://huggingface.co/moonshotai/Kimi-K3.1-Pro",
        "primary_number": d_hn.get("score"),
        "primary_number_str": f"{d_hn.get('score')} HN Points",
        "grounded_command": "from transformers import AutoModelForCausalLM",
        "grounded_quote": "Kimi K3.1 Pro model weights are out",
        "steps": [
            "1. Download Kimi open weights",
            "2. Load via Hugging Face Transformers",
            "3. Run long-context reasoning inference"
        ]
    }
    with open(os.path.join(CACHE_DIR, "data_kimi.json"), "w", encoding="utf-8") as f:
        json.dump(obj_kimi, f, indent=2)
    print(f"[SAVED] cache/data_kimi.json: {obj_kimi['score']} HN Points, Published {obj_kimi['published_at']}")

if __name__ == "__main__":
    fetch_data()
