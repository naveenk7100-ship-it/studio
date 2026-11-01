"""AI Auto-Reels Studio: 8 Structurally Distinct Motion Templates.

Each template features custom:
- Canvas Layouts (split-screen, full-screen terminal, keynote slide, broadcast TV, CAD blueprint)
- Motion Language & Transitions (zoom punch, typewriter, slow dolly, glitch, spring)
- Visual Elements (real screenshots, terminal output, lower thirds, tickers)
- Caption Styling (safe-zone compliant, word-pop, highlighters)
- CTA Designs (auto-fitting pills, ASCII buttons, broadcast banners)
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import config

W, H = config.VIDEO_CONFIG["width"], config.VIDEO_CONFIG["height"]

# Safe zone boundaries (in pixels) for Instagram Reels & YouTube Shorts
SAFE_TOP = config.VIDEO_CONFIG["safe_zone_top"]
SAFE_BOTTOM = H - config.VIDEO_CONFIG["safe_zone_bottom"]
BRAND_HANDLE = config.IG_HANDLE

TEMPLATES_CATALOG = {
    "terminal_hacker": {
        "name": "Terminal Hacker",
        "primary": (0, 255, 102),      # Phosphor Green
        "secondary": (255, 176, 0),    # Amber
        "bg_base": (5, 10, 6),
        "text": (230, 255, 235),
        "mono": True,
        "music_mood": "dark-tech"
    },
    "apple_keynote": {
        "name": "Apple-Keynote Minimal",
        "primary": (255, 255, 255),    # Pure White
        "secondary": (160, 160, 175),  # Space Gray
        "bg_base": (15, 15, 18),
        "text": (255, 255, 255),
        "mono": False,
        "music_mood": "chill-focus"
    },
    "breaking_news": {
        "name": "Breaking News",
        "primary": (235, 30, 50),      # Crimson Red
        "secondary": (255, 215, 0),    # Warning Yellow
        "bg_base": (8, 14, 28),
        "text": (255, 255, 255),
        "mono": False,
        "music_mood": "news-urgent"
    },
    "neon_cyberpunk": {
        "name": "Neon Cyberpunk",
        "primary": (0, 229, 255),      # Neon Cyan
        "secondary": (255, 45, 149),   # Hot Magenta
        "bg_base": (8, 6, 26),
        "text": (255, 255, 255),
        "mono": False,
        "music_mood": "futuristic"
    },
    "blueprint_dev": {
        "name": "Blueprint / Dev Docs",
        "primary": (0, 210, 255),      # Drafting Cyan
        "secondary": (255, 255, 255),  # Drafting White
        "bg_base": (10, 36, 75),       # Blueprint Navy
        "text": (240, 248, 255),
        "mono": True,
        "music_mood": "chill-focus"
    },
    "bold_brutalist": {
        "name": "Bold Brutalist Typography",
        "primary": (255, 225, 0),      # Electric Yellow
        "secondary": (255, 255, 255),  # White
        "bg_base": (12, 12, 12),       # Pitch Black
        "text": (255, 255, 255),
        "mono": False,
        "music_mood": "hype"
    },
    "glassmorphism_ui": {
        "name": "Glassmorphism UI",
        "primary": (120, 180, 255),    # Frost Blue
        "secondary": (220, 130, 255),  # Soft Purple
        "bg_base": (12, 16, 35),
        "text": (255, 255, 255),
        "mono": False,
        "music_mood": "inspiring"
    },
    "cinematic_dark": {
        "name": "Cinematic Dark",
        "primary": (225, 175, 95),     # Warm Amber / Gold
        "secondary": (180, 200, 210),  # Steel Silver
        "bg_base": (6, 7, 10),
        "text": (245, 240, 230),
        "mono": False,
        "music_mood": "dark-tech"
    }
}


def pick_template(topic_type: str, mood_tag: str, last_template: str = "") -> str:
    """Smart rotation & mood-based template selection. Guarantees no back-to-back repetition."""
    templates = list(TEMPLATES_CATALOG.keys())
    eligible = [t for t in templates if t != last_template]

    mood_map = {
        "dark-tech": ["terminal_hacker", "cinematic_dark"],
        "chill-focus": ["apple_keynote", "blueprint_dev"],
        "news-urgent": ["breaking_news", "bold_brutalist"],
        "futuristic": ["neon_cyberpunk", "glassmorphism_ui"],
        "hype": ["bold_brutalist", "neon_cyberpunk"],
        "inspiring": ["glassmorphism_ui", "apple_keynote"],
        "playful": ["bold_brutalist", "glassmorphism_ui"]
    }

    for p in mood_map.get(mood_tag, []):
        if p in eligible:
            return p
    return eligible[0]


# --- STRUCTURAL CANVAS RENDERERS ---

def draw_canvas(template_key: str, t: float, width: int = W, height: int = H) -> Image.Image:
    """Render the base structural canvas for each template."""
    cfg = TEMPLATES_CATALOG.get(template_key, TEMPLATES_CATALOG["terminal_hacker"])
    im = Image.new("RGBA", (width, height), cfg["bg_base"] + (255,))
    d = ImageDraw.Draw(im)

    if template_key == "terminal_hacker":
        # Full-screen CRT terminal with authentic scanlines
        scan_spacing = 8
        scan_off = int((t * 30) % scan_spacing)
        for y in range(scan_off, height, scan_spacing):
            d.line([(0, y), (width, y)], fill=(0, 28, 12, 110), width=1)
        # Top terminal bar
        d.rectangle([(30, 50), (width - 30, 110)], fill=(0, 32, 14, 240), outline=(0, 255, 102, 180), width=2)
        d.ellipse([(55, 72), (73, 90)], fill=(255, 95, 86, 255))
        d.ellipse([(85, 72), (103, 90)], fill=(255, 189, 46, 255))
        d.ellipse([(115, 72), (133, 90)], fill=(39, 201, 63, 255))
        # Terminal title
        d.text((160, 70), "bash - 80x24 [ai-developer-workspace]", fill=cfg["primary"] + (255,))

    elif template_key == "apple_keynote":
        # Minimalist presentation canvas with soft radial spotlight
        cx, cy = width // 2, int(height * 0.45)
        for r in range(700, 100, -80):
            alpha = int(24 * (1.0 - (r / 700)))
            d.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(38, 40, 48, alpha))
        # Top breadcrumb bar
        d.line([(60, 120), (width - 60, 120)], fill=(45, 45, 55, 255), width=2)
        d.text((60, 80), "ANTHROPIC // CLAUDE CODE WORKFLOWS", fill=cfg["secondary"] + (255,))

    elif template_key == "breaking_news":
        # Broadcast Studio Split-Screen Layout
        # Top Red Breaking Banner
        d.rectangle([(0, 40), (width, 130)], fill=cfg["primary"] + (255,))
        # Flashing live dot
        if int(t * 3) % 2 == 0:
            d.ellipse([(50, 75), (70, 95)], fill=(255, 255, 255, 255))
        d.text((85, 72), "LIVE // AI TECH REPORT // OPEN PROTOCOL RADAR", fill=(255, 255, 255, 255))

        # Bottom Live News Ticker Tape (y = 1530 to 1610)
        ticker_y = SAFE_BOTTOM + 20
        d.rectangle([(0, ticker_y), (width, ticker_y + 80)], fill=(12, 18, 32, 250))
        d.rectangle([(0, ticker_y), (220, ticker_y + 80)], fill=cfg["secondary"] + (255,))
        d.text((35, ticker_y + 24), "BREAKING", fill=(0, 0, 0, 255))
        # Animated ticker scroll
        offset = int((t * 160) % 1200)
        ticker_text = "ANTHROPIC OPEN SOURCES MCP /// OVER 1,000+ SERVERS CONNECTED /// VERIFIED DEV RADAR /// "
        d.text((250 - offset, ticker_y + 24), ticker_text + ticker_text, fill=(240, 245, 255, 240))

    elif template_key == "neon_cyberpunk":
        # 3D perspective floor grid
        grid_start = int(height * 0.65)
        d.line([(0, grid_start), (width, grid_start)], fill=cfg["primary"] + (180,), width=3)
        for x in range(-10, 11):
            dest = width // 2 + x * 120
            d.line([(width // 2, grid_start), (dest, height)], fill=cfg["secondary"] + (75,), width=2)
        cycle = (t * 80) % 60
        for y in range(0, height - grid_start, 60):
            cy = grid_start + int(((y + cycle) ** 1.3) * 0.25)
            if cy < height:
                d.line([(0, cy), (width, cy)], fill=cfg["primary"] + (60,), width=2)
        # Cyber HUD header
        d.line([(40, 100), (width - 40, 100)], fill=cfg["primary"] + (140,), width=2)
        d.text((50, 65), "CYBER_RADAR // VER_2.4 [AI_AGENTS]", fill=cfg["primary"] + (255,))

    elif template_key == "blueprint_dev":
        # Technical CAD blueprint grid
        grid = 36
        for x in range(0, width, grid):
            d.line([(x, 0), (x, height)], fill=(18, 55, 110, 85), width=1)
        for y in range(0, height, grid):
            d.line([(0, y), (width, y)], fill=(18, 55, 110, 85), width=1)
        # Major 180px lines
        for x in range(0, width, grid * 5):
            d.line([(x, 0), (x, height)], fill=(28, 85, 150, 140), width=2)
        # Corner technical marks
        d.line([(40, 60), (120, 60)], fill=cfg["primary"] + (255,), width=3)
        d.line([(40, 60), (40, 140)], fill=cfg["primary"] + (255,), width=3)
        d.text((50, 75), "SPEC: ARCHITECTURE-DOC-01", fill=cfg["primary"] + (255,))

    elif template_key == "bold_brutalist":
        # Stark brutalist diagonal warning stripes on top
        d.rectangle([(0, 0), (width, 80)], fill=cfg["primary"] + (255,))
        d.text((40, 22), "★ VERIFIED OPEN SOURCE REPO ★", fill=(0, 0, 0, 255))
        d.rectangle([(30, 110), (width - 30, height - 110)], outline=cfg["primary"] + (255,), width=8)

    elif template_key == "glassmorphism_ui":
        # Floating colored gradient orbs behind frosted cards
        x1 = int(width * 0.3 + 100 * math.sin(t * 0.5))
        y1 = int(height * 0.35 + 80 * math.cos(t * 0.4))
        d.ellipse([(x1 - 350, y1 - 350), (x1 + 350, y1 + 350)], fill=(65, 35, 150, 110))
        x2 = int(width * 0.7 + 90 * math.cos(t * 0.6))
        y2 = int(height * 0.7 + 100 * math.sin(t * 0.45))
        d.ellipse([(x2 - 320, y2 - 320), (x2 + 320, y2 + 320)], fill=(0, 140, 210, 95))

    elif template_key == "cinematic_dark":
        # Cinemascope letterbox bars
        bar_h = 160
        d.rectangle([(0, 0), (width, bar_h)], fill=(0, 0, 0, 255))
        d.rectangle([(0, height - bar_h), (width, height)], fill=(0, 0, 0, 255))
        d.text((50, 175), "FILM SCAN // 35MM CINEMATIC TECH", fill=cfg["primary"] + (180,))

    return im
