"""Build a genome-wide CDS interval index from Ensembl gene models.

Step 1 of the Track 1 pipeline. Produces, per chromosome, a sorted list of
(start, end, gene_symbol) over every protein-coding CDS in the genome.

THIS FILE CONTAINS NO GENE LIST. It indexes all ~20,000 protein-coding genes from
Ensembl's own GFF3. The point of the exercise is to reach the causal gene without being
told it, so no stage of this pipeline may name a candidate -- including this one.

    python3 build_cds_index.py --gff3 <Homo_sapiens.GRCh38.*.gff3.gz> --out cds_index.json.gz
"""
import argparse, collections, gzip, json, pathlib, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gff3", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    gene_name = {}          # gene:ENSG -> symbol
    tx_gene = {}            # transcript:ENST -> gene:ENSG
    cds = collections.defaultdict(list)
    n = 0

    with gzip.open(a.gff3, "rt") as f:
        for line in f:
            if line.startswith("#"):
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) < 9:
                continue
            chrom, feat, start, end, attrs = p[0], p[2], p[3], p[4], p[8]
            if feat == "gene":
                d = dict(kv.split("=", 1) for kv in attrs.split(";") if "=" in kv)
                if d.get("biotype") == "protein_coding":
                    gene_name[d.get("ID", "")] = d.get("Name") or d.get("ID", "").split(":")[-1]
            elif feat == "mRNA":
                d = dict(kv.split("=", 1) for kv in attrs.split(";") if "=" in kv)
                if d.get("Parent") in gene_name:
                    tx_gene[d.get("ID", "")] = d["Parent"]
            elif feat == "CDS":
                d = dict(kv.split("=", 1) for kv in attrs.split(";") if "=" in kv)
                g = tx_gene.get(d.get("Parent", ""))
                if g:
                    cds[chrom].append((int(start), int(end), gene_name[g]))
                    n += 1
            if n and n % 500_000 == 0:
                print(f"  {n:,} CDS records", flush=True)

    # Merge overlapping CDS of the same gene: transcripts share exons heavily, and an
    # unmerged index is ~10x larger for no gain in what it answers.
    out = {}
    for chrom, rows in cds.items():
        rows.sort()
        merged = []
        for s, e, g in rows:
            if merged and merged[-1][2] == g and s <= merged[-1][1] + 1:
                merged[-1][1] = max(merged[-1][1], e)
            else:
                merged.append([s, e, g])
        out[chrom] = merged

    dest = pathlib.Path(a.out)
    with gzip.open(dest, "wt") as f:
        json.dump(out, f)
    genes = {g for rows in out.values() for _, _, g in rows}
    print(f"\n{n:,} CDS records -> {sum(len(v) for v in out.values()):,} merged intervals")
    print(f"{len(genes):,} protein-coding genes across {len(out)} sequences -> {dest}")


if __name__ == "__main__":
    main()
