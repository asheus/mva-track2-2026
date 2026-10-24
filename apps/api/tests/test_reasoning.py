"""Reasoning Agent unit tests — exercise the deterministic (no-LLM) curation path.

These force the fallback by patching out the LLM call, so they are deterministic and fast
whether or not an API key (e.g. a local .env) is present — we assert the curation logic,
not model output.
"""

import unittest
from unittest.mock import patch

from phoenix.agents.reasoning import agent as reasoning


def _context(**overrides):
    ctx = {
        "drug": {
            "name": "Canakinumab",
            "mechanism": "anti-IL-1b",
            "indication": "SJIA",
        },
        "dataset": {"geo_id": "GSE80060", "tissue": "whole_blood"},
        "literature": {
            "active_dimensions": ["Immune", "IFN"],
            "citations": ["PMID:canakinumab-fixture"],
            "gene_panels": {
                "Immune": [
                    {
                        "symbol": "IL1B",
                        "rationale": "Direct target",
                        "source": "PMID:canakinumab-fixture",
                    },
                    {
                        "symbol": "NLRP3",
                        "rationale": "Inflammasome",
                        "source": "PMID:canakinumab-fixture",
                    },
                    {
                        "symbol": "IL18",
                        "rationale": "Inflammasome cytokine",
                        "source": "PMID:canakinumab-fixture",
                    },
                ],
                "IFN": [
                    {
                        "symbol": "IL1B",
                        "rationale": "shared",
                        "source": "PMID:canakinumab-fixture",
                    },
                    {
                        "symbol": "MX1",
                        "rationale": "ISG",
                        "source": "PMID:canakinumab-fixture",
                    },
                ],
            },
        },
        "drug_mechanism": {"target_dimensions": ["Immune"]},
        "iteration": 1,
        "panel_version": 1,
    }
    ctx.update(overrides)
    return ctx


class ReasoningAgentTests(unittest.TestCase):
    def setUp(self):
        # Force the deterministic curation path regardless of any configured LLM key,
        # so these tests assert curation logic (not live model output) and stay fast.
        p = patch.object(
            reasoning, "complete_json", side_effect=RuntimeError("forced-offline")
        )
        p.start()
        self.addCleanup(p.stop)

    def test_output_contract_shape(self):
        out = reasoning.run(_context())
        for key in (
            "agent",
            "owner",
            "status",
            "panel_version",
            "active_dimensions",
            "genes",
            "removed",
            "notes",
        ):
            self.assertIn(key, out)
        self.assertEqual(out["agent"], "reasoning")
        self.assertIn(out["status"], {"ok", "degraded"})

    def test_routes_to_mechanism_target_dimensions(self):
        # drug_mechanism.target_dimensions = ["Immune"], so the IFN dimension is dropped.
        out = reasoning.run(_context())
        self.assertEqual(out["active_dimensions"], ["Immune"])
        self.assertTrue(all(g["dimension"] == "Immune" for g in out["genes"]))

    def test_dedup_keeps_target_gene_once(self):
        out = reasoning.run(_context())
        symbols = [g["symbol"] for g in out["genes"]]
        self.assertEqual(symbols.count("IL1B"), 1)
        self.assertIn("IL1B", symbols)  # direct target retained

    def test_genes_have_required_fields(self):
        out = reasoning.run(_context())
        for gene in out["genes"]:
            self.assertEqual(
                set(gene),
                {"symbol", "dimension", "rationale", "citation", "added_in_iteration"},
            )
            self.assertTrue(gene["citation"])

    def test_active_dimensions_match_genes(self):
        out = reasoning.run(_context())
        used = {g["dimension"] for g in out["genes"]}
        self.assertEqual(set(out["active_dimensions"]), used)

    def test_empty_literature_does_not_crash(self):
        out = reasoning.run(_context(literature={}, drug_mechanism={}))
        self.assertEqual(out["genes"], [])
        self.assertEqual(out["active_dimensions"], [])

    def test_citation_verification_drops_unknown_id(self):
        known = {"PMID:real"}
        self.assertEqual(
            reasoning._verify_citation("PMID:fabricated", known),
            "unverified_model_knowledge",
        )
        self.assertEqual(
            reasoning._verify_citation("PMID:real — title", known), "PMID:real — title"
        )
        self.assertEqual(
            reasoning._verify_citation("unverified_model_knowledge", known),
            "unverified_model_knowledge",
        )

    def test_post_verification_honors_valid_ids_contract(self):
        ctx = _context(
            literature={
                "active_dimensions": ["Immune"],
                "valid_ids": ["PMC777"],
                "citations": [],
                "gene_panels": {
                    "Immune": [
                        {"symbol": "IL1B", "rationale": "target", "source": "PMC777"},
                        {"symbol": "NLRP3", "rationale": "inflammasome", "source": "PMC777"},
                    ]
                },
            }
        )
        llm_out = {
            "agent": "reasoning",
            "owner": "Maaz",
            "status": "ok",
            "panel_version": 1,
            "active_dimensions": ["Immune"],
            "genes": [
                {
                    "symbol": "IL1B",
                    "dimension": "Immune",
                    "rationale": "target",
                    "citation": "PMC777",
                    "added_in_iteration": 1,
                },
                {
                    "symbol": "NLRP3",
                    "dimension": "Immune",
                    "rationale": "inflammasome",
                    "citation": "PMID:fabricated",
                    "added_in_iteration": 1,
                },
            ],
            "removed": [],
            "notes": "llm",
        }
        with patch.object(reasoning, "complete_json", return_value=llm_out):
            out = reasoning.run(ctx)

        by_symbol = {g["symbol"]: g["citation"] for g in out["genes"]}
        self.assertEqual(by_symbol["IL1B"], "PMC777")
        self.assertEqual(by_symbol["NLRP3"], "unverified_model_knowledge")


if __name__ == "__main__":
    unittest.main()
