"""Calibration logic tests — pure / no GEO data or network needed.

The full `run_calibration()` reads GEO matrices (gitignored), so it is exercised by the
live CLI (`python -m scripts.calibrate`), not here. These tests pin the two pieces that
must stay correct regardless of environment: the two-directional concordance rule and the
graceful-degrade behaviour of the Paperclip evidence helper without a key.
"""
import unittest
from unittest.mock import patch

from phoenix import calibration


class ConcordanceRuleTest(unittest.TestCase):
    def test_works_drug_concordant_only_when_confirmed(self):
        self.assertTrue(calibration.concordant("works", "confirmed"))
        self.assertFalse(calibration.concordant("works", "confirmed_weak"))
        self.assertFalse(calibration.concordant("works", "refuted"))
        self.assertFalse(calibration.concordant("works", None))

    def test_failed_drug_concordant_unless_confirmed(self):
        # The engine correctly NOT confirming a failed-indication drug is concordant.
        self.assertTrue(calibration.concordant("failed", "confirmed_weak"))
        self.assertTrue(calibration.concordant("failed", "refuted"))
        self.assertTrue(calibration.concordant("failed", None))
        self.assertFalse(calibration.concordant("failed", "confirmed"))

    def test_unknown_outcome_is_none(self):
        self.assertIsNone(calibration.concordant("maybe", "confirmed"))


class EvidenceDegradeTest(unittest.TestCase):
    def test_evidence_degrades_without_paperclip(self):
        with patch.object(calibration.paperclip, "available", return_value=False):
            ev = calibration.approved_indication_evidence("any query", source="fda")
        self.assertFalse(ev["available"])
        self.assertEqual(ev["ids"], [])
        self.assertEqual(ev["status"], "unavailable")


class TriangulationDegradeTest(unittest.TestCase):
    def test_no_target_returns_unavailable(self):
        t = calibration.target_disease_triangulation(None, "Systemic JIA")
        self.assertFalse(t["available"])

    def test_empty_ensembl_list_unavailable(self):
        t = calibration.target_disease_triangulation([], "Systemic JIA")
        self.assertFalse(t["available"])

    def test_tooluniverse_unavailable_degrades(self):
        from phoenix.tools import tooluniverse as tu
        with patch.object(tu, "run", return_value={"status": "unavailable", "error": "off"}):
            t = calibration.target_disease_triangulation(["ENSG00000125538"], "Systemic JIA")
        self.assertFalse(t["available"])


if __name__ == "__main__":
    unittest.main()
