#!/usr/bin/env python3
"""What trans-splicing efficiency would this genotype need to reach carrier level?

    python3 -m scripts.mva.transsplice_model

WHY THIS CHANGES SOMETHING WE HAD SETTLED. We concluded that allele 1 (p.Leu737Ter) is
unreachable, because its PTC sits 748 nt upstream of the last junction and nonsense-
mediated decay destroys the message before a readthrough agent can act on it.

That reasoning is correct for readthrough and WRONG for trans-splicing, for a reason worth
stating precisely: **NMD acts on mature mRNA, after export and a first round of
translation. Trans-splicing acts on pre-mRNA, in the nucleus, before any of that.** The
pre-mRNA from allele 1 is present and normal; only its spliced product is destroyed. A
trans-splicing molecule that replaces the 3' portion carrying the PTC yields an mRNA with
no PTC at all, which then escapes decay entirely.

So trans-splicing is the one modality on our list that can reach the dead allele. That
matters more here than it would in a simple haploinsufficiency, because allele 1 currently
contributes zero: every percent of efficiency buys protein that does not exist today.

THE MODEL. Trans-splicing is mutation-agnostic -- it replaces a 3' segment regardless of
what mutation that segment carried -- so it acts on both alleles' pre-mRNA at the same
efficiency e:

    allele 1:  0.5 * e                      corrected copies escape NMD; the rest are lost
    allele 2:  0.5 * (e + (1-e) * f2)       corrected copies are wild type; the rest stay N1002K
    total   =  0.5 * (2e + (1-e) * f2)

with f2 the unmeasured output of allele 2, swept as in dosage_model.py. Setting total >= 0.5
(carrier level -- the state ~610 gnomAD carriers occupy, per dosage_headroom.py) gives

    e  >=  (1 - f2) / (2 - f2)

WHY CARRIER LEVEL IS THE RIGHT BAR. Not because it is a cure, but because it is the only
endpoint in this disease whose safety needs no trial to establish: hundreds of people live
there, and none of them has MVA.

WHAT THIS IS NOT. An efficiency requirement is not an efficiency. SMaRT's chronic problem
is precisely the ratio of trans- to cis-splicing, and published PTMs frequently fall far
below the bar computed here. This script states the target a real molecule would have to
clear; it says nothing about whether one does.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
OUT = ROOT / "docs/mva/data/transsplice_model.json"
TARGET = 0.50
SWEEP = [1.00, 0.85, 0.70, 0.55, 0.40, 0.25]


def total(e, f2):
    return 0.5 * (2 * e + (1 - e) * f2)


def main():
    print("REQUIRED TRANS-SPLICING EFFICIENCY TO REACH CARRIER LEVEL (50% of normal)\n")
    print("  allele 1  p.Leu737Ter   contributes 0 today; pre-mRNA is intact, so it is")
    print("                          correctable even though its mRNA is destroyed")
    print("  allele 2  p.Asn1002Lys  contributes f2, unmeasured (experiment 1)\n")
    print(f"  {'if allele 2 delivers':<22}{'total today':>13}{'efficiency needed':>20}"
          f"{'total at that e':>18}")
    print("  " + "-" * 72)
    rows = []
    for f2 in SWEEP:
        need = (1 - f2) / (2 - f2)
        rows.append({"allele2_output": f2, "total_today": total(0.0, f2),
                     "efficiency_needed": need, "total_at_that_efficiency": total(need, f2)})
        print(f"  {f2:>8.0%}              {total(0.0,f2):>12.1%}{need:>19.1%}"
              f"{total(need,f2):>18.1%}")
    print("  " + "-" * 72)

    print("\nWHAT THE BAR LOOKS LIKE")
    print("  Roughly 23-38% across the plausible range of allele 2. That is a demanding")
    print("  number for spliceosome-mediated trans-splicing, whose central difficulty is")
    print("  exactly this ratio -- but it is a number, and it is not 90%.")

    print("\n  Two features of THIS genotype make the bar lower than it would otherwise be:")
    print("   1. Allele 1 sits at zero, so corrected copies are pure gain rather than")
    print("      replacement of something already working.")
    print("   2. Trans-splicing is mutation-agnostic, so one molecule acts on both alleles")
    print("      and the two contributions add.")

    print("\nWHY TRANS-SPLICING AND NOT A circRNA THAT JUST MAKES THE PROTEIN")
    print("  A circular RNA encoding BubR1 would supply protein directly and durably, and")
    print("  that is the wrong property here. Choi 2009 showed that stabilising BubR1")
    print("  beyond its normal window markedly DELAYS chromosome segregation: this protein")
    print("  has to rise and fall with the cell cycle, not simply be present. Trans-splicing")
    print("  corrects the endogenous transcript and leaves the gene's own regulation intact,")
    print("  which for BUB1B is a safety requirement rather than an elegance. The CTNNB1")
    print("  work makes the same argument for the same reason -- dosage sensitivity.")

    print("\nWHAT WOULD FALSIFY THE PREMISE")
    print("  If allele 1's pre-mRNA is not actually available for trans-splicing -- for")
    print("  instance if the locus is transcriptionally silenced rather than merely")
    print("  NMD-targeted -- the allele-1 term is zero at every efficiency and the bar")
    print("  rises to what a single-allele correction demands. Allele-specific pre-mRNA")
    print("  quantification in patient cells settles that, and should precede any PTM design.")

    OUT.write_text(json.dumps({
        "model": "total = 0.5*(2e + (1-e)*f2); e = trans-splicing efficiency",
        "target": TARGET,
        "target_rationale": "carrier level; ~610 gnomAD heterozygous LoF carriers occupy "
                            "it with no severe early phenotype (dosage_headroom.py)",
        "key_asymmetry": "NMD acts on mature mRNA; trans-splicing acts on pre-mRNA, so "
                         "allele 1 is correctable although it is unreachable by readthrough",
        "rows": rows,
        "efficiency_range_needed": [min(r["efficiency_needed"] for r in rows[1:]),
                                    max(r["efficiency_needed"] for r in rows)],
        "caveat": "a required efficiency is not an achieved one; SMaRT's chronic "
                  "limitation is the trans- to cis-splicing ratio",
        "precedent": {"gene": "CTNNB1", "doi": "10.1016/j.omtn.2025.102680",
                      "why": "dosage-sensitive haploinsufficiency treated by SMaRT, "
                             "chosen explicitly as a mutation-agnostic approach that "
                             "preserves endogenous gene regulation"},
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
