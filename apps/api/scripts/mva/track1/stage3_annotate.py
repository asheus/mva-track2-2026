"""Stage 3: annotate the coding candidates with Ensembl VEP, then filter on rarity
and predicted impact, then re-test the biallelic pattern.

    python3 stage3_annotate.py --in stage2.json --out stage3.json [--cache vep_cache.json]

Rules only, no gene names. A variant is kept when BOTH hold:
  * predicted impact is HIGH or MODERATE (VEP's own severity classes -- nonsense,
    frameshift, splice-disrupting, missense and similar; silent and intronic drop out)
  * it is RARE: maximum gnomAD exome/genome allele frequency < --max-af, where "absent
    from gnomAD" counts as 0

Then the biallelic test is re-applied to what survives, because a gene that looked
compound-heterozygous on raw coding calls usually stops looking that way once common
and silent variants are removed. That re-test is where most of the reduction happens.
"""
import argparse, json, pathlib, sys, time, urllib.error, urllib.request

URL = ("https://rest.ensembl.org/vep/human/region?"
       "af_gnomade=1&af_gnomadg=1&canonical=1&pick=1&numbers=0&domains=0")
BATCH = 200
KEEP_IMPACT = {"HIGH", "MODERATE"}


def vep(batch, tries=5):
    body = json.dumps({"variants": batch}).encode()
    for t in range(tries):
        try:
            req = urllib.request.Request(URL, data=body, headers={
                "Content-Type": "application/json", "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and t < tries - 1:
                time.sleep(2 ** t); continue
            raise
        except Exception:
            if t < tries - 1:
                time.sleep(2 ** t); continue
            raise
    return []


def max_gnomad_af(rec, alt):
    """Highest gnomAD AF across exome/genome for this alt allele; 0 if unseen."""
    best = 0.0
    for cv in rec.get("colocated_variants") or []:
        freqs = (cv.get("frequencies") or {})
        for allele, d in freqs.items():
            if alt and allele != alt.split(",")[0]:
                continue
            for k, val in d.items():
                if k.startswith("gnomad") and isinstance(val, (int, float)):
                    best = max(best, float(val))
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cache", default="vep_cache.json")
    ap.add_argument("--max-af", type=float, default=0.01)
    a = ap.parse_args()

    genes = json.loads(pathlib.Path(a.inp).read_text())
    uniq = {}
    for g, vs in genes.items():
        for x in vs:
            uniq[f"{x['chrom']} {x['pos']} . {x['ref']} {x['alt'].split(',')[0]} . . ."] = x
    keys = sorted(uniq)
    print(f"{len(genes):,} genes, {len(keys):,} unique coding variants to annotate", flush=True)

    cache_path = pathlib.Path(a.cache)
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    todo = [k for k in keys if k not in cache]
    print(f"{len(cache):,} cached, {len(todo):,} to fetch "
          f"({(len(todo)+BATCH-1)//BATCH} requests)", flush=True)

    for i in range(0, len(todo), BATCH):
        chunk = todo[i:i + BATCH]
        for rec in vep(chunk):
            cache[rec.get("input", "")] = {
                "csq": rec.get("most_severe_consequence"),
                "impact": ((rec.get("transcript_consequences") or [{}])[0]).get("impact"),
                "gene": ((rec.get("transcript_consequences") or [{}])[0]).get("gene_symbol"),
                "af": max_gnomad_af(rec, rec.get("allele_string", "").split("/")[-1]),
            }
        if (i // BATCH) % 10 == 0:
            cache_path.write_text(json.dumps(cache))
            print(f"  {min(i+BATCH, len(todo)):,}/{len(todo):,} annotated", flush=True)
        time.sleep(0.34)                      # be a good citizen on a public endpoint
    cache_path.write_text(json.dumps(cache))

    kept, dropped_impact, dropped_af, unannotated = {}, 0, 0, 0
    for g, vs in genes.items():
        keep = []
        for x in vs:
            k = f"{x['chrom']} {x['pos']} . {x['ref']} {x['alt'].split(',')[0]} . . ."
            ann = cache.get(k)
            if not ann:
                unannotated += 1; continue
            if ann.get("impact") not in KEEP_IMPACT:
                dropped_impact += 1; continue
            if (ann.get("af") or 0) >= a.max_af:
                dropped_af += 1; continue
            keep.append({**x, **ann})
        if keep:
            kept[g] = keep

    bi = {g: vs for g, vs in kept.items()
          if any(x["zyg"] == "hom" for x in vs)
          or sum(1 for x in vs if x["zyg"] == "het") >= 2}

    print(f"\ndropped: impact not HIGH/MODERATE {dropped_impact:,} | "
          f"gnomAD AF >= {a.max_af} {dropped_af:,} | unannotated {unannotated:,}")
    print(f"surviving variants {sum(len(v) for v in kept.values()):,} in {len(kept):,} genes")
    print(f"still biallelic-compatible: {sum(len(v) for v in bi.values()):,} variants "
          f"in {len(bi):,} genes")
    pathlib.Path(a.out).write_text(json.dumps(bi))
    print(f"-> {a.out}")


if __name__ == "__main__":
    main()
