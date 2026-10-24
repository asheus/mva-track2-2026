# Triage: five Edison analysis bundles

*Assessed 23 Oct 2026. Five README files from executed analysis bundles (one is a
reproduce-instructions file for another). These are a **different class** from the
discovery reports triaged in `TOOL-TRIAGE-KOSMOS-NAD.md`.*

## Why these are weightable and the earlier reports were not

| | Discovery reports (7, triaged separately) | These bundles (5) |
|---|---|---|
| Data | none — "Dataset Description" empty | pinned public releases (DepMap 23Q4 v2, CPTAC LinkedOmicsKB R1, GEO GSE146773) with MD5/SHA-256 manifests |
| Code | none | executed scripts, pinned `requirements.txt`, re-run logs, independent-process reproduction |
| Plan | none | `analysis_plan.json` / `plan.md` recorded **before** outcomes inspected |
| Tests | one-sided narrative | two-sided, FDR-corrected, pre-declared families, exploratory families labelled |
| Negatives | none reported | **reported, including against their own hypotheses** |
| Genotype | wrong (`p.Trp737*`, `L1012P`) | not used — these are gene-level population analyses, so the error cannot occur |

The standing rule says third-party *model output* is never a source of a verdict, score or
number. These are not model opinions; they are reproducible analyses of public data with the
scripts attached — the same category as our own committed queries, except run by someone else.
**They are therefore citable as external corroboration with provenance, and adoptable as ours
only by re-running the bundle.** None of their numbers is imported into the report here.

## The one that touches a live arm: CPTAC SIRT2–BubR1

Our §3.3 table demotes the SIRT2 / NAD⁺ route on mechanism (wrong degradation route, K250
hazard). An earlier discovery report pushed it as the lead, resting partly on a positive
GTEx **RNA** co-expression between `BUB1B` and `SIRT2`. This bundle tests the same
relationship at the **protein** level, properly adjusted, in 503 complete CPTAC tumour cases:

| Adjustment | Partial r | P |
|---|---:|---:|
| none | −0.014 | 0.755 |
| proliferation median only | **+0.399** | 1.2 × 10⁻²⁰ |
| proliferation median **+ cancer type** | **−0.152** | 7.1 × 10⁻⁴ |
| four individual markers + cancer type | −0.136 | 0.0024 |

**The sign reverses on controlling for lineage.** Seven of nine within-cancer estimates are
negative, no cohort survives nine-test BH, and the reversal reproduces in an independently
retrieved PDC archive version (+0.396 → −0.153). The authors' own reading is that the pooled
positive result "should not be interpreted as evidence for a general within-lineage positive
SIRT2–BubR1 relationship."

**What this does for us.** It is independent, protein-level, correctly-adjusted evidence
*against* the abundance rationale for a SIRT2 activator — the exact confound structure we
named (BUB1B is a proliferation marker, so any correlation with it is dominated by cycling
fraction). It corroborates a demotion we had already made, on a better data type than we had,
and it retires the GTEx co-expression argument that the discovery report leaned on. It does
**not** disprove a stabilisation mechanism, and the bundle says so.

## The one that matches our own assay design

The single-cell screen (GEO GSE146773, 1,128 QC-passing U2OS FUCCI cells) is close to what
`ASSAY-DESIGN.md` specifies in spirit: per-cell, cell-cycle-corrected using **independent
FUCCI fluorescence coordinates** rather than RNA scores alone, removing 71.1% of BUB1B
variance. Two results worth keeping:

1. **It quantifies the confound we have only asserted.** Median `BUB1B` TPM: **22.06 (G1) →
   32.66 (S) → 47.91 (G2/M)** — roughly a 2.2× RNA swing across the cycle in one line with
   gated phase. That is the amplitude any bulk pharmacology claim has to beat, and it is RNA,
   not the protein waveform.
2. **No E3 candidate was found.** 534 expressed E3 genes tested; top hit ITCH r = 0.0998,
   **q = 0.158 — nothing passed FDR < 0.05**, and ITCH held a top-ten place in only 41% of
   bootstrap resamples. This matters because the DUBTAC concept raised in a separate
   discovery report requires knowing *which* E3 removes the mutant protein. Coexpression does
   not name one. It is a null on a prerequisite, not on the modality.

## The two DepMap bundles

**HDAC2 / HDAC3 dependency.** HDAC2's association with low BUB1B does not survive adjustment
for proliferation and lineage (q = 0.215). HDAC3 runs the **opposite way** — low-BUB1B models
are *more* dependent on HDAC3, adjusted continuous slope +0.057 per SD, q = 0.046. Both
unadjusted r² values are ≈0.5%, and `BUB1B` correlates with the proliferation proxy at
r = 0.807.

This independently supports **C5**, where we retracted 4-PBA's HDAC inhibition as a
*supporting* mechanism and concluded it points at the disease rather than away from it: if
low-BubR1 cells are more HDAC3-dependent, inhibiting HDAC3 in this child is the wrong
direction. Small effects, but the sign is against the arm we had already demoted.

**FBXW7 dependency.** All three pre-declared primary tests non-significant; a weak adjusted
expression association (P = 0.025) failed FDR (q = 0.150) and was not reproduced rank-based.
FBXW7 is not an arm in this workstream, so this is a null on a hypothesis we never held —
logged only so it is not re-proposed as untested.

## Net effect on the submission

