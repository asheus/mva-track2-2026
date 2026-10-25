# How each candidate would actually work on p.Asn1002Lys

Reasoning from the physical defect outward. One step below corrects a claim I made in
`DECISION.md`.

## The defect, stated physically

What we computed about residue 1002:

- **buried** — relative solvent accessibility **13.9%**
- the wild-type asparagine **donates an acceptor contact**: OD1 to the backbone nitrogen
  of **Trp978**, at 2.83 Å
- the substitution puts a **+1 charge** and **+54.5 Å³** into that buried position
- the nearest charged neighbour is **Arg999 at 6.95 Å — also positive**, so the local field
  is repulsive rather than compensating (signed burden +0.047 e/Å)

Three independent penalties, all acting on the same quantity:

1. **Desolvation.** Burying a lysine ε-amino group costs the free energy of stripping its
   hydration shell. That cost is normally paid by pairing with a buried counter-charge.
   Here there is none — the nearest charge is like-signed.
2. **Lost hydrogen bond.** Lysine's NZ is a donor only. It cannot replace an *acceptor*
   contact, so the OD1→Trp978 bond is not substituted, it is deleted.
3. **Sterics.** +54.5 Å³ in a packed interior.

None of this breaks the protein. It **shifts an equilibrium**:

```
   native  ⇌  partially unfolded  ⇌  unfolded
                      │
                      ├── exposed hydrophobic surface → chaperone recognition
                      └── exposed degron → quality-control ubiquitination → proteasome
```

The mutant spends more time in states where quality control can see it. That is the whole
defect, if hypothesis A is right.

## The equation everything acts on

```
   [BubR1]steady  =        k_synthesis
                     ───────────────────────────────
                     k_quality-control  +  k_scheduled
```

where `k_scheduled` is the **ordered, signal-driven** destruction of correctly folded
BubR1 by APC/C–Cdc20 at anaphase — the event that must keep happening — and
`k_quality-control` is the **conformation-triggered** disposal of misfolded protein, which
is the pathological term we want to reduce.

**Those are two different routes to the proteasome.** Separating them is what makes a
therapy possible at all: the goal is to lower `k_QC` without touching `k_scheduled`.

## 1 · Arimoclomol — raise the refolding capacity

**Chain.** Arimoclomol is a hydroxylamine derivative that acts as a **co-inducer** of the
heat shock response: it does not switch HSF1 on by itself, it **prolongs and amplifies HSF1
activation in cells that are already under proteostatic stress**. Active HSF1 transcribes
HSPA1A/B (HSP70) and its DNAJ co-chaperones. More HSP70 means a partially unfolded BubR1 is
more likely to be captured, held, and returned to native than triaged for destruction.

**Where it acts in the equation.** It lowers `k_QC` by pulling flux back out of the
misfolded pool. It does not inhibit the proteasome and does not touch APC/C–Cdc20, so
`k_scheduled` is unchanged. **The anaphase destruction still fires on time.**

**Why this gene may be unusually favourable for a co-inducer.** A co-inducer needs existing
HSF1 tone to amplify; in an unstressed cell it does little. MVA cells are **aneuploid**, and
aneuploidy produces proteotoxic stress through stoichiometric imbalance of proteins encoded
on mis-segregated chromosomes. So the target cells plausibly carry elevated HSF1 tone
already — the condition a co-inducer requires. That is a mechanistic argument *for* this
drug in *this* disease, and it is testable in patient fibroblasts before anything else.

**What would make it fail.** If N1002K BubR1 is not a chaperone client — if it folds fine
and is lost some other way — more HSP70 changes nothing.

## 2 · 4-phenylbutyrate — and why its mechanism may not transfer

**Chain.** 4-PBA is a short-chain fatty acid whose amphipathic character lets it coat
exposed hydrophobic surfaces on partially folded proteins, reducing aggregation and
shifting the folding equilibrium toward native.

