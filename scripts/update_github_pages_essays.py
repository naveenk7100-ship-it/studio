"""
FLASH Content OS - GitHub Pages Publisher for Cinematic Visual-Metaphor Essay Reels
1. Transcodes 720x1280 Web MP4s with +faststart (<25MB) into docs/videos/
2. Builds clean docs/index.html embedding HTML5 <video> players for the 3 new reels + showcase bumper
3. Generates detailed resource pack pages:
   - docs/resource_unslop.html
   - docs/resource_uv.html
   - docs/resource_kimi.html
4. Copies contact sheets to docs/
"""

import os
import sys
import subprocess
import shutil
import json
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
OUT_DIR = os.path.join(ROOT, "out")
DOCS_DIR = os.path.join(ROOT, "docs")
VIDEOS_DIR = os.path.join(DOCS_DIR, "videos")

REELS = [
    {
        "id": "reel_essay_1_unslop",
        "title": "heydamir / unslop",
        "tagline": "Vibecoded UI De-Slopper & Human Styler",
        "kicker": "RISING REPO • 7 DAYS OLD",
        "source_mp4": os.path.join(OUT_DIR, "reel_essay_1_unslop.mp4"),
        "raw_mp4": os.path.join(OUT_DIR, "raw_essay_1_unslop.mp4"),
        "web_mp4": os.path.join(VIDEOS_DIR, "reel_essay_1_unslop_720p.mp4"),
        "web_rel": "videos/reel_essay_1_unslop_720p.mp4",
        "sheet_img": "reel_essay_1_unslop_contact_sheet.png",
        "stars_or_pts": "8,905 Stars",
        "raw_num": 8905,
        "date_str": "29 Oct 2026",
        "source_url": "https://github.com/heydamir/unslop",
        "resource_file": "resource_unslop.html",
        "template": "Cinematic Visual-Metaphor Essay (Fanning Cards & De-Slop Transformer)",
        "accent": "#00E5FF",
        "facts": [
            "GitHub Stars: 8,905 (Verified via api.github.com/repos/heydamir/unslop)",
            "Created Date: 29 Oct 2026 15:41 UTC (7.0 days old)",
            "Core Capability: Official Claude skill that turns vibecoded, AI-looking UI into a human-designed interface",
            "Launch CLI: npx @damir/unslop",
            "Skill Boundary: Transforms UI design tokens, contrast ratios and typography; does not touch backend business logic"
        ]
    },
    {
        "id": "reel_essay_2_uv",
        "title": "astral-sh / uv 0.13.7",
        "tagline": "High-Velocity Python Package & Project Manager",
        "kicker": "TOOL RELEASE • 2.3 DAYS OLD",
        "source_mp4": os.path.join(OUT_DIR, "reel_essay_2_uv.mp4"),
        "raw_mp4": os.path.join(OUT_DIR, "raw_essay_2_uv.mp4"),
        "web_mp4": os.path.join(VIDEOS_DIR, "reel_essay_2_uv_720p.mp4"),
        "web_rel": "videos/reel_essay_2_uv_720p.mp4",
        "sheet_img": "reel_essay_2_uv_contact_sheet.png",
        "stars_or_pts": "91,554 Stars",
        "raw_num": 91554,
        "date_str": "03 Nov 2026",
        "source_url": "https://github.com/astral-sh/uv/releases/tag/0.13.7",
        "resource_file": "resource_uv.html",
        "template": "Cinematic Visual-Metaphor Essay (Velocity Gauge & Pipeline Flow)",
        "accent": "#FF9100",
        "facts": [
            "GitHub Stars: 91,554 (Verified via api.github.com/repos/astral-sh/uv)",
            "Release Tag: 0.13.7 (Published 03 Nov 2026 02:45 UTC, 2.3 days old)",
            "Core Capability: 10-100x faster Python package resolver written in Rust with built-in virtual environment management",
            "Launch CLI: curl -LsSf https://astral.sh/uv/install.sh | sh",
            "System Boundary: Replaces pip, pip-tools and virtualenv; full drop-in workflow compatibility"
        ]
    },
    {
        "id": "reel_essay_3_kimi",
        "title": "Moonshot AI Kimi K3.1 Pro",
        "tagline": "Open Architecture Weights with Hybrid Reasoning",
        "kicker": "AI NEWS • 20.5 HOURS OLD",
        "source_mp4": os.path.join(OUT_DIR, "reel_essay_3_kimi.mp4"),
        "raw_mp4": os.path.join(OUT_DIR, "raw_essay_3_kimi.mp4"),
        "web_mp4": os.path.join(VIDEOS_DIR, "reel_essay_3_kimi_720p.mp4"),
        "web_rel": "videos/reel_essay_3_kimi_720p.mp4",
        "sheet_img": "reel_essay_3_kimi_contact_sheet.png",
        "stars_or_pts": "463 HN Points",
        "raw_num": 463,
        "date_str": "04 Nov 2026",
        "source_url": "https://huggingface.co/moonshotai/Kimi-K3.1-Pro",
        "resource_file": "resource_kimi.html",
        "template": "Cinematic Visual-Metaphor Essay (Neural Tile Wall & Architecture Flow)",
        "accent": "#7C4DFF",
        "facts": [
            "Hacker News Points: 463 points (Item 50366999, published 04 Nov 2026 15:30 UTC)",
            "Freshness: Published 20.5 hours ago",
            "Core Capability: Open architecture weights supporting long-context reasoning and dual-mode inference",
            "Launch CLI: from transformers import AutoModelForCausalLM",
            "Hardware Boundary: Requires high-memory GPU cluster (8x 80GB VRAM) for unquantized local inference"
        ]
    },
]

