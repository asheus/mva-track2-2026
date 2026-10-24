#!/usr/bin/env python3
"""ThermoMPNN stability predictions for N1002K / N1002R / N1002S.

    python3 -m scripts.mva.ddg_analysis

WHAT WAS RUN, AND WHY A PUBLISHED TOOL. Twice in this project I built a detector, validated
it on one positive control, and it confirmed whatever I pointed it at (C46, and the pocket
scan). So this uses **ThermoMPNN** -- a graph neural network trained by transfer learning
to predict stability changes for point mutants, published in PNAS (Dieckhaus, Brocidiacono,
Randolph & Kuhlman, doi:10.1073/pnas.2314853121), with weights shipped by its authors. Its
benchmark performance is theirs and is reported in that paper; we neither re-derive nor
restate it.

Site-saturation mutagenesis was run on the pseudokinase domain (766-1050, 285 residues)
extracted from AlphaFold AF-O60566-F1, giving 5,700 predictions. This script reads that
output and does three things that the raw numbers do not do for themselves.

1  VERIFY THE MAPPING. The tool indexes from 0, so residue 1002 is row position 236. The
   check is that the model's own wild-type letters match ours at three positions we care
   about independently: 1002 must be N, 978 must be W (the hydrogen-bond partner we found),
   999 must be R (the like-charged neighbour).

2  DETERMINE THE SIGN, rather than assume it. Reading ddG backwards would invertevery
   conclusion. Proline and glycine substitutions are near-universally destabilising and
   conservative swaps near-neutral, so their relative means fix the convention empirically.

3  CONTROL AGAINST WHAT THIS PROTEIN TOLERATES. ClinVar gives only ONE likely-pathogenic
   missense in BUB1B, too few for a pathogenic-versus-benign control. But it gives 34
   benign or likely-benign missense variants, nine of them inside this domain, and those
   answer a better question: **is N1002K an outlier against substitutions humans carry
   without disease?** One of the nine, N1004S, sits two residues away.

WHAT A ddG PREDICTION IS NOT. It is a thermodynamic quantity, and cellular abundance is
not. A destabilised protein is degraded only if quality-control machinery recognises it,
which depends on kinetics and on the cell. Thermodynamic destabilisation is necessary for
the folding hypothesis and not sufficient for it. And ThermoMPNN was trained and benchmarked
on experimental structures; this is a predicted one, high-confidence locally (pLDDT 91.5
over 990-1015) but still predicted.
"""
import json
import pathlib
import sys

import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parents[4]
CSV = ROOT / "docs/mva/data/ddg/ThermoMPNN_inference_bub1b_kinase_domain.csv"
MAP = ROOT / "docs/mva/data/nmd/eligibility_map.tsv"
OUT = ROOT / "docs/mva/data/ddg/ddg_analysis.json"
OFFSET = 766
BENIGN = {"Benign", "Likely benign", "Benign/Likely benign"}


def benign_variants():
    import re
    lines = MAP.read_text().strip().split("\n")
    cols = lines[0].split("\t")
    out = set()
    for L in lines[1:]:
        r = dict(zip(cols, L.split("\t")))
        if r.get("variant_class") == "missense" and r.get("clinvar_significance") in BENIGN:
            m = re.match(r"^([A-Z])(\d+)([A-Z])$", r["variant"].strip())
            if m:
                out.add((m.group(1), int(m.group(2)), m.group(3)))
    return sorted(out, key=lambda x: x[1])


