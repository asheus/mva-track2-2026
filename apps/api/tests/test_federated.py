"""Tests for the federated evidence engine: evidence-object invariants + adjudicator math.

These are pure (no network, no IPD files) so they run in the data-only venv.
"""
import pytest

from phoenix.evidence import Evidence, validate
from phoenix.adjudicator import adjudicate, DEFAULT_WEIGHTS


def _supp(channel, s, c, indication="renal cell carcinoma"):
    return Evidence("sunitinib", indication, channel, f"{channel} claim",
                    direction="supports_rescue" if s >= 0 else "contradicts_rescue",
                    support_score=s, confidence=c, coverage={"datasets": 1})


# --- evidence object invariants --------------------------------------------

def test_not_available_is_canonical():
    e = Evidence.not_available("mri_imaging", "sunitinib", "rcc", "controlled access")
    assert e.observed is False
    assert e.support_score == 0.0 and e.confidence == 0.0
    assert e.direction == "not_available"
    validate(e)  # schema-valid


def test_support_scores_clamped():
    e = Evidence("d", "i", "tissue_transcriptome", "c",
                 direction="supports_rescue", support_score=5, confidence=9)
    assert e.support_score == 1.0 and e.confidence == 1.0


def test_bad_channel_rejected():
    with pytest.raises(ValueError):
        Evidence("d", "i", "not_a_channel", "c")


def test_observed_matches_direction():
    assert _supp("tissue_transcriptome", 0.5, 0.5).observed is True


# --- adjudicator math -------------------------------------------------------

def test_not_available_fully_renormalized_out():
    """Passing explicit not_available objects changes NOTHING — same rank, same coverage.
    (Missingness is renormalized out; the missing panel is reported regardless.)"""
    ev = [_supp("trial_forensics", 0.8, 0.8), _supp("tissue_transcriptome", 0.8, 0.8)]
    r = adjudicate("sunitinib", "rcc", ev)
    r_pad = adjudicate("sunitinib", "rcc", ev + [
        Evidence.not_available("mri_imaging", "sunitinib", "rcc", "x"),
        Evidence.not_available("dna_methylation", "sunitinib", "rcc", "x"),
    ])
    assert r["rescue_rank"] == pytest.approx(r_pad["rescue_rank"], abs=1e-9)
    assert r["coverage_score"] == pytest.approx(r_pad["coverage_score"], abs=1e-9)
    assert r["missing_channels"] == r_pad["missing_channels"]  # full panel either way


def test_coverage_rises_with_more_observed():
    """Coverage is separate: adding a REAL observed channel raises it; rank stays sane."""
    few = adjudicate("sunitinib", "rcc", [_supp("trial_forensics", 0.8, 0.8)])
    more = adjudicate("sunitinib", "rcc",
                      [_supp("trial_forensics", 0.8, 0.8), _supp("tissue_transcriptome", 0.8, 0.8),
                       _supp("perturbation_reversal", 0.8, 0.8)])
    assert more["coverage_score"] > few["coverage_score"]


def test_coverage_is_separate_from_rank():
    r = adjudicate("sunitinib", "rcc", [_supp("trial_forensics", 0.9, 0.9)])
    assert 0 < r["coverage_score"] < 1.0
    assert r["rescue_rank"] > 0.5  # strong single channel still ranks high...
    # ...but only one channel observed, so coverage is low
    assert r["n_observed"] == 1


def test_missing_channels_listed_not_imputed():
    r = adjudicate("sunitinib", "rcc", [_supp("trial_forensics", 0.5, 0.5)])
    assert "mri_imaging" in r["missing_channels"]
    assert "trial_forensics" in r["observed_channels"]


def test_safety_gate_cuts_rank():
    base = [_supp("trial_forensics", 0.8, 0.8), _supp("tissue_transcriptome", 0.8, 0.8)]
    gate = Evidence("sunitinib", "rcc", "clinical_labs", "intrinsic tox",
                    direction="contradicts_rescue", support_score=-0.9, confidence=0.9,
                    is_safety_gate=True)
    r = adjudicate("sunitinib", "rcc", base + [gate])
    assert r["safety_gate"]["applied"] is True
    assert r["safety_gate"]["factor"] < 1.0


def test_contradiction_penalty_and_registry():
    ev = [_supp("trial_forensics", 0.7, 0.8), _supp("tissue_transcriptome", -0.7, 0.8)]
    r = adjudicate("sunitinib", "rcc", ev)
    assert r["contradiction_penalty"] > 0
    assert any(x["type"] == "cross_channel_conflict" for x in r["contradiction_registry"])


def test_abstains_on_low_coverage():
    r = adjudicate("sunitinib", "rcc",
                   [_supp("clinical_labs", 0.5, 0.5)])  # one low-weight channel only
    assert r["verdict"] == "abstain_insufficient_coverage"


def test_do_not_rescue_on_negative_evidence():
    ev = [_supp("trial_forensics", -0.7, 0.8), _supp("tissue_transcriptome", -0.5, 0.7)]
    r = adjudicate("zibotentan", "prostate cancer", ev)
    assert r["verdict"] == "do_not_rescue"
    assert r["rescue_rank"] < 0


