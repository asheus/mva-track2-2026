# Every approach considered, ranked — and where the ranking cannot be trusted

> **RANKING SUPERSEDED 21 Oct 2026 by `RECOMMENDATION.md`.** This page scores viability as
> one axis among eight, and the composite averaged it away: it ranks **trans-splicing
> first**, and trans-splicing has no approved drug, no molecule in any clinical trial, and
> no RTM ever given to a patient for any gene. Applying viability as a *gate* instead
> leaves one approach that is both obtainable and aimed at this genotype's deficit — an
> **NAD⁺ precursor**. The matrix below is kept for the criteria and the re-weighting
> analysis, which remain valid; its final order does not.

*Producer: `scripts/mva/approach_matrix.py`. Fourteen therapeutic approaches plus two
things that are not therapies. Scored only on criteria this project measured, with the
weights declared in the file and the ranking re-run under four different weightings to
separate stable positions from artefacts of how I weighted them.*

## The matrix

`a1` / `a2` = reaches allele 1 (p.Leu737Ter) / allele 2 (p.Asn1002Lys). `wav` = inherits
BubR1's cell-cycle waveform rather than having to manufacture one. Coverage = how many of
the **2,536** catalogued alleles the modality could reach at all.

| approach | a1 | a2 | wav | coverage | in vivo | in humans | killable | status |
|---|---|---|---|---|---|---|---|---|
| Trans-splicing (SMaRT) of endogenous pre-mRNA | 2 | 2 | 2 | 2,536 | 0 | 1 | 2 | untested |
| NAD⁺ precursor (NMN/NR) via SIRT2/K668 | 0 | 2 | 1 | 2,256 | **2** | 2 | 2 | untested |
| trans-RNA initiation on endogenous mRNA | 0 | 2 | 2 | 2,256 | 0 | 0 | 1 | untested |
| CRISPRa at the native promoter | 2 | 2 | 2 | 2,536 | 0 | 0 | 2 | untested |
| Readthrough (ataluren / G418 / ACE-tRNA) | 0 | 0 | 2 | **4** | 0 | 2 | 2 | wrong allele |
| Pharmacological chaperone, pseudokinase pocket | 0 | 2 | 2 | 1,494 | 0 | 2 | 0 | **not evaluable** |
| Checkpoint timing extension | 2 | 2 | 0 | 2,536 | 0 | 1 | 1 | untested |
| Prime editing, ex vivo | 2 | 2 | 2 | 2,536 | 0 | 1 | 0 | untested |
| Senolytics / mTORC1 inhibition | 0 | 0 | 0 | 2,536 | 0 | 2 | 1 | downstream |
| APC/C–Cdc20 inhibition | 0 | 2 | 0 | 2,256 | 0 | 0 | 1 | rejected |
| HDAC inhibition to raise acetylation | 0 | 2 | 0 | 2,256 | 0 | 2 | 1 | argued against |
| circRNA / AAV encoding BubR1 | 2 | 2 | **0** | 2,536 | 0 | 2 | 1 | argued against |
| Splice-modulating ASO (TANGO-style) | 0 | 2 | 2 | **0** | 0 | 2 | 2 | **killed** |
| Neoantigen vaccine | 0 | 0 | 0 | **0** | 0 | 2 | 2 | **killed** |

## The ranking

1. **Trans-splicing (SMaRT)** — the only modality reaching the dead allele; needs 23–38% efficiency
2. **CRISPRa at the native promoter** — *not a therapy; see the caveat below*
3. **NAD⁺ precursor** — the only class with in-vivo evidence of raising this protein
4. Prime editing, ex vivo — corrects blood; MVA's tumours are solid
5. circRNA / AAV encoding BubR1 — *scored too high; see the caveat below*
6. trans-RNA initiation — published weeks ago, endogenous, in vivo in mouse
7. Checkpoint timing extension — the only idea reaching the 280 transcript-less alleles
8. Readthrough — 4 eligible alleles here, or 284 with NMD attenuation
9. HDAC inhibition — K250 stabilises, K668 destabilises; net effect unpredictable
10. Senolytics / mTORC1 — treats accrued damage
11. Splice-modulating ASO — killed by RNA-seq
12. Pharmacological chaperone — not evaluable
13. APC/C–Cdc20 inhibition — arrests every mitosis
14. Neoantigen vaccine — would target the patient

