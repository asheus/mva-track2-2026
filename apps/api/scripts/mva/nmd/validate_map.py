#!/usr/bin/env python3
"""Two external checks on the eligibility map, against labels we did not generate.

    python3 -m scripts.mva.nmd.validate_map

WHY THIS EXISTS. Every validation in this workstream so far tests whether an instrument
REPRODUCES something: the sentinel gate reproduces committed Pangolin scores, the
TrunKitten self-test reproduces a prediction the upstream pipeline already made, the
export audit reproduces a working tree. None of them tests whether the map's calls
PREDICT an independent label. Those are different questions and only the first was being
asked. Surfaced by running the be-ambitious skill on our own deliverable.

TEST 1 -- HELD-OUT POSITIVE CONTROLS.
ClinVar flags 13 BUB1B variants as canonical splice donor/acceptor. Four carry committed
reference scores and are used as sentinels inside the sweep, so they are not independent.
The other NINE are a held-out set with a known mechanism that nothing in this pipeline
has been tuned against. The classifier should call them splice-disrupting.
  PASS: >= 7 of 9 called.   FAIL: <= 5 called.  Between is inconclusive.

TEST 2 -- DOES THE MAP PREDICT PATHOGENICITY?
ClinVar clinical significance is an independent label. If the map carries signal, the
non-coding variants it calls (splice effect detected) should be enriched for
pathogenic/likely-pathogenic relative to those it does not call, among variants with a
definite ClinVar label.
  PASS: Fisher exact p < 0.01 with enrichment in the called group.
  FAIL: no enrichment -- the map has no signal and that is what gets reported.

Both tests read only files already on disk. Neither can be passed by tuning anything,
because the labels come from ClinVar and the mechanism assignments come from Pangolin.

A note on what a FAIL would mean, written before seeing the result so it cannot be
rationalised afterwards: ClinVar's non-coding entries are heavily weighted to VUS and
benign, and splice-disrupting variants that are also pathogenic are rare. A null result
here would most likely mean the test is underpowered rather than that the map is noise --
but distinguishing those two requires reporting the counts, not asserting the
distinction. So the counts are printed whatever happens.
"""
import pathlib
import sys

from scipy.stats import fisher_exact

ROOT = pathlib.Path(__file__).resolve().parents[5]
D = ROOT / "docs/mva/data/nmd"
MAP = D / "eligibility_map.tsv"
NC_VERIFIED = D / "clinvar_noncoding_verified.tsv"
ELIG = D / "noncoding_eligibility.tsv"

# The four variants used as in-sweep sentinels; excluded from the held-out set.
SENTINEL_POS = {40196779, 40200239, 40212488, 40206459}
PATH = ("pathogenic", "likely pathogenic")
BENIGN = ("benign", "likely benign")
CALLED = {"NULL_pending_NMD_of_new_PTC", "HYPOMORPH_protein_made"}
NOT_CALLED = {"NO_SPLICE_MECHANISM"}


def read_tsv(p):
    lines = p.read_text().strip().split("\n")
    cols = lines[0].split("\t")
    return [dict(zip(cols, L.split("\t"))) for L in lines[1:]]


def label(sig):
    s = (sig or "").strip().lower()
    if not s:
        return "none"
    # A record carrying both is conflicting; treat it as neither.
    has_p = any(k in s for k in PATH)
    has_b = any(k in s for k in BENIGN)
    if "conflicting" in s or (has_p and has_b):
        return "conflicting"
    if has_p:
        return "pathogenic"
    if has_b:
        return "benign"
    if "uncertain" in s:
        return "vus"
    return "other"


