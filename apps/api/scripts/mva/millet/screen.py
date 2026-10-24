"""Step 3 of the Millet protocol: fragment-screen the allosteric site against decoys.

A raw docking score is close to meaningless on its own -- it tracks molecular size and
greasiness more than it tracks recognition, which is how the previous campaign ended up
reporting imatinib at -8.80 on a truncation artifact. So every fragment is docked at
the target site AND at four decoy boxes, and what is ranked is the DIFFERENCE.

The decoys are the protein's other real pockets, not random empty space, which makes
the test hard on purpose: the question is not "does this fragment stick to BubR1" but
"does it prefer THIS site to the others".

  ATP site      a genuine, functional pocket -- the hardest decoy
  scar          the face the 766-1050 truncation exposed; a known artifactual attractor
  C-term pocket LIGSITE cluster 3, a real but functionally uninteresting groove
  surface       a solvent-exposed patch with no pocket: the floor

Output: docs/mva/data/millet_screen.json
"""
import json, math, multiprocessing as mp, pathlib, sys, time

ROOT = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(pathlib.Path(__file__).parent))
NS, DATA = ROOT / "docs/mva/data/neurosnap", ROOT / "docs/mva/data"

TARGET = ("allosteric", (-41.850, -9.140, 4.710))
DECOYS = [("atp_site", (-23.599, -18.248, 3.350)),
          ("scar", None),                       # filled from structure below
          ("cterm_pocket", (-15.420, -2.660, -3.670)),
          ("surface", None)]
SCAR_RES = (824, 825, 826, 827, 828, 833, 835)
# Exposed residues with no pocket, >32 A from the target so the boxes cannot overlap,
# and clear of the scar (829 is adjacent to it and was rejected for that reason).
SURFACE_RES = (937, 938, 940)


def centroid(res, positions):
    pts = [a for p in positions for a in res[p]]
    return tuple(sum(q[i] for q in pts) / len(pts) for i in range(3))


def sites():
    res = {}
    for line in open(NS / "bubr1_pseudokinase_766_1050.pdb"):
        if line.startswith("ATOM"):
            res.setdefault(int(line[22:26]), []).append(
                (float(line[30:38]), float(line[38:46]), float(line[46:54])))
    out = [TARGET]
    for name, c in DECOYS:
        if name == "scar":
            c = centroid(res, SCAR_RES)
        elif name == "surface":
            c = centroid(res, SURFACE_RES)
        out.append((name, c))
    return out


_SITES = None


def _init():
    """Build every box's maps once per worker process."""
    global _SITES
    from dock import Site
    _SITES = [(name, Site(c)) for name, c in sites()]


def _one(job):
    from dock import ligand_pdbqt
    i, smiles = job
    pdbqt = ligand_pdbqt(smiles)          # embed once, dock the same conformer everywhere
    row = {"smiles": smiles}
    for name, site in _SITES:
        s, _ = site.dock(pdbqt=pdbqt) if pdbqt else (None, None)
        row[name] = s
    return i, row


def main(limit=None, procs=4):
    limit, procs = (int(limit) if limit else None), int(procs)
    lib = json.loads((DATA / "millet_fragments.json").read_text())
    if limit:
        lib = lib[:int(limit)]
    print(f"screening {len(lib)} fragments x {1 + len(DECOYS)} sites "
          f"= {len(lib) * (1 + len(DECOYS))} docks on {procs} processes")
    for n, c in sites():
        print(f"  {n:14s} {c[0]:8.2f} {c[1]:8.2f} {c[2]:8.2f}")

    # Checkpoint as we go. A 3,785-dock run is long enough that losing it to a killed
    # parent process -- which is exactly how the first attempt ended -- is worse than
    # the cost of rewriting a small JSON file every 25 fragments. A rerun resumes.
    ckpt = DATA / "millet_screen_partial.json"
    done = {}
    if ckpt.exists():
        done = {r["smiles"]: r for r in json.loads(ckpt.read_text())}
        print(f"resuming: {len(done)} fragments already scored", flush=True)

    t0 = time.time()
    rows = [done.get(f["smiles"]) for f in lib]
    todo = [(i, f["smiles"]) for i, f in enumerate(lib) if rows[i] is None]
    print(f"{len(todo)} fragments left to dock", flush=True)
    with mp.Pool(procs, initializer=_init) as pool:
        for k, (i, row) in enumerate(pool.imap_unordered(_one, todo, chunksize=2), 1):
            rows[i] = row
            if k % 25 == 0 or k == len(todo):
                ckpt.write_text(json.dumps([r for r in rows if r], indent=1))
                el = time.time() - t0
                print(f"  {k}/{len(todo)}  {el/60:.1f} min elapsed, "
                      f"{el/k*(len(todo)-k)/60:.1f} min left", flush=True)

    out = []
    for f, r in zip(lib, rows):
        if r is None or r["allosteric"] is None:
            continue
        decoys = [r[n] for n, _ in DECOYS if r.get(n) is not None]
        if not decoys:
            continue
        out.append({**f, "allosteric": r["allosteric"],
                    **{n: r[n] for n, _ in DECOYS},
                    "best_decoy": max(decoys),          # least negative = weakest decoy
                    "mean_decoy": sum(decoys) / len(decoys),
                    "selectivity": r["allosteric"] - min(decoys)})   # negative = prefers target
    (DATA / "millet_screen.json").write_text(json.dumps(out, indent=1))
    print(f"\n{len(out)} fragments scored -> {DATA / 'millet_screen.json'} "
          f"in {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    main(*sys.argv[1:])
