"""Does ddG separate pathogenic from benign BEYOND what burial already explains?

ATLAS-AUDIT.md found that relative solvent accessibility alone separates the two
classes at AUC 0.875 against ddG's 0.963. Stability predictors read burial, so the
honest question is whether they add anything to it. This is the gate on any VUS
nomination: without it we would be ranking "buried residues" and calling it prediction.

Three independent framings, because with this few positives any single one is fragile:
  1. burial-MATCHED pairs   -- compare each pathogenic only against benign variants of
                               similar RSA, so burial cannot contribute to the contrast
  2. STRATIFIED AUC         -- buried and exposed strata scored separately
  3. LOGISTIC, ddG | RSA    -- is the ddG coefficient alive once RSA is in the model

Scores are whole-protein saturation scans, restricted to pLDDT >= 70 where the
AlphaFold model is reliable enough for a ddG to mean anything.
"""
import csv, json, math, pathlib, random, statistics as st, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import bub1b

ROOT = pathlib.Path(__file__).resolve().parents[5]
VAR, NS = ROOT / "docs/mva/data/variants", ROOT / "docs/mva/data/neurosnap"
PLDDT_MIN = 70.0
random.seed(42)


def load():
    plddt = {}
    for l in open(NS / "bubr1_fulllength.pdb"):
        if l.startswith("ATOM") and l[12:16].strip() == "CA":
            plddt[int(l[22:26])] = float(l[60:66])
    rsa = json.load(open(ROOT / "docs/mva/data/rsa_all.json"))
    rsa = {int(k): v for k, v in (rsa.get("rsa", rsa)).items()}
    mpnn = {(int(r["Position"]), r["Post"]): float(r["ProteinMPNN-ddG Score"])
            for r in csv.DictReader(open(NS / "proteinmpnn_ddg_fulllength.csv"))}
    thermo = {(int(r["Position"]), r["Mutant AA"]): -float(r["ddG (kcal/mol)"])   # flip: lower = worse
              for r in csv.DictReader(open(NS / "thermompnn_fulllength.csv"))}
    return plddt, rsa, mpnn, thermo


def labelled(plddt, rsa, mpnn, domains=None):
    """Sanitised corpus via bub1b.load(); the Q921H override lives in bub1b.label().

    `domains` restricts to one mechanism class. This is not a cosmetic filter: a
    ddG asks "does this substitution destabilise the fold", which is the wrong
    question for a variant whose defect is a lost partner contact. Pooling the two
    classes is what made every earlier whole-protein number look weak.
    """
    kept, _, _ = bub1b.load()
    P, B = [], []
    for v in kept:
        if v["consequence"] != "missense": continue
        pos, mt = v["pos"], v["mt"]
        if domains is not None and bub1b.domain(pos) not in domains: continue
        if plddt.get(pos, 0) < PLDDT_MIN or (pos, mt) not in mpnn: continue
        rec = (v["name"], pos, mt, rsa[pos])
        lab = bub1b.label(v)
        if lab == "pathogenic": P.append(rec)
        elif lab == "benign": B.append(rec)
    return P, B


def auc(pos, neg):
    if not pos or not neg: return float("nan")
    return sum((a < b) + 0.5 * (a == b) for a in pos for b in neg) / (len(pos) * len(neg))


def matched_auc(P, B, score, tol, n_perm=20000):
    """AUC over pairs matched on RSA, plus a permutation null that shuffles labels
    only WITHIN each matched set -- so the null preserves burial exactly."""
    pairs, wins = 0, 0.0
    sets = []
    for nm, pos, mt, r in P:
        pool = [b for b in B if abs(b[3] - r) <= tol]
        if not pool: continue
        sp = score[(pos, mt)]
        sb = [score[(q, m)] for _, q, m, _ in pool]
        wins += sum((sp < v) + 0.5 * (sp == v) for v in sb)
        pairs += len(sb)
        sets.append((sp, sb))
    if not pairs: return float("nan"), float("nan"), 0, 0
    obs = wins / pairs
    ge = 0
    for _ in range(n_perm):
        w = 0.0
        for sp, sb in sets:
            allv = [sp] + sb
            pick = random.randrange(len(allv))
            s2 = allv[pick]; rest = allv[:pick] + allv[pick+1:]
            w += sum((s2 < v) + 0.5 * (s2 == v) for v in rest)
        ge += (w / pairs >= obs)
    return obs, ge / n_perm, len(sets), pairs


