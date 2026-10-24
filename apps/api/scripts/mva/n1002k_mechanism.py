#!/usr/bin/env python3
"""What, specifically, does p.Asn1002Lys break?

    python3 -m scripts.mva.n1002k_mechanism

WHY THIS, AND WHY NOW. Every therapeutic statement in this workstream is downstream of one
question: does allele 2 leave protein behind. The map answers that it is ANSWERABLE --
RSA 14.0%, pLDDT 91, buried and confidently modelled -- and not answered.

C41 then narrowed the mechanism. Tested against measured steady-state abundance in PTEN,
TPMT and NUDT15, two candidate axes behaved differently: burying a NEW CHARGE costs
abundance and does so only when buried (rho -0.21/-0.21/-0.14 buried against
+0.04/-0.00/+0.03 exposed, 4,907 measured buried variants), while absolute volume change
showed no burial dependence and reversed in one assay. N1002K is both: Asn -> Lys buries a
new formal positive charge AND adds 54.5 A^3. So the surviving axis is the charge, and
"buries a charge" is where the argument has stopped.

That is a CATEGORY, not a mechanism. A category cannot be falsified in a lab. This file
asks the next question -- which specific interaction does a lysine at 1002 break -- from
the model's own atoms rather than from a summary statistic:

  * every charged side chain within 8 A of N1002's side chain, with its own burial, so a
    like-charge clash is identified rather than assumed;
  * the electrostatic burden a +1 at 1002 would carry, as a sum of 1/r over neighbouring
    formal charges, signed so that repulsion and attraction do not cancel silently;
  * every hydrogen bond N1002's own amide makes, since Asn's ND2/OD1 pair donates and
    accepts and a lysine keeps only the donor.

WHAT WOULD MAKE THIS WRONG. The model is predicted: AlphaFold AF-O60566-F1, and the
pseudokinase domain has ZERO experimental structure coverage (C29c) -- the best of the five
BUB1B PDB entries stops 421 residues short of 1002. pLDDT 91 says the backbone is
confident; it does not promise the side-chain rotamers this file measures distances
between. So every number here is a hypothesis about a predicted structure, and the
reported shell is the thing a wet lab would check first.

NO PASS/FAIL IS DECLARED HERE, deliberately. This file measures a neighbourhood; it does
not test a claim. The claims it feeds are tested in the two sections of
missense_arm.py, which do declare their criteria before looking.
"""
import json
import math
import pathlib
import sys

sys.path.insert(0, __import__("pathlib").Path(__file__).resolve().parent.as_posix())
from neighbourhood_structure import fetch, MAXASA, THREE, VDW   # noqa: E402

OUT = pathlib.Path(__file__).resolve().parents[4] / "docs/mva/data/n1002k_mechanism.json"
TARGET = 1002
SHELL = 8.0          # A, around the side chain
HBOND = 3.5          # A, heavy-atom donor/acceptor distance
# Formal charge carriers at pH 7.4, by the atoms that actually carry the charge.
CHARGED = {
    ("ASP", "OD1"): -0.5, ("ASP", "OD2"): -0.5,
    ("GLU", "OE1"): -0.5, ("GLU", "OE2"): -0.5,
    ("LYS", "NZ"): +1.0,
    ("ARG", "NE"): +0.33, ("ARG", "NH1"): +0.33, ("ARG", "NH2"): +0.33,
}
# His is left out of the formal sum on purpose: mostly neutral at 7.4, and including it
# at +1 would inflate any like-charge burden we report. It is listed separately instead.
HIS_ATOMS = {("HIS", "ND1"), ("HIS", "NE2")}
SIDE_CHAIN_SKIP = {"N", "CA", "C", "O", "OXT"}
ASN_SIDE = {"CB", "CG", "OD1", "ND2"}


def rsa_map(atoms, n=480):
    """Shrake-Rupley RSA per residue; same method as burial_vs_constraint.py."""
    import numpy as np
    xyz = np.array([[a["x"], a["y"], a["z"]] for a in atoms])
    rad = np.array([VDW.get(a["el"], 1.7) for a in atoms]) + 1.4
    seq = np.array([a["seq"] for a in atoms])
    res = {}
    for a in atoms:
        res.setdefault(a["seq"], THREE.get(a["res"], "X"))
    k = np.arange(n)
    off, inc = 2.0 / n, math.pi * (3 - math.sqrt(5))
    y = k * off - 1 + off / 2
    r = np.sqrt(np.maximum(0, 1 - y * y))
    phi = k * inc
    S = np.stack([np.cos(phi) * r, y, np.sin(phi) * r], axis=1)
    area, rmax = {}, rad.max()
    for i in range(len(atoms)):
        d = np.linalg.norm(xyz - xyz[i], axis=1)
        nb = np.where((d < rad[i] + rmax) & (d > 0))[0]
        pts = xyz[i] + rad[i] * S
        dd = np.linalg.norm(pts[:, None, :] - xyz[nb][None, :, :], axis=2)
        acc = int(np.sum(~np.any(dd < rad[nb][None, :], axis=1)))
        area[seq[i]] = area.get(seq[i], 0.0) + 4 * math.pi * rad[i] ** 2 * acc / n
    return {p: 100 * a / MAXASA.get(res[p], 200) for p, a in area.items()}, res


def dist(a, b):
    return math.sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2
                     + (a["z"] - b["z"]) ** 2)


