#!/usr/bin/env python3
"""Daily Instagram token health check & auto-refresh.

Auto-renews Instagram Graph API long-lived access token (60-day validity)
and updates both the local .env and the GitHub Actions repository secret via gh CLI / GitHub PAT.
Fails loudly if the token cannot be refreshed or has expired.
"""
import os
import sys
import json
import subprocess
import requests

def load_env():
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("\"'")
                    if k not in os.environ:
                        os.environ[k] = v

def refresh_instagram_token():
    load_env()
    token = os.getenv("IG_ACCESS_TOKEN", "").strip()
    if not token:
        print("[TOKEN REFRESH] Error: IG_ACCESS_TOKEN not found in environment or .env")
        return False

    print("[TOKEN REFRESH] Checking Instagram access token...")
    # 1. Inspect current token via graph.instagram.com/me
    try:
        me_r = requests.get(f"https://graph.instagram.com/me?fields=id,username&access_token={token}", timeout=15)
        if me_r.status_code == 200:
            me_data = me_r.json()
            print(f"[TOKEN REFRESH] Token is valid for account: @{me_data.get('username')} (ID: {me_data.get('id')})")
        else:
            print(f"[TOKEN CRITICAL] Token inspection returned HTTP {me_r.status_code}: {me_r.text}")
    except Exception as e:
        print(f"[TOKEN REFRESH WARNING] Inspection warning: {e}")

    # 2. Call refresh_access_token
    refresh_url = f"https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token={token}"
    try:
        r = requests.get(refresh_url, timeout=20)
        if r.status_code != 200:
            print(f"[TOKEN REFRESH FAILED] HTTP {r.status_code}: {r.text}")
            return False

        data = r.json()
        new_token = data.get("access_token")
        expires_in = data.get("expires_in", 0)
        days = round(expires_in / 86400, 1)

        print(f"[TOKEN REFRESH SUCCESS] Token refreshed successfully! Valid for {days} days ({expires_in}s).")
        masked = "*" * (len(new_token) - 4) + new_token[-4:]
        print(f"[TOKEN REFRESH] New token ending in: {masked}")

        # 3. Update local .env
        env_file = ".env"
        if os.path.exists(env_file):
            with open(env_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            new_lines = []
            updated = False
            for line in lines:
                if line.startswith("IG_ACCESS_TOKEN="):
                    new_lines.append(f"IG_ACCESS_TOKEN={new_token}\n")
                    updated = True
                else:
                    new_lines.append(line)
            if not updated:
                new_lines.append(f"IG_ACCESS_TOKEN={new_token}\n")
            with open(env_file, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print("[TOKEN REFRESH] Updated local .env file.")

        # 4. Update GitHub Actions secret via gh CLI if available
        try:
            gh_check = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True)
            if gh_check.returncode == 0:
                print("[TOKEN REFRESH] Updating GitHub Actions repository secret 'IG_ACCESS_TOKEN' via gh CLI...")
                set_res = subprocess.run(["gh", "secret", "set", "IG_ACCESS_TOKEN", "-b", new_token], capture_output=True, text=True)
                if set_res.returncode == 0:
                    print("[TOKEN REFRESH SUCCESS] GitHub Actions secret 'IG_ACCESS_TOKEN' updated successfully!")
                else:
                    print(f"[TOKEN REFRESH NOTICE] gh secret set returned: {set_res.stderr.strip()}")
        except Exception as e:
            print(f"[TOKEN REFRESH NOTICE] gh CLI secret update skipped: {e}")

        # Send Telegram reminder on Day 45 (15 days or less remaining)
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if bot_token and chat_id and days <= 15:
            msg = (
                f"⚠️ *FLASH Instagram Token Alert (Day 45+)*\n\n"
                f"Your Instagram long-lived token has *{days} days* remaining.\n"
                f"Auto-refresh has been performed, but please run `python scripts/refresh_tokens.py` locally if needed.\n"
                f"Account: `@flash__ai__digital`"
            )
            try:
                requests.post(
                    f"https://api.telegram.org/bot{bot_token}/sendMessage",
                    json={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"},
                    timeout=10
                )
                print("[TOKEN REFRESH] Sent Day 45+ reminder to Telegram.")
            except Exception as te:
                print(f"[TOKEN REFRESH] Telegram alert failed: {te}")

    except Exception as e:
        print(f"[TOKEN REFRESH EXCEPTION] Critical error during token refresh: {e}")
        return False

if __name__ == "__main__":
    success = refresh_instagram_token()
    if not success:
        print("\n" + "!" * 60)
        print("INSTAGRAM TOKEN HEALTH CHECK FAILED LOUDLY!")
        print("The Instagram Access Token is about to expire or invalid.")
        print("Please refresh your token at developers.facebook.com or log in again.")
        print("!" * 60 + "\n")
        sys.exit(1)
