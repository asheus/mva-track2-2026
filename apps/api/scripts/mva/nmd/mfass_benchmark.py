#!/usr/bin/env python3
"""Build a MEASURED-OUTCOME benchmark for the eligibility map, from MFASS.

    python3 -m scripts.mva.nmd.mfass_benchmark /path/to/snv_data_clean.txt

WHY THIS EXISTS, and why the validation we already have is not enough.
`validate_map.py` tests the map against ClinVar labels and reports a Fisher p of 2.7e-22.
That number is close to meaningless, for two reasons that only became visible on
inspecting its composition (CORRECTIONS C29a, C31):

  * EASY POSITIVES. 10 of the 11 pathogenic variants it calls are canonical +/-1,2.
    ClinVar called them pathogenic BECAUSE they are canonical splice variants, so the
    label and the prediction share a cause. Exactly ONE deeper variant is in the set.
  * FREE NEGATIVES. The 658 benign variants it does not call are mostly common variants
    far from any splice site. A predictor that returned "no effect" for everything more
    than 20 bp from a boundary would score almost perfectly against them.

So the test is easy on both margins. The map exists to classify NON-canonical variants,
and on those variants it has never been measured at all.

MFASS (Chong et al., Mol Cell 2019, doi:10.1016/j.molcel.2018.10.037) fixes both margins
at once. It is a multiplexed splicing reporter assay over 27,733 ExAC variants in 2,198
human exons, each with a MEASURED exon-inclusion index, and it is the right instrument
here for three reasons:

  * the positives are measured, not inferred from a clinical label;
  * the negatives are measured too -- variants assayed and found NOT to disrupt
    splicing, in the same sequence contexts as the positives, which is what makes them
    hard rather than free;
  * 90% of its splice-disrupting variants sit outside the canonical sites, and the
    authors state plainly that these are "difficult to predict a priori".

LICENCE. The MFASS repository (github.com/KosuriLab/MFASS) carries NO licence file, so
all rights are reserved and the data may not be redistributed -- the same finding, and
the same treatment, as CobanAkdemirlab/NMDpredictionmodel. This script therefore takes
the data as a PATH ARGUMENT, never vendors it, and writes only our own derived sample
and metrics. Anyone reproducing this fetches the data themselves and cites the paper.

WHAT COUNTS AS A PASS. Fixed here, before any variant is scored, so the result cannot be
rationalised afterwards:

    sensitivity at CALL=0.2, non-canonical measured SDVs     pass >= 0.70   fail < 0.50
    specificity on non-canonical measured non-SDVs           pass >= 0.80   fail < 0.60

The result to expect, named in advance: a specificity failure. CALL=0.2 was set because
the four committed reference variants all score >= 0.49, which establishes a FLOOR, not a
threshold -- nothing has ever measured what 0.2 costs in false positives. And because
measured disruption runs at only ~3% in these regions, even a good specificity implies
poor precision, so PRECISION AT THE PREVALENCE is reported alongside and is the number
that matters for a map a clinician would read.

A low sensitivity would mean something different and worth separating: MFASS is a
minigene reporter in a cell line, so it measures exon recognition in a construct rather
than endogenous splicing of the native locus. A predictor trained on endogenous data can
be right about the gene and wrong about the reporter. That is a stated limit of the
benchmark, not an excuse available after the fact.
"""
import argparse
import collections
import csv
import json
import pathlib
import random
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
# The per-variant sample is NOT a committed path, and that is a licence requirement
# rather than tidiness. A table of coordinate + ref + alt + measured outcome for 27,000
# MFASS variants IS the MFASS dataset, and the source repository carries no licence, so
# redistributing it is not ours to do -- least of all into a submission repository that
# publishes under CC BY 4.0. Only the AGGREGATE metadata below is committed: counts are
# facts about the data, not the data. Pass --out to put the sample wherever you like.
DEFAULT_OUT = pathlib.Path("/tmp/mfass_benchmark_sample.tsv")
META = ROOT / "docs/mva/data/nmd/mfass_benchmark_meta.json"
SEED = 20261015
CANONICAL = 2          # intronic offsets 1-2 are the canonical splice sites
SOURCE_DOI = "10.1016/j.molcel.2018.10.037"


