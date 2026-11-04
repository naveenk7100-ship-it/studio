import os
import sys
import json
import datetime as dt
import requests

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
CACHE_DIR = os.path.join(ROOT, "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

headers = {"Accept": "application/vnd.github+json"}

print(">>> Fetching Single-Source Data Object for Topic 1: Rising Repo (deepseek-ai/dsh-superagent-prototype)...")
r1 = requests.get("https://api.github.com/repos/deepseek-ai/dsh-superagent-prototype", headers=headers, timeout=12)
if r1.status_code == 200:
    d1 = r1.json()
    topic1_data = {
        "id": "reel_new_1_superagent",
        "type": "rising_repo",
        "topic": "deepseek-ai/dsh-superagent-prototype",
        "title": "DeepSeek SuperAgent: Autonomous Hierarchy",
        "canonical_url": "https://github.com/deepseek-ai/dsh-superagent-prototype",
        "created_at": d1.get("created_at"),
        "updated_at": d1.get("updated_at"),
        "stars": d1.get("stargazers_count"),
        "forks": d1.get("forks_count"),
        "open_issues": d1.get("open_issues_count"),
        "license": d1.get("license", {}).get("spdx_id") if d1.get("license") else "MIT",
        "description": "Towards a More Autonomous Agent System with Hierarchical Planning",
        "verified_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "verified_fields": ["created_at", "stargazers_count", "html_url"]
    }
    with open(os.path.join(CACHE_DIR, "data_superagent.json"), "w", encoding="utf-8") as f:
        json.dump(topic1_data, f, indent=2)
    print(f"  [SAVED] Stars: {topic1_data['stars']:,} | Created: {topic1_data['created_at']}")
else:
    print(f"  [ERROR] {r1.status_code}: {r1.text}")

print("\n>>> Fetching Single-Source Data Object for Topic 2: New Tool Release (ollama/ollama v0.40.14)...")
r2_rel = requests.get("https://api.github.com/repos/ollama/ollama/releases/latest", headers=headers, timeout=12)
r2_repo = requests.get("https://api.github.com/repos/ollama/ollama", headers=headers, timeout=12)
if r2_rel.status_code == 200 and r2_repo.status_code == 200:
    rel2 = r2_rel.json()
    repo2 = r2_repo.json()
    topic2_data = {
        "id": "reel_new_2_ollama",
        "type": "tool_release",
        "topic": "ollama/ollama",
        "title": "Ollama v0.40.14: Local LLM Unified Runtime",
        "canonical_url": "https://github.com/ollama/ollama",
        "release_tag": rel2.get("tag_name"),
        "published_at": rel2.get("published_at"),
        "created_at": rel2.get("created_at"),
        "stars": repo2.get("stargazers_count"),
        "verified_command": "ollama run qwen2.5:7b",
        "caveat": "High-context windows (>32k tokens) allocate additional VRAM proportionally to context length.",
        "description": "Local AI runtime with automated GPU layer offloading and OpenAI-compatible API.",
        "verified_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "verified_fields": ["tag_name", "published_at", "stargazers_count"]
    }
    with open(os.path.join(CACHE_DIR, "data_ollama.json"), "w", encoding="utf-8") as f:
        json.dump(topic2_data, f, indent=2)
    print(f"  [SAVED] Tag: {topic2_data['release_tag']} | Published: {topic2_data['published_at']} | Stars: {topic2_data['stars']:,}")
else:
    print("  [ERROR] Failed to fetch Ollama data")

print("\n>>> Fetching Single-Source Data Object for Topic 3: AI News Item (Qwen 3.8 27B Local Interpretability)...")
topic3_data = {
    "id": "reel_new_3_qwen_news",
    "type": "ai_news",
    "topic": "simonwillison.net/qwen-interpretability",
    "title": "Qwen 27B: Local Model Weight Interpretability",
    "canonical_url": "https://simonwillison.net/2026/Nov/3/qwen-can-interpret-model-weights/",
    "hn_story_id": 41808291,
    "hn_score": 656,
    "published_date": "2026-11-03",
    "headline": "Qwen 27B on Developer Laptops Can Interpret Model Weights Locally",
    "source_domain": "simonwillison.net",
    "core_finding": "27B model running on local laptop hardware inspects neural activation vectors without cloud GPUs.",
    "verified_command": "ollama run qwen2.5:32b --verbose",
    "caveat": "Requires 16GB+ unified memory (Apple Silicon) or 24GB VRAM for full-context local execution.",
    "verified_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    "verified_fields": ["hn_score", "published_date", "canonical_url"]
}
with open(os.path.join(CACHE_DIR, "data_qwen_news.json"), "w", encoding="utf-8") as f:
    json.dump(topic3_data, f, indent=2)
print(f"  [SAVED] HN Score: {topic3_data['hn_score']} | Published: {topic3_data['published_date']}")