def main():
    atoms = fetch()
    print(f"AF-O60566-F1: {len(atoms)} atoms")
    rsa, res1 = rsa_map(atoms)
    tgt = [a for a in atoms if a["seq"] == TARGET]
    if not tgt:
        sys.exit(f"residue {TARGET} not in the model")
    name = tgt[0]["res"]
    print(f"residue {TARGET} is {name} ({res1.get(TARGET)}), "
          f"RSA {rsa.get(TARGET, float('nan')):.1f}%")
    if res1.get(TARGET) != "N":
        print("  WARNING: the model does not carry Asn here; the rest assumes it does")
    side = [a for a in tgt if a["name"] in ASN_SIDE]
    print(f"  side-chain atoms found: {sorted(a['name'] for a in side)}")
    if not side:
        sys.exit("no side-chain atoms for the target; cannot measure a shell")

    # ---------- the charged shell ----------
    print(f"\n{'='*72}\nCHARGED SIDE CHAINS WITHIN {SHELL:.0f} A OF THE N1002 SIDE CHAIN")
    print("=" * 72)
    found = {}
    for a in atoms:
        if a["seq"] == TARGET:
            continue
        key = (a["res"], a["name"])
        q = CHARGED.get(key)
        is_his = key in HIS_ATOMS
        if q is None and not is_his:
            continue
        d = min(dist(a, s) for s in side)
        if d > SHELL:
            continue
        rec = found.setdefault(a["seq"], {"res": a["res"], "d": d, "q": 0.0,
                                          "his": is_his, "atoms": []})
        rec["d"] = min(rec["d"], d)
        rec["atoms"].append(a["name"])
        if q is not None:
            rec["q"] += q
    if not found:
        print("  none. A lysine here would carry no like-charge partner, which makes")
        print("  desolvation rather than repulsion the mechanism to test.")
    pos = neg = 0
    burden = 0.0
    for seq in sorted(found, key=lambda s: found[s]["d"]):
        r = found[seq]
        q = round(r["q"], 2)
        tag = ("HIS, excluded from the sum" if r["his"] and not q
               else "positive" if q > 0 else "negative" if q < 0 else "neutral")
        print(f"  {r['res']}{seq:<5} {r['d']:5.2f} A   formal {q:+.2f}  "
              f"RSA {rsa.get(seq, float('nan')):5.1f}%   {tag}")
        if q > 0:
            pos += 1
        elif q < 0:
            neg += 1
        # signed 1/r burden for a +1 placed at 1002
        if q:
            burden += (1.0 * q) / max(r["d"], 1.0)
    print(f"\n  positive neighbours {pos}   negative neighbours {neg}")
    print(f"  signed electrostatic burden for a +1 at {TARGET}: {burden:+.3f} e/A")
    print("  (positive = net repulsion, negative = net attraction; a sum of q/r over")
    print("   formal charges, not a force field, and not an energy)")

    # ---------- hydrogen bonds the Asn amide makes ----------
    print(f"\n{'='*72}\nHYDROGEN BONDS MADE BY THE N1002 AMIDE (heavy atoms <= "
          f"{HBOND} A)\n{'='*72}")
    hb = []
    for sa in [a for a in side if a["name"] in ("OD1", "ND2")]:
        for a in atoms:
            if a["seq"] == TARGET or a["el"] not in ("N", "O"):
                continue
            d = dist(a, sa)
            if d <= HBOND:
                hb.append((sa["name"], a["res"], a["seq"], a["name"], d))
    if not hb:
        print("  none within the cutoff.")
    for sn, rr, sq, an, d in sorted(hb, key=lambda x: x[4]):
        print(f"  N1002:{sn:<4} -- {rr}{sq}:{an:<4} {d:4.2f} A   "
              f"(partner RSA {rsa.get(sq, float('nan')):.1f}%)")
    print(f"\n  Asn carries BOTH a donor (ND2) and an acceptor (OD1). Lysine's NZ donates")
    print(f"  only, so any contact listed above that depends on OD1 ACCEPTING cannot be")
    print(f"  satisfied by a lysine at this position.")
    lost = [h for h in hb if h[0] == "OD1"]
    print(f"  contacts through OD1, the acceptor lysine cannot replace: {len(lost)}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "model": "AF-O60566-F1 (AlphaFold, predicted; pseudokinase domain has zero "
                 "experimental structure coverage)",
        "residue": TARGET, "wildtype": res1.get(TARGET),
        "rsa_percent": rsa.get(TARGET),
        "shell_angstrom": SHELL,
        "charged_shell": [
            {"residue": f"{found[s]['res']}{s}", "min_distance": round(found[s]["d"], 2),
             "formal_charge": round(found[s]["q"], 2), "rsa_percent": rsa.get(s),
             "his_excluded_from_sum": found[s]["his"] and not round(found[s]["q"], 2)}
            for s in sorted(found, key=lambda s: found[s]["d"])],
        "positive_neighbours": pos, "negative_neighbours": neg,
        "signed_burden_for_plus_one": round(burden, 3),
        "hydrogen_bonds": [{"from": f"N1002:{h[0]}", "to": f"{h[1]}{h[2]}:{h[3]}",
                            "distance": round(h[4], 2)} for h in
                           sorted(hb, key=lambda x: x[4])],
        "acceptor_contacts_lysine_cannot_replace": len(lost),
        "caveat": "A hypothesis about a predicted structure. pLDDT 91 supports the "
                  "backbone, not the side-chain rotamers these distances are measured "
                  "between.",
    }, indent=2) + "\n")
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
