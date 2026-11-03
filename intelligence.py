"""
FLASH Content OS - Daily Intelligence Engine
Scans fresh sources every 6 hours:
- GitHub releases & rising repos
- Hacker News Firebase REST API
- Official AI blog RSS/Atom feeds (Anthropic, OpenAI, Google AI, Meta AI, Mistral, Hugging Face)
Scores candidates for impact, novelty, authority, velocity, and Indian developer relevance.
Deduplicates against history and returns the top 8 candidates for daily briefing.
"""

import os
import sys
import json
import re
import datetime as dt
import xml.etree.ElementTree as ET
import requests
from dotenv import load_dotenv

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
load_dotenv(os.path.join(ROOT, ".env"))

HISTORY_PATH = os.path.join(ROOT, "history.json")
CACHE_DIR = os.path.join(ROOT, "cache")
INTELLIGENCE_CACHE = os.path.join(CACHE_DIR, "intelligence_candidates.json")

GITHUB_TOPICS = [
    "claude-code",
    "mcp",
    "ai-agents",
    "agentic-ai",
    "llm",
    "developer-tools",
    "local-ai",
    "vllm"
]

TIER1_REPOS = [
    "vllm-project/vllm",
    "anthropics/anthropic-sdk-python",
    "modelcontextprotocol/servers",
    "ollama/ollama",
    "huggingface/transformers",
    "meta-llama/llama-models",
    "microsoft/autogen",
    "crewAIInc/crewAI"
]

RSS_FEEDS = [
    {
        "name": "Google AI Blog",
        "url": "https://blog.google/technology/ai/rss/",
        "authority": 20,
        "category": "Official AI Research"
    },
    {
        "name": "OpenAI News",
        "url": "https://openai.com/news/rss.xml",
        "authority": 20,
        "category": "Official AI Research"
    },
    {
        "name": "Hugging Face Blog",
        "url": "https://huggingface.co/blog/feed.xml",
        "authority": 18,
        "category": "Open Source Models"
    },
    {
        "name": "Anthropic SDK Releases",
        "url": "https://github.com/anthropics/anthropic-sdk-python/releases.atom",
        "authority": 20,
        "category": "Official Dev Tools"
    },
    {
        "name": "vLLM Releases",
        "url": "https://github.com/vllm-project/vllm/releases.atom",
        "authority": 19,
        "category": "High-Performance Serving"
    },
    {
        "name": "MCP Servers Releases",
        "url": "https://github.com/modelcontextprotocol/servers/releases.atom",
        "authority": 19,
        "category": "Agent Protocols"
    }
]

def load_history():
    if os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {item.get("key", "").lower() for item in data}
        except Exception:
            return set()
    return set()

def is_builder_relevant(title: str, desc: str) -> bool:
    """Filter out non-builder news (e.g. corporate financial news, politics, executive hires, stock moves)."""
    text = (title + " " + desc).lower()
    # Reject non-builder noise
    noise_keywords = [
        "lawsuit", "sues", "antitrust", "shares tumble", "stock rises", "revenue surges",
        "layoffs", "ceo steps down", "board member", "valuation hits", "ipo filing",
        "quarterly earnings", "lobbying", "regulatory fine"
    ]
    if any(k in text for k in noise_keywords):
        return False
    # Must have builder or developer utility
    builder_keywords = [
        "model", "weights", "benchmark", "inference", "agent", "tool", "sdk", "api",
        "code", "repo", "library", "framework", "dataset", "gpu", "token", "cli",
        "open source", "prompt", "pipeline", "serving", "fine-tuning", "vllm", "claude"
    ]
    return any(k in text for k in builder_keywords)

