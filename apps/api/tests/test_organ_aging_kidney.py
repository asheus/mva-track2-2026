"""Kidney vascular/fibrotic organ-aging axis + zibotentan case study.

Unit tests (synthetic/mocked — no network, no cached GEO) cover the new axis, the
router registration, the two new channels, and the organ-aging tissue scoring logic.
A data-gated integration test exercises the full zibotentan case study when the cached
GEO matrices are present.
"""
import json
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest

from phoenix.evidence import Evidence, validate, CHANNELS

_API = Path(__file__).resolve().parent.parent
_PANELS = json.loads((_API / "phoenix/agents/organ_aging/gene_panels.json").read_text())
_AXIS = "Kidney_Vascular_Fibrotic"


# --- registration -------------------------------------------------------------------------
def test_kidney_axis_registered():
    panel = _PANELS["panels"].get(_AXIS)
    assert panel, "Kidney_Vascular_Fibrotic panel missing"
    syms = [g["symbol"] for g in panel["genes"]]
    assert "EDNRA" in syms and "EDN1" in syms          # zibotentan's target on the panel
    assert len(syms) >= 15
    assert panel["method"] == "unweighted_mean_zscore"
    assert _AXIS in _PANELS["dimensions_populated"]


def test_multi_organ_fibrotic_axes_registered():
    for ax in ("Liver_Fibrotic", "Lung_Fibrotic", "Cardiac_Fibrotic"):
        panel = _PANELS["panels"].get(ax)
        assert panel, f"{ax} panel missing"
        syms = [g["symbol"] for g in panel["genes"]]
        assert "COL1A1" in syms and "TGFB1" in syms     # shared fibrotic core
        assert len(syms) >= 12
        assert ax in _PANELS["dimensions_populated"]


def test_classifier_handles_compartments_and_boolean_fields():
    from phoenix.channels.organ_aging_tissue import _classify
    # tissue compartment alone is NOT a disease (controls are dissected the same way)
    assert _classify("Tubulointerstitium from kidney biopsy") is None
    assert _classify("tissue: Tubulointerstitium from kidney biopsy | diagnosis: tumor nephrectomy") == "control"
    assert _classify("diagnosis: Diabetic nephropathy") == "disease"
    # boolean heart-failure field: 'no' is a control, 'yes' is disease
    assert _classify("heart failure: no | tissue: left ventricle") == "control"
    assert _classify("heart failure: yes | disease status: idiopathic dilated CMP") == "disease"


def test_router_routes_zibotentan_to_kidney_axis():
    from phoenix.agents.drug_mechanism.agent import _HERO_PREDICTIONS, _VALID_DIMENSIONS
    pred = _HERO_PREDICTIONS["zibotentan"]
    assert pred["recommended_organ_aging_dimension"] == _AXIS
    assert "EDNRA" in pred["target_genes"]
    assert _AXIS in _VALID_DIMENSIONS


def test_new_channels_are_valid_evidence():
    for ch in ("endpoint_alignment", "safety_gate"):
        assert ch in CHANNELS
        e = Evidence(asset="zibotentan", candidate_indication="chronic kidney disease",
                     channel=ch, claim="t", direction="supports_rescue",
                     support_score=0.5, confidence=0.6)
        validate(e.to_dict())          # schema accepts the new channel


# --- scoring logic (synthetic, mocked GEO loader) -----------------------------------------
def _synth(elevated: bool):
    """genes x samples matrix where the kidney axis is elevated (or depleted) in disease."""
    genes = [g["symbol"] for g in _PANELS["panels"][_AXIS]["genes"]]
    rng = np.random.default_rng(0)
    dis = [f"d{i}" for i in range(20)]
    ctl = [f"c{i}" for i in range(20)]
    shift = 1.5 if elevated else -1.5
    data = {}
    for s in dis:
        data[s] = rng.normal(shift, 1.0, len(genes))
    for s in ctl:
        data[s] = rng.normal(0.0, 1.0, len(genes))
    expr = pd.DataFrame(data, index=genes)
    groups = {**{s: "disease" for s in dis}, **{s: "control" for s in ctl}}
    return expr, groups


