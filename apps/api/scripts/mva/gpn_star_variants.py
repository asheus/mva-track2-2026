#!/usr/bin/env python3
"""Score the two BUB1B variants with GPN-Star, a third independent predictor.

    python3 -m scripts.mva.gpn_star_variants

WHY A THIRD PREDICTOR. AlphaMissense scores protein-level missense pathogenicity;
AlphaGenome scores regulatory and splicing effects. GPN-Star (Ye et al., Nature
2026, doi:10.1038/s41586-026-11005-5) scores EVOLUTIONARY CONSTRAINT, learned from
whole-genome alignments with an explicit species tree. Three predictors trained on
three different signals agreeing says considerably more than any one of them;
disagreement is informative too, and is the sort of thing an adversarial channel
should weigh rather than average away.

The paper reports "task-dependent advantages of modelling more recent versus deeper
evolution", so all three published human timescales are scored rather than one:
  m447  447-way mammal alignment
  p243  243-way primate alignment   (most recent)
  v100  100-way vertebrate alignment (deepest)

HOW, WITHOUT RUNNING THE MODEL. The authors published precomputed genome-wide
log-likelihood ratios. Each chromosome is a ~1.6 GB parquet of every possible SNV,
sorted by position and split into ~1 M-row groups, so the row groups spanning BUB1B
can be read over HTTP range requests and the rest of the file left alone. A negative
LLR means the alternate allele is disfavoured by evolutionary constraint; more
negative is more constrained.

INTERPRETATION IS RELATIVE, so the two variants are reported against a null built
from every other possible SNV inside BUB1B — the same discipline used for the
AlphaGenome run, and for the same reason: a raw score with nothing to compare it to
is not evidence.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

BASE = ("https://huggingface.co/datasets/songlab/gpn-star-scores/resolve/main/"
        "data/gpn-star-hg38-{model}-200m/llr/llr_chr15.parquet")
MODELS = [("p243", "primate 243-way (most recent)"),
          ("m447", "mammal 447-way"),
          ("v100", "vertebrate 100-way (deepest)")]

GENE_START, GENE_END = 40_161_023, 40_221_136          # BUB1B, GRCh38
VARIANTS = {"L737*  (allele 1)": (40_209_701, "T", "G"),
            "N1002K (allele 2)": (40_220_612, "T", "G")}


def gene_table(url):
    import pyarrow.parquet as pq
    import pyarrow.compute as pc
    from httpfile import HttpFile
    pf = pq.ParquetFile(HttpFile(url))
    md = pf.metadata
    pos_col = pf.schema_arrow.names.index("pos")
    want = []
    for i in range(md.num_row_groups):
        st = md.row_group(i).column(pos_col).statistics
        if st is None or (st.min <= GENE_END and st.max >= GENE_START):
            want.append(i)
    tbl = pf.read_row_groups(want, columns=["pos", "ref", "alt", "llr_calibrated"])
    m = pc.and_(pc.greater_equal(tbl["pos"], GENE_START),
                pc.less_equal(tbl["pos"], GENE_END))
    return tbl.filter(m), len(want)


def main():
    import numpy as np
    print("GPN-Star calibrated LLR — negative = alt allele disfavoured by constraint\n")
    for model, label in MODELS:
        try:
            tbl, ngroups = gene_table(BASE.format(model=model))
        except Exception as e:
            print(f"{model}: FAILED — {type(e).__name__}: {str(e)[:140]}\n")
            continue
        d = tbl.to_pydict()
        pos, ref, alt, llr = d["pos"], d["ref"], d["alt"], np.array(d["llr_calibrated"], float)
        print(f"=== {model}  ({label}) — {len(llr):,} SNVs in BUB1B, {ngroups} row group(s) read ===")
        idx = {}
        for i, (p, r, a) in enumerate(zip(pos, ref, alt)):
            if (p, r, a) in [(v[0], v[1], v[2]) for v in VARIANTS.values()]:
                idx[(p, r, a)] = i
        finite = llr[np.isfinite(llr)]
        print(f"{'variant':<20}{'LLR':>10}{'percentile':>12}{'null median':>13}{'null 1st %ile':>15}")
        for name, (p, r, a) in VARIANTS.items():
            i = idx.get((p, r, a))
            if i is None:
                print(f"{name:<20}{'not found':>10}")
                continue
            v = llr[i]
            pct = 100.0 * float(np.mean(finite < v))
            print(f"{name:<20}{v:>10.3f}{pct:>11.1f}%{np.median(finite):>13.3f}"
                  f"{np.percentile(finite, 1):>15.3f}")
        print()


if __name__ == "__main__":
    main()
