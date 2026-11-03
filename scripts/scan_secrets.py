#!/usr/bin/env python3
"""Pre-commit & pre-push secret scanner.
Scans git staged files / git diff for API keys, passwords, client secrets, and tokens.
Aborts if any secret pattern or non-ignored sensitive file is found.
"""
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

PATTERNS = [
    (r"AIza[0-9A-Za-z\-_]{35}", "Google API Key"),
    (r"GOCSPX-[0-9A-Za-z\-_]{28}", "Google OAuth Client Secret"),
    (r"sk-or-v1-[0-9a-f]{64}", "OpenRouter API Key"),
    (r"sk-[0-9A-Za-z]{32,}", "Generic Secret Key / OpenAI Key"),
    (r"IGAA[0-9A-Za-z\-_]{100,}", "Instagram User Access Token"),
    (r"EAA[0-9A-Za-z\-_]{100,}", "Facebook Access Token"),
    (r"ghp_[0-9A-Za-z]{36}", "GitHub Personal Access Token"),
    (r"gho_[0-9A-Za-z]{36}", "GitHub OAuth Access Token"),
]

# Check for hardcoded literal strings assigned to secret keys
# e.g. GEMINI_API_KEY = "AIzaSy..." or YT_CLIENT_SECRET = "GOCSPX-..."
SECRET_KEY_REGEX = re.compile(
    r"""\b(GEMINI_API_KEY|OPENROUTER_API_KEY|ELEVEN_API_KEY|ELEVENLABS_API_KEY|YT_CLIENT_SECRET|YT_REFRESH_TOKEN|IG_ACCESS_TOKEN|META_APP_SECRET|META_ACCESS_TOKEN)\b\s*[:=]\s*["']([^"'\s#{}]+)["']""",
    re.IGNORECASE
)

SAFE_LITERALS = {
    "", "your_key", "your_api_key", "your_token", "your_secret", "xxx", "here", "todo", "mock", "none"
}

def scan():
    try:
        res = subprocess.run(["git", "diff", "--cached"], cwd=ROOT, capture_output=True, check=True)
        diff_text = res.stdout.decode("utf-8", errors="ignore") if isinstance(res.stdout, bytes) else (res.stdout or "")
    except Exception as e:
        print(f"Error running git diff: {e}")
        return False

    if not diff_text.strip():
        res = subprocess.run(["git", "diff"], cwd=ROOT, capture_output=True)
        diff_text = res.stdout.decode("utf-8", errors="ignore") if isinstance(res.stdout, bytes) else (res.stdout or "")

    findings = []
    current_file = ""

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:].strip()
            continue

        if line.startswith("+") and not line.startswith("+++"):
            added = line[1:].strip()
            # Skip comments and markdown docs
            if current_file.endswith(".md") or added.startswith("#") or added.startswith("//") or added.startswith("*"):
                continue

            # Check for hardcoded literal assignment
            m = SECRET_KEY_REGEX.search(added)
            if m:
                key, val = m.group(1), m.group(2).strip()
                if val.lower() not in SAFE_LITERALS and not val.startswith("${") and not val.startswith("<"):
                    findings.append(f"Hardcoded secret literal assigned to '{key}' in {current_file}: {key}=***")

            # Check known secret regexes
            for pat, desc in PATTERNS:
                if re.search(pat, added):
                    findings.append(f"Secret pattern match ({desc}) in {current_file}")

    if findings:
        print("\n" + "!" * 60)
        print("SECRET SCANNER ABORT: Potential secrets detected in git diff!")
        for f in findings:
            print(f"  - {f}")
        print("Please remove all secrets from the codebase before committing or pushing.")
        print("!" * 60 + "\n")
        return False

    print("Secret scan passed cleanly: No secrets found in git diff.")
    return True

if __name__ == "__main__":
    if not scan():
        sys.exit(1)
