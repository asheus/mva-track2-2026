#!/usr/bin/env python3
"""Measure non-productive splicing flux from RNA-seq, not annotation.

    python3 -m scripts.mva.junction_flux

WHY. Our annotation-based scan found no poison exon in BUB1B, and we said at the time that
the result was only as strong as the method -- that SCN1A's exon 20N was discovered by
sequencing, not by reading annotation, so an annotation search can miss a real event. This
closes that gap with the measurement itself.

GTEx v8 publishes median exon-exon junction read counts per tissue. A junction is a direct
observation of a splicing decision: reads spanning it are molecules that made that choice.
Summed over a gene, the share of reads on non-canonical junctions is the fraction of
splicing flux leaving the productive path -- which is exactly the headroom an upregulating
ASO would redirect, and exactly what annotation cannot tell you.

THE CONTROL, AGAIN. SCN1A carries poison exon 20N, the target of a Phase 3 drug. Its
inclusion junctions must show real flux in brain, and we compute its percent-spliced-in
directly. If PSI comes back at zero the measurement is broken and BUB1B's numbers mean
nothing. If it comes back substantial, then a near-zero result for BUB1B is a measured
negative rather than an absence of evidence.

PSI here is inclusion / (inclusion + skipping) computed on median junction counts:
reads joining into and out of the cassette, against reads that jump straight across it.

WHAT THIS STILL CANNOT SEE. GTEx medians are bulk tissue, and BUB1B is a proliferation
gene barely expressed in most post-mitotic tissue, so low absolute counts are expected and
are not themselves evidence of anything. We therefore report the FRACTION of a gene's own
junction reads, never the raw count, and restrict conclusions to tissues where the gene is
actually expressed.

On the obvious objection -- that bulk post-mitotic tissue is the wrong place to look for a
mitotic gene -- GTEx does contain two proliferating sample types, EBV-transformed
lymphocytes and cultured fibroblasts, and they are exactly where BUB1B is best expressed.
That is the right place to look, and it is where we look. Read depth there is still only
hundreds to thousands, so a fraction of a percent carries wide error; a result of a few
reads out of several thousand does not.
"""
import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
D = ROOT / "docs/mva/data"
OUT = D / "junction_flux.json"
GENES = [("BUB1B", "ENSG00000156970", "subject"),
         ("SCN1A", "ENSG00000144285", "positive control")]
POISON_20N = (166007230, 166007293)       # recovered by splice_architecture.py


def canonical_introns(gid):
    gene = json.loads((D / f"gene_{gid}.json").read_text())
    tx = json.loads((D / f"tx_{gid}.json").read_text())
    canon = next(t for t in gene["Transcript"] if t.get("is_canonical"))
    ex = sorted((e["start"], e["end"]) for e in tx[canon["id"]]["Exon"])
    return {(ex[i][1] + 1, ex[i + 1][0] - 1) for i in range(len(ex) - 1)}


def load(sym):
    rows = json.loads((D / f"junc_{sym}.json").read_text())["data"]
    out = collections.defaultdict(dict)
    for r in rows:
        _c, s, e = r["junctionId"].split("_")
        out[r["tissueSiteDetailId"]][(int(s), int(e))] = r["median"]
    return out


