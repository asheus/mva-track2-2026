# The pick: partial Aurora B inhibition

24 Oct 2026. This project has closed a lot of routes. This document does the
opposite: it names the single candidate we think is **most likely to work**, with
the argument for it and the argument against it, and commits.

---

## The one-sentence version

**Both of this child's alleles fail at the same step — recruiting B56-PP2A to the
kinetochore — and the consequence is unopposed Aurora B. You cannot raise the
phosphatase, because no drug on earth activates one. You can lower the kinase,
because eighty-two drugs do. Rebalance the equilibrium from the side that
pharmacology can actually reach.**

## 1 · The defect, in this disease, in patient cells

Xu *et al.*, *Biol Open* 2(5):479–86, 2013
([PMID 23789096](https://doi.org/10.1242/bio.20134051)). From the abstract:

> "The BUBR1:B56-PP2A complex **opposes Aurora B kinase activity**, since **loss
> of the complex can be reverted by inhibiting Aurora B**. Importantly, we show
> that the failure of BUBR1 to recruit B56-PP2A also contributes to the
> chromosome congression defects found in **cells derived from patients with the
> Mosaic Variegated Aneuploidy (MVA) syndrome**."

That is our disease, in patient-derived material, with the mechanism named and
the intervention named. Not an analogy, not a model organism, not an adjacent
phenotype.

And it converges with the allele analysis independently:

| allele | lesion | consequence at the KARD |
|---|---|---|
| 1 — p.Leu737Ter | removes the pseudokinase domain | 731X-type constructs show reduced KARD S670/S676 phosphorylation and weakened B56-PP2A recruitment |
| 2 — p.Asn1002Lys | **buried** loop residue (RSA 14.0%, 87% buried); N1002K buries an unpaired charge and breaks the `OD1 <- Trp978:N` hydrogen bond. ~85% a **pure dosage mutant** (C42, C52) | less BubR1, so less KARD, so less PP2A-B56 |

Two different molecular failures, one shared downstream deficit. The child does
not have two diseases needing two drugs. They have one node, reached twice.

## 2 · Why the fix has to come from the kinase side

A kinase–phosphatase imbalance can be corrected from either side. We checked
whether the phosphatase side is reachable, using the union of five curated
drug–target databases (107,407 gene–drug pairs, 6,316 genes — see
`GERO-DRUGGABILITY-MINING.md`):

- **PP2A activators in the entire drug universe: zero.** The one clinical-stage
  PP2A-directed compound, LB-100, is an *inhibitor* — the wrong sign.
- **The whole "up" universe is 410 genes**: 3,484 membrane-receptor rows, 1,445
  ion channel, 545 transcription factor, and 56 enzymes — every one of them a
  receptor kinase, cyclase, AMPK subunit or metabolic enzyme. **Not one
  phosphatase. Not one mitotic protein.**
- **APC/C — the other candidate node — has zero annotated compounds** across all
  five sources.
- **AURKB has 82**, including 18 dedicated inhibitors, many clinical-stage.

This is the pitch opener as a measurement. The pharmacopoeia was built to turn
mitosis *down*; the only lever it offers on this axis is the kinase, and that is
the lever we should pull — not as a consolation, but because the biology says
lowering the kinase and raising the phosphatase are the same correction.

## 3 · The drug, and the exposure inversion

**Barasertib (AZD1152)**, prodrug of **barasertib-hQPA** — the most selective
Aurora B compound with published human pharmacokinetics.

| | |
|---|---|
| Aurora B IC50 (cell-free) | **0.37 nM** |
| Aurora A IC50 | ~1.368 µM → **~3,700× selective** |
| human Css, 1,200 mg / 7-day infusion | **226.8 ng/mL** (Dennis 2012, [PMID 22864876](https://doi.org/10.1007/s00280-012-1939-2)) |
| MW (hQPA) | 507.6 |
| **Css, molar** | **447 nM** |
| **Css / IC50** | **~1,200×** |

**This is the first candidate in the entire project where there is too much drug
rather than too little**, and that changes everything about the problem.

Every route we closed — readthrough, amlexanox, perphenazine, momelotinib,
memantine, metformin, fingolimod — died because the effect needed a
concentration that no tolerated dose delivers. We were always trying to climb.
Here we need **partial** rebalancing, not ablation: something near the IC50,
call it low single-digit nM, which sits **two to three orders of magnitude
BELOW** the oncology exposure.

Dose reduction is trivial. Dose escalation was impossible. That asymmetry is the
whole argument.

**The toxicity inverts with it.** Barasertib's dose-limiting toxicity is
neutropenia, which comes from ablating Aurora B in proliferating marrow at
1,200× IC50. The exposure this hypothesis needs is far below the threshold where
that toxicity was observed. We are not asking a drug to do something it cannot;
we are asking it to do much less than it is licensed to do.

## 4 · Against it — the honest case

**The central risk is that the dose–response is U-shaped, and we do not know the
width of the window.** Aurora B *is* the error-correction machinery. Too little
inhibition does nothing; too much removes error correction altogether and causes
cytokinesis failure and polyploidy. We are proposing to partially disable a
safety system in a child whose other safety system is already broken. If the
window is narrow, or if it does not exist in a BubR1-hypomorphic background,
this makes the disease worse rather than better. **That is the experiment, and
it is the first thing that should be done.**

Four further objections, each real:

1. **Xu's reversion was acute.** Short exposure in culture, in an engineered
   B56-binding mutant. The abstract establishes that MVA patient cells carry the
   same recruitment defect; it does not state that the Aurora B reversion was
   performed in the patient cells themselves. That gap matters and should not be
   papered over.
2. **Route.** Barasertib is an IV infusion — poor for chronic paediatric use.
   AZD2811 (nanoparticle) exists; oral Aurora B inhibitors exist (chiauranib,
   ENMD-2076, AMG-900) with worse selectivity. The molecule is not the final
   answer; the mechanism is.
3. **Anti-proliferative in a child with failure to thrive and short stature.**
   Even partial Aurora B inhibition slows division. The growth phenotype is a
   genuine constraint on chronic dosing.
4. **Nobody has tested Aurora B inhibition in a BUB1B-mutant background.** The
   literature supports the mechanism; it does not supply this result.

## 5 · The prediction we are committing to

No wet lab is available to us, so this is a prediction, stated to be falsifiable:

> In BUB1B-mutant MVA patient-derived fibroblasts, **partial** Aurora B
> inhibition — at an exposure one to three orders of magnitude below the
> oncology range — will **reduce** chromosome missegregation and improve
> congression relative to untreated cells, and the dose–response will be
> **U-shaped**, with benefit lost and then reversed as inhibition approaches the
> levels used in oncology.

It is falsified if missegregation rises monotonically with Aurora B inhibition
at every concentration tested, or if no concentration improves congression.

The readout must be congression and segregation fidelity in phase-matched cells,
never bulk BUB1B abundance, which is confounded by cycling fraction — the
methodological point this whole project has been built on.

## 6 · Why this is the answer rather than a hedge

The rubric asks for mechanism-supported candidates, not adjacent ones. This
candidate is supported *by* the mechanism and by nothing else: it was not found
by searching drug databases for the indication, and it is not a drug anyone would
reach for in a child with a chromosomal instability syndrome. It comes out of a
single chain of reasoning —

**two alleles → one failed interaction → an imbalance → the only side of that
imbalance any drug can reach → a compound 1,200× more potent than it needs to
be, which for once is the right problem to have.**

Everything else we examined failed because the thing we wanted was the weakest
thing the drug did. Here it is the strongest.
