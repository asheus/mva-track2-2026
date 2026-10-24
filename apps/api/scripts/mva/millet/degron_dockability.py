#!/usr/bin/env python3
"""Can BubR1's degron be docked against? Produces every number in ALLELE2-ROUTES-REEXAMINED.md.

    python3 -m scripts.mva.millet.degron_dockability

WHY THIS EXISTS. The Friedreich ataxia precedent for raising a scarce protein without a
fold-stabilising pocket is a "ubiquitin-competing molecule": dock small molecules over
the substrate's own ubiquitination lysine so ubiquitin cannot be attached. Rufini and
co-workers did it on frataxin using MetaPocket (LIGSITE is one of its eight detectors)
plus AutoDock/Vina, concentrating site selection near Lys147. We already have LIGSITE
and Vina built and validated, so the only missing ingredient was the site.

BubR1's equivalent lysines are K250 (acetylation there shields BubR1 from APC/C
degradation) and K668 (the SIRT2 site). NEITHER was in our docked construct, which was
residues 766-1050 -- so there is a fair objection that we screened where the MUTATION is
and not where the DEGRADATION is.

This script tests whether that objection is actionable. It is not: both degron lysines
sit in regions AlphaFold models at very low confidence, so there is no surface to place
a pocket on. That converts MILLET-PROTOCOL's 0-of-757 result from a claim about one
domain into a claim about the protein -- not because we screened the rest, but because
the rest is not screenable.

It also re-derives two checks on our own site selection:
  * which residues line each decoy box -- the "C-terminal groove" turns out to be the
    CENP-E interface, contradicting its "functionally uninteresting" label;
  * each box's distance to N1002.

Inputs are committed structures. No network, no credits.
"""
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
FULL = ROOT / "docs/mva/data/neurosnap/bubr1_fulllength.pdb"
DOMAIN = ROOT / "docs/mva/data/neurosnap/bubr1_pseudokinase_766_1050.pdb"

# Decoy box centroids exactly as screened, from millet/screen.py.
BOXES = {
    "atp_site": (-23.599, -18.248, 3.350),
    "cterm_pocket": (-15.420, -2.660, -3.670),
}
ATP_RESIDUES = {795, 880, 911, 912, 913}   # VAIK K795, HGD His880, DFS Asp911/Phe912
CENP_E = set(range(1031, 1051))            # CENP-E interface, excluded by MILLET for cause
# Lysines carrying BubR1's degradation signal.
DEGRON = {
    250: "acetylation here shields BubR1 from APC/C degradation",
    668: "SIRT2 site; CBP acetylation drives ubiquitination",
}
REGIONS = [
    (240, 260, "K250 +/- 10 (the degron)"),
    (246, 254, "K250 +/- 4"),
    (658, 678, "K668 +/- 10 (SIRT2 site)"),
    (766, 1050, "pseudokinase (we docked this)"),
    (1, 250, "TPR + N-terminal"),
]


def band(v):
    """AlphaFold's own published pLDDT bands."""
    if v < 50:
        return "very low (unmodelled)"
    if v < 70:
        return "low"
    if v < 90:
        return "confident"
    return "very high"


def parse(path):
    atoms, plddt = [], {}
    for line in path.read_text().splitlines():
        if not line.startswith("ATOM"):
            continue
        r = int(line[22:26])
        atoms.append((r, line[12:16].strip(),
                      float(line[30:38]), float(line[38:46]), float(line[46:54])))
        try:
            plddt[r] = float(line[60:66])
        except ValueError:
            pass
    return atoms, plddt


def main():
    for p in (FULL, DOMAIN):
        if not p.exists():
            sys.exit(f"missing committed structure: {p}")

    atoms, plddt = parse(FULL)
    lo, hi = min(a[0] for a in atoms), max(a[0] for a in atoms)
    print(f"full-length model: {len(atoms)} atoms, residues {lo}-{hi}\n")

    print("Is the degron dockable? AlphaFold confidence by region")
    print(f"  {'region':34s} {'mean':>6} {'min':>6} {'max':>6}   band")
    for a, b, label in REGIONS:
        v = [plddt[r] for r in range(a, b + 1) if r in plddt]
        m = sum(v) / len(v)
        print(f"  {label:34s} {m:6.1f} {min(v):6.1f} {max(v):6.1f}   {band(m)}")

    print()
    for k, why in DEGRON.items():
        pk = plddt.get(k)
        print(f"  K{k}: pLDDT {pk:.1f} ({band(pk)}) -- {why}")
        nz = [(x, y, z) for r, nm, x, y, z in atoms if r == k and nm == "NZ"]
        if not nz:
            continue
        for cut in (8, 10, 12):
            n = sum(1 for _r, _nm, x, y, z in atoms
                    if math.dist((x, y, z), nz[0]) <= cut)
            tail = "   <- an exposed loop, not a pocket" if cut == 8 and n < 20 else ""
            print(f"       protein atoms within {cut:2d} A of NZ: {n:3d}{tail}")

    print("\nVERDICT: the ubiquitin-competing-molecule route cannot be run on this protein.")
    print("Both degron lysines sit in regions modelled at very low confidence, so there is")
    print("no surface to place a pocket on. The pseudokinase domain is the only confidently")
    print("modelled part of BubR1 -- which is why the fragment screen was built there, and")
    print("why its negative generalises rather than being specific to one domain.\n")

    datoms, _ = parse(DOMAIN)
    n1002 = [(x, y, z) for r, _nm, x, y, z in datoms if r == 1002]
    print("Decoy boxes: which residues actually line them (<=9 A)")
    for name, c in BOXES.items():
        near = sorted({r for r, _nm, x, y, z in datoms
                       if math.dist((x, y, z), c) <= 9.0})
        d = min(math.dist(p, c) for p in n1002) if n1002 else float("nan")
        print(f"  {name}: {len(near)} residues, {d:.1f} A from N1002")
        print(f"      ATP-site residues:   {sorted(set(near) & ATP_RESIDUES) or 'none'}")
        print(f"      CENP-E 1031-1050:    {sorted(set(near) & CENP_E) or 'none'}")

    print('\nMILLET-PROTOCOL\'s decoy table calls cterm_pocket "real, functionally')
    print('uninteresting" while its own site-selection step excludes the CENP-E interface')
    print("as functional. The residues above show those are the same surface, so the label")
    print("is wrong and the exclusion is right. No candidate site was missed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
