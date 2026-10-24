"""Position -> gene lookup over the CDS index. Correct for overlapping genes.

Two traps, both of which bit a first draft of this pipeline and silently cost it the
right answer:

1. A position can lie in MORE THAN ONE gene. Readthrough transcripts overlap their
   parents exactly (BUB1B and BUB1B-PAK6 share a start coordinate), and returning the
   first match splits a gene's variants across two names -- so a gene carrying two
   heterozygous hits looks like two genes carrying one each, and any biallelic test
   fails. This returns ALL containing genes and the caller credits the variant to each.

2. Sorting by start is not enough to prune the backward scan. A long interval starting
   far upstream can still contain the query, so a fixed-width window misses it. We
   precompute a running maximum of end coordinates and walk back until that maximum
   drops below the query, which is exact.
"""
import bisect, gzip, json


class CdsIndex:
    def __init__(self, path):
        raw = json.load(gzip.open(path, "rt"))
        self.rows, self.starts, self.maxend = {}, {}, {}
        for chrom, rows in raw.items():
            rows.sort(key=lambda r: (r[0], r[1]))
            self.rows[chrom] = rows
            self.starts[chrom] = [r[0] for r in rows]
            m, run = [], 0
            for _, e, _ in rows:
                run = max(run, e)
                m.append(run)
            self.maxend[chrom] = m

    def genes_at(self, chrom, pos):
        rows = self.rows.get(chrom)
        if not rows:
            return set()
        hits, m = set(), self.maxend[chrom]
        i = bisect.bisect_right(self.starts[chrom], pos) - 1
        while i >= 0 and m[i] >= pos:
            s, e, g = rows[i]
            if s <= pos <= e:
                hits.add(g)
            i -= 1
        return hits

    @property
    def n_genes(self):
        return len({g for rows in self.rows.values() for _, _, g in rows})
