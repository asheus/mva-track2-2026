#!/usr/bin/env python3
"""Calibrate the missense arm — the half of the map the proband's allele 2 lives in.

    python3 -m scripts.mva.missense_arm

WHY. The splice arm is calibrated against 946 measured outcomes with a sealed evaluation
(C40). The missense arm, 1,494 variants including `p.Asn1002Lys`, has never been
calibrated at all. The session that built the splice calibration made the arm that helps
other patients rigorous while the arm that decides this child's hypothesis rested on
predicted-against-predicted comparison.

C41 supplied the one axis that survives contact with measured protein abundance:
**burying a new charge** costs abundance, and only when buried — replicated across PTEN
and TPMT VAMP-seq and NUDT15, with the exposed correlation at zero each time. Absolute
volume change failed in all three and reversed in one, and is not used here.

So this file does two things. It TESTS whether that axis transfers to BUB1B's own labelled
variants, and it applies the axis across all 1,494 missense — but only where the axis
actually applies, which is the point of calibrating rather than scoring.

TWO TESTS, CRITERIA FIXED BEFORE LOOKING.

TEST A — does the validated axis transfer to this gene?
Among BUB1B's own labelled missense variants, is buried-charge introduction enriched in
pathogenic/likely-pathogenic relative to benign/likely-benign?
  PASS  Fisher exact one-sided p < 0.05 with enrichment in P/LP.
  FAIL  no enrichment.
A FAIL is the outcome to want recorded in advance: it would mean the axis validated on
three other proteins does not hold in BUB1B, and every statement about N1002K then rests
on cross-protein transfer alone, which the report would have to say.
Known limit, stated now: BUB1B's pathogenic alleles are overwhelmingly truncating — 55 of
69 — so the P/LP missense count is small and this test is underpowered by construction.
The counts are printed whatever the p-value does.

TEST B — is AlphaMissense usable on this protein at all?
Five panel variants have MEASURED 5-10x reduced BubR1 (I909T, R814H, L1012P, L844F,
R727C) and two are measured normal (R550Q, Q921H). AlphaMissense should rank the five
above the two.
  PASS  all five score above both normals.   FAIL  fewer than four do.
n is 5 against 2. This cannot be significant and is not treated as significance: it is a
smoke test on whether the predictor is pointing the right way in this protein, and
`predictor_calibration.py` already says so about its own AUCs.

WHAT THE OUTPUT IS, AND IS NOT. Where the validated axis applies — a buried position
taking a new charge — the direction is reported. Where it does not apply, the row says so
instead of borrowing a number from an axis that failed. A missense arm that answers for
every variant would be the thing to distrust.
"""
import collections
import csv
import io
import json
import math
import pathlib
import sys
import urllib.request

sys.path.insert(0, __import__("pathlib").Path(__file__).resolve().parent.as_posix())
from neighbourhood_structure import fetch, MAXASA, THREE, VDW   # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[4]
AM_URL = "https://alphafold.ebi.ac.uk/files/AF-O60566-F1-aa-substitutions.csv"
AM_CACHE = pathlib.Path(__import__("tempfile").gettempdir()) / "am_o60566.csv"
ATLAS = ROOT / "docs/mva/data/variants/ebi_proteins_O60566_variation.json"
MAP = ROOT / "docs/mva/data/nmd/eligibility_map.tsv"
OUT = ROOT / "docs/mva/data/missense_arm.tsv"
META = ROOT / "docs/mva/data/missense_arm.json"

BURIED = 20.0
CHARGED = set("DEKRH")
PATH = ("pathogenic", "likely pathogenic")
BEN = ("benign", "likely benign")
# measured panel, from predictor_calibration.py
DESTAB = ["I909T", "R814H", "L1012P", "L844F", "R727C"]
NORMAL = ["R550Q", "Q921H"]


def rsa_map(atoms, n=480):
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


def load_am():
    raw = (AM_CACHE.read_text() if AM_CACHE.exists() else
           urllib.request.urlopen(urllib.request.Request(
               AM_URL, headers={"User-Agent": "research/1.0"}), timeout=180)
           .read().decode())
    out = {}
    for r in csv.DictReader(io.StringIO(raw)):
        v = r["protein_variant"]
        out[v] = (float(r["am_pathogenicity"]), r["am_class"])
    return out


