#!/usr/bin/env python3
"""Cross NMD-escape predictions for BUB1B nonsense variants with what the
truncated product would retain.

Two independent axes decide whether an NMD-inhibition rationale could even apply
to a given truncating allele:

  1. Does the transcript survive?   -> TrunKitten predicted escape probability
  2. Is the product useful if it does? -> which functional motifs the truncation keeps

Motif coordinates are taken from this repository's own documented values
(docs/mva/NMD-FEASIBILITY.md, docs/mva/ALLELE1-NMD-READTHROUGH.md), not invented here:
  KARD / LxxIxE PP2A-B56 site ...... 669-674   (last functional motif)
  residues contacting the kinase domain  748-753
  pseudokinase domain .............. 766-1050

Usage:
  stratify_bub1b_ptc.py <pred.tsv> <meta.tsv> <out.tsv>
"""
import csv, sys

KARD_END, CONTACT_LO, CONTACT_HI, KINASE_START = 674, 748, 753, 766

def band(res: int) -> tuple[str, str]:
    if res <= KARD_END:
        return ("1_truncates_through_motifs",
                "loses KARD/PP2A-B56 and everything after it")
    if res < CONTACT_LO:
        return ("2_clean_gap",
                "retains all known functional motifs; no kinase-domain contacts lost")
    if res <= CONTACT_HI:
        return ("3_kinase_contact_zone",
                "after KARD but removes residues contacting the kinase domain")
    if res < KINASE_START:
        return ("4_pre_kinase",
                "after the contact zone, before the pseudokinase domain")
    return ("5_within_pseudokinase",
            "truncates inside the pseudokinase domain (766-1050)")

pred = {r["variant_id"]: r for r in csv.DictReader(open(sys.argv[1]), delimiter="\t")}
meta = {r["variant_id"]: r for r in csv.DictReader(open(sys.argv[2]), delimiter="\t")}

rows = []
for vid, m in meta.items():
    p = pred.get(vid)
    if not p:
        continue
    res = int(m["residue"])
    b, why = band(res)
    prob = float(p["escape_prob"])
    rows.append(dict(residue=res, variant_id=vid, hgvs=m["title"],
                     clinvar=m["classification"] or "(none)",
                     escape_prob=round(prob, 4),
                     escape_pred="escape" if int(p["escape_pred_at_youden"]) else "NMD",
                     band=b, product_note=why))
rows.sort(key=lambda r: r["residue"])

with open(sys.argv[3], "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
    w.writeheader(); w.writerows(rows)

# ---- report
print(f"{len(rows)} BUB1B SNV-nonsense variants scored\n")
print(f"{'res':>5} {'ClinVar':28s} {'P(escape)':>9s} {'call':>7s}  band")
for r in rows:
    star = "  <-- proband allele 1" if r["residue"] == 737 else ""
    print(f"{r['residue']:>5} {r['clinvar'][:28]:28s} {r['escape_prob']:9.3f} {r['escape_pred']:>7s}  {r['band']}{star}")

print("\nby band:")
import collections
for b in sorted({r["band"] for r in rows}):
    sub = [r for r in rows if r["band"] == b]
    esc = sum(r["escape_pred"] == "escape" for r in sub)
    print(f"  {b:30s} n={len(sub):2d}  predicted escape={esc}  "
          f"median P={sorted(r['escape_prob'] for r in sub)[len(sub)//2]:.3f}")

print("\nby ClinVar classification:")
for c, sub in sorted(collections.Counter(r["clinvar"] for r in rows).items()):
    s = [r for r in rows if r["clinvar"] == c]
    esc = sum(r["escape_pred"] == "escape" for r in s)
    print(f"  {c[:34]:34s} n={len(s):2d}  predicted escape={esc}")
