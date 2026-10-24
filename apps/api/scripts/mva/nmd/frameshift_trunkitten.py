#!/usr/bin/env python3
"""Score frameshift-derived PTCs with the actual TrunKitten model.

    python3 -m scripts.mva.nmd.frameshift_trunkitten --model-dir <clone>/Model/TrunKitten
    python3 -m scripts.mva.nmd.frameshift_trunkitten --model-dir ... --selftest-only

An earlier version of this analysis declined to run the calibrated model on
frameshift-derived PTCs, arguing the annotation pipeline cannot describe a mutant
transcript. That was too weak a reason. The pipeline cannot, but the FEATURE
DEFINITIONS are explicit and reproducible, so the features can be computed directly
against a mutant transcript and handed to the trained model.

WHAT MAKES THAT LEGITIMATE RATHER THAN A SHORTCUT: a self-test that reproduces a
known prediction. `--selftest` recomputes all eight features for the proband's allele 1
from first principles and scores it. It must return the value this repository already
recorded by the upstream pipeline (0.3163). If it does not, the script exits and scores
nothing, because features computed differently from the training convention would
produce a confidently wrong probability -- the exact failure this workstream keeps
removing.

FEATURE DEFINITIONS, taken from the model's own source (minicat/transcript.py,
sequence.py, conservation.py) rather than inferred:

  last.EJC          categorical {last.exon, penultimate.last50bp, upstream}, on
                    CODING exon rank. penultimate.last50bp requires the PTC within
                    50 nt of the penultimate coding exon's 3' CDS end AND that exon's
                    CDS portion to be >= 50 bp.
  relativePTClocation  PTC CDS position / CDS length (stop-codon inclusive).
  mut.exon          coding-exon rank of the PTC's exon.
  cdsseqs_AU/UC_content  A+T and T+C fraction of the full CDS including native stop.
  phastcons_new3utr_first200_median  median phastCons100way over the first 200
                    transcript bases after the PTC, walked as genomic blocks.
  half_life_PC1, MedianExpression_log2  gene-level; identical for every BUB1B variant,
                    so they are read from this repo's own annotated row rather than
                    re-derived from GTEx and half-life tables we do not hold.

TWO DEVIATIONS, both measured rather than waved through:

  1. phastCons comes from the UCSC API, not the local bigWig the pipeline expects. On
     allele 1 this gives 0.9921 where the pipeline recorded 0.994. The resulting
     prediction shift is 0.006, and across the whole plausible range of that feature
     (0.5 to 0.994) the prediction moves only 0.298 to 0.322 against a 0.431 threshold.
     It is the second-least important of the eight features by SHAP. So the deviation
     cannot flip a call, and the self-test tolerance is set to accommodate it.
  2. For a mutant transcript the denominator of relativePTClocation is the reference
     CDS length minus the skipped exon, keeping the native stop in. The native stop is
     still present in the transcript, merely out of frame. This is a choice, it is
     stated, and no training example constrains it.

The model repository carries no licence, so it is cited and used, never vendored.
"""
import argparse
import json
import pathlib
import statistics
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[5]
D = ROOT / "docs/mva/data"
EXONS_J = D / "cds_exons.json"
CDS_TXT = D / "nmd/bub1b_cds.txt"
ANNOT = D / "nmd/annotated.tsv"
FS_IN = D / "nmd/frameshift_ptc.tsv"
OUT = D / "nmd/frameshift_trunkitten.tsv"
CHROM = "chr15"
STOPS = {"TAA", "TAG", "TGA"}
WINDOW = 200
# allele 1, as the upstream pipeline scored it. The self-test target.
SELFTEST = {"ptc_genomic": 40209701, "ptc_cds": 2210, "expect_prob": 0.3163,
            "tol": 0.01}


def exon_table(spans):
    out, seen = [], 0
    for i, (s, e) in enumerate(spans, 1):
        L = e - s + 1
        out.append({"n": i, "start": s, "end": e, "len": L,
                    "cds_from": seen + 1, "cds_to": seen + L})
        seen += L
    return out


def gene_level():
    """half_life_PC1 and MedianExpression_log2 are gene-level; read our own row."""
    lines = ANNOT.read_text().strip().split("\n")
    cols = lines[0].split("\t")
    r = dict(zip(cols, lines[1].split("\t")))
    return float(r["half_life_PC1"]), float(r["MedianExpression_log2"])


