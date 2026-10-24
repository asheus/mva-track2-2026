"""Repurposing (closed-loop) tests — dataset mapping + degrade-safe, no network."""
import unittest
from unittest.mock import patch

from phoenix import repurposing as rp


class DatasetMapTest(unittest.TestCase):
    def test_maps_known_diseases(self):
        self.assertEqual(rp._dataset_for("Juvenile Idiopathic Arthritis")["geo_id"], "GSE80060")
        self.assertEqual(rp._dataset_for("systemic lupus erythematosus")["geo_id"], "GSE32591")
        self.assertEqual(rp._dataset_for("lupus nephritis")["geo_id"], "GSE32591")
        self.assertIsNone(rp._dataset_for("type 2 diabetes mellitus"))


class DegradeTest(unittest.TestCase):
    def test_degrades_when_discovery_unavailable(self):
        with patch.object(rp, "discover_indications",
                          return_value={"status": "unavailable", "reason": "no cache"}):
            r = rp.predict_repurposing({"name": "Foodrug"})
        self.assertEqual(r["status"], "unavailable")
        self.assertEqual(r["predictions"], [])

    def test_flags_dataset_vs_novel(self):
        disc = {"status": "ok", "target": {"symbols": ["IL1B"]}, "candidates": [
            {"disease": "juvenile idiopathic arthritis", "efo_id": "EFO_1", "score": 0.78,
             "top_datasource": "clinical_precedence", "is_current_indication": True},
            {"disease": "type 2 diabetes mellitus", "efo_id": "EFO_2", "score": 0.95,
             "top_datasource": "europepmc", "is_current_indication": False},
        ]}
        ad = {"axis": "Immune", "cohens_d": 1.07, "q_value": 1e-5, "verdict": "confirmed"}
        with patch.object(rp, "discover_indications", return_value=disc), \
             patch.object(rp, "drug_mechanism", return_value={"recommended_organ_aging_dimension": "Immune"}), \
             patch.object(rp, "_axis_dominance", return_value=ad):
            r = rp.predict_repurposing({"name": "Canakinumab"})
        self.assertEqual(r["status"], "ok")
        by_disease = {p["disease"]: p for p in r["predictions"]}
        # JIA has a dataset -> scored + predicted; T2D has none -> flagged needs-dataset
        self.assertTrue(by_disease["juvenile idiopathic arthritis"]["predicted"])
        self.assertEqual(by_disease["juvenile idiopathic arthritis"]["dataset"], "GSE80060")
        self.assertIsNone(by_disease["type 2 diabetes mellitus"]["dataset"])


if __name__ == "__main__":
    unittest.main()
