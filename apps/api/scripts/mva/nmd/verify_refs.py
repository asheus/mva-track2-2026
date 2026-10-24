#!/usr/bin/env python3
"""Verify every variant's reference base against GRCh38 before anything is submitted.

    python3 -m scripts.mva.nmd.verify_refs

SPLICE-AXIS.md records that the first Pangolin submission was built without checking
that computed positions actually carry the claimed reference base, and that checking
against Ensembl caught a mismatch in 1 of 7 variants. A scan of a thousand variants
submitted on unverified coordinates would bury that failure mode rather than remove it.

Reads clinvar_noncoding.tsv, fetches the reference base at each position from Ensembl in
batched POST requests, and writes the verified subset plus a rejected list. Exits
non-zero if the mismatch rate is high enough to suggest a systematic coordinate error
rather than scattered ClinVar noise.
"""
import json
import pathlib
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[5]
IN = ROOT / "docs/mva/data/nmd/clinvar_noncoding.tsv"
OUT = ROOT / "docs/mva/data/nmd/clinvar_noncoding_verified.tsv"
REJ = ROOT / "docs/mva/data/nmd/clinvar_noncoding_rejected.tsv"
REST = "https://rest.ensembl.org/sequence/region/human"
BATCH = 50
# Above this fraction, assume a systematic coordinate problem and refuse to proceed.
MAX_MISMATCH_RATE = 0.05


def fetch_refs(regions):
    """POST a batch of 1-bp regions; returns sequences in request order."""
    body = json.dumps({"regions": [f"{c}:{p}..{p}" for c, p in regions]}).encode()
    req = urllib.request.Request(
        f"{REST}?coord_system_version=GRCh38", data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"})
    for attempt in range(4):
        try:
            return [d["seq"].upper() for d in
                    json.loads(urllib.request.urlopen(req, timeout=180).read())]
        except Exception as e:
            if attempt == 3:
                raise RuntimeError(f"Ensembl batch failed: {e}")
            time.sleep(2 ** attempt)


def main():
    if not IN.exists():
        sys.exit(f"missing {IN}; run clinvar_noncoding.py first")
    lines = IN.read_text().strip().split("\n")
    cols = lines[0].split("\t")
    rows = [dict(zip(cols, L.split("\t"))) for L in lines[1:]]
    print(f"verifying {len(rows)} reference bases against GRCh38 ...", flush=True)

    ok, bad = [], []
    for i in range(0, len(rows), BATCH):
        chunk = rows[i:i + BATCH]
        # Ensembl wants bare chromosome names.
        seqs = fetch_refs([(r["chrom"].replace("chr", ""), int(r["pos"])) for r in chunk])
        for r, s in zip(chunk, seqs):
            (ok if s == r["ref"] else bad).append({**r, "grch38_base": s})
        print(f"  {min(i + BATCH, len(rows)):5d}/{len(rows)}  "
              f"ok={len(ok)} mismatch={len(bad)}", flush=True)
        time.sleep(0.25)

    rate = len(bad) / len(rows) if rows else 0
    for path, data in ((OUT, ok), (REJ, bad)):
        path.parent.mkdir(parents=True, exist_ok=True)
        hdr = cols + ["grch38_base"]
        with path.open("w") as f:
            f.write("\t".join(hdr) + "\n")
            for r in data:
                f.write("\t".join(str(r.get(c, "")) for c in hdr) + "\n")

    print(f"\nverified  {len(ok)}  -> {OUT.relative_to(ROOT)}")
    print(f"rejected  {len(bad)}  -> {REJ.relative_to(ROOT)}   "
          f"({rate:.2%} mismatch)")
    if bad[:5]:
        print("\nfirst mismatches (ClinVar ref vs GRCh38):")
        for r in bad[:5]:
            print(f"  {r['chrom']}:{r['pos']}  ClinVar says {r['ref']}, "
                  f"GRCh38 has {r['grch38_base']}   {r['hgvs_c']}")
    if rate > MAX_MISMATCH_RATE:
        sys.exit(f"\nmismatch rate {rate:.2%} exceeds {MAX_MISMATCH_RATE:.0%} — this "
                 f"looks systematic, not noise. Resolve the coordinate convention "
                 f"before submitting anything built on it.")
    print("\nmismatch rate within tolerance; the verified set is safe to submit.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
