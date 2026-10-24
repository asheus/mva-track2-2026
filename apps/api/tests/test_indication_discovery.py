"""Indication-Discovery tests — degrade-safe + ranking/novel-flagging logic, no network."""
import unittest
from unittest.mock import patch

from phoenix.agents.indication_discovery import agent as ind


class DegradeTest(unittest.TestCase):
    def test_unavailable_without_target(self):
        with patch.object(ind, "_authoritative_target", return_value=None):
            r = ind.discover_indications({"name": "Foodrug"})
        self.assertEqual(r["status"], "unavailable")
        self.assertEqual(r["candidates"], [])
        self.assertEqual(r["top_novel"], [])


class RankingTest(unittest.TestCase):
    def test_ranks_by_score_and_flags_novel(self):
        info = {"chembl_id": "CHEMBL1", "moa": "IL-1b inhibitor",
                "target_symbols": ["IL1B"], "target_ensembl": ["ENSG1"]}

        def fake_run(name, args, **kw):
            if name == "OpenTargets_get_drug_indications_by_chemblId":
                return {"status": "ok", "output": {"data": {"drug": {"indications": {"rows": [
                    {"disease": {"id": "EFO_curr", "name": "current disease"}}]}}}}}
            if name == "OpenTargets_get_diseases_phenotypes_by_target_ensembl":
                return {"status": "ok", "output": {"data": {"target": {"associatedDiseases": {"rows": [
                    {"disease": {"id": "EFO_novel", "name": "novel disease"},
                     "datasourceScores": [{"id": "genetics", "score": 0.9}]},
                    {"disease": {"id": "EFO_curr", "name": "current disease"},
                     "datasourceScores": [{"id": "clinical_precedence", "score": 0.7}]}]}}}}}
            return {"status": "unavailable"}

        with patch.object(ind, "_authoritative_target", return_value=info), \
             patch.object(ind.TU, "run", side_effect=fake_run):
            r = ind.discover_indications({"name": "Drug"})

        self.assertEqual(r["status"], "ok")
        self.assertEqual(r["candidates"][0]["disease"], "novel disease")   # ranked by score desc
        self.assertEqual(r["candidates"][0]["score"], 0.9)
        self.assertFalse(r["candidates"][0]["is_current_indication"])      # novel flagged
        self.assertTrue(r["candidates"][1]["is_current_indication"])       # current flagged
        self.assertEqual([c["disease"] for c in r["top_novel"]], ["novel disease"])


if __name__ == "__main__":
    unittest.main()
