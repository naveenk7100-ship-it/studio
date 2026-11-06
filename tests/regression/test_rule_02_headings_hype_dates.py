#!/usr/bin/env python3
"""
Regression Test for RULE-02-NO-HYPE-NO-DATES:
Validates that on-screen video text contains:
- NO invented headings ('Hierarchical Task Decomposer', 'Neural Activation Vectors')
- NO unsourced claims ('4x higher throughput', 'viral', 'breakthrough')
- NO self-praise or internal labels ('Source Truth Gates: 100% Tested', 'Zero Hallucinations', 'VERIFIED', 'GROUNDED', 'TECHNICAL ESSAY TAKEAWAY', '[03/08]', 'WOW BEAT')
- NO chapter labels ('CHAPTER 01 - ...') or slide numbering
- NO dates anywhere inside the video.
"""
import unittest
import re

INVENTED_HEADINGS = [
    "hierarchical task decomposer",
    "neural activation vectors",
    "autonomous agent orchestrator",
    "quantum token synthesis"
]

UNSOURCED_HYPE_WORDS = [
    "4x higher throughput",
    "10x faster",
    "viral",
    "breakthrough",
    "insane speed",
    "game changer",
    "unbelievable"
]

INTERNAL_SELF_PRAISE_LABELS = [
    "source truth gates: 100% tested",
    "source truth gates",
    "zero hallucinations",
    "technical essay takeaway",
    "verified",
    "grounded",
    "wow beat",
    "[01/08]",
    "[02/08]",
    "[03/08]",
    "[04/08]"
]

CHAPTER_LABEL_PATTERN = r"(?i)\bchapter\s+\d+\b|\bscene\s+\d+\b|\bslide\s+\d+\b"
DATE_PATTERN = r"(?i)\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2}(st|nd|rd|th)?,\s+\d{4}\b|\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b202[0-9]-[0-1][0-9]-[0-3][0-9]\b|\breleased\s+on\b|\bdate:\b"

def validate_headings_hype_and_dates(on_screen_elements: list) -> dict:
    """Audits on-screen elements (titles, subtitles, cards) against Rule 2."""
    issues = []
    
    for item in on_screen_elements:
        text = item.lower().strip()
        
        # 1. Check invented headings
        for ih in INVENTED_HEADINGS:
            if ih in text:
                issues.append(f"Invented heading detected: '{item}' (matches '{ih}')")
                
        # 2. Check unsourced hype words
        for hw in UNSOURCED_HYPE_WORDS:
            if hw in text:
                issues.append(f"Unsourced hype claim detected: '{item}' (matches '{hw}')")
                
        # 3. Check internal labels / self-praise
        for sl in INTERNAL_SELF_PRAISE_LABELS:
            if sl in text:
                issues.append(f"Self-praise or internal label detected: '{item}' (matches '{sl}')")
                
        # 4. Check chapter / slide labels
        if re.search(CHAPTER_LABEL_PATTERN, text):
            issues.append(f"Chapter/slide label detected: '{item}'")
            
        # 5. Check dates inside video
        if re.search(DATE_PATTERN, text):
            issues.append(f"Date detected inside video element: '{item}'")
            
    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "checked_elements": len(on_screen_elements)
    }


class TestRule02HeadingsHypeDates(unittest.TestCase):

    def test_bad_sample_fails(self):
        """Demonstrates that past bad sample with chapter label, date, hype, and self-praise FAILS."""
        bad_sample = [
            "CHAPTER 01 - Hierarchical Task Decomposer",
            "Source Truth Gates: 100% Tested [03/08]",
            "4x higher throughput breakthrough engine",
            "Released on November 4, 2026"
        ]
        result = validate_headings_hype_and_dates(bad_sample)
        self.assertFalse(result["passed"], "Bad sample MUST fail validation")
        self.assertGreaterEqual(len(result["issues"]), 4)
        print(f"\n[RULE-02] Verified Bad Sample Fails (Detected {len(result['issues'])} defects): {result['issues']}")

    def test_good_sample_passes(self):
        """Demonstrates that clean, factual, technical editorial copy PASSES."""
        good_sample = [
            "DEEPSEEK SUPERAGENT",
            "HIERARCHICAL REASONING ARCHITECTURE",
            "SUB-AGENT DISPATCH & MEMORY COMPACTION",
            "TRY IT IN CLAUDE CODE"
        ]
        result = validate_headings_hype_and_dates(good_sample)
        self.assertTrue(result["passed"], f"Good sample MUST pass: {result['issues']}")
        print(f"[RULE-02] Verified Good Sample Passes: {result['checked_elements']} elements verified clean.")


if __name__ == "__main__":
    unittest.main()
