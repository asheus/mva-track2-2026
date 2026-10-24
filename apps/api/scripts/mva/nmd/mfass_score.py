#!/usr/bin/env python3
"""Score the MFASS benchmark with local Pangolin and apply the pre-stated criteria.

    python3 -m scripts.mva.nmd.mfass_score SAMPLE.tsv REF.fa.gz ANNOT.db [--out-dir DIR]

This is the second half of `mfass_benchmark.py`. That script built a benchmark of
non-canonical variants whose splicing outcome was MEASURED; this one runs the predictor
over it and reports what the map's shipping threshold actually costs.

TWO GATES, BOTH BEFORE ANY METRIC IS BELIEVED.

  1. SAME-INSTRUMENT GATE. The map was built with Pangolin as served by Neurosnap. This
     script runs Pangolin locally, which is a different code path, so the four BUB1B
     variants carrying committed reference scores are injected into the same input file. If the
     local run does not reproduce them within TOL, the two are not the same instrument
     and no benchmark computed here describes the map -- so the script refuses to report.

  2. PRE-STATED CRITERIA. Fixed in `mfass_benchmark.py` before any variant was scored:
       sensitivity >= 0.70 pass, < 0.50 fail
       specificity >= 0.80 pass, < 0.60 fail
     Anything between is INCONCLUSIVE and says so.

WHAT IS REPORTED, AND WHY PRECISION IS THE HEADLINE.
Measured splice disruption runs at ~3.2% among non-canonical intronic variants and ~3.8%
among exonic ones. At that prevalence specificity dominates everything. But the benchmark
sample deliberately takes ALL positives and only a subsample of negatives, so ITS
prevalence is ~19% and any precision computed directly on it is inflated by the sampling
design -- a trap this file fell into on its first version, which claimed to report
"precision at the measured prevalence" while reporting precision at the sample's. Both
are now printed: the sample's, labelled as inflated, and the value corrected to the true
prevalence via sensitivity and specificity, which the sampling does not distort. The
corrected one is the number that decides whether a clinician could read this map.

A ROC is also printed, because if the threshold is the problem rather than the predictor,
that distinction is worth having: a good AUC with a bad operating point means re-derive
the threshold, while a poor AUC means the approach does not work on these variants.

CAVEAT THAT TRAVELS WITH ANY RESULT FROM THIS FILE. MFASS is a minigene reporter assayed
in a cell line. It measures exon recognition in a construct, not endogenous splicing at
the native locus. A predictor can be right about the gene and wrong about the reporter,
so a sensitivity failure here is weaker evidence than a specificity failure -- the
negatives are the part the assay is least able to get wrong.
"""
import argparse
import csv
import math
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
METRICS = ROOT / "docs/mva/data/nmd/mfass_benchmark_metrics.json"
CALL = 0.2             # the threshold the map ships
TOL = 0.03
PASS_SENS, FAIL_SENS = 0.70, 0.50
PASS_SPEC, FAIL_SPEC = 0.80, 0.60
# The same four committed reference scores the sweep gates on.
SENTINELS = {
    (40196779, "G", "A"): ("c.1288+5G>A", 0.49, -0.73),
    (40200239, "A", "G"): ("c.1402-5A>G", 0.85, -0.69),
    (40212488, "A", "G"): ("c.2386-11A>G", 0.76, -0.71),
    (40206459, "G", "A"): ("c.2009+1G>A", 0.73, -0.89),
}
BLOCK = re.compile(r"(ENSG[\d.]+)\|(-?\d+):(-?[\d.]+)\|(-?\d+):(-?[\d.]+)")


