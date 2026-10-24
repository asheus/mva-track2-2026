"""Step 1 of the Millet protocol: pick the allosteric site to screen against.

Millet et al. rescued uroporphyrinogen III synthase by docking an ALLOSTERIC SURFACE
site, fragment-screening it, and then searching approved drugs for the best fragments.
This picks our equivalent site on the BubR1 pseudokinase domain.

THE CRITERION THAT IS NOT PROXIMITY TO THE MUTATION. A pharmacological chaperone
stabilises the fold by binding the NATIVE state; the shift in folding equilibrium is
RT*ln(1 + [L]/Kd) wherever the ligand binds, so long as it binds the folded state and
not the unfolded one. Tafamidis binds the transthyretin tetramer interface, nowhere
near most of the mutations it rescues. So we do NOT require the site to be near N1002,
and we record how far it is rather than selecting on it.

What we DO require, each one fixing a diagnosed failure of the previous docking run
(DOCKING-AUDIT.md) or a known weakness of this structure:

  OPEN      apo volume > 0. Vina holds the receptor rigid and cannot enter a pocket
            that is closed in the apo coordinates. This is why the ATP site -- apo
            volume 0 -- was unreachable, and it disqualifies every cryptic pocket.
  INTACT    far from residues the 766-1050 truncation exposed. Five drugs previously
            converged on that scar and took the whole top of the score distribution.
  REAL      high persistence, and reproduced by the OTHER sampling backend. SYNTHESIS
            records that the two backends disagree on the ATP pocket's geometry, so
            agreement is not assumed, it is tested.
  SILENT    not a functional site. An inhibitor is not a chaperone: the ATP pocket is
            intact here and must stay that way, and the C-terminal helix binds CENP-E.
  DRUGGABLE Lacuna's own score, used last because it is the softest of the five.
"""
import csv, math, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
NS = ROOT / "docs/mva/data/neurosnap"
DOMAIN = (766, 1050)

# The face the truncation exposed -- every residue occluded in full-length BubR1 by the
# 737-764 linker (dock_audit.py: 209 deleted contacts).
SCAR = (766, 794, 824, 825, 826, 827, 828, 833, 835)
# Functional sites inside this domain. Binding either of these makes an inhibitor.
ATP_SITE = (795, 880, 881, 882, 911, 912, 913)
CENPE_INTERFACE = tuple(range(1031, 1051))    # Legal 2020, Kd 318 nM


def coords(pdb):
    res = {}
    for line in open(pdb):
        if line.startswith("ATOM"):
            res.setdefault(int(line[22:26]), []).append(
                (float(line[30:38]), float(line[38:46]), float(line[46:54])))
    return res


def pockets(path):
    out = []
    for x in csv.DictReader(open(path)):
        out.append(dict(
            rank=int(x["Rank"]),
            c=(float(x["Centroid X (Å)"]), float(x["Centroid Y (Å)"]), float(x["Centroid Z (Å)"])),
            apo=float(x["Apo Volume (Å³)"]), maxv=float(x["Maximum Volume (Å³)"]),
            drug=float(x["Druggability"]), pers=float(x["Persistence"]),
            crypt=float(x["Crypticity"]),
            lining=[int("".join(ch for ch in r.split(":")[0] if ch.isdigit()))
                    for r in x["Lining Residues"].split("; ") if any(ch.isdigit() for ch in r)],
        ))
    return out


def dist_to(res, c, positions):
    return min((min(math.dist(a, c) for a in res[p]) for p in positions if p in res),
               default=float("inf"))


def same_site(a, b):
    """Do two pockets describe the same site?

    By shared LINING RESIDUES, not by centroid distance. SYNTHESIS records that the
    two sampling backends agree on which site carries cryptic volume and disagree on
    where its centroid is and how big it is -- so a centroid comparison would reject
    agreement that is really there. A residue set is what the backends actually agree
    on. Jaccard over the lining sets, >= 0.25 counts as the same site.
    """
    A, B = set(a["lining"]), set(b["lining"])
    return len(A & B) / len(A | B) if A | B else 0.0


def main():
    res = coords(NS / "bubr1_pseudokinase_766_1050.pdb")
    nma, omm = pockets(NS / "lacuna_pockets.csv"), pockets(NS / "lacuna_pockets_openmm_wt.csv")

    print("Candidate allosteric sites on the BubR1 pseudokinase domain")
    print("Functional-site and scar tests are by LINING-RESIDUE OVERLAP: a pocket is")
    print("the ATP site if ATP-site residues line it, not if its centroid is nearby.\n")
    print(f"{'src':>4s}{'rk':>3s} {'apoV':>5s} {'drug':>5s} {'pers':>5s} "
          f"{'xmeth':>5s} {'dN1002':>7s}  verdict")

    rows = []
    for src, table, other in (("nma", nma, omm), ("omm", omm, nma)):
        for p in table:
            lining = set(p["lining"])
            # best agreement with any pocket from the other sampling backend
            xmeth = max(same_site(p, q) for q in other)
            d_n = dist_to(res, p["c"], (1002,))

            fails = []
            if p["apo"] <= 0:                       fails.append("closed in apo")
            if lining & set(SCAR):                  fails.append("lines the truncation scar")
            if lining & set(ATP_SITE):              fails.append("lines the ATP site")
            if lining & set(CENPE_INTERFACE):       fails.append("lines the CENP-E interface")
            if xmeth < 0.25:                        fails.append("not reproduced x-method")
            if p["pers"] < 0.5:                     fails.append("low persistence")
            if p["drug"] < 0.7:                     fails.append("low druggability")

            verdict = "PASS" if not fails else "; ".join(fails)
            print(f"{src:>4s}{p['rank']:3d} {p['apo']:5.0f} {p['drug']:5.2f} {p['pers']:5.2f} "
                  f"{xmeth:5.2f} {d_n:7.1f}  {verdict}")
            if not fails:
                rows.append((src, p, xmeth, d_n))

    if not rows:
        sys.exit("\nNo site passes. Do not screen -- fix the criteria or the structure first.")

    rows.sort(key=lambda r: -(r[1]["drug"] * r[1]["pers"]))
    src, p, xmeth, d_n = rows[0]
    lining = sorted(set(p["lining"]))
    print(f"\nSELECTED: {src} pocket {p['rank']}  centre "
          f"{p['c'][0]:.3f}, {p['c'][1]:.3f}, {p['c'][2]:.3f}")
    print(f"  apo volume {p['apo']:.0f} A^3 (OPEN -- a rigid dock can enter it), "
          f"max {p['maxv']:.0f} A^3")
    print(f"  druggability {p['drug']:.2f}, persistence {p['pers']:.2f}, "
          f"crypticity {p['crypt']:.2f}")
    print(f"  lining-set agreement with the other backend: {xmeth:.2f} Jaccard")
    print(f"  {d_n:.0f} A from N1002 -- NOT a selection criterion, see module docstring")
    print(f"  lining residues: {', '.join(map(str, lining))}")
    (NS / "millet_site.txt").write_text(
        f"{p['c'][0]:.3f},{p['c'][1]:.3f},{p['c'][2]:.3f}\n"
        f"# {src} pocket {p['rank']}; lining {','.join(map(str, lining))}\n")
    print(f"\nwrote {NS / 'millet_site.txt'}")


if __name__ == "__main__":
    main()
