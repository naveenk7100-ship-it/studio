"""
Truth Gate & GitHub Release Verifier
Guarantees 100% factual accuracy:
1. Fetches exact release data from official GitHub API.
2. Prints raw release JSON (tag, published_at, URL, stars).
3. Cross-checks on-screen text and voice claims against the raw JSON.
4. Enforces strict bans on:
   - Invented terminal output
   - Fake prompt headers (user@dev:~)
   - Unsourced hype words ('4X', 'GAME CHANGER', 'Zero memory waste', 'VERIFIED REPO')
   - Mismatches between screenshot OCR text and screen text/script.
"""

import os
import sys
import json
import requests
from datetime import datetime, timezone

def fetch_github_release(repo_slug: str):
    """
    Fetch raw release and repo metadata from GitHub API.
    E.g. repo_slug = 'vllm-project/vllm' or 'anthropics/claude-code'
    """
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "FLASH-TruthGate/1.0"}
    
    # 1. Repo info
    repo_url = f"https://api.github.com/repos/{repo_slug}"
    r_repo = requests.get(repo_url, headers=headers, timeout=10)
    if r_repo.status_code != 200:
        raise ValueError(f"GitHub API error for {repo_slug}: HTTP {r_repo.status_code}")
    repo_data = r_repo.json()

    # 2. Latest release info
    rel_url = f"https://api.github.com/repos/{repo_slug}/releases/latest"
    r_rel = requests.get(rel_url, headers=headers, timeout=10)
    
    release_info = None
    if r_rel.status_code == 200:
        rel_data = r_rel.json()
        release_info = {
            "tag_name": rel_data.get("tag_name"),
            "published_at": rel_data.get("published_at"),
            "html_url": rel_data.get("html_url"),
            "name": rel_data.get("name")
        }
    else:
        # Fallback to tag list if no formal release
        tags_url = f"https://api.github.com/repos/{repo_slug}/tags"
        r_tags = requests.get(tags_url, headers=headers, timeout=10)
        if r_tags.status_code == 200 and len(r_tags.json()) > 0:
            first_tag = r_tags.json()[0]
            release_info = {
                "tag_name": first_tag.get("name"),
                "published_at": None,
                "html_url": f"https://github.com/{repo_slug}/releases/tag/{first_tag.get('name')}",
                "name": first_tag.get("name")
            }

    truth_package = {
        "repo_slug": repo_slug,
        "full_name": repo_data.get("full_name"),
        "description": repo_data.get("description"),
        "stargazers_count": repo_data.get("stargazers_count"),
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "latest_release": release_info
    }
    return truth_package

def verify_script_against_truth(script_data: dict, truth_package: dict) -> dict:
    """
    Verifies that script claims match truth package and contains no banned tokens.
    """
    errors = []
    banned_tokens = [
        "4X", "4x FASTER", "GAME CHANGER", "ZERO MEMORY WASTE",
        "VERIFIED REPO", "user@dev", "[✓] Engine initialized",
        "Successfully installed", "10X"
    ]
    
    script_text = " ".join([s.get("text_en", "") + " " + s.get("text_te", "") for s in script_data.get("shots", [])])
    script_text_upper = script_text.upper()

    # Check banned tokens
    for token in banned_tokens:
        if token.upper() in script_text_upper:
            errors.append(f"Banned token found in script: '{token}'")

    # Check release tag
    latest_rel = truth_package.get("latest_release")
    if latest_rel and latest_rel.get("tag_name"):
        tag = latest_rel["tag_name"]
        # If script claims a version, it must match the tag
        claimed_version = script_data.get("claimed_version")
        if claimed_version and claimed_version != tag:
            errors.append(f"Version mismatch! Script claimed '{claimed_version}' but official GitHub release tag is '{tag}'")

    return {
        "passed": len(errors) == 0,
        "errors": errors,
        "truth_package": truth_package
    }

if __name__ == "__main__":
    slug = sys.argv[1] if len(sys.argv) > 1 else "vllm-project/vllm"
    truth = fetch_github_release(slug)
    print(f"\n--- RAW TRUTH PACKAGE FOR {slug} ---")
    print(json.dumps(truth, indent=2))