def logistic(P, B, score):
    """label ~ RSA + ddG, standardised, plain gradient descent. Reports both slopes."""
    X = [(r, score[(p, m)], 1) for _, p, m, r in P] + [(r, score[(p, m)], 0) for _, p, m, r in B]
    rs = [x[0] for x in X]; ds = [x[1] for x in X]
    mr, sr = st.mean(rs), st.pstdev(rs) or 1
    md, sd = st.mean(ds), st.pstdev(ds) or 1
    X = [((r - mr) / sr, (d - md) / sd, y) for r, d, y in X]
    w = [0.0, 0.0, 0.0]
    for _ in range(40000):
        g = [0.0, 0.0, 0.0]
        for r, d, y in X:
            z = w[0] * r + w[1] * d + w[2]
            p = 1 / (1 + math.exp(-max(-30, min(30, z))))
            e = p - y
            g[0] += e * r; g[1] += e * d; g[2] += e
        for i in range(3): w[i] -= 0.02 * g[i] / len(X)
    return w  # [RSA slope, ddG slope, intercept]


def report(P, B, mpnn, thermo, title):
    print(f"{title}, pLDDT >= {PLDDT_MIN:.0f}: {len(P)} pathogenic, {len(B)} benign missense")
    print(f"  pathogenic median RSA {st.median([r for *_ , r in P]):5.1f}%")
    print(f"  benign     median RSA {st.median([r for *_ , r in B]):5.1f}%")
    print(f"  AUC of BURIAL alone (lower RSA = more pathogenic): "
          f"{auc([r for *_, r in P], [r for *_, r in B]):.3f}\n")

    for name, score in (("ProteinMPNN-ddG", mpnn), ("ThermoMPNN", thermo)):
        raw = auc([score[(p, m)] for _, p, m, _ in P], [score[(q, n)] for _, q, n, _ in B])
        print(f"{name}")
        print(f"  unmatched AUC                         {raw:.3f}")
        for tol in (5, 10, 15, 20):
            a, pv, ns, np_ = matched_auc(P, B, score, tol)
            if ns:
                print(f"  RSA-matched within +-{tol:2d}%   AUC {a:.3f}   "
                      f"permutation p = {pv:.4f}   ({ns} pathogenic matched, {np_} pairs)")
        w = logistic(P, B, score)
        print(f"  logistic label ~ RSA + ddG (standardised): "
              f"RSA slope {w[0]:+.2f}, ddG slope {w[1]:+.2f}")
        print(f"     -> ddG {'ADDS to' if abs(w[1]) > 0.35 else 'does NOT clearly add to'} burial\n")


def main():
    plddt, rsa, mpnn, thermo = load()

    # The pooled run first, because it is the one that looks like a null result and
    # is the reason to split at all.
    report(*labelled(plddt, rsa, mpnn), mpnn, thermo, "WHOLE PROTEIN (classes pooled)")
    print("=" * 72 + "\n")
    report(*labelled(plddt, rsa, mpnn, bub1b.FOLDED_DOMAINS), mpnn, thermo,
           "FOLDED CORE only (pseudokinase)")
    print("=" * 72 + "\n")
    P, B = labelled(plddt, rsa, mpnn, bub1b.INTERFACE_DOMAINS)
    if len(P) >= 2 and len(B) >= 2:
        report(P, B, mpnn, thermo, "BINDING INTERFACE only (TPR/KEN/GLEBS)")
    else:
        print(f"BINDING INTERFACE only: {len(P)} pathogenic, {len(B)} benign "
              f"-- too few to score; the class is characterised in ATLAS-AUDIT.md")


if __name__ == "__main__":
    main()
