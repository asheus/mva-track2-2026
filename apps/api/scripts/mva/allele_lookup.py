#!/usr/bin/env python3
"""One row per BUB1B allele: predicted mechanism, and the experiment that would settle it.

    python3 -m scripts.mva.allele_lookup

WHY THIS FILE EXISTS. The evidence for every allele was already computed and it was
scattered: NMD verdicts in the splice/truncation arm, folding verdicts in the missense
arm, structural context in a third place. A clinician or a researcher arriving with one
variant had to know which of our files to open. That is not a scalable deliverable, it is
a pile of correct answers.

This produces the lookup: **give it any BUB1B allele and it returns what is predicted to
happen at the transcript level, what is predicted to happen at the protein level, how
strong that evidence is, and the single experiment that would confirm or refute it.**

THE LAST COLUMN IS THE POINT. A predicted map that only labels variants invites the
reader to treat a prediction as a result -- which is the failure mode this project has
spent 43 corrections avoiding. Every row therefore names its own falsification. A row
whose experiment cannot be stated has no business being called a result.

NOTHING HERE IS NEW SCIENCE. It is a join over outputs that already exist and were
already committed, so no claim is introduced that was not already tested:

    eligibility_map.tsv      2,536 alleles: class, eligibility, evidence tier
    missense_arm.tsv         the buried-charge axis (validated C41, NOT demonstrated
                             in BUB1B itself -- C43), applied where it applies
    noncoding_eligibility.tsv  splice calls with their confidence tier

CALIBRATION TRAVELS WITH THE ROW. The splice tier's operating characteristics are
measured on a sealed split: at the `call` threshold sensitivity 0.392 / specificity 0.986
(precision 0.48 at the 3.2% base rate), at `candidate` 0.793 / 0.872 (precision 0.17).
A reader of any splice row is entitled to know that at the screening tier roughly four
calls in five are wrong, so the summary prints it and the README repeats it.

WHAT THIS IS NOT. Predicted, not assayed. Fabry's equivalent map is determined by a
GLP-validated assay over 1,386 variants and is used for real drug eligibility; this is a
shortlist and a coverage statement. No row is an amenability call, and no row is advice
about any individual.
"""
import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
D = ROOT / "docs/mva/data"
MAP = D / "nmd/eligibility_map.tsv"
MISSENSE = D / "missense_arm.tsv"
SPLICE = D / "nmd/noncoding_eligibility.tsv"
OUT = D / "allele_lookup.tsv"
META = D / "allele_lookup.json"

# eligibility class -> (transcript-level verdict, protein-level verdict, settling experiment)
# The experiment is the discriminating one: it must be able to come back the other way.
VERDICT = {
    "NULL_no_protein": (
        "PTC; decay predicted",
        "none expected",
        "RT-qPCR for transcript level, +/- NMD inhibition, then western for BubR1"),
    "NULL_pending_NMD_of_new_PTC": (
        "skip creates a new PTC; decay predicted",
        "none expected",
        "RT-PCR across the predicted junction to confirm the skip, then western"),
    "TRUNCATED_protein_present": (
        "PTC past the last junction; escapes decay",
        "truncated species expected",
        "western for the truncated species; checkpoint assay for residual function"),
    "HYPOMORPH_protein_made": (
        "in-frame skip; transcript stable",
        "internally deleted protein expected",
        "RT-PCR to confirm the in-frame skip, western for the shortened species"),
    "ABUNDANCE_question_answerable": (
        "no transcript-level defect predicted",
        "abundance is the open question; residue is buried and confidently modelled",
        "ectopic expression + western against wild-type, with a tolerated "
        "same-residue substitution as the internal control"),
    "ABUNDANCE_candidate": (
        "no transcript-level defect predicted",
        "abundance plausibly reduced",
        "ectopic expression + western against wild-type"),
    "FUNCTION_class_suspected": (
        "no transcript-level defect predicted",
        "abundance likely normal; defect expected in binding or activity",
        "co-immunoprecipitation / checkpoint assay, not an abundance western"),
    "AMBIGUOUS_partially_buried": (
        "no transcript-level defect predicted",
        "burial too ambiguous to class",
        "ectopic expression + western; the assay answers it where the structure cannot"),
    "CONTEXT_UNAVAILABLE": (
        "no transcript-level defect predicted",
        "no structural context in the model",
        "ectopic expression + western; no structural prediction is offered"),
    "NO_SPLICE_MECHANISM": (
        "scored for splice effect; none detected",
        "not addressed by the splice arm",
        "assess as a coding variant; a negative splice call is weak evidence "
        "(screening-tier sensitivity 0.793)"),
    "PENDING_not_yet_scored": (
        "not yet scored", "not yet scored", "run the splice sweep for this variant"),
}


