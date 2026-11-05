"""
Generate clean, high-resolution FLASH profile avatar for assets/brand/profile.png
1024x1024 RGBA image with dark cybernetic background, cyan neon glow, electric bolt polygon, and subtle radial gradient.
"""

import os
from PIL import Image, ImageDraw, ImageFilter

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
BRAND_DIR = os.path.join(ROOT, "assets", "brand")
ENG_BRAND_DIR = os.path.join(ROOT, "engine", "public", "brand")
os.makedirs(BRAND_DIR, exist_ok=True)
os.makedirs(ENG_BRAND_DIR, exist_ok=True)

size = (1024, 1024)
img = Image.new("RGBA", size, (10, 14, 23, 255))
draw = ImageDraw.Draw(img)

# Outer circle guide / subtle boundary
center = (512, 512)
radius = 480

# Radial gradient circle
for r in range(radius, 0, -2):
    frac = r / radius
    # Dark navy to vibrant deep blue
    r_val = int(8 + (1 - frac) * 12)
    g_val = int(14 + (1 - frac) * 35)
    b_val = int(28 + (1 - frac) * 75)
    draw.ellipse([512 - r, 512 - r, 512 + r, 512 + r], fill=(r_val, g_val, b_val, 255))

# Outer neon cyan ring
draw.ellipse([512 - 470, 512 - 470, 512 + 470, 512 + 470], outline=(0, 229, 255, 180), width=6)
draw.ellipse([512 - 455, 512 - 455, 512 + 455, 512 + 455], outline=(0, 229, 255, 80), width=2)

# Create lightning bolt layer for neon glow
glow_layer = Image.new("RGBA", size, (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_layer)

# Stylized Lightning Bolt polygon coordinates (sharp, dynamic)
bolt_pts = [
    (540, 160),  # top point
    (380, 510),  # mid left
    (490, 510),  # inner notch
    (430, 840),  # bottom tip
    (670, 440),  # mid right
    (540, 440),  # inner right
]

# Draw soft cyan glow underneath
for w_offset in [30, 20, 10]:
    glow_draw.polygon(bolt_pts, fill=(0, 229, 255, 50))
glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(18))

# Composite glow
img = Image.alpha_composite(img, glow_layer)
draw = ImageDraw.Draw(img)

# Solid cyan bolt core with gradient/highlight
draw.polygon(bolt_pts, fill=(0, 229, 255, 255))

# Inner white highlight polygon for metallic electric shine
shine_pts = [
    (535, 200),
    (420, 490),
    (500, 490),
    (460, 750),
    (620, 460),
    (535, 460),
]
draw.polygon(shine_pts, fill=(255, 255, 255, 190))

# Save to assets/brand/profile.png and engine/public/brand/profile.png
out1 = os.path.join(BRAND_DIR, "profile.png")
out2 = os.path.join(ENG_BRAND_DIR, "profile.png")
img.save(out1, "PNG")
img.save(out2, "PNG")

print(f"Generated brand avatar: {out1} ({os.path.getsize(out1)} bytes)")
print(f"Copied brand avatar: {out2} ({os.path.getsize(out2)} bytes)")
