#!/usr/bin/env python3
"""Re-rank every approach with viability as a GATE, not a criterion.

    python3 -m scripts.mva.viability_gate

WHY THIS SUPERSEDES approach_matrix.py. That script scored viability as one axis among
eight and let a composite average it away. The result ranked trans-splicing first -- and
the very next piece of work established that trans-splicing has **no approved drug, no
molecule in any clinical trial, and no RTM ever given to a patient for any gene**, thirty
years after the modality was demonstrated. A ranking that puts a non-existent drug first
is not a ranking, it is a preference.

So viability is applied here as a gate. An approach that cannot reach a patient does not
compete for first place regardless of how elegant its mechanism is. It can still be
recorded, and it can still be the right long-term bet, but it cannot be the recommendation.

THE GATE
  3  obtainable now        -- approved, in trials, or otherwise available to a patient
  2  in clinical trials    -- the molecule exists and is being given to humans
  1  preclinical only      -- the class exists; nothing has entered a human
  0  no molecule           -- nothing to administer

Only 2 and 3 may be recommended. 1 and 0 are recorded as directions, not options.

WHAT THE GATE DOES NOT DO. It says nothing about whether an approach WORKS. An obtainable
drug aimed at the wrong variable is still wrong, which is why the second column stays:
does the approach address the deficit this genotype actually has.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
OUT = ROOT / "docs/mva/data/viability_gate.json"

# name, viability 0-3, addresses-the-deficit 0-2, evidence-in-BUB1B 0-2, note
ROWS = [
 ("NAD+ precursor (NMN / NR)", 3, 2, 2,
  "available now; 153 registered trials incl. rare monogenic disease and an n=1 in "
  "Li-Fraumeni at NIH. NMN raised BubR1 abundance in vivo (North 2014). Targets "
  "DEGRADATION -- which is also the timed event that releases anaphase."),
 ("Arimoclomol (heat-shock response amplifier)", 3, 2, 0,
  "NEW. Amplifies HSF1/HSP70 to assist misfolded proteins. 12 trials incl. Phase 3 in "
  "ALS, and an OPEN EXPANDED-ACCESS programme for Niemann-Pick C (NCT04316637, status "
  "AVAILABLE, 13 US sites) -- a real route for an n-of-1. Targets FOLDING, so it does "
  "not touch the degradation clock. No evidence in BUB1B."),
 ("4-phenylbutyrate (chemical chaperone)", 3, 2, 0,
  "NEW. Approved for urea cycle disorders in CHILDREN; trialled explicitly as a folding "
  "'corrector' in cystic fibrosis (NCT02323100) and for a destabilising missense in MCAD "
  "deficiency (NCT06069375) -- the closest precedent in shape to N1002K. CAVEAT: 4-PBA "
  "is also a weak HDAC inhibitor, which collides with the K250/K668 argument."),
 ("Combination: folding corrector + degradation modulator", 3, 2, 0,
  "NEW. The CFTR precedent: single agents failed and the approved therapy is a "
  "corrector-plus-potentiator combination. Two obtainable drugs, two mechanisms, one "
  "variable. Untested together and the interaction is unknown."),
 ("Cancer-risk stratification from the allele map", 3, 0, 2,
  "not a drug; needs no new biology; the only output that is actionable this year."),
 ("mTORC1 inhibition (sirolimus) / senolytics", 3, 0, 1,
  "obtainable, but treats accrued damage and cannot prevent mis-segregation."),
 ("Haematopoietic stem cell transplant", 3, 0, 0,
  "NEW. Established in other chromosome-instability syndromes and genuinely obtainable, "
  "but it addresses marrow and leukaemia risk only -- MVA's characteristic tumours are "
  "solid -- at high morbidity."),
 ("Readthrough (ataluren / aminoglycoside)", 3, 0, 0,
  "class obtainable, but only 4 of 2,536 alleles qualify and this child's is not one."),
 ("Partial proteasome inhibition", 3, 1, 0,
  "NEW. Approved drugs exist and it is on-target for degradation -- and it is "
  "non-specific and severely toxic. Listed so it is visibly rejected, not omitted."),
 ("HDAC inhibition", 3, 0, 0,
  "obtainable, and argued against: K250 stabilises BubR1 while K668 destabilises it."),
 ("Prime editing, ex vivo", 2, 1, 0,
  "editing is in human trials; corrects blood, and MVA's tumours are solid."),
 ("AAV gene replacement", 2, 1, 0,
  "deliverable, but a constitutive source fills the anaphase trough -- a mechanism veto."),
 ("trans-RNA translation initiation", 1, 2, 0,
  "Nat Biotechnol, Nov 2025. Right variable, right layer, no human has received one."),
 ("Trans-splicing (SMaRT)", 1, 2, 0,
  "best mechanism fit and the only route to allele 1 -- and NO RTM for any gene has ever "
  "been given to a patient. Required efficiency 23-38% exceeds published RTMs."),
 ("CRISPRa at the native promoter", 1, 2, 0,
  "not deliverable to a child; the right EXPERIMENT for the dosage thesis."),
 ("Pharmacological chaperone, pseudokinase pocket", 0, 1, 0,
  "no molecule; not evaluable -- no structure of 766-1050 above 3.8 A."),
 ("Checkpoint timing extension", 1, 1, 0,
  "only idea reaching the 280 transcript-less alleles; mitotic drugs are cytotoxic."),
 ("Splice-modulating ASO (TANGO)", 0, 0, 0,
  "KILLED: non-canonical junction flux 0.00% vs SCN1A 4.55%."),
 ("APC/C-Cdc20 inhibition", 0, 1, 0, "arrests every mitosis."),
 ("Neoantigen vaccine", 0, 0, 0, "germline variant; it would target the patient."),
]
LABEL = {3: "obtainable now", 2: "in trials", 1: "preclinical", 0: "no molecule"}


def main():
    print("=" * 100)
    print("VIABILITY GATE -- can this reach a patient at all?")
    print("=" * 100)
    print(f"  {'approach':<48}{'viability':>16}{'addresses':>11}{'inBUB1B':>9}")
    print("  " + "-" * 96)
    for n, v, a, e, _ in sorted(ROWS, key=lambda r: (-r[1], -r[2], -r[3])):
        print(f"  {n:<48}{LABEL[v]:>16}{a:>11}{e:>9}")

    passed = [r for r in ROWS if r[1] >= 2]
    blocked = [r for r in ROWS if r[1] < 2]

    print("\n" + "=" * 100)
    print(f"THROUGH THE GATE ({len(passed)} of {len(ROWS)}) -- ranked by whether they "
          f"address THIS genotype's deficit")
    print("=" * 100)
    for i, (n, v, a, e, note) in enumerate(
            sorted(passed, key=lambda r: (-r[2], -r[3], -r[1])), 1):
        print(f"  {i}. {n}   [{LABEL[v]}]")
        print(f"     addresses the deficit: {a}/2   evidence in BUB1B: {e}/2")
        print(f"     {note}\n")

    print("=" * 100)
    print(f"BLOCKED BY THE GATE ({len(blocked)}) -- directions, not options")
    print("=" * 100)
    for n, v, a, e, note in sorted(blocked, key=lambda r: (-r[2], -r[1])):
        print(f"  {n}  [{LABEL[v]}, addresses {a}/2]")
        print(f"    {note}")

    top = sorted(passed, key=lambda r: (-r[2], -r[3], -r[1]))[0]
    print("\n" + "=" * 100)
    print("THE RECOMMENDATION")
    print("=" * 100)
    print(f"  {top[0]} is the only approach that is BOTH obtainable and aimed at the")
    print("  deficit this genotype has. It is the recommendation by elimination, not by")
    print("  enthusiasm -- everything with a better mechanism has no molecule, and")
    print("  everything else obtainable is aimed at something else.")
    print("\n  It is still conditional on one unmeasured fact: that p.Asn1002Lys reduces")
    print("  BubR1 ABUNDANCE. If the N1002R lane and the pT1008 blot say otherwise, this")
    print("  recommendation is aimed at the wrong variable too.")

    OUT.write_text(json.dumps({
        "supersedes": "approach_matrix.py, which averaged viability away and ranked a "
                      "non-existent drug first",
        "gate": {str(k): v for k, v in LABEL.items()},
        "rows": [{"name": n, "viability": v, "viability_label": LABEL[v],
                  "addresses_deficit": a, "evidence_in_bub1b": e, "note": note}
                 for n, v, a, e, note in ROWS],
        "passed_gate": [r[0] for r in passed],
        "blocked_by_gate": [r[0] for r in blocked],
        "recommendation": top[0],
        "recommendation_is_conditional_on":
            "p.Asn1002Lys reducing BubR1 abundance -- untested",
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
