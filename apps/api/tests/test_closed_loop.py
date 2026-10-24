import json
import unittest
from pathlib import Path
from unittest.mock import patch

from phoenix.agents.critique import agent as critique_agent
from phoenix.agents.reasoning import agent as reasoning_agent
from phoenix.orchestrator import loop


FIXTURE = Path(__file__).parent / "fixtures" / "organ_aging_canakinumab.json"


def wave1_fixture(context):
    return {
        "literature": {
            "active_dimensions": ["Immune", "IFN"],
            "citations": ["PMID:canakinumab-fixture"],
            "gene_panels": {
                "Immune": [
                    {"symbol": "IL1B", "rationale": "Direct target axis", "source": "PMID:canakinumab-fixture"},
                    {"symbol": "NLRP3", "rationale": "Inflammasome assembly", "source": "PMID:canakinumab-fixture"},
                    {"symbol": "PYCARD", "rationale": "Inflammasome adapter", "source": "PMID:canakinumab-fixture"},
                    {"symbol": "IL18", "rationale": "Inflammasome cytokine", "source": "PMID:canakinumab-fixture"},
                    {"symbol": "S100A8", "rationale": "Myeloid DAMP", "source": "PMID:canakinumab-fixture"},
                    {"symbol": "S100A9", "rationale": "Myeloid DAMP", "source": "PMID:canakinumab-fixture"}
                ]
            },
        },
        "drug_mechanism": {"target_dimensions": ["Immune"], "expected_direction": "higher_baseline_response"},
    }


def organ_aging_fixture(context):
    return json.loads(FIXTURE.read_text())


def preflight_proceed(context):
    return {
        "agent": "trial_forensics",
        "owner": "Maaz",
        "status": "ok",
        "stage": "target_engagement",
        "action": "PROCEED",
        "target_engagement": "unknown",
        "nct_ids": [],
        "evidence": [],
        "failure_mode": None,
        "notes": "fixture proceed",
    }


def reasoning_fixture(context):
    return {
        "agent": "reasoning",
        "owner": "Maaz",
        "status": "ok",
        "panel_version": context.get("panel_version", 1),
        "active_dimensions": ["Immune"],
        "genes": [
            {"symbol": symbol, "dimension": "Immune", "rationale": "fixture", "citation": "PMID:canakinumab-fixture", "added_in_iteration": 1}
            for symbol in ("IL1B", "NLRP3", "PYCARD", "IL18", "S100A8", "S100A9")
        ],
        "removed": [],
        "notes": "fixture",
    }


def commit_critique(context):
    return {
        "iteration": context["iteration"],
        "panel_version": context["panel_version"],
        "defensibility": 0.91,
        "axes": {"direction": 0.95, "magnitude": 0.95, "panel_completeness": 0.85, "confounding": 0.85},
        "gap_query": None,
        "action": "COMMIT",
        "notes": "fixture commit",
    }


def refine_then_abstain(context):
    if context["iteration"] < loop.MAX_ITER:
        return {
            "iteration": context["iteration"],
            "panel_version": context["panel_version"],
            "defensibility": 0.42,
            "axes": {"direction": 0.3, "magnitude": 0.2, "panel_completeness": 0.6, "confounding": 0.6},
            "gap_query": "add stronger BAFF pathway markers",
            "action": "REFINE",
            "notes": "fixture refine",
        }
    return {
        "iteration": context["iteration"],
        "panel_version": context["panel_version"],
        "defensibility": 0.45,
        "axes": {"direction": 0.3, "magnitude": 0.2, "panel_completeness": 0.7, "confounding": 0.6},
        "gap_query": None,
        "action": "ABSTAIN",
        "notes": "fixture abstain",
    }


def refine_then_commit(context):
    if context["iteration"] == 1:
        return {
            "iteration": context["iteration"],
            "panel_version": context["panel_version"],
            "defensibility": 0.55,
            "axes": {"direction": 0.4, "magnitude": 0.3, "panel_completeness": 0.8, "confounding": 0.7},
            "gap_query": "add stronger BAFF pathway markers",
            "action": "REFINE",
            "notes": "fixture refine",
        }
    return {
        "iteration": context["iteration"],
        "panel_version": context["panel_version"],
        "defensibility": 0.88,
        "axes": {"direction": 0.9, "magnitude": 0.8, "panel_completeness": 0.9, "confounding": 0.8},
        "gap_query": None,
        "action": "COMMIT",
        "notes": "fixture commit after refine",
    }


