#!/usr/bin/env python3
"""Gate 3 of the MVA Track 2 funnel: the paediatric safety gate.

    python3 -m scripts.mva.gate3_safety
    python3 -m scripts.mva.gate3_safety --write

WHY THIS GATE IS THE CENTRE OF THE SUBMISSION, not a compliance step.

The patient is a child whose tumour risk is driven by chromosome missegregation.
Yost et al., Nat Genet 2017 (doi:10.1038/ng.3883) show that risk in MVA tracks
the severity of spindle-checkpoint impairment and is high for biallelic BUB1B,
which is this child's genotype. Two consequences follow, and they point the
opposite way to the mechanism arms:

  1. Immunosurveillance is part of what contains that risk. Arm A's strongest
     mechanistic candidates are TNF blockers and JAK inhibitors — precisely the
     classes carrying black-box CARCINOGENICITY warnings. The best mechanistic
     fit and the worst safety fit are the same molecules.

  2. A genotoxic or cytotoxic agent adds DNA damage to cells that already
     missegregate chromosomes. Antineoplastics are therefore refused here on
     mechanism, not merely on toxicity grade.

So this gate is expected to REFUSE most of what Gate 2 produced. A funnel whose
safety gate passes everything has not been tested; one that refuses its own best
candidates has. What survives is what the report can honestly propose.

WHAT IT CHECKS, and from where.

  withdrawn        Open Targets drugWarnings warningType == "Withdrawn".
                   Hard refusal, no argument.
  carcinogenicity  drugWarnings toxicityClass. In a cancer-predisposition
                   syndrome this is disqualifying rather than a caution.
  cytotoxic        ATC L01 (antineoplastic). Refused per (2) above.
  immunosuppress   ATC L04A, plus an "infectious disease" warning class.
                   Caution, not refusal — the degree matters and IL-1 blockade
                   is not equivalent to broad T-cell suppression.
  chaperone        Targets HSP90/HSP70/HSF1 with an inhibitory mechanism. REFUSED,
                   and the only rule here that is conditional on the GENOTYPE
                   rather than on the drug: this child's entire BubR1 supply is a
                   destabilised missense allele held up by chaperone-dependent
                   quality control, and HSP90 inhibition is measured to remove
                   virtually all destabilised BubR1 (Suijkerbuijk 2010). It would
                   deepen the precise deficit causing the disease. No drug-drug
                   interaction check can see this, because the interaction is with
                   the patient's genotype. Turn it off via
                   PATIENT_HAS_DESTABILISED_ALLELE for a genotype with no
                   destabilised protein to protect.
  route            ATC first letter S (sensory organs) or D (dermatological)
                   means the approved product is TOPICAL. A topical eye drop
                   cannot deliver systemic chemoprevention, so it fails on
                   exposure regardless of its target. This catches Arm B's
                   ophthalmic NSAIDs, which the mechanism gate could not.

WHAT IT DOES NOT DO. It does not establish paediatric dosing, and absence of a
paediatric warning is NOT evidence of paediatric safety. Every survivor carries
`paediatric_evidence: unestablished` until Gate 4 looks for it in the literature
and the trial registries. Nothing here is clinical advice; these are hypotheses
for follow-up, which is what the hackathon asks for.
"""
import argparse, json, pathlib, time, urllib.request

API = "https://api.platform.opentargets.org/api/v4/graphql"
DATA = pathlib.Path(__file__).resolve().parents[2] / "data" / "mva"
G2B, OUT = DATA / "gate2b.json", DATA / "gate3.json"

CARCINOGENIC = {"carcinogenicity"}
INFECTION = {"infectious disease"}