def calculate_score(candidate: dict) -> int:
    """
    Score 0-100:
    - Impact (0-25): Practical utility for developers
    - Novelty (0-20): Breakthrough or major version release
    - Authority (0-20): Official company / tier-1 repo
    - Velocity (0-20): Stars / HN points
    - Indian Developer Relevance (0-15): Local LLMs, budget AI, CLI speed, practical workflows
    - Freshness Multiplier: <24h = 1.0, 1-3d = 0.85, >7d = 0.5
    """
    impact = candidate.get("impact", 15)
    novelty = candidate.get("novelty", 14)
    authority = candidate.get("authority", 15)
    
    # Velocity
    velocity_val = candidate.get("velocity_raw", 0)
    if velocity_val > 50000 or candidate.get("hn_score", 0) > 300:
        velocity = 20
    elif velocity_val > 10000 or candidate.get("hn_score", 0) > 150:
        velocity = 17
    elif velocity_val > 1000 or candidate.get("hn_score", 0) > 50:
        velocity = 14
    else:
        velocity = 10

    # Indian Builder Relevance: local LLM hosting, free tools, zero cost, Ollama, vLLM, Claude Code
    title_and_desc = (candidate.get("title", "") + " " + candidate.get("desc", "")).lower()
    in_relevance = 10
    if any(k in title_and_desc for k in ["local", "gpu", "cost", "speed", "cli", "serve", "quantiz", "agent", "mcp", "pagedattention"]):
        in_relevance = 15
    elif any(k in title_and_desc for k in ["open source", "api", "free", "python", "typescript"]):
        in_relevance = 13

    base_score = impact + novelty + authority + velocity + in_relevance
    
    # Freshness multiplier
    age_days = candidate.get("age_days", 1)
    if age_days <= 1:
        freshness_mult = 1.0
    elif age_days <= 3:
        freshness_mult = 0.85
    elif age_days <= 7:
        freshness_mult = 0.70
    else:
        freshness_mult = 0.45

    final_score = int(min(100, max(10, base_score * freshness_mult)))
    
    # Attach comprehensive score breakdown
    candidate["score_breakdown"] = {
        "impact": impact,
        "novelty": novelty,
        "authority": authority,
        "velocity": velocity,
        "indian_builder_relevance": in_relevance,
        "freshness_multiplier": freshness_mult,
        "final_score": final_score
    }
    return final_score

def scan_github_repos(history_set):
    candidates = []
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    since = (dt.date.today() - dt.timedelta(days=45)).isoformat()
    seen = set()

    for tp in GITHUB_TOPICS[:5]:
        q = f"topic:{tp} created:>{since} stars:>100"
        try:
            r = requests.get(
                "https://api.github.com/search/repositories",
                params={"q": q, "sort": "stars", "order": "desc", "per_page": 6},
                headers=headers,
                timeout=15
            )
            if r.status_code != 200:
                continue

            for it in r.json().get("items", []):
                name = it["full_name"]
                if name.lower() in history_set or name in seen:
                    continue
                seen.add(name)

                stars = it.get("stargazers_count", 0)
                desc = it.get("description") or "Trending AI open-source repository"
                p_date = it.get("updated_at", it.get("created_at", ""))[:10]
                
                # Compute age
                try:
                    p_dt = dt.datetime.strptime(p_date, "%Y-%m-%d").date()
                    age_days = (dt.date.today() - p_dt).days
                except Exception:
                    age_days = 2

                candidates.append({
                    "id": f"gh_{name.replace('/', '_')}",
                    "title": name,
                    "desc": desc,
                    "source_url": it.get("html_url", ""),
                    "source_type": "GitHub Rising Repo",
                    "authority": 16 if stars > 5000 else 14,
                    "velocity_raw": stars,
                    "age_days": age_days,
                    "published_date": p_date,
                    "impact": 22 if "agent" in tp or "mcp" in tp or "vllm" in tp else 18,
                    "novelty": 17,
                    "why_it_matters": f"Trending developer tool with {stars:,} stars addressing {tp} workflows."
                })
        except Exception as e:
            print(f"[INTELLIGENCE] GitHub search notice for topic {tp}: {e}")

    return candidates

def scan_hacker_news(history_set):
    candidates = []
    try:
        r = requests.get("https://hacker-news.firebaseio.com/v0/beststories.json", timeout=10)
        if r.status_code == 200:
            top_ids = r.json()[:30]
            ai_keywords = ["ai", "llm", "claude", "gpt", "model", "agent", "gpu", "inference", "deepseek", "vllm", "anthropic", "openai", "token"]
            
            for item_id in top_ids:
                item_r = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json", timeout=5)
                if item_r.status_code != 200:
                    continue
                item = item_r.json() or {}
                title = item.get("title", "")
                url = item.get("url", f"https://news.ycombinator.com/item?id={item_id}")
                score = item.get("score", 0)
                
                # Check keyword match
                title_lower = title.lower()
                if any(re.search(rf"\b{k}\b", title_lower) for k in ai_keywords):
                    if title.lower() in history_set:
                        continue
                    candidates.append({
                        "id": f"hn_{item_id}",
                        "title": title,
                        "desc": f"Hacker News top discussion ({score} points, {len(item.get('kids', []))} comments).",
                        "source_url": url,
                        "source_type": "Hacker News Top AI",
                        "authority": 16,
                        "velocity_raw": score * 50,
                        "hn_score": score,
                        "age_days": 1,
                        "published_date": dt.date.today().isoformat(),
                        "impact": 20,
                        "novelty": 18,
                        "why_it_matters": f"Viral discussion on Hacker News with {score} points reflecting builder interest."
                    })
    except Exception as e:
        print(f"[INTELLIGENCE] Hacker News scan notice: {e}")

    return candidates

