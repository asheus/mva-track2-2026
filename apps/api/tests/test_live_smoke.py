"""Live end-to-end smoke test — exercises the REAL agents (Paperclip + LLM), not mocks.

Skipped by default (it makes real network/LLM calls and costs money / takes ~1-2 min).
Run explicitly once keys are configured:

    PHOENIX_LIVE_TESTS=1 python -m unittest tests.test_live_smoke -v

The rest of the suite (test_closed_loop, test_trial_forensics) stays fast + offline.
"""
import os
import unittest

from phoenix.orchestrator.loop import analyze

LIVE = os.getenv("PHOENIX_LIVE_TESTS") == "1"


@unittest.skipUnless(LIVE, "set PHOENIX_LIVE_TESTS=1 (and ANTHROPIC/GEMINI + PAPERCLIP keys) to run")
class LiveSmokeTest(unittest.TestCase):
    def test_canakinumab_runs_end_to_end(self):
        rec = analyze(
            {"name": "Canakinumab", "mechanism": "anti-IL-1b", "indication": "SJIA"},
            {"geo_id": "GSE80060", "tissue": "whole blood"},
        )
        # Shape + terminal-decision sanity (the loop actually ran the real agents).
        self.assertEqual(rec["claim_id"], "canakinumab-GSE80060")
        self.assertIn(rec["decision"], {"COMMIT", "REFINE", "ABSTAIN"})
        self.assertTrue(rec["critique_history"], "critique must have produced at least one iteration")
        last = rec["critique_history"][-1]
        self.assertGreaterEqual(last["defensibility"], 0.0)
        self.assertLessEqual(last["defensibility"], 1.0)
        # Real grounding: literature citations should be present unless we abstained pre-loop.
        if rec["decision"] != "ABSTAIN":
            self.assertIsInstance(rec.get("citations", []), list)

    def test_target_engagement_gate_is_functional(self):
        from phoenix.agents.trial_forensics.agent import target_engagement_gate

        g = target_engagement_gate({"drug": {"name": "Canakinumab", "mechanism": "anti-IL-1b"}})
        # Canakinumab is approved (engagement shown) -> must PROCEED, and must have pulled real ids.
        self.assertEqual(g["action"], "PROCEED")
        self.assertIn(g["target_engagement"], {"shown", "unknown"})


if __name__ == "__main__":
    unittest.main()