# ---------------------------------------------------------------------------
# A GENOTYPE-CONDITIONAL REFUSAL: do not strip the chaperone machinery that is
# holding up the patient's only functional allele.
#
# This child's allele 1 is transcript-null (NMD; P(escape) 0.316 on a calibrated
# model), so his ENTIRE supply of BubR1 comes from allele 2, a destabilised
# missense variant cleared by chaperone-dependent quality control. Suijkerbuijk
# 2010 showed DIRECTLY that HSP90 inhibition removes virtually all destabilised
# BubR1. So an HSP90 inhibitor would deepen the exact deficit driving the disease.
#
# This is the symmetric twin of the rule in C5, and it is the reason this gate is
# worth encoding rather than leaving in prose: the contraindication is invisible to
# every standard interaction check, because the drug is not interacting with
# anything the patient is taking -- it is interacting with his genotype.
#
# IT IS CONDITIONAL, AND THAT IS THE POINT. The rule fires only for a patient whose
# functional allele is a destabilised missense protein. A patient with two
# truncating alleles has no destabilised protein to strip, and the rule must NOT
# fire for them. It therefore generalises to any gene: the input is a genotype
# class, not a gene name.
#
# Evidence tiers are kept separate because they are not equal:
#   measured  -- the chaperone was shown to clear THIS protein when inhibited
#   inferred  -- same axis, same direction, but not measured on this protein
CHAPERONE_TARGETS = {
    # HSP90 family. Measured on BubR1 (Suijkerbuijk 2010): geldanamycin removes
    # destabilised BubR1 while wild-type is spared -- the differential is what
    # establishes the mechanism rather than general toxicity.
    "HSP90AA1": "measured", "HSP90AB1": "measured", "HSP90B1": "measured",
    # HSP70 and its co-induction axis. Inhibiting the chaperone the lead arm sets
    # out to AMPLIFY is the same error with the sign flipped. Not measured on BubR1.
    "HSPA1A": "inferred", "HSPA1B": "inferred", "HSPA8": "inferred",
    "HSF1": "inferred",
}
# An activator or co-inducer of these targets is the therapeutic hypothesis, not a
# hazard, so only inhibitory mechanisms are refused.
INHIBITORY_ACTIONS = {"INHIBITOR", "ANTAGONIST", "DEGRADER", "BLOCKER",
                      "NEGATIVE MODULATOR", "NEGATIVE ALLOSTERIC MODULATOR"}
# Set False when the patient has no destabilised-missense allele to protect.
PATIENT_HAS_DESTABILISED_ALLELE = True
# ATC letters are ANATOMICAL groups, not routes. "D" (dermatologicals) contains
# ORAL drugs for skin disease — abrocitinib is D11AH08 and is a systemic tablet,
# so treating "D" as topical was a false positive on the first run. Only the
# sensory-organ groups are reliably topical at the level ATC can tell us.
TOPICAL_ATC_PREFIXES = ("S01", "S02", "S03")
ROUTE_UNVERIFIABLE_PREFIX = "D"
BATCH = 10


def gql(query, variables=None, tries=3):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=body,
                                 headers={"Content-Type": "application/json"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                d = json.loads(r.read())
            if "errors" in d:
                raise RuntimeError(d["errors"][0]["message"][:200])
            return d["data"]
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 ** i)


def warnings_batch(ids):
    decl = ",".join(f"$c{i}:String!" for i in range(len(ids)))
    body = " ".join(
        f"w{i}:drug(chemblId:$c{i}){{name drugWarnings"
        f"{{warningType toxicityClass description year country}}}}"
        for i in range(len(ids)))
    return gql(f"query({decl}){{{body}}}", {f"c{i}": c for i, c in enumerate(ids)})


