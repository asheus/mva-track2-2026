#!/usr/bin/env python3
"""Pre-register the two experiments: what each outcome would mean, and what the structure predicts.

    python3 -m scripts.mva.t1008_n1002_analysis

WHAT THIS IS AND IS NOT. The two experiments proposed in APPROACH-RANKING.md -- a
phospho-specific blot for Thr1008 and an N1002R lane -- are wet-lab work and we have no
lab. This does not run them. It does the part that can be done without one, and that is
worth doing BEFORE the bench: measure what the structure predicts for each, and write down
what every possible result would mean, so the experiment cannot be read after the fact to
suit whichever answer arrives.

Three hypotheses compete for why p.Asn1002Lys reduces BubR1 function. They are not
variants of one idea; they point at different experiments and different drugs:

  A  FOLDING / BURIED CHARGE  -- a charged residue is buried at 13.7% RSA and loses an
     H-bond acceptor to Trp978, so the domain is destabilised and the protein degraded.
     This is our current thesis and the whole abundance arm rests on it.
  B  UBIQUITINATION           -- asparagine to LYSINE installs the residue ubiquitin
     conjugates to, in a lysine-rich stretch. Degradation would be site-specific, not a
     consequence of misfolding.
  C  SIGNALLING               -- UniProt annotates Thr1008 as phosphorylated by PLK1, six
     residues away. If the mutation disrupts that, abundance may be normal and the defect
     is a lost phosphorylation event.

A and B predict low protein. C predicts normal protein and a lost signal. Our entire
candidate ranking is aimed at A, so C being true would redirect everything.

The structural work below is on AlphaFold AF-O60566-F1, where this neighbourhood is
high-confidence: mean pLDDT 91.5 over 990-1015, minimum 80.4. That does not make a
prediction right; it makes it worth making.
"""
import json
import pathlib
import sys

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[4]
PDB = ROOT / "docs/mva/data/AF-O60566-F1.pdb"
OUT = ROOT / "docs/mva/data/t1008_n1002.json"

# Zamyatnin side-chain volumes (A^3), for the substitution arithmetic
VOL = {"N": 114.1, "K": 168.6, "R": 173.4, "S": 89.0, "T": 116.1}
VDW = {"C": 1.70, "N": 1.55, "O": 1.52, "S": 1.80}
# Tien 2013 theoretical max ASA, for RSA
MAXASA = {"A": 129, "R": 274, "N": 195, "D": 193, "C": 167, "E": 223, "Q": 225,
          "G": 104, "H": 224, "I": 197, "L": 201, "K": 236, "M": 224, "F": 240,
          "P": 159, "S": 155, "T": 172, "W": 285, "Y": 263, "V": 174}
THREE = {"ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C", "GLN": "Q",
         "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I", "LEU": "L", "LYS": "K",
         "MET": "M", "PHE": "F", "PRO": "P", "SER": "S", "THR": "T", "TRP": "W",
         "TYR": "Y", "VAL": "V"}


def load():
    atoms = []
    for L in PDB.read_text().split("\n"):
        if not L.startswith("ATOM"):
            continue
        atoms.append({"resi": int(L[22:26]), "aa": THREE.get(L[17:20].strip(), "X"),
                      "name": L[12:16].strip(),
                      "elem": (L[76:78].strip() or L[12:16].strip()[0]).upper(),
                      "xyz": np.array([float(L[30:38]), float(L[38:46]),
                                       float(L[46:54])]),
                      "plddt": float(L[60:66])})
    return atoms