@pytest.mark.parametrize("elevated,expected", [(True, "supports_rescue"), (False, "contradicts_rescue")])
def test_axis_scoring_direction(elevated, expected):
    from phoenix.channels import organ_aging_tissue as oat
    expr, groups = _synth(elevated)
    with patch("phoenix.data_loaders.geo.load_expression", return_value=expr), \
         patch("phoenix.data_loaders.geo.load_groups", return_value=groups):
        e = oat.run("zibotentan", "chronic kidney disease", _AXIS, "GSE_SYNTH")
    d = e.to_dict()
    validate(d)
    assert d["channel"] == "tissue_transcriptome"
    assert d["direction"] == expected
    assert (d["support_score"] > 0) == elevated
    assert d["effect"]["axis"] == _AXIS
    # per-patient organ-age is surfaced (the enrichable fraction); higher when elevated
    pct = d["effect"]["pct_patients_elevated"]
    assert 0.0 <= pct <= 1.0
    assert (pct > 0.4) == elevated


def test_safety_gate_only_gates_not_double_counts():
    """A safety_gate item must lower the rank via the multiplicative gate only — it must not
    also enter the additive support sum or the contradiction penalty."""
    from phoenix.adjudicator import adjudicate
    eff = [Evidence("zibotentan", "ckd", "tissue_transcriptome", "axis up",
                    direction="supports_rescue", support_score=0.8, confidence=0.7),
           Evidence("zibotentan", "ckd", "endpoint_alignment", "endpoint",
                    direction="supports_rescue", support_score=0.7, confidence=0.7)]
    gate = Evidence("zibotentan", "ckd", "safety_gate", "edema",
                    direction="contradicts_rescue", support_score=-0.3, confidence=0.5,
                    is_safety_gate=True)
    no_gate = adjudicate("zibotentan", "ckd", eff)
    with_gate = adjudicate("zibotentan", "ckd", eff + [gate])
    # gate applied and rank lowered, but ONLY through the gate factor
    assert with_gate["safety_gate"]["applied"] is True
    assert with_gate["rescue_rank"] < no_gate["rescue_rank"]
    # safety item carries zero additive contribution and is not a contradiction
    sg = next(c for c in with_gate["per_channel"] if c["channel"] == "safety_gate")
    assert sg["weighted_contribution"] == 0.0 and sg["is_safety_gate"] is True
    assert with_gate["contradiction_penalty"] == 0.0
    assert not any(x.get("type") == "cross_channel_conflict"
                   for x in with_gate["contradiction_registry"])


def test_axis_missing_panel_is_not_available():
    from phoenix.channels import organ_aging_tissue as oat
    e = oat.run("zibotentan", "chronic kidney disease", "No_Such_Axis", "GSE_SYNTH")
    assert e.direction == "not_available"


# --- literature channel (Paperclip/PubMed grounding) --------------------------------------
def test_literature_offline_is_honest_and_valid():
    """Offline (no live flag, no cache): emits a valid Evidence with the curated support but
    NO fabricated citations — provenance honestly notes offline_fallback."""
    from phoenix.channels import literature
    e = literature.run("zibotentan", "chronic kidney disease", channel="endpoint_alignment",
                       claim="EDNRA blockade lowers albuminuria", direction="supports_rescue",
                       support_score=0.7, confidence=0.7, question="EDNRA and albuminuria in CKD?",
                       live=False)
    d = e.to_dict()
    validate(d)
    assert d["channel"] == "endpoint_alignment"
    assert d["support_score"] == 0.7              # curated support preserved
    assert d["sources"] == []                      # no fabricated PMIDs offline
    assert d["effect"]["literature_provider"] == "offline_fallback"