def phastcons_median(blocks):
    vals = []
    for bs, be in blocks:
        u = (f"https://api.genome.ucsc.edu/getData/track?genome=hg38;"
             f"track=phastCons100way;chrom={CHROM};start={bs-1};end={be}")
        d = json.loads(urllib.request.urlopen(u, timeout=120).read())
        tr = d.get("phastCons100way") or []
        if isinstance(tr, dict):
            tr = tr.get(CHROM, [])
        for it in tr:
            v, st, en = it.get("value"), it.get("start"), it.get("end")
            if v is None:
                continue
            for _ in range(max(1, (en or (st or 0) + 1) - (st or 0))):
                vals.append(float(v))
    return (statistics.median(vals) if vals else float("nan")), len(vals)


def new3utr_blocks(exons, ptc_genomic, window=WINDOW):
    """First `window` transcript bases after the PTC, as genomic blocks (+ strand)."""
    blocks, remaining, started = [], window, False
    for ex in exons:
        if remaining <= 0:
            break
        if not started:
            if ex["start"] <= ptc_genomic <= ex["end"]:
                started, bs, be = True, ptc_genomic + 1, ex["end"]
            else:
                continue
        else:
            bs, be = ex["start"], ex["end"]
        L = be - bs + 1
        if L <= 0:
            continue
        if L <= remaining:
            blocks.append((bs, be))
            remaining -= L
        else:
            blocks.append((bs, bs + remaining - 1))
            remaining = 0
            break
    return blocks, window - remaining


def cds_to_genomic(exons, cds_pos):
    for ex in exons:
        if ex["cds_from"] <= cds_pos <= ex["cds_to"]:
            return ex["start"] + (cds_pos - ex["cds_from"]), ex["n"]
    return None, None


def last_ejc_category(exons, exon_rank, ptc_cds):
    """{last.exon, penultimate.last50bp, upstream} on coding-exon rank."""
    n = len(exons)
    if n <= 1 or exon_rank == n:
        return "last.exon"
    if exon_rank == n - 1:
        pen = exons[n - 2]
        d = pen["cds_to"] - ptc_cds
        if 0 <= d <= 50 and pen["len"] >= 50:
            return "penultimate.last50bp"
        return "upstream"
    return "upstream"


def au(s):
    s = s.upper()
    return (s.count("A") + s.count("T")) / len(s)


def uc(s):
    s = s.upper()
    return (s.count("T") + s.count("C")) / len(s)


def score(model, spec, row):
    import pandas as pd
    from catboost import Pool
    order, cats = spec["features_in_order"], spec["categorical_features"]
    X = pd.DataFrame([[row[c] for c in order]], columns=order)
    for c in cats:
        X[c] = X[c].astype(str)
    return float(model.predict_proba(
        Pool(X, cat_features=[order.index(c) for c in cats]))[0][1])


def build_row(exons, cds, ptc_cds, hl, expr):
    """All eight features for a PTC at CDS position `ptc_cds` in this exon model."""
    g, rank = cds_to_genomic(exons, ptc_cds)
    if g is None:
        return None, None
    blocks, taken = new3utr_blocks(exons, g)
    phc, nvals = phastcons_median(blocks)
    return {
        "last.EJC": last_ejc_category(exons, rank, ptc_cds),
        "relativePTClocation": ptc_cds / len(cds),
        "half_life_PC1": hl,
        "cdsseqs_AU_content": au(cds),
        "mut.exon": rank,
        "cdsseqs_UC_content": uc(cds),
        "phastcons_new3utr_first200_median": phc,
        "MedianExpression_log2": expr,
    }, {"ptc_genomic": g, "exon_rank": rank, "new3utr_nt": taken,
        "phastcons_n": nvals}


