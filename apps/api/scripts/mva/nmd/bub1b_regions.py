#!/usr/bin/env python3
"""Derive each variant's region on the BUB1B canonical transcript, instead of asking
ClinVar for it.

    python3 -m scripts.mva.nmd.bub1b_regions

THE BUG THIS REPLACES (C35, C36). The variant set was built with the ClinVar query

    BUB1B[gene] AND "intron variant"[Molecular consequence]

which does not require the gene and the consequence to describe the SAME FEATURE. PAK6
overlaps BUB1B's last two exons, so 200 variants that are EXONIC on the BUB1B canonical
transcript carry an "intron variant" consequence computed on a PAK6 transcript, and they
entered a set described as BUB1B intronic variants. All 200 are intronic in PAK6
ENST00000453867 and ENST00000441369; only 2 of 200 are intronic in any BUB1B transcript.

The fix is not a different transcript and not a cleverer ClinVar filter. It is to stop
treating a third party's gene-agnostic annotation as the answer to a question we can
compute exactly: *given a genomic position, is it exonic or intronic on
ENST00000287598?* ClinVar's consequence is kept verbatim as provenance and as something
to disagree with, never as the classification.

WHY THIS TRANSCRIPT, established externally rather than by self-agreement (C36).
ENST00000287598 is Ensembl's canonical BUB1B transcript (`is_canonical: 1`), 23 exons,
1,050 aa. Its CDS sums to 3,153 nt = 1,050 aa + stop, matching UniProt O60566; the full
exon model including UTRs derives the committed CDS-only model identically; and it
reproduces the HGVS of both of the proband's alleles from coordinates alone. Agreeing
with ClinVar's own HGVS was deliberately NOT counted as evidence, because two parties
choosing the same wrong transcript would also agree.

THE SELFTEST IS THE POINT. The four variants carrying committed reference scores have
intronic offsets stated in their names -- +5, -5, -11, +1 -- and this module must
reproduce each offset AND which side of the exon it falls on, from the coordinate alone.
If it cannot, every region in the output is suspect and nothing is written.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
TX = ROOT / "docs/mva/data/bub1b_transcript.json"
IN = ROOT / "docs/mva/data/nmd/clinvar_noncoding_verified.tsv"
OUT = ROOT / "docs/mva/data/nmd/bub1b_regions.tsv"
CANONICAL_SPLICE = 2

# position -> (expected signed intronic offset). Sign follows HGVS: + is downstream of
# the exon end (donor side), - is upstream of the exon start (acceptor side).
SELFTEST = {
    40196779: ("c.1288+5G>A", +5),
    40200239: ("c.1402-5A>G", -5),
    40212488: ("c.2386-11A>G", -11),
    40206459: ("c.2009+1G>A", +1),
    # and two exonic controls: the proband's own alleles, with their CDS positions
    40209701: ("c.2210T>G allele 1", None),
    40220612: ("c.3006T>G allele 2", None),
}
EXONIC_SELFTEST = {40209701: 2210, 40220612: 3006}


def load_tx():
    t = json.loads(TX.read_text())
    if t["strand"] != 1:
        sys.exit("this module assumes the + strand, which BUB1B is")
    t["exons"] = [tuple(x) for x in t["exons"]]
    return t


def classify(pos, t):
    """(region, signed_intronic_offset, cds_pos) for a genomic position.

    region is one of: cds_exonic, utr5_exonic, utr3_exonic, canonical_splice_site,
    intronic, outside_transcript.
    """
    exons, cs, ce = t["exons"], t["cds_start"], t["cds_end"]
    if not (t["transcript_start"] <= pos <= t["transcript_end"]):
        return "outside_transcript", None, None
    for s, e in exons:
        if s <= pos <= e:
            if cs <= pos <= ce:
                seen = 0
                for a, b in exons:
                    x, y = max(a, cs), min(b, ce)
                    if x > y:
                        continue
                    if x <= pos <= y:
                        return "cds_exonic", None, seen + (pos - x) + 1
                    seen += y - x + 1
            return ("utr5_exonic" if pos < cs else "utr3_exonic"), None, None
    # intronic: find the flanking exons
    prev = max((e for s, e in exons if e < pos), default=None)
    nxt = min((s for s, e in exons if s > pos), default=None)
    if prev is None or nxt is None:
        return "intronic", None, None
    d_donor = pos - prev          # +n past the upstream exon's end
    d_accept = pos - nxt          # -n before the downstream exon's start
    off = d_donor if d_donor <= -d_accept else d_accept
    region = ("canonical_splice_site" if abs(off) <= CANONICAL_SPLICE else "intronic")
    return region, off, None


def selftest(t):
    ok = True
    print("SELFTEST -- offsets and sides reproduced from coordinates alone")
    for pos, (label, expect) in SELFTEST.items():
        region, off, cds = classify(pos, t)
        if expect is not None:
            good = off == expect
            print(f"  {label:22s} chr15:{pos}  offset {str(off):>4}  "
                  f"expected {expect:+d}  {'PASS' if good else 'FAIL'}  [{region}]")
            ok &= good
        else:
            want = EXONIC_SELFTEST[pos]
            good = region == "cds_exonic" and cds == want
            print(f"  {label:22s} chr15:{pos}  {region:14s} CDS {cds}  "
                  f"expected CDS {want}  {'PASS' if good else 'FAIL'}")
            ok &= good
    return ok


def main():
    for p in (TX, IN):
        if not p.exists():
            sys.exit(f"missing {p}")
    t = load_tx()
    print(f"{t['transcript']}.{t['version']}  canonical={t['is_canonical']}  "
          f"{len(t['exons'])} exons  {t['protein_length_aa']} aa\n")
    if not selftest(t):
        sys.exit("\nSELFTEST FAILED -- refusing to write regions. Every region in the "
                 "output would be suspect.")
    print("  selftest passed\n")

    lines = IN.read_text().strip().split("\n")
    cols = lines[0].split("\t")
    rows = [dict(zip(cols, L.split("\t"))) for L in lines[1:]]

    counts, conflicts = {}, []
    out = []
    for r in rows:
        pos = int(r["pos"])
        region, off, cds = classify(pos, t)
        counts[region] = counts.get(region, 0) + 1
        # ClinVar says intronic; our transcript says the position is in an exon.
        clin = r["consequence"]
        conflict = int(clin == "intronic" and region.endswith("exonic"))
        if conflict:
            conflicts.append(r)
        out.append({**r, "tx_region": region,
                    "tx_intronic_offset": "" if off is None else off,
                    "tx_cds_pos": "" if cds is None else cds,
                    "clinvar_consequence": clin,
                    "consequence_conflict": conflict})

    print("REGION ON THE BUB1B CANONICAL TRANSCRIPT -- derived, not inherited")
    for k in sorted(counts, key=lambda x: -counts[x]):
        print(f"  {k:24s} {counts[k]:5d}")
    print(f"  {'TOTAL':24s} {len(rows):5d}")

    print(f"\nCONFLICTS -- ClinVar says intron variant, our transcript says exonic: "
          f"{len(conflicts)}")
    print("  These are BUB1B-exonic / PAK6-intronic (C36). They are kept and scored --")
    print("  an exonic variant disrupts splicing at 3.8% in our MFASS reconstruction --")
    print("  but they are NOT counted as non-coding, and the coding-pipeline recall")
    print("  argument does not apply to them.")

    truly_noncoding = sum(v for k, v in counts.items()
                          if k in ("intronic", "canonical_splice_site"))
    print(f"\nTHE NUMBER THE RECALL ARGUMENT MAY USE: {truly_noncoding}")
    print(f"  (intronic + canonical splice sites, on the BUB1B canonical transcript)")
    print(f"  not {len(rows)}, which is the whole set a protein-level predictor "
          f"cannot score")

    cw = cols + ["tx_region", "tx_intronic_offset", "tx_cds_pos",
                 "consequence_conflict"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        f.write("\t".join(cw) + "\n")
        for r in out:
            f.write("\t".join(str(r.get(c, "")).replace("\t", " ") for c in cw) + "\n")
    print(f"\nwrote {len(out)} rows -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
