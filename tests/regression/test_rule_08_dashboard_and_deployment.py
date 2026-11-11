import os
import json
import subprocess
import unittest

ROOT = r"C:\Users\navee\OneDrive\Desktop\studio"

class TestRule08DashboardAndDeployment(unittest.TestCase):
    def setUp(self):
        self.docs_dir = os.path.join(ROOT, "docs")
        self.review_html = os.path.join(self.docs_dir, "review", "index.html")
        self.review_json = os.path.join(self.docs_dir, "review", "review_data.json")
        self.videos_dir = os.path.join(self.docs_dir, "videos")

    def test_dashboard_file_exists(self):
        self.assertTrue(os.path.exists(self.review_html), "docs/review/index.html must exist")

    def test_no_invented_stars_or_fake_badges(self):
        with open(self.review_html, "r", encoding="utf-8") as f:
            html = f.read()

        # Banned invented numbers mentioned by user
        banned_invented = ["37,200", "45,100", "18,900", "Zero Interleaving", "Installed 0 dependencies"]
        for b in banned_invented:
            self.assertNotIn(b, html, f"Invented/unsupported string '{b}' found in review dashboard")

        # Banned fake badges
        banned_badges = ["ZERO-HALLUCINATION", "ZERO HALLUCINATIONS"]
        for b in banned_badges:
            self.assertNotIn(b, html, f"Fake badge '{b}' found in review dashboard")

    def test_review_data_sync(self):
        if not os.path.exists(self.review_json):
            self.skipTest("review_data.json not yet generated")
        with open(self.review_json, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("videos", data)
        self.assertIn("v7_tools", data["videos"])
        self.assertIn("v7_discovery", data["videos"])

    def test_deployed_videos_exist_and_audited(self):
        for vid_name in ["reel_v7_tools_720p.mp4", "reel_v7_discovery_720p.mp4"]:
            vid_path = os.path.join(self.videos_dir, vid_name)
            if not os.path.exists(vid_path):
                continue
            self.assertGreater(os.path.getsize(vid_path), 1_000_000, f"{vid_name} is too small (<1MB)")

            # Check audit json exists and has ok: true
            audit_p = vid_path + ".audit.json"
            if os.path.exists(audit_p):
                with open(audit_p, "r", encoding="utf-8") as f:
                    aud = json.load(f)
                failed = [c["name"] for c in aud.get("checks", []) if not c.get("ok")]
                self.assertEqual(len(failed), 0, f"Audit failed for {vid_name}: {failed}")

if __name__ == "__main__":
    unittest.main()
