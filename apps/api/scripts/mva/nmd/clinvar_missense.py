#!/usr/bin/env python3
"""Pull every BUB1B missense SNV from ClinVar with its residue number.

    python3 -m scripts.mva.nmd.clinvar_missense

Needed for the eligibility join. We hold computed stability deltas for only 30 missense
variants, but RSA is known for all 1,050 residues, so every missense variant can at
least be assigned a STRUCTURAL CONTEXT -- which decides whether the abundance question
is answerable for it at all. That is the honest unit of output: not a fabricated
eligibility call, but which class of evidence applies.

The residue number comes from the p. notation in the ClinVar title. Variants whose title
carries no parseable p.XxxNNNYyy are dropped and counted rather than guessed at.
"""
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[5]
OUT = ROOT / "docs/mva/data/nmd/clinvar_missense.tsv"
E = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
Q = ('BUB1B[gene] AND "single nucleotide variant"[Type of variation] '
     'AND "missense variant"[Molecular consequence]')
AA3 = {"Ala": "A", "Arg": "R", "Asn": "N", "Asp": "D", "Cys": "C", "Gln": "Q",
       "Glu": "E", "Gly": "G", "His": "H", "Ile": "I", "Leu": "L", "Lys": "K",
       "Met": "M", "Phe": "F", "Pro": "P", "Ser": "S", "Thr": "T", "Trp": "W",
       "Tyr": "Y", "Val": "V"}


def main():
    u = (f"{E}/esearch.fcgi?db=clinvar&term={urllib.parse.quote(Q)}"
         f"&retmax=5000&retmode=json")
    uids = json.loads(urllib.request.urlopen(u, timeout=120).read())
    uids = uids["esearchresult"]["idlist"]
    print(f"{len(uids)} missense uids", flush=True)

    rows, dropped = [], 0
    for i in range(0, len(uids), 200):
        chunk = ",".join(uids[i:i + 200])
        uu = f"{E}/esummary.fcgi?db=clinvar&id={chunk}&retmode=xml"
        for attempt in range(4):
            try:
                x = urllib.request.urlopen(uu, timeout=180).read().decode()
                break
            except Exception as e:
                if attempt == 3:
                    sys.exit(f"esummary failed: {e}")
                time.sleep(2 ** attempt)
        for uid, body in re.findall(
                r'<DocumentSummary uid="(\d+)">(.*?)</DocumentSummary>', x, re.S):
            t = re.search(r"<title>(.*?)</title>", body, re.S)
            if not t:
                dropped += 1
                continue
            title = t.group(1).replace("&gt;", ">").replace("&lt;", "<").strip()
            m = re.search(r"\(p\.([A-Za-z]{3})(\d+)([A-Za-z]{3})\)", title)
            if not m or m.group(1) not in AA3 or m.group(3) not in AA3:
                dropped += 1
                continue
            chrom = pos = ""
            loc = re.search(r"<variation_loc>(.*?)</variation_loc>", body, re.S)
            if loc:
                for blk in re.findall(r"<assembly_set>(.*?)</assembly_set>",
                                      loc.group(1), re.S):
                    if ">GRCh38<" not in blk:
                        continue
                    c = re.search(r"<chr>(.*?)</chr>", blk)
                    s = re.search(r"<start>(\d+)</start>", blk)
                    if c and s:
                        chrom, pos = f"chr{c.group(1)}", s.group(1)
                    break
            sig = re.search(r"<description>(.*?)</description>", body, re.S)
            hg = re.search(r"(c\.\d+[ACGT]>[ACGT])", title)
            rows.append({
                "uid": uid, "chrom": chrom, "pos": pos,
                "hgvs_c": hg.group(1) if hg else "",
                "residue": int(m.group(2)),
                "aa_from": AA3[m.group(1)], "aa_to": AA3[m.group(3)],
                "variant": f"{AA3[m.group(1)]}{m.group(2)}{AA3[m.group(3)]}",
                "clinvar_significance": (sig.group(1).strip() if sig else "").replace("\t", " "),
            })
        time.sleep(0.4)

    rows.sort(key=lambda r: r["residue"])
    cols = ["uid", "chrom", "pos", "hgvs_c", "residue", "aa_from", "aa_to",
            "variant", "clinvar_significance"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        f.write("\t".join(cols) + "\n")
        for r in rows:
            f.write("\t".join(str(r[c]) for c in cols) + "\n")
    print(f"wrote {len(rows)} missense variants -> {OUT.relative_to(ROOT)}")
    print(f"dropped (no parseable p. change): {dropped}")
    inside = sum(1 for r in rows if 766 <= r["residue"] <= 1050)
    print(f"  in the pseudokinase domain (766-1050): {inside}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
