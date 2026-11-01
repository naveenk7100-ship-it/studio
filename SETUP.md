# AI Tech Auto-Reels: setup (one time, ~30 min)

Daily 2 videos: 12:30 PM IST (repo spotlight, ElevenLabs voice) and 8:30 PM IST (AI/Claude Code topic, free edge-tts voice).
Auto-posts to Instagram Reels + YouTube Shorts. Runs free on GitHub Actions.

## 1. GitHub repo
1. Create a **public** repo (public = unlimited free Actions minutes), upload all these files.
2. Settings > Secrets and variables > Actions > add the secrets below.

## 2. Secrets
| Secret | Where to get |
|---|---|
| GEMINI_API_KEY | aistudio.google.com > Get API key (free) |
| ELEVEN_API_KEY, ELEVEN_VOICE_ID | elevenlabs.io (profile key; voice ID from your voice page) |
| YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN | step 3 |
| IG_USER_ID, IG_ACCESS_TOKEN | step 4 |
| CLOUDINARY_URL (optional fallback) | cloudinary.com free > Dashboard > API Environment variable |
Optional variable (Variables tab): BRAND = your channel name shown on top-left.

## 3. YouTube
1. console.cloud.google.com > new project > enable **YouTube Data API v3**.
2. OAuth consent screen (External) > add yourself as Test user > then **Publish app** to "In production".
3. Credentials > Create OAuth client ID > Desktop app > download JSON.
4. On laptop: `pip install google-auth-oauthlib` then `python get_yt_token.py client_secret.json` > copy the refresh token.
5. IMPORTANT: new unaudited API projects can have uploads forced to PRIVATE by YouTube. If your first upload is private, apply for the free API compliance audit (support form "YouTube API Services Audit"). Until then, uploads still arrive in your Studio as private and you can flip them public.

## 4. Instagram
1. Instagram must be Creator/Business and linked to a Facebook Page (done).
2. developers.facebook.com > Create app (Business type) > add **Instagram Graph API** (use "Instagram API with Facebook Login").
3. Graph API Explorer: select your app, permissions: `instagram_basic, instagram_content_publish, pages_show_list, pages_read_engagement, business_management`. Generate token.
4. Make it long-lived: GET `/oauth/access_token?grant_type=fb_exchange_token&client_id=APP_ID&client_secret=APP_SECRET&fb_exchange_token=SHORT_TOKEN`.
5. GET `/me/accounts` with the long-lived token: the Page `access_token` there does not expire. Use that as IG_ACCESS_TOKEN.
6. GET `/PAGE_ID?fields=instagram_business_account` > the id is IG_USER_ID.
7. While the app is in Development mode, only you (admin) can post: that is fine for your own account.

## 5. Test
Actions tab > daily-reels > Run workflow > slot 1, dry = true (makes the video, no posting; download from Artifacts). Then dry = false.

## Offline preview (no keys)
`pip install -r requirements.txt` (+ ffmpeg) then `python main.py --mock some_voice.mp3`

## Notes
- Instagram: max ~25 API posts/day, 2/day is far inside the limit.
- Scheduled runs can start 5-20 min late on GitHub; normal.
- Topic repeats are blocked via history.json (auto-committed).
- After 2 weeks check Insights (IG + YT Studio) for your best hours, then change the two cron lines in .github/workflows/daily.yml (cron is UTC; IST = UTC + 5:30).
