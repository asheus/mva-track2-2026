# Repurposing candidates for a child with BUB1B-associated mosaic variegated aneuploidy

**Rare Disease, Real Kid: The MVA Hackathon 2026 — Track 2 (Drug Repurposing)**
**Maaz Asher Khurram** &mdash; mk7790@nyu.edu  
Proband WGS_EX2312012. Updated 24 Oct 2026.

> **These are hypotheses for follow-up, not evidence that any medicine works.**
> Nothing here is clinical advice, and no proposal below has been tested in
> mosaic variegated aneuploidy or in this child.

---

## 1. Summary

We carry **two therapeutic theses**. They are ranked, and the ranking changed late
in this work when we asked which one is actually aimed at this child's lesion.

**Lead — Thesis B: raise the amount of BubR1 the child still makes.**
Allele 2 (`p.Asn1002Lys`) is a **folding-class** variant: the protein is made,
misfolds, and is cleared by chaperone-dependent quality control. That is a druggable
axis with approved agents, and it is the only route where mechanism and paediatric
safety currently coincide. The candidate is **arimoclomol**, an HSF1 co-inducer
FDA-approved as Miplyffa on 20 Sep 2024 for Niemann–Pick type C in children aged two
and over.

**This report's first draft named sodium phenylbutyrate (4-PBA) instead, and the
reversal is the clearest single illustration of how it was audited.** 4-PBA was chosen
partly *because* it is an HDAC inhibitor: we counted that as a third mechanism pointing
the same way. It points the other way. HDAC inhibition induces premature sister
chromatid separation and strips BubR1 from kinetochores (Magnaghi-Jaulin 2007; Dowling
2005), and MVA1's other name is **premature chromatid separation syndrome**. Either the
activity is live at achievable exposure and the drug partially phenocopies the disease,
or it is not live and the third leg was never there. There is no reading in which it
counts in favour. 4-PBA remains the better-characterised paediatric agent and is kept
as a stated alternative with that hazard attached; arimoclomol carries the matched
mechanism without it (`CORRECTIONS-2026-10-06.md`, C5 and C7).

**Adjunct — Thesis A: blunt the senescence-associated secretory phenotype.**
**Anakinra and canakinumab**, reached by a six-gate screen of **5,202 molecules**
in which three independent instruments converged on the IL-1 axis. This was our
original lead. It is retained because the screen behind it is sound and the
convergence was not engineered, but it treats a *downstream consequence*; Thesis B
treats the lesion.

**Two findings make Thesis B specific to this disease rather than borrowed from
another protein.** First, aneuploid cells **lose HSF1 and HSP90** and cannot mount a
heat-shock response — so this child's aneuploidy depletes the very folding capacity
that would buffer a destabilised BubR1, and a chaperone co-inducer restores a
depleted system rather than augmenting a normal one (§3.3). Second, the field
excludes chaperone candidates when the active site is affected; **N1002 sits 26.7 Å
from the ATP site**, so the pocket is intact and the lesion is purely in the fold —
the configuration this drug class is built for (§3.2).

**And one thing is ruled out rather than merely untested.** BubR1's pseudokinase
domain has **no ligandable allosteric site that is not already a functional site** —
a 757-fragment screen on a validated instrument found its one non-functional groove
indistinguishable from bare protein (§3.4). That closes the *pharmacological*
chaperone route, which binds the target directly. It leaves the lead intact, because
neither candidate binds BubR1: both act in ***trans*** on folding capacity — 4-PBA as
a chemical chaperone, arimoclomol through HSF1 — a distinction this report is careful
to keep.

**Why the order flipped.** Thesis A's premise rests on two human datasets that
disagree (§5). Thesis B's premise — that N1002K is a folding variant — is the one
we could test, and did: within the folding class, stability prediction separates
pathogenic from benign at **AUC 0.879–0.920** against a burial-matched null
(permutation *p* ≤ 0.0052 at every matching window), where pooling mechanism classes had destroyed the signal
entirely (AUC 0.714, *below* burial alone). See `SYNTHESIS.md`.

**Self-assessed verdicts, reported separately:**

| | thesis | verdict | the binding uncertainty |
|---|---|---|---|
| **B** | allele-2 stabilisation | **mechanistically grounded, magnitude probably insufficient; carries a tumour-promotion hazard** | dose anchor retracted (C6); BubR1 is an RMS survival dependency (C4) |
| **A** | IL-1 / SASP blockade | `interesting_under_supported` | two human datasets disagree by cell type |
| **C** | aneuploidy-selective killing (KIF18A) | **refuted on one of two original grounds** | SAC-routed killing holds; the "no euploid compartment" ground was retracted (C2) |

**A third arm, and it is the one the clinical record forces.** `CHEMOSENSITIVITY-ARM.md`.
Antimitotic chemotherapy kills by triggering **checkpoint-dependent mitotic arrest** — and
this child's checkpoint is genetically crippled, which is the diagnosis. Vincristine is a
backbone of rhabdomyosarcoma therapy, the tumour this child has already had. Germline
*BUB1B* variants that **reduce BubR1 expression and stability** — precisely this lesion —
drive taxane resistance via premature mitotic exit, and direct *BUB1B* knockdown shifts
antimitotic IC50 roughly tenfold.

That reframes the task from *what drug can we add* to **which approved drugs will and will
not work in this genotype** — and it gives the lead a second, far more measurable
rationale: if low BubR1 blunts checkpoint-dependent chemotherapy, then raising it is
potentially **chemosensitising**, testable as an adjunct rather than only as a chronic
disease-modifier. The honest limits are set out in full in that document; the largest is
that the direct drug evidence is taxane rather than vincristine, which is a cheap
experiment away.

**A fourth arm, tested and refuted — and the refutation is the most useful result in this
section.** `ANEUPLOIDY-SELECTIVE-ARM.md`. Rather than fix the checkpoint, kill the
chromosomally unstable cells: **KIF18A** inhibitors do exactly that, are in clinical
trials, and spare chromosomally stable cells. It fails here twice over. First, KIF18A
inhibition kills *through* SAC activation — and the published rescue experiment in the
osteosarcoma study is **BubR1 siRNA**, this child's lesion, which abolishes the killing.
Our second original ground — that CIN-selectivity needs a euploid compartment to spare —
is **retracted** (C2): the real axis is transformed vs untransformed (Janssen 2009:
untransformed fibroblasts could not be sensitised), and MVA is mosaic, so a euploid
fraction exists. What survives is narrower and still useful: a selectivity argument must
name the contrast it actually relies on.

Together those two arms state one rule, derived from the genotype rather than from any
single drug:

> **The direction of effect of SAC deficiency on cytotoxic therapy is not fixed. It is
> conditioned on the observation window, on achieved drug concentration, and on which of
> BubR1's two functions — checkpoint signalling or chromosome alignment — the lesion
> impairs.**

An earlier version of this section stated a one-directional rule: that any SAC-routed
therapy would underperform here. **That is retracted** (`CORRECTIONS-2026-10-06.md`, C1).
Three primary sources carry the opposite sign — Lee 2004 (robust arrest *is* resistance;
BubR1 RNAi *reversed* paclitaxel resistance), Janssen 2009 (taxol sensitisation came
specifically from reducing BubR1, a dual-function protein, and *not* from reducing Mad2),
and Dowling 2005 (checkpoint inactivation potentiates microtubule-drug killing).

Cohen-Sharir 2021 (Nature 590:486–91) resolves the apparent contradiction in the cell
population that matters here: aneuploid cells are *less* sensitive to **short-term** SAC
inhibition but become *increasingly* sensitive **over time**, because they keep dividing
and accumulate unstable, less-fit karyotypes. The sign flips with the window. Our original
rule took the 72-hour sign and extrapolated it to clinical response, which is precisely
the extrapolation that paper forbids.

**The symmetric half, which we had never written down:** any chronic agent that *degrades*
SAC function is contraindicated in a SAC-deficient child. Applied honestly it convicts our
own lead — 4-PBA is an HDAC inhibitor, and HDAC inhibition induces premature sister
chromatid separation and strips BubR1 from kinetochores (C5). MVA1's other name is
premature chromatid separation syndrome.

**Every high-risk intervention ever reported in this syndrome supports the same
conclusion, and that is stronger than the statistics we had been citing (C28b).**
`MVA-THERAPEUTIC-EVIDENCE-BASE.md` tabulates them, and they split by *what they aimed at*
rather than by how aggressive they were. The ones that **removed or treated a consequence**
worked: tamoxifen gave sustained complete remission of a *MAD2L1BP* granulosa cell tumour;
surgery alone carried a *MAD1L1* patient through 12 neoplasias to no new pathology since
2014; a renal transplant at 20 under ciclosporin was tolerated in *BUB1B* MVA1. The ones
that tried to **repair or replace the system** failed: growth hormone in *CEP57* was
ineffective and regretted in print, G-CSF and romiplostim gave "no response", and
antiepileptics did not control the seizures.

**The sharpest case is HSCT in MVA1 — the same gene as this child.** A TCRαβ/CD19-depleted
matched-unrelated graft on treosulfan-based reduced-intensity conditioning **achieved its
mechanistic goal**: it engrafted, was well tolerated, and **cleared the monosomy 7 clone**.
Then graft rejection on day +47, pancytopenia, multi-organ sepsis, and **death on day
+156**. The authors state plainly that this *"needs to be taken into consideration for HSCT
in other MVA patients."* It is not a treatment that failed to work; it is a treatment that
worked and whose own complications killed the patient. Any proposal in this syndrome has to
be read against that.

**Neither thesis outranks surveillance, and the clinical record strengthens that.** This
child's presenting event was **rhabdomyosarcoma** — the predicted tumour type, already
realised (§2) — so what is owed is *survivor* surveillance for relapse and second
primaries rather than prophylaxis. `STANDARD-OF-CARE.md` establishes that expected
benefit from LFS-style tumour surveillance done well — 5-year survival 59.6% → 88.9%,
in a tumour spectrum that clusters in the first three years of life — is almost
certainly greater than from any repurposed drug we can currently propose. If one
thing is acted on, it should be surveillance. Everything below is hypothesis
generation for follow-up, ranked honestly, and it does not compete with that.

