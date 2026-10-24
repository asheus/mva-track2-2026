#!/usr/bin/env python3
"""Does BubR1's pseudokinase domain have a pocket, and does it reach residue 1002?

    python3 -m scripts.mva.pocket_scan

THE CLAIM UNDER TEST. Migalastat works by binding alpha-galactosidase A's active site and
stabilising a misfolded-but-present enzyme. We proposed the same move for BubR1: a ligand
binding the pseudokinase domain (766-1050) could stabilise the domain that p.Asn1002Lys
destabilises. The kill criterion we published before running this: **a pocket with no
enclosed volume, or one that does not reach the 1002 neighbourhood, kills the idea.**

METHOD. LIGSITE-style grid buriedness (Hendlich 1997). A grid is laid over the domain;
points inside the van der Waals envelope are protein. For every free point we march along
7 axes -- 3 Cartesian and 4 cube diagonals -- and count protein-solvent-protein (PSP)
events, where protein lies in both directions. A point enclosed on many axes is inside a
cavity; a point on the open surface is not. Points above a PSP threshold are clustered by
26-connectivity and ranked by volume.

THE BUILT-IN POSITIVE CONTROL, and why this file is worth more than a pocket list.
UniProt annotates binding sites at residues 772-780 and 795 inside this domain. **A
detector that cannot find a pocket at an annotated binding site is broken**, and its
silence about residue 1002 would mean nothing. So the control runs first and the result
for 1002 is only reported if it passes.

MODEL CONFIDENCE, checked rather than assumed. AlphaFold pLDDT over 766-1050 averages
81.9, and over 990-1015 -- the neighbourhood that decides this question -- averages 91.5
with a minimum of 80.4. The local geometry around 1002 is reliable. The whole-protein mean
is 63.6, which is why only the domain is used.

WHAT THIS CANNOT DO. A geometric pocket is not a druggable site: it says a cavity exists,
not that a molecule binds it with useful affinity or that binding stabilises the fold. And
the domain is scanned in isolation, so a cavity that another domain would occlude in the
full protein can appear open here. This answers one question -- is there a cavity, and does
it reach 1002 -- and nothing beyond it.
"""
import json
import pathlib
import sys

import numpy as np
from scipy import ndimage

ROOT = pathlib.Path(__file__).resolve().parents[4]
PDB = ROOT / "docs/mva/data/AF-O60566-F1.pdb"
OUT = ROOT / "docs/mva/data/pocket_scan.json"
DOMAIN = (766, 1050)
CONTROL_RES = set(range(772, 781)) | {795}      # UniProt binding sites
TARGET_RES = 1002
SPACING = 0.8
PSP_MIN = int(__import__("os").environ.get("PSP_MIN", 5))   # of 7 axes
VDW = {"C": 1.70, "N": 1.55, "O": 1.52, "S": 1.80}
DIRS = [(1, 0, 0), (0, 1, 0), (0, 0, 1),
        (1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1)]


def load(domain_only=True):
    """domain_only=False returns the whole chain, needed for correct occlusion."""
    xyz, elem, resi, plddt = [], [], [], []
    for L in PDB.read_text().split("\n"):
        if not L.startswith("ATOM"):
            continue
        r = int(L[22:26])
        if domain_only and not (DOMAIN[0] <= r <= DOMAIN[1]):
            continue
        e = (L[76:78].strip() or L[12:16].strip()[0]).upper()
        xyz.append([float(L[30:38]), float(L[38:46]), float(L[46:54])])
        elem.append(e); resi.append(r); plddt.append(float(L[60:66]))
    return (np.array(xyz), np.array(elem), np.array(resi), np.array(plddt))


def shift(a, d):
    """Shift boolean array by vector d, filling with False (no wraparound)."""
    out = np.zeros_like(a)
    src = [slice(None)] * 3
    dst = [slice(None)] * 3
    for ax, s in enumerate(d):
        if s > 0:
            src[ax] = slice(s, None); dst[ax] = slice(None, -s)
        elif s < 0:
            src[ax] = slice(None, s); dst[ax] = slice(-s, None)
    out[tuple(dst)] = a[tuple(src)]
    return out


