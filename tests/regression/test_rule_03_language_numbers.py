#!/usr/bin/env python3
"""
Regression Test for RULE-03-LANGUAGE-NUMBERS:
Validates that on-screen video text contains:
- NO Telugu script Unicode characters (\u0C00-\u0C7F)
- NO relative time words in English or romanized Telugu ('yesterday', 'ninna', 'today', 'last week', 'repu', 'tomorrow')
- NO spelled-out numbers ('five' -> '5', 'hundred' -> '100').
"""
import unittest
import re
import sys

# Ensure UTF-8 console output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

RELATIVE_TIME_WORDS = [
    r"\byesterday\b",
    r"\bninna\b",
    r"\btoday\b",
    r"\beeroju\b",
    r"\biroju\b",
    r"\blast week\b",
    r"\bmonna\b",
    r"\btomorrow\b",
    r"\brepu\b"
]

SPELLED_OUT_NUMBERS = [
    r"\bone\b", r"\btwo\b", r"\bthree\b", r"\bfour\b", r"\bfive\b",
    r"\bsix\b", r"\bseven\b", r"\beight\b", r"\bnine\b", r"\bten\b",
    r"\bhundred\b", r"\bthousand\b"
]

def validate_language_and_numbers(on_screen_elements: list) -> dict:
    """Audits typography and linguistics against Rule 3."""
    issues = []
    
    for item in on_screen_elements:
        # 1. Telugu Unicode characters check
        telugu_chars = re.findall(r"[\u0C00-\u0C7F]", item)
        if telugu_chars:
            issues.append(f"Telugu script Unicode detected: '{item}' ({len(telugu_chars)} chars)")
            
        text_lower = item.lower()
        
        # 2. Relative time words check
        for rtw in RELATIVE_TIME_WORDS:
            if re.search(rtw, text_lower):
                clean_rtw = rtw.replace(r"\b", "")
                issues.append(f"Relative time word detected: '{clean_rtw}' in '{item}'")
                
        # 3. Spelled-out numbers check
        for son in SPELLED_OUT_NUMBERS:
            # Allow common English phrases like "one creator" only if allowed by schema,
            # but rule strictly says "spelled-out numbers (use digits)".
            # Let's catch standalone spelled out numbers.
            if re.search(son, text_lower):
                clean_son = son.replace(r"\b", "")
                # Exclude compound words like "someone"
                issues.append(f"Spelled-out number detected: '{clean_son}' in '{item}' (use digits instead)")
                
    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "checked_elements": len(on_screen_elements)
    }


class TestRule03LanguageNumbers(unittest.TestCase):

    def test_bad_sample_fails(self):
        """Demonstrates that past bad sample with Telugu script, relative time words, and spelled out numbers FAILS."""
        bad_sample = [
            "నిన్న విడుదలైన కొత్త మోడల్", # Telugu Unicode script
            "ninna release aina tool",       # Romanized Telugu relative time word
            "yesterday we tested three tools" # English relative time word + spelled out number
        ]
        result = validate_language_and_numbers(bad_sample)
        self.assertFalse(result["passed"], "Bad sample MUST fail validation")
        self.assertGreaterEqual(len(result["issues"]), 3)
        print(f"\n[RULE-03] Verified Bad Sample Fails (Detected {len(result['issues'])} defects): {result['issues']}")

    def test_good_sample_passes(self):
        """Demonstrates that pure Latin Tenglish with digits and absolute context PASSES."""
        good_sample = [
            "3 AI TOOLS TESTED",
            "VLLM ENGINE LO 2X SPEED",
            "TERMINAL LO TRY CHEYYANDI",
            "600 TOKENS PER SECOND"
        ]
        result = validate_language_and_numbers(good_sample)
        self.assertTrue(result["passed"], f"Good sample MUST pass: {result['issues']}")
        print(f"[RULE-03] Verified Good Sample Passes: {result['checked_elements']} elements verified clean.")


if __name__ == "__main__":
    unittest.main()
