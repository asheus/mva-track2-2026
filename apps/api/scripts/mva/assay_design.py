#!/usr/bin/env python3
"""Power and feasibility parameters for the mitotic-index-controlled BubR1 assay.

    python3 -m scripts.mva.assay_design

Both public screens failed for the same structural reason: BubR1 abundance tracks the cell
cycle so strongly that it swamps any specific pharmacological effect in bulk data. The fix
is not a better statistical correction. It is an assay whose readout is **blind to
cell-cycle stage by construction**.

This computes the numbers that decide whether such an assay is practical: how large an
effect it must resolve, how many cells per well that needs, and what the ordering of our
own ThermoMPNN predictions implies for calibration.
"""
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
OUT = ROOT / "docs/mva/data/assay_design.json"

REQUIRED_FOLD = 1.43        # dosage_model.py: allele 2 at 70% needs 1.43x to reach 50%
DDG = {"N1002S": 0.944, "N1002R": 1.419, "N1002K": 1.507}   # ddg_analysis.py
RT = 0.616                  # kcal/mol at 310 K


def cells_for_zprime(effect, cv, target_z=0.5):
    """Cells per well so that well-level means separate at Z' >= target.

    Z' = 1 - 3(sd_pos + sd_neg)/|mean_pos - mean_neg|. With equal CV in both arms and
    well means over n cells, sd_well = cv/sqrt(n). Solving for n.
    """
    allowed = (1 - target_z) * effect / 6.0        # per-arm sd, as a fraction of the mean
    if allowed <= 0:
        return None
    return math.ceil((cv / allowed) ** 2)


def main():
    print("=" * 84)
    print("1  WHAT EFFECT MUST BE RESOLVED")
    print("=" * 84)
    print(f"   dosage model: allele 2 needs ~{REQUIRED_FOLD:.2f}x to reach carrier level")
    print(f"   so the assay must reliably separate a {(REQUIRED_FOLD-1)*100:.0f}% change")
    print("   in the mutant-to-wild-type ratio. That is the design target, not 2-fold.")

    print("\n" + "=" * 84)
    print("2  CELLS PER WELL, for Z' >= 0.5")
    print("=" * 84)
    print(f"   {'per-cell CV':>12}{'cells needed':>15}   note")
    for cv in [0.25, 0.40, 0.60, 0.80]:
        n = cells_for_zprime(REQUIRED_FOLD - 1, cv)
        note = ("comfortable for high-content imaging" if n <= 2000
                else "needs flow cytometry" if n <= 20000 else "impractical")
        print(f"   {cv:>12.0%}{n:>15,}   {note}")
    print("\n   High-content imaging routinely yields 1,000-5,000 cells per 384-well.")
    print("   Even at a pessimistic 80% per-cell CV the requirement is met.")

    print("\n" + "=" * 84)
    print("3  CALIBRATION LADDER, pre-registered from our own ddG predictions")
    print("=" * 84)
    print("   If the assay measures stability, it must reproduce this ORDER. Converting")
    print("   ddG to an expected abundance ratio assumes degradation scales with the")
    print("   unfolded fraction, which is a strong assumption -- so the ORDER is the test,")
    print("   not the magnitudes.")
    print(f"\n   {'variant':<10}{'ddG (kcal/mol)':>16}{'rank':>7}")
    for v, d in sorted(DDG.items(), key=lambda x: x[1]):
        print(f"   {v:<10}{d:>16.3f}{sorted(DDG.values()).index(d)+1:>7}")
    gapKR = DDG["N1002K"] - DDG["N1002R"]
    gapKS = DDG["N1002K"] - DDG["N1002S"]
    print(f"\n   K - R = {gapKR:.3f} kcal/mol  -> predicted INDISTINGUISHABLE")
    print(f"   K - S = {gapKS:.3f} kcal/mol  -> predicted clearly separated")
    print("   So the assay passes calibration if S sits above K and R, and K and R sit")
    print("   together. If K and R separate, the folding model is wrong -- which is the")
    print("   same falsification the bench experiment was already designed to deliver.")

    print("\n" + "=" * 84)
    print("4  WHY A RATIO, AND NOT A CORRECTION")
    print("=" * 84)
    print("   Measuring mutant and wild-type BubR1 in the SAME cell and taking the ratio")
    print("   cancels, by construction rather than by modelling:")
    for x in ["cell-cycle stage", "transcription and translation rate", "cell size",
              "well position and plate effects", "illumination and focus",
              "compound effects on general protein synthesis"]:
        print(f"     - {x}")
    print("\n   A compound that arrests cells in G2/M raises BOTH reporters and leaves the")
    print("   ratio flat. That is the entire point: the confound that defeated both public")
    print("   screens is rejected automatically instead of being corrected afterwards.")

    OUT.write_text(json.dumps({
        "design_target_fold": REQUIRED_FOLD,
        "cells_per_well": {f"cv_{int(cv*100)}": cells_for_zprime(REQUIRED_FOLD-1, cv)
                           for cv in [0.25, 0.40, 0.60, 0.80]},
        "zprime_target": 0.5,
        "calibration_ladder_ddg": DDG,
        "predicted_order": [v for v, _ in sorted(DDG.items(), key=lambda x: x[1])],
        "K_minus_R": round(gapKR, 3), "K_minus_S": round(gapKS, 3),
        "ratio_cancels": ["cell-cycle stage", "synthesis rate", "cell size",
                          "plate effects", "imaging variation", "global translation"],
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
