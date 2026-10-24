import json
import unittest
from pathlib import Path
from unittest.mock import patch

from phoenix.agents.trial_forensics import agent as trial_forensics
from phoenix.orchestrator import loop


FIXTURE = Path(__file__).parent / "fixtures" / "organ_aging_canakinumab.json"


def organ_aging_fixture(context):
    return json.loads(FIXTURE.read_text())


def wave1_fixture(context):
    return {
        "literature": {
            "active_dimensions": ["Immune"],
            "citations": ["PMID:trial-forensics-fixture"],
            "gene_panels": {"Immune": [{"symbol": "IL1B", "rationale": "fixture", "source": "PMID:trial-forensics-fixture"}]},
        },
        "drug_mechanism": {"target_dimensions": ["Immune"]},
    }


def reasoning_fixture(context):
    return {
        "agent": "reasoning",
        "owner": "Maaz",
        "status": "ok",
        "panel_version": context.get("panel_version", 1),
        "active_dimensions": ["Immune"],
        "genes": [
            {"symbol": symbol, "dimension": "Immune", "rationale": "fixture", "citation": "PMID:trial-forensics-fixture", "added_in_iteration": 1}
            for symbol in ("IL1B", "NLRP3", "PYCARD", "IL18", "S100A8", "S100A9")
        ],
        "removed": [],
        "notes": "fixture",
    }


def assert_schema_shape(test_case, record):
    for key in ("claim_id", "drug", "dataset", "verdict", "decision", "iteration_count", "panel_version", "critique_history", "created_at"):
        test_case.assertIn(key, record)
    test_case.assertIn(record["decision"], {"COMMIT", "REFINE", "ABSTAIN"})
    test_case.assertIsInstance(record["critique_history"], list)
    test_case.assertTrue(record["critique_history"])
    for item in record["critique_history"]:
        for key in ("iteration", "panel_version", "defensibility", "axes", "action"):
            test_case.assertIn(key, item)


def commit_critique(context):
    return {
        "iteration": context["iteration"],
        "panel_version": context["panel_version"],
        "defensibility": 0.9,
        "axes": {"direction": 0.9, "magnitude": 0.9, "panel_completeness": 0.9, "confounding": 0.9},
        "gap_query": None,
        "action": "COMMIT",
        "notes": "fixture commit",
    }


class TrialForensicsTest(unittest.TestCase):
    def test_gate_defaults_to_proceed_without_evidence(self):
        with patch.object(trial_forensics.paperclip, "available", return_value=False):
            out = trial_forensics.target_engagement_gate({"drug": {"name": "Canakinumab"}})

        self.assertEqual(out["action"], "PROCEED")
        self.assertEqual(out["target_engagement"], "unknown")

    def test_gate_abstains_only_on_positive_no_engagement_evidence(self):
        out = trial_forensics.target_engagement_gate({
            "drug": {"name": "Examplemab"},
            "trial_forensics_evidence": "The phase 2 trial showed no pharmacodynamic effect and no target engagement.",
        })

        self.assertEqual(out["action"], "ABSTAIN")
        self.assertEqual(out["target_engagement"], "not_shown")
        self.assertEqual(out["failure_mode"], "target_invalidation_no_engagement")

    def test_gate_normalizes_llm_not_shown_variant(self):
        with patch.object(
            trial_forensics, "complete_json", return_value={"target_engagement": "not shown"}
        ):
            out = trial_forensics.target_engagement_gate(
                {
                    "drug": {"name": "Examplemab"},
                    "trial_forensics_evidence": "PD section reported mixed interpretation.",
                }
            )

        self.assertEqual(out["target_engagement"], "not_shown")
        self.assertEqual(out["action"], "ABSTAIN")

    def test_gate_invalid_llm_label_falls_back_to_unknown(self):
        with patch.object(
            trial_forensics, "complete_json", return_value={"target_engagement": "inconclusive"}
        ):
            out = trial_forensics.target_engagement_gate(
                {
                    "drug": {"name": "Examplemab"},
                    "trial_forensics_evidence": "PD section reported mixed interpretation.",
                }
            )

        self.assertEqual(out["target_engagement"], "unknown")
        self.assertEqual(out["action"], "PROCEED")

    def test_stratifies_fixture_responders(self):
        out = trial_forensics.stratify_responders({
            "organ_aging": organ_aging_fixture({}),
            "trial_forensics_preflight": {"target_engagement": "shown", "evidence": ["NCT01327846"]},
        })

        self.assertEqual(out["verdict"], "hyper_responder_subgroup")
        self.assertEqual(out["responder_subgroup"]["stratifier"], "Q4 Immune-aging")
        self.assertEqual(out["responder_subgroup"]["responder_rate"], 1.0)
        self.assertEqual(out["responder_subgroup"]["baseline_rate"], 0.0)
        self.assertEqual(out["effect_sizes"][0]["metric"], "interaction_p")

    def test_loop_early_abstention_validates_against_schema(self):
        with (
            patch.object(loop, "wave1", side_effect=wave1_fixture),
            patch.object(loop, "load_response", return_value={}),
            patch.object(loop, "target_engagement_gate", return_value={
                "agent": "trial_forensics",
                "owner": "Maaz",
                "status": "ok",
                "stage": "target_engagement",
                "action": "ABSTAIN",
                "target_engagement": "not_shown",
                "nct_ids": ["NCT-no-engagement-fixture"],
                "evidence": ["No target engagement fixture"],
                "failure_mode": "target_invalidation_no_engagement",
                "notes": "fixture",
            }),
        ):
            record = loop.analyze({"name": "Examplemab", "mechanism": "anti-example"}, {"geo_id": "GSE-fixture"})

        self.assertEqual(record["decision"], "ABSTAIN")
        self.assertEqual(record["abstention_class"], "target_invalidation_no_engagement")
        assert_schema_shape(self, record)

    def test_loop_commit_adds_responder_subgroup(self):
        with (
            patch.object(loop, "wave1", side_effect=wave1_fixture),
            patch.object(loop, "load_response", return_value={}),
            patch.object(loop, "target_engagement_gate", return_value={
                "agent": "trial_forensics",
                "owner": "Maaz",
                "status": "ok",
                "stage": "target_engagement",
                "action": "PROCEED",
                "target_engagement": "shown",
                "nct_ids": ["NCT01327846"],
                "evidence": ["Target engagement shown fixture"],
                "failure_mode": None,
                "notes": "fixture",
            }),
            patch.object(loop, "reasoning", side_effect=reasoning_fixture),
            patch.object(loop, "organ_aging", side_effect=organ_aging_fixture),
            patch.object(loop, "critique", side_effect=commit_critique),
            patch.object(loop, "commercial", return_value={"status": "ok", "responder_fraction": 0.5, "addressable_market_usd_bn": 2.5, "note": "fixture"}),
        ):
            record = loop.analyze({"name": "Canakinumab", "mechanism": "anti-IL-1b"}, {"geo_id": "GSE80060"})

        self.assertEqual(record["decision"], "COMMIT")
        self.assertEqual(record["verdict"], "hyper_responder_subgroup")
        self.assertIsNotNone(record["responder_subgroup"])
        assert_schema_shape(self, record)


if __name__ == "__main__":
    unittest.main()
