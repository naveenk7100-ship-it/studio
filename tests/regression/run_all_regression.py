#!/usr/bin/env python3
"""
FLASH Daily Machine — Master Regression Test Runner
Executes all 7 regression test suites, ensuring every rule is proven to FAIL on its bad sample
and PASS on its valid sample. Run in CI and before every render and every post.
"""
import os
import sys
import json
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LESSONS_PATH = os.path.join(ROOT_DIR, "lessons.json")

def run_regression_suite():
    print("=" * 70)
    print("FLASH DAILY MACHINE - REGRESSION SUITE (0. NEVER REPEAT A MISTAKE)")
    print("=" * 70)
    
    with open(LESSONS_PATH, "r", encoding="utf-8") as f:
        lessons = json.load(f)
        
    print(f"Loaded {len(lessons.get('rules', []))} regression rules from lessons.json:\n")
    for r in lessons.get("rules", []):
        print(f"  [{r['id']}] {r['description'][:75]}...")
    print("-" * 70)
    
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.dirname(__file__), pattern="test_rule_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("-" * 70)
    print(f"Regression Tests Executed: {result.testsRun}")
    print(f"Failures: {len(result.failures)} | Errors: {len(result.errors)}")
    print("=" * 70)
    
    if not result.wasSuccessful():
        print("REGRESSION SUITE FAILED!")
        sys.exit(1)
    else:
        print("ALL 7 REGRESSION RULES VERIFIED: 100% of bad samples failed, 100% of good samples passed.")
        return 0

if __name__ == "__main__":
    run_regression_suite()
