import urllib.request
import json

headers = {'User-Agent': 'Mozilla/5.0'}

def inspect_repo(repo):
    print(f"\n================ INSPECTING {repo} ================")
    # 1. Repo info
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}", headers=headers)
    with urllib.request.urlopen(req) as resp:
        d = json.loads(resp.read().decode('utf-8'))
        print(f"Stars: {d['stargazers_count']}")
        print(f"Created: {d['created_at']}")
        print(f"License: {d.get('license', {}).get('spdx_id') if d.get('license') else 'None'}")
        print(f"Description: {d.get('description')}")
    
    # 2. Latest release
    try:
        req = urllib.request.Request(f"https://api.github.com/repos/{repo}/releases/latest", headers=headers)
        with urllib.request.urlopen(req) as resp:
            rel = json.loads(resp.read().decode('utf-8'))
            print(f"Latest Release: {rel.get('tag_name')} published at {rel.get('published_at')}")
    except Exception as e:
        print(f"No release endpoint or error: {e}")

    # 3. Readme snippet
    try:
        req = urllib.request.Request(f"https://api.github.com/repos/{repo}/readme", headers=headers)
        with urllib.request.urlopen(req) as resp:
            rd = json.loads(resp.read().decode('utf-8'))
            import base64
            content = base64.b64decode(rd['content']).decode('utf-8', errors='ignore')
            print("README Snippet (first 400 chars):")
            print(content[:400])
    except Exception as e:
        print(f"Error fetching readme: {e}")

if __name__ == "__main__":
    inspect_repo("wheresryan22/anatomy")
    inspect_repo("browser-use/browser-use")
    inspect_repo("astral-sh/ruff")
