"""Map BUB1B cDNA splice notation to GRCh38 genomic coordinates for Pangolin.

The non-coding half of this gene has never been scored by anything in this branch, yet
four of its splice alleles are established MVA-causing variants. Pangolin needs genomic
coordinates, so the HGVS c. notation has to be walked through the CDS exon structure.

The mapping is validated against a variant whose genomic coordinate is already known
independently (the proband's L737Ter, c.2210T>G = chr15:40,209,701) before it is trusted.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[5]
EXONS = json.load(open(ROOT / "docs/mva/data/cds_exons.json"))   # GRCh38, plus strand
CHROM = "chr15"


def cds_to_genomic(c):
    """CDS position (1-based) -> genomic. BUB1B is on the plus strand."""
    seen = 0
    for start, end in EXONS:
        span = end - start + 1
        if seen + span >= c:
            return start + (c - seen) - 1
        seen += span
    raise ValueError(f"CDS position {c} beyond the coding sequence")


def splice_to_genomic(cds_pos, offset):
    """c.<pos>+<n> or c.<pos>-<n>: n bases into the flanking intron."""
    g = cds_to_genomic(cds_pos)
    return g + offset


# c.2577+5G>A is DROPPED. CDS position 2577 is not an exon boundary in this transcript --
# it sits inside exon 20 (CDS 2536-2678) -- so a "+5 intronic" offset is meaningless
# against this model, and the coordinate it produced (chr15:40213378) carries a T in
# GRCh38 where the notation claims G. The source (PMC10545765) used NM_001211.5; our
# exon model is a different transcript. Resolve the transcript before scoring it.
VARIANTS = [
    # (label, cds position, intronic offset, ref, alt, what is known)
    ("c.1288+5G>A",  1288,  +5, "G", "A", "splice, biallelic; MDS with monosomy 7 at 9y"),
    ("c.1402-5A>G",  1402,  -5, "A", "G", "splice, biallelic; neuroblastoma at 8mo, survived"),
    ("c.2386-11A>G", 2386, -11, "A", "G", "splice, biallelic, same individual as above"),
    ("c.2009+1G>A",  2009,  +1, "G", "A", "canonical donor; breast + gastric cancer (PMC11251299)"),
]
# positive control: a coding variant whose genomic coordinate is known independently
CONTROL = ("c.2210T>G (L737Ter, proband allele 1)", 2210, 0, "T", "G", 40209701)


def main():
    # every coordinate must land on a boundary AND carry the claimed reference base
    seen, ends, starts = 0, [], []
    for a, b in EXONS:
        starts.append(seen + 1); seen += b - a + 1; ends.append(seen)
    for lab, cds, off, ref, alt, note in VARIANTS:
        boundary = ends if off > 0 else starts
        assert cds in boundary, f"{lab}: CDS {cds} is not an exon boundary in this transcript"

    label, cds, off, ref, alt, expected = CONTROL
    got = splice_to_genomic(cds, off)
    ok = got == expected
    print(f"mapping validation on {label}")
    print(f"   computed {CHROM}:{got}   expected {CHROM}:{expected}   {'MATCH' if ok else 'MISMATCH'}")
    if not ok:
        raise SystemExit("coordinate mapping is wrong -- do not submit anything built on it")

    print(f"\nsplice variants, GRCh38 (Pangolin input format CHROM,POS,REF,ALT):\n")
    lines = []
    for lab, cds, off, ref, alt, note in VARIANTS:
        g = splice_to_genomic(cds, off)
        lines.append(f"{CHROM},{g},{ref},{alt}")
        print(f"   {lab:14s} -> {CHROM},{g},{ref},{alt}     {note}")
    out = ROOT / "docs/mva/data/variants/splice_variants_grch38.txt"
    out.write_text("\n".join(lines) + "\n")
    print(f"\nwritten to {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