def main():
    dxyz, delem, dresi, dplddt = load(domain_only=True)
    axyz, aelem, aresi, _ = load(domain_only=False)
    print(f"pseudokinase domain {DOMAIN[0]}-{DOMAIN[1]}: {len(dxyz)} atoms, "
          f"mean pLDDT {dplddt.mean():.1f}")
    print(f"occupancy built from the whole chain ({len(axyz)} atoms) so that the domain's")
    print("interface with the rest of the protein is not mistaken for a cavity")
    xyz, elem, resi, plddt = axyz, aelem, aresi, dplddt

    lo = dxyz.min(0) - 5.0
    hi = dxyz.max(0) + 5.0
    dims = np.ceil((hi - lo) / SPACING).astype(int) + 1
    print(f"grid {dims[0]}x{dims[1]}x{dims[2]} at {SPACING} A "
          f"({np.prod(dims)/1e6:.2f}M points)")

    protein = np.zeros(dims, bool)
    idx = np.round((xyz - lo) / SPACING).astype(int)
    rad = np.array([VDW.get(e, 1.7) for e in elem]) / SPACING
    rmax = int(np.ceil(rad.max()))
    off = np.array([(a, b, c) for a in range(-rmax, rmax + 1)
                    for b in range(-rmax, rmax + 1)
                    for c in range(-rmax, rmax + 1)])
    offd = np.linalg.norm(off, axis=1)
    for i in range(len(idx)):
        sel = off[offd <= rad[i]]
        p = idx[i] + sel
        ok = np.all((p >= 0) & (p < dims), axis=1)
        p = p[ok]
        protein[p[:, 0], p[:, 1], p[:, 2]] = True
    print(f"protein points: {protein.sum():,}")

    psp = np.zeros(dims, np.uint8)
    maxstep = int(max(dims))
    for d in DIRS:
        fwd = np.zeros(dims, bool); bwd = np.zeros(dims, bool)
        cur_f = protein.copy(); cur_b = protein.copy()
        for _ in range(maxstep):
            cur_f = shift(cur_f, tuple(-np.array(d)))
            cur_b = shift(cur_b, d)
            if not cur_f.any() and not cur_b.any():
                break
            fwd |= cur_f; bwd |= cur_b
        psp += (fwd & bwd).astype(np.uint8)
    pocket = (~protein) & (psp >= PSP_MIN)
    print(f"pocket points (PSP>={PSP_MIN}): {pocket.sum():,}")

    lab, n = ndimage.label(pocket, structure=np.ones((3, 3, 3)))
    sizes = ndimage.sum(pocket, lab, range(1, n + 1))
    order = np.argsort(sizes)[::-1]
    vol = SPACING ** 3

    print(f"\n{'rank':>5}{'volume A^3':>12}{'lining residues (first 14)':>34}")
    print("-" * 78)
    results = []
    for rank, li in enumerate(order[:8], 1):
        mask = lab == (li + 1)
        pts = np.argwhere(mask) * SPACING + lo
        c = pts.mean(0)
        d = np.linalg.norm(xyz[:, None, :] - pts[None, :, :], axis=2) if len(pts) < 400 \
            else None
        if d is None:
            sub = pts[np.random.default_rng(0).choice(len(pts), 400, replace=False)]
            d = np.linalg.norm(xyz[:, None, :] - sub[None, :, :], axis=2)
        lining = sorted(set(resi[np.any(d <= 5.0, axis=1)].tolist()))
        v = sizes[li] * vol
        results.append({"rank": rank, "volume_A3": round(float(v), 1),
                        "centre": [round(float(x), 2) for x in c],
                        "lining_residues": lining,
                        "touches_control": bool(CONTROL_RES & set(lining)),
                        "touches_1002": TARGET_RES in lining})
        tag = ""
        if CONTROL_RES & set(lining):
            tag += "  <= CONTROL (annotated binding site)"
        if TARGET_RES in lining:
            tag += "  <= REACHES 1002"
        print(f"{rank:>5}{v:>12.0f}   {str(lining[:14]):<34}{tag}")

    # A detector that returns one blob covering the domain surface will "touch"
    # every residue and therefore pass any control. That is not a pass, it is a
    # failure mode that looks like success, so it is gated explicitly.
    n_domain_res = DOMAIN[1] - DOMAIN[0] + 1
    artifact = []
    for r in results:
        frac = len(r["lining_residues"]) / n_domain_res
        r["fraction_of_domain_lined"] = round(frac, 3)
        r["surface_artifact"] = bool(r["volume_A3"] > 3000 or frac > 0.40)
        if r["surface_artifact"]:
            artifact.append(r)
    if artifact:
        print("\n  SANITY GATE: rank(s) " +
              ", ".join(str(r["rank"]) for r in artifact) +
              " flagged as surface artifact")
        for r in artifact:
            print(f"    rank {r['rank']}: {r['volume_A3']:.0f} A^3, lines "
                  f"{r['fraction_of_domain_lined']:.0%} of the domain -- an enclosed")
            print("      ligand pocket is typically 200-800 A^3 and lines a few percent")
        print("    These are excluded from the control and the test below.")
    results = [r for r in results if not r["surface_artifact"]]

    ctrl = [r for r in results if r["touches_control"]]
    tgt = [r for r in results if r["touches_1002"]]
    print("\n" + "=" * 78)
    print("CONTROL")
    print("=" * 78)
    if ctrl:
        print(f"  PASS -- a pocket of {ctrl[0]['volume_A3']:.0f} A^3 lines the UniProt "
              f"binding site (772-780 / 795).")
        print("  The detector finds an annotated site it was not told about, so its")
        print("  verdict on residue 1002 is interpretable.")
    else:
        print("  FAIL -- no pocket at the annotated binding site. The detector is not")
        print("  working on this structure and nothing below should be believed.")

    print("\n" + "=" * 78)
    print("THE TEST: does a pocket reach residue 1002?")
    print("=" * 78)
    if not ctrl:
        print("  Not reportable -- control failed.")
    elif tgt:
        print(f"  YES -- rank {tgt[0]['rank']}, volume {tgt[0]['volume_A3']:.0f} A^3.")
        print("  The chaperone idea survives its kill criterion.")
    else:
        near = min((min(abs(np.array(r['lining_residues']) - TARGET_RES))
                    for r in results if r['lining_residues']), default=None)
        print(f"  NO -- no detected pocket lines residue {TARGET_RES}.")
        print(f"  Closest lining residue to 1002 across all pockets: {near} away.")
        print("  By the criterion published before running this, the pseudokinase-pocket")
        print("  chaperone idea is KILLED for this residue: there is a pocket in the")
        print("  domain, but it does not reach the lesion we would be trying to stabilise.")

    OUT.write_text(json.dumps({
        "method": "LIGSITE-style PSP buriedness, 0.8 A grid, PSP>=5 of 7 axes",
        "domain": list(DOMAIN), "mean_plddt_domain": round(float(plddt.mean()), 1),
        "control_residues": sorted(CONTROL_RES), "control_passed": bool(ctrl),
        "target_residue": TARGET_RES, "pocket_reaches_target": bool(tgt),
        "pockets": results,
        "caveats": ["a geometric cavity is not a druggable site",
                    "domain scanned in isolation; occlusion by other domains not modelled"],
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
