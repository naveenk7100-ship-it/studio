"""YouTube OAuth 2.0 flow to acquire a long-lived refresh token.

Run:
  python auth_yt.py
Or if your browser redirected to localhost:56131/?code=...:
  python auth_yt.py --code "PASTE_CODE_OR_REDIRECT_URL_HERE"
"""
import os
import re
import sys
import requests
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

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

load_env()
CLIENT_ID = os.getenv("YT_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("YT_CLIENT_SECRET", "")

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

def save_and_verify_token(refresh_token, client_id, client_secret):
    masked = "*" * (len(refresh_token) - 4) + refresh_token[-4:]
    print(f"\n[SUCCESS] Acquired YT_REFRESH_TOKEN: {masked}")

    # Verify credentials by listing the authenticated channel
    try:
        cred = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=SCOPES
        )
        yt = build("youtube", "v3", credentials=cred)
        res = yt.channels().list(mine=True, part="snippet").execute()
        items = res.get("items", [])
        if items:
            title = items[0]["snippet"]["title"]
            print(f"[VERIFIED] Authenticated YouTube Channel: '{title}' (ID: {items[0]['id']})")
        else:
            print("[INFO] Authorized successfully, but no YouTube channel found for this Google account.")
    except Exception as e:
        print(f"[NOTE] Channel lookup notice: {e}")

    # Save to local .env
    env_file = ".env"
    lines = []
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

    updated = False
    new_lines = []
    for line in lines:
        if line.startswith("YT_REFRESH_TOKEN="):
            new_lines.append(f"YT_REFRESH_TOKEN={refresh_token}\n")
            updated = True
        else:
            new_lines.append(line)

    if not updated:
        new_lines.append(f"YT_REFRESH_TOKEN={refresh_token}\n")

    with open(env_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"[SAVED] Appended YT_REFRESH_TOKEN safely into {env_file}")


def exchange_code(raw_input, redirect_uri="http://localhost:56131/"):
    code = raw_input.strip()
    if "code=" in code:
        m = re.search(r"code=([^&]+)", code)
        if m:
            code = requests.utils.unquote(m.group(1))

    print(f"Exchanging authorization code: {code[:15]}...")
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }
    r = requests.post(token_url, data=data, timeout=30)
    if r.status_code != 200:
        # Try alternate redirect_uri without port or with standard ports
        for alt_uri in ["http://localhost", "http://127.0.0.1", "http://localhost:8080/"]:
            data["redirect_uri"] = alt_uri
            r2 = requests.post(token_url, data=data, timeout=30)
            if r2.status_code == 200:
                r = r2
                break

    if r.status_code != 200:
        print(f"[ERROR] Token exchange failed ({r.status_code}): {r.text}")
        return False

    res_json = r.json()
    refresh_token = res_json.get("refresh_token")
    if not refresh_token:
        print(f"[WARNING] No refresh token in response (token already granted?): {res_json}")
        return False

    save_and_verify_token(refresh_token, CLIENT_ID, CLIENT_SECRET)
    return True


def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--code" and len(sys.argv) > 2:
            arg = sys.argv[2]
        exchange_code(arg)
        return

    from google_auth_oauthlib.flow import InstalledAppFlow
    client_config = {
        "installed": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost", "http://127.0.0.1"]
        }
    }
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    print("=" * 60)
    print("Authorization URL:")
    print(auth_url)
    print("=" * 60)
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
    if creds.refresh_token:
        save_and_verify_token(creds.refresh_token, CLIENT_ID, CLIENT_SECRET)

if __name__ == "__main__":
    main()
