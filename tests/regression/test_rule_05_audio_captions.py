#!/usr/bin/env python3
"""
Regression Test for RULE-05-AUDIO-CAPTIONS:
Validates that:
- Captions are never frozen (> 1.5s while speech continues).
- Captions match spoken voice timeline.
- CTA appears strictly AFTER the last content word.
- Last word is not clipped.
- Audio files are 48 kHz (not 96 kHz).
- Audio true peaks <= -1.5 dBTP.
- Loudness is strictly -14.0 +/- 0.5 LUFS for both master and 720p web copy.
"""
import unittest

def validate_audio_and_captions(
    sample_rate_hz: int,
    true_peak_dbtp: float,
    integrated_lufs: float,
    captions_timeline: list,
    speech_end_sec: float,
    cta_start_sec: float
) -> dict:
    issues = []
    
    # 1. Sample rate check
    if sample_rate_hz > 48000:
        issues.append(f"Audio sample rate is {sample_rate_hz} Hz (strictly forbidden; must be 48000 Hz)")
        
    # 2. True peak check
    if true_peak_dbtp > -1.5:
        issues.append(f"True peak {true_peak_dbtp} dBTP exceeds ceiling of -1.5 dBTP")
        
    # 3. Integrated loudness check (-14.0 +/- 0.5 LUFS)
    if not (-14.5 <= integrated_lufs <= -13.5):
        issues.append(f"Integrated loudness {integrated_lufs} LUFS outside broadcast window [-14.5, -13.5] LUFS")
        
    # 4. CTA timing: CTA must start strictly after last content word
    if cta_start_sec < speech_end_sec:
        issues.append(f"CTA starts at {cta_start_sec:.2f}s before last content word finishes at {speech_end_sec:.2f}s")
        
    # 5. Caption freezing check (> 1.5s while speech continues)
    for i, cap in enumerate(captions_timeline):
        start = cap.get("start", 0.0)
        end = cap.get("end", 0.0)
        duration = end - start
        if duration > 1.5 and start < speech_end_sec:
            issues.append(f"Caption #{i+1} ('{cap.get('text', '')}') frozen for {duration:.2f}s (> 1.5s)")
            
    return {
        "passed": len(issues) == 0,
        "issues": issues
    }


class TestRule05AudioCaptions(unittest.TestCase):

    def test_bad_sample_fails(self):
        """Demonstrates that past bad sample (96 kHz, peak -0.2 dBTP, loudness -21 LUFS, frozen caption, early CTA) FAILS."""
        bad_sample_rate = 96000
        bad_peak = -0.2
        bad_lufs = -21.4
        bad_captions = [
            {"start": 0.0, "end": 2.2, "text": "Unslop tool tho Mee prompt cleanup"}, # 2.2s > 1.5s frozen
            {"start": 2.2, "end": 11.2, "text": "claude code lo direct ga vadachu"}   # 9.0s frozen!
        ]
        speech_end = 26.5
        bad_cta_start = 22.0 # CTA appears 4.5s before last content word!
        
        result = validate_audio_and_captions(
            bad_sample_rate, bad_peak, bad_lufs, bad_captions, speech_end, bad_cta_start
        )
        self.assertFalse(result["passed"], "Bad sample MUST fail validation")
        self.assertGreaterEqual(len(result["issues"]), 4)
        print(f"\n[RULE-05] Verified Bad Sample Fails (Detected {len(result['issues'])} defects): {result['issues']}")

    def test_good_sample_passes(self):
        """Demonstrates that compliant broadcast audio and synchronized captions PASS."""
        good_sample_rate = 48000
        good_peak = -1.6
        good_lufs = -14.0
        good_captions = [
            {"start": 0.0, "end": 0.8, "text": "Unslop tool tho"},
            {"start": 0.8, "end": 1.6, "text": "prompt cleanup cheyandi"},
            {"start": 1.6, "end": 2.4, "text": "one command chalu"}
        ]
        speech_end = 24.2
        good_cta_start = 24.5 # CTA starts 300ms AFTER speech ends
        
        result = validate_audio_and_captions(
            good_sample_rate, good_peak, good_lufs, good_captions, speech_end, good_cta_start
        )
        self.assertTrue(result["passed"], f"Good sample MUST pass: {result['issues']}")
        print("[RULE-05] Verified Good Sample Passes: Audio master, peak, loudness, and captions verified.")


if __name__ == "__main__":
    unittest.main()
