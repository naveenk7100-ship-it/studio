#!/usr/bin/env python3
"""
Regression Test for RULE-06-VISUAL-MOTION-NO-REPEAT:
Validates that:
- Captured images/crops are never repeated (perceptual-hash uniqueness).
- Text contrast is >= 4.5:1 with no ghosted text.
- Hero visual is >= 45% of height with no empty dark areas.
- Motion metric: median MAD >= 1.0, at least one burst second > 20, <= 3 consecutive seconds < 0.5.
- Phase-correlation jitter variance is <= 0.05 px^2.
- Top-right link chip is forbidden (lower-third source domain only while capture is on screen).
"""
import unittest

def validate_visual_motion_and_composition(
    image_perceptual_hashes: list,
    min_contrast_ratio: float,
    hero_visual_height_pct: float,
    per_second_motion_mad: list,
    jitter_variance_px2: float,
    has_top_right_link_chip: bool
) -> dict:
    issues = []
    
    # 1. Perceptual hash uniqueness check (no repeated captures/crops)
    seen_hashes = {}
    for idx, phash in enumerate(image_perceptual_hashes):
        if phash in seen_hashes:
            issues.append(f"Repeated image detected: capture #{idx+1} has identical hash '{phash}' to capture #{seen_hashes[phash]+1}")
        else:
            seen_hashes[phash] = idx
            
    # 2. Text contrast ratio (WCAG AA >= 4.5:1)
    if min_contrast_ratio < 4.5:
        issues.append(f"Text contrast {min_contrast_ratio:.2f}:1 fails WCAG AA minimum 4.5:1 (unreadable/ghosted text)")
        
    # 3. Hero visual coverage (>= 45% of height, no empty dark void)
    if hero_visual_height_pct < 45.0:
        issues.append(f"Hero visual coverage is {hero_visual_height_pct:.1f}% (< 45.0% minimum; excessive dark void)")
        
    # 4. Motion metric targets: median >= 1.0, burst second > 20, max 3 consecutive seconds < 0.5
    if len(per_second_motion_mad) > 0:
        import numpy as np
        med_motion = float(np.median(per_second_motion_mad))
        max_motion = float(np.max(per_second_motion_mad))
        
        if med_motion < 1.0:
            issues.append(f"Median 1s motion MAD is {med_motion:.2f} (< 1.0 target)")
        if max_motion <= 20.0:
            issues.append(f"No burst second exceeds 20.0 MAD (peak motion was {max_motion:.2f})")
            
        consecutive_low = 0
        max_consecutive_low = 0
        for m in per_second_motion_mad:
            if m < 0.5:
                consecutive_low += 1
                if consecutive_low > max_consecutive_low:
                    max_consecutive_low = consecutive_low
            else:
                consecutive_low = 0
                
        if max_consecutive_low > 3:
            issues.append(f"Detected {max_consecutive_low} consecutive static seconds with motion < 0.5 (max allowed: 3)")
            
    # 5. Jitter variance (<= 0.05 px^2)
    if jitter_variance_px2 > 0.05:
        issues.append(f"Phase-correlation jitter variance {jitter_variance_px2:.4f} px^2 exceeds ceiling 0.05 px^2 (camera shake detected)")
        
    # 6. Top-right link chip forbidden
    if has_top_right_link_chip:
        issues.append("Forbidden top-right link chip detected (must use source-domain lower-third without dates)")
        
    return {
        "passed": len(issues) == 0,
        "issues": issues
    }


class TestRule06VisualMotionNoRepeat(unittest.TestCase):

    def test_bad_sample_fails(self):
        """Demonstrates that past bad sample with repeated image, low motion, low contrast, and top-right chip FAILS."""
        bad_hashes = ["hash_abc123", "hash_def456", "hash_abc123"] # duplicate hash!
        bad_contrast = 2.4 # ghosted text
        bad_hero_height = 32.0 # large dark void
        bad_motion = [0.4, 0.3, 0.2, 0.1, 0.4, 0.3, 0.5, 0.6] # 6 consecutive seconds < 0.5, max 0.6, median 0.35
        bad_jitter = 0.12 # camera shake
        has_top_right_chip = True
        
        result = validate_visual_motion_and_composition(
            bad_hashes, bad_contrast, bad_hero_height, bad_motion, bad_jitter, has_top_right_chip
        )
        self.assertFalse(result["passed"], "Bad sample MUST fail validation")
        self.assertGreaterEqual(len(result["issues"]), 5)
        print(f"\n[RULE-06] Verified Bad Sample Fails (Detected {len(result['issues'])} defects): {result['issues']}")

    def test_good_sample_passes(self):
        """Demonstrates that distinct images, strong contrast, 3D camera motion, and clean framing PASS."""
        good_hashes = ["hash_01_repo", "hash_02_docs", "hash_03_telemetry", "hash_04_terminal"]
        good_contrast = 7.8
        good_hero_height = 58.0
        good_motion = [1.2, 1.4, 1.1, 24.5, 1.3, 1.5, 1.2, 0.9] # median 1.25, burst 24.5 > 20
        good_jitter = 0.012
        has_top_right_chip = False
        
        result = validate_visual_motion_and_composition(
            good_hashes, good_contrast, good_hero_height, good_motion, good_jitter, has_top_right_chip
        )
        self.assertTrue(result["passed"], f"Good sample MUST pass: {result['issues']}")
        print("[RULE-06] Verified Good Sample Passes: Image uniqueness, contrast, and 3D motion verified.")


if __name__ == "__main__":
    unittest.main()