def load(path):
    with open(path, newline="") as f:
        return [r for r in csv.DictReader(f, delimiter="\t")
                if r["category"] == "mutant"
                and r["snp_position_hg38_1based"] not in ("NA", "")]


def resolve_strands(rows):
    """Derive each exon's strand from its own coordinates rather than trusting the
    table's `strand` column, which contradicts the coordinates for 6 of 2,198 exons.

    rel_position is the offset of the SNP within the 170 bp construct, counted along the
    transcribed strand. So it is recoverable from the genomic coordinates in exactly one
    of two ways, and which one works identifies the strand. Requiring agreement across
    every variant in an exon makes this a determination rather than a guess: these exons
    carry a median of ~13 variants each.
    """
    by_exon = collections.defaultdict(list)
    for r in rows:
        by_exon[r["ensembl_id"]].append(r)

    def fits(r, strand):
        s, e = int(r["start_hg38_0based"]), int(r["end_hg38_0based"])
        pos, rp = int(r["snp_position_hg38_1based"]), int(r["rel_position"])
        return ((pos - s) if strand == "+" else (e - pos + 1)) == rp

    strand_of, unresolved, contradicted = {}, [], []
    for ex, rs in by_exon.items():
        p = all(fits(r, "+") for r in rs)
        n = all(fits(r, "-") for r in rs)
        if p == n:                      # both or neither -> we cannot place the exon
            unresolved.append(ex)
            continue
        strand_of[ex] = "+" if p else "-"
        if strand_of[ex] != rs[0]["strand"]:
            contradicted.append(ex)
    return strand_of, unresolved, contradicted


