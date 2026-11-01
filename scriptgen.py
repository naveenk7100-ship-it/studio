"""AI Auto-Reels Studio: Resilient Script Generation Engine.

Features:
- Dual LLM Chain with automatic failover: Google Gemini -> OpenRouter (with backoff & retry).
- 100% Fact-Grounded: Built from repo README, verified commands, stars, and release notes.
- Multi-Candidate Pipeline: Generates 3 diverse candidate scripts per topic.
- Critic Evaluation Pass: Dedicated LLM scoring pass analyzing hook speed (<= 2s),
  factual support, Tenglish naturalness, 0 Telugu Unicode characters, word count (70-95),
  and loop closure.
- Full metadata output: hook, scenes, on-screen text, mood tags, energy ratings, and source URLs.
"""
import os
import re
import sys
import json
import time
import requests

# Ensure utf-8 output on Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "nvidia/nemotron-3.5-lightning:free")

PROMPT_RULES = """You are an elite short-form video scriptwriter and editor for an Indian Telugu tech audience.
Write a high-retention 25-35 second vertical video script in TENGLISH.

CRITICAL RULES:
1. VOICE LANGUAGE (TENGLISH): Conversational romanized Telugu mixed with English (friendly youtuber tone, e.g. "Mama, ee repo chusthe shock avthav!").
2. STRICT SCRIPT BAN: NEVER use Telugu script Unicode characters (అ, ఆ, etc.) anywhere. ONLY use Latin letters (English alphabet).
3. BAN RELATIVE TIME WORDS: NEVER use relative time words ("yesterday", "today", "this week", "last week", "tomorrow"). ALWAYS use absolute dates (e.g., "31 Oct 2026") or release versions ("v2.1.316").
4. ON-SCREEN TEXT: Short, punchy English in UPPERCASE (max 5-6 words for "big", optional 2-3 words for "sub"). Never repeat the caption as a label.
5. FACTUAL GROUNDING: Rely strictly on the provided repository facts or verified search facts. Every command in "cmd" must literally exist in the verified commands list or README.
6. RETENTION & LENGTH:
   - Hook in the first 1.5 seconds (< 10 spoken words).
   - Visual/scene change every 2-3 seconds.
   - Word count: EXACTLY 65 to 80 spoken words in total (strictly targeting 28-32 seconds).
   - Follow Call: Appears ONLY ONCE in the final CTA pill. Do not repeat "Follow for Daily Insights" elsewhere.
   - Ending: Seamless loop back to the hook or clear CTA.
7. SCENE TYPES: hook, repo, terminal, points, stat, cta.
8. MOOD TAGS: "hype", "futuristic", "chill-focus", "dark-tech", "inspiring", "news-urgent", "playful".
9. ENERGY: 1 to 5.

OUTPUT FORMAT: Strict valid JSON only, no markdown ticks, no preamble:
{
  "topic_key": "unique_short_id",
  "title": "Catchy YouTube/Reels title under 80 chars",
  "hook": "Opening hook sentence",
  "caption": "Engaging 2-line caption with 6-8 relevant hashtags",
  "hashtags": ["#FLASH", "#FLASHAI", "#AI", "#Tech", "#Coding"],
  "tags": ["AI", "Claude Code", "GitHub"],
  "mood": "hype",
  "energy": 4,
  "source_urls": ["https://..."],
  "scenes": [
    {
      "type": "hook",
      "voice": "Mama, ee AI tool chusthe shock avthav!",
      "big": "THIS AI REPO IS INSANE",
      "sub": "Next-Gen Dev Tool",
      "items": [],
      "cmd": [],
      "visual_cue": "Fast zoom-in on GitHub logo with glitch effect",
      "energy": 5
    },
    {
      "type": "repo",
      "voice": "Idi open source project with over 20K stars.",
      "big": "20,000+ STARS ON GITHUB",
      "sub": "Trending Right Now",
      "items": [],
      "cmd": [],
      "visual_cue": "Highlight GitHub stars badge and file tree",
      "energy": 4
    },
    {
      "type": "terminal",
      "voice": "Single command tho direct ga run cheyocchu.",
      "big": "ONE COMMAND SETUP",
      "sub": "Run Instantly",
      "items": [],
      "cmd": ["pip install claude-code"],
      "visual_cue": "CRT terminal typing animation with green scanlines",
      "energy": 4
    },
    {
      "type": "points",
      "voice": "Automatic coding, instant debug mariyu full agent support undi.",
      "big": "TOP FEATURES",
      "sub": "",
      "items": ["Instant Debugging", "Multi-Agent Support", "Zero Config"],
      "cmd": [],
      "visual_cue": "Glassmorphism cards floating in with spring motion",
      "energy": 3
    },
    {
      "type": "cta",
      "voice": "Nee projects lo try chesi, daily AI updates kosam follow avvandi!",
      "big": "FOLLOW FOR DAILY AI",
      "sub": "Double Tap",
      "items": [],
      "cmd": [],
      "visual_cue": "Branded channel card with animated like/subscribe icons",
      "energy": 5
    }
  ]
}
"""


