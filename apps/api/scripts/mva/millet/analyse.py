"""Does anything actually prefer the allosteric site, or is this fragment stickiness?

With 757 fragments and five boxes, some fragment scores best at the target by chance.
Two tests separate a site effect from a ligand effect, and the second is the one that
matters.

SITE TEST. Compare the whole score distribution at each box. If the allosteric site's
distribution is not shifted relative to the decoys, the site is not unusually
attractive and no individual hit from it should be believed.

FRAGMENT TEST, with a null built the same way as the burial-matched control in
STABILITY-AXIS. For each fragment define

    delta = score(site) - mean(score at the other four boxes)

which cancels that fragment's intrinsic greasiness -- the confounder that let a blind
dock report imatinib at -8.80 on a truncation artifact. Then compute delta for the
DECOYS TOO, each in turn treated as if it were the target. Those decoy deltas are the
null: they are what "a fragment prefers this box" looks like at a box nobody cares
about. An allosteric delta is a hit only if it is an outlier against that null, and
the empirical false-positive rate is read off directly.
"""
import json, pathlib, statistics as st, sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
DATA = ROOT / "docs/mva/data"
SITES = ["allosteric", "atp_site", "scar", "cterm_pocket", "surface"]


def delta(row, site):
    """score at `site` minus the mean of the other four boxes.

    A natural objection: a decoy's "other four" contains the target, while the
    target's does not, so the comparison might be rigged against the target. It is
    not. With M the mean of all five boxes, s - mean(others) = 1.25 * (s - M) for
    every site -- a pure rescaling of symmetric centring, verified numerically to
    four decimals across all five boxes. Ranking and the empirical FPR are therefore
    identical under either formulation.
    """
    others = [row[s] for s in SITES if s != site and row.get(s) is not None]
    return row[site] - st.mean(others) if row.get(site) is not None and others else None


def main():
    rows = [r for r in json.loads((DATA / "millet_screen.json").read_text())
            if all(r.get(s) is not None for s in SITES)]
    print(f"{len(rows)} fragments scored at all five boxes\n")

    print("SITE TEST -- score distribution per box (kcal/mol, more negative = better)")
    print(f"{'box':14s} {'median':>7s} {'q1':>7s} {'q9':>7s} {'best':>7s}")
    for s in SITES:
        v = sorted(r[s] for r in rows)
        print(f"{s:14s} {st.median(v):7.2f} {v[len(v)//10]:7.2f} "
              f"{v[9*len(v)//10]:7.2f} {v[0]:7.2f}")

    print("\nFRAGMENT TEST -- delta = this box minus the mean of the other four")
    null = [d for s in SITES[1:] for r in rows if (d := delta(r, s)) is not None]
    tgt = [(delta(r, "allosteric"), r) for r in rows]
    tgt = [(d, r) for d, r in tgt if d is not None]
    null.sort()
    print(f"null (decoy deltas, n={len(null)}): median {st.median(null):+.2f}, "
          f"1st percentile {null[len(null)//100]:+.2f}, best {null[0]:+.2f}")
    ds = sorted(d for d, _ in tgt)
    print(f"allosteric deltas (n={len(ds)}): median {st.median(ds):+.2f}, "
          f"1st percentile {ds[len(ds)//100]:+.2f}, best {ds[0]:+.2f}")

    # Empirical FPR: fraction of NULL deltas at least this extreme.
    def fpr(d):
        return sum(1 for x in null if x <= d) / len(null)

    print(f"\n{'rank':>4s} {'allo':>6s} {'delta':>6s} {'FPR':>7s} {'par':>4s}  fragment")
    tgt.sort(key=lambda t: t[0])
    hits = []
    for i, (d, r) in enumerate(tgt[:15], 1):
        f = fpr(d)
        print(f"{i:4d} {r['allosteric']:6.2f} {d:+6.2f} {f:7.4f} {r['n_parents']:4d}  {r['smiles']}")
        hits.append({**r, "delta": d, "fpr": f})

    keep = [h for h in hits if h["fpr"] <= 0.01]
    print(f"\n{len(keep)} of the top 15 clear a 1% empirical false-positive rate")
    if not keep:
        print("NOTHING SURVIVES THE NULL. The site does not discriminate and no")
        print("fragment from this screen should be carried forward.")
    # This file is the statistics only. to_approved_drugs.py consumes it and writes
    # millet_hits.json; the two must not share an output path or whichever runs second
    # silently overwrites the other's work.
    (DATA / "millet_ranked.json").write_text(json.dumps(hits, indent=1))
    print(f"wrote {DATA / 'millet_ranked.json'}")


if __name__ == "__main__":
    main()
