"""Why does N1002K look damaging when N1004S, two residues away, looks harmless?

Computes burial (relative solvent accessibility), local packing and pLDDT for the
1000-1015 neighbourhood from AlphaFold AF-O60566-F1 (v6), and lines each residue up
against what the predictors said.
"""
import math, urllib.request, json, os

PDB = "/tmp/bubr1.pdb"
# Tien 2013 theoretical max ASA
MAXASA = {"A":129,"R":274,"N":195,"D":193,"C":167,"E":223,"Q":225,"G":104,"H":224,
          "I":197,"L":201,"K":236,"M":224,"F":240,"P":159,"S":155,"T":172,"W":285,
          "Y":263,"V":174}
THREE = {"ALA":"A","ARG":"R","ASN":"N","ASP":"D","CYS":"C","GLU":"E","GLN":"Q",
         "GLY":"G","HIS":"H","ILE":"I","LEU":"L","LYS":"K","MET":"M","PHE":"F",
         "PRO":"P","SER":"S","THR":"T","TRP":"W","TYR":"Y","VAL":"V"}
VDW = {"C":1.70,"N":1.55,"O":1.52,"S":1.80}


def fetch():
    if not os.path.exists(PDB):
        url = json.load(urllib.request.urlopen(
            "https://alphafold.ebi.ac.uk/api/prediction/O60566"))[0]["pdbUrl"]
        open(PDB, "wb").write(urllib.request.urlopen(url).read())
    atoms = []
    for ln in open(PDB):
        if ln.startswith("ATOM"):
            atoms.append(dict(name=ln[12:16].strip(), res=ln[17:20].strip(),
                              seq=int(ln[22:26]), x=float(ln[30:38]),
                              y=float(ln[38:46]), z=float(ln[46:54]),
                              b=float(ln[60:66]), el=ln[76:78].strip() or ln[12:16].strip()[0]))
    return atoms


def sphere(n=200):
    pts, off, inc = [], 2.0/n, math.pi*(3-math.sqrt(5))
    for k in range(n):
        y = k*off - 1 + off/2
        r = math.sqrt(max(0.0, 1-y*y)); phi = k*inc
        pts.append((math.cos(phi)*r, y, math.sin(phi)*r))
    return pts


def sasa(atoms, probe=1.4, n=200):
    """Shrake-Rupley."""
    S = sphere(n)
    out = {}
    for i, a in enumerate(atoms):
        ra = VDW.get(a["el"], 1.7) + probe
        near = [b for j, b in enumerate(atoms) if j != i and
                (a["x"]-b["x"])**2+(a["y"]-b["y"])**2+(a["z"]-b["z"])**2 < (ra+2.0+probe)**2]
        acc = 0
        for sx, sy, sz in S:
            px, py, pz = a["x"]+ra*sx, a["y"]+ra*sy, a["z"]+ra*sz
            if not any((px-b["x"])**2+(py-b["y"])**2+(pz-b["z"])**2 <
                       (VDW.get(b["el"],1.7)+probe)**2 for b in near):
                acc += 1
        out.setdefault(a["seq"], 0.0)
        out[a["seq"]] += 4*math.pi*ra*ra*acc/n
    return out


def main():
    atoms = fetch()
    LO, HI = 990, 1020
    # Context must be SPATIAL, not sequence-based: a sequence window silently drops
    # packing partners that are distant in sequence but close in space (W973 for
    # N1002; the whole helix face for L1012), which inflates RSA and can turn a
    # buried residue into an apparently exposed one.
    core = [a for a in atoms if LO <= a["seq"] <= HI]
    sub = [b for b in atoms if any((b["x"]-a["x"])**2+(b["y"]-a["y"])**2
                                   +(b["z"]-a["z"])**2 < 20.0**2 for a in core)]
    area = sasa(sub)
    seqres = {}
    for a in atoms: seqres.setdefault(a["seq"], THREE.get(a["res"], "X"))
    plddt = {}
    for a in atoms: plddt.setdefault(a["seq"], []).append(a["b"])

    # heavy-atom contacts within 4.5 A, excluding i-1/i/i+1
    def contacts(r):
        mine = [a for a in atoms if a["seq"] == r]
        hits = set()
        for a in mine:
            for b in atoms:
                if abs(b["seq"]-r) <= 1: continue
                d2 = (a["x"]-b["x"])**2+(a["y"]-b["y"])**2+(a["z"]-b["z"])**2
                if d2 < 4.5**2: hits.add(b["seq"])
        return sorted(hits)

    AM = {999:0.112, 1002:0.923, 1004:0.048, 1005:0.152, 1012:0.872, 1008:None}
    GPN = {999:"40/55/47", 1002:"14/32/16", 1004:"99/97/99", 1005:"47/36/64",
           1012:"76/96/13", 1008:"—"}

    print(f"  {'res':>6} {'aa':>3} {'RSA':>7} {'buried?':>9} {'pLDDT':>6} "
          f"{'contacts':>9}  {'AM':>6}  {'GPN m/p/v':>12}")
    print("  " + "-"*78)
    for r in range(996, 1016):
        aa = seqres[r]
        rsa = 100*area[r]/MAXASA.get(aa, 200)
        c = contacts(r)
        tag = "BURIED" if rsa < 20 else "partial" if rsa < 40 else "exposed"
        am = f"{AM[r]:.3f}" if r in AM and AM[r] is not None else ""
        gp = GPN.get(r, "")
        star = " <<<" if r in (1002, 1004) else ""
        print(f"  {r:>6} {aa:>3} {rsa:6.1f}% {tag:>9} "
              f"{sum(plddt[r])/len(plddt[r]):6.1f} {len(c):9d}  {am:>6}  {gp:>12}{star}")

    print()
    for r in (1002, 1004):
        print(f"  residue {r} ({seqres[r]}) contacts: "
              + ", ".join(f"{seqres[x]}{x}" for x in contacts(r)))


if __name__ == "__main__":
    main()
