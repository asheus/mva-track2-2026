# A mitotic-index-controlled assay for BubR1 rescue

Both public screens failed for one structural reason: **BubR1 abundance tracks the cell
cycle so strongly that it swamps any specific pharmacological effect in bulk data.** Of 322
transcript signatures and 11 protein signatures where BubR1 rose, not one survived the
confound control.

The fix is not a better statistical correction. It is an assay whose readout is **blind to
cell-cycle stage by construction**.

*Parameters computed by `scripts/mva/assay_design.py`.*

## The design principle

**Measure mutant and wild-type BubR1 in the same cell and report the ratio.**

That single choice cancels — by construction, not by modelling — every term that defeated
the public screens:

| cancelled | why it matters |
|---|---|
| cell-cycle stage | the confound that killed both screens |
| transcription and translation rate | a compound that slows global synthesis lowers both |
| cell size, ploidy | MVA cells are aneuploid and vary in DNA content |
| well position, plate effects | 384-well screening artefacts |
| illumination, focus, exposure | imaging artefacts |

**A compound that arrests cells in G2/M raises both reporters and leaves the ratio flat.**
It is rejected automatically rather than corrected afterwards.

## Construct

A single bicistronic cassette so both reporters share one promoter and one transcript:

```
   P(weak)  ──  BubR1^N1002K – mNeonGreen  ── P2A ──  BubR1^WT – mScarlet  ── pA
```

- **Weak/physiological promoter** (e.g. PGK or a truncated CMV), not strong CMV.
  Over-expressed BubR1 saturates the quality-control machinery and abolishes exactly the
  difference we are trying to measure. Endogenous-locus knock-in is the gold standard and
  the harder path; the episomal version is what gets built first.
- **P2A, not IRES** — near-stoichiometric translation of both cistrons from one mRNA.
- Tag placement must be tested at both termini: BubR1's regulatory sites sit at **K250**
  (APC/C gating) and **K668** (SIRT2 axis), and a tag that occludes either invalidates the
  readout.

## Cell system

**hTERT-RPE-1**, not HEK293. RPE-1 is near-diploid with an intact spindle assembly
checkpoint. HEK293 is hypotriploid with a compromised checkpoint — an indefensible
background in which to study a checkpoint protein in a chromosome-instability disease.

Hits are then re-tested in **patient-derived fibroblasts**, which carry the real genotype
and the real genetic background.

## Readout

High-content imaging, 384-well:

- **mNeonGreen / mScarlet per-cell ratio** — the primary readout
- **Hoechst DNA content** — bins cells into G1 / S / G2-M
- **phospho-histone H3 (Ser10)** — separates true mitosis from G2

Cell-cycle stage is still measured, not because the ratio needs correcting, but to
**verify** that the ratio is stage-independent. If it is not, the construct is wrong.

## The five controls, and what each one would catch

**1 · Confound control — the one that matters.** Nocodazole, or **Ro-3306**. Ro-3306 is a
CDK1 inhibitor that arrests cells at the G2/M boundary, and it is the compound that scored
**obs/exp 5.26** in the public proteomics screen — a confound with a known, measured
signature. It must raise **both** reporters and leave the ratio **unchanged**. If the ratio
moves under Ro-3306, the assay has a stage artefact and is not fit for purpose.

**2 · Null control.** WT-mNeonGreen / WT-mScarlet — the same protein with both tags. The
ratio must be flat at 1.0 across every condition and every cell-cycle bin. This catches
fluorophore maturation differences, photobleaching, and tag-induced instability, and it
calibrates the small departure from stoichiometry that P2A leaves behind.

**3 · Tag swap.** Run mutant-mNeonGreen/WT-mScarlet **and** mutant-mScarlet/WT-mNeonGreen.
If a hit flips with the tags, it is an artefact of the fluorophores, not of BubR1.

**4 · Rescue-positive control.** Brief proteasome inhibition (MG132). If the mutant is
preferentially degraded, this raises the ratio. **If MG132 does not move the ratio, either
the mutant is not proteasome-degraded or the assay cannot detect rescue** — and in either
case nothing else from the plate should be believed.