def adjudicate(row, warns):
    atc = row.get("atc") or []
    lv1 = {a[0] for a in atc}
    wtypes = {(w.get("warningType") or "").lower() for w in warns}
    tox = {(w.get("toxicityClass") or "").lower() for w in warns if w.get("toxicityClass")}

    reasons = []
    verdict = "proceed_with_monitoring"

    if "withdrawn" in wtypes:
        return "refuse_withdrawn", ["withdrawn from market (Open Targets drugWarnings)"], tox

    if any(a.startswith("L01") for a in atc):
        verdict = "refuse_cytotoxic"
        reasons.append("ATC L01 antineoplastic: adds DNA damage to cells that "
                       "already missegregate chromosomes")

    if tox & CARCINOGENIC:
        verdict = "refuse_carcinogenicity" if verdict == "proceed_with_monitoring" else verdict
        reasons.append("black-box carcinogenicity warning, in a child with a "
                       "cancer-predisposition syndrome")

    # Chaperone-dependency refusal. Genotype-conditional -- see CHAPERONE_TARGETS.
    if PATIENT_HAS_DESTABILISED_ALLELE:
        actions = {str(x).upper() for x in (row.get("actions") or [])}
        hits = sorted(set(row.get("targets") or {}) & set(CHAPERONE_TARGETS))
        # No recorded action is not evidence of a non-inhibitory one. Open Targets
        # leaves `actions` empty often enough that treating empty as "safe" would
        # silently void the rule, so an unknown action is refused and labelled.
        inhibitory = (not actions) or bool(actions & INHIBITORY_ACTIONS)
        if hits and inhibitory:
            tiers = {CHAPERONE_TARGETS[h] for h in hits}
            tier = "measured" if "measured" in tiers else "inferred"
            verdict = "refuse_chaperone_dependency"
            reasons.append(
                f"inhibits the chaperone machinery holding up this patient's only "
                f"functional allele ({', '.join(hits)}; evidence: {tier}"
                f"{', action not recorded — refused on the precautionary side' if not actions else ''}). "
                f"His allele 1 is transcript-null, so all BubR1 comes from a "
                f"destabilised missense allele cleared by chaperone-dependent QC; "
                f"HSP90 inhibition is shown to remove virtually all of it "
                f"(Suijkerbuijk 2010). Invisible to any drug-drug interaction check")

    if atc and all(a.startswith(TOPICAL_ATC_PREFIXES) for a in atc):
        verdict = "refuse_no_systemic_exposure"
        reasons.append(f"approved product is topical, sensory-organ only "
                       f"(ATC {sorted(atc)}); cannot deliver systemic effect")
    elif atc and all(a.startswith(ROUTE_UNVERIFIABLE_PREFIX) for a in atc):
        reasons.append(f"ATC {sorted(atc)} is dermatological, which does NOT "
                       "settle route — the group holds both oral and topical "
                       "products. Route must be checked per product at Gate 4")

    if verdict == "proceed_with_monitoring":
        if any(a.startswith("L04A") for a in atc):
            reasons.append("immunosuppressant (ATC L04A): degree of "
                           "immunosurveillance loss must be argued explicitly")
            verdict = "caution_immunosuppression"
        if tox & INFECTION:
            reasons.append("black-box infection warning")
            verdict = "caution_immunosuppression"

    return verdict, reasons or ["no disqualifying signal found"], tox


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    if not G2B.exists():
        raise SystemExit(f"missing {G2B} — run gate2b_reverse.py --write first")
    cands = json.loads(G2B.read_text())["candidates"]
    ids = [c["chembl"] for c in cands]

    warns = {}
    for i in range(0, len(ids), BATCH):
        chunk = ids[i:i + BATCH]
        data = warnings_batch(chunk)
        for j, cid in enumerate(chunk):
            d = data.get(f"w{j}") or {}
            warns[cid] = d.get("drugWarnings") or []

    out, tally = [], {}
    for c in cands:
        verdict, reasons, tox = adjudicate(c, warns.get(c["chembl"], []))
        r = dict(c)
        r.update(verdict=verdict, safety_reasons=reasons,
                 toxicity_classes=sorted(tox),
                 paediatric_evidence="unestablished")
        out.append(r)
        tally[verdict] = tally.get(verdict, 0) + 1

    order = ["proceed_with_monitoring", "caution_immunosuppression",
             "refuse_carcinogenicity", "refuse_cytotoxic",
             "refuse_no_systemic_exposure", "refuse_withdrawn"]
    print(f"Gate 2 candidates in: {len(cands)}\n")
    for v in order:
        if v not in tally:
            continue
        print(f"{v}  ({tally[v]})")
        for r in sorted(out, key=lambda x: x["inn"]):
            if r["verdict"] != v:
                continue
            arms = ",".join(sorted(r["arms"]))
            bs = " [biosimilar]" if r["biosimilar_flag"] else ""
            print(f"   {r['inn']:<22} {arms:<26}{bs}")
            for why in r["safety_reasons"]:
                print(f"       - {why}")
        print()

    survivors = [r for r in out if r["verdict"].startswith(("proceed", "caution"))]
    print(f"SURVIVING GATE 3: {len(survivors)} of {len(cands)}")

    if a.write:
        OUT.write_text(json.dumps(
            {"gate": 3, "api": API, "in": len(cands),
             "tally": tally, "surviving": len(survivors),
             "candidates": sorted(out, key=lambda r: (r["verdict"], r["inn"]))},
            indent=1) + "\n")
        print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
