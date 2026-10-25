# Phoenix head-to-head: running the engine against the hand-built funnel

Run 10 Sep 2026, after the owner opened the remaining hosts. This is the check that
was owed: the six gates were written from scratch and borrowed only Phoenix's design
vocabulary, so "does Phoenix reach the same answer" was untested until now.

## What ran, and what did not

| Phoenix component | Status |
|---|---|
| GEO expression loading | **runs** (after the `ftp://` -> HTTPS loader fix) |
| organ-aging scoring / Cohen's d | **runs** |
| mechanism resolution (Open Targets) | **runs** |
| literature retrieval | PubMed fallback available; Paperclip key unset |
| **adversarial refutation judge** | **cannot run** — no LLM key set |
| Adjudicator | pure math, runs on whatever channels exist |

Per Phoenix's own convention, a missing channel lowers coverage and never the score,
so the absent adversarial channel is a coverage reduction, not a failure.

## A correction: the "no MVA cohort" claim was wrong

`TRACK2-PLAN.md` stated there is no MVA patient expression cohort. That was too
strong, and searching GEO directly (rather than PubMed) found several:

| accession | organism | n | what it is |
|---|---|---:|---|
| **GSE22206** | human | 14 | homozygous *BUB1B* splice mutation with confirmed MVA, vs controls and heterozygous relatives |
| **GSE197267** | human | 5 | biallelic *MAD1L1* LOF — a SAC-loss MVA variant; single-cell |
| GSE134780/1 | mouse | 23/9 | BubR1 allelic-series MVA progeria model |
| GSE270226 | mouse | 2 | BubR1-knockout embryo, single cell |

GSE197267 **could not be loaded**: it is RNA-seq shipping counts in a supplementary
tar rather than embedded VALUE tables, which Phoenix's loader explicitly does not
handle. GSE22206 loaded at 18,197 x 14.

## The result, which contradicts Arm A

`scripts/mva_bub1b_cohort.py` scores all nine Phoenix axes on GSE22206. The design
carries a natural allele-dose gradient — control, heterozygous relative, homozygous
proband — so an axis genuinely driven by BUB1B loss should order that way.

**Lymphoblastoid lines** (n=2 proband, 4 control, 4 relative):

| axis | proband vs ctl | het vs ctl | dose-ordered |
|---|---:|---:|---|
| **Immune (the SASP axis)** | **−1.75** | −1.20 | yes |
| IFN | +0.87 | −1.09 | no |
| Senescence | +0.60 | −1.63 | no |

**The Immune axis is DOWN in the proband, not up.** It is dose-ordered, so the
direction is internally consistent — and it is the opposite of what Arm A predicts.
Fibroblasts (n=2 vs 2) point the same way but produce |d| values of 10–16, which are
variance artefacts of two samples per arm and are reported here only to be dismissed.

## How much this should move the verdict

**It should move it, but not collapse it.** Three things bound the finding:

1. **n=2 per arm.** Cohen's d on two samples is descriptive. There is no confidence
   interval here and none is implied.
2. **Lymphoblastoid lines are EBV-immortalised.** Immortalisation directly perturbs
   the senescence and inflammatory programmes being measured, which is close to
   disqualifying for this particular question.
3. **The other human dataset points the other way.** Villarroya-Beltri et al.,
   *Science Advances* 2022 ([DOI](https://doi.org/10.1126/sciadv.abq5914)) profiled a
   patient with biallelic *MAD1L1* LOF — a SAC-loss MVA variant — by single-cell RNA
   on **primary blood cells**, and report "mitochondrial stress accompanied by
   systemic inflammation with enhanced interferon and NFκB signaling both in aneuploid
   and euploid cells, suggesting a non-cell autonomous response."

Point 3 is the stronger evidence on the stronger tissue, and its "non-cell
autonomous" finding is precisely a paracrine mechanism — the thing Arm A proposes to
interrupt. It also names **NF-κB**, the master SASP regulator through which IL-1β
signals, which is mechanistically closer to the leads than a generic inflammation
claim would be.

So the two human datasets disagree, and the disagreement is explicable by cell type:
immortalised lines versus primary cells. That is a real limitation of the tissue
channel, not a tie to be split.

## Effect on the submission

- The tissue channel is now **observed but discordant**, where it was previously
  absent. Coverage rises; confidence does not.
- Arm A's verdict stays `interesting_under_supported`. It does not rise on the
  MAD1L1 evidence, and it does not fall to `under_supported` on GSE22206 — one
  n=2 immortalised-line comparison cannot carry that weight either.
- **The proposed first experiment changes.** The report previously said: measure
  IL-1β/IL-6/hsCRP in patient material. That is now sharper — measure them in
  **primary cells, not immortalised lines**, and include an interferon/NF-κB readout,
  because that is the axis the better human dataset actually implicates.

## What a full Phoenix run would still add

The adversarial refutation channel is the one component that could not run. On this
evidence it is also the one that would matter most: two human datasets pointing
opposite ways is exactly the situation that channel exists to adjudicate. Running it
needs `ANTHROPIC_API_KEY` (or `OPENROUTER_API_KEY`) in `apps/api/.env`.
