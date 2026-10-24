"""How reproducible is a single Vina score? The screen's statistic depends on it.

The screen ranks fragments on delta = score(site) - mean(score at four decoy boxes).
If re-running the SAME fragment at the SAME box with a different random seed moves the
score by as much as the between-box differences, then delta is measuring the random
number generator and the hit list is noise.

This docks a sample of the real library at the target box under several seeds and
compares the within-fragment seed spread against the between-box spread the screen
actually uses. The comparison, not either number alone, is the answer.
"""
import json, pathlib, statistics as st, sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
ROOT = pathlib.Path(__file__).resolve().parents[5]
DATA = ROOT / "docs/mva/data"
TARGET = (-41.848, -9.137, 4.710)
SEEDS = [1, 7, 42, 1234, 99991]
N_FRAG = 8


def main():
    from dock import Site, ligand_pdbqt
    lib = json.loads((DATA / "millet_fragments.json").read_text())
    sample = lib[:: max(1, len(lib) // N_FRAG)][:N_FRAG]

    sites = {s: Site(TARGET, seed=s) for s in SEEDS}
    print(f"{len(sample)} fragments x {len(SEEDS)} seeds at the target box\n")
    print(f"{'fragment':34s} {'mean':>6s} {'sd':>5s} {'range':>6s}")
    sds = []
    for f in sample:
        pdbqt = ligand_pdbqt(f["smiles"])
        if pdbqt is None:
            continue
        vals = []
        for s in SEEDS:
            sc, _ = sites[s].dock(pdbqt=pdbqt)
            if sc is not None:
                vals.append(sc)
        if len(vals) < 3:
            continue
        sd = st.stdev(vals)
        sds.append(sd)
        print(f"{f['smiles'][:34]:34s} {st.mean(vals):6.2f} {sd:5.2f} {max(vals)-min(vals):6.2f}")

    print(f"\nmedian within-fragment seed SD: {st.median(sds):.3f} kcal/mol")

    # The comparison that matters: how big are the between-box differences the screen
    # is trying to detect, measured on whatever the screen has scored so far?
    part = DATA / "millet_screen_partial.json"
    if part.exists():
        rows = json.loads(part.read_text())
        SITES = ["allosteric", "atp_site", "scar", "cterm_pocket", "surface"]
        deltas = []
        for r in rows:
            v = [r[s] for s in SITES if r.get(s) is not None]
            if len(v) == len(SITES):
                others = [r[s] for s in SITES[1:]]
                deltas.append(r["allosteric"] - st.mean(others))
        if deltas:
            deltas.sort()
            print(f"between-box delta on {len(deltas)} fragments scored so far: "
                  f"median {st.median(deltas):+.2f}, best {deltas[0]:+.2f}, "
                  f"spread(1st-99th) {deltas[len(deltas)//100]:+.2f} to {deltas[-1-len(deltas)//100]:+.2f}")
            ratio = abs(deltas[0]) / st.median(sds) if st.median(sds) else float("inf")
            print(f"\nthe best delta is {ratio:.1f}x the seed noise")
            print("A ratio near 1 means the hit list is the random number generator.")


if __name__ == "__main__":
    main()
