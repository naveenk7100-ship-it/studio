import requests
import json
from datetime import datetime, timezone

headers = {"User-Agent": "FLASH-Verification-Agent"}

def verify_repo(full_name):
    print(f"\n--- Checking Repo: {full_name} ---")
    url = f"https://api.github.com/repos/{full_name}"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"Failed to fetch {full_name}: {r.status_code}")
        return None
    data = r.json()
    
    # check contributors
    r_contrib = requests.get(f"{url}/contributors?per_page=10", headers=headers)
    num_contribs = len(r_contrib.json()) if r_contrib.status_code == 200 else 0
    
    # check latest release
    r_rel = requests.get(f"{url}/releases/latest", headers=headers)
    rel_data = r_rel.json() if r_rel.status_code == 200 else {}
    
    info = {
        "full_name": data.get("full_name"),
        "description": data.get("description"),
        "created_at": data.get("created_at"),
        "updated_at": data.get("updated_at"),
        "stargazers_count": data.get("stargazers_count"),
        "forks_count": data.get("forks_count"),
        "open_issues_count": data.get("open_issues_count"),
        "contributors_count_sample": num_contribs,
        "html_url": data.get("html_url"),
        "latest_release_tag": rel_data.get("tag_name"),
        "latest_release_date": rel_data.get("published_at"),
    }
    print(json.dumps(info, indent=2))
    return info

def verify_hn(item_id):
    print(f"\n--- Checking HN Item: {item_id} ---")
    r = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json")
    if r.status_code != 200:
        return None
    data = r.json()
    info = {
        "id": data.get("id"),
        "title": data.get("title"),
        "score": data.get("score"),
        "by": data.get("by"),
        "time": data.get("time"),
        "iso_date": datetime.fromtimestamp(data.get("time", 0), tz=timezone.utc).isoformat(),
        "url": data.get("url"),
    }
    print(json.dumps(info, indent=2))
    return info

if __name__ == "__main__":
    # Test Rising Repos
    verify_repo("astral-sh/uv")
    verify_repo("anthropics/anthropic-sdk-python")
    verify_repo("heydamir/unslop")
    verify_repo("seedds/nxnative")
    
    # Test HN Stories
    verify_hn(50366999) # Kimi K3.1 Pro
    verify_hn(50369106) # Go JSON v2
    verify_hn(50368626) # Anthropic Provable Inference