def scan_rss_feeds(history_set):
    candidates = []
    headers = {"User-Agent": "FLASH-Intelligence-Bot/2.0 (Mozilla/5.0)"}

    for feed in RSS_FEEDS:
        try:
            r = requests.get(feed["url"], headers=headers, timeout=12)
            if r.status_code != 200:
                continue

            root = ET.fromstring(r.content)
            # Support both RSS and Atom
            is_atom = "feed" in root.tag or root.tag.endswith("feed")
            
            items = []
            if is_atom:
                # Namespace handling
                ns = {"atom": "http://www.w3.org/2005/Atom"}
                entries = root.findall("atom:entry", ns) or root.findall("{http://www.w3.org/2005/Atom}entry") or root.findall("entry")
                for entry in entries[:4]:
                    title_elem = entry.find("atom:title", ns) or entry.find("{http://www.w3.org/2005/Atom}title") or entry.find("title")
                    link_elem = entry.find("atom:link", ns) or entry.find("{http://www.w3.org/2005/Atom}link") or entry.find("link")
                    updated_elem = entry.find("atom:updated", ns) or entry.find("{http://www.w3.org/2005/Atom}updated") or entry.find("updated")
                    
                    title = title_elem.text.strip() if title_elem is not None and title_elem.text else ""
                    href = link_elem.attrib.get("href", "") if link_elem is not None else ""
                    pub_date = (updated_elem.text if updated_elem is not None and updated_elem.text else "")[:10]
                    items.append((title, href, pub_date))
            else:
                # RSS 2.0
                channel = root.find("channel")
                if channel is not None:
                    for it in channel.findall("item")[:4]:
                        title = it.findtext("title") or ""
                        link = it.findtext("link") or ""
                        pub_date = it.findtext("pubDate") or dt.date.today().isoformat()
                        items.append((title, link, pub_date[:16]))

            for title, url, p_date in items:
                if not title or title.lower() in history_set:
                    continue
                
                candidates.append({
                    "id": f"rss_{abs(hash(url)) % 100000}",
                    "title": title,
                    "desc": f"Official release/announcement from {feed['name']}.",
                    "source_url": url,
                    "source_type": feed["name"],
                    "authority": feed["authority"],
                    "velocity_raw": 10000,
                    "age_days": 1,
                    "published_date": p_date or dt.date.today().isoformat(),
                    "impact": 24,
                    "novelty": 20,
                    "why_it_matters": f"Official announcement from {feed['name']} impacting AI workflows."
                })
        except Exception as e:
            print(f"[INTELLIGENCE] RSS feed scan notice for {feed['name']}: {e}")

    return candidates

def collect_and_rank_intelligence() -> list:
    print("\n--- Running FLASH Daily Intelligence Scanner ---")
    history_set = load_history()
    
    all_candidates = []
    
    # 1. RSS Feeds
    rss_items = scan_rss_feeds(history_set)
    print(f"Scanned RSS items: {len(rss_items)}")
    all_candidates.extend(rss_items)
    
    # 2. Hacker News
    hn_items = scan_hacker_news(history_set)
    print(f"Scanned Hacker News AI items: {len(hn_items)}")
    all_candidates.extend(hn_items)
    
    # 3. GitHub Trending Repos
    gh_items = scan_github_repos(history_set)
    print(f"Scanned GitHub items: {len(gh_items)}")
    all_candidates.extend(gh_items)
    
    # Score each candidate
    for cand in all_candidates:
        cand["score"] = calculate_score(cand)
    
    # Deduplicate by URL or title
    deduped = []
    seen_urls = set()
    seen_titles = set()
    
    for cand in sorted(all_candidates, key=lambda x: -x["score"]):
        url = cand["source_url"].lower().rstrip("/")
        title = cand["title"].lower().strip()
        if url in seen_urls or title in seen_titles:
            continue
        seen_urls.add(url)
        seen_titles.add(title)
        deduped.append(cand)
    
    top_8 = deduped[:8]
    print(f"Top 8 intelligence candidates ranked successfully.")
    
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(INTELLIGENCE_CACHE, "w", encoding="utf-8") as f:
        json.dump(top_8, f, indent=2)
        
    return top_8

if __name__ == "__main__":
    top = collect_and_rank_intelligence()
    for i, t in enumerate(top, 1):
        print(f"\n#{i} [{t['score']}/100] {t['title']} ({t['source_type']})")
        print(f"   URL: {t['source_url']}")
        print(f"   Why it matters: {t['why_it_matters']}")
