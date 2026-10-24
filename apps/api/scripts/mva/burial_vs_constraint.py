"""Does burial predict constraint across the BUB1B pseudokinase domain?

The intuition that a buried residue is 'protected' and therefore tolerant of change is
exactly backwards for protein structure. This measures the real relationship across all
285 residues of the pseudokinase domain, rather than asserting it.

RSA by Shrake-Rupley on AlphaFold AF-O60566-F1 (numpy), probe 1.4 A, 960 sphere points,
Tien 2013 theoretical max-ASA. Constraint from GPN-Star m447 and AlphaMissense, averaged
over every possible substitution at each residue.
"""
import json, math, statistics, sys, csv, urllib.request
import numpy as np
sys.path.insert(0, __import__("pathlib").Path(__file__).resolve().parent.as_posix())
from neighbourhood_structure import fetch, MAXASA, THREE, VDW

KINASE = range(766, 1051)


def rsa_all(atoms, n=960):
    xyz = np.array([[a["x"], a["y"], a["z"]] for a in atoms])
    rad = np.array([VDW.get(a["el"], 1.7) for a in atoms]) + 1.4
    seq = np.array([a["seq"] for a in atoms])
    k = np.arange(n); off = 2.0/n; inc = math.pi*(3-math.sqrt(5))
    y = k*off - 1 + off/2; r = np.sqrt(np.maximum(0, 1-y*y)); phi = k*inc
    S = np.stack([np.cos(phi)*r, y, np.sin(phi)*r], axis=1)
    area = {}
    for i in range(len(atoms)):
        d = np.linalg.norm(xyz - xyz[i], axis=1)
        nb = np.where((d < rad[i] + rad.max()) & (d > 0))[0]
        pts = xyz[i] + rad[i]*S
        dd = np.linalg.norm(pts[:, None, :] - xyz[nb][None, :, :], axis=2)
        acc = np.sum(~np.any(dd < rad[nb][None, :], axis=1))
        area[seq[i]] = area.get(seq[i], 0.0) + 4*math.pi*rad[i]**2*acc/n
    return area


def main():
    atoms = fetch()
    seqres = {}
    for a in atoms: seqres.setdefault(a["seq"], THREE.get(a["res"], "X"))
    area = rsa_all(atoms)
    rsa = {r: 100*area[r]/MAXASA.get(seqres[r], 200) for r in area}

    # mean predicted impact per residue, over all substitutions
    lines = urllib.request.urlopen(
        "https://alphafold.ebi.ac.uk/files/AF-O60566-F1-aa-substitutions.csv").read().decode().splitlines()
    am = {}
    for r in csv.DictReader(lines):
        p = int(r["protein_variant"][1:-1])
        am.setdefault(p, []).append(float(r["am_pathogenicity"]))
    gpn = {}
    for p, rf, al, l in json.load(open("docs/mva/data/gpn_m447_coding.json")):
        gpn.setdefault(p, []).append(l)
    cds = sorted(json.load(open("docs/mva/data/cds_exons.json")))
    # genomic -> protein residue
    c = 0; g2p = {}
    for a, b in cds:
        for g in range(a, b+1):
            c += 1; g2p[g] = (c+2)//3
    gpn_res = {}
    for p, rf, al, l in json.load(open("docs/mva/data/gpn_m447_coding.json")):
        r = g2p.get(p)
        if r: gpn_res.setdefault(r, []).append(l)

    rows = [(r, rsa[r], statistics.mean(am[r]), statistics.mean(gpn_res[r]))
            for r in KINASE if r in rsa and r in am and r in gpn_res]

    print(f"Pseudokinase domain, {len(rows)} residues with all three measures\n")
    bands = [(0, 5, "core (0-5%)"), (5, 20, "buried (5-20%)"),
             (20, 40, "partial (20-40%)"), (40, 101, "exposed (>40%)")]
    print(f"  {'burial band':>18} {'n':>4} {'mean AlphaMissense':>20} {'mean GPN-Star LLR':>19}")
    print("  " + "-"*66)
    for lo, hi, lab in bands:
        sel = [x for x in rows if lo <= x[1] < hi]
        if not sel: continue
        print(f"  {lab:>18} {len(sel):4d} {statistics.mean(x[2] for x in sel):20.3f} "
              f"{statistics.mean(x[3] for x in sel):19.3f}")

    def spearman(a, b):
        ra = {v: i for i, v in enumerate(sorted(a))}
        rb = {v: i for i, v in enumerate(sorted(b))}
        A = [ra[x] for x in a]; B = [rb[x] for x in b]
        ma, mb = statistics.mean(A), statistics.mean(B)
        num = sum((x-ma)*(y-mb) for x, y in zip(A, B))
        den = math.sqrt(sum((x-ma)**2 for x in A)*sum((y-mb)**2 for y in B))
        return num/den
    R = [x[1] for x in rows]
    print(f"\n  Spearman, RSA vs mean AlphaMissense : {spearman(R,[x[2] for x in rows]):+.3f}"
          "   (negative = more buried, more damaging)")
    print(f"  Spearman, RSA vs mean GPN-Star LLR  : {spearman(R,[x[3] for x in rows]):+.3f}"
          "   (positive = more buried, more constrained)")

    print("\n  Our residues of interest:")
    for r in (1002, 1004, 1008, 1012, 999, 1005, 921, 909):
        if r in rsa:
            print(f"    {seqres[r]}{r:<5} RSA {rsa[r]:5.1f}%  "
                  f"mean AM {statistics.mean(am[r]):.3f}  "
                  f"mean GPN {statistics.mean(gpn_res.get(r,[0])):+.2f}")
    json.dump({str(r): rsa[r] for r in rsa}, open("docs/mva/data/rsa_all.json", "w"))


if __name__ == "__main__":
    main()
