#!/usr/bin/env python3
"""Derive the map's calling threshold from measured data, on a held-out split.

    python3 -m scripts.mva.nmd.mfass_threshold SAMPLE.tsv SCORED.csv

WHY A SPLIT, AND WHY THIS IS NOT JUST TURNING A KNOB.
C38 established that CALL = 0.2 fails the pre-registered sensitivity criterion badly
(0.330 against a 0.70 pass bar) while passing specificity easily (0.988), and that
AUC 0.882 puts the fault in the operating point rather than the method. The obvious next
move is to pick the threshold that performs best on the benchmark. That move is wrong:
a threshold chosen on the same data it is then scored against reports its own best case,
and the number would be optimistic by an unknown amount.

So the benchmark is split in half, stratified on the measured label with a fixed seed.
Thresholds are derived on the DERIVE half only. Every performance number reported is from
the HELD-OUT half, which played no part in choosing them. The gap between the two is
printed, because that gap is the honest estimate of how much the derivation overfits.

WHY TIERS RATHER THAN ONE THRESHOLD.
A single cut was always the weaker design, and the benchmark makes the cost visible: at
3.2% prevalence a threshold sensitive enough to catch most disruption produces about as
many false calls as true ones, and a threshold precise enough to trust catches a third.
No single number is both. The Fabry precedent this workstream keeps citing does not use
one either -- its assay reports amenable, not amenable, and indeterminate. So the map
gets three tiers whose boundaries are derived here:

    CALL_HIGH   specificity-led. A call at or above this is one to act on.
    CALL_SCREEN sensitivity-led, meeting the pre-stated 0.70 bar if reachable.
                Between SCREEN and HIGH the variant is a candidate, not a call.
    below       not called -- and with sensitivity what it is, "not called" is a weak
                statement, not evidence of no splice effect.

PREVALENCE. Precision is always reported corrected to the rate these variants actually
occur (3.2% non-canonical intronic, 3.8% exonic, from our own MFASS reconstruction), never
at the sample's ~19%, which the sampling design inflates (C38a).
"""
import argparse
import csv
import json
import math
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
OUT = ROOT / "docs/mva/data/nmd/mfass_thresholds.json"
SEED = 20261016
# THREE-WAY SPLIT, adopted from the Agentic Scientist pipeline's sealed-final-evaluation
# phase (SakanaAI/AI-Scientist-v3, Apache-2.0, arXiv:2610.18933).
#
# The two-way split this file shipped with was already weaker than it looked, and the
# weakness is mine rather than the method's. A held-out set consulted ONCE is a test set.
# This one has been consulted at n=1025, 1273, 1280 and 1334 while tier boundaries, the
# region-vs-pooled rule and MIN_POS_PER_REGION were being chosen -- so it had quietly
# become a validation set, and every "held-out" number reported from it carries an
# unknown optimism.
#
# So: DERIVE fits thresholds, VALIDATE is consulted freely for choices between
# candidates, and SEALED is opened exactly once, at the end, and never informs any
# choice. Opening it requires --open-seal and is appended to a log, so it cannot be
# opened repeatedly without leaving a trace.
SPLIT = (0.50, 0.25, 0.25)       # derive / validate / sealed
SEAL_LOG = ROOT / "docs/mva/data/nmd/seal_openings.log"
TARGET_SENS = 0.70          # the pre-stated bar from mfass_benchmark.py
MIN_SPEC_HIGH = 0.98        # what "a call to act on" has to clear
PREVALENCE = (("non-canonical intronic", 0.032), ("exonic", 0.038))
BLOCK_MIN = 200             # refuse to derive on fewer than this many per split
MIN_POS_PER_REGION = 60     # below this a region cut is noise with a decimal point


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def corrected_precision(sens, spec, pi):
    num = sens * pi
    den = num + (1 - spec) * (1 - pi)
    return num / den if den else 0.0


def load(sample_path, scored_path):
    import re
    blk = re.compile(r"(ENSG[\d.]+)\|(-?\d+):(-?[\d.]+)\|(-?\d+):(-?[\d.]+)")
    scores = {}
    for line in pathlib.Path(scored_path).read_text().split("\n"):
        if not line or line.startswith("CHROM"):
            continue
        f = line.split(",")
        if len(f) < 5:
            continue
        try:
            pos = int(f[1])
        except ValueError:
            continue
        g = l = 0.0
        for _gene, _gp, gs, _lp, ls in blk.findall(",".join(f[4:])):
            g = max(g, abs(float(gs)))
            l = max(l, abs(float(ls)))
        scores[(f[0].replace("chr", ""), pos, f[2], f[3])] = max(g, l)
    out = []
    for r in csv.DictReader(open(sample_path, newline=""), delimiter="\t"):
        k = (r["chrom"].replace("chr", ""), int(r["pos"]), r["ref"], r["alt"])
        if k in scores:
            out.append((scores[k], r["measured_sdv"] == "1", r["region"]))
    return out


