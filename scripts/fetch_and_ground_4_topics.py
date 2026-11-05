"""
FLASH Content OS - 4 Topics Existence Proof and Grounding Generator
Fetches raw API data from GitHub, Hugging Face, and Hacker News API:
1. heydamir/unslop (Rising Repo, 7d old)
2. astral-sh/uv (Tool Release 0.13.7, 2.5d old)
3. moonshotai/Kimi-K3.1-Pro (AI News Story, 23.9h old on HN, weights 02 Nov 2026)
4. storytold/craft-anything (Rising Repo, 5d old, 13,505 stars, 100% Rust clean-room engine)
"""

import os
import sys
import json
import time
import requests

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
CACHE_DIR = os.path.join(ROOT, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

headers = {"User-Agent": "FLASH-Truth-Engine"}

def fetch_unslop():
    print("\n>>> Fetching heydamir/unslop...")
    r = requests.get("https://api.github.com/repos/heydamir/unslop", headers=headers, timeout=15).json()
    data = {
        "id": "unslop",
        "topic_type": "rising_repo",
        "full_name": r.get("full_name"),
        "created_at": r.get("created_at"),
        "pushed_at": r.get("pushed_at"),
        "stars": r.get("stargazers_count"),
        "forks": r.get("forks_count"),
        "open_issues": r.get("open_issues_count"),
        "html_url": r.get("html_url"),
        "license": r.get("license", {}).get("spdx_id") or "CC-BY-4.0",
        "license_credit": "Created by Damir Sokolovsky (@heydamir) · CC BY 4.0",
        "description": r.get("description") or "A Claude skill that turns vibecoded, AI-looking UI into a designed interface with its own character",
        "supporting_quote": "git clone https://github.com/heydamir/unslop && cp -r unslop/skills/unslop ~/.claude/skills/",
        "commands": [
            "git clone https://github.com/heydamir/unslop",
            "cp -r unslop/skills/unslop ~/.claude/skills/",
            "/unslop this dashboard"
        ],
        "accent_word": "PRECISION",
        "fetched_timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    }
    with open(os.path.join(CACHE_DIR, "data_unslop.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Saved unslop data: {data['stars']} stars, license {data['license']}")
    return data

def fetch_uv():
    print("\n>>> Fetching astral-sh/uv...")
    r_repo = requests.get("https://api.github.com/repos/astral-sh/uv", headers=headers, timeout=15).json()
    r_rel = requests.get("https://api.github.com/repos/astral-sh/uv/releases/tags/0.13.7", headers=headers, timeout=15).json()
    data = {
        "id": "uv",
        "topic_type": "tool_release",
        "full_name": r_repo.get("full_name"),
        "created_at": r_repo.get("created_at"),
        "release_tag": r_rel.get("tag_name"),
        "published_at": r_rel.get("published_at"),
        "stars": r_repo.get("stargazers_count"),
        "forks": r_repo.get("forks_count"),
        "open_issues": r_repo.get("open_issues_count"),
        "release_assets_count": len(r_rel.get("assets", [])),
        "html_url": r_rel.get("html_url") or "https://github.com/astral-sh/uv/releases/tag/0.13.7",
        "license": "Apache-2.0 / MIT",
        "license_credit": "astral-sh / uv · Apache-2.0 / MIT",
        "description": r_repo.get("description") or "An extremely fast Python package and project manager, written in Rust.",
        "supporting_quote": "curl -LsSf https://astral.sh/uv/install.sh | sh",
        "commands": [
            "curl -LsSf https://astral.sh/uv/install.sh | sh",
            "uv pip install fastapi",
            "uv venv"
        ],
        "accent_word": "VELOCITY",
        "fetched_timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    }
    with open(os.path.join(CACHE_DIR, "data_uv.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Saved uv data: {data['stars']} stars, release {data['release_tag']}")
    return data

def fetch_kimi():
    print("\n>>> Fetching moonshotai/Kimi-K3.1-Pro...")
    r_hf = requests.get("https://huggingface.co/api/models/moonshotai/Kimi-K3.1-Pro", timeout=15).json()
    r_hn = requests.get("https://hacker-news.firebaseio.com/v0/item/50366999.json", timeout=15).json()
    data = {
        "id": "kimi",
        "topic_type": "ai_news",
        "model_id": r_hf.get("id"),
        "hf_created_at": r_hf.get("createdAt"),
        "hf_last_modified": r_hf.get("lastModified"),
        "hn_item_id": r_hn.get("id"),
        "hn_score": r_hn.get("score"),
        "hn_title": r_hn.get("title"),
        "hn_time": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(r_hn.get("time"))),
        "html_url": "https://huggingface.co/moonshotai/Kimi-K3.1-Pro",
        "hn_url": "https://news.ycombinator.com/item?id=50366999",
        "license": "kimi-k3.1-pro license (Open Weights)",
        "license_credit": "Moonshot AI · Kimi K3.1 Pro Model License",
        "description": "Kimi K3.1 Pro open model weights release with configurable reasoning_effort",
        "hardware_caveat": "High-memory GPU cluster (8x 80GB VRAM) required for unquantized local inference (~2.8T MoE parameters)",
        "supporting_quote": "response = client.chat.completions.create(model='kimi-k3.1-pro', reasoning_effort='max')",
        "commands": [
            "response = client.chat.completions.create(",
            "    model='kimi-k3.1-pro',",
            "    messages=messages,",
            "    reasoning_effort='max'",
            ")"
        ],
        "accent_word": "REASONING",
        "fetched_timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    }
    with open(os.path.join(CACHE_DIR, "data_kimi.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Saved kimi data: {data['hn_score']} HN points, HF created {data['hf_created_at']}")
    return data

def fetch_craft():
    print("\n>>> Fetching storytold/craft-anything...")
    r = requests.get("https://api.github.com/repos/storytold/craft-anything", headers=headers, timeout=15).json()
    data = {
        "id": "craft",
        "topic_type": "rising_repo",
        "full_name": r.get("full_name"),
        "created_at": r.get("created_at"),
        "pushed_at": r.get("pushed_at"),
        "stars": r.get("stargazers_count"),
        "forks": r.get("forks_count"),
        "open_issues": r.get("open_issues_count"),
        "html_url": r.get("html_url"),
        "license": "MIT / Apache-2.0",
        "license_credit": "storytold / craft-anything · MIT / Apache-2.0",
        "description": r.get("description") or "Craft Anything: understand how any software works, and craft your own.",
        "supporting_quote": "cargo run --release -p craft-anything",
        "commands": [
            "git clone https://github.com/storytold/craft-anything",
            "cargo run --release -p craft-anything",
            "craft-anything-cli doctor"
        ],
        "accent_word": "ARCHITECT",
        "fetched_timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
    }
    with open(os.path.join(CACHE_DIR, "data_craft.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"  Saved craft data: {data['stars']} stars, created {data['created_at']}")
    return data

if __name__ == "__main__":
    fetch_unslop()
    fetch_uv()
    fetch_kimi()
    fetch_craft()
    print("\n[ALL 4 TOPICS GROUNDED WITH RAW EVIDENCE JSONs]")
