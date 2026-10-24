"""Interpreter tests — deterministic fallback + cache + citation verification, no network."""
import unittest
from unittest.mock import patch

from phoenix import interpretation as it


WORKS = {"drug": "Canakinumab", "indication": "juvenile idiopathic arthritis", "target": "IL1B",
         "axis": "Immune", "cohens_d": 1.066, "verdict": "confirmed",
         "known_outcome": "works", "triangulation_score": 0.779}
FAILED = {"drug": "Rituximab", "indication": "lupus nephritis", "target": "MS4A1",
          "axis": "Hematologic", "cohens_d": -0.26, "verdict": "refuted",
          "known_outcome": "failed", "triangulation_score": 0.683}


class DeterministicTest(unittest.TestCase):
    def test_template_rationale_no_llm(self):
        # No PHOENIX_INTERPRET_LIVE -> deterministic template, never raises, no network.
        r = it.interpret(WORKS, use_cache=False)
        self.assertEqual(r["source"], "template")
        self.assertIn("Immune", r["rationale"])
        self.assertIsNone(r["failure_mode"])           # a "works" + confirmed case has no failure mode

    def test_failure_mode_for_failed_case(self):
        r = it.interpret(FAILED, use_cache=False)
        self.assertIsNotNone(r["failure_mode"])         # failed -> hypothesis emitted
        self.assertIn("MS4A1", r["failure_mode"])


class LiveAndCacheTest(unittest.TestCase):
    def test_llm_path_verifies_citations_and_caches(self):
        fake = {"rationale": "IL-1b drives sJIA.", "failure_mode": None,
                "citations": ["PMID:123", "PMID:999"]}   # 999 not in evidence -> dropped
        with patch.dict("os.environ", {"PHOENIX_INTERPRET_LIVE": "1"}), \
             patch.object(it, "_retrieve", return_value=("evidence PMID:123", ["PMID:123"])), \
             patch.object(it.llm, "complete_json", return_value=fake):
            r = it.interpret({**WORKS, "drug": "TestDrugZ"}, use_cache=False)
        self.assertEqual(r["source"], "llm")
        self.assertEqual(r["citations"], ["PMID:123"])   # hallucinated 999 verified out
        it._cache_path({**WORKS, "drug": "TestDrugZ"}).unlink(missing_ok=True)

    def test_llm_failure_degrades_to_template(self):
        with patch.dict("os.environ", {"PHOENIX_INTERPRET_LIVE": "1"}), \
             patch.object(it, "_retrieve", return_value=("", [])), \
             patch.object(it.llm, "complete_json", side_effect=RuntimeError("no key")):
            r = it.interpret({**FAILED, "drug": "TestDrugY"}, use_cache=False)
        self.assertEqual(r["source"], "template")        # never raises


if __name__ == "__main__":
    unittest.main()
