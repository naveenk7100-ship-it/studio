#!/usr/bin/env python3
"""
Regression Test for RULE-01-COMMANDS:
Validates that commands are verifiable from repo documentation,
flags fake packages ('npx @damir/unslop'), mismatched model commands ('qwen2.5' under Qwen 3.6),
unsafe flags ('--dangerously-skip-permissions'), and broken mid-token words.
"""
import unittest
import re

def validate_commands(commands_list: list, repo_readme_text: str, model_context: str = "") -> dict:
    """Checks command validity against documentation and safety rules."""
    unsafe_flags = ["--dangerously-skip-permissions", "--no-verify", "--force-all"]
    fake_patterns = [r"npx\s+@damir/unslop", r"npm\s+i\s+-g\s+@damir/unslop"]
    
    issues = []
    for cmd in commands_list:
        # 1. Unsafe flags
        for flag in unsafe_flags:
            if flag in cmd:
                issues.append(f"Unsafe flag detected: {flag} in '{cmd}'")
                
        # 2. Fake packages
        for fp in fake_patterns:
            if re.search(fp, cmd, re.IGNORECASE):
                issues.append(f"Fake or unverifiable command detected: '{cmd}'")
                
        # 3. Model mismatch
        if "qwen 3.6" in model_context.lower() and "qwen2.5" in cmd.lower():
            issues.append(f"Mismatched model command: '{cmd}' for context '{model_context}'")
            
        # 4. Broken mid-token hyphenation or corrupted word
        if re.search(r"\b[a-zA-Z]+-\s+[a-zA-Z]+\b", cmd) or re.search(r"\b[a-zA-Z]{1,2}\s+[a-zA-Z]{1,2}\s+[a-zA-Z]{1,2}\b", cmd):
            issues.append(f"Broken mid-token or corrupted words in command: '{cmd}'")
            
        # 5. Must exist or be entailed by documentation
        clean_cmd = cmd.strip()
        if clean_cmd not in repo_readme_text:
            # check normalized
            norm_cmd = re.sub(r"\s+", " ", clean_cmd).lower()
            norm_readme = re.sub(r"\s+", " ", repo_readme_text).lower()
            if norm_cmd not in norm_readme:
                issues.append(f"Command not found verbatim in documentation: '{cmd}'")
                
    return {
        "passed": len(issues) == 0,
        "issues": issues,
        "checked_commands": len(commands_list)
    }


class TestRule01Commands(unittest.TestCase):

    def test_bad_sample_fails(self):
        """Demonstrates that past bad sample with fake npx package and unsafe flags FAILS."""
        bad_sample_commands = [
            "npx @damir/unslop --dangerously-skip-permissions",
            "ollama run qwen2.5-coder:32b" # while context is Qwen 3.6
        ]
        readme_docs = (
            "To install unslop:\n"
            "git clone https://github.com/heydamir/unslop\n"
            "copy skills/unslop into ~/.claude/skills\n"
            "run /unslop inside Claude Code"
        )
        result = validate_commands(bad_sample_commands, readme_docs, model_context="Qwen 3.6 Interpretability")
        self.assertFalse(result["passed"], "Bad sample MUST fail validation")
        self.assertGreaterEqual(len(result["issues"]), 3)
        print(f"\n[RULE-01] Verified Bad Sample Fails (Detected {len(result['issues'])} defects): {result['issues']}")

    def test_good_sample_passes(self):
        """Demonstrates that genuine documentation commands PASS."""
        good_sample_commands = [
            "git clone https://github.com/heydamir/unslop",
            "/unslop"
        ]
        readme_docs = (
            "To install unslop:\n"
            "git clone https://github.com/heydamir/unslop\n"
            "copy skills/unslop into ~/.claude/skills\n"
            "run /unslop inside Claude Code"
        )
        result = validate_commands(good_sample_commands, readme_docs, model_context="unslop")
        self.assertTrue(result["passed"], f"Good sample MUST pass: {result['issues']}")
        print(f"[RULE-01] Verified Good Sample Passes: {result['checked_commands']} commands verified verbatim.")


if __name__ == "__main__":
    unittest.main()
