#!/usr/bin/env python3
"""Parse ClinVar esummary XML into a PTC variant table for the NMD pipeline.

Keeps only single-nucleotide variants producing p.XxxNNNTer with a GRCh38
position, because TrunCat/TrunKitten are models for PTC-producing SNVs.
Frameshift and splice alleles are deliberately dropped, not silently mixed in.

Usage: clinvar_ptc.py <esummary.xml> <GENE> <ENST.version> <out_variants.tsv> <out_meta.tsv>
"""
import re, csv, sys

xml_path, gene, tx, out_v, out_m = sys.argv[1:6]
x = open(xml_path).read()
recs = re.findall(r'<DocumentSummary uid="(\d+)">(.*?)</DocumentSummary>', x, re.S)

rows = []
dropped = {"not_snv_nonsense": 0, "no_grch38": 0}
for uid, body in recs:
    t = re.search(r"<title>(.*?)</title>", body, re.S)
    if not t:
        continue
    title = t.group(1).replace("&gt;", ">").replace("&lt;", "<").strip()
    m = re.search(r"c\.(\d+)([ACGT])>([ACGT])\s*\(p\.[A-Za-z]{3}(\d+)Ter\)", title)
    if not m:
        dropped["not_snv_nonsense"] += 1
        continue
    pos = ""
    loc = re.search(r"<variation_loc>(.*?)</variation_loc>", body, re.S)
    if loc:
        for blk in re.findall(r"<assembly_set>(.*?)</assembly_set>", loc.group(1), re.S):
            if "GRCh38" in blk:
                s = re.search(r"<start>(.*?)</start>", blk)
                if s:
                    pos = s.group(1)
    if not pos:
        dropped["no_grch38"] += 1
        continue
    germ = re.search(r"<germline_classification>.*?<description>(.*?)</description>", body, re.S)
    chrom = re.search(r"<chr>(.*?)</chr>", loc.group(1)) if loc else None
    rows.append(dict(uid=uid, chrom="chr" + chrom.group(1) if chrom else "",
                     position=int(pos), ref=m.group(2), alt=m.group(3),
                     residue=int(m.group(4)),
                     cls=(germ.group(1).strip() if germ else ""), title=title))
rows.sort(key=lambda r: r["residue"])

with open(out_v, "w", newline="") as fh:
    w = csv.writer(fh, delimiter="\t")
    w.writerow(["variant_id", "contig", "position", "refAllele", "altAllele", "gene", "txnames"])
    for r in rows:
        w.writerow([f"{gene}_p.{r['residue']}Ter_{r['uid']}", r["chrom"], r["position"],
                    r["ref"], r["alt"], gene, tx])
with open(out_m, "w", newline="") as fh:
    w = csv.writer(fh, delimiter="\t")
    w.writerow(["variant_id", "gene", "residue", "classification", "title"])
    for r in rows:
        w.writerow([f"{gene}_p.{r['residue']}Ter_{r['uid']}", gene, r["residue"], r["cls"], r["title"]])

print(f"{gene}: {len(recs)} ClinVar records -> {len(rows)} SNV-nonsense with GRCh38 position")
print(f"  dropped: {dropped}")
if rows:
    print(f"  residues: {[r['residue'] for r in rows]}")
