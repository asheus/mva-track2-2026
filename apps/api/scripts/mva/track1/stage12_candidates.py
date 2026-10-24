"""Stages 1-2 of genome-wide prioritisation: coding + biallelic-compatible.

    python3 stage12_candidates.py --vcf <vcf.gz> --index cds_index.json.gz --out stage2.json

NO GENE IS NAMED ANYWHERE IN THIS PIPELINE. The whole point is to reach the causal gene
from the callset and the phenotype alone, so every stage is a general rule.

Stage 1  PASS, non-reference, and inside a protein-coding CDS interval.
Stage 2  the gene shows a genotype pattern compatible with recessive disease: at least
         one homozygous-alternate call, or at least two heterozygous calls that could be
         in trans. A variant in overlapping genes is credited to EACH of them.
"""
import argparse, collections, json, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from cds_lookup import CdsIndex


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vcf", required=True)
    ap.add_argument("--index", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    import pysam

    ix = CdsIndex(a.index)
    print(f"CDS index: {ix.n_genes:,} protein-coding genes", flush=True)
    v = pysam.VariantFile(a.vcf)
    sample = list(v.header.samples)[0]

    tot = npass = nnonref = ncds = 0
    by_gene = collections.defaultdict(list)
    for r in v:
        tot += 1
        if list(r.filter.keys()) not in ([], ["PASS"]):
            continue
        npass += 1
        gt = r.samples[sample].get("GT") or ()
        alleles = {g for g in gt if g is not None}
        if not alleles or alleles == {0}:
            continue
        nnonref += 1
        genes = ix.genes_at(r.chrom, r.pos)
        if not genes:
            continue
        ncds += 1
        zyg = "het" if 0 in alleles else "hom"
        rec = {"chrom": r.chrom, "pos": r.pos, "ref": r.ref,
               "alt": ",".join(r.alts or ()), "zyg": zyg,
               "dp": r.samples[sample].get("DP"), "gq": r.samples[sample].get("GQ")}
        for g in genes:
            by_gene[g].append(rec)
        if tot % 1_000_000 == 0:
            print(f"  {tot:,} records scanned", flush=True)

    bi = {g: vs for g, vs in by_gene.items()
          if any(x["zyg"] == "hom" for x in vs)
          or sum(1 for x in vs if x["zyg"] == "het") >= 2}

    print(f"\n{'total records':22s} {tot:>10,}")
    print(f"{'PASS':22s} {npass:>10,}")
    print(f"{'non-reference':22s} {nnonref:>10,}")
    print(f"{'in a coding CDS':22s} {ncds:>10,}  across {len(by_gene):,} genes")
    print(f"{'biallelic-compatible':22s} {sum(len(v) for v in bi.values()):>10,}  "
          f"across {len(bi):,} genes")
    pathlib.Path(a.out).write_text(json.dumps(bi))
    print(f"-> {a.out}")


if __name__ == "__main__":
    main()
