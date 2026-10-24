"""The calibration, redone with a negative set that is not starved.

STABILITY-AXIS.md could only put four measured-reduced alleles against ONE allele
with measured-normal protein. Perfect separation with a single negative is p=0.20 --
not significant, and it was reported as such.

The variant atlas supplies what was missing: ClinVar/UniProt annotate benign and
likely-benign missense variants inside the pseudokinase domain, every one of which
already has a score in the saturation matrices. That turns n=1 into a real test.

These negatives are ANNOTATIONS, not measurements. That is weaker evidence per
variant than the functional westerns behind the four positives, and it is the main
caveat on everything below.

ONE annotation is overridden. ClinVar/UniProt call Q921H pathogenic, but Suijkerbuijk
2010 (PMC2887387) measured it directly -- "the Q921H mutation was indistinguishable
from wild-type LAP-BUBR1, both on protein level and functionality" -- and the same
sentence explains the annotation: Q921H was reported on ONE ALLELE together with
L844F, and the paper concludes "the L844F substitution is the likely cause of mitotic
defects in the patient". Q921H is the passenger. A direct measurement beats a database
assertion that is explainable as passenger mis-attribution, so it is scored benign.
"""
import csv, json, pathlib, statistics as st

ROOT = pathlib.Path(__file__).resolve().parents[5]
VAR = ROOT / "docs/mva/data/variants"
NS = ROOT / "docs/mva/data/neurosnap"
AA3 = {"Ala":"A","Arg":"R","Asn":"N","Asp":"D","Cys":"C","Gln":"Q","Glu":"E","Gly":"G",
       "His":"H","Ile":"I","Leu":"L","Lys":"K","Met":"M","Phe":"F","Pro":"P","Ser":"S",
       "Thr":"T","Trp":"W","Tyr":"Y","Val":"V"}


def parse(p):
    """p.Leu1012Pro -> (1012,'L','P'); returns None for anything else."""
    if not p or not p.startswith("p.") or len(p) < 8:
        return None
    body = p[2:]
    wt, mt = body[:3], body[-3:]
    if wt not in AA3 or mt not in AA3:
        return None
    try:
        return int(body[3:-3]), AA3[wt], AA3[mt]
    except ValueError:
        return None


def load_scores():
    mpnn, thermo = {}, {}
    for r in csv.DictReader(open(NS / "proteinmpnn_ddg_saturation.csv")):
        mpnn[(int(r["Position"]), r["Post"])] = float(r["ProteinMPNN-ddG Score"])
    for r in csv.DictReader(open(NS / "thermompnn_saturation.csv")):
        thermo[(int(r["Position"]), r["Mutant AA"])] = float(r["ddG (kcal/mol)"])
    return mpnn, thermo


def mannwhitney(pos, neg):
    """AUC plus a normal-approximation z (both groups are big enough here)."""
    wins = sum((a < b) + 0.5 * (a == b) for a in pos for b in neg)
    n1, n2 = len(pos), len(neg)
    auc = wins / (n1 * n2)
    mu = n1 * n2 / 2
    sd = (n1 * n2 * (n1 + n2 + 1) / 12) ** 0.5
    return auc, (wins - mu) / sd


def main():
    d = json.load(open(VAR / "ebi_proteins_O60566_variation.json"))
    d = d[0] if isinstance(d, list) else d
    mpnn, thermo = load_scores()

    pathogenic, benign = [], []
    for x in d["features"]:
        if not x["begin"].isdigit():
            continue
        p = int(x["begin"])
        if not (766 <= p <= 1050):
            continue
        if x.get("alternativeSequence") == "*" or x.get("consequenceType") != "missense":
            continue
        sigs = {c["type"] for c in x.get("clinicalSignificances", [])}
        prot = next((l["loc"] for l in x.get("locations", []) if l.get("loc", "").startswith("p.")), None)
        t = parse(prot)
        if not t:
            continue
        pos, wt, mt = t
        if (pos, mt) not in mpnn or (pos, mt) not in thermo:
            continue
        rec = (f"{wt}{pos}{mt}", mpnn[(pos, mt)], -thermo[(pos, mt)])  # both: lower = worse
        label = f"{wt}{pos}{mt}"
        if label == "Q921H":                      # measured WT-like; see module docstring
            benign.append(rec)
        elif sigs & {"Pathogenic", "Likely pathogenic"}:
            pathogenic.append(rec)
        elif sigs & {"Benign", "Likely benign"}:
            benign.append(rec)

    print(f"pseudokinase-domain missense with both a clinical label and a stability score")
    print(f"  pathogenic / likely pathogenic : {len(pathogenic)}")
    print(f"  benign / likely benign         : {len(benign)}\n")
    print("  pathogenic:", ", ".join(r[0] for r in sorted(pathogenic, key=lambda r: r[1])))
    print("  benign    :", ", ".join(r[0] for r in sorted(benign, key=lambda r: r[1])[:14]), "...\n")

    for i, name in ((1, "ProteinMPNN-ddG"), (2, "ThermoMPNN")):
        P = [r[i] for r in pathogenic]
        N = [r[i] for r in benign]
        auc, z = mannwhitney(P, N)
        print(f"{name:16s} AUC {auc:.3f}  z {z:+.2f}   "
              f"median pathogenic {st.median(P):+.2f} vs benign {st.median(N):+.2f}")

    print("\nfor comparison, the same test on the set STABILITY-AXIS.md had to use:")
    print("  4 measured-reduced against 1 measured-normal -> AUC 1.00, p = 0.20, not significant")


if __name__ == "__main__":
    main()
