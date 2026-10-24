"""Re-derive every number in docs/mva/STABILITY-AXIS.md from the committed CSVs.

Three independent stability predictors over the BubR1 pseudokinase domain, scored
against the corpus variants whose protein levels were actually measured.

Sign conventions are established empirically rather than assumed -- the three
methods do not agree on direction, and getting one backwards inverts the result:
  ProteinMPNN-ddG  negative = destabilising  (wild-type -> wild-type is exactly 0)
  ThermoMPNN       positive = destabilising  (kcal/mol; service doc: <= -0.5 stabilising)
  EvoEF2           positive = destabilising  (mutant total energy minus wild-type)
Every score below is re-oriented to "lower = more destabilising" before use.
"""
import csv, json, bisect, itertools, statistics as st, pathlib

DATA = pathlib.Path(__file__).resolve().parents[5] / "docs/mva/data/neurosnap"

# Corpus missense variants inside the pseudokinase domain, from docs/mva/VARIANT-TABLE.md.
MEASURED_REDUCED = ["R814H", "L844F", "I909T", "L1012P"]   # protein 5-10x reduced
MEASURED_NORMAL  = ["Q921H"]                               # indistinguishable from wild-type
INFERRED_BENIGN  = ["R893S", "R999Q", "N1004S", "D1005E"]  # not measured -- see caveats
PROBAND          = "N1002K"
ALPHAMISSENSE = {"R770Q": 0.068, "R814H": 0.221, "L844F": 0.292, "R893S": 0.579,
                 "I909T": 0.451, "Q921H": 0.491, "R999Q": 0.112, "N1002K": 0.923,
                 "N1004S": 0.048, "D1005E": 0.152, "L1012P": 0.872}
CORPUS = list(ALPHAMISSENSE)


def load():
    mpnn, thermo, evoef = {}, {}, {}
    wt_self = []
    synonymous = set()
    for r in csv.DictReader(open(DATA / "proteinmpnn_ddg_saturation.csv")):
        v = float(r["ProteinMPNN-ddG Score"])
        mpnn[(int(r["Position"]), r["Post"])] = v
        if r["Pre"] == r["Post"]:
            wt_self.append(v)
            synonymous.add((int(r["Position"]), r["Post"]))
    # the empirical check that fixes the sign convention
    assert wt_self and max(abs(x) for x in wt_self) < 1e-9, "wild-type self-score is not zero"
    for r in csv.DictReader(open(DATA / "thermompnn_saturation.csv")):
        thermo[(int(r["Position"]), r["Mutant AA"])] = float(r["ddG (kcal/mol)"])
    for r in csv.DictReader(open(DATA / "evoef2_corpus_ddg.csv")):
        m = r["mutant_definition"]                    # e.g. "NA1002K"
        evoef[m[0] + m[2:]] = float(r["delta_score_total"])
    return mpnn, thermo, evoef, len(wt_self), synonymous


def at(table, v):
    return table[(int(v[1:-1]), v[-1])]


def auc_exact(pos, neg, score):
    """AUC plus an exact one-sided permutation p. score: lower = more destabilising."""
    wins = sum((score[a] < score[b]) + 0.5 * (score[a] == score[b]) for a in pos for b in neg)
    vals = [score[v] for v in pos + neg]
    tot = ge = 0
    for c in itertools.combinations(range(len(vals)), len(pos)):
        P = [vals[i] for i in c]
        N = [vals[i] for i in range(len(vals)) if i not in c]
        w = sum((a < b) + 0.5 * (a == b) for a in P for b in N)
        tot += 1
        ge += (w >= wins)
    return wins / (len(pos) * len(neg)), ge / tot


def spearman(a, b):
    ra = {v: i for i, v in enumerate(sorted(a, key=a.get))}
    rb = {v: i for i, v in enumerate(sorted(b, key=b.get))}
    xs = [ra[v] for v in a]; ys = [rb[v] for v in a]
    mx, my = st.mean(xs), st.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = (sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)) ** 0.5
    return num / den


