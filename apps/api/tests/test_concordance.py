"""Concordance verdict + degrade tests — no gseapy / network needed."""
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from phoenix.agents.organ_aging import concordance as cc


def _toy():
    # 4 genes x 6 samples; Immune set up in disease, with within-group variance (so d is defined).
    genes = ["A", "B", "C", "D"]
    samples = ["D1", "D2", "D3", "C1", "C2", "C3"]
    data = np.array([
        [6, 5, 4, 2, 1, 0],   # A (up in disease)
        [6, 5, 4, 2, 1, 0],   # B
        [3, 4, 2, 3, 4, 2],   # C (flat — no group difference)
        [4, 3, 2, 4, 3, 2],   # D
    ], dtype=float)
    expr = pd.DataFrame(data, index=genes, columns=samples)
    groups = {s: ("disease" if s.startswith("D") else "control") for s in samples}
    gene_sets = {"Immune": ["A", "B"], "Flat": ["C", "D"]}
    return expr, groups, gene_sets


class ConcordanceTest(unittest.TestCase):
    def test_oas_present_and_ssgsea_degrades(self):
        expr, groups, gene_sets = _toy()
        with patch.object(cc, "_ssgsea_axis_d", return_value={}):   # simulate gseapy absent
            res = cc.axis_method_concordance(expr, groups, gene_sets)
        self.assertEqual(res["status"], "ssgsea_unavailable")
        self.assertGreater(res["axes"]["Immune"]["oas_d"], 0.5)      # OAS still computed, disease-up
        self.assertEqual(res["axes"]["Immune"]["concordance"], "ssgsea_unavailable")

    def test_verdicts(self):
        expr, groups, gene_sets = _toy()
        with patch.object(cc, "_ssgsea_axis_d", return_value={"Immune": 0.9, "Flat": -0.8}):
            res = cc.axis_method_concordance(expr, groups, gene_sets)
        self.assertEqual(res["status"], "ok")
        self.assertEqual(res["axes"]["Immune"]["concordance"], "concordant")       # both up, notable
        # Flat: OAS ~0 (flat genes) but computed; ssGSEA -0.8 -> weak/discordant, not "incomputable".
        self.assertIsNotNone(res["axes"]["Flat"]["oas_d"])
        self.assertIn(res["axes"]["Flat"]["concordance"], {"discordant", "concordant_weak"})


if __name__ == "__main__":
    unittest.main()