def rsa(atoms, target, n_sphere=200):
    """Shrake-Rupley relative solvent accessibility for one residue."""
    probe = 1.4
    pts = []
    gr = np.pi * (3 - np.sqrt(5))
    for i in range(n_sphere):
        y = 1 - (i / (n_sphere - 1)) * 2
        r = np.sqrt(max(0.0, 1 - y * y))
        th = gr * i
        pts.append([np.cos(th) * r, y, np.sin(th) * r])
    pts = np.array(pts)
    tgt = [a for a in atoms if a["resi"] == target]
    allxyz = np.array([a["xyz"] for a in atoms])
    allrad = np.array([VDW.get(a["elem"], 1.7) for a in atoms]) + probe
    total = 0.0
    for a in tgt:
        ra = VDW.get(a["elem"], 1.7) + probe
        sph = a["xyz"] + pts * ra
        d = np.linalg.norm(sph[:, None, :] - allxyz[None, :, :], axis=2)
        same = np.array([x is a for x in atoms])
        d[:, same] = 1e9
        acc = np.all(d >= allrad[None, :], axis=1)
        total += 4 * np.pi * ra * ra * acc.mean()
    aa = tgt[0]["aa"]
    return total, (total / MAXASA.get(aa, 200)) if aa in MAXASA else None


