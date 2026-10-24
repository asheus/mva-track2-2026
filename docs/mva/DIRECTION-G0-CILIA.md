# The direction we named and never worked: MVA as a ciliopathy, and a G0 assay

*Opened 23 Oct 2026. This is a research direction, not a candidate recommendation.*

## Why this is the strongest unworked direction

`TRACK2-PLAN.md` lists an "Arm C — ciliopathy", cites a **review** (Miyamoto & Matsuura
2015, Oncotarget), points it at HDAC6 inhibitors as a generic ciliogenesis-promoting route,
and goes no further. `TRACK2-REPORT.md` mentions a "ciliopathy axis" twice in passing.
**The word "G0" appears nowhere in this repository.** The primary paper and its mechanism
were never engaged.

According to PubMed, that primary paper is Miyamoto et al. 2011, *Hum Mol Genet*
([PMID 21389084](https://doi.org/10.1093/hmg/ddr090)), titled *"Insufficiency of BUBR1, a
mitotic spindle checkpoint regulator, causes impaired ciliogenesis in vertebrates."* From the
abstract, verbatim where it matters:

- *"BUBR1 is essential for the primary cilium formation, and ... the PCS (MVA) syndrome is
  thus a **novel ciliopathy**."*
- *"Patients with the syndrome often develop Dandy-Walker complex and **polycystic
  kidneys**; implying a critical role of BUBR1 in morphogenesis."*
- The mechanism: *"BUBR1 is required for ubiquitin-mediated proteasomal degradation of
  **CDC20 in the G0 phase** and maintains **APC/C–CDH1** activity that regulates the optimal
  level of **dishevelled** for ciliogenesis."*
- Medaka `bubr1` knockdown gave ciliary dysfunction, cerebellar defects and perturbed
  left–right asymmetry.

## 1 · It dissolves the measurement problem that killed everything else

Every instrument in this project has broken on one confound. `DRUG-SCREEN.md`: a plain search
for drugs that raise `BUB1B` returns mitotic poisons, because arresting cells in mitosis
raises the bulk signal. `ASSAY-DESIGN.md`: of 322 transcript and 11 protein signatures where
BubR1 rose, **not one survived the confound control**, and the fix had to be an assay "blind
to cell-cycle stage by construction" — ratiometric internal controls, mitotic-index gating,
Ro-3306 arrest controls. The Edison single-cell bundle put the RNA swing at roughly **2.2×
across the cycle** (median TPM 22.06 G1 → 47.91 G2/M).

**A G0 ciliation assay has no cycling fraction to confound.** Serum-starve into quiescence,
score percent ciliated cells. The confound is not corrected for; it is absent by
construction. That is a stronger position than anything `ASSAY-DESIGN.md` could engineer.

## 2 · It is a functional readout, which is what C48 says we now need

**C48** established, from Sieben 2019, that *"BUBR1 allelic effects beyond protein level and
aneuploidy contribute to disease heterogeneity"* — mice with comparable total BubR1 had
different phenotypes — and that total abundance is therefore unsafe as a sole target variable
or endpoint. Ciliation is a function, not an abundance. It measures the thing C48 says we
should be measuring instead of a Western band.

## 3 · The rescue is already demonstrated in a cell line we already cite

Matsuura's chromosome-15 transfer into patient cells is the centrepiece of our own argument
that this child's cells are correctable — we cite it for restored BubR1, kinetochore
localisation and mitotic behaviour. The same corrected line reportedly restored ciliation.
So the positive control exists and has been run.

**Numbers to check before use.** A third-party report read Miyamoto's ciliation figures as
roughly **1–4% in patient cells versus ~30% in controls**. The abstract does not state those
percentages, so they are **unverified** and must be read off the paper's figures before
appearing anywhere. If they hold, the dynamic range is 7–30×, against the 2–6-fold protein
differences and per-cell segregation-error rates our mitotic assays have to work with.

## 4 · The non-obvious part: it offers a target *downstream* of the lesion

This project has spent its entire length trying to raise BubR1, and failing — no approved
agent, a 0-of-757 fragment screen, two null drug screens, a demoted NAD⁺ arm, a chaperone
lead whose magnitude was borrowed. Miyamoto's mechanism offers somewhere else to stand:

    BubR1 insufficiency  →  CDC20 accumulates in G0  →  APC/C–CDH1 activity falls
                         →  dishevelled mis-set  →  no cilium

Each arrow after the first is a node that does not require raising BubR1 at all.

**And there is a safety asymmetry worth noticing.** `APPROACHES-ALL.md` rejected APC/C–Cdc20
inhibition with "arrests every mitosis", which is correct — for *mitotic* CDC20. But the
ciliary lesion is **CDC20 excess in G0**, in cells that are not dividing. Lowering CDC20 in a
quiescent compartment is a different perturbation in a different cell state from inhibiting it
in mitosis, and apcin — which targets the CDC20 D-box pocket and which our report already
discusses — has its central liability only where there is a spindle. The thing we rejected may
be usable precisely because the target compartment is not cycling.

That is a hypothesis about exposure, not a guarantee, and it is the first thing to attack.

## What this does not do, stated plainly

- **It does not address the cancer risk.** Restoring a cilium does nothing about aneuploidy,
  missegregation, or the rhabdomyosarcoma this child has already had. Those remain the
  life-threatening features and this direction does not touch them. At best this is an
  endpoint for the growth, renal and developmental features.
- **It only partially unifies the renal phenotype.** Miyamoto reports *polycystic kidneys*;
  this child has *nephrocalcinosis*. A cilia defect predicts cysts, not calcification, which
  is exactly the gap a third-party analysis identified in arguing for a second renal
  diagnosis. The cilia link makes renal involvement in MVA published and mechanistic; it does
  not explain mineral deposition.
- **Dishevelled has an "optimal level"**, per the paper's own wording. So this is a window,
  not a monotone target, and over-correction may be as harmful as the deficit. Any
  intervention needs a dose–response, not a direction.
- **Fibroblast ciliation may not reflect renal tubular ciliation**, and G0 fibroblasts are not
  a developing kidney.
- **A quiescent cell eventually re-enters the cycle.** A G0-restricted intervention is only
  G0-restricted for as long as the cell stays there.

## The first three experiments, cheapest first

1. **Read Miyamoto's figures** and record the actual ciliation percentages, the cell lines,
   the starvation protocol and the n. Everything above depends on them and none of it should
   be written up until they are in a committed query.
2. **Reproduce the ciliation deficit in this child's cells** against a healthy control and,
   if obtainable, the chromosome-15-corrected line. Percent ciliated, G0-arrested, blinded,
   independent cultures as replicates. This is the positive control for every screen that
   follows and it is a few plates and an imaging session.
3. **Measure G0 CDC20 and APC/C–CDH1 activity** in the same cells. If CDC20 is not elevated in
   this child's quiescent cells, the downstream-target argument in §4 fails immediately and
   cheaply, which is the point of running it third rather than last.

Only if all three hold does screening modalities against ciliation make sense — and at that
point every parked arm (chaperone, NAD⁺, NMD inhibition, readthrough, E3 inhibition) can be
screened against a confound-free readout with a real dynamic range, which is the thing this
project has never had.