def classify(r, strand):
    """(region, distance) for the SNP, measured against the exon's own boundaries."""
    s = int(r["start_hg38_0based"])
    i1, el, i2 = int(r["intron1_len"]), int(r["exon_len"]), int(r["intron2_len"])
    pos = int(r["snp_position_hg38_1based"])
    lead = i1 if strand == "+" else i2          # genomic-order first flank
    a, b = s + lead + 1, s + lead + el
    if a <= pos <= b:
        return "exonic", min(pos - a, b - pos)
    return "intronic", (a - pos if pos < a else pos - b)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mfass", help="path to MFASS processed_data/snv/snv_data_clean.txt "
                                  "(fetch it yourself; it is not redistributable)")
    ap.add_argument("--n-pos", type=int, default=0,
                    help="sample this many positives (0 = take all)")
    ap.add_argument("--n-neg", type=int, default=0,
                    help="sample this many negatives (0 = take all)")
    ap.add_argument("--out", default=str(DEFAULT_OUT),
                    help="where to write the per-variant sample. NOT a committed path: "
                         "the source data carry no licence and may not be redistributed")
    a = ap.parse_args()
    if not pathlib.Path(a.mfass).exists():
        sys.exit(f"missing {a.mfass}")

    rows = load(a.mfass)
    strand_of, unresolved, contradicted = resolve_strands(rows)
    print(f"{len(rows)} MFASS mutants with an hg38 coordinate")
    print(f"strand resolved for {len(strand_of)} exons; unresolvable {len(unresolved)}")
    print(f"exons whose coordinates contradict the table's strand column: "
          f"{len(contradicted)}")
    if unresolved:
        print("  unresolved exons are DROPPED, not guessed:", ", ".join(unresolved[:8]))

    kept = [r for r in rows if r["ensembl_id"] in strand_of]
    buckets = collections.Counter()
    sdv = collections.Counter()
    labelled = collections.Counter()
    tagged = []
    for r in kept:
        region, d = classify(r, strand_of[r["ensembl_id"]])
        bucket = ("canonical" if region == "intronic" and d <= CANONICAL
                  else "non_canonical_intronic" if region == "intronic" else "exonic")
        buckets[bucket] += 1
        lof = r["strong_lof"]
        if lof in ("TRUE", "FALSE"):
            labelled[bucket] += 1
            sdv[bucket] += (lof == "TRUE")
            tagged.append((r, region, d, bucket, lof == "TRUE"))

    print("\nregion                      n       measured SDV rate")
    for b in ("canonical", "non_canonical_intronic", "exonic"):
        rate = f"{sdv[b] / labelled[b]:.1%}" if labelled[b] else "n/a"
        print(f"  {b:24s} {buckets[b]:6d}   {sdv[b]:5d}/{labelled[b]:<6d} = {rate}")
    k, t = sum(sdv.values()), sum(labelled.values())
    print(f"  {'TOTAL':24s} {sum(buckets.values()):6d}   {k:5d}/{t:<6d} = {k / t:.1%}")
    print(f"\nreproduction check: the paper reports 1,050 SDVs of 27,733 variants "
          f"(3.8%); we get {k} of {t} ({k / t:.1%})")
    outside = k - sdv["canonical"]
    print(f"SDVs outside the canonical sites: {outside}/{k} = {outside / k:.1%}  "
          f"(the paper says 83%, on a definition of 'canonical site' it does not give "
          f"in the abstract; ours is intronic offset 1-2 only)")

    # ---- the benchmark set: non-canonical only, which is the whole point ----
    bench = [x for x in tagged if x[3] != "canonical"]
    pos = [x for x in bench if x[4]]
    neg = [x for x in bench if not x[4]]
    print(f"\nnon-canonical benchmark pool: {len(pos)} measured SDVs, "
          f"{len(neg)} measured non-SDVs")
    rng = random.Random(SEED)
    if a.n_pos and a.n_pos < len(pos):
        pos = rng.sample(pos, a.n_pos)
    if a.n_neg and a.n_neg < len(neg):
        neg = rng.sample(neg, a.n_neg)
    sample = pos + neg
    rng.shuffle(sample)
    print(f"sampling {len(pos)} positives + {len(neg)} negatives "
          f"= {len(sample)} to score (seed {SEED})")

    out_path = pathlib.Path(a.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cols = ["chrom", "pos", "ref", "alt", "ensembl_exon", "strand", "region",
            "distance_to_boundary", "measured_sdv", "delta_dpsi"]
    with out_path.open("w") as f:
        f.write("\t".join(cols) + "\n")
        for r, region, d, bucket, is_sdv in sample:
            f.write("\t".join([
                r["chr"], r["snp_position_hg38_1based"], r["ref_allele"],
                r["alt_allele"], r["ensembl_id"], strand_of[r["ensembl_id"]],
                region, str(d), "1" if is_sdv else "0",
                r.get("delta_dpsi", "")]) + "\n")
    META.write_text(json.dumps({
        "source": "MFASS, Chong et al. Mol Cell 2019",
        "source_doi": SOURCE_DOI,
        "source_repo": "github.com/KosuriLab/MFASS",
        "licence": "no licence file in the source repository; all rights reserved. "
                   "Data are NOT redistributed here -- only our derived sample.",
        "seed": SEED,
        "canonical_definition": "intronic offset 1-2 from an exon boundary",
        "pool_non_canonical_positives": len([x for x in bench if x[4]]),
        "pool_non_canonical_negatives": len([x for x in bench if not x[4]]),
        "sampled_positives": sum(1 for x in sample if x[4]),
        "sampled_negatives": sum(1 for x in sample if not x[4]),
        "exons_strand_contradicted": contradicted,
        "exons_unresolved": unresolved,
        "pass_criteria": {"sensitivity": {"pass": 0.70, "fail": 0.50},
                          "specificity": {"pass": 0.80, "fail": 0.60}},
    }, indent=2) + "\n")
    print(f"\nwrote {len(sample)} rows -> {out_path}  (NOT committed: source data are not redistributable)")
    print(f"wrote metadata           -> {META.relative_to(ROOT)}  (aggregate counts only)")
    print("\nPASS CRITERIA ARE FIXED IN THIS FILE AND IN THE METADATA, BEFORE SCORING:")
    print("  sensitivity >= 0.70 passes, < 0.50 fails")
    print("  specificity >= 0.80 passes, < 0.60 fails")
    print("Precision at the measured prevalence is reported alongside and is the number")
    print("that matters for a map a clinician would read.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
