import requests
import json
from datetime import datetime, timezone

headers = {"User-Agent": "FLASH-Discovery-Bot"}

print("================ 1. RISING REPOS (Created > 2026-10-06) ================")
try:
    r1 = requests.get("https://api.github.com/search/repositories?q=created:>2026-10-06+stars:>500&sort=stars&order=desc", headers=headers, timeout=15)
    repos = r1.json().get("items", [])[:15]
    for rp in repos:
        print(f"Repo: {rp['full_name']} | Stars: {rp['stargazers_count']} | Created: {rp['created_at']} | URL: {rp['html_url']}")
except Exception as e:
    print(f"Error searching repos: {e}")

print("\n================ 2. FRESH TOOL / FRAMEWORK RELEASES (< 14 days) ================")
check_repos = [
    "astral-sh/uv",
    "microsoft/markitdown",
    "agno-agi/agno",
    "huggingface/transformers",
    "vllm-project/vllm", # blocked
    "fastapi/fastapi",
    "pydantic/pydantic",
    "meta-llama/llama-models",
    "karpathy/nanoGPT",
    "anthropics/anthropic-sdk-python",
    "simonw/datasette",
]
for cr in check_repos:
    try:
        r2 = requests.get(f"https://api.github.com/repos/{cr}/releases/latest", headers=headers, timeout=10)
        if r2.status_code == 200:
            rel = r2.json()
            pub_date = rel.get("published_at")
            tag = rel.get("tag_name")
            print(f"Repo: {cr} | Release: {tag} | Published: {pub_date} | URL: {rel.get('html_url')}")
    except Exception as e:
        pass

print("\n================ 3. HACKER NEWS TOP TECH & AI STORIES (< 48 hrs) ================")
try:
    r3 = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
    top_ids = r3.json()[:30]
    for sid in top_ids[:20]:
        item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=5).json()
        if not item:
            continue
        title = item.get("title", "")
        url = item.get("url", "")
        score = item.get("score", 0)
        time_sec = item.get("time", 0)
        dt = datetime.fromtimestamp(time_sec, tz=timezone.utc).isoformat()
        print(f"HN Item: {sid} | Score: {score} | Date: {dt} | Title: {title} | URL: {url}")
except Exception as e:
    print(f"Error querying HN: {e}")
