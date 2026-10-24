#!/usr/bin/env python3
"""Pull every non-coding BUB1B SNV from ClinVar, with GRCh38 coordinates.

    python3 -m scripts.mva.nmd.clinvar_noncoding          # writes the variant table

WHY. Our Track 1 cascade is coding-only (CORRECTIONS C10), and C17 established that in
this gene the second allele has been found OUTSIDE the coding sequence four separate
times -- once invisible even to genome sequencing. The visible competitor submissions
use coding annotation and ClinVar intersection, so every team in this challenge,
including us, would miss a non-coding second allele. This is the input set for closing
that gap.

Scope: single-nucleotide variants with molecular consequence "intron variant" or
"synonymous variant", plus the canonical splice donor/acceptor set which is retained as
POSITIVE CONTROLS -- their mechanism is already known, so a scan that fails to flag them
is broken.

Reference bases are NOT trusted from ClinVar titles. SPLICE-AXIS.md records that 1 of 7
hand-mapped coordinates carried the wrong reference base, caught only by checking
Ensembl, so verification is a separate step (verify_refs.py) and this script only
records what ClinVar says.
"""
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[5]
OUT = ROOT / "docs/mva/data/nmd/clinvar_noncoding.tsv"
E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
GENE = "BUB1B"
# BUB1B spans chr15:40,160,984-40,221,137. From 40,217,428 the gene overlaps PAK6 and the
# BUB1B-PAK6 readthrough, and a multi-gene annotation breaks Pangolin's CSV writer and
# fails the whole job (C25a). Variants at or past this point must be submitted alone.
OVERLAP_FROM = 40217428
CLASSES = {
    "intron variant": "intronic",
    "synonymous variant": "synonymous",
    "splice donor variant": "splice_donor",
    "splice acceptor variant": "splice_acceptor",
}


def esearch(consequence):
    q = (f'{GENE}[gene] AND "single nucleotide variant"[Type of variation] '
         f'AND "{consequence}"[Molecular consequence]')
    u = (f"{E}/esearch.fcgi?db=clinvar&term={urllib.parse.quote(q)}"
         f"&retmax=5000&retmode=json")
    d = json.loads(urllib.request.urlopen(u, timeout=120).read())
    return d["esearchresult"]["idlist"]


def esummary(uids):
    """Fetch in batches; ClinVar rejects very long id lists."""
    out = []
    for i in range(0, len(uids), 200):
        chunk = ",".join(uids[i:i + 200])
        u = f"{E}/esummary.fcgi?db=clinvar&id={chunk}&retmode=xml"
        for attempt in range(4):
            try:
                out.append(urllib.request.urlopen(u, timeout=180).read().decode())
                break
            except Exception as e:
                if attempt == 3:
                    sys.exit(f"esummary failed after retries: {e}")
                time.sleep(2 ** attempt)
        time.sleep(0.4)
    return out


def parse(xml_blobs, consequence_label):
    rows = []
    for x in xml_blobs:
        for uid, body in re.findall(
                r'<DocumentSummary uid="(\d+)">(.*?)</DocumentSummary>', x, re.S):
            t = re.search(r"<title>(.*?)</title>", body, re.S)
            if not t:
                continue
            title = (t.group(1).replace("&gt;", ">").replace("&lt;", "<").strip())
            # GRCh38 location block
            chrom = start = ref = alt = ""
            loc = re.search(r"<variation_loc>(.*?)</variation_loc>", body, re.S)
            if loc:
                for blk in re.findall(r"<assembly_set>(.*?)</assembly_set>",
                                      loc.group(1), re.S):
                    if ">GRCh38<" not in blk:
                        continue
                    c = re.search(r"<chr>(.*?)</chr>", blk)
                    s = re.search(r"<start>(\d+)</start>", blk)
                    r_ = re.search(r"<ref>([ACGT]+)</ref>", blk)
                    a_ = re.search(r"<alt>([ACGT]+)</alt>", blk)
                    if c and s:
                        chrom, start = c.group(1), s.group(1)
                        ref = r_.group(1) if r_ else ""
                        alt = a_.group(1) if a_ else ""
                    break
            if not (chrom and start):
                continue
            # Fall back to the HGVS in the title when ref/alt are absent from the block.
            if not (ref and alt):
                m = re.search(r"([ACGT])>([ACGT])", title)
                if m:
                    ref, alt = m.group(1), m.group(2)
            if not (ref and alt and len(ref) == 1 and len(alt) == 1):
                continue
            sig = re.search(r"<description>(.*?)</description>", body, re.S)
            hgvs = re.search(r"(c\.[-+*\d_]+[ACGT]>[ACGT])", title)
            rows.append({
                "uid": uid,
                "chrom": f"chr{chrom}",
                "pos": int(start),
                "ref": ref,
                "alt": alt,
                "hgvs_c": hgvs.group(1) if hgvs else "",
                "consequence": consequence_label,
                "clinvar_significance": (sig.group(1).strip() if sig else "").replace("\t", " "),
                "in_overlap_region": int(int(start) >= OVERLAP_FROM),
            })
    return rows


def main():
    all_rows, seen = [], set()
    for consequence, label in CLASSES.items():
        uids = esearch(consequence)
        print(f"{label:16s} {len(uids):5d} uids", flush=True)
        rows = parse(esummary(uids), label)
        kept = 0
        for r in rows:
            key = (r["chrom"], r["pos"], r["ref"], r["alt"])
            if key in seen:      # a variant can carry several consequences
                continue
            seen.add(key)
            all_rows.append(r)
            kept += 1
        print(f"{'':16s} {kept:5d} parsed with GRCh38 coords + single-base ref/alt",
              flush=True)

    all_rows.sort(key=lambda r: r["pos"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cols = ["uid", "chrom", "pos", "ref", "alt", "hgvs_c", "consequence",
            "clinvar_significance", "in_overlap_region"]
    with OUT.open("w") as f:
        f.write("\t".join(cols) + "\n")
        for r in all_rows:
            f.write("\t".join(str(r[c]) for c in cols) + "\n")

    n_overlap = sum(r["in_overlap_region"] for r in all_rows)
    print(f"\nwrote {len(all_rows)} variants -> {OUT.relative_to(ROOT)}")
    print(f"  batchable (BUB1B-only region):   {len(all_rows) - n_overlap}")
    print(f"  must run solo (PAK6 overlap):    {n_overlap}")
    by = {}
    for r in all_rows:
        by[r["consequence"]] = by.get(r["consequence"], 0) + 1
    for k, v in sorted(by.items()):
        print(f"  {k:16s} {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
