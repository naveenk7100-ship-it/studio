#!/usr/bin/env python3
"""
Regression Test for RULE-04-NUMBER-CONSISTENCY:
Validates that:
- Numbers agree inside one video and between video, Pages, and caption.
- Counters do not show 0 as a shot.
- Screenshot URL bars contain the exact repo URL (not org page or missing path).
- Cookie banners are completely absent in captures.
"""
import unittest
import re

def validate_number_consistency_and_captures(
    video_numbers: list,
    pages_numbers: list,
    caption_numbers: list,
    counter_shots: list,
    screenshot_url_bars: list,
    captured_image_ocr_texts: list
) -> dict:
    issues = []
    
    # 1. Number consistency
    # Compare key metrics across surfaces
    v_set = set(str(n) for n in video_numbers)
    p_set = set(str(n) for n in pages_numbers)
    c_set = set(str(n) for n in caption_numbers)
    
    # Check if numbers declared in video match caption & pages
    for n in v_set:
        if n not in p_set:
            issues.append(f"Number '{n}' present in video but missing in Pages essay")
        if n not in c_set:
            issues.append(f"Number '{n}' present in video but missing in caption")
            
    # 2. Counters that show 0 as a shot
    for shot in counter_shots:
        val = shot.get("value", None)
        is_hero_shot = shot.get("is_hero_shot", False)
        if (val == 0 or val == "0" or val == "0k" or val == "$0") and is_hero_shot:
            issues.append(f"Counter shows 0 as a hero shot: '{shot}'")
            
    # 3. Screenshot URL bars
    for url_info in screenshot_url_bars:
        url = url_info.get("url", "")
        expected_repo = url_info.get("expected_repo", "")
        # Flag if org page instead of repo or path truncated
        if url.rstrip("/").count("/") < 4 and "github.com" in url:
            issues.append(f"Screenshot URL bar shows org/profile page instead of repo: '{url}'")
        elif expected_repo and expected_repo.lower() not in url.lower():
            issues.append(f"Wrong repo URL in screenshot URL bar: '{url}' (expected '{expected_repo}')")
            
    # 4. Cookie banners
    cookie_terms = ["accept cookies", "we use cookies", "cookie preferences", "manage cookies", "privacy choices"]
    for idx, text in enumerate(captured_image_ocr_texts):
        t_low = text.lower()
        for ct in cookie_terms:
            if ct in t_low:
                issues.append(f"Cookie banner detected in capture #{idx+1}: matches '{ct}'")
                
    return {
        "passed": len(issues) == 0,
        "issues": issues
    }


class TestRule04NumberConsistency(unittest.TestCase):

    def test_bad_sample_fails(self):
        """Demonstrates that past bad sample with mismatched numbers, 0-counter shot, org URL, and cookie banner FAILS."""
        video_nums = ["12000", "450"]
        pages_nums = ["15000", "450"] # 12000 vs 15000 mismatch
        caption_nums = ["10000"]      # mismatch
        counter_shots = [{"name": "stars_counter", "value": 0, "is_hero_shot": True}]
        screenshot_urls = [{"url": "https://github.com/vllm-project", "expected_repo": "vllm-project/vllm"}] # org page
        captures_ocr = ["Welcome to our website. We use cookies to improve your experience. Accept Cookies."]
        
        result = validate_number_consistency_and_captures(
            video_nums, pages_nums, caption_nums, counter_shots, screenshot_urls, captures_ocr
        )
        self.assertFalse(result["passed"], "Bad sample MUST fail validation")
        self.assertGreaterEqual(len(result["issues"]), 4)
        print(f"\n[RULE-04] Verified Bad Sample Fails (Detected {len(result['issues'])} defects): {result['issues']}")

    def test_good_sample_passes(self):
        """Demonstrates that consistent metrics, exact repo URLs, and clean captures PASS."""
        video_nums = ["28400", "600"]
        pages_nums = ["28400", "600", "2026"]
        caption_nums = ["28400", "600"]
        counter_shots = [{"name": "stars_counter", "value": 28400, "is_hero_shot": True}]
        screenshot_urls = [{"url": "https://github.com/vllm-project/vllm", "expected_repo": "vllm-project/vllm"}]
        captures_ocr = ["vLLM: Easy, fast, and cheap LLM serving for everyone. pip install vllm."]
        
        result = validate_number_consistency_and_captures(
            video_nums, pages_nums, caption_nums, counter_shots, screenshot_urls, captures_ocr
        )
        self.assertTrue(result["passed"], f"Good sample MUST pass: {result['issues']}")
        print("[RULE-04] Verified Good Sample Passes: Numbers, repo URLs, and clean captures verified.")


if __name__ == "__main__":
    unittest.main()
