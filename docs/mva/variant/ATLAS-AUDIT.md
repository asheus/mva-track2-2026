# Audit of BUB1B-MUTATION-ATLAS.md

Run under `.claude/skills/fact-check`: every literature claim checked at primary
source, every pipeline number re-derived through a **different path than the one that
produced it** (Law 1 — producer ≠ verifier).

The atlas was produced from the EBI Proteins aggregate. It is therefore re-derived here
against **ClinVar directly via NCBI eutils**, which is a different source and a different
query path, not a re-run of `variant_atlas.py`.

**Two claims are materially wrong and one headline result is qualified.** Details below,
worst first.

---

## 1. REFUTED — "the EBI aggregate is near-complete for deposited variants"

The atlas closed with that sentence. ClinVar directly holds **2,493** BUB1B records
against the aggregate's 1,629, **101** pathogenic/likely-pathogenic against 69, and
**854** benign/likely-benign against 102.

Most of the gap is a category mismatch and not a miss: ClinVar's total includes **612
synonymous** and **456 intronic** records that a *protein*-variation endpoint cannot
represent. Protein-altering records in ClinVar come to roughly 1,592, against the
aggregate's 1,629 — those reconcile.

But the claim as written is still wrong in two directions at once:

- the aggregate **omits** every non-coding variant ClinVar holds, including splice
  alleles that `NEUROSNAP-TOOLBOX.md` separately identifies as real MVA alleles;
- the aggregate **adds** UniProt assertions ClinVar does not carry as pathogenic (see §3).

**Corrected claim:** the aggregate is near-complete for *protein-altering* variants, is
blind to the non-coding half of ClinVar, and is not a superset or a subset of it.

## 2. QUALIFIED — the AUC 0.963 is substantially a burial effect

This is the finding that most changes what the branch should say.

The powered calibration reports ProteinMPNN-ddG separating pathogenic from benign
missense in the pseudokinase domain at **AUC 0.963**. Re-derived against relative solvent
accessibility from `data/rsa_all.json` — a single geometric number computed with no
stability predictor of any kind:

| | median RSA | |
|---|---|---|
| pathogenic missense (n=5) | **3.4%** | 0.3, 0.6, 3.4, 3.6, 16.3 |
| benign missense (n=28) | **31.6%** | |
| **AUC of burial alone** | **0.875** | |

**Burial alone reaches 0.875 where ΔΔG reaches 0.963.** ΔΔG predictors read burial, so
most of the separation is available without them. With five positives the increment is
not statistically distinguishable from zero.

This does not refute "the stability axis separates these classes". It refutes the
stronger reading that the predictors are contributing the separation. The defensible
statement is: **pathogenic missense alleles in this domain are buried and benign ones are
exposed; ΔΔG methods recover that, and are not yet shown to add to it.**

It also exposes an ascertainment mechanism rather than a bug: disease missense alleles
get published from buried, structurally consequential positions, while tolerated variants
are catalogued from exposed ones. The classifier is partly learning how variants come to
be reported.

*(N1002K sits at RSA 14.0% — more buried than the benign median, less than the other
positives. Its position in this argument is real but not extreme.)*

## 3. CONFOUND — positives and negatives come from different curators

| | asserted by |
|---|---|
| I909T, L1012P, L844F, Q921H | **UniProt alone** |
| Q950E | Ensembl alone |
| R814H | ClinVar + Ensembl + NCI-TCGA + UniProt |
| all 28 benign | Ensembl and/or ClinVar — **none by UniProt** |

**4 of 6 positives are UniProt-only; 0 of 28 negatives are.** Label and source are almost
perfectly correlated, so the test could in principle separate curators rather than
biology.

This is mitigated but not removed. UniProt's calls here are literature-curated MVA alleles
from Hanks 2004 and Suijkerbuijk 2010, and **four of them carry direct functional
measurements** (5–10× reduced protein) rather than assertions — the positives do not rest
on annotation alone. ClinVar lacks them as pathogenic missense because old literature
alleles were never deposited as such by a clinical lab, not because ClinVar disputes them.