def label(sigs):
    s = " ".join(x.lower() for x in sigs)
    hp = any(k in s for k in PATH)
    hb = any(k in s for k in BEN)
    if hp and hb:
        return None                       # conflicting; excluded both ways
    if hp:
        return "P/LP"
    if hb:
        return "B/LB"
    return None


def main():
    atoms = fetch()
    rsa, seqres = rsa_map(atoms)
    am = load_am()
    print(f"structure {len(atoms)} atoms · RSA for {len(rsa)} residues · "
          f"AlphaMissense for {len(am)} substitutions")

    feats = json.loads(ATLAS.read_text())
    feats = feats.get("features", feats if isinstance(feats, list) else [])
    labelled = []
    for f in feats:
        if f.get("consequenceType") != "missense":
            continue
        lab = label([c.get("type", "") for c in (f.get("clinicalSignificances") or [])])
        if not lab:
            continue
        try:
            pos = int(f["begin"])
        except (KeyError, ValueError):
            continue
        ref, alt = f.get("wildType"), f.get("alternativeSequence")
        if not ref or not alt or len(ref) != 1 or len(alt) != 1:
            continue
        if pos not in rsa:
            continue
        labelled.append({"pos": pos, "ref": ref, "alt": alt, "label": lab,
                         "rsa": rsa[pos],
                         "buried_charge": int(rsa[pos] < BURIED and alt in CHARGED
                                              and ref not in CHARGED)})
    print(f"labelled missense with a position in the model: {len(labelled)}")

    # ---------------- TEST A ----------------
    print("\n" + "=" * 72)
    print("TEST A  does buried-charge introduction transfer to BUB1B's own labels?")
    print("=" * 72)
    tab = collections.Counter((r["label"], r["buried_charge"]) for r in labelled)
    a = tab[("P/LP", 1)]
    b = tab[("P/LP", 0)]
    c = tab[("B/LB", 1)]
    d = tab[("B/LB", 0)]
    print(f"                buried charge   not")
    print(f"  P/LP          {a:13d}   {b:3d}")
    print(f"  B/LB          {c:13d}   {d:3d}")
    print(f"\n  P/LP missense n={a+b}  (BUB1B's pathogenic alleles are 55/69 truncating,")
    print(f"  so this margin is small by construction, not by sampling accident)")
    verdict_a = "UNDERPOWERED"
    if (a + b) and (c + d):
        try:
            from scipy.stats import fisher_exact
            odds, p = fisher_exact([[a, b], [c, d]], alternative="greater")
            rate_p = a / (a + b)
            rate_b = c / (c + d)
            print(f"\n  rate in P/LP {rate_p:.1%}   rate in B/LB {rate_b:.1%}")
            print(f"  Fisher exact one-sided: OR={odds:.3g}  p={p:.4g}")
            verdict_a = "PASS" if p < 0.05 else "FAIL (no enrichment at p<0.05)"
            print(f"  verdict: {verdict_a}")
            if verdict_a.startswith("FAIL"):
                print("\n  So the axis validated on PTEN, TPMT and NUDT15 is NOT")
                print("  demonstrated in BUB1B's own labelled variants. Every statement")
                print("  about N1002K's abundance then rests on cross-protein transfer,")
                print("  and the report must say exactly that.")
        except ImportError:
            print("  scipy unavailable; counts reported, no test run")
    else:
        print("\n  a margin is empty: no test possible, nothing claimed")

    # ---------------- TEST B ----------------
    print("\n" + "=" * 72)
    print("TEST B  does AlphaMissense point the right way on the measured panel?")
    print("=" * 72)
    def sc(v):
        return am.get(v, (float("nan"), "?"))[0]
    print("  measured 5-10x REDUCED:")
    for v in DESTAB:
        print(f"    {v:8s} {sc(v):.4f}   RSA "
              f"{rsa.get(int(''.join(ch for ch in v[1:-1] if ch.isdigit())), float('nan')):5.1f}%")
    print("  measured NORMAL:")
    for v in NORMAL:
        print(f"    {v:8s} {sc(v):.4f}")
    hi = max(sc(v) for v in NORMAL)
    above = [v for v in DESTAB if sc(v) > hi]
    print(f"\n  destabilising variants scoring above BOTH normals: "
          f"{len(above)}/5  ({', '.join(above) if above else 'none'})")
    verdict_b = ("PASS" if len(above) == 5 else
                 "FAIL" if len(above) < 4 else "INCONCLUSIVE")
    print(f"  verdict (5 pass / <4 fail): {verdict_b}")
    print("  n is 5 against 2; this is a direction check, never a significance claim.")

    # ---------------- the arm ----------------
    print("\n" + "=" * 72)
    print("APPLYING THE AXIS ACROSS THE MAP'S MISSENSE VARIANTS")
    print("=" * 72)
    lines = MAP.read_text().strip().split("\n")
    cols = lines[0].split("\t")
    rows = [dict(zip(cols, L.split("\t"))) for L in lines[1:]]
    mis = [r for r in rows if r["variant_class"] == "missense"]
    out, tally = [], collections.Counter()
    import re
    for r in mis:
        m = re.match(r"^([A-Z])(\d+)([A-Z])$", (r.get("residue") or "").strip()) or \
            re.match(r"^([A-Z])(\d+)([A-Z])$", (r.get("variant") or "").strip())
        if not m:
            tally["unparsed_variant_string"] += 1
            continue
        ref, pos, alt = m.group(1), int(m.group(2)), m.group(3)
        rs = rsa.get(pos)
        amv = am.get(f"{ref}{pos}{alt}", (None, None))[0]
        if rs is None:
            cls, why = "AXIS_NA_no_structure", "position absent from the model"
        elif not (alt in CHARGED and ref not in CHARGED):
            cls, why = "AXIS_NA_no_new_charge", "introduces no new charge"
        elif rs >= BURIED:
            cls, why = "AXIS_NA_not_buried", f"RSA {rs:.1f}% is not buried"
        else:
            cls = "ABUNDANCE_RISK_buried_new_charge"
            why = f"RSA {rs:.1f}%, {ref}->{alt} buries a new charge"
        tally[cls] += 1
        out.append({"variant": f"{ref}{pos}{alt}", "pos": pos, "ref": ref, "alt": alt,
                    "rsa": "" if rs is None else round(rs, 1),
                    "alphamissense": "" if amv is None else amv,
                    "axis_class": cls, "basis": why,
                    "clinvar_significance": r.get("clinvar_significance", "")})
    for k, v in tally.most_common():
        print(f"  {k:36s} {v:5d}")
    print(f"\n  the validated axis APPLIES to "
          f"{tally['ABUNDANCE_RISK_buried_new_charge']} of {len(mis)} missense variants.")
    print("  For the rest it says nothing, and the row records why rather than")
    print("  substituting a number from the axis that failed external validation.")
    n1002 = [o for o in out if o["pos"] == 1002 and o["alt"] == "K"]
    if n1002:
        o = n1002[0]
        print(f"\n  THE PROBAND'S ALLELE 2: {o['variant']}  RSA {o['rsa']}%  "
              f"AlphaMissense {o['alphamissense']}  ->  {o['axis_class']}")

    cw = ["variant", "pos", "ref", "alt", "rsa", "alphamissense", "axis_class",
          "basis", "clinvar_significance"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        f.write("\t".join(cw) + "\n")
        for o in out:
            f.write("\t".join(str(o.get(k, "")).replace("\t", " ") for k in cw) + "\n")
    META.write_text(json.dumps({
        "axis": "buried new charge introduction (validated on measured abundance, C41)",
        "axis_not_used": "absolute volume change — failed in all three assays, C41a",
        "buried_rsa_threshold": BURIED,
        "test_a": {"question": "does the axis transfer to BUB1B's own labels?",
                   "plp_buried_charge": a, "plp_other": b,
                   "benign_buried_charge": c, "benign_other": d,
                   "verdict": verdict_a},
        "test_b": {"question": "does AlphaMissense point the right way on the panel?",
                   "destabilising_above_both_normals": len(above),
                   "of": len(DESTAB), "verdict": verdict_b},
        "axis_applies_to": tally["ABUNDANCE_RISK_buried_new_charge"],
        "missense_total": len(mis),
        "tally": dict(tally),
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)} and {META.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
