# A calibrated NMD prediction for allele 1, and what it does and does not settle

**Run 13 Oct 2026.** Allele 1 of this proband is **p.Leu737Ter** (`c.2210T>G`,
chr15:40,209,701 T>G). Every downstream argument about that allele depends on one
assumption: that its transcript is degraded by nonsense-mediated decay. Until now this
workstream asserted that from the **50–55 nt rule** — the PTC lies well upstream of the
last exon–exon junction, therefore NMD-competent. A binary rule, applied by hand.

`NMD-FEASIBILITY.md` and `CORRECTIONS-2026-10-06.md` C19(c) both identify the allele-1
question as the better-posed crux of this whole workstream, and an independent review
nominated it as the disagreement that should have been posed first. So replacing a hand-
applied binary rule with a calibrated, feature-explicit prediction is a direct upgrade to
the load-bearing assumption.

## What was run

**TrunKitten**, the 8-feature reduced form of **TrunCat**, from
`CobanAkdemirlab/NMDpredictionmodel`, accompanying the preprint *"Unveiling the Hidden
Rules: Enhancing NMD Prediction for Protein-Truncating Variants"*
(doi:10.64898/2026.06.26.734884). TrunCat is a CatBoost classifier trained on NMD measured
directly from paired whole-genome and RNA-seq data in 10,306 TOPMed samples across 5,749
germline truncating variants; the preprint reports ROC-AUC ≈ 0.78 against ≈ 0.71 for the
rule-based standard, and states that the canonical 50–55 nt rule explains only about half
of the observed variability. TrunKitten is the reduced model the authors provide
explicitly *"for prediction on external cohorts where reproducing the full 619-feature
annotation pipeline is impractical."*

Reference data: GENCODE v26 (hg38), hg38 chr15 FASTA, UCSC phastCons 100-way (chr15,
converted to bedGraph over the region of interest), GTEx v8 median TPM, and the authors'
committed mRNA half-life table.

## The result

| | |
|---|---|
| **escape probability** | **0.3163** |
| model threshold (Youden) | 0.4314 |
| **predicted class** | **NMD — transcript degraded, does not escape** |

So the prediction **agrees with our existing call**, and that is worth stating plainly:
the 50–55 nt rule gave the right answer here. What the model adds is the magnitude. An
escape probability of **0.32 is not negligible** — roughly a one-in-three predicted chance
of escape, from a model whose own discrimination is ROC-AUC ≈ 0.78. "Predicted to undergo
NMD, with meaningful residual probability of escape" is a materially different claim from
"NMD-competent by the 50–55 nt rule", and it is the honest one.

## The 8 features, as computed

| feature | value |
|---|---|
| `last.EJC` | upstream |
| `relativePTClocation` | 0.7009 |
| `half_life_PC1` | −0.1291 |
| `cdsseqs_AU_content` | 0.5661 |
| `mut.exon` | 17 |
| `cdsseqs_UC_content` | 0.4539 |
| `phastcons_new3utr_first200_median` | 0.994 |
| `MedianExpression_log2` | 0.4417 |

## Three independent confirmations of our own annotation

The run reproduced, from GENCODE v26 directly rather than from our own parsing:

- **23 exons, 23 coding exons**, PTC in **exon 17** — our files said "exon 17/23". Match.
- **CDS length 3,153 nt** = 1,050 residues plus stop — matching BubR1's length in UniProt
  O60566, which an independent review had verified separately.
- Canonical transcript **ENST00000287598** resolved from the GTF rather than assumed.
- phastCons at the PTC position is **0.972**, and the median across the first 200 nt of the
  new 3′UTR is **0.994** — independently consistent with the ClinVar submitter note on the
  *other* allele that the position is conserved (C16).

## Limits, stated before anyone leans on this

1. **The model is a prediction, not a measurement.** ROC-AUC ≈ 0.78 means roughly one call
   in five is on the wrong side of the boundary in the authors' own evaluation. This does
   not measure NMD in this child; it predicts it from transcript features.
2. **Our variant is not in the authors' precomputed sets.** Their shipped ClinVar (30,129),
   gnomAD (137,858) and GREGoR (2,549) prediction files contain **no *BUB1B* rows at all**,
   so no cross-check against their own output was possible for this gene.
3. **The preprint is not peer reviewed.**
4. **The reduced model is not the headline model.** TrunKitten uses 8 of TrunCat's 619
   features and carries its own threshold (0.4314 vs TrunCat's 0.4747). The authors
   position it as the practical option for external cohorts, not as the better model.
5. **It does not answer the second half of the crux.** Whether the 736-residue product
   would be *functional* if decay were bypassed remains open — that is the 731X-versus-753X
   split our own `NMD-FEASIBILITY.md` calls "the real gap", and no NMD predictor addresses
   it.

## Validation performed

**An end-to-end cross-check against the authors' own published predictions.** Because no
*BUB1B* variant appears in their shipped prediction files, a direct check on this gene was
impossible — so instead we took **12 chr15 variants from their own ClinVar prediction set**,
resolved each gene's canonical transcript from the GTF, and ran them through our
installation from scratch. Their published values come from **TrunCat** (619 features); ours
come from **TrunKitten** (8 features), so exact agreement is not expected.

| | result |
|---|---|
| class agreement (NMD vs escape) | **12 / 12** |
| Pearson *r*, TrunCat vs TrunKitten probabilities | **0.966** |
| range covered | 0.118 → 0.810 (their values), spanning both classes |

Two different models, one of which we ran ourselves on reference data we assembled
ourselves, agreeing on every call across the full probability range. That is the evidence
that the 0.3163 for p.Leu737Ter reflects the published method rather than a
misconfiguration on our side — which, after this workstream's correction history, is the
only basis on which the number is worth reporting at all.

- The pipeline's own test suite: **40 of 40 passed**.
- Annotation QC flags all clean: transcript found, no boundary ambiguity, new 3′UTR
  non-empty, half-life present, expression present, no missing conservation. One benign
  `version_mismatch` (we supplied `ENST00000287598.10`; the version was stripped and
  matched), reported honestly by their own QC.

## Two things found in the process, both worth reporting upstream

**A reproducible crash on current pandas.** `minicat/halflife.py:61` calls `.lower()` on a
gene-symbol cell guarded only by truthiness. Under pandas 3.0.6 the committed half-life
table loads with the new `str` dtype, under which `.astype(str)` does **not** render a null
as the string `"nan"` — it stays a genuine missing value, which is a truthy float. Exactly
one of 13,921 gene symbols is null, and it aborts the entire pipeline with
`AttributeError: 'float' object has no attribute 'lower'`. The one-line fix is an
`isinstance(sym, str)` guard. On older pandas, where that column would be `object` dtype,
the code works — so this will bite anyone running it on a current stack.

**The repository carries no licence.** No `LICENSE`, `LICENSE.md`, `LICENSE.txt` or
`COPYING` on either `main` or `master`, checked 13 Oct 2026. Absent a licence grant the
default is all rights reserved.

## Consequence for what we can ship

**We may use the tool and cite it; we may not redistribute it.** Running a published tool
to compute a number and citing the source is ordinary practice. Vendoring unlicensed code
into a submission repository that must be public under CC BY 4.0 is not, and the organisers
state submissions may be rerun. So:

- this document, our input file and our conversion scripts are ours and ship;
- the model, its weights and the `minicat` package are **not** vendored;
- reproduction instructions point at the authors' repository and the preprint DOI.

A reader can reproduce this number by cloning the upstream repository themselves. That is
the correct dependency boundary, and it is also why the prediction is reported here with
its inputs and features in full rather than as a bare number.