def metrics(pairs, thr):
    tp = sum(1 for s, y, _ in pairs if y and s >= thr)
    fn = sum(1 for s, y, _ in pairs if y and s < thr)
    fp = sum(1 for s, y, _ in pairs if not y and s >= thr)
    tn = sum(1 for s, y, _ in pairs if not y and s < thr)
    sens = tp / (tp + fn) if tp + fn else 0.0
    spec = tn / (tn + fp) if tn + fp else 0.0
    return tp, fn, fp, tn, sens, spec


def candidates(pairs):
    """Every distinct score, as a possible cut. Coarse grids hide the answer: C38's
    sweep stepped 0.1 and could only say 'below 0.1', which is not a threshold."""
    return sorted({round(s, 4) for s, _, _ in pairs}, reverse=True)



# ---------------------------------------------------------------------------
# REGION-SPLIT DERIVATION
#
# Exonic and non-canonical intronic variants are not the same problem. Their measured
# disruption rates differ (3.8% vs 3.2% in our own reconstruction, C32) and the mechanism
# differs -- an exonic variant disrupts an exonic splicing element, an intronic one
# usually weakens or creates a site -- so there is no reason a single score cut should be
# optimal for both.
#
# The test applied here is NOT "does stratifying change the numbers", which it always
# will. It is "does a region-specific threshold BEAT the pooled threshold on that
# region's own held-out rows". If it does not, the pooled threshold wins on simplicity
# and on having been derived from more data, and the stratification is dropped. A split
# that merely fits each region's derive half better is overfitting with extra steps.
# ---------------------------------------------------------------------------


def derive_on(derive, target_sens, min_spec_high):
    """The same derivation rules, applied to whatever subset is handed in."""
    cands = candidates(derive)
    high = next((thr for thr in sorted(cands)
                 if metrics(derive, thr)[5] >= min_spec_high), None)
    screen = next((thr for thr in cands
                   if metrics(derive, thr)[4] >= target_sens), None)
    j_thr, j_val = None, -2.0
    for thr in cands:
        _, _, _, _, se, sp = metrics(derive, thr)
        if se + sp - 1 > j_val:
            j_thr, j_val = thr, se + sp - 1
    return {"call_high": high, "call_screen": screen, "youden": j_thr,
            "youden_j": j_val}


def region_of(r):
    """MFASS rows carry 'exonic' or 'intronic'; canonical sites are already excluded
    from the benchmark pool by mfass_benchmark.py."""
    return r[2]


