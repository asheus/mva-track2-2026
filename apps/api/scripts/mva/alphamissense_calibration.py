"""Calibrate AlphaMissense against the measured BUB1B variants.

Ground truth is taken from the committed extraction (docs/mva/bub1b-dosage-review/
extracted_units.json, units D05 and D06), which traces to Suijkerbuijk 2010
(PMC2887387). Scores are the full AlphaMissense atlas for O60566, fetched from
the AlphaFold API.

The question is not "does AlphaMissense call MVA variants pathogenic" -- it is
whether AlphaMissense carries information about PROTEIN ABUNDANCE specifically,
which is the axis this child's case turns on.
"""
import csv, sys, urllib.request, statistics

AM_URL = "https://alphafold.ebi.ac.uk/files/AF-O60566-F1-aa-substitutions.csv"
KINASE = range(766, 1051)          # pseudokinase domain, Zhang 2026 map

# --- ground truth (docs/mva/bub1b-dosage-review/extracted_units.json) ---
DESTABILISED = {                    # D05: 5-10 fold decrease, fail to restore function
    "I909T": "MVA proband allele; 10-20% residual",
    "R814H": "MVA proband allele; 10-20% residual",
    "L1012P": "MVA proband allele; 10-20% residual",
    "L844F": "MVA proband allele; 10-20% residual",
    "R727C": "MVA proband allele; 10-20% residual",
}
NORMAL_ABUNDANCE = {                # D06: levels unchanged vs wild-type
    "Y155C": "TPR; separation-of-function, PATHOGENIC but stable",
    "R550Q": "fully functional",
    "Q921H": "IN kinase domain, indistinguishable from wild-type",
}
QUERY = {"N1002K": "the proband's allele 2 -- abundance unmeasured"}
OTHER = {
    "A739S": "monoallelic, recurrent pregnancy loss (PCS 8.93%)",
    "W722R": "monoallelic, recurrent pregnancy loss (PCS 13.79%)",
}


def load(path=None):
    lines = (open(path).read() if path else
             urllib.request.urlopen(AM_URL).read().decode()).splitlines()
    scores, by_pos = {}, {}
    for r in csv.DictReader(lines):
        v = r["protein_variant"]
        s = float(r["am_pathogenicity"])
        scores[v] = (s, r["am_class"])
        by_pos.setdefault(int(v[1:-1]), []).append(s)
    return scores, by_pos


def pct_rank(value, pool):
    return 100.0 * sum(1 for x in pool if x < value) / len(pool)


def main():
    scores, by_pos = load(sys.argv[1] if len(sys.argv) > 1 else None)

    kin = [s for p, ss in by_pos.items() if p in KINASE for s in ss]
    non = [s for p, ss in by_pos.items() if p not in KINASE for s in ss]

    print("=" * 74)
    print("POSITIONAL BASELINE -- is a high score in the kinase domain informative?")
    print("=" * 74)
    for nm, pool in (("pseudokinase 766-1050", kin), ("rest of protein", non)):
        hi = 100.0 * sum(1 for x in pool if x >= 0.564) / len(pool)
        print(f"  {nm:24s} n={len(pool):6d}  mean={statistics.mean(pool):.3f}"
              f"  median={statistics.median(pool):.3f}  {hi:5.1f}% called pathogenic")

    print()
    print("=" * 74)
    print("THE MEASURED VARIANTS")
    print("=" * 74)
    print(f"  {'variant':9s} {'AM':>6s} {'class':>6s} {'%ile in domain':>15s}   ground truth")
    print("  " + "-" * 70)

    groups = [("DESTABILISED (measured 10-20% residual)", DESTABILISED),
              ("NORMAL ABUNDANCE (measured unchanged)", NORMAL_ABUNDANCE),
              ("QUERY", QUERY),
              ("OTHER / monoallelic", OTHER)]
    got = {}
    for title, grp in groups:
        print(f"\n  -- {title}")
        for v, truth in grp.items():
            s, cls = scores[v]
            pos = int(v[1:-1])
            pool = kin if pos in KINASE else non
            got.setdefault(title, []).append(s)
            print(f"  {v:9s} {s:6.3f} {cls:>6s} {pct_rank(s,pool):14.1f}%   {truth}")

    print()
    print("=" * 74)
    print("VERDICT")
    print("=" * 74)
    d = got["DESTABILISED (measured 10-20% residual)"]
    n = got["NORMAL ABUNDANCE (measured unchanged)"]
    q = got["QUERY"][0]
    print(f"  destabilised      mean {statistics.mean(d):.3f}  range {min(d):.3f}-{max(d):.3f}")
    print(f"  normal abundance  mean {statistics.mean(n):.3f}  range {min(n):.3f}-{max(n):.3f}")
    print(f"  separation achieved: {'YES' if min(d) > max(n) else 'NO -- the classes OVERLAP'}")
    q921 = scores["Q921H"][0]
    print(f"\n  the decisive control -- Q921H (kinase domain, functionally NORMAL): {q921:.3f}")
    print(f"    scored below all 5 destabilised? {'YES' if q921 < min(d) else 'NO'}")
    print(f"\n  N1002K = {q:.3f}  -> sits {'INSIDE' if min(d) <= q <= max(d) else 'OUTSIDE'}"
          f" the measured-destabilised range")


if __name__ == "__main__":
    main()
