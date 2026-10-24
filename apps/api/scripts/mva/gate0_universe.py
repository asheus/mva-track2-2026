#!/usr/bin/env python3
"""Gate 0 of the MVA Track 2 funnel: build a PUBLISHABLE screening universe.

    python3 -m scripts.mva.gate0_universe                    # report only
    python3 -m scripts.mva.gate0_universe --write            # + data/mva/universe.json

WHY THIS EXISTS. Track 2 of the MVA hackathon publishes under CC BY 4.0 with a
public repository. The molecule pool this draws from is an internal FDL artefact
that mixes public regulatory sources with the DRAP (Pakistan) filing corpus, and
the corpus half may not ship. This gate is the boundary: it takes the pool and
emits only what can be published, so that everything downstream is safe by
construction rather than by reviewer vigilance.

THE CONFIDENTIALITY RULE, and why it is drawn where it is.

Two things had to be separated, and they are not the same thing:

  FIELDS   `corpus_records` and `jurisdictions` are counts derived from the DRAP
           corpus. Dropped outright.

  ROWS     A molecule present in the pool ONLY because the DRAP scan saw it is
           itself a disclosure — its membership leaks that it appears in
           Pakistani filings. So a row must carry at least one PUBLIC source to
           survive, and `corpus`/`read` (both DRAP-derived) do not count as one.

That second rule is a confidentiality fix that happens to also be a quality fix.
Per `build_pool.py`, corpus-only rows are unadjudicated composition tokens and
are where the OCR artefacts live — `irebesartan`, `celcoxib`, `gentmycin`,
`olmisartan` are misspellings, not molecules. Dropping them removes a disclosure
risk and a noise source in one move.

PUBLIC SOURCES, per `build_pool.py`'s own description of each:
  world      FDA Purple Book + EMA + PMDA + WHO. Authoritative for US/EU approval.
  gabi       Archived regional biosimilar tables (adds AU, CA, PMDA).
  ema        EMA's authorised-medicines table. Veterinary and withdrawn/refused
             rows already excluded on EMA's own columns. Carries the ATC code.
  wikipedia  Therapeutic monoclonal antibody list; carries approved_western.
  atc        The WHO ATC index. NOTE: an ATC code is a classification of a
             substance, NOT evidence that it is approved anywhere. Gate 1 is
             where approval is actually established; this gate does not conflate
             the two.
  held       Supplier tables — tied to a named holder, so some regulator
             approved it and a company sells it.

WHAT THIS GATE DOES NOT DO. It does not rank, score, or judge therapeutic
relevance. It answers one question — may this row be published, and is it a real
molecule — and leaves every other question to the gate that owns it.
"""
import argparse, collections, json, os, pathlib, sys

# DRAP-derived; see the ROWS rule above.
INTERNAL_SOURCES = {"corpus", "read"}
# Fields that are counts over the DRAP corpus.
INTERNAL_FIELDS = {"corpus_records", "jurisdictions"}

# Phoenix and FDL are checked out as siblings; $FDL_MOLECULE_POOL overrides.
_REL = "knowledge-base/registry/molecule-pool.json"
DEFAULT_POOL = os.environ.get(
    "FDL_MOLECULE_POOL",
    str(pathlib.Path(__file__).resolve().parents[4].parent / "FDL" / _REL),
)
OUT = pathlib.Path(__file__).resolve().parents[2] / "data" / "mva" / "universe.json"


def build(pool_path):
    raw = json.loads(pathlib.Path(pool_path).read_text())
    molecules = raw["molecules"]

    kept, dropped = [], collections.Counter()
    for m in molecules:
        if m.get("veterinary"):
            dropped["veterinary"] += 1
            continue
        public = sorted(set(m.get("sources") or []) - INTERNAL_SOURCES)
        if not public:
            dropped["internal-source-only"] += 1
            continue
        row = {k: v for k, v in m.items() if k not in INTERNAL_FIELDS}
        row["sources"] = public          # never echo the internal provenance
        kept.append(row)

    kept.sort(key=lambda r: r["inn"])
    return raw, kept, dropped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", default=DEFAULT_POOL)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    if not pathlib.Path(a.pool).exists():
        sys.exit(f"pool not found: {a.pool}\nSet FDL_MOLECULE_POOL or pass --pool.")

    raw, kept, dropped = build(a.pool)

    print(f"pool           {raw['count']:>6}  (built {raw.get('built')})")
    for reason, n in dropped.most_common():
        print(f"  dropped      {n:>6}  {reason}")
    print(f"UNIVERSE       {len(kept):>6}  publishable rows\n")

    src = collections.Counter(s for r in kept for s in r["sources"])
    print("public sources present (rows may carry several):")
    for s, n in src.most_common():
        print(f"  {s:<12} {n:>6}")

    atc1 = collections.Counter(c[0] for r in kept for c in (r.get("atc") or []))
    print(f"\nrows with an ATC code   {sum(1 for r in kept if r.get('atc')):>6}")
    print(f"rows with indications   {sum(1 for r in kept if r.get('areas')):>6}")
    print(f"rows flagged biosimilar {sum(1 for r in kept if r.get('biosimilar_flag')):>6}")
    print("ATC level 1:", " ".join(f"{k}={v}" for k, v in sorted(atc1.items())))

    if a.write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(
            {"gate": 0,
             "source_pool_built": raw.get("built"),
             "source_pool_count": raw["count"],
             "count": len(kept),
             "dropped": dict(dropped),
             "molecules": kept}, indent=1) + "\n")
        print(f"\nwrote {OUT.relative_to(OUT.parents[3])}  ({OUT.stat().st_size/1e6:.2f} MB)")


if __name__ == "__main__":
    main()