def test_literature_replays_cached_citations(tmp_path, monkeypatch):
    """A cached citation set is replayed offline and attached as Evidence.sources."""
    from phoenix.channels import literature
    monkeypatch.setattr(literature, "_CACHE", tmp_path)
    q = "EDNRA and albuminuria in CKD?"
    cache = tmp_path / f"{literature._slug('zibotentan')}__{literature._slug('chronic kidney disease')}__{literature._slug(q)}.json"
    cache.write_text(json.dumps({"ids": ["12345678", "23456789"], "provider": "pubmed"}))
    e = literature.run("zibotentan", "chronic kidney disease", channel="safety_gate",
                       claim="edema risk", direction="contradicts_rescue", support_score=-0.3,
                       confidence=0.5, question=q, is_safety_gate=True, live=False)
    d = e.to_dict()
    assert d["sources"] == ["12345678", "23456789"]
    assert "12345678" in d["claim"] and d["effect"]["n_citations"] == 2


# --- adversarial self-refutation -----------------------------------------------------------
def test_refute_offline_is_honest(tmp_path, monkeypatch):
    """Offline + uncached: does not fabricate a refutation verdict — emits a neutral,
    low-confidence 'not run offline' Evidence."""
    from phoenix.channels import literature
    monkeypatch.setattr(literature, "_CACHE", tmp_path)   # empty cache -> true offline path
    e = literature.refute("zibotentan", "prostate cancer", "thesis", outcome_cutoff="2011-02-01",
                          live=False)
    d = e.to_dict()
    validate(d)
    assert d["channel"] == "literature_refutation"
    assert d["direction"] == "neutral" and d["support_score"] == 0.0
    assert d["effect"]["refuted"] is None
    assert d["temporality_cutoff"] == "2011-02-01"


def test_refute_replays_refuted_verdict(tmp_path, monkeypatch):
    """A cached 'refuted' verdict becomes contradicts_rescue evidence that feeds the
    contradiction penalty, with the disconfirming citations as sources."""
    from phoenix.channels import literature
    from phoenix.adjudicator import adjudicate
    from phoenix.evidence import Evidence
    monkeypatch.setattr(literature, "_CACHE", tmp_path)
    cache = tmp_path / f"refute__{literature._slug('zibotentan')}__{literature._slug('prostate cancer')}.json"
    cache.write_text(json.dumps({"refuted": True, "severity": 0.7,
                                 "summary": "ENTHUSE M0/M1 showed no OS benefit; on-target edema.",
                                 "citing_ids": ["10.1002/cpt.2582"], "provider": "paperclip"}))
    ref = literature.refute("zibotentan", "prostate cancer", "thesis", live=False)
    d = ref.to_dict()
    validate(d)
    assert d["direction"] == "contradicts_rescue" and d["support_score"] < 0
    assert d["sources"] == ["10.1002/cpt.2582"] and d["contradictions"]
    # it lowers the rank vs a thesis without it
    supp = [Evidence("zibotentan", "prostate cancer", "tissue_transcriptome", "axis up",
                     direction="supports_rescue", support_score=0.6, confidence=0.7)]
    with_ref = adjudicate("zibotentan", "prostate cancer", supp + [ref])
    without = adjudicate("zibotentan", "prostate cancer", supp)
    assert with_ref["rescue_rank"] < without["rescue_rank"]
    assert with_ref["contradiction_penalty"] > 0


def test_refute_survived_is_consensus(tmp_path, monkeypatch):
    from phoenix.channels import literature
    monkeypatch.setattr(literature, "_CACHE", tmp_path)
    cache = tmp_path / f"refute__{literature._slug('zibotentan')}__{literature._slug('chronic kidney disease')}.json"
    cache.write_text(json.dumps({"refuted": False, "severity": 0.0,
                                 "summary": "no material disconfirming evidence", "citing_ids": [],
                                 "provider": "paperclip"}))
    ref = literature.refute("zibotentan", "chronic kidney disease", "thesis", live=False)
    d = ref.to_dict()
    # survived = weak-positive consensus (must not dilute the rank toward zero)
    assert d["direction"] == "supports_rescue" and 0 < d["support_score"] <= 0.3
    assert d["effect"]["refuted"] is False and "SURVIVED" in d["claim"]


# --- self-correcting refinement loop (the graft) ------------------------------------------
def _ev(channel, direction, s, c, gate=False):
    return Evidence("zibotentan", "ckd", channel, f"{channel} claim", direction=direction,
                    support_score=s, confidence=c, is_safety_gate=gate)