---

## 2. Variant mechanism

**Genotype.** Compound heterozygous *BUB1B* (chr15q15.1), consistent with mosaic
variegated aneuploidy syndrome 1 (MIM 257300, MONDO_0009759).

| Allele | Coordinate (GRCh38) | HGVS | Effect | Evidence |
|---|---|---|---|---|
| 1 | chr15:40,209,701 T>G | `c.2210T>G` | **p.Leu737Ter** — truncating | rs759242053; ClinVar **pathogenic** for MVA1 |
| 2 | chr15:40,220,612 T>G | `c.3006T>G` | **p.Asn1002Lys** — missense | this **nucleotide** change is not in ClinVar, but the **same protein change** is: VCV004600147.1 (`c.3006T>A`), **VUS**, 19 Sep 2025 (C16); AlphaMissense **0.9229, likely_pathogenic** — but see C43: AlphaMissense fails its direction check on this protein's measured panel, so this score is reported for completeness and is **not** treated as evidence |

Both were confirmed by Ensembl VEP against transcript ENST00000287598, **and both are
present in the proband's own VCF** — heterozygous and PASS, at high confidence
(`proband/confirm_variants.py`). The derivation and the child's data agree. Allele 2
is absent from ClinVar, so before running VEP we independently derived it by
reconstructing the reading frame from three annotated neighbours (R999Q at
40,220,602; N1004S at 40,220,617; D1005E at 40,220,621), which agree to the base
pair. The reconstruction and VEP give the same answer.

**Direction of effect: loss of function.** Allele 1 truncates 314 residues from a
1,050-residue protein. Domain annotations on ENSP00000287598 place the BubR1
kinase domain at **750–1045** (CDD `cd14029` STKc_BubR1_vert) or **782–1042**
(Gene3D 1.10.510.10), with a tighter kinase-like core at 791–984 (SuperFamily
SSF56112). p.Leu737Ter therefore stops translation **immediately upstream of the
kinase domain on every annotation, removing all of it** — not merely part.

Allele 2, p.Asn1002Lys, falls **inside** the domain on the BubR1-specific CDD
model and on Gene3D, but **outside** the tighter SuperFamily core. The structure
settles what the annotations leave ambiguous: in AlphaFold `AF-O60566-F1`,
**residue 1002 has pLDDT 91.1 — "very high" confidence**, sitting in a
well-ordered region (kinase domain mean 82.8). Residue 737 has pLDDT 73.6 and sits
at the boundary of a disordered linker (residues 600–749 mean **44.8**). So
p.Leu737Ter truncates at the end of a disordered segment immediately before the
ordered catalytic module and removes all of it, and p.Asn1002Lys substitutes a
residue in a confidently-folded part of that module — which is where a missense
substitution is most likely to be structurally consequential. The Mad3/Bub1 homology
region (Pfam PF08311, 57–179) is unaffected by either allele.

**Transcript-level evidence (AlphaGenome).** Both variants were scored with
AlphaGenome over a 524 kb window centred on BUB1B, against a null built from 12
random SNVs inside the same gene:

| scorer | null median | null max | L737* | N1002K |
|---|---:|---:|---:|---:|
| RNA_SEQ | 0.0132 | 0.0202 | 0.0101 | **0.0476** |
| SPLICE_SITES | 0.0059 | 0.0078 | **0.0244** | 0.0117 |
| SPLICE_JUNCTIONS | 0.0318 | 0.0870 | **0.1769** | 0.0722 |

p.Leu737Ter scores **above the within-gene null maximum** on both splice scorers —
roughly 2x on junctions and 3x on splice sites. That is consistent with a
transcript-level consequence, most plausibly **nonsense-mediated decay**, which
matters here specifically: NMD is what makes allele 1 a true null rather than a
stable truncated protein, and the null-plus-hypomorph argument below depends on
that distinction. p.Asn1002Lys's strongest signal is expression, also above the
null maximum.

Two limits travel with this. Absolute effect sizes are small (0.01–0.18) and the
null is only 12 variants, so this is suggestive rather than established. And
AlphaGenome scores regulatory and splicing effects, **not** protein-level
pathogenicity — a low score is never evidence that a nonsense variant is benign.