def main():
    mpnn, thermo, evoef, n_wt, synonymous = load()
    print(f"wild-type self-score is 0.0 at all {n_wt} positions -- sign convention confirmed\n")

    # all three oriented so that lower = more destabilising
    S = {"ProteinMPNN-ddG": {v: at(mpnn, v) for v in CORPUS},
         "ThermoMPNN":      {v: -at(thermo, v) for v in CORPUS},
         "EvoEF2":          {v: -evoef[v] for v in CORPUS}}

    note = {**{v: "MEASURED 5-10x reduced" for v in MEASURED_REDUCED},
            "Q921H": "MEASURED normal", "N1002K": "*** PROBAND ***",
            "R770Q": "architectural match", "R893S": "in unaffected father",
            "R999Q": "neighbour", "N1004S": "neighbour", "D1005E": "neighbour"}
    print(f"{'variant':9s} {'MPNN':>7s} {'Thermo':>7s} {'EvoEF2':>9s} {'AM':>6s}   note")
    print("-" * 78)
    for v in sorted(CORPUS, key=lambda x: S["ProteinMPNN-ddG"][x]):
        print(f"{v:9s} {at(mpnn,v):7.2f} {at(thermo,v):7.2f} {evoef[v]:9.2f} "
              f"{ALPHAMISSENSE[v]:6.3f}   {note[v]}")

    print("\nCalibration against measured protein levels (exact one-sided permutation p):")
    print(f"{'method':18s} {'strict AUC':>11s} {'p':>8s}   {'wide AUC':>9s} {'p':>8s}")
    scores = dict(S)
    scores["AlphaMissense"] = {v: -ALPHAMISSENSE[v] for v in CORPUS}
    for name, sc in scores.items():
        a1, p1 = auc_exact(MEASURED_REDUCED, MEASURED_NORMAL, sc)
        a2, p2 = auc_exact(MEASURED_REDUCED, MEASURED_NORMAL + INFERRED_BENIGN, sc)
        print(f"{name:18s} {a1:11.2f} {p1:8.4f}   {a2:9.2f} {p2:8.4f}")

    print("\nAgreement between the three methods (Spearman over the 11 corpus variants):")
    for a, b in itertools.combinations(S, 2):
        print(f"  {a:16s} vs {b:16s} {spearman(S[a], S[b]):.3f}")

    print(f"\n{PROBAND} in the context of every substitution in the domain:")
    for name, table, worse_is in (("ProteinMPNN-ddG", mpnn, "lower"), ("ThermoMPNN", thermo, "higher")):
        # ProteinMPNN's grid includes wild-type self-scores; ThermoMPNN's does not.
        # Drop them by identity, not by value, so both denominators are 5,415 real
        # substitutions and a genuine prediction of exactly 0.00 is not discarded.
        vals = sorted(v for k, v in table.items() if k not in synonymous)
        v = at(table, PROBAND)
        p = 100 * bisect.bisect_left(vals, v) / len(vals)
        p = p if worse_is == "lower" else 100 - p
        rank = sorted(CORPUS, key=lambda x: S[name][x]).index(PROBAND) + 1
        print(f"  {name:16s} {v:7.2f}  more destabilising than {100-p:5.1f}% of {len(vals)} substitutions"
              f"  | rank {rank}/11 in corpus")

    # positional intolerance: is it the site, or the lysine?
    print("\nPer-position mean ProteinMPNN-ddG (is the site fragile, or is lysine the problem?):")
    permut = {p: st.mean([mpnn[(p, a)] for a in "ACDEFGHIKLMNPQRSTVWY" if mpnn[(p, a)] != 0.0])
              for p in range(766, 1051)}
    order = sorted(permut, key=permut.get)
    for p, label in ((1002, "N1002 proband"), (1012, "L1012 analogue"),
                     (921, "Q921 measured-normal"), (1004, "N1004 benign neighbour")):
        print(f"  {label:24s} mean {permut[p]:6.2f}  rank {order.index(p)+1:3d} of 285 most intolerant")
    at1002 = sorted((mpnn[(1002, a)], a) for a in "ACDEFGHIKLMNPQRSTVWY" if a != "N")
    print("  worst substitutions at 1002: " + ", ".join(f"{a} {d:.1f}" for d, a in at1002[:6]))
    print(f"  lysine ranks {[a for d,a in at1002].index('K')+1} of 19 at position 1002")


if __name__ == "__main__":
    main()