class ClosedLoopTest(unittest.TestCase):
    def test_fixture_can_commit(self):
        with (
            patch.object(loop, "wave1", side_effect=wave1_fixture),
            patch.object(loop, "load_response", return_value={}),
            patch.object(loop, "target_engagement_gate", side_effect=preflight_proceed),
            patch.object(loop, "reasoning", side_effect=reasoning_fixture),
            patch.object(loop, "organ_aging", side_effect=organ_aging_fixture),
            patch.object(loop, "critique", side_effect=commit_critique),
            patch.object(loop, "commercial", return_value={"status": "ok", "responder_fraction": 0.5, "addressable_market_usd_bn": 2.5, "note": "fixture"}),
        ):
            record = loop.analyze_legacy({"name": "Canakinumab", "mechanism": "anti-IL-1b"}, {"geo_id": "GSE80060"})

        self.assertEqual(record["decision"], "COMMIT")
        self.assertEqual(record["verdict"], "hyper_responder_subgroup")
        self.assertEqual(record["iteration_count"], 1)
        self.assertGreaterEqual(record["critique_history"][0]["defensibility"], loop.COMMIT_THRESHOLD)
        self.assertEqual(record["effect_sizes"][0]["dimension"], "Immune")

    def test_missing_effects_abstains_after_three_iterations(self):
        with (
            patch.object(loop, "wave1", side_effect=wave1_fixture),
            patch.object(loop, "load_response", return_value={}),
            patch.object(loop, "target_engagement_gate", side_effect=preflight_proceed),
            patch.object(loop, "reasoning", side_effect=reasoning_fixture),
            patch.object(loop, "organ_aging", return_value={"active_dimensions": [], "effect_sizes": []}),
            patch.object(loop, "critique", side_effect=refine_then_abstain),
        ):
            record = loop.analyze_legacy({"name": "Belimumab", "mechanism": "anti-BAFF"}, {"geo_id": "GSE-stub"})

        self.assertEqual(record["decision"], "ABSTAIN")
        self.assertEqual(record["verdict"], "principled_abstention")
        self.assertEqual(record["iteration_count"], loop.MAX_ITER)
        self.assertEqual(record["abstention_class"], "insufficient_panel_coverage")

    def test_refine_then_commit_threads_gap_query(self):
        wave1_gap_queries = []

        def wave1_with_gap_record(context):
            wave1_gap_queries.append(context.get("gap_query"))
            return wave1_fixture(context)

        with (
            patch.object(loop, "wave1", side_effect=wave1_with_gap_record),
            patch.object(loop, "load_response", return_value={}),
            patch.object(loop, "target_engagement_gate", side_effect=preflight_proceed),
            patch.object(loop, "reasoning", side_effect=reasoning_fixture),
            patch.object(loop, "organ_aging", side_effect=organ_aging_fixture),
            patch.object(loop, "critique", side_effect=refine_then_commit),
            patch.object(loop, "commercial", return_value={"status": "ok", "responder_fraction": 0.5, "addressable_market_usd_bn": 2.5, "note": "fixture"}),
        ):
            record = loop.analyze_legacy({"name": "Canakinumab", "mechanism": "anti-IL-1b"}, {"geo_id": "GSE80060"})

        self.assertEqual(record["decision"], "COMMIT")
        self.assertEqual(record["iteration_count"], 2)
        self.assertEqual(wave1_gap_queries, [None, "add stronger BAFF pathway markers"])


class AgentFallbackTest(unittest.TestCase):
    def test_reasoning_fallback_without_llm(self):
        with patch.object(reasoning_agent, "complete_json", side_effect=RuntimeError("offline")):
            out = reasoning_agent.run({**wave1_fixture({}), "iteration": 1, "panel_version": 1})

        self.assertEqual(out["status"], "degraded")
        # Reasoning curates dimensions that actually have panel genes (Immune in the fixture).
        self.assertIn("Immune", out["active_dimensions"])
        self.assertTrue(out["genes"])

    def test_critique_fallback_commits_fixture(self):
        context = {
            "iteration": 1,
            "panel_version": 1,
            "reasoning": reasoning_fixture({"panel_version": 1}),
            "organ_aging": organ_aging_fixture({}),
            "dataset": {"geo_id": "GSE80060"},
        }
        with patch.object(critique_agent, "complete_json", side_effect=RuntimeError("offline")):
            out = critique_agent.run(context)

        self.assertEqual(out["action"], "COMMIT")
        self.assertGreaterEqual(out["defensibility"], loop.COMMIT_THRESHOLD)


if __name__ == "__main__":
    unittest.main()
