#!/usr/bin/env python3
"""Extract several disjoint windows from a wigFix.gz into one bedGraph (single pass)."""
import gzip, sys
src, out = sys.argv[1], sys.argv[2]
# remaining args: chrom:lo-hi
iv = []
for a in sys.argv[3:]:
    c, rng = a.split(":"); lo, hi = rng.split("-"); iv.append((c, int(lo), int(hi)))
pos=None; cur=None; step=1; n=0
with gzip.open(src,"rt") as fh, open(out,"w") as w:
    for line in fh:
        if line.startswith("fixedStep"):
            kv=dict(p.split("=",1) for p in line.split()[1:])
            cur=kv["chrom"]; pos=int(kv["start"]); step=int(kv.get("step",1)); continue
        if pos is None: continue
        for c,lo,hi in iv:
            if cur==c and lo<=pos<=hi:
                w.write(f"{c}\t{pos-1}\t{pos}\t{line.strip()}\n"); n+=1
                break
        pos+=step
print(f"wrote {n:,} rows")