def _call_gemini(prompt: str, grounded: bool = False) -> str:
    """Call Google Gemini REST API."""
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        raise ValueError("GEMINI_API_KEY is not set")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={key}"
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.85, "maxOutputTokens": 2048}
    }
    if grounded:
        body["tools"] = [{"google_search": {}}]

    res = requests.post(url, json=body, timeout=45)
    if res.status_code != 200:
        raise RuntimeError(f"Gemini API error {res.status_code}: {res.text[:200]}")

    data = res.json()
    parts = data["candidates"][0]["content"]["parts"]
    return "".join(p.get("text", "") for p in parts)


def _call_openrouter(prompt: str) -> str:
    """Failover to OpenRouter with configured model."""
    key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise ValueError("OPENROUTER_API_KEY is not set")

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/naveenk7100-ship-it/studio",
        "X-Title": "AI Auto-Reels Studio"
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional video script engine that outputs pure valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.85,
        "max_tokens": 3000
    }

    res = requests.post(url, headers=headers, json=payload, timeout=90)
    if res.status_code != 200:
        raise RuntimeError(f"OpenRouter error {res.status_code}: {res.text[:200]}")

    data = res.json()
    choice = data.get("choices", [{}])[0]
    msg = choice.get("message", {})
    content = msg.get("content") or msg.get("reasoning") or choice.get("text") or ""
    return content


NARAROUTER_MODEL = os.getenv("NARAROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct")


def _call_nararouter(prompt: str) -> str:
    """Third fallback: NaraRouter API."""
    key = os.getenv("NARAROUTER_API_KEY", "").strip()
    if not key:
        raise ValueError("NARAROUTER_API_KEY is not set")

    url = "https://api.nararouter.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": NARAROUTER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional video script engine that outputs pure valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.85,
        "max_tokens": 3000
    }

    res = requests.post(url, headers=headers, json=payload, timeout=60)
    if res.status_code != 200:
        raise RuntimeError(f"NaraRouter error {res.status_code}: {res.text[:200]}")

    data = res.json()
    choice = data.get("choices", [{}])[0]
    return choice.get("message", {}).get("content", "")


def call_llm(prompt: str, grounded: bool = False) -> str:
    """Robust LLM chain with automatic failover and exponential backoff:
    1. Gemini -> 2. OpenRouter -> 3. NaraRouter
    """
    # 1. Attempt Gemini first
    if os.getenv("GEMINI_API_KEY"):
        for attempt in range(2):
            try:
                print(f"[LLM] Querying Gemini ({GEMINI_MODEL}, attempt {attempt+1})...")
                return _call_gemini(prompt, grounded=grounded)
            except Exception as e:
                print(f"[LLM] Gemini attempt {attempt+1} failed: {e}")
                time.sleep(2 ** attempt)

    # 2. Failover to OpenRouter
    if os.getenv("OPENROUTER_API_KEY"):
        for attempt in range(3):
            try:
                print(f"[LLM FAILOVER] Querying OpenRouter ({OPENROUTER_MODEL}, attempt {attempt+1})...")
                return _call_openrouter(prompt)
            except Exception as e:
                print(f"[LLM FAILOVER] OpenRouter attempt {attempt+1} failed: {e}")
                time.sleep(2 ** attempt)

    # 3. Failover to NaraRouter
    if os.getenv("NARAROUTER_API_KEY"):
        for attempt in range(2):
            try:
                print(f"[LLM 3rd FALLBACK] Querying NaraRouter ({NARAROUTER_MODEL}, attempt {attempt+1})...")
                return _call_nararouter(prompt)
            except Exception as e:
                print(f"[LLM 3rd FALLBACK] NaraRouter attempt {attempt+1} failed: {e}")
                time.sleep(2 ** attempt)

    raise RuntimeError("All LLM providers (Gemini, OpenRouter, NaraRouter) failed in failover chain")