**5 · Calibration ladder, pre-registered.** Three variants, with the order fixed in advance
by our ThermoMPNN predictions:

| variant | ΔΔG | predicted |
|---|---|---|
| N1002S | +0.944 | least destabilised |
| N1002R | +1.419 | **indistinguishable from K** (Δ 0.088 kcal/mol) |
| N1002K | +1.507 | most destabilised |

The assay passes calibration if **S sits above K and R in abundance, and K and R sit
together**. If **K and R separate**, the folding model is wrong and the defect is
ubiquitination at the new lysine — the same falsification the bench experiment was already
designed to deliver, now built into the screen's own controls.

## Power

The design target is set by the dosage model: allele 2 needs about **1.43×**, so the assay
must resolve a **43%** change in ratio — not a two-fold change.

| per-cell CV | cells per well for Z′ ≥ 0.5 |
|---|---|
| 25% | 49 |
| 40% | 125 |
| 60% | 281 |
| **80%** (pessimistic) | **499** |

High-content imaging routinely yields 1,000–5,000 cells per 384-well. **The requirement is
met even under pessimistic assumptions**, which is the main reason this assay is worth
building rather than merely proposing.

## Compound library — bake the viability gate into the screen

Screen **approved drugs only** (Prestwick, NCATS Pharmaceutical Collection, or an
FDA-approved Selleck set — roughly 1,500–3,000 compounds). Our own ranking already
established that an approach which cannot reach a patient does not compete, so a screen
restricted to approved agents makes **every hit actionable by construction**. It also keeps
the plate count small enough for one person.

Arimoclomol and an NAD⁺ precursor go on the plate as named candidates, not as a separate
experiment.

## Secondary readouts, both of which our own analysis made mandatory

**Half-life, by HaloTag pulse-chase or cycloheximide chase.** The ratio says abundance
changed; this says whether **degradation rate** changed, which is the mechanism we claim.

**Mitotic timing, by live imaging (NEBD to anaphase).** This is not optional. Choi 2009
showed an undegradable BubR1 markedly delays chromosome segregation, so **a hit that raises
the ratio while extending mitosis is a failure, not a success.** The acceptance criterion is
therefore a conjunction: *ratio up **and** mitotic timing unchanged*.

A tertiary readout, in hits only: **micronucleus frequency**, as the first look at whether
raising BubR1 actually reduces mis-segregation.

## Failure modes, named in advance

| risk | mitigation |
|---|---|
| over-expression saturates quality control and flattens the difference | weak promoter; knock-in version as the follow-up |
| tag occludes K250 or K668 regulation | test both termini; tag-swap control |
| P2A stoichiometry is not exactly 1:1 | the WT/WT null control calibrates the offset |
| RPE-1 does not reflect patient tissue | re-test hits in patient fibroblasts |
| a hit raises BubR1 by arresting cells | rejected by construction; Ro-3306 verifies |

## What this assay does not do

- **It says nothing about allele 1.** p.Leu737Ter leaves no protein to measure, and no
  compound found here can reach it. The 280 transcript-less alleles in our map stay out of
  reach.
- **It is not a therapy.** A hit is a lead that would still need the patient's own cells,
  then a mechanistic biomarker, then an n-of-1 — the order the Li-Fraumeni study validated.
- **It measures a tagged, episomal construct**, not endogenous BubR1 in a child.

## Why it is worth building anyway

It is the one experiment that the two failed screens actually specify. Public compendia
cannot answer this question — not because the data are poor, but because **bulk measurement
of a cell-cycle gene cannot separate regulation from mitotic index**. An internal
ratiometric control separates them by construction, the power requirement is met at
realistic variance, and the calibration ladder tests a prediction we committed to before
running anything.

And it carries its own refutation: if Ro-3306 moves the ratio, or MG132 does not, the assay
is wrong and says so on the same plate.
