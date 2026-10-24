"""An apo-surface pocket detector, independent of Lacuna.

WHY A SECOND INSTRUMENT. Lacuna is a CRYPTIC pocket finder: it samples conformers and
ranks sites by how much they open under motion. That is the wrong bias for the Millet
protocol, which needs a pocket that is ALREADY OPEN in the apo structure -- a rigid
dock cannot enter anything else. Lacuna's top-10 is also a top-10, so an ordinary open
groove can be ranked out by ten cryptic ones. This measures the static surface instead
and is free of that bias.

METHOD. LIGSITE (Hendlich, Rippmann & Barnickel, J Mol Graph Model 1997): grid the
protein, and for each empty grid point scan the three axes and four cube diagonals,
counting protein-solvent-protein (PSP) events -- directions where protein is hit going
both ways. A point enclosed on many axes is inside a concavity. Points above a PSP
threshold are clustered by contiguity and each cluster is one pocket.

The two instruments answer to different failure modes and are meant to disagree.
"""
import math, pathlib, sys
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[5]
NS = ROOT / "docs/mva/data/neurosnap"

SPACING = 1.0        # grid, A
VDW = 1.8            # uniform heavy-atom radius, A -- LIGSITE uses a single radius
PROBE = 1.4          # water
MIN_PSP = 5          # of 7 scan directions; 5 is LIGSITE's default, 6 is stricter
MIN_POINTS = 40      # >= 40 A^3, below which a "pocket" is a surface dimple

# Same exclusions as select_site.py, applied to this instrument's output too.
SCAR = (766, 794, 824, 825, 826, 827, 828, 833, 835)
ATP_SITE = (795, 880, 881, 882, 911, 912, 913)
CENPE_INTERFACE = tuple(range(1031, 1051))


def load(pdb):
    xyz, resid = [], []
    for line in open(pdb):
        if line.startswith("ATOM") and line[76:78].strip() != "H":
            xyz.append((float(line[30:38]), float(line[38:46]), float(line[46:54])))
            resid.append(int(line[22:26]))
    return np.array(xyz), np.array(resid)


def psp_grid(xyz):
    """Occupancy grid, then PSP counts on the free points."""
    lo, hi = xyz.min(0) - 5.0, xyz.max(0) + 5.0
    shape = np.ceil((hi - lo) / SPACING).astype(int) + 1
    occ = np.zeros(shape, bool)
    r = VDW + PROBE
    span = int(math.ceil(r / SPACING))
    off = np.arange(-span, span + 1) * SPACING
    dx, dy, dz = np.meshgrid(off, off, off, indexing="ij")
    ball = (dx**2 + dy**2 + dz**2) <= r**2
    for p in xyz:                                   # stamp each atom's ball
        i = np.round((p - lo) / SPACING).astype(int)
        s = tuple(slice(max(0, i[k] - span), min(shape[k], i[k] + span + 1)) for k in range(3))
        b = tuple(slice(max(0, span - i[k]),
                        ball.shape[k] - max(0, i[k] + span + 1 - shape[k])) for k in range(3))
        occ[s] |= ball[b]

    # Seven scan directions: 3 axes + 4 body diagonals.
    dirs = [(1,0,0),(0,1,0),(0,0,1),(1,1,1),(1,1,-1),(1,-1,1),(1,-1,-1)]
    psp = np.zeros(shape, np.int8)
    for d in dirs:
        fwd = _hits_along(occ, d)
        bwd = _hits_along(occ, tuple(-c for c in d))
        psp += (fwd & bwd).astype(np.int8)
    return occ, psp, lo


def _hits_along(occ, d):
    """For every cell, is there any occupied cell further along direction d?"""
    seen = np.zeros_like(occ)
    cur = occ.copy()
    # Shift-and-or until nothing new appears; bounded by the longest grid diagonal.
    for _ in range(max(occ.shape)):
        cur = _shift(cur, d)
        new = cur & ~seen
        if not new.any():
            break
        seen |= cur
    return seen


def _shift(a, d):
    out = np.zeros_like(a)
    src = tuple(slice(max(0, c), a.shape[i] + min(0, c)) for i, c in enumerate(d))
    dst = tuple(slice(max(0, -c), a.shape[i] + min(0, -c)) for i, c in enumerate(d))
    out[dst] = a[src]
    return out