**Evolutionary constraint (GPN-Star).** A third predictor, orthogonal to the other
two: GPN-Star (Ye et al., *Nature* 2026,
[DOI](https://doi.org/10.1038/s41586-026-11005-5)) scores constraint learned from
whole-genome alignments with an explicit species tree. Both variants were looked up
in the authors' precomputed genome-wide log-likelihood ratios and ranked against
**every other possible SNV in BUB1B** (n = 180,342), on all three published human
timescales — the paper reports task-dependent advantages of recent versus deep
evolution, so no single timescale is privileged:

| | primate 243-way | mammal 447-way | vertebrate 100-way |
|---|---:|---:|---:|
| **L737\*** | −6.35 (1.3rd %ile) | −6.73 (1.5th %ile) | −6.87 (1.3rd %ile) |
| **N1002K** | −5.68 (1.9th %ile) | **−7.78 (0.9th %ile)** | −7.42 (1.0th %ile) |
| *null median* | *−0.27* | *−0.78* | *−0.20* |

**Both variants fall in the most-constrained 1–2% of all possible BUB1B SNVs on
every timescale**, roughly ten to thirty times more negative than a typical variant
in the gene. N1002K is markedly more constrained on the deeper mammal and vertebrate
alignments than on primates alone, which is what deep conservation of a residue looks
like — consistent with its position in the confidently-folded kinase core above.

So three predictors trained on three different signals — protein-level
(AlphaMissense), transcript-level (AlphaGenome) and evolutionary (GPN-Star) — agree
on both alleles. None of the three was selected after seeing the others.

**That agreement is worth less than this report originally claimed, and the reason is
measured.** AlphaMissense was tested on this protein's own measured panel — five variants
with 5–10× reduced BubR1 by western, two measured normal — and it ranks only **one of the
five** above both normals. `Q921H`, measured normal, outscores four of the five
measured-destabilising variants; `R814H`, measured at 5–10× reduced, scores 0.22
(`missense_arm.py`, CORRECTIONS C43). A predictor that points the wrong way four times in
five on this protein's measured variants does not get a vote on allele 2, so
**AlphaMissense's 0.9229 for N1002K is withdrawn as evidence** and the agreement above
rests on two predictors, not three.

The verdict hinges on `Q921H`: drop it and all five destabilising variants clear the
remaining normal, turning 1/5 into 5/5. There is a real case for dropping it — it sat on
the same allele as `L844F`, the authors attributed causality to `L844F`, and it was never
tested as the only variant on an allele. It is kept anyway, for the same reason §3.5 keeps
the weaker posterior: discarding the one inconvenient data point is not how a number is
obtained.

The null-plus-hypomorph architecture is what makes
MVA1 survivable — biallelic complete *BUB1B* loss is embryonic lethal — so a
viable patient essentially must carry one truncating and one partial-function allele.

**Pathway disrupted.** BUB1B (BubR1) is a core component of the **spindle assembly
checkpoint** (SAC), which delays anaphase until every kinetochore is correctly
attached. Loss of SAC function permits anaphase with unattached or mis-attached
chromosomes, producing the constitutional mosaic aneuploidy that names the disease.

**Downstream consequence, and why it is genotype-specific.** Not all MVA carries
tumour risk. Yost et al., *Nature Genetics* 2017
([DOI](https://doi.org/10.1038/ng.3883)) state that "individuals with biallelic
TRIP13 or BUB1B mutations have a high risk of embryonal tumors, and here we show
that their cells display severe SAC impairment. MVA due to biallelic CEP57
mutations, or of unknown cause, is not associated with embryonal tumors and cells
from these individuals show minimal SAC deficiency." **Risk tracks the severity of
checkpoint impairment.** This child is in the high-risk group by genotype, not by
inference. The associated tumour spectrum is embryonal broadly — Wilms tumour,
**rhabdomyosarcoma**, leukaemia, Sertoli–Leydig tumours — and the association is
constitutional rather than somatic: Hanks et al., *Cancer Letters* 2005
([DOI](https://doi.org/10.1016/j.canlet.2005.08.006)) screened 30 Wilms tumours,
10 ALLs and 20 rhabdomyosarcomas and found somatic *BUB1B* mutations "unlikely to
be common in sporadic childhood cancers."

**The prediction is realised, not prospective — and that is the strongest
genotype–phenotype evidence in this report.** The clinical record
(`PHENOTYPE-GROUNDING.md`, HPO terms) shows the proband's presenting event was
**rhabdomyosarcoma (HP:0002859)** — the malignancy that triggered urgent
investigation. That tumour type sits inside the embryonal spectrum Yost assigns
specifically to biallelic *BUB1B* with severe SAC impairment. So the chain
*genotype → severe SAC impairment → embryonal tumour* is not an inference this
report makes about a child at risk; **it is an observation about a child in whom it
already happened.** The record's other features corroborate the rest of the model:
intrauterine growth restriction (HP:0001518), short stature (HP:0004322), failure to
thrive (HP:0001508) and skeletal muscle atrophy (HP:0003202) are the growth-restriction
picture BubR1 hypomorph mice show, which is the dose–phenotype relationship §3.1
reasons from. And **parental recurrent spontaneous abortion (HP:0200067)** is
independent support for a heritable biallelic mechanism — each parent carrying one
allele — which is what the unphased *trans* inference needs and what a *cis*
arrangement would not produce.

**Three things this changes downstream, which earlier drafts did not carry.** Cancer
risk is **realised**, so surveillance shifts from prophylaxis to *survivor*
surveillance for relapse and second primaries. A child treated for rhabdomyosarcoma
has had **cytotoxic therapy**, which bears directly on the IL-1 arm's infection risk
(§4.2) and on marrow reserve. And **nephrocalcinosis from birth (HP:0000121)** is a
renal finding that any chronic agent in a small child has to answer to — including
4-PBA's sodium load (§3.5).

**The constraint this places on any repurposing proposal, and the escape from it.**
A missing checkpoint cannot be pharmacologically restored — there is no agonist for a
truncated kinase. That reasoning drove the original search entirely toward *downstream
consequences*, and we pursued three: aneuploidy-induced senescence and its secretory
phenotype; cancer predisposition; and a ciliopathy axis (Miyamoto & Matsuura,
*Oncotarget* 2015, [DOI](https://doi.org/10.18632/oncotarget.5244)). That became §4.

**But the premise is only half true, and the half it misses is the lead.** It holds
for allele 1, which is a true null. It does **not** hold for allele 2: `p.Asn1002Lys`
is a missense variant in a confidently-folded domain, so the protein is *made*. If it
is destabilised rather than catalytically dead, the target is not a missing function
to be agonised but a **protein abundance to be raised** — and that is upstream of every
downstream consequence at once. §3 tests that premise and follows it.

---

## 3. The lead — raise the protein the child still has

A missing checkpoint cannot be restored pharmacologically: there is no agonist for a
truncated kinase. But this child is not checkpoint-null. Allele 2 makes protein. The
question Thesis B asks is whether we can make it make **more**.

### 3.1 How much more, and can either allele supply it?

Taking one wild-type allele as 50 units of a 100-unit diploid normal, the estimated
baseline here is **~17 units** (`estimate_bubr1_dosage.py`). Two targets bracket the
ask: **~35 units** is the milder published comparator where the phenotype is
attenuated (**~2×**), and **~50 units** is carrier-equivalent, where MVA does not
appear at all (**~3×**). Full derivation in `WHICH-ALLELE-TO-TARGET.md`.

| route | ceiling | feasible in this child? |
|---|---|---|
| Allele 1 — **readthrough drug** | **+0.5 units** against a needed +18 | **No — dead on arithmetic** |
| Allele 1 — **NMD inhibition** | **+40 units** | best ceiling; no safe drug exists |
| Allele 2 — **stabilisation** | needs ~2× | **the only open route** |

**Readthrough is not merely unproven here — it is quantitatively insufficient, by
~35-fold.** Across ~5,800 pathogenic PTCs measured head-to-head, median readthrough
ranges from 0.08% (gentamicin) to 1.32% (SJ6986); the *top decile* reaches 4.28% at
best. This child's PTC is a **poor substrate on three of the three known context
rules** — the +1 nucleotide is A, the −1 is G, and the upstream codon is GAG, all
unfavourable. Only the UGA stop identity favours readthrough, and we had previously
over-read that single feature. And readthrough acts only on NMD survivors: the PTC
sits **747 nt** upstream of the last exon–exon junction, exceeding the 50–55 nt rule
thirteenfold, flanked by two truncations empirically confirmed transcript-null in
patients (731X, 753X). **Crossed off**, and with it DAP, ELX-02, and ataluren — whose
clinical failure now looks like what the biochemistry predicts.

**NMD inhibition has the only large ceiling and two blockers.** No NMD inhibitor is
approved anywhere for NMD inhibition. **Amlexanox is better credentialled than this
report previously said, and the earlier text — "a topical/short-course agent, not chronic
systemic dosing in an infant" — is withdrawn (23 Oct 2026).** It has decades of approved
use, an oral indication in Japan, and has completed a randomised, double-blind,
placebo-controlled **oral** trial in 42 adults (Oral et al. 2017, *Cell Metab*,
[PMID 28683283](https://doi.org/10.1016/j.cmet.2017.06.006)); it rescues **UGA** PTCs
functionally in patient-derived neuronal cells at 100 µM
([PMID 37513945](https://doi.org/10.3390/ph16071034)). The real blockers are different and
are set out in `ALLELE1-APPROVED-DRUGS.md`: the measured free Cmax (0.11–0.29 µM) falls
short of every reported effective concentration — by ~90–900× against the 25–100 µM
TBK1/TFEB separation, while a claimed 0.4 µM activity that would have narrowed the gap to
~1.4–3.6× could not be traced to any indexed publication, so it is recorded as an open
uncertainty rather than a correction (**C51**), amlexanox separately inhibits the innate-immune kinases
TBK1/IKKε, and NMD inhibition remains global. And the mouse data place the risk exactly where this child is
vulnerable — **neurological tissues were the most responsive to NMD change**, in a
child of this age on chronic systemic dosing. **Correction:** earlier drafts justified
this by saying the child's phenotype is dominated by microcephaly and developmental
delay. The clinical record lists neither — that was imported from the general MVA
literature and the hypomorph mouse (`PHENOTYPE-GROUNDING.md`). The neurotoxicity
concern stands on the mouse tissue data and on chronic dosing in an infant, but it is
**weaker than it was written**, and we say so rather than keep a convenient reason.
Whether
the 1–736 protein would even function is unresolved (our estimate: ~70/30 that it
behaves like the rescuing 731X rather than the failing 753X, from a two-point
calibration on orphaned hydrophobic surface). **Best ceiling, no safe way to reach it
today.**

So allele 2 is not chosen because it is better. Its ceiling is lower. It is chosen
because it is the only one where mechanism and an acceptable safety profile coincide.

### 3.2 The premise, and how we tested it

Thesis B stands or falls on one claim: **N1002K is a folding variant**, not an
interface variant. If it is not, chaperone amplification is aimed at the wrong
mechanism and the whole arm collapses.

We tested it by first discovering that the question had been asked wrong. Pathogenic
*BUB1B* missense alleles split into two mechanism classes, and stability prediction
applies to only one:

| class | example alleles | ΔΔG AUC | what is broken |
|---|---|---:|---|
| **binding interface** — TPR, GLEBS | R36Q, T40M, K400E | **0.364** — worse than chance | the partner contact (KNL1, BUB3) |
| **folded core** — pseudokinase | R814H, L844F, I909T, L1012P | **0.952** | the fold itself |

Pooling them destroys the signal (whole-protein AUC 0.714, *below* burial's 0.760) —
which is what every earlier number that looked unstable actually was. Split correctly,
this reproduces **Suijkerbuijk 2010's two-class model** from structure alone, where the
original came from westerns.

The serious objection is that ΔΔG predictors read solvent accessibility, so this could
be a burial result wearing a costume. Tested directly — each pathogenic variant compared
only against benign variants of similar RSA, permutation null shuffling labels *within*
matched sets:

| matching window | ±5% | ±10% | ±15% | ±20% |
|---|---|---|---|---|
| ProteinMPNN-ddG AUC | 0.879 | 0.889 | **0.920** | 0.917 |
| permutation *p* | 0.0052 | 0.0046 | 0.0008 | **0.0006** |

Stable at every window; logistic regression gives ΔΔG a slope of **−2.53** against
burial's **−0.22**. Three predictors agree on ranks at Spearman 0.88–0.91, and one
(EvoEF2) is a force field rather than a network, so the agreement is not shared
training data. **N1002K is placed 2nd, 3rd and 4th worst** of the eleven corpus
variants in its domain by the three methods.

**What is supported and what is not.** *Destabilising* is supported. *Severely
destabilising* is not — magnitude is method-dependent. The mechanism is **positional,
not chemical**: lysine is only the 10th worst of 19 substitutions at 1002, but the
site is the **21st most intolerant of 285**. "This position cannot take substitution"
is supported; "lysine's charge clashes" is not. The neighbouring-residue puzzle
resolves cleanly — **N1004 ranks 256th of 285**, two adjacent residues at opposite
ends of the tolerance distribution.

Confidence that N1002K is a folding variant: **high, but still inference.** Nothing
here measures BubR1 abundance in a cell.

**And "does it fold?" is the wrong binary.** The pharmacological-chaperone field
targets mutants that are *"intrinsically active but unstable"*, whose activity is low
*"because they are cleared by the quality control system"* — a protein that cannot
fold at all is not a candidate; one that folds but spends too long unfolded is exactly
the candidate. Destabilising-but-not-severe is the amenable profile, not the hopeless
one.

**The field's exclusion criterion is that a chaperone is "of no use if the active site
is affected", and we measured it** (`dock_audit.py`):

| residue | distance to ATP-site centre |
|---|---:|
| **N1002 (proband)** | **26.7 Å** |
| W978 (top VUS nomination) | 28.5 Å |
| L1012 (known pathogenic) | 18.7 Å |
| K795 (VAIK lysine) | 2.4 Å |

N1002's closest approach to the catalytic lysine is 28.6 Å: **the nucleotide pocket is
untouched.** We had been filing that as a disappointment — nothing there to fix. It is
the opposite. A lesion in the fold with the site intact is the one configuration this
drug class is built for. The same rule **excludes allele 1 outright** — chaperones are
"not useful ... in which the protein is absent because the gene is affected by ... a
stop gain mutation" — which is the dosage conclusion of §3.1 reached independently,
by the field's own eligibility rule.

### 3.3 The candidate, and why the ranking inside the class reversed

The axis is **raising folding capacity in *trans***, and two mechanisms do it:

1. **Chemical chaperone** — assists folding directly, which is the actual lesion.
2. **HSP70 / HSF1 induction** — raises quality-control capacity. Treatments that
   induce Hsp70 restored activity to **17 of 18 (94%)** disease-causing missense CBS
   mutants, and the same treatments rescued mutant p53 and MTHFR
   (Singh et al. 2010, PLoS Genet, [PMID 20066033](https://doi.org/10.1371/journal.pgen.1000807)).
   An earlier study rescued four CBS mutants with osmolyte chemical chaperones, and
   found the rescuable ones were those predicted to *decrease* solvent-accessible
   surface area (Singh et al. 2007, [PMID 17540596](https://doi.org/10.1016/j.ymgme.2007.04.011)).

   **The caveat this precedent carries, added 23 Oct 2026 (C47).** The three treatments
   achieving that 94% were **ethanol, proteasome inhibitors, or deletion of the *Hsp26*
   small heat-shock gene** — and the paper states Hsp70 induction is **"necessary but
   not sufficient"** for rescue. None of the three is pharmacological HSF1 co-induction:
   two are not givable to a child and one is a yeast deletion. So the 94% establishes
   that *this mutation class is rescuable by shifting the chaperone environment*, which
   is the load-bearing claim. It does **not** establish that raising Hsp70 alone
   achieves it. Any magnitude transferred from this paper to arimoclomol inherits the
   insufficiency clause, and the report previously cited the number without it.

Both candidates reach that axis. **4-PBA** does (1) and (2); **arimoclomol** does (2)
by co-inducing HSF1, which is the transcription factor aneuploid cells are *depleted
of* (§3.3 below, and the reason this class is disease-specific here rather than
borrowed).

**A third mechanism was originally counted and has been retracted.** 4-PBA is also an
HDAC inhibitor, and we read that as favourable: HDAC2/3 remove the protective K250
acetylation that shields BubR1 from APC/C degradation, so inhibiting them should
*preserve* it. That reasoning is incomplete to the point of being backwards. HDAC
inhibition **induces premature sister chromatid separation and overrides the spindle
assembly checkpoint**, with loss of MAD2 from the kinetochore, transcription-
independently (Magnaghi-Jaulin 2007, Cancer Res 67:6360–67,
doi:10.1158/0008-5472.CAN-06-3012), and abrogates BubR1 kinetochore localisation and
phosphorylation specifically (Dowling 2005). This child's syndrome is named for
premature chromatid separation. 4-PBA is a weak, millimolar HDAC inhibitor, so whether
the activity is live at therapeutic exposure is genuinely open — but both answers are
bad for the argument: live, and it partially phenocopies the disease; not live, and the
third leg does not exist. The general rule, which this report had not written down
until the audit forced it: **any chronic agent that degrades SAC function is
contraindicated in a SAC-deficient child.** Applied honestly it convicted our own lead
(`CORRECTIONS-2026-10-06.md`, C5).

**Arimoclomol carries the matched mechanism without that liability**, and is
FDA-approved — Miplyffa, 20 Sep 2024, Niemann–Pick type C, children aged two and over,
in combination with miglustat. Four of our own documents had described it as "phase 3
in ALS" with a "thin paediatric history", which was eighteen months out of date (C7).
It is not an HDAC inhibitor.

**What 4-PBA still has, and why it is kept rather than dropped.** Two things
arimoclomol does not. First, **selectivity evidence**: in RPE65 missense disease, PBA
left wild-type expression unchanged while significantly raising the three mutants — it
raises the unstable allele without over-raising normal protein, which matters when the
protein is an oncogene-adjacent mitotic regulator. Second, **paediatric depth**:
approved for chronic management of urea cycle disorders, a neonatal-onset indication,
decades of use, multiple formulations. That is not a theoretical profile; it is babies,
for years — and it reaches below arimoclomol's age-two floor.

So the honest statement is not that one agent won. It is that the class is right, the
mechanism-matched member of it has no checkpoint liability and is approved, and the
member with the deeper paediatric record carries a hazard pointed directly at this
child's syndrome. **Both are hypotheses for follow-up. Neither has ever been tested on
BubR1** (§5).
**Carried, not buried:** the FDA review of Ravicti (glycerol phenylbutyrate) flagged
*"potential neurotoxicity in pediatric patients under two years of age"* and required
post-marketing PK studies in infants. Sodium load and palatability are real issues in
chronic paediatric dosing.

| | mechanism match | magnitude precedent | paediatric safety | verdict |
|---|---|---|---|---|
| **Arimoclomol / HSF1 co-inducers** | correct (chaperone amplification), no checkpoint liability | rescues glucocerebrosidase, destabilised rhodopsin | **FDA-approved (Miplyffa, 20 Sep 2024) for NPC in children ≥2**; not an HDAC inhibitor | **lead** (C7) |
| 4-PBA | folding + QC, **but HDAC inhibition phenocopies premature chromatid separation** | 94% rescue of CBS missense ([PMID 20066033](https://doi.org/10.1371/journal.pgen.1000807)) — but by ethanol/proteasome/*Hsp26*-deletion, with Hsp70 induction "necessary but not sufficient" (C47); mutant-selective; wild-type-sparing | approved, neonatal indication — reaches below age 2 | **demoted to stated alternative** (C5) |
| SIRT2 activation / NAD+ | **wrong degradation route**, plus a K250 hazard | strong — but in a hypomorph, not a folding mutant | not used in this indication | **demoted** |
| Proteasome inhibition | correct route | rescues in vitro | not viable chronically in a child | no |
| HSP90 inhibitors | **actively harmful** | — | — | **standing refusal** |

**The SIRT2 demotion is the argument that decides this ranking**, and it demotes
where this workstream was heading. Suijkerbuijk showed misfolded BubR1 is cleared by
**chaperone-dependent quality control** — levels collapse under HSP90 inhibition,
proteasome inhibition rescues. The SIRT2/K668 axis is a different route: CBP
acetylation driving ubiquitination of the *normally folded* protein, i.e.
**physiological turnover**. Our problem is quality-control triage. Not the same
pathway. *(A sequence check en route: the literature disagrees on whether the SIRT2
site is K668 or K688. Against `ENSP00000287598`, residue 668 is K and 668–675 is
`KLSPIIED`, an exact LxxIxE PP2A-B56 motif; residue 688 is **S**. The "K688" papers
have the number wrong.)* SIRT2 also deacetylates the protective K250, and the
acetylation-defective knock-in mouse is **embryonic lethal when homozygous** — 339
live animals monitored, no homozygous newborns. Not a residue to perturb in a child
whose disease is already chromosomal instability plus cancer predisposition.

**HSP90 inhibitors remain refused outright**: they remove virtually all destabilised
BubR1 — this child's entire supply.

#### The argument that makes this arm specific to MVA rather than borrowed

Everything above is a mechanism-*class* argument: 4-PBA works in other proteins, so it
might work here. One finding makes it specific to this disease.

**Aneuploid human cells have consistently lower HSF1 protein, downregulated HSP90, and
a profound defect in mounting the heat-shock response — and constitutively active HSF1
rescues their protein-folding defect.**

That closes a loop. Destabilised BubR1 → weakened checkpoint → aneuploidy → **HSF1 and
HSP90 fall** → less folding capacity → more BubR1 cleared. This child's cells are
chronically aneuploid by definition of the diagnosis, so the chaperone capacity that
would buffer a destabilised protein **is itself depleted by the phenotype that protein
causes.**

This re-founds the HSP70-inducing arm on a stronger claim. Not "raises quality-control
capacity", which is true of any cell, but **restores capacity this disease measurably
removes**. It also confirms the HSP90 refusal from an unrelated direction: aneuploid
cells are already *significantly more sensitive* to HSP90 inhibition than diploids.

**What it does not settle, and we are not choosing a side.** Depleted capacity could
mean a capacity-restoring drug delivers more than the generic 1.5–3× range — or it
could be exactly why such a drug underdelivers here. Both readings are available. It
is a reason to measure HSF1 and HSP90 in patient cells, not a reason to claim a
larger effect. Full treatment in `BINDING-AND-STABILISING.md`.

### 3.4 What we tried, and failed, on the structural side

We attempted to make this a **structure-guided** proposal rather than a
mechanism-class analogy. Two sampling methods agree the BubR1 pseudokinase ATP site
carries **cryptic druggable volume**; if a ligand could occupy it, the chaperone idea
becomes a pose. Ten ligands were docked blind into the domain — ATP as positive
control, metformin as negative, deucravacitinib because it binds the TYK2
**pseudokinase** domain and is the nearest clinical precedent.

**Zero of ten landed within 12 Å of the ATP site. ATP itself finished 38 Å away.**

A positive control that misses by 38 Å does not refute a target; it says the
instrument is wrong. Two artifacts explain it, and both are diagnosable
(`DOCKING-AUDIT.md`, reproduce with `dock_audit.py`):

- **The truncation scar.** Five structurally unrelated drugs converged on residues
  **824–835** — every residue of which is occluded in full-length BubR1 by the
  737–764 linker, **209 deleted contacts** across the site. It is not a binding
  site; it is the scar left by carving the domain out, and it captured the entire
  top of the score distribution including the best pose (imatinib, −8.80). On
  surface that survives intact, nothing scores better than −7.24.
- **A rigid receptor cannot enter a cryptic pocket.** The pocket's **apo volume is
  0 Å³** — cryptic means closed in the apo coordinates. Vina holds the receptor
  rigid. The experiment could not have succeeded.

**The run is uninformative about the site, not evidence against it.** We report it
because reporting that −8.80 pose as a hit — which is what this would have looked
like without the occlusion check — would have been a fabricated lead in a document
about a real child.

**What it changes upstream is the point: nothing.** The arm that survives does not
need a pocket. 4-PBA does not occupy a site on BubR1; it raises folding capacity in
*trans* and never touches the target. That is why §3.3 ranks it on mechanism match
and paediatric safety rather than on affinity, and why a failed docking campaign
leaves it exactly where it was.

**We then ran the protocol that does it properly, and it returned a clean negative.**
Millet and co-workers rescued uroporphyrinogen III synthase by docking an **allosteric
surface site**, fragment-screening it, validating by thermal shift and NMR, and then
searching approved drugs for lookalikes — which found **ciclopirox**, an approved
antifungal. Run on BubR1 with a validated instrument (`MILLET-PROTOCOL.md`):

- **Site selection excluded every good pocket for cause.** The one open, persistent,
  cross-method-reproducible pocket is lined by **His880 and Phe912** — the catalytic
  spine. The other druggable ones are lined by **Leu1031/Leu1035**, the CENP-E
  interface. An inhibitor is not a chaperone. A second, independent detector (LIGSITE
  on the static structure) found exactly one pocket free of both: **134 Å³ at residues
  814–820 / 864–875 / 891–905**, intact in full-length, built from four distant
  sequence segments and so genuinely native-state selective.
- **The instrument was validated first**: re-docking crystal complexes recovered
  **3 of 4 poses under 2 Å** (imatinib in ABL at 1.03 Å), and seed-to-seed SD is
  **0.012 kcal/mol**.
- **757 fragments × 5 boxes. The target site is the best box for zero of them** —
  identical to a flat-surface control, against 48% for the ATP site. Its median score
  is 0.15 kcal/mol from bare protein. **0 of 757 clear a 1% empirical false-positive
  rate** against a null built from the decoys themselves.

**The conclusion is stronger than "we found nothing":** the BubR1 pseudokinase domain
has **no ligandable allosteric site that is not already a functional site**. The site
we found is geometrically real but shallow — real ≠ druggable. And the controls behaved
exactly as the earlier audit predicted, with the truncation scar scoring near the top,
which is what licenses reading this as a measurement rather than another void run.

**How far that generalises, stated precisely (added 14 Oct 2026, C26b).** All five boxes
lie inside residues 766–1050, so read strictly this is a result about one domain, and
earlier drafts of this report used it as though it closed the structure-guided route for
the whole protein. It does close it, but the argument has to be made rather than assumed:
**the pseudokinase domain is the only part of BubR1 that structure prediction models with
any confidence.** The degradation-determining lysines — K250, where acetylation shields
BubR1 from APC/C, and K668 — sit at pLDDT 47.5 and 30.2, in the long intrinsically
disordered middle region that makes BubR1 a scaffold. There is no surface there to place
a pocket on. So the negative extends to the whole protein not because we screened the
rest but because the rest is not screenable, and that distinction is the honest form of
the claim (`ALLELE2-ROUTES-REEXAMINED.md`, `millet/degron_dockability.py`).

This also closes a route the field has used on another gene with exactly our problem.
In Friedreich ataxia — where residual frataxin level likewise sets disease severity and
no fold-stabilising pocket exists — **ubiquitin-competing molecules** that bind the
substrate and block its own ubiquitination raise frataxin in patient cells. The published
recipe uses consensus pocket detection (LIGSITE among eight detectors) and AutoDock/Vina,
both of which we have validated, with site selection concentrated on the ubiquitination
lysine. Such a molecule need not stabilise anything, so our fragment negative does not
exclude it — the disorder at K250 and K668 does.

**A route that needs no stabilising site at all.** A DUBTAC is a PROTAC run backwards:
a ligand for the target linked to **EN523, which binds the deubiquitinase OTUB1**, so
the chimera strips the K48 degradation chain instead of adding one. `NJH-2-057`
(lumacaftor + EN523) raises ΔF508-CFTR **above what lumacaftor achieves alone**. The
requirement drops from *"find a molecule that stabilises the fold"* — which our
structure work could not deliver — to *"find a molecule that binds"*. A follow-on
platform used a **DNA motif** as the targeting arm, so it need not even be drug-like;
BubR1 has four characterised interaction motifs that could serve. **No DUBTAC is
approved anywhere and none has been made against BubR1** — this is a research
direction, not a proposal for this child. It is here because it is the only route
that survives the absence of a druggable pocket.

### 3.5 What Thesis B does not establish

- **Nobody has ever tested 4-PBA, or any chaperone inducer, on BubR1.** Not once.
  Every precedent above is a different protein. This is a mechanism-class argument.
- **The magnitude is at the edge.** Chemical chaperones typically deliver 1.5–3×
  rescue. We need ~2× for the attenuated phenotype and ~3× for carrier-equivalent.
  That is the optimistic end of the observed range, not the middle.
- **It rests on N1002K being an abundance lesion — quantified, not asserted.**
  **P(abundance) = 0.79, 95% CI 0.44–0.98** on the measured kinase-domain panel
  (5 of 6 destabilising; `scripts/mva/abundance_posterior.py`). Dropping the sole
  exception gives 0.92 (0.62–1.00), and there is a documented reason to: Q921H sat on
  the same allele as L844F and the authors attributed causality to L844F, so it was
  never tested as the only variant on an allele. **The weaker figure is the one that
  ships**, because discarding the one inconvenient data point is not how a headline
  number should be obtained.
  **One physicochemical axis survives external validation; the other does not, and the
  difference was measured rather than argued.** N1002K is the **only variant in the
  comparison that buries a NEW formal positive charge**, at RSA 12.9% and pLDDT 91.1;
  every charged panel member *loses* charge instead. That axis is now externally
  supported: against **measured** steady-state protein abundance in three independent
  multiplexed assays (PTEN and TPMT VAMP-seq, NUDT15), burying a charge costs abundance
  and doing it at the surface costs nothing — ρ −0.210/−0.209/−0.140 at buried positions
  against +0.037/−0.003/+0.031 at exposed ones, on 4,907 buried measured variants
  (`burial_dependence_test.py`, CORRECTIONS C41).


  **§3.5a — what the lysine specifically breaks.** "Buries a charge" is a category, and a
  category cannot be falsified in a lab, so the model's own atoms were asked which
  interaction a lysine at 1002 destroys (`n1002k_mechanism.py`, C42).

  It is **not** a like-charge repulsion variant. Within 8 Å of the N1002 side chain there
  is exactly one charged group — Arg999 at 6.95 Å, carrying +0.33 of a guanidinium — for a
  signed burden of **+0.047 e/Å**, which is negligible, and there are **zero** negative
  charges, so a buried lysine would have no counter-charge either. The mechanism is
  desolvation of an *unpaired* buried charge.

  What it does break is one bond. N1002's amide makes three hydrogen bonds:
  `OD1 ← Trp978:N` at 2.83 Å, `ND2 → Val998:O` at 2.83 Å, `ND2 → Trp978:O` at 2.95 Å.
  Asn carries **both** a donor and an acceptor; lysine's NZ **donates only**. The two ND2
  donations could in principle be satisfied by a lysine; the **OD1 ← Trp978:N contact
  cannot be**, leaving a backbone amide without its acceptor at RSA 13.7%.

  This is not the W978 packing claim VUS-NOMINATION.md withdrew. That argued outward from
  N1002 to say `W978L` was an independent prediction, and died because the contact shell is
  statistically empty — 5 of its 10 residues above their burial-matched median, 5 below.
  This runs inward, names one backbone hydrogen bond, and does not depend on the shell.

  Tested against all 19 substitutions at position 1002 — groups fixed from the mechanism
  before the scores were read — AlphaMissense orders them as the mechanism predicts
  (donor-only-and-positive 0.904, no-polar 0.885, acceptor-and-negative 0.841,
  **acceptor-and-neutral 0.685**), and `N1002S` at 0.348 is the only substitution there it
  does not call likely-pathogenic. Three things cut against it and are stated rather than
  smoothed: 18 of 19 are likely-pathogenic, so this explains gradation and not intolerance;
  the three worst are Trp, Phe and Pro, meaning the dominant signal at 1002 is **sterics**,
  the axis that failed external validation; and `N1002Q` scores 0.907 while keeping both
  donor and acceptor, so preserving an acceptor is not sufficient. Ordering *within* one
  position is also a weaker claim than ranking across the protein, which is the claim C43
  shows AlphaMissense cannot support here.

  N1002K's side-chain volume change of **+54.5 Å³** was previously offered as a second,
  independent axis. **It is withdrawn as support.** On the same measured-abundance data,
  volume change shows no burial dependence in PTEN or TPMT and *reverses* in NUDT15
  (−0.176, CI excluding zero). The number is still true and still inside the panel's
  destabilising range; what it no longer has is external evidence that it predicts
  abundance where a residue is buried. One validated axis is a weaker claim than two, and
  it is the claim we have.
  **It remains the single load-bearing assumption in Track 2 and it has not been
  measured in this child.** A posterior over six comparators bounds a belief; it does
  not observe a protein level, and the CI's lower bound is 0.44.

  **And the support is narrower than it was, because we tested it (C43).** The
  buried-charge axis is validated against measured protein abundance in three other
  proteins, but asked whether it transfers to *BUB1B's own* labelled variants it **fails**:
  2 of 19 pathogenic missense bury a new charge against 2 of 100 benign — a fivefold odds
  ratio in the right direction, at p = 0.1193. That failure is structural rather than
  accidental, since 55 of this gene's 69 pathogenic alleles truncate and only 19 missense
  carry a pathogenic label at all. So the axis is **not demonstrated in this gene**, and
  the allele-2 abundance argument rests on cross-protein transfer plus the specific
  hydrogen bond in §3.5a. Across the whole arm the axis applies to **50 of 1,494** missense
  variants; for the other 1,444 `missense_arm.tsv` records why it does not apply rather
  than substituting the volume axis that failed in C41a.
- **4-PBA's HDAC inhibition is broad**, and broad epigenetic modulation in a
  cancer-predisposed infant raises questions this analysis does not answer.
- **The renal phenotype argues against the lead's formulation, and we did not see it
  until late.** The record shows **nephrocalcinosis from birth (HP:0000121)**. Sodium
  phenylbutyrate carries a substantial sodium load, which `STABILISATION-STRATEGY.md`
  raised only as a palatability and dosing nuisance. Against a kidney already
  depositing calcium it is a different objection, and it is one the glycerol
  formulation (Ravicti) was designed to avoid — except that the same FDA review flagged
  potential neurotoxicity under age two. **Neither formulation is clean here**, and
  that trade needs a nephrologist rather than this analysis.
- **No molecule proposed here binds BubR1, and none can be.** The fragment screen
  (§3.4) found no ligandable allosteric site, so this arm rests entirely on
  *trans*-acting proteostasis and would not be rescued by a better docking run.
  Any future claim that a small molecule stabilises BubR1 **directly** contradicts
  this result and needs to answer it.
- **Allele 2 is made as protein — now established by elimination, not assumed.**
  It could have failed to produce protein three ways: NMD (excluded twice over —
  no stop codon is created, and the variant is in the final exon where a PTC
  escapes decay by construction), cryptic splicing (**excluded by measurement
  14 Oct 2026**: Pangolin gain +0.01 / loss 0.00, stable at window widths of 50,
  300 and 1000 nt, with a positive control reproducing its committed score
  exactly — §3.6, `SPLICE-ALLELE2.md`), or not at all. So the open question is
  **two-way, not three-way**: abundance or function.

### 3.6 Where computation stops, and what that means for this submission

This is worth stating directly rather than leaving as an apology in a limitations
list, because it defines what the deliverable actually is.

**Computation settled more here than is usual, and all of it by exclusion:**

| question | settled by | result |
|---|---|---|
| which allele can a drug reach? | readthrough arithmetic | allele 1 is ~35× short — *quantitatively* insufficient, not merely unproven |
| is allele 1's transcript destroyed? | calibrated decay model | P(escape) 0.316 — predicted decay, with the residual stated |
| could allele 2 escape translation? | Pangolin, control-validated | no — gain +0.01, three window widths |
| is there a druggable site on the target? | 757-fragment screen, validated instrument | no — 0 of 757 at 1% FPR |
| which mechanism class is allele 2 in? | measured comparator panel | folding class at an **83% base rate** (5 of 6) |
| is any drug class contraindicated by the genotype? | mechanism-derived gate rule | yes — chaperone inhibitors, invisible to any interaction check (§4, C25c) |

**What computation cannot settle, and no amount more of it would:** whether allele
2's lesion is *abundance* (protein scarce, chaperone-amplification on-target) or
*function* (protein present, each molecule working poorly, so raising the amount
achieves nothing). Those need opposite interventions.

But "cannot settle" is not "has nothing to say", and the distinction matters to anyone
deciding whether this arm is worth pursuing. The question is **quantified**:
**P(abundance) = 0.79, 95% CI 0.44–0.98**, from the measured kinase-domain panel, with
two independent physicochemical axes agreeing (§3.5). Note what does *not* carry the
argument: burial. The panel's one tolerated variant is *more* buried than allele 2, so
a burial-based reading would get this wrong — what separates them is **buried charge
introduction**, the one axis that survives testing against measured protein abundance
(C41). Substitution volume was previously named alongside it and is withdrawn: on the
same measured data it shows no burial dependence, and reverses in one of three assays.
So the honest statement is not "we don't know", and it is no longer "two independent
axes agree" either. It is "about four-to-one on, on six comparators, with one externally
validated physicochemical axis rather than two, and the lower bound of that interval
is 0.44."

**So the deliverable is a ranked, falsifiable hypothesis with its discriminating
experiment specified — not a drug recommendation.** The experiment is cheap and needs
no patient material: ectopic LAP-BubR1 N1002K versus wild-type versus **Q921H as the
internal negative control**, which is the assay built in 2010 and is a plasmid, a
transfection and a blot. It would convert the single largest inference in this
workstream into a measurement, and it would also settle the magnitude question that
C6 retracted.

**And the experiment has a name, a threshold and a regulatory precedent — it is not our
invention.** Fabry disease has had a formal, FDA- and EMA-sanctioned version of exactly
this question for a decade, called **amenability**: a variant is amenable to chaperone
therapy if it yields *"abnormally folded or less stable proteins with retained enzymatic
activity"*, which is word-for-word the abundance-versus-function distinction. It is
decided by a **GLP-validated in vitro assay** — HEK-293 cells transfected with the
specific mutation, incubated with drug — and a variant is amenable on a **≥1.2-fold
increase over baseline plus a ≥3% absolute increase in wild-type activity**. **600** mutant forms were expressed in HEK-293 and **268** found
amenable (Benjamin et al. 2017, Genet Med 19:430-438), and the current product
information carries **376** distinct amenable entries, counted off the label by
`fabry_precedent.py`. (A figure of "1,386 variants" appeared in earlier drafts of this
report, was never sourced, and is retracted — C44.) So our proposed blot should be specified as an amenability
determination against those criteria, not as a bespoke experiment.

The same precedent carries an uncomfortable implication we should state rather than
leave for a reviewer to notice: **the company that commercialised this strategy built an
assay, not a predictor**, and ran it per variant, hundreds of times. That is the field's own verdict on
whether computation settles this question, and it agrees with the paragraph above rather
than with our posterior. See `HOW-OTHERS-SOLVED-IT.md`.

**Our problem is also not unusual, which is the strongest thing to say about
generalisability.** Reduced protein abundance is *"the most frequent mechanism by which
rare missense variants cause disease"*, with surveys putting **40–60% of pathogenic
variants** in that class. And in the one protein where the question has been answered
exhaustively — the vasopressin 2 receptor — a multiplexed assay over *all possible*
variants found more than half of pathogenic ones poorly expressed, and a single
stabiliser **rescued 87% of the destabilised set**, with the non-rescued variants
falling on the drug's own binding site. A single molecule covering most of a variant
spectrum is the regime an n-of-1 patient needs.

### 3.7 The scalable version of this child's question

Everything above answers one question for one variant. The generalisation is a
**deep mutational scan of *BUB1B* with an abundance readout, run ± a chaperone
co-inducer** — which would classify every *BUB1B* variant as amenable or not **and**
test the drug, in one pooled experiment, on the template the V2R study established.
That converts an n-of-1 finding into something the next family can use, and it is the
honest form of the scalability claim: a proposal with a named precedent, not a result.

**One design constraint, which the precedents hide and we should not.** Every success in
this class — V2R, CFTR, α-Gal A — is a membrane or secreted protein with a trafficking
checkpoint, so surface expression or lysosomal delivery gives a readout you can sort
cells on. **BubR1 is a nuclear kinetochore scaffold; there is nothing to stain on the
surface.** A BubR1 scan needs a tagged-abundance reporter or a mitotic-phenotype readout
instead, and choosing between them is real experimental design rather than a detail.

Claiming that computation identified the mechanism would be the error. Declining to
name the experiment that would, having narrowed it to one two-way question, would be
the other.

---

### The gate gained a genotype-conditional refusal

Added 14 Oct 2026 (C25c). Every other rule in Gate 3 is a fact about the *drug*:
withdrawn, carcinogenic, cytotoxic, topical. This one is a fact about the **patient**.

Allele 1 is transcript-null, so this child's entire BubR1 supply is a destabilised
missense allele held up by chaperone-dependent quality control — and Suijkerbuijk 2010
measured that HSP90 inhibition removes virtually all destabilised BubR1. An HSP90
inhibitor would therefore deepen the precise deficit causing the disease. **No
drug–drug interaction check can see this**, because the interaction is not with another
drug; it is with the genotype.

It is implemented as a genotype condition rather than a drug blocklist, so it
generalises: the input is "the patient's functional allele is a destabilised missense
protein", not "the gene is *BUB1B*". For a patient with two truncating alleles there is
no destabilised protein to strip and the rule does not fire. Evidence tiers stay
separate — *measured* for HSP90, *inferred* for HSP70/HSF1, where the direction is
certain and nobody has measured it on BubR1 — and activators of the same targets are
untouched, since co-inducing HSF1 is the therapeutic hypothesis.

**It refuses nothing in the current funnel: 13 of 34 survive, unchanged.** No HSP90
inhibitor is approved, so Gate 1's approval tiering removes the class before Gate 3
sees it. That is reported rather than left silent, and `tests/test_gate3_chaperone.py`
demonstrates in seven cases that the rule can fire — including that it must *not* fire
on an activator, which would otherwise refuse our own lead.

---

## 4. The adjunct arm — IL-1 blockade

This was our original lead, and the work behind it stands: a six-gate screen of
5,202 molecules in which three instruments that were not tuned to agree converged
on one axis. It is now ranked **second**, for a reason worth stating plainly rather
than burying: **it treats a downstream consequence, and Thesis B treats the lesion.**
Its premise — that SASP output is elevated in this child — rests on two human
datasets that disagree (§5), and unlike Thesis B's premise we had no way to test it
here. It is retained, not demoted to a footnote, because if the folding thesis is
wrong this is what is left, and because the safety gate below is the most transferable
part of the whole method. *(Within §4 this arm is called **Arm A**, the funnel's
own terminology, alongside the cancer-predisposition and ciliopathy arms it was
run against.)*

### 4.1 Method — a six-gate funnel

Each gate asks one question, is implemented as a committed script, and reports
what it excluded as well as what it passed.

| Gate | Question | In | Out |
|---|---|---:|---:|
| 0 | Is it a real, publishable molecule? | 5,202 | 4,945 |
| 1 | Is it an **approved medicine**? | 4,945 | 1,485 |
| 2 | Does it act on a target an MVA mechanism runs through? | 1,485 | 34 |
| 3 | Is it safe **in this child**? | 34 | 13 |
| 4 | Does the thesis survive adversarial attack? | 13 | 13 (1 branch refuted) |
| 5 | Has it ever been given to a child? | 13 | 11 studied, **2 leads** |

Gate 1 replaced a filter we had planned and found wrong: requiring a WHO ATC code
is not an approval test, because ATC classifies substances irrespective of
approval. Approval is now tiered by regulator evidence, and the excluded tier is
retained so exclusions stay auditable.

Gate 2 is run in **both directions** — target→drug and drug→mechanism — because
Open Targets' clinical-candidate list is curated rather than exhaustive. This
caught a systematic blind spot: rapalogs are annotated on **FKBP1A, not MTOR**
(sirolimus binds FKBP12, and the complex inhibits mTORC1), so a target set naming
MTOR misses sirolimus and everolimus entirely. Any drug whose annotated target is
a proximal binding partner rather than the effector is invisible to single-direction
target screening.

---

### 4.2 Gate 3 — the safety gate refused our best candidates

This is the centre of the analysis, not a compliance step.

Arm A's strongest mechanistic hits and the worst safety risks are **the same
molecules**. Every TNF blocker (adalimumab, infliximab, etanercept, golimumab) and
most JAK inhibitors (tofacitinib, baricitinib, upadacitinib, abrocitinib) carry a
black-box **carcinogenicity** warning. In a child whose tumour risk arises from
chromosome missegregation — where immunosurveillance is part of what contains it —
that is disqualifying rather than a caution. Seven further candidates were refused
as ATC L01 antineoplastics **on mechanism**: adding DNA damage to cells that
already missegregate chromosomes is the wrong direction, independent of toxicity grade.

We deliberately carried the mitotic targets (AURKA, PLK1, TTK/MPS1, KIF11, WEE1)
into Gate 2 so the safety gate could be seen refusing them. **All return zero
approved drugs** — every agent against them is investigational. No approved-drug
screen can propose a mitotic poison to this child. The danger was real but unreachable.

**A finding that inverts the access argument.** None of the 13 survivors has a
biosimilar, because all five biosimilar-available molecules were refused on
carcinogenicity. For this child the affordable options are unsafe and the safer
options are expensive orphan biologics. **Access is the binding constraint on the
answer, not a closing remark.**

---

### 4.3 Gate 4 — we tried to kill our own thesis

The strongest objection is not immunosuppression. It is mechanistic:

> Senescence is a tumour-suppressive barrier. A child who continuously
> missegregates chromosomes depends on it. Suppressing senescence biology could
> remove a defence and *increase* tumour risk.

The objection has real support — Li et al., *Oncotarget* 2016
([DOI](https://doi.org/10.18632/oncotarget.7864)) conclude that p53-mediated
arrest, senescence and apoptosis "control genomic stability in vivo."

**The thesis survives because the objection conflates two separable things.**
Senescence *arrest* is the protective half. The **SASP** is the paracrine output
of cells that have already arrested, and it is tumour-promoting in surrounding
tissue: Coppé et al., *PLoS Biology* 2008
([DOI](https://doi.org/10.1371/journal.pbio.0060301)) show SASP from
**genotoxic-stress-induced** senescence — the state chronically aneuploid cells
occupy — drives invasiveness "by a paracrine mechanism that depended largely on
the SASP factors interleukin (IL)-6 and IL-8."

An anti-IL-1 or anti-IL-6 antibody does not stop a damaged cell arresting. It
blunts what the arrested cell secretes. **The barrier stays; the tumour-promoting
signal falls.**

#### What this refutes

| Intervention | Effect on the barrier | Verdict |
|---|---|---|
| SASP blockade (anti-IL-1, anti-IL-6) | arrest intact | survives |
| **Senolysis** (navitoclax, dasatinib+quercetin, BCL-2 inhibition) | **barrier removed** | **contested — see below** |

#### We ran this a second time, and it refuted us

Round 1 called senolysis a *positive refutation* and this report led with it. A
second adversarial round, searching specifically for what had been done in the BubR1
model rather than reasoning from senescence biology in general, found the opposite.

Baker et al., *Nature* 2011 ([DOI](https://doi.org/10.1038/nature10600)) — the
foundational senescent-cell-clearance paper — was performed **in the BubR1 progeroid
mouse**, the closest available model to this child's genotype: "life-long removal of
p16(Ink4a)-expressing cells delayed onset of these phenotypes… late-life clearance
attenuated progression of already established age-related disorders." Clearing
senescent cells in a BubR1-deficient animal **helped**.

The claim is **downgraded to contested, not reversed**, because three things limit
Baker as a counter: cancer incidence was not its primary endpoint, and tumour risk was
our actual concern; progeroid phenotypes are not the embryonal-tumour axis that
dominates this child's risk; and INK-ATTAC is genetic ablation, not a drug with
navitoclax's or dasatinib's toxicity in a child.

**Honest statement:** in the closest animal model senolysis improved healthspan;
whether it raises or lowers tumour risk in a SAC-deficient child is unresolved, and
our original claim was overstated. Full record in `GATE4-ROUND2-SELF-REFUTATION.md`.

#### The same search strengthened Arm A's premise

Rao, Asch & Yamada, *Molecular Carcinogenesis* 2016
([DOI](https://doi.org/10.1002/mc.22539)) states the mechanism this report had
inferred: mitotically damaged cells activate p21/p27/p16 and drive "tissue-level
senescence/aging through inflammatory paracrine mechanisms called SASP", and with
weakened immune surveillance under systemic CIN, surviving senescent and aneuploid
cells produce "an inflammatory, pro-tumorigenic, and senescent/aging microenvironment."

That cuts both ways, and we say so: it supports SASP blockade *and* it supports
senolysis. The two are better described as untested alternatives aimed at the same
pathology from different ends than as opposites.

#### The remaining objection, tested

Does blunting inflammation raise cancer risk? For IL-1 specifically the largest
randomised test went the other way. CANTOS (Ridker et al., *Lancet* 2017,
n=10,061, [DOI](https://doi.org/10.1016/S0140-6736(17)32247-X)) reports
dose-dependent reductions in incident lung cancer (HR 0.61 at 150 mg, **HR 0.33 at
300 mg**) and lung cancer mortality (HR 0.23 at 300 mg).

**We do not claim CANTOS transfers.** Different population, cancer and mechanism of
risk. It defeats only the general claim that IL-1β blockade is cancer-permissive.
And its cost travels with the claim: in the same trial "fatal infections or sepsis
were significantly more common in the canakinumab groups," and all-cause mortality
did not differ (HR 0.94, 95% CI 0.83–1.06). **An IL-1 proposal trades infection
risk for a hypothesised oncological benefit. That trade is the proposal.**

---

### 4.4 What the funnel returned

Gate 5 counted paediatric exposure from ClinicalTrials.gov eligibility ages rather
than asserting it. 11 of 13 survivors have been studied in children at phase 2+.

| | anakinra | canakinumab |
|---|---|---|
| Mechanism | IL-1 receptor antagonist | anti-IL-1β monoclonal |
| Paediatric studies (phase 2+) | **29** | **28** |
| Youngest eligibility seen | neonatal | neonatal |
| Gate 3 verdict | caution_immunosuppression | caution_immunosuppression |
| Carcinogenicity black box | none | none |

**The convergence was not engineered.** Gate 3 kept the IL-1 axis from regulatory
drug-warning data; Gate 4 found it is the one mechanism whose large randomised
evidence points away from cancer risk; Gate 5 found the same two molecules are the
best characterised in children. Three instruments, three data sources, one answer.

**A risk this arm did not price in.** Gate 3 flagged both leads
`caution_immunosuppression` on their labels. The clinical record adds a specific
reason: this child has been **treated for rhabdomyosarcoma**, so prior cytotoxic
therapy and its effect on marrow reserve and infection risk compound an IL-1 blocker's
own signal — and CANTOS already showed fatal infections and sepsis significantly more
common under canakinumab. The trade §4.3 describes gets worse, not better, in a
treated oncology patient. Any n-of-1 protocol has to be written against the actual
treatment history, which this analysis does not have.

**Proposed follow-up, in order** — and note that step (1) is the *same experiment*
that would settle Thesis B, on the same cells, which is the practical argument for
running both arms off one sample: (1) measure IL-1β/IL-6 and hsCRP **in primary
patient cells, not immortalised lines**, and include an interferon/NF-κB readout —
the cell-type caveat above is why, and the MAD1L1 single-cell data is why those
extra readouts belong in the panel. This is the missing evidence and it is
measurable; (2) if elevated, an n-of-1
protocol with explicit infection monitoring; (3) tumour surveillance continues
regardless, since nothing proposed here treats the underlying checkpoint defect.

---

## 5. Limitations

**On Thesis B (the lead):**

- **No chaperone inducer has ever been tested on BubR1.** Every precedent is a
  different protein. This is a mechanism-class argument, and it is the single
  largest gap in the lead.
- **The magnitude ask sits at the edge of the precedent.** ~2× for the attenuated
  phenotype, ~3× for carrier-equivalent, against a typical chemical-chaperone
  rescue of 1.5–3×.
- **Everything rests on a predicted structure.** No experimental structure covers
  N1002 at the resolution ΔΔG methods assume, and nothing here measures BubR1
  abundance in a cell — it predicts folding thermodynamics, one contributor among
  several.
- **Five pathogenic anchors carry the folding-class calibration.** They are
  source-confounded (4 of 6 positives asserted by UniProt alone, 0 of 28 negatives),
  mitigated only because four carry direct functional measurements rather than
  annotations. The negatives are annotations, not measurements.
- **There is no ligandable allosteric site, and this is now measured rather than
  assumed.** Our first structural attempt was *void* — a blind, rigid dock that
  scored its own truncation scar and never entered the ATP site (apo volume 0 Å³).
  We then ran the Millet protocol properly on a validated instrument, and it
  returned a **clean negative**: the one groove free of both the catalytic spine and
  the CENP-E interface is the best box for **0 of 757 fragments**, indistinguishable
  from bare protein, and **0 of 757 clear a 1% empirical false-positive rate**
  (§3.4, `MILLET-PROTOCOL.md`).
- **So the *pharmacological* chaperone version of this arm is closed**, and the
  distinction now matters: a pharmacological chaperone binds the target directly and
  needs a pocket we do not have. Both candidates are **proteostasis regulators acting
  in *trans*** — 4-PBA chemically, arimoclomol through HSF1 — and neither binds
  BubR1, which is why the lead survives a negative that kills the structure-guided
  route. The report should not
  be read as proposing anything that occupies a site on this protein.
- **The cryptic pocket's geometry is not reproducible between sampling methods.**
  They agree the ATP site carries cryptic druggable volume; they disagree on where
  and how much. Quote the claim, not the numbers — and note the screen found even
  the *open* pockets unremarkable, so cryptic volume is not a latent opportunity
  here.
- **The allele-1 route is closed on today's drugs, not permanently.** A selective
  NMD inhibitor with paediatric safety data would immediately outrank everything
  here on its +40-unit ceiling.

**On Thesis A (the adjunct):**

- **The tissue channel is observed but DISCORDANT, and this is what demoted this
  arm.** An earlier draft said no MVA expression cohort exists; that was
  wrong. GSE22206 profiles a homozygous *BUB1B* patient with confirmed MVA against
  controls and heterozygous relatives. Scoring Phoenix's axes on it puts the
  **Immune (SASP) axis DOWN in the proband (d = −1.75), dose-ordered across the
  allele series** — the opposite of Arm A's prediction. Three things bound that:
  n=2 per arm makes Cohen's d descriptive only; the cells are EBV-immortalised
  lymphoblastoid lines, which perturbs the very programmes being measured; and the
  better human dataset points the other way (below). Full analysis in
  `PHOENIX-HEADTOHEAD.md`.
- **Counterweight, on better tissue.** Villarroya-Beltri et al., *Science Advances*
  2022 ([DOI](https://doi.org/10.1126/sciadv.abq5914)) profiled a biallelic *MAD1L1*
  SAC-loss patient — an MVA variant — by single-cell RNA on **primary blood cells**,
  reporting "systemic inflammation with enhanced interferon and NFκB signaling both
  in aneuploid and euploid cells, suggesting a non-cell autonomous response." That
  is a paracrine mechanism in the direction Arm A predicts, and NF-κB is the
  regulator through which IL-1β signals.
- **The two human datasets disagree, and the disagreement is explicable by cell
  type** — immortalised lines versus primary cells. That is a real limit of the
  evidence, not a tie to split. The verdict stays `interesting_under_supported`:
  it does not rise on MAD1L1, and one n=2 immortalised-line comparison cannot sink it.
- **Trial channel remains empty.** No trial of any lead in a chromosomal
  instability syndrome.
- Paediatric trial eligibility is not approval, not safety in this child, and not
  evidence in a chromosomal instability syndrome.
- Gate 1's excluded tier contains false negatives — celecoxib is approved but
  absent from the centralised EMA table we screened on.
- Drug-name resolution reached 989 of 1,485 (67%); misses concentrate in vaccines,
  immunoglobulins and combination products.
- Metformin and dasatinib are geroprotection/senolytic candidates our target-first
  method structurally cannot reach.

**Cross-cutting:**

- **Both alleles are now confirmed in the proband's own callset** (this replaces the
  earlier limitation that they were not). `proband/confirm_variants.py` queries the
  challenge VCF directly: both sites are present, **heterozygous, FILTER=PASS, at maximum
  genotype quality**, at high read depth with allele balances consistent with
  germline heterozygosity rather than mosaicism, which matters in a mosaic-aneuploidy
  syndrome. The script prints only these two loci and writes no extract: the DTA
  forbids resharing, so what is committed is the query, not the data.
- **Trans configuration is still not proven, and this is now the precise gap.** The two
  sites are **10,911 bp apart** and the callset carries no physical phasing for either
  (GATK `PGT`/`PID` are null; short-read fragments cannot span that distance). Compound
  heterozygosity therefore remains an inference — from the diagnosis, and from the fact
  that a *cis* arrangement would leave one intact allele and would not cause disease.
  **The clinical record adds independent support**: parental recurrent spontaneous
  abortion (HP:0200067) is what a heritable biallelic mechanism produces, with each
  parent carrying one allele — and is not what *cis* predicts. Still not proof.
  **Parental genotyping remains the single cheapest decisive experiment available**, and
  it is the one we would run first.
- **The non-coding half of the gene IS scored, and this limitation was false.**
  Corrected 23 Oct 2026; the earlier text claimed "456 intronic and 612 synonymous
  ClinVar records... neither thesis currently sees them." Both halves were wrong. The
  denominators were stale (`clinvar_noncoding.tsv` holds **429** intronic, **563**
  synonymous and **13** canonical splice-site records, 1,005 in all), and the set was
  not merely seen but fully scored: `data/nmd/eligibility_map.tsv` carries **1,005 rows,
  every one with a direct Pangolin call plus exon frame arithmetic and none pending**,
  yielding **287 survivors** (60 `call`, 227 `candidate`) of which **40** fall in the
  `candidate_hypomorph_protein_made` tier — the exact class Thesis B addresses. The four
  known MVA-causing splice alleles are in it as scored calls (`c.751+1G>T`, gain 0.87 /
  loss −0.90; `c.2009+1G>A`, 0.73 / −0.89).

  **What the real limitation is, and it is a sensitivity limitation.** The arm is
  externally calibrated against MFASS on a sealed split
  (`data/nmd/mfass_benchmark_metrics.json`, n_scored **4,946**): **sensitivity 0.357**
  (95% CI 0.327–0.388), **specificity 0.986** (0.982–0.989), precision 0.860. So the map
  is a high-precision, low-recall screen: a positive call is usually right, and it misses
  roughly two thirds of real splice disruption. A negative is close to uninformative.
  That is the honest limitation and it should have been this bullet all along.

  **Why this correction matters more than the others.** A limitation asserting that an
  analysis does not exist is worse than an unstated one: it tells a reader the work was
  not done. This arm is the only component of the workstream with stated operating
  characteristics measured on held-out data in a different gene set, which makes it the
  most transferable thing here — and the report was actively denying it.
- **Source quality was a first-order problem, not a housekeeping one.** The protein-level
  variant aggregate carries seven distinct defect classes, all found by audit: six
  records typed `missense` whose allele is a stop codon, 41 whose wild-type residue
  contradicts the reference sequence (nucleotide letters in an amino-acid field —
  invisible because A, C, G and T are all valid residue codes, and one reached a
  nomination list), and 84 filed with cDNA coordinates in the protein-position field.
  All are handled once, in `variants/bub1b.py`. **No single source is complete and
  none fail the same way.**

Six defects of our own were found and fixed during this work — a target-annotation
blind spot, an ATC-group-as-route error, a trial age-unit error, a regex that silently
truncated frameshift variants, a residue check that rejected a real insertion allele,
and a variant that passed every automated filter while belonging to a different gene.
**Each was caught only by cross-checking one instrument against another**, which is an
argument for building funnels that disagree with themselves — and the docking audit in
§3.4 is the same principle applied to a result we wanted to be true.

---

## 6. Scalability

**The funnel (§4) is a parameterised script over public APIs** (Open Targets, Ensembl
VEP, ClinicalTrials.gov). Changing the mechanism arms — a target list with a written
rationale per target — retargets it at another gene or disease without touching the
machinery. The paediatric and safety gates are disease-agnostic. It applies wherever a
rare-disease genotype implies a pathway and one needs to know which approved drugs
reach it, and which must not.

**The stability axis (§3) scales differently, and further.** Once calibrated on a
gene's own pathogenic and benign alleles, it ranks every other variant in the same
domain for free. Applied here it nominates **30 of 203 pseudokinase-domain missense
VUS at a 4% empirical false-positive rate**, thresholded by specificity against 25
benign controls rather than against the weakest pathogenic anchor. ClinVar holds
1,497 missense VUS in *BUB1B* alone. The nominations are hypothesis-generating and
folding-mechanism only — and the top ones follow exactly N1002K's pattern, ordinary
substitutions at extraordinarily intolerant positions (`W978L`: 8th worst of 19 at a
position ranked 3rd of 285; `N1002K`: 10th worst of 19 at a position ranked 21st).

**The transferable method is the two-class split, not the predictor.** The result that
makes this work is that ΔΔG separates pathogenic from benign at AUC 0.952 inside the
folding class and 0.364 — worse than chance — across binding interfaces, so pooling
them destroys the signal. Any gene with both a folded domain and a protein-interaction
surface has this problem, and most variant-effect pipelines pool. Splitting first, then
testing against a **burial-matched** null so the result cannot be solvent accessibility
in disguise, is the part worth copying.

**And the negative controls are part of the method, not an afterthought.** Four results
in this report exist only because a control was run: the N1002K pocket effect that
benign controls reproduced exactly (structure preparation, not biology); the packing
shell that burial-matching showed was unconstrained; the docking campaign whose
best-scoring pose sat on our own truncation scar; and the fragment screen, where decoy
boxes turned "our site's best fragment scores −5.64" into "that fragment has a 34%
empirical false-positive rate" (§3.4).

**The transferable part is the shape of that last one.** Dock the target *and* the
protein's other real pockets, rank the difference rather than the score, and build the
null from the decoys themselves. It is the same move as the burial-matched permutation
above — control for the confounder, then ask whether anything survives — and it is what
separates a ligandability measurement from a ranked list of greasy molecules. Validating
the instrument first (crystal re-docking, seed variance) is the other half: a
systematically mistyped receptor is wrong at every box equally, so no decoy could
reveal it.

---

## Methods disclosure

**Provider:** Anthropic. **Interface:** Claude Code (cloud sessions). **Models:** Claude
Opus 5, with a short final segment on Claude Opus 5.5. **Setting:** commercial terms, no
training on customer content. **Plan/tier: `[TEAM TO COMPLETE BEFORE SUBMISSION]`** — the
organisers require provider, plan-or-tier and setting; the tier is an account fact this
analysis cannot verify about itself.

The AI's role was substantive and is stated plainly: it wrote every script, performed
the literature synthesis, and drafted these documents. It also produced the errors
listed under Limitations and, in several cases, the controls that caught them. All
numbers derive from committed scripts over public APIs, re-derived from raw records by
`verify_report.py`; all literature claims cite primary sources.

Full answers to the organisers' methods-description form are in
**`METHODS-DESCRIPTION.md`** (and `methods_description_track2_filled.xlsx`).

## Acknowledgement

> *"This work was made possible through the Hackathon, organized by Sage
> Bionetworks in partnership with the MVA Society, Hugging Face, and BEACON (The
> Benchmarking, Evaluation, and Assessment Consortium for Science), with prize
> sponsorship from AWS and Anthropic. We are deeply grateful to the child and
> their family who generously contributed their data and their story to advance
> research into this rare disease. We acknowledge their trust in making this
> Hackathon possible."*
