"""Offline tests for the Data Agent + GEO search tool. No network, no LLM."""

import json
import unittest
from unittest.mock import patch

from phoenix.agents.data import agent as da
from phoenix.tools import geo_search

CANDIDATES = [
    {
        "geo_id": "GSE111",
        "title": "RA whole blood expression",
        "summary": "",
        "taxon": "Homo sapiens",
        "n_samples": 100,
        "gds_type": "Expression profiling by array",
        "platform": "GPL570",
        "supp_file": "",
        "pub_date": "2020",
        "entry_type": "GSE",
    },
    {
        "geo_id": "GSE222",
        "title": "RA synovium RNA-seq",
        "summary": "",
        "taxon": "Homo sapiens",
        "n_samples": 40,
        "gds_type": "Expression profiling by high throughput sequencing",
        "platform": "GPL24676",
        "supp_file": "",
        "pub_date": "2021",
        "entry_type": "GSE",
    },
]


class DataAgentTests(unittest.TestCase):
    def test_no_candidates_abstains(self):
        # complete_json is also called by query-expansion now — mock it so the test makes no LLM call.
        with (
            patch.object(da.geo_search, "find_candidates", return_value=[]),
            patch.object(da, "complete_json", side_effect=RuntimeError("no key")),
        ):
            out = da.run({"drug": {"name": "Foo", "indication": "RA"}})
        self.assertEqual(out["status"], "no_dataset_found")
        self.assertIsNone(out["geo_id"])

    def test_llm_unavailable_uses_top_candidate(self):
        with (
            patch.object(da.geo_search, "find_candidates", return_value=CANDIDATES),
            patch.object(da, "complete_json", side_effect=RuntimeError("no key")),
            patch.object(da.paperclip, "available", return_value=False),
        ):
            out = da.run(
                {"drug": {"name": "Foo", "mechanism": "anti-X", "indication": "RA"}}
            )
        self.assertEqual(out["status"], "ok")
        self.assertEqual(out["geo_id"], "GSE111")  # top-ranked array candidate
        self.assertEqual(out["candidates_considered"], 2)

    def test_hallucinated_pick_falls_back_to_candidate(self):
        with (
            patch.object(da.geo_search, "find_candidates", return_value=CANDIDATES),
            patch.object(
                da,
                "complete_json",
                return_value={
                    "geo_id": "GSE999",
                    "tissue": "blood",
                    "confidence": "high",
                    "rationale": "x",
                },
            ),
            patch.object(da.paperclip, "available", return_value=False),
        ):
            out = da.run({"drug": {"name": "Foo", "indication": "RA"}})
        self.assertEqual(out["geo_id"], "GSE111")  # GSE999 not a candidate -> top match
        self.assertIn("notes", out)


class GeoSearchTests(unittest.TestCase):
    def test_normalize_gds_to_gse(self):
        rec = geo_search._normalize(
            "200012345",
            {
                "accession": "GDS5678",
                "gse": "111",
                "title": "T",
                "n_samples": "50",
                "gdsType": "Expression profiling by array",
            },
        )
        self.assertEqual(rec["geo_id"], "GSE111")
        self.assertEqual(rec["n_samples"], 50)

    def test_summaries_parses_json(self):
        fake = json.dumps(
            {
                "result": {
                    "uids": ["1"],
                    "1": {
                        "accession": "GSE80060",
                        "title": "sJIA",
                        "n_samples": "206",
                        "gdsType": "Expression profiling by array",
                        "gpl": "GPL570",
                        "taxon": "Homo sapiens",
                    },
                }
            }
        ).encode()
        with (
            patch.object(geo_search, "_get", return_value=fake),
            patch.object(geo_search.time, "sleep"),
        ):
            recs = geo_search.summaries(["1"])
        self.assertEqual(recs[0]["geo_id"], "GSE80060")
        self.assertEqual(recs[0]["n_samples"], 206)


if __name__ == "__main__":
    unittest.main()
