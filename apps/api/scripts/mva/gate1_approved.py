#!/usr/bin/env python3
"""Gate 1 of the MVA Track 2 funnel: establish APPROVAL, and tier it honestly.

    python3 -m scripts.mva.gate1_approved
    python3 -m scripts.mva.gate1_approved --write

WHY THIS EXISTS, and why it is not the gate originally planned. The first draft
of the funnel said "require an ATC code" as the approval filter. That is wrong.
A WHO ATC code classifies a SUBSTANCE; it is assigned to compounds that are not
approved anywhere, and treating it as an approval signal would let the funnel
propose an unapproved molecule as a repurposing candidate. The hackathon asks
for "existing, approved medications", so approval has to be evidenced, not
inferred from a classification.

The pool's sources differ in what they can support, so this gate tiers rather
than filters, and the tier travels with every row downstream:

  A  approved, primary regulator evidence
     `ema`   EMA's authorised-medicines table, withdrawn/refused already excluded
     `world` FDA Purple Book / EMA / PMDA / WHO
     `gabi`  archived regional approval tables (AU, CA, PMDA)
     `held`  a named supplier sells it, so some regulator approved it
     -> may be proposed as an approved medication.

  B  approval asserted by a secondary source
     `wikipedia` therapeutic-antibody list with approved_western true
     -> may be proposed, but the report must say the evidence is secondary and
        re-derive it from a regulator before it ships.

  C  classification only
     `atc` alone, or wikipedia with approved_western not true
     -> NOT proposable as approved. Retained because a tier-C row can still be
        mechanistically informative (it may name the pathway a tier-A drug hits),
        but it can never be the answer.

Tier C is kept rather than dropped precisely so that the count of what was
excluded, and why, stays visible. A funnel that silently discards is a funnel
nobody can audit.
"""
import argparse, collections, json, pathlib

HERE = pathlib.Path(__file__).resolve()
DATA = HERE.parents[2] / "data" / "mva"
IN, OUT = DATA / "universe.json", DATA / "gate1.json"

PRIMARY = {"ema", "world", "gabi", "held"}


def tier(row):
    srcs = set(row.get("sources") or [])
    if srcs & PRIMARY:
        return "A"
    if "wikipedia" in srcs and row.get("approved_western") is True:
        return "B"
    return "C"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    if not IN.exists():
        raise SystemExit(f"missing {IN} — run gate0_universe.py --write first")
    rows = json.loads(IN.read_text())["molecules"]

    for r in rows:
        r["approval_tier"] = tier(r)
    counts = collections.Counter(r["approval_tier"] for r in rows)

    print(f"gate 0 universe   {len(rows):>6}")
    for t, label in (("A", "approved, primary regulator evidence"),
                     ("B", "approval asserted by secondary source"),
                     ("C", "classification only — NOT proposable")):
        print(f"  tier {t}         {counts[t]:>6}  {label}")
    proposable = counts["A"] + counts["B"]
    print(f"PROPOSABLE (A+B)  {proposable:>6}\n")

    ab = [r for r in rows if r["approval_tier"] in ("A", "B")]
    print(f"of the proposable set:")
    print(f"  with ATC code   {sum(1 for r in ab if r.get('atc')):>6}")
    print(f"  with indication {sum(1 for r in ab if r.get('areas')):>6}")
    print(f"  biosimilar      {sum(1 for r in ab if r.get('biosimilar_flag')):>6}")

    if a.write:
        OUT.write_text(json.dumps(
            {"gate": 1, "count": len(rows), "tiers": dict(counts),
             "proposable": proposable, "molecules": rows}, indent=1) + "\n")
        print(f"\nwrote {OUT.name}")


if __name__ == "__main__":
    main()
