#!/usr/bin/env python3
"""Extract a genomic window from a UCSC fixedStep wigFix.gz into bedGraph.

Kept outside the cloned repo deliberately; input path is taken as an argument.
bedGraph is 0-based half-open: chrom, start0, end0, value.
"""
import gzip, sys

src, chrom, lo, hi, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
pos = None          # 1-based position of the next value
cur_chrom = None
step = 1
n = 0
with gzip.open(src, "rt") as fh, open(out, "w") as w:
    for line in fh:
        if line.startswith("fixedStep"):
            kv = dict(p.split("=", 1) for p in line.split()[1:])
            cur_chrom = kv["chrom"]; pos = int(kv["start"]); step = int(kv.get("step", 1))
            continue
        if pos is None:
            continue
        if cur_chrom == chrom and lo <= pos <= hi:
            w.write(f"{chrom}\t{pos-1}\t{pos}\t{line.strip()}\n")
            n += 1
        elif cur_chrom == chrom and pos > hi:
            break
        pos += step
print(f"wrote {n:,} bedGraph rows for {chrom}:{lo:,}-{hi:,} -> {out}")
