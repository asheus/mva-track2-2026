#!/usr/bin/env python3
"""Every therapeutic approach considered, scored on criteria we actually measured.

    python3 -m scripts.mva.approach_matrix

WHY A SCRIPT AND NOT A LIST. A ranking is an argument, and the usual way it goes wrong is
that the weights are chosen after the preferred answer. So the criteria here are only ones
this project measured, the weights are declared in the file, and the last section
**re-ranks under four different weightings** to show which positions are stable and which
are artefacts of how I weighted them. A result that moves under reasonable re-weighting is
reported as unstable rather than as a finding.

THE CRITERIA, and where each came from
  reaches_a1      can it act on p.Leu737Ter? Only the pre-mRNA and DNA layers can, because
                  NMD destroys the mature message (MODALITY-LAYERS.md)
  reaches_a2      can it act on p.Asn1002Lys?
  waveform        does it inherit BubR1's cell-cycle oscillation, or must it manufacture
                  one? (DOSAGE-TIMING.md -- a limiter solves a ceiling, not a waveform)
  map_coverage    of the 2,536 catalogued alleles, how many could this modality reach at
                  all? (allele_lookup.tsv; 280 lose the transcript outright)
  invivo_bub1b    is there in-vivo evidence it raises THIS protein?
  in_humans       has the modality been in people, in any disease?
  effect_known    do we know the size of effect required? (dosage_model.py: ~1.4x)
  killable        is there a cheap experiment that could rule it out?
  our_status      what happened when we tested it here

SCORING is deliberately coarse -- 0, 1 or 2 -- because the inputs do not support more
precision, and a three-decimal score would imply a confidence we do not have.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
OUT = ROOT / "docs/mva/data/approach_matrix.json"
TOTAL_ALLELES = 2536

# name, a1, a2, waveform, coverage, invivo, humans, effect_known, killable, status, note
A = [
 ("Trans-splicing (SMaRT) of endogenous pre-mRNA", 2, 2, 2, 2536, 0, 1, 2, 2, "untested",
  "only modality reaching the dead allele; needs 23-38% efficiency"),
 ("NAD+ precursor (NMN/NR) via SIRT2/K668", 0, 2, 1, 2256, 2, 2, 2, 2, "untested",
  "only class with in-vivo evidence of raising BubR1; slows the clock it rides on"),
 ("trans-RNA initiation on endogenous mRNA", 0, 2, 2, 2256, 0, 0, 2, 1, "untested",
  "Nat Biotechnol Nov 2025; endogenous and in vivo in mouse, but weeks old"),
 ("CRISPRa at the native BUB1B promoter", 2, 2, 2, 2536, 0, 0, 2, 2, "untested",
  "not deliverable as therapy; the right experiment for the dosage thesis"),
 ("Readthrough (ataluren / G418 / ACE-tRNA)", 0, 0, 2, 4, 0, 2, 1, 2, "wrong allele",
  "needs a PTC in a surviving transcript: 4 alleles, or 284 with NMD attenuation"),
 ("Pharmacological chaperone, pseudokinase pocket", 0, 2, 2, 1494, 0, 2, 1, 0,
  "NOT EVALUABLE", "no validated tool here; no structure of 766-1050 above 3.8 A"),
 ("Checkpoint timing extension", 2, 2, 0, 2536, 0, 1, 0, 1, "untested",
  "only idea reaching the 280 transcript-less alleles; mitotic drugs are cytotoxic"),
 ("Prime editing, ex vivo", 2, 2, 2, 2536, 0, 1, 2, 0, "untested",
  "c.3006T>G is a transversion; corrects blood, and MVA's tumours are solid"),
 ("Senolytics / mTORC1 inhibition", 0, 0, 0, 2536, 0, 2, 0, 1, "downstream",
  "treats accrued damage; p21 effects are bidirectional by tissue"),
 ("APC/C-Cdc20 inhibition", 0, 2, 0, 2256, 0, 0, 1, 1, "rejected",
  "on-target but arrests every mitosis"),
 ("HDAC inhibition to raise acetylation", 0, 2, 0, 2256, 0, 2, 0, 1, "argued against",
  "K250 stabilises and K668 destabilises; net effect unpredictable"),
 ("circRNA / AAV encoding BubR1", 2, 2, 0, 2536, 0, 2, 2, 1, "argued against",
  "constitutive source fills the anaphase trough"),
 ("Splice-modulating ASO (TANGO-style)", 0, 2, 2, 0, 0, 2, 2, 2, "KILLED",
  "no poison exon; non-canonical junction flux 0.00% vs SCN1A 4.55%"),
 ("Neoantigen vaccine", 0, 0, 0, 0, 0, 2, 0, 2, "KILLED",
  "germline variant is in every cell; it would target the patient"),
]
# multipliers applied to the rest of the list, not ranked as therapies themselves
ADJUNCTS = [
 ("Mosaic selection as an amplifier", "lowers trans-splicing's bar from holding 23-38% "
  "to seeding an expanding clone -- but only in renewing tissue, not the brain"),
 ("Cancer-risk stratification from the map", "not a therapy; the only clinically "
  "actionable output available today, and it needs no new biology"),
]

WEIGHTS = {
 "default -- what to do next, no wet lab":
    {"a1": 2, "a2": 2, "wave": 2, "cov": 2, "invivo": 2, "humans": 1, "eff": 1, "kill": 3},
 "if the goal is THIS child only":
    {"a1": 3, "a2": 3, "wave": 2, "cov": 0, "invivo": 3, "humans": 2, "eff": 1, "kill": 1},
 "if the goal is the most children":
    {"a1": 1, "a2": 1, "wave": 1, "cov": 4, "invivo": 1, "humans": 1, "eff": 1, "kill": 1},
 "if the goal is fastest to a human":
    {"a1": 1, "a2": 2, "wave": 1, "cov": 1, "invivo": 3, "humans": 4, "eff": 2, "kill": 2},
}


def score(row, w):
    _n, a1, a2, wave, cov, inv, hum, eff, kill, status, _note = row
    covn = 2 * cov / TOTAL_ALLELES
    s = (w["a1"] * a1 + w["a2"] * a2 + w["wave"] * wave + w["cov"] * covn
         + w["invivo"] * inv + w["humans"] * hum + w["eff"] * eff + w["kill"] * kill)
    if status in ("KILLED", "NOT EVALUABLE", "rejected"):
        s *= 0.25            # kept visible, cannot rank high
    return s


def main():
    print("=" * 100)
    print("ALL APPROACHES CONSIDERED  (0/1/2 per criterion; coverage of 2,536 alleles)")
    print("=" * 100)
    print(f"  {'approach':<46}{'a1':>3}{'a2':>3}{'wav':>4}{'coverage':>10}"
          f"{'inVivo':>7}{'human':>6}{'kill':>5}  status")
    print("  " + "-" * 96)
    for r in A:
        n, a1, a2, wv, cov, inv, hum, eff, kill, st, _ = r
        print(f"  {n:<46}{a1:>3}{a2:>3}{wv:>4}{cov:>10,}{inv:>7}{hum:>6}{kill:>5}  {st}")

    print("\n" + "=" * 100)
    print("RANKING UNDER THE DEFAULT WEIGHTING")
    print("=" * 100)
    w0 = WEIGHTS["default -- what to do next, no wet lab"]
    ranked = sorted(A, key=lambda r: -score(r, w0))
    for i, r in enumerate(ranked, 1):
        print(f"  {i:>2}. {r[0]:<48} {score(r, w0):6.1f}   {r[10]}")

    print("\n" + "=" * 100)
    print("DOES THE RANKING SURVIVE RE-WEIGHTING?")
    print("=" * 100)
    orders = {}
    for label, w in WEIGHTS.items():
        orders[label] = [r[0] for r in sorted(A, key=lambda r: -score(r, w))]
    names = [r[0] for r in A]
    print(f"  {'approach':<48}" + "".join(f"{k.split(' -- ')[0][:11]:>13}"
                                          for k in WEIGHTS))
    print("  " + "-" * 96)
    spread = {}
    for n in names:
        pos = [orders[k].index(n) + 1 for k in WEIGHTS]
        spread[n] = max(pos) - min(pos)
        print(f"  {n:<48}" + "".join(f"{p:>13}" for p in pos))

    print("\n  STABLE (position moves by <=1 across all four weightings):")
    for n, s in sorted(spread.items(), key=lambda x: x[1]):
        if s <= 1:
            print(f"    {orders[list(WEIGHTS)[0]].index(n)+1:>2}. {n}")
    print("\n  UNSTABLE (moves by 3 or more -- the weighting is doing the work, not the evidence):")
    for n, s in sorted(spread.items(), key=lambda x: -x[1]):
        if s >= 3:
            print(f"    moves {s} places: {n}")

    print("\n" + "=" * 100)
    print("NOT RANKED AS THERAPIES")
    print("=" * 100)
    for n, note in ADJUNCTS:
        print(f"  {n}\n    {note}")

    OUT.write_text(json.dumps({
        "criteria": "reaches allele1/allele2, waveform inherited, map coverage, in-vivo "
                    "evidence in BUB1B, in humans, effect size known, cheaply killable",
        "total_alleles": TOTAL_ALLELES,
        "approaches": [dict(zip(
            ["name", "reaches_a1", "reaches_a2", "waveform", "map_coverage",
             "invivo_bub1b", "in_humans", "effect_known", "killable", "status", "note"],
            r)) for r in A],
        "weightings": WEIGHTS,
        "rank_default": [r[0] for r in ranked],
        "position_spread_across_weightings": spread,
        "adjuncts": [{"name": n, "note": t} for n, t in ADJUNCTS],
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
