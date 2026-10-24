# The NMD instrument across all three MVA genes — and the one result that survived its confound

**Run 13 Oct 2026.** Reproduce with `apps/api/scripts/mva/nmd/clinvar_ptc.py` then
`stratify_ptc.py`; inputs and outputs in `data/nmd/`. Supersedes the BUB1B-only
`NMD-STRATIFIED-BUB1B.md`, which remains for the band analysis specific to that gene.

## What changed to make it general

The BUB1B-only version hand-coded three motif boundaries from our own files. That does not
scale, and a "scalable" instrument that needs a human to look up domain coordinates per
gene is not scalable. `stratify_ptc.py` now reads domain architecture from **UniProt**, so
the only per-gene input is an accession.

Scope: **48 ClinVar single-nucleotide nonsense variants** across *BUB1B* (37), *CEP57*
(10) and *TRIP13* (1), each scored with TrunKitten (model, validation and limits in
`NMD-PREDICTION-TRUNKITTEN.md`) and cross-tabulated against retained UniProt features.
All 48 passed annotation QC with no missing features.

**UniProt independently confirmed two of our own coordinates**: BUB1B's protein kinase
domain at **766–1050** (our files say 766) and a binding site at residue **795** (our files
document VAIK K795). Note the KARD/PP2A-B56 site at 669–674 that the BUB1B band analysis
relies on is **not** a UniProt feature — it is literature-derived, and that provenance
difference is now explicit rather than blurred.

## The headline, and why it needed checking

The naive comparison looks dramatic:

| ClinVar class | predicted to escape NMD |
|---|---|
| Uncertain significance | **4 / 5 (80%)** |
| Pathogenic | **1 / 34 (2.9%)** |

That is a far starker separation than the preprint's own finding that VUS escape NMD about
1.7× more often than pathogenic variants. **It is also exactly the shape an artefact would
take**, because a variant near the 3′ end both escapes NMD more readily *and* is more
likely to be called a VUS, for the same underlying reason: it truncates less protein.

So the first thing to do was test position, not report the number.

## Escape is U-shaped in position, which is the confound made visible

| fraction of protein retained | n | predicted to escape |
|---|---|---|
| 0.00 – 0.10 | 3 | **3 (100%)** |
| 0.10 – 0.25 | 8 | 0 |
| 0.25 – 0.50 | 14 | 0 |
| 0.50 – 0.75 | 12 | 0 |
| 0.75 – 0.90 | 6 | 2 (33%) |
| 0.90 – 1.00 | 5 | 2 (40%) |

**Zero of 34 variants in the middle 65% of the coding sequence are predicted to escape.**
Escape appears only at the two ends — start-proximal PTCs (residues 34, 57, 67 of BubR1)
and 3′-proximal ones. Both are established NMD biology, and neither was encoded anywhere in
our analysis: the model produced them. The VUS do sit late (median retained fraction 0.840
versus 0.440 for everything else), so the confound is real and large.

## The association survives a position-matched comparison

Restricting to variants retaining ≥75% of the protein — where all the escaping VUS sit:

| | n | predicted to escape | median P(escape) |
|---|---|---|---|
| **VUS** | 4 | **4 / 4** | **0.685** |
| non-VUS | 7 | **0 / 7** | 0.300 |

At comparable positions, the two classes separate cleanly and do not overlap in call. The
non-VUS comparators are *BUB1B* 813, 826, 826, 950, 959, 966 and *TRIP13* 354, all
predicted NMD at P = 0.18–0.34.

**Why this is worth reporting.** A nonsense variant classified as uncertain, and predicted
to escape decay, is one where the usual inference chain — PTC, therefore decay, therefore
null allele, therefore pathogenic — fails at its first step. That is precisely the
reclassification reservoir the preprint argues for, and here it concentrates in the VUS
class of a disease-specific gene set after the obvious confound is removed.

## What this does not establish, stated before anyone quotes the 4/4

- **n = 4 versus n = 7.** No effect size should be taken from this, and the unmatched
  80%-versus-2.9% figure above should not be quoted at all.
- **Gene and class are partly confounded.** Three of the four escaping VUS are *CEP57*;
  six of the seven matched non-VUS are *BUB1B*. Within *BUB1B* alone the comparison is
  1/1 versus 0/6 — same direction, but a single variant.
- **These are predictions.** ROC-AUC ≈ 0.78 applies to every row.
- **ClinVar classes are not independent observations.** Submitters share evidence, and
  "uncertain" partly encodes *how little protein is lost*, which is the very axis under test.
- **Escaping NMD is not the same as being benign, nor as being pathogenic.** A stable
  truncated protein may be inert, hypomorphic, or dominant-negative. The prediction
  relocates the question; it does not answer it.

## Where the instrument degenerates, reported rather than hidden

**TRIP13 has one ClinVar SNV nonsense variant and zero annotated UniProt domains.** The
pipeline runs on it without modification and returns a prediction (residue 354,
P = 0.178, NMD) — but with no domain annotation there is no retention axis, so the
instrument collapses to a bare NMD call, and with n = 1 there is nothing to stratify.

That is the honest scalability answer. The method generalises **mechanically** to any gene
with a UniProt accession and ClinVar PTCs, and generalises **usefully** only where both the
domain annotation and the variant count are non-trivial. For the three MVA genes that means
*BUB1B* fully, *CEP57* partially, *TRIP13* not at all.

## The clinical stratification this sits inside

Yost et al. 2017 (doi:10.1038/ng.3883) established that embryonal tumour risk in MVA tracks
**severity of checkpoint impairment**, not aneuploidy as such: biallelic *BUB1B* or *TRIP13*
carry high risk with severe SAC impairment, while *CEP57* MVA shows minimal SAC deficiency
and is not associated with embryonal tumours. So the three genes are not interchangeable,
and a per-gene NMD table is the right granularity — pooling them would average across
groups the clinical literature deliberately separates.
