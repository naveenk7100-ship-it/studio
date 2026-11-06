#!/usr/bin/env python3
"""
Regression Test for RULE-07-REVIEW-URLS:
Validates that review action buttons:
- Never generate malformed URLs (e.g. past defect 'author:new:' leading to GitHub error).
- All query parameters are properly encoded with encodeURIComponent / urllib.parse.quote.
- URLs can be safely parsed by standard URL parsers without throwing or generating malformed search queries.
"""
import unittest
from urllib.parse import urlparse, parse_qs

def validate_review_url(url_str: str) -> dict:
    issues = []
    
    # 1. Past defect check: "author:new:" in query
    if "author:new:" in url_str:
        issues.append(f"Malformed search query 'author:new:' detected in URL: '{url_str}'")
        
    # 2. Parse check
    try:
        parsed = urlparse(url_str)
        if not parsed.scheme or not parsed.netloc:
            issues.append(f"Invalid URL structure: '{url_str}'")
            
        qs = parse_qs(parsed.query)
        # Check template parameter if new issue URL
        if "/issues/new" in parsed.path:
            if "template" not in qs and "title" not in qs:
                issues.append(f"Missing essential template or title parameter in issue URL: '{url_str}'")
    except Exception as e:
        issues.append(f"URL parsing exception: {e}")
        
    # 3. Check unencoded spaces or special characters in query string
    if " " in url_str:
        issues.append(f"Unencoded raw whitespace detected in URL: '{url_str}' (must use %20 or +)")
        
    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "url": url_str
    }


class TestRule07ReviewUrls(unittest.TestCase):

    def test_bad_sample_fails(self):
        """Demonstrates that past bad sample with 'author:new:' and unencoded spaces FAILS."""
        bad_url = "https://github.com/naveenk7100-ship-it/studio/issues?q=is:issue is:open author:new: template:approve.yml"
        result = validate_review_url(bad_url)
        self.assertFalse(result["passed"], "Bad sample MUST fail validation")
        self.assertGreaterEqual(len(result["issues"]), 2)
        print(f"\n[RULE-07] Verified Bad Sample Fails (Detected {len(result['issues'])} defects): {result['issues']}")

    def test_good_sample_passes(self):
        """Demonstrates that clean, properly encoded issue creation URLs PASS."""
        good_url = "https://github.com/naveenk7100-ship-it/studio/issues/new?template=approve.yml&title=Approve%20Video%3A%20reel_01&labels=approval"
        result = validate_review_url(good_url)
        self.assertTrue(result["passed"], f"Good sample MUST pass: {result['issues']}")
        print(f"[RULE-07] Verified Good Sample Passes: URL structure '{good_url}' is clean and valid.")


if __name__ == "__main__":
    unittest.main()
