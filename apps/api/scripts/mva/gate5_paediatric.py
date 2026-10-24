#!/usr/bin/env python3
"""Gate 5: paediatric exposure and access, for the candidates that survived Gate 3.

    python3 -m scripts.mva.gate5_paediatric
    python3 -m scripts.mva.gate5_paediatric --write

WHY THIS ORDER. The plan put "access" at Gate 5, but Gate 3 already answered the
access question in the way that matters and inverted it: NONE of the survivors has
a biosimilar, because all five biosimilar-available molecules were refused on
carcinogenicity. So the remaining access question is not "is it cheap" but "has
this drug ever been given to a child at all", which every survivor left open as
`paediatric_evidence: unestablished`. That gap is now the largest one in the
submission, so this gate closes it first.

WHAT IT MEASURES. ClinicalTrials.gov API v2 carries eligibility age per study, so
paediatric exposure can be counted rather than asserted. For each survivor:

  child_studies      interventional studies whose stdAges include CHILD
  child_late_phase   of those, PHASE2/3/4 - i.e. exposure at therapeutic intent
                     rather than a first-in-human safety run
  min_age_seen       the youngest minimumAge across child studies

WHAT THIS IS AND IS NOT. A CHILD-eligible trial is evidence that paediatric dosing
exists and has been studied. It is NOT approval, NOT evidence of safety in THIS
child, and NOT evidence in a chromosomal instability syndrome. It moves a candidate
from "unknown in children" to "studied in children", which is the honest distance
this instrument can travel.

KNOWN NOISE, not silently filtered. `query.intr` matches combination studies, so
"Everolimus and Anakinra ... in Advanced Cancers" counts under anakinra. That
inflates counts for drugs used as add-ons in oncology. The count is a floor on
attention, not a precise exposure measure, and is reported as such.
"""
import argparse, json, pathlib, time, urllib.parse, urllib.request

CTG = "https://clinicaltrials.gov/api/v2/studies"
DATA = pathlib.Path(__file__).resolve().parents[2] / "data" / "mva"
IN, OUT = DATA / "gate3.json", DATA / "gate5.json"
LATE = {"PHASE2", "PHASE3", "PHASE4"}


def fetch(drug, page_size=200):
    params = {"query.intr": drug, "countTotal": "true", "pageSize": str(page_size),
              "fields": "NCTId,Phase,OverallStatus,MinimumAge,StdAge"}
    url = f"{CTG}?{urllib.parse.urlencode(params)}"
    for i in range(3):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return json.loads(r.read())
        except Exception:
            if i == 2:
                raise
            time.sleep(2 ** i)


def years(age):
    if not age:
        return None
    try:
        n, unit = age.split()[0], age.split()[1].lower()
    except (ValueError, IndexError):
        return None
    try:
        n = float(n)
    except ValueError:
        return None
    # ClinicalTrials.gov uses Days/Weeks/Months/Years. Omitting Days made a
    # "1 Day" minimum read as 1.0 YEARS, which understates how young a cohort was.
    if unit.startswith("day"):
        return n / 365.25
    if unit.startswith("week"):
        return n / 52
    if unit.startswith("month"):
        return n / 12
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    surv = [c for c in json.loads(IN.read_text())["candidates"]
            if c["verdict"].startswith(("proceed", "caution"))]
    print(f"{len(surv)} Gate 3 survivors\n")
    print(f"{'drug':<22}{'total':>7}{'child':>7}{'late':>6}  youngest   verdict")

    out = []
    for c in sorted(surv, key=lambda x: x["inn"]):
        d = fetch(c["inn"])
        studies = d.get("studies") or []
        child, late, ages = 0, 0, []
        for s in studies:
            e = (s.get("protocolSection") or {}).get("eligibilityModule") or {}
            if "CHILD" not in (e.get("stdAges") or []):
                continue
            child += 1
            ages.append(years(e.get("minimumAge")))
            ph = ((s.get("protocolSection") or {}).get("designModule") or {}).get("phases") or []
            if set(ph) & LATE:
                late += 1
        seen = [x for x in ages if x is not None]
        youngest = min(seen) if seen else None
        r = dict(c)
        r.update(ctg_total=d.get("totalCount"), child_studies=child,
                 child_late_phase=late,
                 min_age_years_seen=round(youngest, 2) if youngest is not None else None,
                 paediatric_evidence=("studied_in_children" if late
                                      else "child_eligible_early_phase" if child
                                      else "none_found"))
        out.append(r)
        ystr = f"{youngest:.2f}y" if youngest is not None else "-"
        print(f"{c['inn']:<22}{d.get('totalCount',0):>7}{child:>7}{late:>6}  {ystr:<10} {r['paediatric_evidence']}")
        time.sleep(0.3)

    studied = [r for r in out if r["paediatric_evidence"] == "studied_in_children"]
    print(f"\nstudied in children at phase 2+: {len(studied)} of {len(out)}")
    print("  " + ", ".join(sorted(r["inn"] for r in studied)))
    none = [r for r in out if r["paediatric_evidence"] == "none_found"]
    if none:
        print(f"no paediatric study found: {', '.join(sorted(r['inn'] for r in none))}")

    if a.write:
        OUT.write_text(json.dumps(
            {"gate": 5, "source": CTG, "in": len(surv),
             "studied_in_children": len(studied),
             "candidates": sorted(out, key=lambda r: (-r["child_late_phase"], r["inn"]))},
            indent=1) + "\n")
        print(f"wrote {OUT.name}")


if __name__ == "__main__":
    main()