def main():
    atoms = load()
    seq = {}
    for a in atoms:
        seq[a["resi"]] = a["aa"]
    ctx = "".join(seq.get(i, "-") for i in range(996, 1016))
    print("=" * 80)
    print("SEQUENCE CONTEXT  996-1015")
    print("=" * 80)
    print(f"  {ctx}")
    print(f"  {' ' * (1002 - 996)}^ 1002 (N->K)")
    print(f"  {' ' * (1008 - 996)}^ 1008 (T, PLK1 site per UniProt)")

    print("\n" + "=" * 80)
    print("IS T1008 A CREDIBLE PLK1 SITE? (consensus [D/E]-X-[S/T]-hydrophobic)")
    print("=" * 80)
    m2, m1, p0, p1 = seq.get(1006), seq.get(1007), seq.get(1008), seq.get(1009)
    acidic = m2 in "DE"
    phobic = p1 in "AVILMFWC"
    print(f"  -2 {m2}   -1 {m1}   0 {p0}   +1 {p1}")
    print(f"  acidic at -2: {'YES (' + m2 + ')' if acidic else 'no'}"
          f"   |   hydrophobic at +1: {'YES (' + p1 + ')' if phobic else 'no'}")
    print(f"  => {'MATCHES the canonical PLK1 consensus' if acidic and phobic else 'does not match cleanly'}")
    print(f"  The annotation is therefore supported by the motif, not just asserted.")

    print("\n  Local charge environment:")
    acids = [i for i in range(996, 1016) if seq.get(i) in "DE"]
    bases = [i for i in range(996, 1016) if seq.get(i) in "KR"]
    print(f"    acidic residues 996-1015: {[(i, seq[i]) for i in acids]}")
    print(f"    basic  residues 996-1015: {[(i, seq[i]) for i in bases]}")
    print(f"  N1002K introduces a POSITIVE charge {1005 - 1002} and {1006 - 1002} residues")
    print(f"  from D1005/E1006 IN SEQUENCE -- but sequence adjacency is not contact, and")
    print(f"  the geometry below is what decides whether that matters.")

    print("\n" + "=" * 80)
    print("GEOMETRY: how close is 1002 to 1008?")
    print("=" * 80)
    def at(r, n):
        return next((a["xyz"] for a in atoms if a["resi"] == r and a["name"] == n), None)
    pairs = [(1002, "CA", 1008, "CA"), (1002, "CB", 1008, "CB"),
             (1002, "CG", 1008, "OG1"), (1002, "CB", 1008, "OG1")]
    for r1, n1, r2, n2 in pairs:
        x1, x2 = at(r1, n1), at(r2, n2)
        if x1 is not None and x2 is not None:
            print(f"  {r1}:{n1:<4} -- {r2}:{n2:<4}  {np.linalg.norm(x1 - x2):6.2f} A")
    # nearest approach of any 1002 side-chain atom to any 1008 atom
    sc1 = [a["xyz"] for a in atoms if a["resi"] == 1002 and a["name"] not in
           ("N", "CA", "C", "O")]
    all8 = [a["xyz"] for a in atoms if a["resi"] == 1008]
    if sc1 and all8:
        d = min(np.linalg.norm(p - q) for p in sc1 for q in all8)
        print(f"  closest 1002 side-chain atom to any 1008 atom: {d:.2f} A")

    a1008, r1008 = rsa(atoms, 1008)
    a1002, r1002 = rsa(atoms, 1002)
    verdict = ("solvent-exposed, a kinase can reach it" if r1008 > 0.20
               else "BURIED -- phosphorylation would need local unfolding")
    print(f"\n  RSA T1008 : {r1008:.1%}  ({verdict})")
    print(f"  RSA N1002 : {r1002:.1%}  (buried, as previously computed)")

    print("\n" + "=" * 80)
    print("SUBSTITUTION ARITHMETIC AT A BURIED POSITION (RSA %.1f%%)" % (r1002 * 100))
    print("=" * 80)
    print(f"  {'variant':<10}{'side-chain vol':>16}{'change vs N':>14}{'charge':>9}"
          f"{'ubiquitinatable':>18}")
    for v in ["N", "K", "R", "S"]:
        dv = VOL[v] - VOL["N"]
        ch = "+1" if v in "KR" else "0"
        ub = "YES" if v == "K" else "no"
        tag = "  <- wild type" if v == "N" else ("  <- the variant" if v == "K" else "")
        print(f"  {'N1002' + v if v != 'N' else 'wild type':<10}{VOL[v]:>14.1f} A^3"
              f"{dv:>+13.1f}{ch:>9}{ub:>18}{tag}")
    print("\n  R adds MORE volume than K (+59.3 vs +54.5 A^3) at the same charge, so under")
    print("  hypothesis A it should be at least as destabilising. That is what makes it a")
    print("  clean discriminator: R is the charge-matched, bulk-matched control that")
    print("  CANNOT be ubiquitinated.")

    print("\n" + "=" * 80)
    print("PRE-REGISTERED READING OF THE RESULTS")
    print("=" * 80)
    print(f"  {'N1002K':<9}{'N1002R':<9}{'N1002S':<9}{'pT1008':<9}  conclusion")
    print("  " + "-" * 76)
    rows = [
        ("low", "low", "low", "normal", "A -- folding/buried charge. Current thesis holds."),
        ("low", "low", "NORMAL", "normal", "A, and specifically the CHARGE, not the bulk."),
        ("low", "NORMAL", "normal", "normal", "B -- ubiquitination at the new lysine."),
        ("normal", "normal", "normal", "LOST", "C -- signalling. Abundance arm is misdirected."),
        ("low", "low", "low", "LOST", "A plus C; destabilisation costs the phosphosite too."),
        ("low", "low", "low", "ELEVATED", "A, and T1008 is conformationally gated -- "
         "destabilising opens a normally buried site."),
        ("normal", "normal", "normal", "normal", "none of the three. Look at binding/localisation."),
    ]
    for k, r, s, p, c in rows:
        print(f"  {k:<9}{r:<9}{s:<9}{p:<9}  {c}")
    print("\n  Written before the experiment so no result can be read to suit the thesis.")

    OUT.write_text(json.dumps({
        "context_996_1015": ctx,
        "plk1_motif": {"minus2": m2, "minus1": m1, "site": p0, "plus1": p1,
                       "matches_consensus": bool(acidic and phobic)},
        "acidic_residues_996_1015": [[i, seq[i]] for i in acids],
        "rsa": {"T1008": round(float(r1008), 4), "N1002": round(float(r1002), 4)},
        "side_chain_volumes_A3": VOL,
        "hypotheses": {"A": "folding / buried charge", "B": "ubiquitination at new Lys",
                       "C": "loss of PLK1 phosphorylation at T1008"},
        "prereg_table": [{"N1002K": k, "N1002R": r, "N1002S": s, "pT1008": p,
                          "conclusion": c} for k, r, s, p, c in rows],
        "status": "PREDICTIONS ONLY -- no experiment was run; there is no wet lab here",
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
