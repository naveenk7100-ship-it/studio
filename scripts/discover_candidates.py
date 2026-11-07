import urllib.request
import json
import datetime as dt

headers = {'User-Agent': 'Mozilla/5.0'}

# 1. Search recently created repositories with high star velocity (> 1000 stars, created in last 30 days)
since_date = (dt.date.today() - dt.timedelta(days=30)).isoformat()
url1 = f"https://api.github.com/search/repositories?q=created:>{since_date}+stars:>1000&sort=stars&order=desc"

print(f"--- QUERYING RISING REPOSITORIES (Created > {since_date}) ---")
try:
    req = urllib.request.Request(url1, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        for item in data.get('items', [])[:10]:
            print(f"Repo: {item['full_name']}")
            print(f"  Stars: {item['stargazers_count']}")
            print(f"  License: {item.get('license', {}).get('spdx_id') if item.get('license') else 'None'}")
            print(f"  Created: {item['created_at']}")
            print(f"  Desc: {item.get('description', '')[:100]}")
            print(f"  URL: {item['html_url']}\n")
except Exception as e:
    print(f"Error querying rising repos: {e}")

# 2. Query top trending / recent releases (last 14 days)
release_since = (dt.date.today() - dt.timedelta(days=14)).isoformat()
print(f"\n--- QUERYING RECENT RELEASES (Published > {release_since}) ---")
target_repos = [
    "browser-use/browser-use",
    "cocktailpeanut/dal",
    "fastapi/fastapi",
    "astral-sh/ruff",
    "meta-llama/llama-stack",
    "anthropics/anthropic-sdk-python",
    "simonw/llm",
    "exo-explore/exo",
    "agno-agi/agno",
    "All-Hands-AI/OpenHands",
    "Comfy-Org/ComfyUI_frontend"
]

for repo in target_repos:
    try:
        url_rel = f"https://api.github.com/repos/{repo}/releases/latest"
        req = urllib.request.Request(url_rel, headers=headers)
        with urllib.request.urlopen(req) as resp:
            rel = json.loads(resp.read().decode('utf-8'))
            print(f"Repo: {repo}")
            print(f"  Tag: {rel.get('tag_name')}")
            print(f"  Published: {rel.get('published_at')}")
            print(f"  Name: {rel.get('name')}\n")
    except Exception as e:
        # Check repo info if no release
        try:
            url_repo = f"https://api.github.com/repos/{repo}"
            req = urllib.request.Request(url_repo, headers=headers)
            with urllib.request.urlopen(req) as resp:
                rinfo = json.loads(resp.read().decode('utf-8'))
                print(f"Repo: {repo} (No releases endpoint)")
                print(f"  Stars: {rinfo.get('stargazers_count')}")
                print(f"  Updated: {rinfo.get('updated_at')}")
                print(f"  License: {rinfo.get('license', {}).get('spdx_id') if rinfo.get('license') else 'None'}\n")
        except:
            pass
