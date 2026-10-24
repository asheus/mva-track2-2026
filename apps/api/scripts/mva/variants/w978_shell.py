"""Is W978L an independent prediction, or just a buried tryptophan?

VUS-NOMINATION.md highlighted W978L because W978 packs against N1002, the proband's
residue -- framing it as a second prediction falling out of the same structural
argument. That framing is only worth anything if the packing shell is doing work.

The sceptical alternative: big buried aromatics always score terribly on ddG, so W978L
would top any such list regardless of what it touches, and "packs against N1002" is
decoration.

Discriminating test: compare N1002's contact shell against BURIAL-MATCHED positions
elsewhere in the same domain. If the shell is no more intolerant than equally buried
residues, the shell framing adds nothing and must be dropped.
"""
import csv, json, math, pathlib, random, statistics as st

ROOT = pathlib.Path(__file__).resolve().parents[5]
NS = ROOT / "docs/mva/data/neurosnap"
random.seed(42)
TARGET, CUTOFF = 1002, 5.0          # heavy-atom contact distance, angstrom


def main():
    atoms, plddt = {}, {}
    for l in open(NS / "bubr1_fulllength.pdb"):
        if not l.startswith("ATOM"): continue
        p = int(l[22:26])
        atoms.setdefault(p, []).append((float(l[30:38]), float(l[38:46]), float(l[46:54])))
        if l[12:16].strip() == "CA": plddt[p] = float(l[60:66])
    rsa = json.load(open(ROOT / "docs/mva/data/rsa_all.json"))
    rsa = {int(k): v for k, v in (rsa.get("rsa", rsa)).items()}
    mpnn = {}
    for r in csv.DictReader(open(NS / "proteinmpnn_ddg_fulllength.csv")):
        mpnn.setdefault(int(r["Position"]), {})[r["Post"]] = float(r["ProteinMPNN-ddG Score"])
    seq = json.load(open(ROOT / "docs/mva/data/variants/ebi_proteins_O60566_variation.json"))
    seq = (seq[0] if isinstance(seq, list) else seq)["sequence"]

    # contact shell, computed from the structure rather than recalled
    shell = sorted(p for p in atoms if p != TARGET and
                   min(math.dist(a, b) for a in atoms[p] for b in atoms[TARGET]) <= CUTOFF)
    print(f"N1002 contact shell at {CUTOFF} A heavy-atom distance: "
          f"{', '.join(seq[p-1] + str(p) for p in shell)}\n")

    def intolerance(p):
        """mean ddG over all substitutions -- how badly the position tolerates change"""
        return st.mean([v for a, v in mpnn[p].items() if a != seq[p - 1]])

    dom = [p for p in range(766, 1051) if p in mpnn and plddt.get(p, 0) >= 70]
    print(f"{'position':10s} {'RSA%':>6s} {'mean ddG':>9s} {'rank/285':>9s}")
    for p in shell + [TARGET]:
        if p not in mpnn: continue
        order = sorted(dom, key=intolerance)
        tag = "  <- PROBAND" if p == TARGET else ("  <- W978" if p == 978 else "")
        print(f"{seq[p-1]+str(p):10s} {rsa[p]:6.1f} {intolerance(p):9.2f} "
              f"{order.index(p)+1 if p in order else '-':>9}{tag}")

    # the discriminating comparison
    shell_in = [p for p in shell if p in dom]
    print(f"\nburial-matched control: for each shell residue, 200 random domain positions")
    print(f"within +-3% RSA, asking how often the shell residue is MORE intolerant\n")
    wins, tot, details = 0, 0, []
    for p in shell_in:
        pool = [q for q in dom if q not in shell_in and q != TARGET and abs(rsa[q] - rsa[p]) <= 3]
        if len(pool) < 5: continue
        ip = intolerance(p)
        w = sum(1 for q in pool if ip < intolerance(q))
        details.append((seq[p-1]+str(p), w / len(pool), len(pool)))
        wins += w; tot += len(pool)
    for nm, frac, n in details:
        print(f"   {nm:8s} more intolerant than {frac:5.1%} of {n} burial-matched positions")
    print(f"\n   shell overall: {wins/tot:.1%} of burial-matched comparisons "
          f"(50% = the shell adds nothing beyond burial)")
    # sign test across shell residues
    above = sum(1 for _, f, _ in details if f > 0.5)
    print(f"   shell residues above their own burial-matched median: {above}/{len(details)}")


if __name__ == "__main__":
    main()
