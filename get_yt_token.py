"""Run ONCE on your laptop: python get_yt_token.py client_secret.json  -> prints YT refresh token."""
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
f = InstalledAppFlow.from_client_secrets_file(sys.argv[1], ["https://www.googleapis.com/auth/youtube.upload"])
c = f.run_local_server(port=0, access_type="offline", prompt="consent")
print("\nYT_REFRESH_TOKEN =", c.refresh_token)
