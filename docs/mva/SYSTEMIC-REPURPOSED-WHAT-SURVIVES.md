# Systemic + repurposed: what actually survives

*23 Oct 2026. The constraint set: **approved**, **systemically delivered**, viable in **this**
child.*

> **Assumption declared once, and used throughout.** The clinical record is eight HPO
> terms. It establishes that **rhabdomyosarcoma occurred** (HP:0002859, "the presenting
> oncological event that triggered urgent investigation") and **contains no treatment data
> whatsoever** — no agent, no regimen, no dates, no risk group, no response. Where this
> document reasons about cytotoxic exposure, marrow reserve or survivorship it is reasoning
> **under the assumption that an RMS was treated**, which is standard practice but is *not*
> in the record and is not established for this child. Corrected 23 Oct 2026 (**C50**); the
> earlier text asserted it. The other constraints — nephrocalcinosis from birth, systemic
> growth restriction, spindle-checkpoint deficit — are record-supported or genotype-derived.

## The headline, stated plainly

**No approved systemic drug modifies this disease.** Everything in this workstream that would
have raised BubR1 has now failed, and each failure is measured rather than assumed:

| Route | Why it is closed | Where |
|---|---|---|
| Readthrough (aminoglycosides, ataluren, DAP, ELX-02) | realistic ceiling **+0.53 percentage points** of BubR1; aminoglycoside oto/nephrotoxicity against nephrocalcinosis | `WHICH-ALLELE-TO-TARGET.md` |
| NMD inhibition (amlexanox) | **free Cmax 0.11–0.29 µM.** 90–900× short of the 25–100 µM at which the TBK1/TFEB separation is reported, and a claimed 0.4 µM activity that would have narrowed this to ~1.4–3.6× **could not be traced to any indexed paper** (C51). Still closed: fed 50→100 mg buys 1.47×, and the oral product was withdrawn 2017 | `ALLELE1-APPROVED-DRUGS.md`, **C51** |
| SIRT2 / NAD⁺ | K250 hazard retained (the mitigating citation is untraceable); CPTAC protein-level association reverses on lineage adjustment | **C49**, `TRIAGE-EDISON-BUNDLES.md` |
| Chaperone (arimoclomol) | magnitude was borrowed and withdrawn; HSF1 is itself a tumour-supportive programme; the measured folding axis for this mutation class is **HSP90**, not HSP70 | **C47**, safety-seat F2 |
| 4-PBA | HDAC liability; renal tubular acidosis hazard against nephrocalcinosis; **no carcinogenicity data** | **C5**, safety-seat F4 |
| HSP90 inhibitors | would strip this child's entire BubR1 supply | standing refusal |
| Direct BubR1 binders | **0 of 757** fragments at 1% FPR; predicted ATP-pocket druggability 0.006–0.071 | §3.4 |
| Proteasome inhibition | not viable chronically in a child; protein retention ≠ functional rescue | §3.3 |

## The two traps that look perfect and are not

Both satisfy "approved + oral + chronic + paediatric" better than anything we propose. Both
must be refused on mechanism, and for the same reason.

**Colchicine.** Inhibits NMD below 0.4 µM; approved; decades of chronic paediatric dosing in
FMF. It is a **microtubule destabiliser** — an anti-mitotic — and this child's disease *is* a
spindle-checkpoint defect. Its NMD activity is most likely a consequence of the cytoskeletal
disruption that disqualifies it.

**Givinostat (Duvyzat).** FDA-approved March 2024, oral twice daily, DMD, **ages 6 and up** —
genuinely chronic paediatric systemic dosing, and it is precisely what `TRACK2-PLAN.md`'s
Arm C (ciliopathy) nominated. It is a **pan-HDAC inhibitor**, and three independent lines say
that is the wrong direction here:

1. **C5** — HDAC inhibition phenocopies premature chromatid separation; it points *at* the
   disease.
2. **DepMap 23Q4** — low-`BUB1B` models are **more**, not less, HDAC3-dependent (adjusted
   slope +0.057/SD, q = 0.046).
3. **Li 2017** ([PMID 28935703](https://doi.org/10.1242/dev.153353)) — HDAC3 catalytic
   activity is required for spindle microtubule stability and kinetochore–microtubule
   attachment; knockdown blocked oocytes at metaphase I.

Plus thrombocytopenia on label — which matters more if the RMS was treated, per the
assumption above.

**The pattern worth naming:** a filter of "approved + systemic + chronic paediatric" surfaces
both of these first. That filter is insufficient on its own in a chromosome-instability
syndrome, because the agents with the best chronic-paediatric credentials are
disproportionately ones that perturb the cytoskeleton or chromatin.

## What does survive, and it is not a disease-modifying drug

### 1. Vinorelbine — retain it, on a genotype argument (C11)

The only candidate in this workstream that points **with** the standard of care, and it meets
three of the four constraints outright — approved, systemic, established in paediatric
oncology — and bears directly on this child's own tumour type.

**What I cannot claim, and did claim in the first version of this file.** I wrote that
vinorelbine is *"already part of this child's own regimen."* **The record does not say that**,
and I inferred it from the fact that vinorelbine is the EpSSG RMS 2005 maintenance arm. Whether
this child received it depends on whether the tumour was treated at all, on risk
stratification (maintenance is for high-risk disease), and on protocol era and country — none
of which is in the record. The honest form is **conditional**: *if* vinorelbine is on the
table for this child, now or at relapse, the genotype argues for retaining rather than
avoiding it.

- With low-dose cyclophosphamide it is the maintenance arm of **EpSSG RMS 2005**, which moved
  5-year overall survival **73.7% → 86.5%** (HR 0.52; Bisogno et al., *Lancet Oncol* 2019).
- Klotz et al. 2012 (*J Cell Sci* 125:887–95): *"vinorelbine ... kills APC-deficient cells ...
  **more effectively** than wild-type ... due to the ability of vinorelbine to **kill cells in
  interphase independently of mitotic arrest**."*
- Our own retracted rule (**C1**) implied SAC-routed killing should underperform here. Klotz
  inverts that for this specific drug.

**So the action is to retain an established therapy, not to add or avoid one.** That is a real
genotype-directed recommendation and it is the most defensible one available.

**Honest limits, carried from C11:** the SAC compromise in Klotz is *APC* loss, not a *BUB1B*
lesion; the interphase killing is p53- and BIM-dependent; the cells are colorectal; and
**vinorelbine has never been tested in a BubR1-hypomorphic background.** It also never reached
`TRACK2-REPORT.md` at all, which the Review Room's direction seat flagged (F7).

### 2. Surveillance, which outranks every drug here on expected benefit

`STANDARD-OF-CARE.md` already concludes this, and the AACR/Nakano 2024 guideline explicitly
includes MVA: **renal ultrasound every three months to age seven**, plus clinical review for
rhabdomyosarcoma. If the tumour was treated and is controlled, this becomes relapse and
second-primary surveillance; if it is active, oncological management takes precedence and
the surveillance framing does not apply.

It is not a drug and it is not novel, which is exactly why it keeps being passed over. It is
still the intervention with the largest expected benefit for this child.

### 3. The IL-1 arm, which is approved and systemic but under-supported

Anakinra and canakinumab are approved, systemic, and anakinra reaches **neonates** (NOMID) —
the best chronic-paediatric credential in this document. But Thesis A is logged
`interesting_under_supported`, the arrest/SASP separability claim holding up Gate 4 carries
**no citation**, and **C9**/Hong 2022 makes IL-6 two-signed in chromosomally unstable cells.
The safety seat additionally found malignancy-risk language in *both* labels, neutropenia
(Ilaris 15.9%; Kineret ANC monitoring), and a **live-vaccine prohibition** in a child who
may need post-chemotherapy revaccination.

## What would change this

Three things, in order of how much they would move it:

1. **Measure whether the 737X truncated protein is made and functional at physiological
   dose.** The entire allele-1 case rests on LAP-731X rescuing — and 753X *fails*. Our 737X
   sits between them at ~70/30 off a two-point calibration. This is a blot and a checkpoint
   assay.
2. **Run the G0 ciliation assay** (`DIRECTION-G0-CILIA.md`). It is the only readout in this
   project with no cell-cycle confound by construction, and it would let every parked arm be
   screened against a real dynamic range.
3. **Find the free-drug concentration at which any agent raises BubR1 in this child's cells.**
   Every route closed above was closed on exposure or mechanism — not one was closed on a
   measurement in this patient's own material.
