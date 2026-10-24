#!/usr/bin/env python3
"""Which already-safe drugs raise BUB1B transcript, in public perturbation data?

    python3 -m scripts.mva.bub1b_drug_screen

THE IDEA, which is a good one. Our problem is a shortfall of about 1.4x in BubR1. If some
compound already given to humans happens to raise BUB1B -- off-target, by accident, as a
side effect of something else -- it would clear the viability gate before we started.
Public drug-perturbation expression data can be asked that question directly.

THE TRAP THAT MAKES A NAIVE ANSWER WORTHLESS. BUB1B is a cell-cycle gene. Its transcript
rises whenever a larger fraction of cells is in G2/M -- which happens with any compound
that arrests cells in mitosis, and with anything that increases proliferation. A plain
search for "drugs that raise BUB1B" returns mitotic poisons, and a mitotic poison is the
last thing to give a child with a chromosome-instability syndrome.

So every hit is scored against a **mitotic module** of twenty co-regulated genes. For a
gene set of size N drawn from a background of G genes, the number of panel members expected
by chance is panel_size * N/G. Observed-over-expected near 1 means BUB1B came up without
its module -- which is the only interesting case. Observed-over-expected well above 1 means
the compound moved the cell cycle, and BUB1B went along for the ride.

FOUR INDEPENDENT SOURCES, because one is an anecdote:
  LINCS_L1000_Chem_Pert_Consensus_Sigs   consensus per compound, L1000 assay
  RummaGEO_DrugPerturbations_2025        GEO RNA-seq, which is what was actually asked for
  Sciplex_Drug_Perturbation_Signatures   single-cell RNA-seq
  Drug_Perturbations_from_GEO_up         older GEO compendium
A compound appearing in several of these is worth more than its rank in any one.

WHAT THIS CANNOT ESTABLISH, and it matters here. These are **transcript** measurements. Our
defect is at the protein level: p.Asn1002Lys makes mRNA normally and is predicted to be
destabilised afterwards. Raising transcript raises the synthesis term and would help --
steady state is synthesis over degradation -- but a transcript hit is a lead, not a
mechanism, and it is not evidence that the protein rises.
"""
import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
LIB = ROOT / "docs/mva/data/lincs"
OUT = ROOT / "docs/mva/data/lincs/bub1b_drug_screen.json"
GENE = "BUB1B"
BACKGROUND = 20000

def load_mitotic_panel():
    """MSigDB Hallmark G2-M Checkpoint + Mitotic Spindle, minus BUB1B itself.

    A hand-picked 20-gene panel had no statistical power here: for a 245-gene signature
    the expected overlap is 0.25, so observing none is unsurprising and says nothing. A
    ~390-gene module makes the expected overlap 4.8 for a LINCS set and ~30 for a RummaGEO
    set, which is enough for absence to be informative.
    """
    f = LIB / "MSigDB_Hallmark_2020.txt"
    panel = set()
    for line in f.read_text(errors="ignore").split("\n"):
        if not line.strip():
            continue
        parts = line.split("\t")
        if parts[0].strip() in {"G2-M Checkpoint", "Mitotic Spindle"}:
            panel |= {g.split(",")[0].strip().upper() for g in parts[1:] if g.strip()}
    panel.discard(GENE)
    return panel


MITOTIC = None

LIBS = ["LINCS_L1000_Chem_Pert_Consensus_Sigs", "RummaGEO_DrugPerturbations_2025",
        "Sciplex_Drug_Perturbation_Signatures_2025", "Drug_Perturbations_from_GEO_up"]


def is_up(term, lib):
    t = term.upper()
    if lib == "Drug_Perturbations_from_GEO_up":
        return True
    if t.endswith(" DN") or t.endswith(" DOWN"):
        return False
    return t.endswith(" UP") or " UP " in t or t.endswith("_UP")


def drug_name(term, lib):
    t = re.sub(r"\s+(UP|DN|DOWN)$", "", term.strip(), flags=re.I)
    if lib == "Sciplex_Drug_Perturbation_Signatures_2025":
        t = re.sub(r"^\S+\s+", "", t)                      # strip cell line
        t = re.sub(r"\s+\d+(\.\d+)?(NM|UM|MM)\s+\d+H$", "", t, flags=re.I)
    if lib == "RummaGEO_DrugPerturbations_2025":
        t = re.sub(r"^GSE\S+\s+\d+\s+V\s+\d+\s+", "", t)
        t = re.sub(r"\s+(HUMAN|MOUSE|RAT)$", "", t, flags=re.I)
    if lib == "Drug_Perturbations_from_GEO_up":
        t = re.sub(r"\s+(DB\d+|\d{4,})\s+.*$", "", t)
    return t.strip().upper()