## What survives re-weighting, and what does not

The ranking was re-run under four goals: *what to do next with no wet lab*, *this child
only*, *the most children*, and *fastest to a human*.

**Stable across all four (moves ≤1 place):**
- **Trans-splicing — 1st, 1st, 1st, 2nd.** The top position is not an artefact of weighting.
- Prime editing, 4th–5th. Senolytics, 9th–10th. Chaperone, 11th–12th. Vaccine, 13th–14th.

**NAD⁺ moves only between 1st and 3rd**, which makes the top two a genuinely stable pair:
*trans-splicing on the merits, NAD⁺ on readiness.*

**Unstable — the weighting is doing the work, not the evidence:**
- **Readthrough moves 4 places** (6th to 10th). It is excellent on human readiness and
  almost irrelevant on coverage for this genotype, so any weighting that trades those two
  swings it. Its rank should not be quoted without the weighting.
- **trans-RNA moves 3 places** (6th to 9th), for the opposite reason: strong mechanism fit,
  no human history at all.

## Two places the scoring is wrong, stated rather than patched

A composite score cannot express a veto, and two rows prove it.

**circRNA / AAV encoding BubR1 ranks 5th and should not.** It scores well on coverage, on
reaching both alleles and on human familiarity — and it fails the one criterion that is
disqualifying rather than merely costly. BubR1 must *fall* at anaphase; a constitutive
source fills the trough, and Choi 2009 showed an undegradable BubR1 markedly delays
chromosome segregation. `waveform = 0` is a veto, not a −2. The arithmetic averages it
away.

**CRISPRa ranks 2nd and is not a therapy.** It is not deliverable to a child. It ranks high
because it genuinely does reach both alleles and inherits the native regulation — which
makes it the right *experiment* for the dosage thesis, and the wrong entry in a therapy
ranking. It belongs beside the adjuncts.

Both are left in place rather than quietly re-scored, because the useful thing here is the
demonstration that the composite has limits, not a number tuned until it agreed with the
prose.

## Not ranked, because they are not therapies

- **Mosaic selection as an amplifier.** Aneuploid cells are less fit, so corrected cells
  outgrow their neighbours — lowering trans-splicing's bar from *holding* 23–38% to seeding
  an expanding clone. Only in renewing tissue; it does nothing for the already-accrued
  brain phenotype.
- **Cancer-risk stratification from the map.** Not a therapy, and the only clinically
  actionable output available today, requiring no new biology.

## The honest summary

**Best on the merits: trans-splicing.** Stable at the top under every weighting tried. It
is the only approach that reaches p.Leu737Ter, because trans-splicing acts on pre-mRNA
before NMD destroys the message; it inherits the cell-cycle waveform; and being
mutation-agnostic it serves the whole map rather than one genotype. Its bar is 23–38%
efficiency, which is where SMaRT has historically struggled.

**Best bet today: the NAD⁺ route.** The only class with in-vivo evidence of raising BubR1,
already in humans including an n-of-1 in a germline cancer-predisposition syndrome. It now
carries one extra obligation: it works by slowing degradation, and degradation is the timed
event, so mitotic timing must be measured alongside abundance.

**Best next action: neither.** Add the **N1002R** lane and the **pT1008** blot to the
experiment already designed. Every approach above assumes p.Asn1002Lys reduces BubR1
*abundance*. One construct separates folding from ubiquitination outright, and the whole
table is built on an assumption nobody has tested.

**And the number that does not move whatever we choose: 280 of 2,536 alleles lose the
transcript.** Eight of the fourteen approaches cannot reach them at all. That boundary has
now survived five changes of technology in this project, which is the strongest evidence we
have that the map, not any one candidate, is the durable thing here.