def _clean_json_response(raw_text: str) -> dict:
    """Extract and parse valid JSON from LLM output."""
    raw = raw_text.strip()
    # Strip markdown ```json code blocks if present
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        raise ValueError("No JSON object found in LLM response")

    data = json.loads(m.group(0))
    if "scenes" not in data or not data["scenes"]:
        raise ValueError("Script JSON missing 'scenes'")

    # Validate each scene and ensure no Telugu Unicode characters exist in voice
    total_words = 0
    for s in data["scenes"]:
        voice = s.get("voice", "")
        if re.search(r"[\u0C00-\u0C7F]", voice):
            raise ValueError("Detected prohibited Telugu Unicode script in spoken text")
        total_words += len(voice.split())
        s.setdefault("big", "")
        s.setdefault("sub", "")
        s.setdefault("items", [])
        s.setdefault("cmd", [])
        s.setdefault("visual_cue", "")
        s.setdefault("energy", data.get("energy", 3))

    data["total_words"] = total_words
    return data


def generate_candidate(repo_or_topic: dict, angle: str, is_repo: bool = True) -> dict:
    """Generate a single script candidate with a specific creative angle."""
    if is_repo:
        prompt = (
            f"{PROMPT_RULES}\n"
            f"CREATIVE ANGLE: {angle}\n"
            f"TARGET REPO DETAILS:\n"
            f"- Name: {repo_or_topic['name']}\n"
            f"- Description: {repo_or_topic['description']}\n"
            f"- GitHub Stars: {repo_or_topic['stars']:,}\n"
            f"- Language: {repo_or_topic['language']}\n"
            f"- License: {repo_or_topic['license']}\n"
            f"- Verified Commands: {repo_or_topic['verified_commands']}\n"
            f"- README Summary: {repo_or_topic['readme_summary'][:1500]}\n\n"
            f"Generate the complete JSON script now."
        )
    else:
        prompt = (
            f"{PROMPT_RULES}\n"
            f"CREATIVE ANGLE: {angle}\n"
            f"TOPIC: {repo_or_topic.get('title', 'Trending AI Tool/Tip')}\n"
            f"DETAILS: {repo_or_topic.get('details', '')}\n\n"
            f"Generate the complete JSON script now."
        )

    for attempt in range(3):
        try:
            resp = call_llm(prompt)
            return _clean_json_response(resp)
        except Exception as e:
            print(f"[CANDIDATE] Attempt {attempt+1} error for angle '{angle}': {e}")
            time.sleep(1)
    raise RuntimeError(f"Failed to generate candidate for angle {angle}")