def cluster(mask):
    """Label 6-connected components without scipy."""
    lab = np.zeros(mask.shape, np.int32)
    n = 0
    idx = np.argwhere(mask)
    pos = {tuple(p): i for i, p in enumerate(idx)}
    for start in map(tuple, idx):
        if lab[start]:
            continue
        n += 1
        stack = [start]
        lab[start] = n
        while stack:
            c = stack.pop()
            for k in range(3):
                for s in (-1, 1):
                    nb = list(c); nb[k] += s; nb = tuple(nb)
                    if nb in pos and not lab[nb]:
                        lab[nb] = n
                        stack.append(nb)
    return lab, n


def main(pdb=None):
    pdb = pdb or NS / "bubr1_pseudokinase_766_1050.pdb"
    xyz, resid = load(pdb)
    print(f"{len(xyz)} heavy atoms, grid {SPACING} A, PSP >= {MIN_PSP}/7")
    occ, psp, lo = psp_grid(xyz)
    mask = (~occ) & (psp >= MIN_PSP)
    print(f"{mask.sum()} buried free grid points")
    lab, n = cluster(mask)
    print(f"{n} raw clusters\n")

    out = []
    for c in range(1, n + 1):
        pts = np.argwhere(lab == c)
        if len(pts) < MIN_POINTS:
            continue
        centre = pts.mean(0) * SPACING + lo
        world = pts * SPACING + lo
        d = np.linalg.norm(xyz[None, :, :] - world[:, None, :], axis=2)
        lining = sorted(set(resid[np.unique(np.argwhere(d < 5.0)[:, 1])].tolist()))
        depth = float(psp[lab == c].mean())
        out.append(dict(vol=len(pts) * SPACING**3, centre=centre,
                        lining=lining, depth=depth))
    out.sort(key=lambda p: -p["vol"])
    print(f"{'#':>2s} {'vol':>6s} {'meanPSP':>7s}  centre                    verdict")
    passing = []
    for i, p in enumerate(out[:12], 1):
        lining = set(p["lining"])
        fails = []
        if lining & set(SCAR):            fails.append("lines the truncation scar")
        if lining & set(ATP_SITE):        fails.append("lines the ATP site")
        if lining & set(CENPE_INTERFACE): fails.append("lines the CENP-E interface")
        verdict = "PASS" if not fails else "; ".join(fails)
        print(f"{i:2d} {p['vol']:6.0f} {p['depth']:7.2f}  "
              f"{p['centre'][0]:7.2f},{p['centre'][1]:7.2f},{p['centre'][2]:7.2f}  {verdict}")
        print(f"   lining: {','.join(map(str, p['lining']))}")
        if not fails:
            passing.append(p)

    if not passing:
        sys.exit("\nNo open pocket is free of the functional sites and the scar. "
                 "Do not screen.")
    best = passing[0]
    c = best["centre"]
    (NS / "millet_site.txt").write_text(
        f"{c[0]:.3f},{c[1]:.3f},{c[2]:.3f}\n"
        f"# LIGSITE PSP>={MIN_PSP} cluster, {best['vol']:.0f} A^3\n"
        f"# lining {','.join(map(str, best['lining']))}\n")
    print(f"\nSELECTED {best['vol']:.0f} A^3 at "
          f"{c[0]:.3f}, {c[1]:.3f}, {c[2]:.3f} -> {NS / 'millet_site.txt'}")
    return out


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)


def native_state_selective(lining, pdb=None):
    """Does this site exist only in the FOLDED protein?

    A ligand stabilises a fold only if it binds the native state preferentially. A
    pocket whose walls come from one stretch of sequence can persist in a partly
    unfolded chain; one whose walls are brought together by tertiary contacts cannot.
    Reports the sequence separation across the lining set -- large separations mean
    the site is a tertiary feature and a ligand for it is native-state-selective.
    """
    import itertools
    pairs = [abs(a - b) for a, b in itertools.combinations(sorted(lining), 2)]
    far = sum(1 for p in pairs if p > 30)
    segs, cur = [], [sorted(lining)[0]]
    for a, b in zip(sorted(lining), sorted(lining)[1:]):
        if b - a <= 3:
            cur.append(b)
        else:
            segs.append(cur); cur = [b]
    segs.append(cur)
    return {"segments": [(s[0], s[-1]) for s in segs],
            "frac_pairs_over_30": far / len(pairs) if pairs else 0.0,
            "median_separation": sorted(pairs)[len(pairs) // 2] if pairs else 0}