def main():
    for p in (MAP, NC_VERIFIED, ELIG):
        if not p.exists():
            sys.exit(f"missing {p}")

    verified = read_tsv(NC_VERIFIED)
    called_keys = {(r["chrom"], r["pos"], r["ref"], r["alt"])
                   for r in read_tsv(ELIG)}
    rows = read_tsv(MAP)
    # Every variant scored for a splice effect, whatever region it sits in.
    # Not "the non-coding set": 763 of these are exonic on the canonical
    # transcript and only 241 are intronic or at a canonical splice site (C37).
    nc = [r for r in rows if r["variant_class"].startswith("splice-scored")]
    scored = [r for r in nc if r["eligibility"] != "PENDING_not_yet_scored"]
    print(f"splice-scored rows: {len(nc)}   scored so far: {len(scored)}   "
          f"pending: {len(nc) - len(scored)}")
    if len(scored) < 50:
        print("\nToo little coverage to test yet; re-run when the sweep is further on.")
        return 0

    # ---------------- TEST 1: held-out canonical splice variants ----------------
    print("\n" + "=" * 70)
    print("TEST 1  held-out canonical splice variants (known mechanism)")
    print("=" * 70)
    canon = [r for r in verified if r["consequence"].startswith("splice_")]
    held = [r for r in canon if int(r["pos"]) not in SENTINEL_POS]
    print(f"{len(canon)} canonical splice variants; {len(canon) - len(held)} used as "
          f"sentinels; {len(held)} held out")
    hit, miss, pending = [], [], []
    for r in held:
        key = (r["chrom"], r["pos"], r["ref"], r["alt"])
        row = next((x for x in nc if x["variant"] in (r.get("hgvs_c"),
                    f"{r['chrom']}:{r['pos']}")), None)
        if row is not None and row["eligibility"] == "PENDING_not_yet_scored":
            pending.append(r)
        elif key in called_keys:
            hit.append(r)
        else:
            miss.append(r)
    for r in hit:
        print(f"  CALLED      {r.get('hgvs_c') or r['pos']:>16s}  {r['consequence']}")
    for r in miss:
        print(f"  NOT CALLED  {r.get('hgvs_c') or r['pos']:>16s}  {r['consequence']}")
    for r in pending:
        print(f"  pending     {r.get('hgvs_c') or r['pos']:>16s}  {r['consequence']}")
    testable = len(hit) + len(miss)
    if testable == 0:
        print("  none of the held-out set scored yet -- test cannot run")
    else:
        print(f"\n  {len(hit)}/{testable} held-out canonical splice variants called")
        verdict = ("PASS" if len(hit) >= 7 else
                   "FAIL" if len(hit) <= 5 else "INCONCLUSIVE")
        print(f"  verdict (threshold 7 pass / 5 fail of 9): {verdict}")
        if testable < 9:
            print(f"  NOTE: only {testable} of 9 scored so far, so the thresholds are "
                  f"not yet properly applicable")

    # ---------------- TEST 2: does the map predict pathogenicity? ----------------
    print("\n" + "=" * 70)
    print("TEST 2  does a splice call predict a pathogenic ClinVar label?")
    print("=" * 70)
    tab = {("called", "pathogenic"): 0, ("called", "benign"): 0,
           ("not", "pathogenic"): 0, ("not", "benign"): 0}
    dist = {}
    for r in scored:
        grp = ("called" if r["eligibility"] in CALLED
               else "not" if r["eligibility"] in NOT_CALLED else None)
        lab = label(r["clinvar_significance"])
        dist[(grp, lab)] = dist.get((grp, lab), 0) + 1
        if grp and lab in ("pathogenic", "benign"):
            tab[(grp, lab)] += 1
    print("\n  full label distribution (why the 2x2 is small):")
    for k in sorted(dist, key=lambda x: (str(x[0]), str(x[1]))):
        print(f"    {str(k[0]):10s} {k[1]:12s} {dist[k]}")
    a, b = tab[("called", "pathogenic")], tab[("called", "benign")]
    c, d = tab[("not", "pathogenic")], tab[("not", "benign")]
    print(f"\n              pathogenic  benign")
    print(f"  called      {a:10d}  {b:6d}")
    print(f"  not called  {c:10d}  {d:6d}")
    if min(a + b, c + d) == 0 or (a + c) == 0:
        print("\n  UNDERPOWERED: a margin is empty, so no test is possible. This is a")
        print("  statement about ClinVar's non-coding content, not about the map.")
    else:
        odds, p = fisher_exact([[a, b], [c, d]], alternative="greater")
        print(f"\n  Fisher exact (one-sided, enrichment in called): "
              f"OR={odds:.3g}  p={p:.4g}")
        verdict = "PASS" if p < 0.01 else "FAIL (no enrichment at p<0.01)"
        print(f"  verdict: {verdict}")
        if p >= 0.01 and (a + c) < 10:
            print("  CAVEAT: fewer than 10 pathogenic labels in total, so a null result")
            print("  here is weak evidence either way. Reported, not explained away.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