def tsv(p):
    if not p.exists():
        return []
    lines = p.read_text().strip().split("\n")
    cols = lines[0].split("\t")
    return [dict(zip(cols, L.split("\t"))) for L in lines[1:]]


def main():
    rows = tsv(MAP)
    if not rows:
        sys.exit(f"missing or empty {MAP}")
    missense = {r["variant"]: r for r in tsv(MISSENSE)}
    splice_tier = {}
    for r in tsv(SPLICE):
        key = (r.get("hgvs_c") or "").strip() or f"chr15:{r.get('pos','')}"
        splice_tier[key] = r.get("tier", "")

    out, tally, no_experiment = [], collections.Counter(), 0
    for r in rows:
        elig = r["eligibility"]
        tx, prot, exp = VERDICT.get(
            elig, ("not classified", "not classified", ""))
        if not exp:
            no_experiment += 1
        allele = (r.get("residue") or "").strip() or r["variant"]
        # the missense arm's axis call, where the validated axis applies at all
        axis = ""
        m = missense.get(allele) or missense.get(r.get("variant", ""))
        if m:
            axis = m.get("axis_class", "")
            if axis == "ABUNDANCE_RISK_buried_new_charge":
                prot = ("buries a new charge at a buried position -- the one axis "
                        "validated against measured abundance (C41)")
        tier = splice_tier.get(r.get("variant", ""), "")
        tally[elig] += 1
        out.append({
            "allele": allele,
            "class": r["variant_class"],
            "clinvar": r.get("clinvar_significance", ""),
            "transcript_level": tx,
            "protein_level": prot,
            "evidence_tier": r.get("evidence_status", ""),
            "splice_call_tier": tier,
            "missense_axis": axis,
            "settling_experiment": exp,
            "metric": r.get("metric", ""),
        })

    cols = ["allele", "class", "clinvar", "transcript_level", "protein_level",
            "evidence_tier", "splice_call_tier", "missense_axis",
            "settling_experiment", "metric"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        f.write("\t".join(cols) + "\n")
        for o in out:
            f.write("\t".join(str(o.get(c, "")).replace("\t", " ") for c in cols) + "\n")

    print(f"{len(out)} alleles, one row each -> {OUT.relative_to(ROOT)}")
    print(f"\nevery row names its own falsification; rows with no experiment: "
          f"{no_experiment}")
    print("\nBY PREDICTED MECHANISM")
    for k, v in tally.most_common():
        tx = VERDICT.get(k, ("?",))[0]
        print(f"  {k:32s} {v:5d}   {tx}")

    tx_decay = sum(v for k, v in tally.items() if "decay predicted" in
                   VERDICT.get(k, ("",))[0])
    protein_made = sum(v for k, v in tally.items()
                       if VERDICT.get(k, ("", ""))[1].startswith(
                           ("truncated", "internally deleted")))
    print(f"\n  transcript-level defect predicted (decay): {tx_decay}")
    print(f"  protein predicted present despite the lesion: {protein_made}")

    META.write_text(json.dumps({
        "alleles": len(out),
        "rows_without_a_settling_experiment": no_experiment,
        "by_mechanism": dict(tally),
        "splice_tier_operating_characteristics": {
            "call": {"threshold": 0.16, "sensitivity": 0.392, "specificity": 0.986,
                     "precision_at_3.2pct": 0.481},
            "candidate": {"threshold": 0.02, "sensitivity": 0.793, "specificity": 0.872,
                          "precision_at_3.2pct": 0.170},
            "measured_on": "sealed quarter of 946 assayed MFASS variants, opened once"},
        "missense_axis_status": "validated against measured abundance in PTEN, TPMT and "
                                "NUDT15 (C41); NOT demonstrated in BUB1B's own labelled "
                                "variants (C43, OR 5.76, p=0.1193)",
        "caveat": "Predicted, not assayed. No row is an amenability call and no row is "
                  "advice about any individual.",
    }, indent=2) + "\n")
    print(f"wrote {META.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
