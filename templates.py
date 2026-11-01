"""AI Auto-Reels Studio: 8-Template Motion Engine & Styling System.

Templates:
1. terminal_hacker   - Green/Amber CRT, scanlines, monospace typing, retro terminal window
2. neon_cyberpunk    - Perspective grid, cyan/magenta neon glow, glitch effects
3. apple_keynote     - Ultra-clean minimal, soft radial spotlight, huge crisp modern type
4. glassmorphism_ui  - Floating frosted-glass cards, gradient orbs, soft specular borders
5. breaking_news     - Red urgent ticker banner, lower thirds, high-impact broadcast layout
6. blueprint_dev     - Technical navy engineering grid, white architectural lines, blueprint docs
7. bold_brutalist    - Stark high-contrast electric yellow & black, thick geometric blocks
8. cinematic_dark    - Film grain, heavy vignette, cinemascope letterbox feel, golden hour accents
"""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920

# Safe zone boundaries (in pixels)
SAFE_TOP = 260
SAFE_BOTTOM = 1500

TEMPLATES_CATALOG = {
    "terminal_hacker": {
        "name": "Terminal Hacker",
        "primary": (0, 255, 102),      # Phosphor Green
        "secondary": (255, 176, 0),    # Amber
        "bg_base": (4, 10, 6),
        "text": (230, 255, 235),
        "mono": True,
        "music_mood": "dark-tech"
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
    "apple_keynote": {
        "name": "Apple-Keynote Minimal",
        "primary": (255, 255, 255),    # Pure White
        "secondary": (160, 160, 170),  # Space Gray
        "bg_base": (14, 14, 18),
        "text": (255, 255, 255),
        "mono": False,
        "music_mood": "chill-focus"
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
    "breaking_news": {
        "name": "Breaking News",
        "primary": (255, 30, 60),      # Crimson Red
        "secondary": (255, 215, 0),    # Warning Yellow
        "bg_base": (8, 14, 28),
        "text": (255, 255, 255),
        "mono": False,
        "music_mood": "news-urgent"
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
        "secondary": (255, 255, 255),  # Paper White
        "bg_base": (12, 12, 12),       # Pitch Black
        "text": (255, 255, 255),
        "mono": False,
        "music_mood": "hype"
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
    """Smart rotation & mood-based template selection logic.

    Guarantees no consecutive repeat and picks visually fitting styles.
    """
    templates = list(TEMPLATES_CATALOG.keys())
    # Filter out last used template
    eligible = [t for t in templates if t != last_template]

    # Mood-based affinities
    mood_map = {
        "hype": ["bold_brutalist", "neon_cyberpunk"],
        "futuristic": ["neon_cyberpunk", "terminal_hacker"],
        "dark-tech": ["terminal_hacker", "cinematic_dark"],
        "news-urgent": ["breaking_news", "bold_brutalist"],
        "chill-focus": ["apple_keynote", "blueprint_dev"],
        "inspiring": ["glassmorphism_ui", "apple_keynote"],
        "playful": ["bold_brutalist", "glassmorphism_ui"]
    }

    preferred = mood_map.get(mood_tag, [])
    for p in preferred:
        if p in eligible:
            return p

    # Fallback rotation
    return eligible[0]


# --- PROCEDURAL BACKGROUND GENERATORS ---

def draw_background(template_key: str, t: float, width: int = W, height: int = H) -> Image.Image:
    """Render procedural background according to template theme."""
    cfg = TEMPLATES_CATALOG.get(template_key, TEMPLATES_CATALOG["neon_cyberpunk"])
    im = Image.new("RGBA", (width, height), cfg["bg_base"] + (255,))
    d = ImageDraw.Draw(im)

    if template_key == "terminal_hacker":
        # Green scanlines & CRT phosphor vignette
        scanline_spacing = 8
        scan_offset = int((t * 24) % scanline_spacing)
        for y in range(scan_offset, height, scanline_spacing):
            d.line([(0, y), (width, y)], fill=(0, 25, 10, 110), width=1)
        # Terminal header bar
        d.rectangle([(40, 60), (width - 40, 110)], fill=(0, 35, 15, 230))
        d.text((60, 72), "[bash - 80x24 - AI_STUDIO_TERMINAL]", fill=cfg["primary"] + (255,))
        d.line([(40, 110), (width - 40, 110)], fill=cfg["primary"] + (255,), width=2)

    elif template_key == "neon_cyberpunk":
        # Moving neon grid at bottom
        grid_y_start = int(height * 0.65)
        d.line([(0, grid_y_start), (width, grid_y_start)], fill=cfg["primary"] + (180,), width=3)
        # Perspective vertical grid lines
        horizon_x = width // 2
        for x_step in range(-12, 13):
            dest_x = horizon_x + x_step * 110
            d.line([(horizon_x, grid_y_start), (dest_x, height)], fill=cfg["secondary"] + (80,), width=2)
        # Horizontal moving lines
        grid_cycle = (t * 80) % 60
        for y_off in range(0, height - grid_y_start, 60):
            curr_y = grid_y_start + int(((y_off + grid_cycle) ** 1.3) * 0.25)
            if curr_y < height:
                d.line([(0, curr_y), (width, curr_y)], fill=cfg["primary"] + (60,), width=2)

    elif template_key == "apple_keynote":
        # Minimalist studio lighting / radial soft gradient
        spotlight_r = 750
        cx, cy = width // 2, int(height * 0.45)
        # Subtle layered circles for soft lighting
        for r_step in range(spotlight_r, 100, -80):
            alpha = int(22 * (1.0 - (r_step / spotlight_r)))
            d.ellipse(
                [(cx - r_step, cy - r_step), (cx + r_step, cy + r_step)],
                fill=(45, 48, 58, alpha)
            )

    elif template_key == "glassmorphism_ui":
        # Floating vibrant pastel orbs behind glass
        orb_x1 = int(width * 0.3 + 120 * math.sin(t * 0.6))
        orb_y1 = int(height * 0.35 + 90 * math.cos(t * 0.5))
        d.ellipse([(orb_x1 - 350, orb_y1 - 350), (orb_x1 + 350, orb_y1 + 350)], fill=(70, 40, 160, 120))

        orb_x2 = int(width * 0.7 + 100 * math.cos(t * 0.7))
        orb_y2 = int(height * 0.7 + 110 * math.sin(t * 0.55))
        d.ellipse([(orb_x2 - 320, orb_y2 - 320), (orb_x2 + 320, orb_y2 + 320)], fill=(0, 150, 220, 100))

    elif template_key == "breaking_news":
        # Red studio top bar & lower news ticker tape
        d.rectangle([(0, 60), (width, 120)], fill=cfg["primary"] + (255,))
        d.text((60, 75), "LIVE // TECH BREAKING // REPO RADAR", fill=(255, 255, 255, 255))

        # Bottom ticker bar
        ticker_y = SAFE_BOTTOM + 80
        d.rectangle([(0, ticker_y), (width, ticker_y + 70)], fill=(15, 22, 40, 240))
        d.rectangle([(0, ticker_y), (220, ticker_y + 70)], fill=cfg["secondary"] + (255,))
        d.text((30, ticker_y + 20), "ALERT", fill=(0, 0, 0, 255))
        # Animated ticker text
        ticker_offset = int((t * 140) % 800)
        d.text((250 - ticker_offset, ticker_y + 20), "DAILY AI REPO UPDATE /// CLAUDE CODE WORKFLOWS /// OPEN SOURCE RADAR /// ", fill=(240, 240, 255, 230))

    elif template_key == "blueprint_dev":
        # Fine technical drafting grid
        grid_size = 40
        for x in range(0, width, grid_size):
            d.line([(x, 0), (x, height)], fill=(20, 65, 120, 90), width=1)
        for y in range(0, height, grid_size):
            d.line([(0, y), (width, y)], fill=(20, 65, 120, 90), width=1)
        # Major 200px lines
        for x in range(0, width, grid_size * 5):
            d.line([(x, 0), (x, height)], fill=(30, 95, 160, 160), width=2)
        # Corner alignment markers
        d.line([(50, 50), (120, 50)], fill=cfg["primary"] + (255,), width=3)
        d.line([(50, 50), (50, 120)], fill=cfg["primary"] + (255,), width=3)
        d.text((60, 60), "SPEC: DEV-01", fill=cfg["primary"] + (255,))

    elif template_key == "bold_brutalist":
        # Stark geometric blocks & diagonal warning accent
        d.rectangle([(0, 0), (width, 80)], fill=cfg["primary"] + (255,))
        d.text((40, 20), "★ TECH DISCOVERY LOG ★", fill=(0, 0, 0, 255))
        # Brutalist thick border frame
        d.rectangle([(30, 110), (width - 30, height - 110)], outline=cfg["primary"] + (255,), width=8)

    elif template_key == "cinematic_dark":
        # Cinemascope Letterbox bars
        bar_height = 140
        d.rectangle([(0, 0), (width, bar_height)], fill=(0, 0, 0, 255))
        d.rectangle([(0, height - bar_height), (width, height)], fill=(0, 0, 0, 255))
        # Subtle vignette border
        d.rectangle([(40, bar_height + 20), (width - 40, height - bar_height - 20)], outline=(35, 30, 25, 90), width=2)

    return im
