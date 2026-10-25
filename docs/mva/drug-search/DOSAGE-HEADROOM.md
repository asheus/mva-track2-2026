# The target level already has 610 living examples

A different angle entirely: not a new mechanism, but the use of population genetics to
answer the three questions a therapy actually needs — **what level to aim for, whether
that level is safe, and whether the gene can be moved at all.**

*gnomAD v4 and GTEx v8, retrieved 21 Oct 2026. Producer: `dosage_headroom.py`.*

## The problem with our dosage model

Every therapeutic argument we have made rests on a model whose two ends were borrowed:
a disease threshold from **seven families** (Matsuura 2006) and a dose-response from
**mice** (Baker 2004). Both are small. Neither tells a therapy what level to aim at or
whether arriving there is safe.

That experiment has already been run, at scale, by accident.

## Q1 — Is 50% of BubR1 safe in humans?

gnomAD v4 holds roughly **731,000 people**, depleted of severe pediatric disease. Anyone
carrying one loss-of-function *BUB1B* allele sits near 50% of normal BubR1 for life.

```
  pLI                                 5.5e-17      ~0 -> NOT haploinsufficient
  observed / expected LoF             0.624        (90% CI 0.525 - 0.747)
  LoF variants observed / expected    86 / 137.7

  distinct high-confidence LoF variants      218
  LoF alleles observed (carriers)            610
  LoF HOMOZYGOTES observed                     0
  alleles sampled                     ~1,461,894   (~730,947 people)
```

**About 610 people carry one dead *BUB1B* allele and are not MVA patients.** And **zero**
are homozygous in 731,000 — the floor below is real, exactly as complete BubR1 loss being
incompatible with development would predict.

So 50% is not merely "above threshold." **It is a state humans occupy for a lifetime, at a
sample size no clinical trial will ever reach.**

**The nuance that keeps this honest.** o/e of 0.624 is *not* 1.0 — there is mild depletion,
so heterozygous *BUB1B* loss is not perfectly neutral, and the CI upper bound of 0.747
cannot rule out weak selection. That converges with Sieben 2020, which found mice carrying
**monoallelic** *BubR1* mutations "prone to select MVA-related pathologies later in life."
Two independent lines, population and mouse, saying the same thing: carriers are mostly
fine, not flawlessly fine. The claim is **absence of a severe early phenotype**, never
perfect health — gnomAD is not phenotyped and cannot support more.

## Q2 — Can the locus be moved at all?

If no common variant shifts *BUB1B* expression, every expression-raising strategy is
fighting the gene's own regulation. GTEx says otherwise:

```
  single-tissue eQTL associations     213
  distinct tissues with a signal        7
  independent signals                   8
  |NES| max / median              0.708 / 0.192
```

| rsID | tissue | NES | MAF | distance from TSS |
|---|---|---|---|---|
| rs56282503 | Brain, cerebellar hemisphere | **0.709** | 0.25 | **+114 kb** |
| rs56205728 | Brain, cerebellum | **0.684** | 0.26 | **+114 kb** |
| rs12594280 | Brain, cerebellar hemisphere | −0.405 | 0.33 | −781 kb |
| rs4244573 | Testis | −0.205 | 0.34 | −15 kb |

The two strongest independent signals are **the same distal element ~114 kb from the
transcription start site**, carried by a quarter of the population. The locus is regulated,
not dosage-locked, and the element doing the regulating has coordinates.

**What this does not say.** NES is a slope on normal-quantile-transformed expression, **not
a fold change**, and we deliberately do not convert it into a multiple to set against our
~1.4× requirement — that conversion would be the kind of invented number this project
keeps correcting. And the signals sit in cerebellum, testis and artery, not in a
proliferating cell state. They prove the locus *responds*; they do not prove it responds
where this disease happens.

## What this changes about the pitch

**The goal stops being "correct the mutation" and becomes "reach carrier level."**

That reframing does real work:

- **The endpoint needs no trial to establish as survivable.** ~610 people already live
  there. In a disease with **zero registered trials**, no validated endpoint and no
  trial-sized natural history, that is the only safety claim available that does not
  require enrolling anyone.
- **It bounds the risk from above.** Choi 2009's warning — that too much BubR1 delays
  chromosome segregation — lives *above* normal. Nothing here argues against aiming at
  half of normal.
- **It makes the target modest and concrete.** Not restoration to wild type. Not a cure.
  Move one number from wherever allele 2 leaves it up to a level that 610 people occupy
  safely.
- **The proband's own parents are obligate carriers.** The therapeutic goal, stated
  plainly, is to make the child's cells behave more like their parents' already do.

## How it fits the rest

| question | source | answer |
|---|---|---|
| what level causes disease? | Matsuura 2006, 7 families | below ~50% |
| does the phenotype scale with dose? | Baker 2004, mice | yes, graded |
| what is this genotype's ceiling? | `dosage_model.py` | 50%, and strictly below it |
| **is 50% safe in humans?** | **gnomAD, n≈731,000** | **yes — 610 carriers, 0 homozygotes** |
| **can the locus be moved?** | **GTEx, 213 eQTLs** | **yes — 8 independent signals** |
| by how much must it move? | `dosage_model.py` | ~1.4× if allele 2 retains 70% |

Six rows, five of them now resting on something larger than seven families and a mouse.

The two open questions are unchanged and neither is answered here: **does N1002K actually
reduce abundance** (experiment 1, a western blot), and **does any available agent raise
BubR1 in the cells that matter** (experiment 2). Population genetics cannot answer either.
What it does is make them worth asking — by showing that the level they would aim at is
one that hundreds of people already live at, in a gene that demonstrably responds to
regulation.