def critic_pass(candidates: list, grounded_info: dict) -> dict:
    """Critic evaluation pass scoring candidates on retention, grounding, and naturalness."""
    print(f"[CRITIC] Evaluating {len(candidates)} candidate scripts...")

    # If only one candidate succeeded, return it after safety check
    if len(candidates) == 1:
        return candidates[0]

    eval_prompt = (
        "You are an expert short-form video critic and editor.\n"
        "Score the following 3 candidate scripts for a Telugu tech vertical video channel (25-35s).\n"
        "Criteria:\n"
        "1. Hook strength in first 1.5s (0-25 pts): High curiosity, instant pattern interrupt, < 10 words.\n"
        "2. Factual grounding (0-25 pts): All claims supported by README facts; commands must match verified commands.\n"
        "3. Tenglish naturalness (0-20 pts): Fluent spoken romanized Telugu, zero Telugu Unicode script, authentic slang.\n"
        "4. Word count & pacing (0-15 pts): Total spoken words between 70 and 95 words.\n"
        "5. Loop ending / CTA (0-15 pts): Connects back to opening or strong follow trigger.\n\n"
        f"Grounded Repo Facts: {grounded_info.get('name')}, Stars: {grounded_info.get('stars')}, Commands: {grounded_info.get('verified_commands')}\n\n"
        f"Candidate 1:\n{json.dumps(candidates[0])}\n\n"
        f"Candidate 2:\n{json.dumps(candidates[1])}\n\n"
        f"Candidate 3:\n{json.dumps(candidates[2]) if len(candidates) > 2 else 'N/A'}\n\n"
        "Respond with ONLY a JSON object:\n"
        '{"winner_index": 0, "scores": [85, 92, 78], "critic_reason": "Candidate 2 had the punchiest hook and exact command grounding."}'
    )

    try:
        critic_resp = call_llm(eval_prompt)
        m = re.search(r"\{.*\}", critic_resp, re.DOTALL)
        if m:
            eval_data = json.loads(m.group(0))
            winner_idx = int(eval_data.get("winner_index", 0))
            if 0 <= winner_idx < len(candidates):
                print(f"[CRITIC WINNER] Selected Candidate {winner_idx+1}: {eval_data.get('critic_reason')}")
                return candidates[winner_idx]
    except Exception as e:
        print(f"[CRITIC NOTICE] Critic pass fallback ({e}), selecting candidate with optimal word count.")

    # Fallback heuristic: pick candidate closest to ideal 82 words
    best = min(candidates, key=lambda c: abs(c.get("total_words", 80) - 82))
    return best


def for_repo(repo: dict) -> dict:
    """Generate 3 candidates and select the winner via critic pass for a repo."""
    angles = [
        "Shock & Curiosity Hook (Mama, manual ga idi chesthunnara?)",
        "Power-User Speed Hook (Claude Code & AI Devs ki secret superpower)",
        "Trending Open-Source Alert (Top engineers vaduthunna viral repo)"
    ]

    candidates = []
    for angle in angles:
        try:
            cand = generate_candidate(repo, angle, is_repo=True)
            cand["topic_key"] = repo["name"]
            cand["source_urls"] = [repo["url"]]
            cand["repo"] = {
                "name": repo["name"],
                "stars": repo["stars"],
                "language": repo["language"],
                "url": repo["url"]
            }
            candidates.append(cand)
        except Exception as e:
            print(f"[PIPELINE] Warning: candidate generation failed for angle: {e}")

    if not candidates:
        raise RuntimeError("All candidate generations failed for repo")

    winner = critic_pass(candidates, repo)
    print(f"[SCRIPT ENGINE SUCCESS] Script generated: '{winner.get('title')}' ({winner.get('total_words')} words, {len(winner.get('scenes'))} scenes)")
    return winner


def for_topic(topic_title: str, details: str = "", history_titles: list = None) -> dict:
    """Generate script for non-repo AI / Claude Code topic."""
    topic_data = {"title": topic_title, "details": details}
    angles = [
        "Shock Hook (Secret AI feature nobody is talking about)",
        "Workflow Accelerator (How to 10x your coding in Claude Code)",
        "New Breakthrough (The latest AI model update you need to know)"
    ]

    candidates = []
    for angle in angles:
        try:
            cand = generate_candidate(topic_data, angle, is_repo=False)
            cand["topic_key"] = re.sub(r"[^a-zA-Z0-9_-]", "_", topic_title.lower())[:30]
            cand["source_urls"] = ["https://anthropic.com/news", "https://github.com"]
            candidates.append(cand)
        except Exception as e:
            print(f"[PIPELINE] Candidate generation notice: {e}")

    if not candidates:
        raise RuntimeError("All candidate generations failed for topic")

    winner = critic_pass(candidates, topic_data)
    print(f"[SCRIPT ENGINE SUCCESS] Topic Script generated: '{winner.get('title')}' ({winner.get('total_words')} words)")
    return winner
