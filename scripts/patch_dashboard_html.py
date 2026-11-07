"""
Patch docs/review/index.html to inject the 12-second Style Test Showcase section.
"""

import os

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"
HTML_PATH = os.path.join(ROOT, "docs", "review", "index.html")

target = """        <!-- ==================== TAB 1: TODAY'S REELS ==================== -->
        <div id="tab-today" class="tab-panel active">
            <!-- Selector Chips -->"""

replacement = """        <!-- ==================== TAB 1: TODAY'S REELS ==================== -->
        <div id="tab-today" class="tab-panel active">
            <!-- ==================== 12-SECOND STYLE TEST SHOWCASE ==================== -->
            <div class="glass-card" style="margin-bottom: 24px; border: 2px solid #00E5FF; background: rgba(11, 37, 46, 0.4);">
                <div class="card-kicker" style="color: #00E5FF;">STEP 1: 12-SECOND VISUAL OVERHAUL STYLE TEST • wheresryan22 / anatomy</div>
                <h2 style="font-size: 22px; margin: 8px 0 12px 0;">3 Cinematic Explainer Look Variants</h2>
                <p style="font-size: 14px; color: var(--text-secondary); margin-bottom: 16px;">
                    Review the 3 lighting & depth variants below (voice + word-by-word captions + ducked music pulse + scene-matched foley). Pick your preferred look before we scale to full 28s reels.
                </p>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
                    <!-- Variant A -->
                    <div style="background: rgba(4, 18, 23, 0.85); border: 1.5px solid #00E5FF; border-radius: 12px; padding: 14px;">
                        <div style="font-weight: 800; color: #00E5FF; margin-bottom: 4px; font-size: 16px;">Variant A: Deep Teal Studio</div>
                        <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 10px;">Volumetric light shafts • Cyan accents • Exploded view</div>
                        <div class="video-box" style="margin-bottom: 10px;">
                            <video src="../videos/style_test_variant_a_720p.mp4" controls playsinline preload="metadata" poster="../style_test_variant_a_contact_sheet.png"></video>
                        </div>
                        <div style="font-size: 12px; color: var(--text-secondary);">
                            MAD: <b>3.40</b> | Empty: <b>23.1%</b> | Loudness: <b>-13.9 LUFS</b>
                        </div>
                    </div>
                    <!-- Variant B -->
                    <div style="background: rgba(8, 22, 42, 0.85); border: 2px solid #E2B878; border-radius: 12px; padding: 14px; box-shadow: 0 0 20px rgba(226, 184, 120, 0.2);">
                        <div style="font-weight: 800; color: #E2B878; margin-bottom: 4px; font-size: 16px;">Variant B: Blueprint Drafting (Recommended)</div>
                        <div style="font-size: 12px; color: var(--text-secondary); margin-bottom: 10px;">Drafting board 3D • Sepia gold • Technical crosshairs</div>
                        <div class="video-box" style="margin-bottom: 10px;">
                            <video src="../videos/style_test_variant_b_720p.mp4" controls playsinline preload="metadata" poster="../style_test_variant_b_contact_sheet.png"></video>
                        </div>
                        <div style="font-size: 12px; color: #10B981; font-weight: 700;">
                            PASSES ALL GATES: MAD <b>3.29</b> | Empty: <b>16.1%</b> | <b>-13.9 LUFS</b>
                        </div>
                    </div>
                    <!-- Variant C -->
                    <div style="background: rgba(241, 245, 249, 0.98); color: #0F172A; border: 1.5px solid #059669; border-radius: 12px; padding: 14px;">
                        <div style="font-weight: 800; color: #059669; margin-bottom: 4px; font-size: 16px;">Variant C: Light Museum Vitrine</div>
                        <div style="font-size: 12px; color: #475569; margin-bottom: 10px;">Luminous gallery • Frosted acrylic 3D pedestal • Emerald</div>
                        <div class="video-box" style="margin-bottom: 10px;">
                            <video src="../videos/style_test_variant_c_720p.mp4" controls playsinline preload="metadata" poster="../style_test_variant_c_contact_sheet.png"></video>
                        </div>
                        <div style="font-size: 12px; color: #059669; font-weight: 700;">
                            MAD: <b>2.71</b> | Empty: <b>15.0%</b> | Loudness: <b>-13.9 LUFS</b>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Selector Chips -->"""

with open(HTML_PATH, "r", encoding="utf-8") as f:
    content = f.read()

if target in content:
    content = content.replace(target, replacement, 1)
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("SUCCESS: Injected Style Test showcase into docs/review/index.html")
else:
    print("Target not found. It may already be injected.")
