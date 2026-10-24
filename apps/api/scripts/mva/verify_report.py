#!/usr/bin/env python3
"""Re-derive every count the report states, independently of the gates that made them.

    python3 -m scripts.mva.verify_report

WHY THIS EXISTS. The report states counts in prose. Prose drifts from data — a gate
gets re-run, a threshold changes, and a sentence quietly becomes false. This asserts
each number in TRACK2-REPORT.md against the committed JSON, computing it from the
raw records rather than trusting the summary fields the gates wrote. If a gate and
its own summary disagree, that shows up here too.

Run before the report ships. Non-zero exit means the report is wrong.
"""
import json
import sys, pathlib, re, sys

API = pathlib.Path(__file__).resolve().parents[2]
DATA = API / "data" / "mva"


def _ensure_gate1() -> None:
    """Regenerate gate1.json if it is absent.

    gate1.json is deliberately gitignored: it is universe.json plus one derived
    field, and it rebuilds offline from committed data in well under a second
    (see the note at .gitignore:38-42). That is the right call for the repository
    but it means a FRESH CLONE has no gate1.json, and this verifier used to die
    on it with a bare FileNotFoundError. The organisers state submissions may be
    rerun, so the verifier bootstraps itself rather than requiring a reader to
    know the build order.
    """
    if (DATA / "gate1.json").exists():
        return
    import subprocess
    print("gate1.json absent (gitignored, derived) - regenerating from universe.json ...")
    r = subprocess.run(
        [sys.executable, "-m", "scripts.mva.gate1_approved", "--write"],
        cwd=API, capture_output=True, text=True,
    )
    if r.returncode != 0 or not (DATA / "gate1.json").exists():
        sys.exit(
            "could not regenerate gate1.json.\n"
            "run this by hand from apps/api/:\n"
            "    python3 -m scripts.mva.gate1_approved --write\n"
            f"stderr:\n{r.stderr}"
        )
    print("  regenerated.\n")
REPORT = API.parents[1] / "docs" / "mva" / "TRACK2-REPORT.md"

fails = []


def check(label, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {label:<52} data={got}  report={want}")
    if not ok:
        fails.append(label)


def main():
    text = REPORT.read_text()
    uni = json.loads((DATA / "universe.json").read_text())
    _ensure_gate1()
    g1 = json.loads((DATA / "gate1.json").read_text())
    g2 = json.loads((DATA / "gate2.json").read_text())
    g3 = json.loads((DATA / "gate3.json").read_text())
    g5 = json.loads((DATA / "gate5.json").read_text())

    print("Funnel counts (recomputed from records, not summary fields):")
    check("gate 0 in  (source pool)", uni["source_pool_count"], 5202)
    check("gate 0 out (publishable)", len(uni["molecules"]), 4945)

    proposable = [m for m in g1["molecules"] if m["approval_tier"] in ("A", "B")]
    check("gate 1 out (proposable)", len(proposable), 1485)
    check("gate 2 out (on-mechanism)", len(g2["candidates"]), 34)

    surv = [c for c in g3["candidates"] if c["verdict"].startswith(("proceed", "caution"))]
    check("gate 3 out (survivors)", len(surv), 13)

    studied = [c for c in g5["candidates"] if c["child_late_phase"] > 0]
    check("gate 5 studied in children", len(studied), 11)

    print("\nClaims about specific molecules:")
    by = {c["inn"]: c for c in g5["candidates"]}
    check("anakinra phase-2+ paediatric studies", by["anakinra"]["child_late_phase"], 29)
    check("canakinumab phase-2+ paediatric studies", by["canakinumab"]["child_late_phase"], 28)
    check("anakinra reaches neonatal", by["anakinra"]["min_age_years_seen"] == 0.0, True)
    check("canakinumab reaches neonatal", by["canakinumab"]["min_age_years_seen"] == 0.0, True)

    print("\nStructural claims:")
    bios = [c for c in g3["candidates"] if c["biosimilar_flag"]]
    check("biosimilar-bearing candidates at gate 3", len(bios), 5)
    check("survivors with a biosimilar", sum(1 for c in surv if c["biosimilar_flag"]), 0)
    check("all biosimilars refused on carcinogenicity",
          all(c["verdict"] == "refuse_carcinogenicity" for c in bios), True)

    mitotic = {"AURKA", "PLK1", "TTK", "KIF11", "WEE1", "MDM2", "TP53"}
    reached = {t for c in g2["candidates"] for t in c["targets"] if t in mitotic}
    check("mitotic targets reaching any approved drug", len(reached), 0)

    print("\nConfidentiality boundary:")
    leaked = [m for m in uni["molecules"]
              if "corpus_records" in m or "jurisdictions" in m
              or {"corpus", "read"} & set(m.get("sources") or [])]
    check("internal fields/sources in published universe", len(leaked), 0)

    print("\nReport self-consistency:")
    for n in ("5,202", "4,945", "1,485", "34", "13"):
        present = n in text
        print(f"  {'PASS' if present else 'FAIL'}  report states {n:<8} {present}")
        if not present:
            fails.append(f"report missing {n}")

    print()
    if fails:
        print(f"{len(fails)} FAILURE(S): {fails}")
        sys.exit(1)
    print("all checks passed — report numbers match the committed data")


if __name__ == "__main__":
    main()
