import os
import subprocess
from dotenv import dotenv_values

HERE = r"C:\Users\navee\OneDrive\Desktop\studio"
vals = dotenv_values(os.path.join(HERE, ".env"))

REPO = "naveenk7100-ship-it/studio"

secret_map = {
    "GEMINI_API_KEY": vals.get("GEMINI_API_KEY"),
    "OPENROUTER_API_KEY": vals.get("OPENROUTER_API_KEY"),
    "NARAROUTER_API_KEY": vals.get("NARA_API_KEY") or vals.get("OPENROUTER_API_KEY"),
    "ELEVEN_API_KEY": vals.get("ELEVEN_API_KEY"),
    "ELEVEN_VOICE_ID": vals.get("ELEVEN_VOICE_ID"),
    "TELEGRAM_BOT_TOKEN": vals.get("TELEGRAM_BOT_TOKEN"),
    "TELEGRAM_CHAT_ID": vals.get("TELEGRAM_CHAT_ID"),
    "IG_USER_ID": vals.get("IG_USER_ID"),
    "IG_ACCESS_TOKEN": vals.get("IG_ACCESS_TOKEN"),
    "YT_CLIENT_ID": vals.get("YT_CLIENT_ID"),
    "YT_CLIENT_SECRET": vals.get("YT_CLIENT_SECRET")
}

for k, v in secret_map.items():
    if v and str(v).strip():
        cmd = ["gh", "secret", "set", k, "--body", str(v).strip(), "--repo", REPO]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[GITHUB SECRET] Set: {k} (status: OK)")
        else:
            print(f"[GITHUB SECRET ERROR] {k}: {res.stderr.strip()}")
    else:
        print(f"[GITHUB SECRET SKIPPED] {k} (empty in .env)")

print("All GitHub secrets updated successfully.")