def wilson(k, n, z=1.96):
    """Wilson score interval: honest at the small counts and extreme rates this produces,
    where a normal-approximation interval would run past 0 or 1."""
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def write_csv(rows, path):
    """CSV, not VCF, and the reason is a dependency break rather than a preference.

    Pangolin's VCF path calls `vcf.parser._Info(...)` with the field list of PyVCF 0.6.8.
    The only PyVCF that installs on this container's Python 3.13 is PyVCF3 1.0.4, whose
    `_Info` namedtuple gained a `type_code` field, so the VCF path dies on its own header
    line before scoring anything. Pangolin's CSV path never touches that call.

    This is a route around a packaging incompatibility, not around a check: the CSV output
    carries the same `gene|pos:score|pos:score|Warnings:` blocks as the VCF output and as
    the Neurosnap runs the map was built from, so the sentinel gate still has to pass on
    the same values. Patching the installed Pangolin would also have worked -- it is
    GPL-3.0 and modification is permitted -- but using a code path its author shipped is
    preferable to carrying a local patch of the instrument we are benchmarking with.
    """
    with path.open("w") as f:
        f.write("CHROM,POS,REF,ALT\n")
        for r in rows:
            f.write(f"{r['chrom']},{r['pos']},{r['ref']},{r['alt']}\n")


def _rows(path):
    """(key, rest-of-line) per scored variant. The Pangolin column itself contains
    commas when several genes are reported, so the first four fields are taken as the
    key and the regex is applied to everything after them."""
    for line in path.read_text().split("\n"):
        if not line or line.startswith("CHROM"):
            continue
        f = line.split(",")
        if len(f) < 5:
            continue
        try:
            pos = int(f[1])
        except ValueError:
            continue
        yield (f[0].replace("chr", ""), pos, f[2], f[3]), ",".join(f[4:])


def read_pangolin(path):
    """Max |score| over every gene block reported for the variant.

    Taking the maximum across genes rather than picking one is the right rule for a
    benchmark over 2,198 exons in arbitrary genes: the question being tested is "does the
    predictor see a splice effect at this position", and for the single-gene loci that are
    the large majority it is identical to picking the gene."""
    out = {}
    for key, rest in _rows(path):
        best_g = best_l = 0.0
        for _gene, _gp, g, _lp, l in BLOCK.findall(rest):
            best_g = max(best_g, abs(float(g)))
            best_l = max(best_l, abs(float(l)))
        out[key] = (best_g, best_l)
    return out


