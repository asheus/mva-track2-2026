#!/usr/bin/env python3
"""Gene-agnostic PTC stratifier: NMD escape x what the truncated product retains.

Replaces the BUB1B-specific banding in stratify_bub1b_ptc.py. Domain architecture
is read from UniProt features rather than hand-coded, so the only per-gene input is
an accession. That is what makes this run on CEP57 and TRIP13 without edits -- and
what exposes, honestly, that it degenerates to a bare NMD prediction for a gene
UniProt does not annotate.

A PTC at residue R yields a product of R-1 residues. So a feature is
  retained   if end   <  R
  truncated  if start <  R <= end
  lost       if start >= R

Usage: stratify_ptc.py <pred.tsv> <meta.tsv> <uniprot_domains.json> <out.tsv>
"""
import csv, json, sys, collections

pred = {r["variant_id"]: r for r in csv.DictReader(open(sys.argv[1]), delimiter="\t")}
meta = list(csv.DictReader(open(sys.argv[2]), delimiter="\t"))
uni  = json.load(open(sys.argv[3]))

# Features worth reporting as functional units. Disordered regions and bare
# binding sites are kept out of the retained/lost summary: they are not domains,
# and including them would inflate the appearance of domain loss.
KEEP = {"Domain", "Region", "Coiled coil", "Motif"}
SKIP_DESC = ("disordered",)

def units(gene):
    g = uni.get(gene)
    if not g:
        return []
    return [f for f in g["features"]
            if f["type"] in KEEP and not any(s in f["desc"].lower() for s in SKIP_DESC)]

rows = []
for m in meta:
    p = pred.get(m["variant_id"])
    if not p:
        continue
    gene, R = m["gene"], int(m["residue"])
    g = uni.get(gene, {})
    plen = g.get("length")
    retained, truncated, lost = [], [], []
    for f in units(gene):
        label = (f["desc"] or f["type"])[:40]
        if f["end"] < R:        retained.append(label)
        elif f["start"] < R:    truncated.append(label)
        else:                   lost.append(label)
    rows.append(dict(
        gene=gene, residue=R, variant_id=m["variant_id"],
        protein_len=plen or "",
        frac_retained=round((R - 1) / plen, 3) if plen else "",
        escape_prob=round(float(p["escape_prob"]), 4),
        escape_call="escape" if int(p["escape_pred_at_youden"]) else "NMD",
        clinvar=m["classification"] or "(none)",
        n_annotated_units=len(units(gene)),
        retained="; ".join(retained) or "-",
        truncated="; ".join(truncated) or "-",
        lost="; ".join(lost) or "-",
        hgvs=m["title"],
    ))
rows.sort(key=lambda r: (r["gene"], r["residue"]))

with open(sys.argv[4], "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
    w.writeheader(); w.writerows(rows)

for gene in sorted({r["gene"] for r in rows}):
    sub = [r for r in rows if r["gene"] == gene]
    g = uni.get(gene, {})
    nu = sub[0]["n_annotated_units"]
    esc = sum(r["escape_call"] == "escape" for r in sub)
    print(f"\n=== {gene}  ({g.get('accession','?')}, {g.get('length','?')} aa, "
          f"{nu} annotated functional unit(s))  n={len(sub)}  predicted escape={esc}")
    print(f"{'res':>5} {'frac':>5} {'P(esc)':>7} {'call':>7}  {'ClinVar':26s} retained -> lost")
    for r in sub:
        print(f"{r['residue']:>5} {r['frac_retained']:>5} {r['escape_prob']:7.3f} "
              f"{r['escape_call']:>7}  {r['clinvar'][:26]:26s} {r['retained'][:34]} -> {r['lost'][:34]}")

print("\n--- escape rate by gene:")
for gene in sorted({r["gene"] for r in rows}):
    sub = [r for r in rows if r["gene"] == gene]
    esc = sum(r["escape_call"] == "escape" for r in sub)
    print(f"  {gene:8s} {esc}/{len(sub)}")
print("\n--- escape rate by ClinVar class (all genes):")
for c, n in sorted(collections.Counter(r["clinvar"] for r in rows).items()):
    s = [r for r in rows if r["clinvar"] == c]
    print(f"  {c[:34]:34s} {sum(x['escape_call']=='escape' for x in s)}/{n}")