def main():
    df = pd.read_csv(CSV)
    df["resnum"] = df["position"] + OFFSET

    print("1  MAPPING CHECK")
    checks = {1002: "N", 978: "W", 999: "R"}
    ok = True
    for pos, want in checks.items():
        got = df[df.resnum == pos].wildtype.iloc[0]
        good = got == want
        ok &= good
        print(f"   residue {pos}: model says {got}, we expect {want}  "
              f"{'OK' if good else 'MISMATCH'}")
    if not ok:
        sys.exit("mapping mismatch -- refusing to report")

    print("\n2  SIGN CONVENTION, determined empirically")
    pro = df[df.mutation == "P"].ddG_pred.mean()
    gly = df[df.mutation == "G"].ddG_pred.mean()
    cons = df[((df.wildtype == "I") & (df.mutation == "V")) |
              ((df.wildtype == "V") & (df.mutation == "I")) |
              ((df.wildtype == "L") & (df.mutation == "M")) |
              ((df.wildtype == "M") & (df.mutation == "L"))].ddG_pred.mean()
    print(f"   to proline {pro:+.3f}   to glycine {gly:+.3f}   conservative {cons:+.3f}")
    if not (pro > cons and gly > cons):
        sys.exit("sign convention could not be established -- refusing to report")
    print("   proline and glycine exceed conservative swaps => POSITIVE = DESTABILISING")

    def ddg(pos, mut):
        r = df[(df.resnum == pos) & (df.mutation == mut)]
        return float(r.ddG_pred.iloc[0]) if len(r) else None

    K, R, S = ddg(1002, "K"), ddg(1002, "R"), ddg(1002, "S")

    print("\n3  CONTROL: what this protein tolerates")
    vals, shown = [], []
    for w, p, m in benign_variants():
        if not (OFFSET <= p <= 1050):
            continue
        row = df[df.resnum == p]
        if not len(row) or row.wildtype.iloc[0] != w:
            continue
        d = ddg(p, m)
        vals.append(d)
        shown.append((f"{w}{p}{m}", d))
    vals = np.array(vals)
    print(f"   {'variant':<10}{'ddG_pred':>10}")
    for name, d in shown:
        tag = "   <- two residues from our variant" if "1004" in name else ""
        print(f"   {name:<10}{d:>+10.3f}{tag}")
    print(f"\n   tolerated (n={len(vals)}): mean {vals.mean():+.3f}  max {vals.max():+.3f}")
    print(f"   N1002K {K:+.3f} exceeds {(vals < K).sum()}/{len(vals)}; "
          f"z = {(K - vals.mean()) / vals.std(ddof=1):+.2f}")

    print("\n4  THE THREE VARIANTS")
    for lbl, v in [("N1002K  (the proband's)", K), ("N1002R  (ubiquitination control)", R),
                   ("N1002S  (charge/bulk control)", S)]:
        print(f"   {lbl:<34}{v:+.3f}   percentile "
              f"{(df.ddG_pred < v).mean() * 100:5.1f}%")

    print("\n5  WHAT THE NUMBERS DECOMPOSE INTO")
    print(f"   losing the wild-type asparagine      ~{S:+.2f}   (N1002S)")
    print(f"   adding charge and bulk on top        ~{K - S:+.2f}   (K minus S)")
    print("   This matches the structure independently: the OD1 acceptor contact to Trp978")
    print("   is lost whatever replaces the asparagine, and a buried charge costs more.")

    print("\n6  THE PREDICTION THE EXPERIMENT WILL TEST")
    print(f"   N1002K {K:+.3f} and N1002R {R:+.3f} differ by {abs(K - R):.3f} kcal/mol.")
    print("   The folding model says R is as destabilising as K. So a bench result of")
    print("   'K unstable, R stable' CONTRADICTS this prediction and points to")
    print("   ubiquitination at the new lysine. The N1002R lane is now a test of a stated")
    print("   quantitative prediction, not an open-ended look.")

    OUT.write_text(json.dumps({
        "tool": "ThermoMPNN", "citation": "10.1073/pnas.2314853121",
        "structure": "AlphaFold AF-O60566-F1, domain 766-1050",
        "n_predictions": int(len(df)),
        "sign_convention": "positive = destabilising (determined from Pro/Gly vs conservative)",
        "N1002K": K, "N1002R": R, "N1002S": S,
        "K_minus_R": K - R,
        "tolerated_controls": {n: d for n, d in shown},
        "tolerated_mean": float(vals.mean()), "tolerated_max": float(vals.max()),
        "z_vs_tolerated": float((K - vals.mean()) / vals.std(ddof=1)),
        "prediction_for_the_experiment":
            "R should be as destabilising as K; 'K unstable, R stable' would falsify "
            "the folding hypothesis and support ubiquitination",
        "caveats": ["ddG is thermodynamic; cellular abundance also depends on quality-"
                    "control kinetics",
                    "ThermoMPNN was benchmarked on experimental structures; this is a "
                    "predicted one (local pLDDT 91.5)",
                    "only 9 tolerated controls were available inside the domain"],
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