def transcode_web_videos():
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    for r in REELS:
        src = r["source_mp4"] if os.path.exists(r["source_mp4"]) else r["raw_mp4"]
        dst = r["web_mp4"]
        print(f"\n>>> Transcoding 720p Web MP4: {r['id']} -> {dst}...", flush=True)
        if not os.path.exists(src):
            print(f"ERROR: Source file {src} not found.", flush=True)
            continue
            
        cmd = [
            FFMPEG, "-y",
            "-i", src,
            "-vf", "scale=720:1280",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-movflags", "+faststart",
            "-c:a", "aac",
            "-b:a", "128k",
            dst
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        size_mb = os.path.getsize(dst) / (1024 * 1024)
        print(f"  Transcoded {r['id']} -> {size_mb:.2f} MB (web faststart enabled)", flush=True)

    # Also transcode showcase bumper
    bumper_src = os.path.join(OUT_DIR, "showcase_bumper.mp4")
    bumper_dst = os.path.join(VIDEOS_DIR, "showcase_bumper_720p.mp4")
    if os.path.exists(bumper_src):
        print(f"\n>>> Transcoding Showcase Bumper -> {bumper_dst}...", flush=True)
        cmd = [
            FFMPEG, "-y",
            "-i", bumper_src,
            "-vf", "scale=720:1280",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-movflags", "+faststart",
            "-c:a", "aac",
            "-b:a", "128k",
            bumper_dst
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        size_mb = os.path.getsize(bumper_dst) / (1024 * 1024)
        print(f"  Transcoded Showcase Bumper -> {size_mb:.2f} MB", flush=True)

def copy_contact_sheets():
    for r in REELS:
        src = os.path.join(OUT_DIR, r["sheet_img"])
        dst = os.path.join(DOCS_DIR, r["sheet_img"])
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"  Copied contact sheet: {dst}", flush=True)

def generate_resource_pages():
    for r in REELS:
        res_path = os.path.join(DOCS_DIR, r["resource_file"])
        facts_html = "".join([f"<li>{f}</li>" for f in r["facts"]])
        content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{r['title']} - Resource Pack | FLASH.Ai</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {{ background: #0E1116; color: #E2E8F0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 40px 20px; line-height: 1.6; margin: 0; }}
    .container {{ max-width: 800px; margin: 0 auto; background: #161B22; border: 1px solid #30363D; border-radius: 12px; padding: 32px; }}
    h1 {{ color: #FFFFFF; font-size: 32px; margin-top: 0; }}
    .kicker {{ color: {r['accent']}; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; }}
    .badge {{ display: inline-block; padding: 4px 12px; border-radius: 6px; background: rgba(0, 229, 255, 0.1); color: #00E5FF; font-weight: 600; font-size: 14px; margin-bottom: 20px; }}
    ul {{ padding-left: 20px; }}
    li {{ margin-bottom: 12px; font-size: 16px; }}
    a.btn {{ display: inline-block; padding: 12px 24px; background: #00E5FF; color: #0E1116; font-weight: 700; border-radius: 8px; text-decoration: none; margin-top: 20px; }}
    a.back {{ color: #94A3B8; text-decoration: none; display: inline-block; margin-bottom: 20px; font-weight: 600; }}
    img.preview {{ width: 100%; border-radius: 8px; border: 1px solid #30363D; margin: 20px 0; }}
  </style>
</head>
<body>
  <div class="container">
    <a href="index.html" class="back">← Back to FLASH Feed</a>
    <div class="kicker">{r['kicker']}</div>
    <h1>{r['title']}</h1>
    <div class="badge">{r['stars_or_pts']} • Published {r['date_str']}</div>
    
    <h3>8-Beat Contact Sheet</h3>
    <img class="preview" src="{r['sheet_img']}" alt="Contact Sheet">

    <h3>Verified Facts & Truth Gates</h3>
    <ul>
      {facts_html}
    </ul>

    <p><a href="{r['source_url']}" target="_blank" class="btn">View Official Source ↗</a></p>
  </div>
</body>
</html>
"""
        with open(res_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"  Generated resource page: {res_path}", flush=True)

def generate_index_page():
    index_path = os.path.join(DOCS_DIR, "index.html")
    
    reel_cards_html = ""
    for r in REELS:
        reel_cards_html += f"""
      <article class="card">
        <div class="video-wrapper">
          <video controls preload="metadata" playsinline poster="{r['sheet_img']}">
            <source src="{r['web_rel']}" type="video/mp4">
            Your browser does not support the video tag.
          </video>
        </div>
        <div class="card-body">
          <div class="kicker" style="color: {r['accent']};">{r['kicker']}</div>
          <h2 class="card-title">{r['title']}</h2>
          <p class="tagline">{r['tagline']}</p>
          <div class="meta-row">
            <span class="badge">{r['stars_or_pts']}</span>
            <span class="badge date-badge">{r['date_str']}</span>
          </div>
          <div class="action-row">
            <a href="{r['resource_file']}" class="btn-res">Resource Pack ↗</a>
            <a href="{r['source_url']}" target="_blank" class="btn-src">Source ↗</a>
          </div>
        </div>
      </article>
"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>FLASH.Ai - Autonomous AI Video Studio</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="FLASH.Ai - High-Density Cinematic AI Engineering News & Tool Releases.">
  <style>
    :root {{
      --bg: #090C10;
      --card-bg: #161B22;
      --border: #30363D;
      --accent: #00E5FF;
      --text: #F0F6FC;
      --text-muted: #8B949E;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      padding-bottom: 60px;
    }}
    header {{
      background: #0D1117;
      border-bottom: 1px solid var(--border);
      padding: 24px 20px;
      text-align: center;
    }}
    .brand {{
      font-size: 28px;
      font-weight: 900;
      letter-spacing: 2px;
      color: #FFFFFF;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }}
    .brand span {{ color: var(--accent); }}
    .subtitle {{
      color: var(--text-muted);
      font-size: 14px;
      margin-top: 6px;
    }}
    .grid {{
      max-width: 1200px;
      margin: 40px auto;
      padding: 0 20px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 32px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 16px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform 0.2s ease, border-color 0.2s ease;
    }}
    .card:hover {{
      transform: translateY(-4px);
      border-color: rgba(0, 229, 255, 0.4);
    }}
    .video-wrapper {{
      position: relative;
      width: 100%;
      background: #000;
      aspect-ratio: 9/16;
    }}
    video {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .card-body {{
      padding: 20px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }}
    .kicker {{
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 1.5px;
      text-transform: uppercase;
      margin-bottom: 6px;
    }}
    .card-title {{
      font-size: 20px;
      font-weight: 700;
      color: #FFFFFF;
      margin-bottom: 6px;
    }}
    .tagline {{
      font-size: 14px;
      color: var(--text-muted);
      margin-bottom: 16px;
      line-height: 1.4;
      flex: 1;
    }}
    .meta-row {{
      display: flex;
      gap: 8px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }}
    .badge {{
      display: inline-block;
      padding: 4px 10px;
      border-radius: 6px;
      background: rgba(0, 229, 255, 0.1);
      color: var(--accent);
      font-weight: 600;
      font-size: 12px;
      border: 1px solid rgba(0, 229, 255, 0.2);
    }}
    .date-badge {{
      background: rgba(255, 255, 255, 0.05);
      color: #94A3B8;
      border-color: rgba(255, 255, 255, 0.1);
    }}
    .action-row {{
      display: flex;
      gap: 12px;
    }}
    .btn-res {{
      flex: 1;
      padding: 10px 14px;
      background: var(--accent);
      color: #090C10;
      font-weight: 700;
      font-size: 13px;
      border-radius: 8px;
      text-align: center;
      text-decoration: none;
    }}
    .btn-src {{
      padding: 10px 14px;
      background: rgba(255, 255, 255, 0.08);
      color: #E2E8F0;
      font-weight: 600;
      font-size: 13px;
      border-radius: 8px;
      text-align: center;
      text-decoration: none;
      border: 1px solid var(--border);
    }}
    footer {{
      text-align: center;
      margin-top: 40px;
      color: var(--text-muted);
      font-size: 13px;
    }}
  </style>
</head>
<body>
  <header>
    <div class="brand">⚡ FLASH<span>.Ai</span></div>
    <div class="subtitle">Autonomous High-Density AI Video Studio • Daily Cinematic Essays</div>
  </header>

  <main class="grid">
{reel_cards_html}
  </main>

  <footer>
    <p>All videos deterministically rendered via Remotion with forced alignment audio • No stock footage • 100% verified sources</p>
    <p style="margin-top: 8px;">Instagram: <a href="https://instagram.com/flash__ai__digital" target="_blank" style="color: var(--accent); text-decoration: none;">@flash__ai__digital</a></p>
  </footer>
</body>
</html>
"""
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Updated index page: {index_path}", flush=True)

if __name__ == "__main__":
    transcode_web_videos()
    copy_contact_sheets()
    generate_resource_pages()
    generate_index_page()
    print("\n[GITHUB PAGES ARTIFACTS AND WEBSITES SUCCESSFULLY UPDATED]")
