"""Rank BUB1B variants of uncertain significance by predicted destabilisation.

GATED ON burial_control.py. Nomination is only defensible where two things hold:

  1. ddG survives RSA-matched controls. It does, inside the pseudokinase domain:
     matched AUC 0.879-0.920, permutation p 0.0006-0.0052, stable across every
     matching window, with a logistic ddG slope of -2.53 against RSA's -0.22.
  2. The variant's mechanism is folding. It is not, outside that domain. Pathogenic
     missense in TPR and GLEBS score ddG AUC 0.364 -- WORSE THAN CHANCE -- because
     those are binding interfaces for KNL1 and BUB3 and the mechanism is lost
     interaction, not lost stability. T40M is pathogenic and predicted STABILISING.

So this ranks ONLY pseudokinase-domain missense VUS, and it is hypothesis-generating,
not a clinical call. It recapitulates Suijkerbuijk 2010's two-class model from
structure alone: "all MVA mutations fall in two distinct classes: those that impose
specific defects in checkpoint activity or microtubule attachment and those that lower
BUBR1 protein abundance."
"""
import csv, json, pathlib, statistics as st, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import bub1b

ROOT = pathlib.Path(__file__).resolve().parents[5]
VAR, NS = ROOT / "docs/mva/data/variants", ROOT / "docs/mva/data/neurosnap"
LO, HI, PLDDT_MIN = 766, 1050, 70.0


def main():
    plddt = {}
    for l in open(NS / "bubr1_fulllength.pdb"):
        if l.startswith("ATOM") and l[12:16].strip() == "CA":
            plddt[int(l[22:26])] = float(l[60:66])
    rsa = json.load(open(ROOT / "docs/mva/data/rsa_all.json"))
    rsa = {int(k): v for k, v in (rsa.get("rsa", rsa)).items()}
    mpnn = {(int(r["Position"]), r["Post"]): float(r["ProteinMPNN-ddG Score"])
            for r in csv.DictReader(open(NS / "proteinmpnn_ddg_fulllength.csv"))}
    thermo = {(int(r["Position"]), r["Mutant AA"]): float(r["ddG (kcal/mol)"])
              for r in csv.DictReader(open(NS / "thermompnn_fulllength.csv"))}

    kept, _, _ = bub1b.load()

    # the calibration anchors: what do KNOWN pathogenic folding-class alleles score?
    anchors = {"R814H": None, "L844F": None, "I909T": None, "Q950E": None, "L1012P": None}
    vus, ben = [], []
    for v in kept:
        if v["consequence"] != "missense": continue
        p, mt, nm = v["pos"], v["mt"], v["name"]
        if not (LO <= p <= HI) or plddt.get(p, 0) < PLDDT_MIN: continue
        if (p, mt) not in mpnn or (p, mt) not in thermo: continue
        if nm in anchors: anchors[nm] = (mpnn[(p, mt)], thermo[(p, mt)], rsa[p])
        lab = bub1b.label(v)
        if lab == "vus": vus.append((nm, p, mpnn[(p, mt)], thermo[(p, mt)], rsa[p]))
        elif lab == "benign": ben.append((mpnn[(p, mt)], thermo[(p, mt)]))

    print(f"pseudokinase-domain missense VUS with a reliable structure: {len(vus)}\n")
    print("calibration anchors (known pathogenic, folding class):")
    for k, v in anchors.items():
        if v: print(f"   {k:8s} MPNN {v[0]:6.2f}   Thermo {v[1]:+5.2f}   RSA {v[2]:5.1f}%")
    # Thresholds are set by SPECIFICITY against the known benign set, not by the
    # weakest pathogenic anchor. Anchoring on the weakest (Q950E, asserted by Ensembl
    # alone) nominated 36% of all VUS, which cannot be right -- most VUS are benign.
    def cuts(frac):
        bm = sorted(b[0] for b in ben); bt = sorted((b[1] for b in ben), reverse=True)
        k = max(0, int(len(ben) * frac) - 1)
        return bm[k], bt[k]

    print(f"\n   benign controls in this domain with scores: {len(ben)}")
    for frac, tier in ((0.04, "HIGH"), (0.12, "MODERATE")):
        cm, ct = cuts(frac)
        sel = [v for v in vus if v[2] <= cm and v[3] >= ct]
        fp = sum(1 for b in ben if b[0] <= cm and b[1] >= ct)
        print(f"\n== {tier} confidence: both methods beyond the {frac:.0%}-specificity cut "
              f"(MPNN {cm:.2f}, Thermo {ct:+.2f})")
        print(f"   known benign passing this bar: {fp}/{len(ben)} = {fp/len(ben):.0%} "
              f"(the empirical false-positive rate)")
        print(f"   VUS nominated: {len(sel)} of {len(vus)} ({len(sel)/len(vus):.0%})")
        print(f"   {'variant':9s} {'MPNN':>7s} {'Thermo':>7s} {'RSA%':>6s}")
        for nm, pp, m, t, r in sorted(sel, key=lambda v: v[2]):
            print(f"   {nm:9s} {m:7.2f} {t:+7.2f} {r:6.1f}")
        if tier == "HIGH": nom = sorted(sel, key=lambda v: v[2])
    if vus:
        print(f"\nfor contrast, the median VUS: MPNN {st.median([v[2] for v in vus]):.2f}, "
              f"Thermo {st.median([v[3] for v in vus]):+.2f}, RSA {st.median([v[4] for v in vus]):.1f}%")
    json.dump([{"variant": n, "pos": p, "proteinmpnn_ddg": m, "thermompnn_ddg": t, "rsa_pct": r}
               for n, p, m, t, r in nom], open(VAR / "vus_nominations.json", "w"), indent=1)


if __name__ == "__main__":
    main()
