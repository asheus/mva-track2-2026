"""The chaperone-dependency refusal in Gate 3 must fire, and must not over-fire.

Written because the rule refuses NOTHING in the live funnel: no HSP90 inhibitor is
approved, so Gate 1's approval tiering removes the whole class before Gate 3 sees
it. A rule that never fires is indistinguishable from a rule that does not work,
and the project's standing practice is that an instrument reporting no change must
first be shown capable of reporting one. These are that demonstration.

    python3 -m pytest apps/api/tests/test_gate3_chaperone.py -q
"""
import pytest

from scripts.mva import gate3_safety as g3


def _row(targets, actions=("INHIBITOR",), atc=("L01XX",)):
    return {"inn": "synthetic", "atc": list(atc), "actions": list(actions),
            "targets": {t: "synthetic test target" for t in targets}}


def test_hsp90_inhibitor_is_refused():
    v, reasons, _ = g3.adjudicate(_row(["HSP90AA1"]), [])
    assert v == "refuse_chaperone_dependency", v
    assert any("chaperone machinery" in r for r in reasons)
    assert any("measured" in r for r in reasons)


def test_hsf1_inhibitor_is_refused_on_the_weaker_tier():
    v, reasons, _ = g3.adjudicate(_row(["HSF1"], atc=("N05XX",)), [])
    assert v == "refuse_chaperone_dependency"
    # HSF1 inhibition is the lead arm with the sign flipped, but it has not been
    # measured on BubR1, and the reason string must not claim that it has.
    assert any("inferred" in r for r in reasons)
    assert not any("evidence: measured" in r for r in reasons)


def test_an_activator_of_the_same_target_is_not_refused():
    # Co-inducing HSF1 IS the therapeutic hypothesis. If the rule caught activators
    # it would refuse the lead candidate, which is the failure mode worth guarding.
    v, _, _ = g3.adjudicate(_row(["HSF1"], actions=("ACTIVATOR",), atc=("N05XX",)), [])
    assert v != "refuse_chaperone_dependency", v


def test_unknown_action_is_refused_not_waved_through():
    # Open Targets leaves `actions` empty often enough that treating empty as
    # non-inhibitory would silently void the rule.
    v, reasons, _ = g3.adjudicate(_row(["HSP90AB1"], actions=()), [])
    assert v == "refuse_chaperone_dependency"
    assert any("action not recorded" in r for r in reasons)


def test_rule_is_off_for_a_genotype_with_nothing_to_protect():
    # A patient with two truncating alleles has no destabilised protein to strip.
    # The rule must be conditional on the genotype, not hardcoded to the gene.
    g3.PATIENT_HAS_DESTABILISED_ALLELE = False
    try:
        v, _, _ = g3.adjudicate(_row(["HSP90AA1"], atc=("N05XX",)), [])
        assert v != "refuse_chaperone_dependency", v
    finally:
        g3.PATIENT_HAS_DESTABILISED_ALLELE = True


def test_a_non_chaperone_drug_is_untouched():
    v, _, _ = g3.adjudicate(_row(["IL1R1"], atc=("L04AC03",)), [])
    assert v != "refuse_chaperone_dependency", v


def test_withdrawn_still_short_circuits_everything():
    # The withdrawn check returns before any other rule; adding ours must not have
    # moved it.
    v, _, _ = g3.adjudicate(_row(["HSP90AA1"]), [{"warningType": "Withdrawn"}])
    assert v == "refuse_withdrawn", v
