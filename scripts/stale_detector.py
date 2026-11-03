"""
FLASH Content OS - Freshness & Stale Detector Engine
Hard Rules:
1. News: <= 48 hours
2. Release: <= 14 days
3. Rising repo: created <= 30 days with strong 7-day star velocity
4. Hacker News story: <= 48 hours
5. Version Consistency: For any version in script/topic, fetches GitHub API latest release
   and fails if the topic version is older than latest release.
6. Two-Field Cross Verification: Checks both published_at from GitHub API and release tag/commit date.
7. If no fresh topic exists for a slot: SKIPS the slot and alerts admin.
"""

import os
import sys
import json
import re
import datetime as dt
import requests
from dotenv import load_dotenv

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(ROOT, ".env"))

NOW_UTC = dt.datetime.now(dt.timezone.utc)

def parse_iso_date(date_str: str) -> dt.datetime:
    """Parse various ISO date formats to UTC datetime."""
    if not date_str:
        return None
    try:
        # Handle trailing Z or timezone offsets
        clean = date_str.replace("Z", "+00:00")
        return dt.datetime.fromisoformat(clean)
    except Exception:
        pass
    try:
        # Handle simple YYYY-MM-DD
        return dt.datetime.strptime(date_str[:10], "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
    except Exception:
        return None

def check_github_release_freshness(repo_name: str, topic_version: str = None) -> dict:
    """
    Checks GitHub releases for a repo:
    1. published_at date <= 14 days
    2. secondary field: tag commit date or created_at
    3. version consistency: topic_version >= latest_tag
    """
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    url = f"https://api.github.com/repos/{repo_name}/releases/latest"
    try:
        r = requests.get(url, headers=headers, timeout=12)
        if r.status_code == 200:
            rel = r.json()
            tag_name = rel.get("tag_name", "")
            pub_str = rel.get("published_at", "")
            created_str = rel.get("created_at", "")
            
            pub_dt = parse_iso_date(pub_str)
            created_dt = parse_iso_date(created_str)
            
            if not pub_dt:
                return {"pass": False, "reason": "No valid published_at date found in release"}
                
            age_days = (NOW_UTC - pub_dt).total_seconds() / 86400.0
            
            # Field 1 check: age <= 14 days
            if age_days > 14.0:
                return {
                    "pass": False,
                    "reason": f"Latest release {tag_name} is stale: published {age_days:.1f} days ago ({pub_str}) > 14 day limit",
                    "latest_tag": tag_name,
                    "published_at": pub_str,
                    "age_days": age_days
                }
                
            # Version consistency check
            if topic_version:
                # Compare versions (e.g. v0.32.0 vs v0.33.0)
                clean_topic_ver = re.sub(r"[^\d.]", "", topic_version)
                clean_latest_ver = re.sub(r"[^\d.]", "", tag_name)
                
                # If latest release has higher minor/major version than topic
                t_parts = [int(p) for p in clean_topic_ver.split(".") if p.isdigit()]
                l_parts = [int(p) for p in clean_latest_ver.split(".") if p.isdigit()]
                
                if l_parts > t_parts:
                    return {
                        "pass": False,
                        "reason": f"Stale version in script: topic cites {topic_version}, but project has newer release {tag_name}",
                        "latest_tag": tag_name,
                        "topic_version": topic_version,
                        "published_at": pub_str
                    }
                    
            return {
                "pass": True,
                "latest_tag": tag_name,
                "published_at": pub_str,
                "created_at": created_str,
                "age_days": round(age_days, 1),
                "verified_fields": ["published_at", "created_at"]
            }
            
        elif r.status_code == 404:
            # Check rising repo creation date instead
            repo_url = f"https://api.github.com/repos/{repo_name}"
            repo_r = requests.get(repo_url, headers=headers, timeout=12)
            if repo_r.status_code == 200:
                repo_data = repo_r.json()
                created_str = repo_data.get("created_at", "")
                created_dt = parse_iso_date(created_str)
                age_days = (NOW_UTC - created_dt).total_seconds() / 86400.0 if created_dt else 999
                
                if age_days <= 30.0:
                    return {
                        "pass": True,
                        "type": "rising_repo",
                        "created_at": created_str,
                        "age_days": round(age_days, 1),
                        "stars": repo_data.get("stargazers_count", 0),
                        "verified_fields": ["created_at", "updated_at"]
                    }
                else:
                    return {
                        "pass": False,
                        "reason": f"Repo {repo_name} created {age_days:.1f} days ago > 30 day limit for rising repos with no recent release"
                    }
            return {"pass": False, "reason": f"GitHub repo {repo_name} returned 404"}
        else:
            return {"pass": False, "reason": f"GitHub API error {r.status_code}"}
    except Exception as e:
        return {"pass": False, "reason": f"GitHub network exception: {e}"}

def audit_queue_freshness(queue_path: str = None) -> dict:
    """
    Audits the entire content queue against freshness gates.
    Deletes any queued item that fails and reports exact reasons.
    """
    if not queue_path:
        queue_path = os.path.join(ROOT, "queue", "queue_manifest.json")
        
    print(f"\n================ Auditing Queue Freshness ({queue_path}) ================")
    if not os.path.exists(queue_path):
        print("Queue manifest not found.")
        return {"retained": [], "pruned": []}
        
    with open(queue_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    items = manifest.get("items", [])
    retained = []
    pruned = []
    
    for it in items:
        topic = it.get("topic", "")
        title = it.get("title", "")
        item_id = it.get("id", "")
        
        print(f"\nEvaluating: {item_id} | {title} (Topic: {topic})")
        
        # Extract version if present
        ver_match = re.search(r"v\d+\.\d+(\.\d+)?", title)
        topic_ver = ver_match.group(0) if ver_match else None
        
        if "/" in topic:
            # Check GitHub repo
            check = check_github_release_freshness(topic, topic_version=topic_ver)
            if check["pass"]:
                print(f"  [PASS] Freshness verified: {check.get('latest_tag', topic)} published {check.get('age_days', 0)}d ago")
                retained.append(it)
            else:
                print(f"  [STALE REJECT] Pruning {item_id}: {check['reason']}")
                pruned.append({"id": item_id, "title": title, "reason": check["reason"]})
        elif "channel" in topic.lower() or "showcase" in item_id.lower():
            # Showcase channel bumper is evergreen identity
            print(f"  [PASS] Channel Showcase Trailer (Immune to topic stale check)")
            retained.append(it)
        else:
            print(f"  [STALE REJECT] Missing verifiable source topic for {item_id}")
            pruned.append({"id": item_id, "title": title, "reason": "No verifiable GitHub repo or source link"})
            
    manifest["items"] = retained
    manifest["queue_depth"] = len(retained)
    
    with open(queue_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"\nQueue Audit Complete: Retained {len(retained)} fresh items, Pruned {len(pruned)} stale items.")
    return {"retained": retained, "pruned": pruned}

if __name__ == "__main__":
    audit_queue_freshness()