ClinVar direct holds **1,497 missense records but only 1 classified pathogenic/likely
pathogenic**, which independently corroborates the atlas's central structural claim:
missense pathogenicity in this gene is rare and truncation is the mechanism.

## 4. CORRECTED — two phenotype descriptions were wrong at source

- **p.Val870Ala (PMC11352340).** Recorded as "tumour-suppressor variant table, cancer
  genomics cohort". The paper is *"The Personalized Inherited Signature Predisposing to
  Non-Small-Cell Lung Cancer in Non-Smokers"* (Cancers, 2024) — a **germline** signature
  in **non-smoking NSCLC**. Corrected in the addendum.
- **p.Arg770Ter (PMC5894988).** Recorded as "described as causing premature chromatid
  separation trait". The paper is a **cutaneous melanoma with ≥2 independent primary
  cancers** germline cohort (PLoS One, 2018), and its exact words are *"which **as
  previously described** could cause premature chromatid separation trait"* — the paper is
  **citing** prior work, not demonstrating it. Law 2: affiliation ≠ authorship. Recorded
  as secondhand.

## 5. VERIFIED at primary source

| claim | verdict |
|---|---|
| Q921H "indistinguishable from wild-type … both on protein level and functionality" | **verbatim, confirmed** (PMC2887387) |
| Q921H and L844F on one allele; "L844F … the likely cause" | **verbatim, confirmed** |
| `p.Trp803Hisfs*10`, `c.2405_2406insCC`, maternal, het, "This study" | **confirmed**; fetal absent nasal bone + hypertelorism |
| `p.Glu213Glyfs*15`, `c.638del`, lung cancer, n=1, age 57 | **confirmed**; same paper reports `p.(Arg67Ter)` in 3 carriers (2 breast, 1 ovarian) |
| `p.I941T` is **KIAA1804**, not BUB1B | **confirmed false positive** |
| all four new alleles carry explicit `BUB1B` gene attribution in-window | **confirmed** |
| 6 consequence-type corrections in the aggregate | **confirmed** by allele inspection |
| 62 of 285 pseudokinase positions unseen; absence ~22% by chance | **holds** |

## 6. Unresolved, carried forward

- ~~**R770Q vs R770Ter**~~ — **RESOLVED 15 Sep 2026.** Located the primary source for our
  R770Q entry: PMC11306263, a 2024 forensic case report of sudden unexpected postnatal
  collapse. It gives `c.2309G>A`, rs1422532977, compound heterozygous with
  `p.Arg194Ter` (`c.580C>T`, rs28989186, paternal). The aggregate's nonsense allele is
  `c.2308C>T`, rs750364303. **Two distinct variants at adjacent nucleotides of one codon** —
  our transcription was correct and there is no parsing error. What was wrong is the
  weight: the presentation is **SUPC, not MVA**, death was from sepsis after
  hypoxic-ischaemic encephalopathy, the variant is a **VUS (ACMG class 3)** that the paper
  says "is not reported in scientific literature", and the authors write *"it is not
  possible to demonstrate the causal effect of this mutation"*. The "architectural match"
  framing is downgraded in `VARIANT-TABLE.md`.
- **Hanks 2004 remains unobtainable.** Abstract retrieved (five families, two with
  embryonal rhabdomyosarcoma, truncating and missense) but the variant table is in the
  body, and Nature Genetics 2004 has no PMC deposit and is not in Paperclip by DOI or
  PMID. UniProt's curation of it — R550Q, R814H, L844F, I909T, each cited to PMID
  15475955 — stays the best available proxy and is secondhand.
- **R550Q** — our corpus says measured fully functional, the aggregate says Pathogenic.
- The four splice alleles remain unscored by anything.

## What this audit changes

`STABILITY-AXIS.md` and the atlas must not claim the stability predictors are carrying
the calibration. They recover a burial signal that a solvent-accessibility number already
carries at AUC 0.875. The four functionally-measured alleles remain the strongest evidence
in the branch, and they are measurements, not annotations.
