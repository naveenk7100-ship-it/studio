"""Curate and ground trending AI and dev-tool GitHub repositories via GitHub REST API."""
import os
import re
import sys
import requests
import datetime as dt

# Set utf-8 encoding for safe output on Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

TOPICS = [
    "claude-code",
    "mcp",
    "ai-agents",
    "agentic-ai",
    "llm",
    "ai-tools",
    "developer-tools",
    "generative-ai"
]

def _headers():
    h = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "AI-Auto-Reels-Studio/2.0"
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def extract_verified_commands(readme_text: str):
    """Extract literal CLI commands that actually exist in the README."""
    commands = []
    # 1. Look inside markdown code blocks
    for block in re.findall(r"```(?:bash|sh|shell|console|zsh)?\s*\n(.*?)\n```", readme_text, re.DOTALL):
        for line in block.splitlines():
            clean = line.strip().lstrip("$# ").strip()
            if any(clean.startswith(c) for c in ["pip ", "npm ", "npx ", "git ", "docker ", "cargo ", "brew ", "uv ", "pnpm ", "yarn "]):
                if clean not in commands and len(clean) < 75:
                    commands.append(clean)

    # 2. Look for standalone shell lines
    for line in readme_text.splitlines()[:150]:
        clean = line.strip().lstrip("$# ").strip()
        if any(clean.startswith(c) for c in ["pip install ", "npm i ", "npx ", "docker run ", "git clone ", "uv pip "]):
            if clean not in commands and len(clean) < 75:
                commands.append(clean)

    return commands[:4]


def get_repo_details(full_name: str) -> dict:
    """Fetch complete verified repository details and README for LLM grounding."""
    h = _headers()
    # 1. Repository metadata
    r = requests.get(f"https://api.github.com/repos/{full_name}", headers=h, timeout=20)
    r.raise_for_status()
    data = r.json()

    # 2. Latest release
    release_tag = "latest"
    try:
        rel = requests.get(f"https://api.github.com/repos/{full_name}/releases/latest", headers=h, timeout=10)
        if rel.status_code == 200:
            release_tag = rel.json().get("tag_name", "latest")
    except Exception:
        pass

    # 3. Raw README text
    readme_text = ""
    try:
        rm_h = h.copy()
        rm_h["Accept"] = "application/vnd.github.raw+json"
        rm_r = requests.get(f"https://api.github.com/repos/{full_name}/readme", headers=rm_h, timeout=20)
        if rm_r.status_code == 200:
            readme_text = rm_r.text
    except Exception as e:
        print(f"[TOPICS] Notice: README fetch error for {full_name}: {e}")

    commands = extract_verified_commands(readme_text)
    license_name = data.get("license", {}).get("name") if data.get("license") else "Open Source"

    # Clean README summary for LLM context (strip HTML tags and markdown images)
    cleaned_readme = re.sub(r"<[^>]+>", "", readme_text)
    cleaned_readme = re.sub(r"!\[.*?\]\(.*?\)", "", cleaned_readme)
    cleaned_readme = re.sub(r"\n{3,}", "\n\n", cleaned_readme)

    return {
        "name": data["full_name"],
        "description": data.get("description") or "",
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "language": data.get("language") or "Python",
        "license": license_name,
        "release": release_tag,
        "url": data["html_url"],
        "topics": data.get("topics", [])[:6],
        "verified_commands": commands,
        "readme_summary": cleaned_readme[:2200]
    }


def candidates():
    """Find fresh, rising AI repositories from GitHub."""
    since = (dt.date.today() - dt.timedelta(days=60)).isoformat()
    seen = set()
    out = []

    for tp in TOPICS:
        q = f"topic:{tp} created:>{since} stars:>60"
        try:
            r = requests.get(
                "https://api.github.com/search/repositories",
                params={"q": q, "sort": "stars", "order": "desc", "per_page": 10},
                headers=_headers(),
                timeout=25
            )
            if r.status_code != 200:
                continue

            for it in r.json().get("items", []):
                name = it["full_name"]
                desc = it.get("description") or ""
                # Skip duplicate, empty descriptions, or non-English/CJK descriptions
                if name in seen or not desc or len(desc) < 15:
                    continue
                if re.search(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", desc):
                    continue

                seen.add(name)
                out.append({
                    "name": name,
                    "desc": desc[:250],
                    "stars": it["stargazers_count"],
                    "lang": it.get("language") or "",
                    "url": it["html_url"],
                    "topics": it.get("topics", [])[:5]
                })
        except Exception as e:
            print(f"[TOPICS] GitHub search notice for topic '{tp}': {e}")

    out.sort(key=lambda x: -x["stars"])
    return out


def pick_repo(history=None, skip=()):
    """Pick the highest quality unposted repo and fetch its grounded details."""
    history = history or []
    used = {h.get("key", "").lower() for h in history}
    skip_set = {s.lower() for s in skip}

    for c in candidates():
        name_lower = c["name"].lower()
        if name_lower not in used and name_lower not in skip_set:
            try:
                print(f"[TOPICS] Grounding candidate repo: {c['name']} ({c['stars']} stars)...")
                detailed = get_repo_details(c["name"])
                return detailed
            except Exception as e:
                print(f"[TOPICS] Could not ground {c['name']}, trying next ({e})")
                continue
    return None