**No conclusion changes.** Every result here either corroborates a demotion we had already
made (SIRT2, HDAC) or is a null on something we do not claim (FBXW7, the E3 identity). The
two things worth carrying forward are the **measured 2.2× cell-cycle RNA amplitude**, which
is a number for a confound we had only described, and the **named absence of an E3 candidate**,
which is the missing prerequisite for any degradation-directed modality.

Nothing here is adopted into `TRACK2-REPORT.md` as our own result. Doing that would require
re-running the bundles, which is not a good use of the hours remaining before the deadline.

---

## Second batch, 23 Oct 2026 — ten files, five analyses, no conclusion changes

Ten more files. Three are duplicates: `d87c975b-analysis_report.md` repeats the single-cell
E3 screen triaged above verbatim (same 1,128 cells, ITCH r = 0.0998, q = 0.158), and
`05b71e9b-report-2.md` / `3530691c-report-2.md` are byte-identical to each other. Two more are
README/full-report pairs for the same work. So the ten files are **five analyses**.

### The one that clarifies something: BubR1 and the chaperone machinery

The sharpest open question in this workstream has been whether the mutant protein is a
chaperone client, and *which* chaperone. This bundle reran **SAINTexpress on the deposited
BioID spectral counts** against the original negative controls and reproduced the deposited
statistics, finding three significant BubR1 proximity associations:

| Partner | Refit AvgP | Refit BFDR | Fold over controls | Meets study's AvgP ≥ 0.98 |
|---|---:|---:|---:|---|
| DNAJC7 | 1.00 | 0.00 | 8.13 | yes |
| HSPA12B | 0.98 | 0.00 | 6.28 | yes |
| DNAJA2 | — | < 0.05 | — | no |

Three things make this useful rather than just suggestive:

1. **No qualifying AP-MS interaction was found.** So this is proximity, not a stable physical
   complex — the same distinction that made the earlier discovery report's HSP70 claim
   unsafe, now resolved in the direction of proximity-only.
2. **The partners are J-domain co-chaperones, not HSP70 itself.** DNAJC7, DNAJA2 and HSPA12B
   are not HSPA1A/HSPA8. The earlier report's claim rested on HSPA1A/HSPA2 AP-MS baits while
   its own trajectory concluded there was no convincing evidence of cytosolic HSPA1A/HSPA8
   client status. This is consistent with that negative.
3. **Neither DNAJC7 nor HSPA12B associates with proliferation-corrected BUB1B expression** in
   DepMap 23Q4.

**What it does for us.** It further separates the two chaperone axes. The *measured* folding
dependency for this mutation class is **HSP90** — Suijkerbuijk 2010's geldanamycin result,
where mutants collapse and wild-type does not. The HSP70/HSF1 axis, which is arimoclomol's
mechanism, remains supported only by proximity and by the insufficiency-caveated CBS
precedent (**C47**). That is one more reason the arimoclomol lead keeps its mechanism and
loses its borrowed magnitude, and it is independent of C47's route.

### The three that corroborate demotions already made

- **SIRT2–BUB1B single-cell RNA** (GSE146773 + GSE72056 melanoma): no robust inverse
  association; correction turns a null into a very small positive one that is not robust to
  independent FUCCI measurement or rank-based analysis. Notably, the authors state it does
  **not** show that cycle confounding produced the earlier negative CPTAC protein
  correlation — so the protein-level negative stands on its own.
- **CPTAC SIRT2–FBXW7 / SIRT2–CDC27**: pooled associations significant with proliferation
  adjustment alone, gone after cancer-type adjustment, and significant within no adequately
  sampled cohort. The same lineage-confound signature as the SIRT2–BubR1 result above.
  Worth one note of data hygiene: this bundle flags that **FZR1 encodes APC/C Cdh1 while CDH1
  encodes E-cadherin**, and analysed FZR1 as intended with literal CDH1 kept separate. That
  is a real trap in any APC/C-Cdh1 query, ours included.
- **DNAJC7–UBE4A co-dependency**: a small but significant **negative** association (more
  DNAJC7-dependent models are *less* UBE4A-dependent), with no BUB1B-expression context
  surviving the prespecified joint correction. Null on a three-gene pathway we never claimed.

### The one new arm, and why it does not survive our own prior findings

**RXR agonists in LINCS L1000.** 362 release-matched signatures, 69 hits across four
annotated compounds — but **bexarotene contributes 56 of 69** and is the only compound with a
positive overall median; the other three are near zero or negative. The authors' own reading:
"not a robust RXR class effect... not an on-target RXR mechanism or restoration of BubR1
protein."

Nobody in this workstream proposed RXR agonism, so this is a new hypothesis arriving with its
own negative. Two things retire it independently of that. First, L1000 Level 5 values are
**transcriptional** consensus z-scores, and `DRUG-SCREEN.md` established that transcript-level
`BUB1B` signals in bulk perturbation data are dominated by cell-cycle redistribution — the
single-cell bundle above puts that RNA swing at roughly 2.2× across the cycle, which an
isolated z-score above 1 does not clear. Second, bexarotene is a systemic retinoid:
teratogenic, with lipid and thyroid effects, in a growth-restricted child with realised
malignancy and nephrocalcinosis. It fails the safety seat's constraints before the mechanism
is even argued.

### Net

**Nothing changes.** One finding sharpens the chaperone picture in the direction C47 and the
safety seat already pointed; three corroborate demotions; one is a new arm that arrives
pre-refuted. Across both batches — fifteen files, ten distinct analyses — no conclusion in
`TRACK2-REPORT.md` has moved, and the two findings that *did* move our position came from
primary papers (**C48**), not from any of these bundles.