def test_refine_approves_only_after_safety_and_refutation():
    """A positive thesis must NOT commit prioritize until BOTH safety and refutation are seen —
    the engine refines (acquires more) instead of green-lighting early."""
    from phoenix.refine import adjudicate_with_refinement
    runners = [
        ("tissue_transcriptome", lambda: _ev("tissue_transcriptome", "supports_rescue", 0.9, 0.7)),
        ("endpoint_alignment", lambda: _ev("endpoint_alignment", "supports_rescue", 0.7, 0.7)),
        ("literature_refutation", lambda: _ev("literature_refutation", "supports_rescue", 0.2, 0.5)),
        ("safety_gate", lambda: _ev("safety_gate", "contradicts_rescue", -0.3, 0.5, gate=True)),
    ]
    rec = adjudicate_with_refinement("zibotentan", "ckd", runners)
    assert len(rec["refine_trace"]) >= 3                      # it refined, didn't one-shot
    if rec["verdict"] == "prioritize_for_validation":
        assert {"safety_gate", "literature_refutation"} <= set(rec["observed_channels"])
    # no earlier round committed a GO without the required channels
    for t in rec["refine_trace"][:-1]:
        assert t["action"].startswith("REFINE") or t["action"].startswith("ABSTAIN")


def test_refine_rejects_fast_without_full_panel():
    """A negative thesis can commit do_not_rescue as soon as the evidence opposes it —
    it need not acquire the safety gate first."""
    from phoenix.refine import adjudicate_with_refinement
    runners = [
        ("tissue_transcriptome", lambda: _ev("tissue_transcriptome", "contradicts_rescue", -0.9, 0.7)),
        ("literature_refutation", lambda: _ev("literature_refutation", "contradicts_rescue", -0.7, 0.7)),
        ("endpoint_alignment", lambda: _ev("endpoint_alignment", "contradicts_rescue", -0.4, 0.5)),
        ("safety_gate", lambda: _ev("safety_gate", "contradicts_rescue", -0.3, 0.5, gate=True)),
    ]
    rec = adjudicate_with_refinement("zibotentan", "ckd", runners)
    assert rec["verdict"] == "do_not_rescue"
    assert rec["refine_trace"][-1]["action"] == "COMMIT"
    assert "safety_gate" not in rec["observed_channels"]      # committed before needing it


def test_refine_skips_not_available_channels():
    from phoenix.refine import adjudicate_with_refinement
    runners = [
        ("tissue_transcriptome", lambda: Evidence.not_available("tissue_transcriptome", "zibotentan", "ckd", "no data")),
        ("endpoint_alignment", lambda: _ev("endpoint_alignment", "supports_rescue", 0.7, 0.7)),
    ]
    rec = adjudicate_with_refinement("zibotentan", "ckd", runners)
    assert "tissue_transcriptome" not in rec["observed_channels"]   # not_available not counted
    assert rec["refine_trace"][0]["acquired"].endswith("(not_available)")


# --- full case study (needs cached GEO) ---------------------------------------------------
def _geo_cached(geo_id: str) -> bool:
    try:
        from phoenix.data_loaders import geo
        geo.load_expression(geo_id)
        return True
    except Exception:
        return False


@pytest.mark.skipif(not (_geo_cached("GSE30529") and _geo_cached("GSE55945")),
                    reason="cached GEO matrices (GSE30529, GSE55945) not present")
def test_case_study_verdicts():
    from phoenix.adjudicator import adjudicate
    from scripts import zibotentan_case_study as cs
    axis = cs._mechanism()["axis"]
    assert axis == _AXIS

    prostate = adjudicate("zibotentan", "prostate cancer",
                          cs._channels("prostate cancer", axis))
    ckd = adjudicate("zibotentan", "chronic kidney disease",
                     cs._channels("chronic kidney disease", axis))

    assert prostate["verdict"] == "do_not_rescue"
    assert ckd["verdict"] in ("interesting_under_supported", "prioritize_for_validation")
    assert ckd["rescue_rank"] > prostate["rescue_rank"]
