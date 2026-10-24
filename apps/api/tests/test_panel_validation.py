"""Panel-validation tests — verdict logic + degrade-safe, no network."""
import unittest
from unittest.mock import patch

from phoenix import panel_validation as pv


def _enrich(term, adj_p):
    return {"status": "ok", "output": {"data": {"enriched_terms": [
        {"term": term, "adjusted_p_value": adj_p, "overlap_count": 13, "overlapping_genes": ["MX1"]}]}}}


class ValidateTest(unittest.TestCase):
    def test_validated_when_term_matches_and_significant(self):
        def fake(name, args, **kw):
            if name == "Enrichr_enrich":
                return _enrich("Interferon Alpha/Beta Signaling R-HSA-909733", 4.1e-27)
            if name == "MSigDB_get_gene_set_members":
                return {"status": "ok", "output": {"data": {"genes": ["MX1", "ISG15", "OAS1"]}}}
            return {"status": "unavailable"}
        with patch.object(pv.TU, "run", side_effect=fake):
            v = pv.validate_panel("IFN", ["MX1", "ISG15", "OAS1", "IFIT1"])
        self.assertEqual(v["status"], "ok")
        self.assertTrue(v["label_match"])
        self.assertTrue(v["significant"])
        self.assertTrue(v["validated"])
        self.assertEqual(v["canonical"]["panel_in_canonical"], 3)

    def test_not_validated_on_wrong_pathway(self):
        with patch.object(pv.TU, "run",
                          side_effect=lambda n, a, **k: _enrich("Glycolysis R-HSA-70171", 1e-10)
                          if n == "Enrichr_enrich" else {"status": "unavailable"}):
            v = pv.validate_panel("IFN", ["A", "B"])
        self.assertFalse(v["label_match"])    # "glycolysis" is not an IFN keyword
        self.assertFalse(v["validated"])

    def test_degrades_without_tooluniverse(self):
        with patch.object(pv.TU, "run", return_value={"status": "unavailable"}):
            v = pv.validate_panel("IFN", ["A", "B"])
        self.assertEqual(v["status"], "unavailable")
        self.assertIsNone(v["validated"])


if __name__ == "__main__":
    unittest.main()