def main():
    global MITOTIC
    MITOTIC = load_mitotic_panel()
    print(f"mitotic module: {len(MITOTIC)} genes "
          f"(Hallmark G2-M Checkpoint + Mitotic Spindle, BUB1B removed)\n")
    rows, per_lib_bg = [], {}
    for lib in LIBS:
        f = LIB / f"{lib}.txt"
        if not f.exists():
            print(f"  missing {f.name} -- skipped", file=sys.stderr)
            continue
        hits, allup, panel_frac_bg = 0, 0, []
        for line in f.read_text(errors="ignore").split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            term, genes = parts[0], {g.split(",")[0].strip().upper()
                                     for g in parts[1:] if g.strip()}
            if not is_up(term, lib):
                continue
            allup += 1
            n = len(genes)
            if n == 0:
                continue
            obs = len(genes & MITOTIC)
            exp = len(MITOTIC) * n / BACKGROUND
            panel_frac_bg.append(obs / exp if exp > 0 else 0)
            if GENE not in genes:
                continue
            hits += 1
            rows.append({"library": lib, "term": term, "drug": drug_name(term, lib),
                         "set_size": n, "mitotic_observed": obs,
                         "mitotic_expected": round(exp, 2),
                         "obs_over_exp": round(obs / exp, 2) if exp > 0 else None})
        import statistics as st
        per_lib_bg[lib] = {"up_sets": allup, "bub1b_hits": hits,
                           "median_obs_over_exp_all_sets":
                               round(st.median(panel_frac_bg), 2) if panel_frac_bg else None}
        print(f"  {lib:<46} up-sets {allup:>6}  BUB1B hits {hits:>4}")

    print(f"\n{'='*96}\nTHE CONFOUND, QUANTIFIED\n{'='*96}")
    for lib, b in per_lib_bg.items():
        print(f"  {lib:<46} median mitotic obs/exp across ALL up-sets: "
              f"{b['median_obs_over_exp_all_sets']}")
    oe = [r["obs_over_exp"] for r in rows if r["obs_over_exp"] is not None]
    import statistics as st
    print(f"\n  Across the {len(rows)} BUB1B-containing sets, median mitotic obs/exp is "
          f"{st.median(oe):.2f}")
    print("  If that is well above 1, most hits are cell-cycle signatures, not BUB1B-specific.")

    # POWER. obs/exp = 0 is only informative if the set was big enough that we EXPECTED
    # to see panel genes. For a 245-gene LINCS set, expected is 0.245, and seeing none has
    # Poisson probability 0.78 -- it means nothing. So a hit counts as BUB1B-specific only
    # where expected >= 2, i.e. where absence of the module is actually surprising.
    import math
    for r in rows:
        e = r["mitotic_expected"]
        r["powered"] = e >= 2.0
        r["p_at_most_observed"] = (
            round(sum(math.exp(-e) * e**k / math.factorial(k)
                      for k in range(r["mitotic_observed"] + 1)), 4) if e > 0 else None)
    specific = sorted([r for r in rows if r["powered"] and r["obs_over_exp"] is not None
                       and r["obs_over_exp"] <= 2.0],
                      key=lambda r: (r["obs_over_exp"], -r["set_size"]))
    powered = [r for r in rows if r["powered"]]
    print(f"\n{'='*96}\nHITS WHERE BUB1B ROSE WITHOUT ITS MODULE\n{'='*96}")
    print(f"  Of {len(rows)} BUB1B-containing sets, only {len(powered)} are large enough")
    print(f"  for the absence of the mitotic module to be meaningful (expected >= 2).")
    print(f"  {len(specific)} of those {len(powered)} have obs/exp <= 2.")
    print(f"\n  {'drug':<40}{'library':<22}{'size':>6}{'mitotic obs/exp':>18}")
    for r in specific[:25]:
        print(f"  {r['drug'][:38]:<40}{r['library'][:20]:<22}{r['set_size']:>6}"
              f"{r['obs_over_exp']:>18.2f}")

    print(f"\n{'='*96}\nCROSS-LIBRARY: drugs seen raising BUB1B in more than one source\n{'='*96}")
    bydrug = collections.defaultdict(set)
    for r in rows:
        bydrug[r["drug"]].add(r["library"])
    multi = sorted([(d, libs) for d, libs in bydrug.items() if len(libs) >= 2],
                   key=lambda x: -len(x[1]))
    print(f"  {len(multi)} drugs appear in >=2 independent libraries")
    for d, libs in multi[:25]:
        sp = [r for r in rows if r["drug"] == d and r["obs_over_exp"] is not None]
        med = st.median([r["obs_over_exp"] for r in sp]) if sp else None
        print(f"  {d[:44]:<46} {len(libs)} libs   median mitotic obs/exp {med}")

    OUT.write_text(json.dumps({
        "question": "does any already-safe drug raise BUB1B transcript?",
        "confound": "BUB1B is a cell-cycle gene; anything that arrests cells in G2/M or "
                    "raises proliferation raises it. Every hit is scored against a "
                    "20-gene mitotic module, observed over expected for the set size.",
        "mitotic_panel": sorted(MITOTIC),
        "per_library": per_lib_bg,
        "n_bub1b_sets": len(rows),
        "median_mitotic_obs_over_exp_in_hits": st.median(oe) if oe else None,
        "specific_hits": specific[:60],
        "multi_library_drugs": [{"drug": d, "libraries": sorted(l)} for d, l in multi[:60]],
        "limit": "transcript, not protein. Our defect is post-translational, so a "
                 "transcript hit raises the synthesis term but is not evidence the "
                 "protein rises.",
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
