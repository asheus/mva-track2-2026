"""Tissue-gate tests — logic + degrade-safe, no network."""
import unittest
from unittest.mock import patch

from phoenix import tissue_gate as tg


def _gtex(tpm_by_gene, tissue="Whole_Blood"):
    def run(name, args, **kw):
        g = args.get("gene_symbol")
        if g in tpm_by_gene:
            return {"status": "ok", "output": {"data": {"geneExpression": [
                {"tissueSiteDetailId": tissue, "median": tpm_by_gene[g], "geneSymbol": g}]}}}
        return {"status": "unavailable"}
    return run


class TissueGateTest(unittest.TestCase):
    def test_no_tissue_map(self):
        r = tg.panel_tissue_gate(["A"], "spleen-xyz")
        self.assertEqual(r["status"], "no_tissue_map")

    def test_degrades_without_gtex(self):
        with patch.object(tg.TU, "run", return_value={"status": "unavailable"}):
            r = tg.panel_tissue_gate(["A", "B"], "whole_blood")
        self.assertEqual(r["status"], "unavailable")

    def test_flags_silent_genes(self):
        with patch.object(tg.TU, "run", side_effect=_gtex({"A": 200.0, "B": 0.1, "C": 5.0})):
            r = tg.panel_tissue_gate(["A", "B", "C"], "whole_blood")
        self.assertEqual(r["status"], "ok")
        self.assertEqual(r["silent_genes"], ["B"])          # 0.1 TPM < 1.0
        self.assertEqual(r["n_expressed"], 2)
        self.assertTrue(r["reliable"])                       # 2/3 expressed


if __name__ == "__main__":
    unittest.main()