def region_split_report(derive, held, pooled):
    print("\n" + "=" * 70)
    print("REGION-SPLIT DERIVATION -- does stratifying beat pooling?")
    print("=" * 70)
    prev = dict(PREVALENCE)
    regions = sorted({region_of(r) for r in derive + held})
    verdicts = {}
    for reg in regions:
        d = [r for r in derive if region_of(r) == reg]
        h = [r for r in held if region_of(r) == reg]
        dp, hp = sum(1 for r in d if r[1]), sum(1 for r in h if r[1])
        pi = prev.get("exonic" if reg == "exonic" else "non-canonical intronic", 0.032)
        print(f"\n  {reg}:  derive {len(d)} ({dp} pos)   held-out {len(h)} ({hp} pos)"
              f"   base rate {pi:.1%}")
        if dp < MIN_POS_PER_REGION or hp < MIN_POS_PER_REGION:
            print(f"    fewer than {MIN_POS_PER_REGION} positives in a split -- "
                  f"REFUSING to derive a region threshold from this. A cut fitted to "
                  f"a few dozen positives is noise with a decimal point.")
            verdicts[reg] = "insufficient_data"
            continue
        own = derive_on(d, TARGET_SENS, MIN_SPEC_HIGH)
        print(f"    region-derived:  youden {own['youden']}   "
              f"call_high {own['call_high']}   call_screen {own['call_screen']}")
        print(f"    pooled-derived:  youden {pooled['youden']}   "
              f"call_high {pooled['call_high']}")
        best = {}
        for label, thr in (("region threshold", own["youden"]),
                           ("pooled threshold", pooled["youden"])):
            if thr is None:
                continue
            tp, fn, fp, tn, se, sp = metrics(h, thr)
            pr = corrected_precision(se, sp, pi)
            print(f"      {label:18s} thr {thr:<6} held-out sens {se:.3f}  "
                  f"spec {sp:.3f}  J {se + sp - 1:.3f}  precision {pr:.3f}")
            best[label] = (se + sp - 1, se, sp, pr, thr)
        if len(best) == 2:
            rj = best["region threshold"][0]
            pj = best["pooled threshold"][0]
            margin = rj - pj
            if abs(margin) < 0.02:
                verdicts[reg] = "no_benefit"
                print(f"      -> held-out J differs by {margin:+.3f}, inside noise. "
                      f"POOLED WINS on simplicity and on more derivation data.")
            elif margin > 0:
                verdicts[reg] = "region_wins"
                print(f"      -> region threshold better by {margin:+.3f} held-out J. "
                      f"Stratification earns its keep here.")
            else:
                verdicts[reg] = "pooled_wins"
                print(f"      -> region threshold WORSE by {margin:+.3f} held-out J, "
                      f"which is what overfitting looks like. POOLED WINS.")
    return verdicts


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sample")
    ap.add_argument("scored")
    ap.add_argument("--out", default=str(OUT),
                    help="where to write the derived thresholds. Milestone runs during "
                         "scoring write to a scratch path so interim values never land "
                         "on the committed one.")
    ap.add_argument("--open-seal", action="store_true",
                    help="open the sealed split and report on it. Do this ONCE, when "
                         "tuning is finished. Every opening is appended to "
                         "seal_openings.log, so a second opening is visible.")
    ap.add_argument("--quiet", action="store_true",
                    help="one summary line instead of the full report, for trajectory "
                         "logging")
    a = ap.parse_args()
    out_path = pathlib.Path(a.out)
    pairs = load(a.sample, a.scored)
    pos = [p for p in pairs if p[1]]
    neg = [p for p in pairs if not p[1]]
    print(f"{len(pairs)} scored variants: {len(pos)} measured SDV, {len(neg)} not")
    if len(pos) < BLOCK_MIN // 4 or len(neg) < BLOCK_MIN:
        print(f"\nToo few to split responsibly (need >= {BLOCK_MIN // 4} positives and "
              f">= {BLOCK_MIN} negatives per the whole set). Refusing to derive.")
        return 1

    rng = random.Random(SEED)
    rng.shuffle(pos)
    rng.shuffle(neg)

    def three(xs):
        a = int(len(xs) * SPLIT[0])
        b = a + int(len(xs) * SPLIT[1])
        return xs[:a], xs[a:b], xs[b:]

    dp, vp, sp_ = three(pos)
    dn, vn, sn = three(neg)
    derive, held, sealed = dp + dn, vp + vn, sp_ + sn
    print(f"derive  : {len(dp):4d} pos / {len(dn):4d} neg   fits thresholds")
    print(f"validate: {len(vp):4d} pos / {len(vn):4d} neg   consulted for choices")
    print(f"SEALED  : {len(sp_):4d} pos / {len(sn):4d} neg   "
          f"{'OPENED' if a.open_seal else 'untouched'}\n")

    cands = candidates(derive)

    # CALL_HIGH: most sensitive threshold that still clears MIN_SPEC_HIGH
    high = None
    for thr in sorted(cands):
        if metrics(derive, thr)[5] >= MIN_SPEC_HIGH:
            high = thr
            break
    # CALL_SCREEN: most specific threshold that reaches TARGET_SENS
    screen = None
    for thr in cands:
        if metrics(derive, thr)[4] >= TARGET_SENS:
            screen = thr
            break
    # Youden's J, for reference
    j_thr, j_val = None, -2
    for thr in cands:
        _, _, _, _, se, sp = metrics(derive, thr)
        if se + sp - 1 > j_val:
            j_thr, j_val = thr, se + sp - 1

    print("DERIVED ON THE DERIVE SPLIT ONLY")
    print(f"  CALL_HIGH   {high}    (most sensitive cut with specificity >= "
          f"{MIN_SPEC_HIGH})")
    print(f"  CALL_SCREEN {screen}  (most specific cut reaching sensitivity "
          f">= {TARGET_SENS})")
    print(f"  Youden J    {j_thr}  (J = {j_val:.3f}, reference only)")
    if screen is None:
        print(f"\n  NOTE: sensitivity {TARGET_SENS} is NOT REACHABLE at any threshold in")
        print("  this data. That is a finding about the predictor, not a tuning failure,")
        print("  and it means the pre-stated bar cannot be met by moving the cut alone.")

    print("\nEVALUATED ON THE HELD-OUT SPLIT (and on the derive split, to show the gap)")
    rows = {}
    for name, thr in (("CALL_HIGH", high), ("CALL_SCREEN", screen),
                      ("Youden J", j_thr), ("old CALL=0.2", 0.2)):
        if thr is None:
            continue
        _, _, _, _, dse, dsp = metrics(derive, thr)
        tp, fn, fp, tn, se, sp = metrics(held, thr)
        s_lo, s_hi = wilson(tp, tp + fn)[1:]
        p_lo, p_hi = wilson(tn, tn + fp)[1:]
        print(f"\n  {name}  (threshold {thr})")
        print(f"    held-out  sensitivity {se:.3f} ({s_lo:.3f}-{s_hi:.3f})   "
              f"specificity {sp:.3f} ({p_lo:.3f}-{p_hi:.3f})")
        print(f"    derive    sensitivity {dse:.3f}              "
              f"specificity {dsp:.3f}")
        print(f"    overfit gap: sensitivity {dse - se:+.3f}  specificity {dsp - sp:+.3f}")
        for nm, pi in PREVALENCE:
            print(f"    precision at {pi:.1%} ({nm}): "
                  f"{corrected_precision(se, sp, pi):.3f}")
        rows[name] = {"threshold": thr, "held_sensitivity": se,
                      "held_specificity": sp,
                      "derive_sensitivity": dse, "derive_specificity": dsp,
                      "corrected_precision": {nm: corrected_precision(se, sp, pi)
                                               for nm, pi in PREVALENCE}}

    pooled = {"call_high": high, "call_screen": screen, "youden": j_thr}
    sealed_result = None
    if a.open_seal:
        import datetime
        print("\n" + "=" * 70)
        print("SEALED FINAL EVALUATION -- this split informed no choice")
        print("=" * 70)
        sealed_result = {}
        for name, thr in (("CALL_HIGH", high), ("CALL_SCREEN", screen),
                          ("Youden J", j_thr)):
            if thr is None:
                continue
            tp, fn, fp, tn, se, spc = metrics(sealed, thr)
            print(f"  {name:12s} thr {thr:<6} sensitivity {se:.3f}  "
                  f"specificity {spc:.3f}")
            for nm, pi in PREVALENCE:
                print(f"      precision at {pi:.1%} ({nm}): "
                      f"{corrected_precision(se, spc, pi):.3f}")
            sealed_result[name] = {"threshold": thr, "sensitivity": se,
                                   "specificity": spc,
                                   "corrected_precision": {
                                       nm: corrected_precision(se, spc, pi)
                                       for nm, pi in PREVALENCE}}
        SEAL_LOG.parent.mkdir(parents=True, exist_ok=True)
        with SEAL_LOG.open("a") as f:
            f.write(f"{datetime.datetime.now(datetime.timezone.utc).isoformat()}  "
                    f"n_scored={len(pairs)}  sealed_n={len(sealed)}  "
                    f"thresholds={pooled}\n")
        print(f"\n  opening appended to {SEAL_LOG.relative_to(ROOT)} -- a second")
        print("  opening after further tuning is visible there and invalidates this one.")
    region_verdicts = {}
    if not a.quiet:
        region_verdicts = region_split_report(derive, held, pooled)

    if a.quiet:
        h = rows.get("CALL_HIGH", {})
        s = rows.get("Youden J", {})
        print(f"n={len(pairs):5d} pos={len(pos):4d}  CALL_HIGH={high}  "
              f"CALL_SCREEN={screen}  youden={j_thr}  "
              f"held_sens@J={s.get('held_sensitivity', 0):.3f}  "
              f"held_spec@J={s.get('held_specificity', 0):.3f}  "
              f"prec@J={s.get('corrected_precision', {}).get('non-canonical intronic', 0):.3f}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({
        "seed": SEED, "n_scored": len(pairs),
        "derive_n": len(derive), "held_out_n": len(held),
        "target_sensitivity": TARGET_SENS, "min_specificity_high": MIN_SPEC_HIGH,
        "call_high": high, "call_screen": screen, "youden_j": j_thr,
        "results": rows,
        "region_split": region_verdicts,
        "split": {"derive": len(derive), "validate": len(held),
                  "sealed": len(sealed)},
        "sealed_evaluation": sealed_result,
        "note": "Thresholds derived on the derive split; all reported performance is "
                "held-out. Precision is corrected to the true prevalence, never the "
                "sample's.",
    }, indent=2) + "\n")
    try:
        print(f"\nwrote {out_path.relative_to(ROOT)}")
    except ValueError:
        print(f"\nwrote {out_path}  (scratch -- interim, not committed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