def test_prioritize_on_strong_multichannel():
    ev = [_supp("trial_forensics", 0.7, 0.8), _supp("tissue_transcriptome", 0.85, 0.75),
          _supp("perturbation_reversal", 0.6, 0.6), _supp("single_cell_transcriptome", 0.5, 0.6)]
    r = adjudicate("sunitinib", "renal cell carcinoma", ev)
    assert r["verdict"] == "prioritize_for_validation"


def test_weights_are_transparent():
    assert DEFAULT_WEIGHTS["trial_forensics"] >= DEFAULT_WEIGHTS["mri_imaging"]


# --- temporality / pre-outcome enforcement ----------------------------------

from phoenix import temporality


def test_is_pre_outcome():
    assert temporality.is_pre_outcome("2010-01-01", "2011-02-01") is True
    assert temporality.is_pre_outcome("2015-01-01", "2011-02-01") is False
    assert temporality.is_pre_outcome(None, "2011-02-01") is None      # unknown -> not eligible
    assert temporality.is_pre_outcome("2010-01-01", None) is None


def _dated(channel, s, c, date, indication="prostate cancer"):
    return Evidence("zibotentan", indication, channel, f"{channel}",
                    direction="supports_rescue" if s >= 0 else "contradicts_rescue",
                    support_score=s, confidence=c, coverage={"datasets": 1}, evidence_date=date)


def test_pre_outcome_excludes_post_outcome_evidence():
    ev = [_dated("tissue_transcriptome", -0.8, 0.6, "2014-12-01"),   # POST 2011 cutoff
          _dated("trial_forensics", 0.5, 0.6, "2009-01-01")]         # PRE
    rec = adjudicate("zibotentan", "prostate cancer", ev, outcome_cutoff="2011-02-01")
    # retrospective sees both
    assert set(rec["observed_channels"]) == {"tissue_transcriptome", "trial_forensics"}
    # pre-outcome sees only the pre-dated one
    assert rec["pre_outcome"]["observed_channels"] == ["trial_forensics"]
    excluded = {x["channel"] for x in rec["pre_outcome"]["excluded_post_outcome"]}
    assert "tissue_transcriptome" in excluded


def test_pre_outcome_admissible_only_with_eligible_evidence():
    # all evidence post-outcome -> not admissible
    ev = [_dated("tissue_transcriptome", -0.8, 0.7, "2014-12-01")]
    rec = adjudicate("zibotentan", "prostate cancer", ev, outcome_cutoff="2011-02-01")
    assert rec["pre_outcome"]["admissible"] is False
    assert rec["pre_outcome"]["n_observed"] == 0
    # one pre-dated channel -> admissible
    ev2 = ev + [_dated("perturbation_reversal", -0.6, 0.6, "2009-01-01")]
    rec2 = adjudicate("zibotentan", "prostate cancer", ev2, outcome_cutoff="2011-02-01")
    assert rec2["pre_outcome"]["admissible"] is True
    assert rec2["pre_outcome"]["n_observed"] == 1


def test_evidence_date_resolves_from_source_registry():
    # no explicit evidence_date -> resolved from sources via temporality.SOURCE_DATE
    e = Evidence("sunitinib", "renal cell carcinoma", "tissue_transcriptome", "t",
                 direction="supports_rescue", support_score=0.5, confidence=0.8,
                 sources=["GSE53757"])
    rec = adjudicate("sunitinib", "renal cell carcinoma", [e])  # cutoff from registry (2006)
    pc = rec["per_channel"][0]
    assert pc["evidence_date"] == "2014-02-01"
    assert pc["pre_outcome_eligible"] is False     # 2014 GEO post-dates 2006 approval
    assert rec["temporality"]["outcome_cutoff"] == "2006-01-26"


def test_trial_study_id_resolves_to_pre_outcome_date():
    # control-arm trial_forensics carries study_ids, not GEO accessions. Their enrollment-era
    # dates live in temporality.TRIAL_DATE and must resolve through the same lookup, making the
    # control-arm prognostic signal admissible BEFORE the trial readout.
    assert temporality.source_date("Prostat_AstraZe_2009_144") == "2009-01-01"
    e = Evidence("zibotentan", "prostate cancer", "trial_forensics", "control-arm forensics",
                 direction="supports_rescue", support_score=0.28, confidence=0.6,
                 sources=["Prostat_AstraZe_2008_103", "Prostat_AstraZe_2009_144"])
    rec = adjudicate("zibotentan", "prostate cancer", [e])  # cutoff from registry (2011-02-01)
    pc = rec["per_channel"][0]
    assert pc["evidence_date"] == "2009-01-01"        # latest pooled study, still pre-readout
    assert pc["pre_outcome_eligible"] is True          # 2009 < 2011 ENTHUSE failure
    assert rec["pre_outcome"]["admissible"] is True
    assert "trial_forensics" in rec["pre_outcome"]["observed_channels"]


def test_retrospective_backcompat_keys_present():
    ev = [_supp("trial_forensics", 0.5, 0.6)]
    rec = adjudicate("sunitinib", "rcc", ev)
    for k in ("verdict", "rescue_rank", "coverage_score", "observed_channels", "per_channel"):
        assert k in rec
    assert "pre_outcome" in rec and "temporality" in rec
