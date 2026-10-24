"""Did N1002K change the pocket landscape? Controls say no.

Lacuna's conformational sampling is driven by the input structure, so any mutation
reshuffles the ensemble. The only way to read a mutant run is against mutations known
to be harmless. N1004S is N1002's own neighbour and the 256th most tolerant of the
domain's 285 positions; Q921H is the one corpus allele with measured-normal protein.

It also compares normal-mode sampling against implicit-solvent MD on wild-type, which
is what decides whether the cryptic ATP-site pocket is real or a normal-mode artefact.
"""
import csv, math, pathlib

DATA = pathlib.Path(__file__).resolve().parents[5] / "docs/mva/data/neurosnap"


def load(name):
    return [dict(rank=int(x["Rank"]),
                 c=(float(x["Centroid X (Å)"]), float(x["Centroid Y (Å)"]), float(x["Centroid Z (Å)"])),
                 crypt=float(x["Crypticity"]), drug=float(x["Druggability"]),
                 pers=float(x["Persistence"]), apo=float(x["Apo Volume (Å³)"]),
                 maxv=float(x["Maximum Volume (Å³)"]))
            for x in csv.DictReader(open(DATA / name))]


def atoms():
    out = {}
    for l in open(DATA / "bubr1_pseudokinase_766_1050.pdb"):
        if l.startswith("ATOM"):
            out.setdefault(int(l[22:26]), []).append(
                (float(l[30:38]), float(l[38:46]), float(l[46:54])))
    return out


def main():
    A = atoms()
    near = lambda p, c: min(math.dist(a, c) for a in A[p])
    wt = load("lacuna_pockets_wt_nma.csv")
    atp = max(wt, key=lambda p: p["crypt"])      # the fully-cryptic ATP-site pocket

    print("Does N1002K change the pocket landscape? Same site, matched by centroid.\n")
    print(f"{'structure':16s} {'d(A)':>5s} {'crypt':>6s} {'drug':>6s} {'maxV':>6s} {'persist':>7s}   label")
    print(f"{'wild-type':16s} {'-':>5s} {atp['crypt']:6.2f} {atp['drug']:6.2f} "
          f"{atp['maxv']:6.0f} {atp['pers']:7.2f}   reference (raw AlphaFold)")
    for f, label in (("lacuna_pockets_n1002k_nma.csv", "PROBAND"),
                     ("lacuna_pockets_n1004s_nma.csv", "benign control"),
                     ("lacuna_pockets_q921h_nma.csv", "benign control")):
        M = load(f)
        m = min(M, key=lambda p: math.dist(atp["c"], p["c"]))
        name = f.split("_")[2].upper()
        print(f"{name:16s} {math.dist(atp['c'], m['c']):5.1f} {m['crypt']:6.2f} {m['drug']:6.2f} "
              f"{m['maxv']:6.0f} {m['pers']:7.2f}   {label}")
    print("\nThe two benign controls reproduce the proband's numbers exactly, so the shift\n"
          "from the wild-type reference is structure preparation -- every mutant was rebuilt\n"
          "by EvoEF2 while wild-type was the raw AlphaFold carve -- and not the mutation.\n")

    print("Normal modes versus implicit-solvent MD, both on wild-type:")
    om = load("lacuna_pockets_wt_openmm.csv")
    print(f"{'#':>2} {'crypt':>6} {'drug':>5} {'persist':>7} {'apoV':>5} {'maxV':>5} "
          f"{'dK795':>6} {'dD911':>6} {'dN1002':>7}")
    for p in om:
        print(f"{p['rank']:>2} {p['crypt']:6.2f} {p['drug']:5.2f} {p['pers']:7.2f} {p['apo']:5.0f} "
              f"{p['maxv']:5.0f} {near(795,p['c']):6.1f} {near(911,p['c']):6.1f} {near(1002,p['c']):7.1f}")
    closed = [p for p in om if p["apo"] == 0]
    atp_md = [p for p in om if near(911, p["c"]) < 5 and p["apo"] == 0]
    print(f"\nfully-closed (apo volume 0) pockets: {len(closed)} of {len(om)} under MD, "
          f"{len([p for p in wt if p['apo']==0])} of {len(wt)} under normal modes")
    print(f"fully-closed pockets within 5 A of D911 under MD: {[p['rank'] for p in atp_md]}")
    n = min(om, key=lambda p: near(1002, p["c"]))
    n_nma = min(wt, key=lambda p: near(1002, p["c"]))
    print(f"closest pocket to N1002: {near(1002,n['c']):.1f} A under MD (rank {n['rank']}, "
          f"crypt {n['crypt']:.2f}, drug {n['drug']:.2f}), "
          f"versus {near(1002,n_nma['c']):.1f} A under normal modes")


if __name__ == "__main__":
    main()
