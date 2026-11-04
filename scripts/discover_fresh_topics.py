import requests
import json
import datetime as dt

now = dt.datetime.now(dt.timezone.utc)
headers = {"Accept": "application/vnd.github+json"}

print("=== 1. Live GitHub Rising Repos (created <= 30 days) ===")
since_30d = (now - dt.timedelta(days=30)).strftime("%Y-%m-%d")
q = f"created:>{since_30d} stars:>500"
r = requests.get(
    "https://api.github.com/search/repositories",
    params={"q": q, "sort": "stars", "order": "desc", "per_page": 10},
    headers=headers,
    timeout=15,
)
if r.status_code == 200:
    for item in r.json().get("items", [])[:8]:
        name = item["full_name"]
        stars = item["stargazers_count"]
        created = item["created_at"]
        desc = item.get("description", "") or ""
        print(f"Repo: {name} | Stars: {stars} | Created: {created} | Desc: {desc[:70]}")
else:
    print(f"Error {r.status_code}: {r.text[:100]}")

print("\n=== 2. Live GitHub Releases (Tier-1 repos <= 14 days) ===")
tier1 = [
    "ollama/ollama",
    "astral-sh/uv",
    "meta-llama/llama-models",
    "huggingface/transformers",
    "fastapi/fastapi",
    "ggerganov/llama.cpp",
    "karpathy/nanoGPT",
    "browser-use/browser-use",
]
for repo in tier1:
    rel_r = requests.get(
        f"https://api.github.com/repos/{repo}/releases/latest",
        headers=headers,
        timeout=10,
    )
    if rel_r.status_code == 200:
        rel = rel_r.json()
        pub = rel.get("published_at", "")
        tag = rel.get("tag_name", "")
        if pub:
            pub_dt = dt.datetime.fromisoformat(pub.replace("Z", "+00:00"))
            age = (now - pub_dt).total_seconds() / 86400
            print(f"Repo: {repo} | Tag: {tag} | Published: {pub} ({age:.1f}d ago)")

print("\n=== 3. Hacker News Top AI Stories (<= 48h) ===")
hn_r = requests.get(
    "https://hacker-news.firebaseio.com/v0/beststories.json", timeout=10
)
if hn_r.status_code == 200:
    for sid in hn_r.json()[:30]:
        item = (
            requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{sid}.json",
                timeout=5,
            ).json()
            or {}
        )
        title = item.get("title", "")
        score = item.get("score", 0)
        time_sec = item.get("time", 0)
        age_h = (now.timestamp() - time_sec) / 3600
        if age_h <= 48 and any(
            k in title.lower()
            for k in [
                "ai",
                "llm",
                "open",
                "gpu",
                "agent",
                "model",
                "code",
                "python",
                "rust",
                "database",
            ]
        ):
            print(
                f"HN: {title} | Score: {score} | Age: {age_h:.1f}h | URL: {item.get('url', '')}"
            )
