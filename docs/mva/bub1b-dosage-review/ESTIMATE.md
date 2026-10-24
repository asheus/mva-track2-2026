# Estimating this child's BubR1 level without measuring it

> **RETRACTION, 6 Oct 2026 — the therapeutic dose target derived here is withdrawn.**
> The ~2–3× ask brackets against patient MVA-41C at 35% residual BubR1. That patient is
> **731X / Y155C**; 731X is transcript-null, so the whole 35% is Y155C protein, and line 82
> of this file already records Y155C as **"not destabilising"**. That patient therefore has
> MVA at a near-normal protein *level* — their deficit is **functional, not quantitative** —
> so matching their number does not reproduce their state. Level and function are
> independent axes and this bracket conflated them. Line 42 had already written the
> contradiction down ("Y155C is buried and scores high, yet is measured neutral") and the
> estimate used the comparator anyway. The honest ask is larger than 2–3× and is not
> currently well bounded. See `../CORRECTIONS-2026-10-06.md` C6. The level-estimation
> arithmetic below (allele-2 output, NMD of 737X) is unaffected; only the *therapeutic
> target* inferred from the comparator is retracted.


Proband `WGS_EX2312012`, BUB1B **p.Leu737\*** / **p.Asn1002Lys**.

No one has measured his BubR1. This is the closest we can get from published comparators,
with the reasoning exposed so it can be attacked. Reproducible via
`apps/api/scripts/mva/estimate_bubr1_dosage.py`.

## Answer first

| | |
|---|---|
| **Point estimate** | **~17% of normal BubR1** |
| Plausible range | **10–25%** |
| Where that sits | **above** the 6–13% cellular cliff; **at the severe end** of the 17–50% band where MVA actually occurs |
| To reach the milder published comparator | a **~2.1-fold** increase |

## The model

`total BubR1 = allele 1 + allele 2`. Allele 1 is a null. So **the child's entire BubR1
supply comes from N1002K**, and the whole estimate reduces to one question: does that
missense destabilise the protein?

## Allele 1 contributes zero — and this is now computed, not assumed

The premature stop at c.2210 lies **747 nt upstream of the last exon–exon junction**, in
**exon 17 of 23** (computed from Ensembl `ENST00000287598`). The 50–55 nt rule is exceeded
by more than thirteenfold. NMD is predicted with about as much confidence as the rule allows.

It is also *bracketed by two empirically confirmed cases*: 731X sits 766 nt upstream and
753X 700 nt upstream, and both are transcript-null in real patients. This child's stop
falls between them. **Allele 1 = 0.**

## Allele 2 — the calibration, including the part that failed

The literature hands us a calibration set: five kinase-domain substitutions measured as
destabilising (I909T, R814H, L1012P, L844F, R727C) and three measured as not (Q921H,
R550Q, Y155C).

**I first tried to predict class from structure and it did not work.** I computed
solvent accessibility from the AlphaFold model and built a physicochemical disruption
score. It fails: Y155C is buried and scores high, yet is measured neutral. Reporting the
score as if it had worked would have been the easy and wrong thing to do.

The reason it fails is the actual finding: **domain context dominates physicochemistry.**
Y155C is in the TPR domain, and the primary source says abundance falls "most severely
when mutations occurred in or near the kinase domain, but **less** by a mutation in the
N-terminal TPR domain." Once restricted to the only valid comparison — kinase-domain
residues — the picture is clean:

| variant | domain | RSA | pLDDT | measured |
|---|---|---:|---:|---|
| L1012P | kinase | 0.2% | 95.3 | destabilising |
| L844F | kinase | 0.9% | 85.9 | destabilising |
| I909T | kinase | 3.6% | 87.0 | destabilising |
| R727C | near kinase | 6.2% | 88.5 | destabilising |
| R814H | kinase | 16.4% | 90.2 | destabilising |
| **Q921H** | kinase | 1.4% | 83.2 | **tolerated** |
| **N1002K** | **kinase** | **12.9%** | **91.1** | **unknown** |

**Base rate inside the kinase domain: 5 of 6 destabilise (83%).** The paper's own section
heading is "All kinase domain-localized mutations in BUBR1 reduce overall BUBR1 protein
abundance", and the single exception, Q921H, was on the same allele as L844F — the authors
concluded L844F was the causal one.

What separates Q921H from the rest is not burial but **how conservative the swap is**:
Gln→His is +9 Å³ with no formal charge. **N1002K is +54 Å³ and introduces a formal positive
charge at a mostly-buried, confidently-folded site (pLDDT 91.1).** L1012P — the most
destabilising in the set — is ten residues away.

**Conclusion: N1002K is predicted destabilising.** Not proven. Predicted, at a base rate
of 83%, with the physicochemistry pointing the same way.

## The number, from an internal control

This is the step that makes the estimate more than hand-waving. Two published patient lines
share this child's architecture — a null truncation in the 731–753 window plus one missense
— and differ **only** in whether the missense partner destabilises:

| line | genotype | missense partner | BubR1 |
|---|---|---|---:|
| MVA-41C | 731X / Y155C | **not** destabilising | **35%** |
| MVA-12C | 753X / R814H | **destabilising** | **17%** |

That is a controlled two-point comparison sitting inside the literature. A non-destabilising
partner lands near 35%; a destabilising one near 17%.

**This child is architecturally MVA-12C. Point estimate ~17%.**

Cross-check: those two values are figure-derived and quarantined under the review protocol —
but the *text-verified* statement that patient lines run "2–6 fold" below wild-type
converts to 17–50%, which brackets 35% (2.9-fold) and 17% (5.9-fold) exactly. Two
instruments, independent, agreeing.

## Why the range goes down to 10% and not just 17%

The two measurement systems **disagree**, and the disagreement is not in our favour:

- **Patient lines** (native transcription, NMD active): 2–6 fold → 17–50% of diploid.
- **Ectopic LAP-BUBR1** (equalised transcription, NMD bypassed): kinase-domain mutants at
  5–10 fold below wild-type → the missense allele accumulates to 10–20% of a normal
  allele → **5–10% of diploid** once allele 1 is null.

Probably ectopic overexpression saturates chaperone and degradation capacity differently.
The patient lines are the more physiological anchor and are the ones tied to real people.
But the ectopic system is the better-*controlled* measurement of the missense allele in
isolation, and it points lower. Collapsing that to a tidy single number would hide
something clinically material:

> **At ~17% he is above the cellular cliff. At ~10% he is sitting on it.**

That difference is the difference between a cell population that mostly segregates
correctly and one that mostly does not. It is the strongest argument for actually running
the blot.

## What would falsify this

- **A western blot on his fibroblasts or LCLs.** Directly measures the thing being estimated. If it lands outside 10–25%, the model is wrong and should be said so.
- **N1002K stability in an ectopic system**, the assay already used for I909T and L1012P. If N1002K behaves like Q921H rather than R814H, the estimate moves to ~35% and the outlook improves.
- **Cycloheximide-chase plus HSP90 and proteasome inhibition** on his cells — tests the *mechanism*, not just the level, and is the subject of the folding deep-dive.

## What it licenses

A **~2.1-fold** increase in BubR1 would move him from the MVA-12C comparator to the
MVA-41C one. That is the quantitative target any abundance-raising strategy has to clear —
and it is a far more tractable ask than "restore normal levels". Forced overexpression of
the unstable mutants I909T and L1012P to wild-type levels "fully restored" checkpoint
function, so the ceiling is reachable in principle.

**Every number here is inference from other people's cells.** Stated so it can be checked,
and so the one measurement that would replace all of it is unmistakable.
