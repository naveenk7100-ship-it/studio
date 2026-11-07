"""
FLASH Content OS - Update Review Dashboard with 12-Second Style Test Showcase
Injects the 3 Style Test variants (Variant A, Variant B, Variant C) into docs/review/index.html
"""

import os
import sys
import json

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
HTML_PATH = os.path.join(ROOT, "docs", "review", "index.html")

STYLE_TESTS = [
    {
        "id": "variant_a",
        "title": "Style Test: Variant A",
        "topic": "Deep Teal Studio Aesthetic",
        "tagline": "Volumetric Light Shafts • Cyan #00E5FF • Exploded 3D Assembly",
        "web_video": "../videos/style_test_variant_a_720p.mp4",
        "sheet_img": "../style_test_variant_a_contact_sheet.png",
        "accent": "#00E5FF",
        "badges": ["12.0s STYLE TEST", "DEEP TEAL STUDIO", "3D EXPLODED VIEW", "-13.9 LUFS"],
        "description": "Deep teal studio (#041217 to #0B252E), electric cyan accents (#00E5FF), volumetric light sweeps, millimeter coordinate grid, Raptor 2 3D exploded view with parallax, typed monospace command, and active FLASH logo payoff."
    },
    {
        "id": "variant_b",
        "title": "Style Test: Variant B",
        "topic": "Warm Paper-and-Ink Blueprint",
        "tagline": "Drafting Board 3D • Sepia Drafting Gold #E2B878 • Architectural Ticks",
        "web_video": "../videos/style_test_variant_b_720p.mp4",
        "sheet_img": "../style_test_variant_b_contact_sheet.png",
        "accent": "#E2B878",
        "badges": ["12.0s STYLE TEST", "BLUEPRINT DRAFTING", "3D EXPLODED VIEW", "-13.9 LUFS"],
        "description": "Architectural drafting board (#08162A to #10335C), sepia drafting ink (#E2B878), millimeter technical crosshairs, measurement ticks, Raptor 2 deconstruction with mechanical callouts, typed command, and blueprint seal."
    },
    {
        "id": "variant_c",
        "title": "Style Test: Variant C",
        "topic": "Light Museum Vitrine Aesthetic",
        "tagline": "Luminous Gallery • Frosted Acrylic 3D Pedestal • Emerald #059669 Accents",
        "web_video": "../videos/style_test_variant_c_720p.mp4",
        "sheet_img": "../style_test_variant_c_contact_sheet.png",
        "accent": "#059669",
        "badges": ["12.0s STYLE TEST", "MUSEUM VITRINE", "3D EXPLODED VIEW", "-14.0 LUFS"],
        "description": "Luminous museum exhibition gallery (#F1F5F9 to #CBD5E1), directional studio key lighting, frosted acrylic vitrine pedestal, emerald precision callouts (#059669), high-contrast charcoal captions, and pristine gallery lockup."
    }
]

def update_html():
    if not os.path.exists(HTML_PATH):
        print(f"Error: {HTML_PATH} does not exist")
        return

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        html = f.read()

    # Create injection block
    json_block = json.dumps(STYLE_TESTS, indent=4)
    # Check if STYLE_TESTS already defined
    if "const STYLE_TESTS =" in html:
        print("STYLE_TESTS already present in dashboard HTML.")
    else:
        # Insert before const REELS =
        replacement = f"const STYLE_TESTS = {json_block};\n\n    const REELS ="
        html = html.replace("const REELS =", replacement)
        with open(HTML_PATH, "w", encoding="utf-8") as f:
            f.write(html)
        print("Updated dashboard with STYLE_TESTS data.")

if __name__ == "__main__":
    update_html()