**The problem, which the attractive precedent hides.** Most of 4-PBA's evidence base is
**ER protein folding** — CFTR above all, a membrane protein folded in the ER, where 4-PBA
also acts by relieving the unfolded protein response. **BubR1 is a soluble nuclear and
cytosolic protein. It is not an ER client, and the UPR arm of 4-PBA's mechanism is simply
not available here.**

Add the confound we already recorded — 4-PBA is a weak HDAC inhibitor, and HDAC inhibition
is unpredictable for BubR1 because K250 acetylation stabilises it while K668 acetylation
destabilises it — and 4-PBA is **mechanistically the weakest of the three**, despite having
the most attractive clinical precedent. The MCAD missense trial is the right shape and the
wrong compartment.

## 3 · NAD⁺ precursor — and a correction to what I said

**Chain.** NMN or NR feeds the salvage pathway to raise NAD⁺. NAD⁺ is the obligate
co-substrate of the sirtuins. **SIRT2 deacetylates BubR1 at Lys668**, and the deacetylated
state is the stable one; the acetyltransferase CBP opposes it. So raising NAD⁺ raises SIRT2
activity, lowers acetyl-K668, and extends BubR1 half-life.

**The correction.** In `DECISION.md` I wrote that the NAD⁺ route is "the only one of the
four whose mechanism of action and principal risk are the same event," because it works by
slowing the destruction that releases anaphase. **That conflated two different switches.**

- **K250** acetylation, written by PCAF, **blocks APC/C–Cdc20** degradation — that is the
  scheduled, anaphase-releasing route (Choi 2009).
- **K668** acetylation, written by CBP and removed by SIRT2, is a **separate** stability
  determinant, and nothing in North 2014 identifies APC/C–Cdc20 as the ligase acting on it.

They are different sites with opposite signs on different routes. So raising NAD⁺ acts on
the K668 axis, **not demonstrably on the anaphase axis**, and the conflict I asserted is
weaker than I claimed.

**What survives of the concern.** Net abundance still rises, and the question that remains
is whether the scheduled destruction can still clear the larger pool on time. That is a
quantitative worry, not a mechanistic contradiction — and it is exactly why mitotic timing
has to be measured alongside abundance. The obligation stands; the reasoning behind it was
overstated.

**Net effect on the ranking:** this *partially rehabilitates* NAD⁺ against arimoclomol.
Arimoclomol still has the cleaner separation — it provably does not touch either
degradation route — but NAD⁺'s disadvantage is smaller than I said.

## 4 · The combination — and an imperfect analogy

**Chain.** A folding agent lowers the flux *into* the misfolded pool; a degradation
modulator lowers the clearance *of* what still misfolds. Different steps, so the effects on
steady state should compound rather than overlap.

**Where the CFTR analogy holds and where it does not.** It holds in the lesson that single
agents failed and a combination was approved. It does **not** hold in kind: CFTR's corrector
and potentiator act on **folding** and on **channel gating** — two different properties.
Our combination would act on folding and on degradation, which are two steps in **one**
property, abundance. Non-redundant, but a weaker form of orthogonality than Trikafta's.

## For contrast, the blocked approaches, in the same terms

- **trans-RNA** raises `k_synthesis` — more protein made per transcript. Different term of
  the equation entirely, and the only one of the four that would work even if the mutant
  folds perfectly.
- **Trans-splicing** removes the variable: the corrected message encodes wild-type protein,
  so `k_QC` returns to normal because there is nothing abnormal to recognise. That is why it
  ranks first on mechanism and nowhere on viability.

## What this reasoning predicts, and how it fails

If hypothesis A (folding) holds, then **arimoclomol and 4-PBA should act and NAD⁺ should
also act** — all three lower the denominator. If the protein folds normally and is lost by
a site-specific route instead, **the chaperone arm does nothing and only the NAD⁺ arm can
work.**

So the mechanisms are not merely different stories about the same drug choice. **They make
divergent predictions in the same experiment** — the one the N1002R lane settles. A
chaperone cannot rescue a protein that was never misfolded.
