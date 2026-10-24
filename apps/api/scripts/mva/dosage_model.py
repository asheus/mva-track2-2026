#!/usr/bin/env python3
"""How much functional BubR1 does this genotype make, and how much rescue is needed?

    python3 -m scripts.mva.dosage_model

WHY THIS IS A SCRIPT AND NOT A SENTENCE. Asked "what fraction of normal BubR1 does the
proband make", the tempting answer is a single number. There isn't one, because exactly
one input is unmeasured: how much functional protein allele 2 delivers. Writing "about
35%" would be inventing that input and hiding it inside a conclusion.

So this computes the whole curve instead, with the unknown named and exposed. What comes
out is more useful than a point estimate: it shows how far below the disease threshold the
genotype sits for any value of the unknown, and therefore **how large a rescue would have
to be** -- which turns out to be the load-bearing number for choosing a modality.

THE MODEL. Two alleles, each contributing at most half of normal output:

    total = 0.5 * f1 + 0.5 * f2

where f is functional protein output relative to one wild-type allele.

  f1 = 0  for p.Leu737Ter. Justified twice over, which is why it is fixed and not
          swept: (a) the PTC sits 748 nt upstream of the last exon-exon junction, far
          past the ~50 nt boundary, so the transcript is a canonical NMD substrate
          (ptc_context.py); (b) even for transcript that escapes decay, a protein
          terminating at residue 737 of 1,050 lacks the entire pseudokinase domain
          (766-1050) and the CENP-E interface (1031-1050), so it is not functional
          BubR1 by any reading. Both routes give zero, so f1 = 0 is not an assumption
          that could reasonably be relaxed.

  f2 = unknown for p.Asn1002Lys. This is the swept parameter and the thing experiment 1
       measures. Our map predicts it is < 1 (reduced abundance: buried residue, new
       buried charge, lost H-bond acceptor to Trp978) but puts no number on it, because
       the axis behind that prediction is validated in three other proteins and NOT in
       this one.

THE THRESHOLD, from the literature rather than from us. Matsuura et al. studied seven
families with this disease and concluded that "> 50% decrease in expression (or activity)
of BubR1 is involved in the PCS syndrome" (Am J Med Genet A 2006,
doi:10.1002/ajmg.a.31069) -- i.e. disease appears below roughly half of normal. The same
paper restored normal BubR1 levels and normal mitotic behaviour in patient cells by
transferring a chromosome 15, which is the strongest existing evidence that the defect is
a dosage defect and that correcting dosage corrects the cell.

THE RESULT THAT MATTERS. Because allele 1 contributes nothing, this genotype's ceiling is
50% -- precisely the threshold. The child is affected, so f2 < 1 and the true value is
below it. The gap to close is therefore the shortfall, not a doubling, and the required
fold-increase printed below is small for any plausible f2. A modality that raises BubR1
abundance by tens of percent is in range; nothing needs to invent a new allele.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
OUT = ROOT / "docs/mva/data/dosage_model.json"

F1 = 0.0                      # p.Leu737Ter, justified in the docstring
THRESHOLD = 0.50              # Matsuura 2006: disease below ~50% of normal
SWEEP = [1.00, 0.85, 0.70, 0.55, 0.40, 0.25]


def total(f1, f2):
    return 0.5 * f1 + 0.5 * f2


def main():
    rows = []
    print("PREDICTED FUNCTIONAL BubR1 FOR THE PROBAND'S GENOTYPE")
    print("  allele 1  p.Leu737Ter   f1 = 0.00  (NMD substrate; truncation removes the")
    print("                                      pseudokinase domain 766-1050)")
    print("  allele 2  p.Asn1002Lys  f2 = swept (unmeasured -- this is experiment 1)")
    print(f"\n  disease threshold from the literature: below {THRESHOLD:.0%} of normal")
    print("\n  if allele 2 delivers      total functional      vs threshold      "
          "fold-increase in allele 2\n  (fraction of one WT)      BubR1 (% of normal)"
          "                        needed to reach it")
    print("  " + "-" * 94)
    for f2 in SWEEP:
        t = total(F1, f2)
        need = THRESHOLD / t if t > 0 else float("inf")
        verdict = "AT threshold" if abs(t - THRESHOLD) < 1e-9 else "below"
        rows.append({"allele2_output_fraction": f2, "total_fraction_of_normal": t,
                     "relation_to_threshold": verdict,
                     "fold_increase_in_allele2_needed": round(need, 2)})
        print(f"  {f2:>6.0%}                    {t:>6.1%}                "
              f"{verdict:<13s}     {need:>5.2f}x")
    print("  " + "-" * 94)

    print("\nWHAT THIS SAYS")
    print("  The ceiling is 50% because one allele contributes nothing -- which is")
    print("  exactly the threshold the literature identifies. The proband is affected,")
    print("  so allele 2 delivers less than a full wild-type allele's worth and the true")
    print("  value lies strictly below 50%.")
    print("\n  The therapeutic consequence: the gap to close is the shortfall, not a")
    print("  doubling. Even at the pessimistic end of the sweep the required increase in")
    print("  allele 2's output is a small multiple, which is the range a drug that raises")
    print("  BubR1 abundance could plausibly reach.")

    print("\nWHAT WOULD FALSIFY THE WHOLE FRAME")
    print("  If experiment 1 finds N1002K abundance NORMAL (f2 = 1), this genotype sits")
    print("  AT 50% and the defect is not abundance but function -- the abundance arm")
    print("  dies and a checkpoint-activity assay replaces it. The model is built so that")
    print("  outcome is visible rather than absorbed.")

    OUT.write_text(json.dumps({
        "model": "total = 0.5*f1 + 0.5*f2, f = functional output per allele vs wild type",
        "allele1": {"hgvs_p": "p.Leu737Ter", "f": F1,
                    "justification": [
                        "PTC 748 nt upstream of the last exon-exon junction -> canonical "
                        "NMD substrate (ptc_context.py)",
                        "truncation at 737/1050 removes the pseudokinase domain (766-1050) "
                        "and the CENP-E interface (1031-1050)"]},
        "allele2": {"hgvs_p": "p.Asn1002Lys", "f": "unmeasured; swept",
                    "our_prediction": "reduced (<1) -- buried residue, new buried charge, "
                                      "lost H-bond acceptor to Trp978",
                    "prediction_status": "axis validated in PTEN/TPMT/NUDT15, NOT in BUB1B"},
        "threshold": {"value": THRESHOLD,
                      "source": "Matsuura et al., Am J Med Genet A 2006, "
                                "doi:10.1002/ajmg.a.31069",
                      "quote": ">50% decrease in expression (or activity) of BubR1 is "
                               "involved in the PCS syndrome"},
        "ceiling_is_the_threshold": True,
        "sweep": rows,
        "falsifier": "f2 = 1 (normal abundance) would move the defect from abundance to "
                     "function and retire the abundance arm",
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
