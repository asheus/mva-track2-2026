#!/usr/bin/env python3
"""Does any safe drug raise BubR1 PROTEIN, in public mass-spectrometry data?

    python3 -m scripts.mva.bub1b_proteomics_screen

WHY THIS IS THE RIGHT LAYER. The transcript screen (DRUG-SCREEN.md) found nothing, and was
always aimed past the lesion: p.Asn1002Lys makes mRNA normally and is predicted to be
destabilised AFTER translation. Protein abundance is where the defect lives, so
drug-perturbation proteomics asks the question directly.

SOURCE. Proteomics Drug Atlas 2023 via Enrichr -- 1,747 drug signatures measured by mass
spectrometry, covering 8,220 proteins.

THE SAME CONFOUND, AND THE SAME CONTROL. BubR1 protein also rises with mitotic index, so a
compound that arrests cells in G2/M raises it without doing anything useful. Every hit is
scored against the MSigDB Hallmark G2-M Checkpoint + Mitotic Spindle module.

TWO CORRECTIONS THE TRANSCRIPT SCREEN TAUGHT US, both applied here from the start:
  - the background is the number of proteins the assay MEASURED (8,220), not a nominal
    20,000 genes, and the panel must be intersected with that background before expected
    overlap is computed. Using the wrong background inflates or deflates every score.
  - a specificity test needs power. With ~149-protein signatures and a panel of this size,
    expected overlap is around 6, so observing few panel members is genuinely informative.

THE ASYMMETRY IS ITSELF A RESULT. 52 drugs lower BubR1 protein and only 11 raise it. A
protein that is easy to lower and hard to raise is what the biology predicts -- BubR1 is
actively degraded on a schedule -- and it sets expectations for any therapy aimed at
raising it.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
LIB = ROOT / "docs/mva/data/lincs"
OUT = LIB / "bub1b_proteomics_screen.json"
GENE = "BUB1B"
ATLAS = "Proteomics_Drug_Atlas_2023"


def read_lib(name):
    sets = {}
    for line in (LIB / f"{name}.txt").read_text(errors="ignore").split("\n"):
        if not line.strip():
            continue
        p = line.split("\t")
        sets[p[0]] = {g.split(",")[0].strip().upper() for g in p[1:] if g.strip()}
    return sets


def panel():
    out = set()
    for line in (LIB / "MSigDB_Hallmark_2020.txt").read_text(errors="ignore").split("\n"):
        p = line.split("\t")
        if p and p[0].strip() in {"G2-M Checkpoint", "Mitotic Spindle"}:
            out |= {g.split(",")[0].strip().upper() for g in p[1:] if g.strip()}
    out.discard(GENE)
    return out


def main():
    sets = read_lib(ATLAS)
    background = set().union(*sets.values())
    MIT = panel() & background          # only what this assay could have measured
    print(f"{ATLAS}: {len(sets)} signatures, {len(background)} proteins measured")
    print(f"mitotic module: {len(panel())} genes, {len(MIT)} of them detectable here\n")

    up = {t: g for t, g in sets.items() if t.strip().lower().endswith(" up")}
    dn = {t: g for t, g in sets.items() if t.strip().lower().endswith(" down")}
    up_hits = {t: g for t, g in up.items() if GENE in g}
    dn_hits = {t: g for t, g in dn.items() if GENE in g}
    print(f"BubR1 protein DOWN in {len(dn_hits)} drug signatures")
    print(f"BubR1 protein UP   in {len(up_hits)} drug signatures")
    print(f"  -> {len(dn_hits)/max(len(up_hits),1):.1f}x easier to lower than to raise\n")

    rows = []
    for t, genes in sorted(up_hits.items()):
        n = len(genes)
        obs = len(genes & MIT)
        exp = len(MIT) * n / len(background)
        drug = re.sub(r"\s+up$", "", t.strip(), flags=re.I)
        rows.append({"drug": drug, "set_size": n, "mitotic_observed": obs,
                     "mitotic_expected": round(exp, 2),
                     "obs_over_exp": round(obs / exp, 2) if exp else None})
    rows.sort(key=lambda r: r["obs_over_exp"] if r["obs_over_exp"] is not None else 99)

    print("=" * 92)
    print("EVERY DRUG THAT RAISES BubR1 PROTEIN, scored against the mitotic confound")
    print("=" * 92)
    print(f"  {'drug':<22}{'proteins':>9}{'mitotic obs':>13}{'expected':>10}{'obs/exp':>9}   reading")
    for r in rows:
        oe = r["obs_over_exp"]
        read = ("BubR1-specific" if oe is not None and oe <= 1.0 else
                "mixed" if oe is not None and oe <= 2.0 else "CELL-CYCLE SIGNATURE")
        print(f"  {r['drug'][:20]:<22}{r['set_size']:>9}{r['mitotic_observed']:>13}"
              f"{r['mitotic_expected']:>10.1f}{oe:>9.2f}   {read}")

    clean = [r for r in rows if r["obs_over_exp"] is not None and r["obs_over_exp"] <= 1.0]
    print(f"\n  {len(clean)} of {len(rows)} raise BubR1 without raising the mitotic module.")

    # cross-check against the other proteomics library
    try:
        other = read_lib("ProteomicsDB_2020")
        oh = {t for t, g in other.items() if GENE in g}
        print(f"\n  ProteomicsDB_2020 contains BUB1B in {len(oh)} sets "
              f"(tissue/cell-line expression, not drug perturbation -- no overlap expected)")
    except Exception:
        pass

    OUT.write_text(json.dumps({
        "source": ATLAS, "signatures": len(sets), "proteins_measured": len(background),
        "mitotic_panel_detectable": len(MIT),
        "bub1b_down_signatures": len(dn_hits), "bub1b_up_signatures": len(up_hits),
        "up_hits": rows,
        "bub1b_specific": [r["drug"] for r in clean],
        "caveats": ["one dataset, no independent replication of any single drug",
                    "cell lines, not patient tissue",
                    "an up-call is a direction, not a magnitude -- nothing here says "
                    "whether the rise approaches the ~1.4x this genotype needs",
                    "a drug that raises wild-type BubR1 need not raise a destabilised "
                    "mutant, which is degraded for a different reason"],
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