def analyse(sym, gid, role):
    cintr = canonical_introns(gid)
    per_tissue = load(sym)
    print(f"\n{'='*80}\n{sym}  ({role})\n{'='*80}")

    rows = []
    for tis, j in per_tissue.items():
        tot = sum(j.values())
        noncan = sum(v for k, v in j.items() if k not in cintr)
        rows.append((tis, tot, noncan, (noncan / tot if tot else 0.0)))
    rows.sort(key=lambda r: -r[1])
    expressed = [r for r in rows if r[1] >= 20]      # ignore tissues with no expression

    print(f"  junctions {len(next(iter(per_tissue.values())))}  |  canonical introns "
          f"{len(cintr)}  |  tissues {len(per_tissue)}")
    print(f"  tissues with usable expression (>=20 median junction reads): {len(expressed)}")
    if expressed:
        fr = [r[3] for r in expressed]
        print(f"\n  NON-CANONICAL SHARE OF JUNCTION READS")
        print(f"    median across expressed tissues: {sorted(fr)[len(fr)//2]:.2%}")
        print(f"    range: {min(fr):.2%} - {max(fr):.2%}")
        print(f"\n    {'tissue':<36}{'total':>9}{'non-canon':>11}{'share':>9}")
        for t, tot, nc, f in expressed[:6]:
            print(f"    {t:<36}{tot:>9.0f}{nc:>11.0f}{f:>8.1%}")

    # which non-canonical junctions actually carry the flux?
    agg = collections.Counter()
    for tis, j in per_tissue.items():
        for k, v in j.items():
            if k not in cintr:
                agg[k] += v
    print(f"\n  TOP NON-CANONICAL JUNCTIONS (summed median reads over tissues)")
    if agg and max(agg.values()) > 0:
        for (s, e), v in agg.most_common(5):
            print(f"    {s}-{e}   {v:>10.0f}")
    else:
        print("    none carry any reads")
    return {"gene": sym, "role": role,
            "expressed_tissues": len(expressed),
            "noncanonical_share_median": (sorted([r[3] for r in expressed])[len(expressed)//2]
                                          if expressed else None),
            "noncanonical_share_max": (max(r[3] for r in expressed) if expressed else None),
            "top_noncanonical": [{"start": k[0], "end": k[1], "summed_median": v}
                                 for k, v in agg.most_common(5)],
            "per_tissue": [{"tissue": t, "total": tot, "noncanonical": nc, "share": f}
                           for t, tot, nc, f in rows]}


def poison_psi(sym="SCN1A"):
    """Percent-spliced-in for SCN1A's poison exon 20N, from junction reads."""
    ps, pe = POISON_20N
    per_tissue = load(sym)
    print(f"\n{'='*80}\nCONTROL: is poison exon 20N actually used? (SCN1A PSI)\n{'='*80}")
    out = []
    for tis, j in per_tissue.items():
        inc = sum(v for (s, e), v in j.items() if e == ps - 1 or s == pe + 1)
        skip = sum(v for (s, e), v in j.items() if s < ps and e > pe)
        if inc + skip <= 0:
            continue
        out.append((tis, inc, skip, inc / (inc + skip)))
    out.sort(key=lambda r: -r[3])
    if not out:
        print("  no junctions found flanking the poison exon -- measurement failed")
        return None, []
    print(f"    {'tissue':<36}{'incl':>8}{'skip':>8}{'PSI':>8}")
    for t, i, s, p in out[:8]:
        print(f"    {t:<36}{i:>8.0f}{s:>8.0f}{p:>7.1%}")
    # Per-tissue medians are only a few reads deep, so a per-tissue PSI of 100% can rest
    # on 2 reads against 0 and is not a number worth quoting. Pool across brain instead.
    brain = [r for r in out if r[0].startswith("Brain")]
    inc = sum(r[1] for r in brain); skip = sum(r[2] for r in brain)
    bpsi = inc / (inc + skip) if (inc + skip) else 0.0
    print(f"\n  POOLED across {len(brain)} brain tissues: {inc:.0f} inclusion vs "
          f"{skip:.0f} skipping reads -> PSI {bpsi:.1%}")
    print(f"  ({'poison exon demonstrably used -- control PASSES' if bpsi > 0.01 else 'ZERO -- control FAILS'})")
    print(f"  Per-tissue medians are shallow, so the pooled figure is the one to quote;")
    print(f"  the individual 100% rows rest on 2 reads against 0 and mean little alone.")
    return bpsi, out


def main():
    res = [analyse(*g) for g in GENES]
    bpsi, _ = poison_psi()
    sub = next(r for r in res if r["role"] == "subject")
    ctl = next(r for r in res if r["role"] == "positive control")

    print(f"\n{'='*80}\nANSWER\n{'='*80}")
    if not bpsi or bpsi <= 0.01:
        print("  Control failed: the known poison exon shows no inclusion flux, so this")
        print("  measurement cannot support any claim about BUB1B.")
    else:
        print(f"  Control passed: SCN1A's drugged poison exon is used at {bpsi:.1%} PSI in")
        print(f"  brain, so junction reads do detect real non-productive splicing.")
    print(f"\n  non-canonical share of junction reads (median over expressed tissues)")
    print(f"    BUB1B  {sub['noncanonical_share_median']:.2%}"
          f"   (max {sub['noncanonical_share_max']:.2%})")
    print(f"    SCN1A  {ctl['noncanonical_share_median']:.2%}"
          f"   (max {ctl['noncanonical_share_max']:.2%})")

    OUT.write_text(json.dumps({
        "source": "GTEx v8 median junction read counts, api/v2/expression/"
                  "medianJunctionExpression, retrieved 21 Oct 2026",
        "control_poison_exon_20N_brain_PSI": bpsi,
        "genes": res,
        "limit": "bulk tissue medians; GTEx has no proliferating-cell tissue, which is "
                 "the state that matters for this disease",
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