def first_stop(seq, frame_start):
    for i in range(frame_start, len(seq) - 2, 3):
        if seq[i:i + 3].upper() in STOPS:
            return i
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model-dir", required=True,
                    help="path to the cloned Model/TrunKitten directory")
    ap.add_argument("--selftest-only", action="store_true")
    a = ap.parse_args()
    md = pathlib.Path(a.model_dir)
    spec = json.loads((md / "model/trunkitten_features.json").read_text())
    from catboost import CatBoostClassifier
    model = CatBoostClassifier()
    model.load_model(str(md / "model/trunkitten.cbm"))
    thr = spec["youden_threshold"]

    cds = CDS_TXT.read_text().strip()
    ref_exons = exon_table(json.loads(EXONS_J.read_text()))
    hl, expr = gene_level()

    # ---- gate: reproduce a prediction the upstream pipeline already made ----
    print("SELF-TEST: recompute allele 1 p.Leu737Ter from first principles")
    row, meta = build_row(ref_exons, cds, SELFTEST["ptc_cds"], hl, expr)
    p = score(model, spec, row)
    for k in spec["features_in_order"]:
        print(f"    {k:36s} {row[k]}")
    print(f"  escape_prob = {p:.6f}   pipeline recorded "
          f"{SELFTEST['expect_prob']}   delta {abs(p - SELFTEST['expect_prob']):.4f}")
    ok = abs(p - SELFTEST["expect_prob"]) <= SELFTEST["tol"]
    print(f"  {'PASS' if ok else 'FAIL'} (tolerance {SELFTEST['tol']}, set to absorb "
          f"the UCSC-vs-bigWig phastCons difference)")
    if not ok:
        sys.exit("\nSelf-test failed. Scoring nothing: features computed differently "
                 "from the training convention would return a confidently wrong "
                 "probability.")
    if a.selftest_only:
        return 0

    if not FS_IN.exists():
        sys.exit(f"missing {FS_IN}; run frameshift_ptc.py first")
    lines = FS_IN.read_text().strip().split("\n")
    cols = lines[0].split("\t")
    rows = [dict(zip(cols, L.split("\t"))) for L in lines[1:]]
    print(f"\nScoring {len(rows)} frameshift-derived PTCs with the trained model\n")

    out = []
    for r in rows:
        skipped = int(r["skipped_exon"])
        ex = ref_exons[skipped - 1]
        # Mutant transcript: excise the skipped exon from CDS and exon model.
        mut_cds = cds[:ex["cds_from"] - 1] + cds[ex["cds_to"]:]
        spans = [(e["start"], e["end"]) for e in ref_exons if e["n"] != skipped]
        mut_exons = exon_table(spans)
        stop_i = first_stop(mut_cds, ex["cds_from"] - 1)
        if stop_i is None:
            print(f"  {r.get('hgvs_c') or r['pos']}: no downstream stop, skipped")
            continue
        ptc_cds = stop_i + 1
        frow, meta = build_row(mut_exons, mut_cds, ptc_cds, hl, expr)
        if frow is None:
            print(f"  {r.get('hgvs_c') or r['pos']}: PTC outside the mutant model")
            continue
        p = score(model, spec, frow)
        call = "escape" if p >= thr else "decay"
        out.append({**r, "mutant_cds_len": len(mut_cds), "ptc_cds_in_mutant": ptc_cds,
                    "last_EJC": frow["last.EJC"],
                    "relativePTClocation": f"{frow['relativePTClocation']:.6f}",
                    "mut_exon": frow["mut.exon"],
                    "phastcons_new3utr": f"{frow['phastcons_new3utr_first200_median']:.4f}",
                    "escape_prob": f"{p:.6f}", "threshold": f"{thr:.4f}",
                    "model_call": call,
                    "basis": "TrunKitten, features computed on the mutant transcript"})
        print(f"  {(r.get('hgvs_c') or r['pos']):>16s}  skip exon {skipped:2d}  "
              f"PTC@{ptc_cds:4d}/{len(mut_cds)}  {frow['last.EJC']:20s} "
              f"P(escape)={p:.4f}  -> {call}")

    cw = ["chrom", "pos", "ref", "alt", "hgvs_c", "consequence",
          "clinvar_significance", "gain", "loss", "skipped_exon", "mutant_cds_len",
          "ptc_cds_in_mutant", "last_EJC", "relativePTClocation", "mut_exon",
          "phastcons_new3utr", "escape_prob", "threshold", "model_call", "basis"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        f.write("\t".join(cw) + "\n")
        for r in out:
            f.write("\t".join(str(r.get(c, "")).replace("\t", " ") for c in cw) + "\n")
    print(f"\nwrote {len(out)} rows -> {OUT.relative_to(ROOT)}")
    print("\nThese are MODEL calls, gated on a self-test that reproduced a prediction")
    print("the upstream pipeline had already made. The model was trained on")
    print("PTC-producing SNVs; a frameshift-derived PTC is a different lesion class")
    print("reaching the same surveillance machinery, and that extrapolation is stated")
    print("rather than hidden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