def signed_pangolin(path):
    """Signed (gain, loss) per variant, for the sentinel comparison."""
    out = {}
    for key, rest in _rows(path):
        for _gene, _gp, g, _lp, l in BLOCK.findall(rest):
            out.setdefault(key, (float(g), float(l)))
    return out


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sample", help="output of mfass_benchmark.py (uncommitted path)")
    ap.add_argument("reference", help="GRCh38 FASTA (bgzipped)")
    ap.add_argument("annotation", help="Pangolin gffutils .db")
    ap.add_argument("--out-dir", default="/tmp/mfass_score")
    ap.add_argument("--skip-run", action="store_true",
                    help="reuse an existing Pangolin output in --out-dir")
    a = ap.parse_args()

    d = pathlib.Path(a.out_dir)
    d.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(a.sample, newline=""), delimiter="\t"))
    print(f"{len(rows)} benchmark variants "
          f"({sum(1 for r in rows if r['measured_sdv'] == '1')} measured SDVs)")

    sent_rows = [{"chrom": "chr15", "pos": p, "ref": r, "alt": al}
                 for (p, r, al) in SENTINELS]
    variant_file = d / "benchmark.csv"
    write_csv([{"chrom": r["chrom"] if r["chrom"].startswith("chr")
                else "chr" + r["chrom"], "pos": r["pos"], "ref": r["ref"],
                "alt": r["alt"]} for r in rows] + sent_rows, variant_file)
    print(f"wrote {variant_file}")

    out_prefix = d / "benchmark_pangolin"
    if not a.skip_run:
        cmd = ["pangolin", str(variant_file), a.reference, a.annotation,
               str(out_prefix)]
        print("running:", " ".join(cmd), flush=True)
        p = subprocess.run(cmd, capture_output=True, text=True)
        sys.stdout.write(p.stdout[-3000:])
        sys.stderr.write(p.stderr[-3000:])
        if p.returncode != 0:
            sys.exit(f"pangolin failed with exit {p.returncode}")
    res_path = pathlib.Path(str(out_prefix) + ".csv")
    if not res_path.exists():
        sys.exit(f"no Pangolin output at {res_path}")

    # ---------------- GATE 1: same instrument ----------------
    print("\n" + "=" * 70)
    print("GATE 1  does local Pangolin reproduce the committed reference scores?")
    print("=" * 70)
    signed = signed_pangolin(res_path)
    gate_ok, seen = True, 0
    for (pos, ref, alt), (lab, eg, el) in SENTINELS.items():
        got = signed.get(("15", pos, ref, alt))
        if got is None:
            print(f"  {lab:14s} NOT SCORED locally")
            gate_ok = False
            continue
        seen += 1
        ok = abs(got[0] - eg) < TOL and abs(got[1] - el) < TOL
        gate_ok &= ok
        print(f"  {lab:14s} got {got[0]:+.2f}/{got[1]:+.2f}  "
              f"expected {eg:+.2f}/{el:+.2f}  {'PASS' if ok else 'FAIL'}")
    if not gate_ok or seen == 0:
        print("\n  GATE FAILED. The local run is not the instrument the map was built")
        print("  with, so no benchmark computed from it describes the map. Refusing to")
        print("  report metrics -- this is the same refusal the sweep makes.")
        return 1
    print("\n  all four reproduce: the local run IS the map's instrument")

    # ---------------- metrics ----------------
    scores = read_pangolin(res_path)
    pairs = []
    missing = 0
    for r in rows:
        key = (r["chrom"].replace("chr", ""), int(r["pos"]), r["ref"], r["alt"])
        s = scores.get(key)
        if s is None:
            missing += 1
            continue
        pairs.append((max(s), r["measured_sdv"] == "1", r["region"]))
    print(f"\nscored {len(pairs)} of {len(rows)}; "
          f"{missing} not returned by Pangolin (skipped: outside a gene, or "
          f"reference mismatch)")

    def metrics(subset, thr):
        tp = sum(1 for s, y, _ in subset if y and s >= thr)
        fn = sum(1 for s, y, _ in subset if y and s < thr)
        fp = sum(1 for s, y, _ in subset if not y and s >= thr)
        tn = sum(1 for s, y, _ in subset if not y and s < thr)
        return tp, fn, fp, tn

    tp, fn, fp, tn = metrics(pairs, CALL)
    sens, sl, sh = wilson(tp, tp + fn)
    spec, pl, ph = wilson(tn, tn + fp)
    prec, cl, ch = wilson(tp, tp + fp) if tp + fp else (0.0, 0.0, 0.0)
    print("\n" + "=" * 70)
    print(f"RESULT at the shipping threshold CALL = {CALL}")
    print("=" * 70)
    print(f"                 called   not called")
    print(f"  measured SDV   {tp:6d}   {fn:10d}")
    print(f"  measured not   {fp:6d}   {tn:10d}")
    print(f"\n  sensitivity  {sens:.3f}  (95% CI {sl:.3f}-{sh:.3f})   "
          f"pass >= {PASS_SENS}, fail < {FAIL_SENS}")
    print(f"  specificity  {spec:.3f}  (95% CI {pl:.3f}-{ph:.3f})   "
          f"pass >= {PASS_SPEC}, fail < {FAIL_SPEC}")
    # The sample takes ALL positives and a subsample of negatives, so its prevalence
    # (~19%) is nowhere near the rate these variants actually occur (3.2-3.8%, measured
    # in our own reconstruction). Precision computed on the sample is therefore inflated
    # and is NOT the number a reader of the map needs -- it is reported only to be
    # corrected. The corrected value follows from sensitivity, specificity and the true
    # prevalence, none of which the sampling distorts.
    samp_prev = (tp + fn) / len(pairs) if pairs else 0.0
    print(f"\n  precision    {prec:.3f}  (95% CI {cl:.3f}-{ch:.3f})   on THIS sample, "
          f"whose prevalence is {samp_prev:.1%} -- enriched, so inflated")
    print("\n  PRECISION AT THE RATE THESE VARIANTS ACTUALLY OCCUR:")
    corrected = {}
    for nm, pi in (("non-canonical intronic", 0.032), ("exonic", 0.038)):
        cp = ((sens * pi) / ((sens * pi) + ((1 - spec) * (1 - pi)))
              if (sens * pi) + ((1 - spec) * (1 - pi)) else 0.0)
        corrected[nm] = cp
        print(f"    {pi:.1%}  {nm:24s} -> precision {cp:.3f}")
    print("  ^ this is the number a reader of the map needs.")

    def verdict(v, p, f):
        return "PASS" if v >= p else "FAIL" if v < f else "INCONCLUSIVE"
    vs, vp = verdict(sens, PASS_SENS, FAIL_SENS), verdict(spec, PASS_SPEC, FAIL_SPEC)
    print(f"\n  sensitivity verdict: {vs}")
    print(f"  specificity verdict: {vp}")

    # ROC, to separate "wrong threshold" from "wrong approach"
    ys = sorted(pairs, key=lambda x: -x[0])
    P = sum(1 for _, y, _ in ys if y)
    N = len(ys) - P
    auc = 0.0
    if P and N:
        rank_sum = sum(i + 1 for i, (_, y, _) in enumerate(sorted(pairs, key=lambda x: x[0]))
                       if y)
        auc = (rank_sum - P * (P + 1) / 2) / (P * N)
    print(f"\n  ROC AUC {auc:.3f}  over {P} positives and {N} negatives")
    print("  a good AUC with a failing operating point means re-derive the threshold;")
    print("  a poor AUC means the approach does not work on non-canonical variants.")

    print("\n  by region, at the same threshold:")
    for reg in ("intronic", "exonic"):
        sub = [x for x in pairs if x[2] == reg]
        if not sub:
            continue
        a_, b_, c_, d_ = metrics(sub, CALL)
        se = a_ / (a_ + b_) if a_ + b_ else 0.0
        sp = d_ / (c_ + d_) if c_ + d_ else 0.0
        pr = a_ / (a_ + c_) if a_ + c_ else 0.0
        print(f"    {reg:10s} n={len(sub):5d}  sens {se:.3f}  spec {sp:.3f}  "
              f"precision {pr:.3f}")

    # threshold sweep, so the re-derivation is on the record rather than asserted
    print("\n  threshold sweep (what the operating point costs):")
    print("    thr    sens   spec   precision")
    for thr in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8):
        a_, b_, c_, d_ = metrics(pairs, thr)
        se = a_ / (a_ + b_) if a_ + b_ else 0.0
        sp = d_ / (c_ + d_) if c_ + d_ else 0.0
        pr = a_ / (a_ + c_) if a_ + c_ else 0.0
        mark = "  <- shipping" if abs(thr - CALL) < 1e-9 else ""
        print(f"    {thr:.1f}   {se:.3f}  {sp:.3f}  {pr:.3f}{mark}")

    # A smoke run on a handful of variants once wrote 1.000/1.000/1.000 to this path.
    # Those numbers are arithmetically correct and scientifically worthless, and the
    # committed metrics file is exactly where a reader would go for the benchmark result.
    # So small runs are allowed -- they are how the gate gets tested -- but they do not
    # get to occupy the path that answers "how good is the map".
    MIN_N = 500
    if len(pairs) < MIN_N:
        print(f"\n  n = {len(pairs)} is below MIN_N = {MIN_N}: metrics NOT written to")
        print(f"  {METRICS.relative_to(ROOT)}. A run this small cannot answer the")
        print("  question that file is read for, whatever the point estimates say.")
        return 0
    METRICS.write_text(__import__("json").dumps({
        "threshold": CALL, "n_scored": len(pairs), "n_missing": missing,
        "tp": tp, "fn": fn, "fp": fp, "tn": tn,
        "sensitivity": sens, "sensitivity_ci95": [sl, sh],
        "specificity": spec, "specificity_ci95": [pl, ph],
        "precision": prec, "precision_ci95": [cl, ch],
        "roc_auc": auc,
        "sensitivity_verdict": vs, "specificity_verdict": vp,
        "criteria": {"sensitivity": {"pass": PASS_SENS, "fail": FAIL_SENS},
                     "specificity": {"pass": PASS_SPEC, "fail": FAIL_SPEC}},
        "same_instrument_gate": "PASS",
        "caveat": "MFASS is a minigene reporter in a cell line: it measures exon "
                  "recognition in a construct, not endogenous splicing at the native "
                  "locus.",
    }, indent=2) + "\n")
    print(f"\nwrote {METRICS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
