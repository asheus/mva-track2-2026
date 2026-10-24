# Corrections of 6 Oct 2026 — seven retractions, with sources

Five independent first-principles audits were run against this workstream on 6 Oct 2026.
Each was given the same brief and a different reasoning method. They converged on defects
this file records. **Every claim below was re-verified against the primary source before
retraction** — the audits are listed as the prompt, never as the evidence.

The common failure mode is worth naming, because it is more useful than any single fix:
this workstream repeatedly asked *what supports the thesis* and not *what would make it
wrong*. The phrase "three mechanisms all pointing the same way" (previously in
`STABILISATION-STRATEGY.md`) is the signature — three legs pointing one way is a reason to
check whether one of them points at the disease. One did.

---

## C1 — The SAC-dependency rule was one-directional. Sign is window-conditioned. **RETRACTED AS STATED.**

**Was:** *"Any therapy whose cytotoxicity routes through SAC-dependent mitotic arrest is
predicted to underperform in this child."*

Three primary sources carry the opposite sign:

- **Lee et al. 2004** (Mol Cancer Ther 3:661–69, PMID 15210851) — *"Cells that are
  relatively resistant to killing by these drugs block robustly in mitosis, whereas cells
  sensitive to killing block only transiently in mitosis before undergoing nuclear
  fragmentation and death ... Sensitivity to paclitaxel correlated with decreased BubR1
  protein expression ... Silencing of BubR1 via RNA interference ... reversed resistance to
  paclitaxel and nocodazole."*
- **Janssen, Kops & Medema 2009** (PNAS 106:19108–13, doi:10.1073/pnas.0904343106) —
  *"Sensitization to taxol was achieved by reducing levels of Mps1 or BubR1, proteins having
  dual roles in checkpoint activation and chromosome alignment, but not by reducing Mad2,
  functioning solely in the mitotic checkpoint."*
- **Dowling et al. 2005** (Cancer Biol Ther 4:197–206, PMID 15753652) — *"TSA abrogated the
  phosphorylation and kinetochore localization of the mitotic checkpoint protein BubR1 ...
  by inactivating the spindle checkpoint, TSA can potentiate the lethal effects of
  microtubule-disrupting drugs."*

**The resolution, and the replacement claim.** **Cohen-Sharir et al. 2021** (Nature
590:486–91, doi:10.1038/s41586-020-03114-6) measures both signs in the population that
matters here:

> *"aneuploid cancer cells were **less sensitive** than diploid cells to **short-term**
> exposure to multiple SAC inhibitors. Indeed, aneuploid cancer cells became
> **increasingly sensitive** to inhibition of SAC **over time** ... kept dividing when the
> SAC was inhibited, resulting in the accumulation of mitotic defects, and in unstable and
> less-fit karyotypes."*

So the sign flips with the observation window: short-term escape from arrest reads as
resistance; long-term karyotype deterioration reads as sensitivity. **This workstream took
the short-term sign and extrapolated it to clinical response.** The corrected claim is that
the direction of effect is conditioned on observation window, on achieved drug
concentration, and on *which of BubR1's two functions* (checkpoint signalling vs chromosome
alignment) a given lesion impairs — Janssen's Mad2-vs-BubR1 contrast being the direct
evidence that these dissociate.

**Consequence.** Any prescribing-adjacent phrasing that advised against vinca alkaloids or
taxanes rested on half the literature and is withdrawn. Nothing here is clinical advice.

## C2 — "No euploid compartment to spare" was the wrong axis. **RETRACTED.**

`ANEUPLOIDY-SELECTIVE-ARM.md` reason 2 argued CIN-selective agents cannot work in
constitutional aneuploidy because no chromosomally stable compartment exists. The relevant
axis is **transformed vs untransformed**, not aneuploid vs euploid: Janssen 2009 reports
*"untransformed human fibroblasts with reduced Mps1 levels could not be sensitized to
sublethal doses of taxol."* MVA is also mosaic, so a substantial euploid fraction exists.
Reason 1 (KIF18A kills through SAC activation; BubR1 siRNA is the published rescue) stands,
and Cohen-Sharir independently corroborates the KIF18A dependency. The corollary built on
reason 2 — "distrust every oncology-borrowed selectivity argument" — is withdrawn as
stated; the narrower true form is that a selectivity argument must name the contrast it
relies on.

**C2 refinement, same day — the axis is agent-class-specific, and for one class the
original conclusion was right for the wrong reason, and the true reason is worse.**
**C2 second amendment — I attributed Janssen's control to the wrong protein.** The
sentence I leaned on reads *"untransformed human fibroblasts with reduced **Mps1** levels
could not be sensitized to sublethal doses of taxol"* — **Mps1, not BubR1**. Janssen tested
the untransformed-cell control on Mps1 only, so "normal tissue is spared" is **unsupported
for the BubR1 arm** and my transformed-vs-untransformed framing overstated what that paper
licenses. The Mad2-vs-BubR1 dual-function contrast (C1) is unaffected; only the
normal-tissue inference falls. This is the second amendment to C2, both of them mine.

For Janssen's taxol result the contrast is transformed vs untransformed **for Mps1**. But the
*aneuploidy-selective* class (AICAR, 17-AAG, chloroquine; Tang, Williams, Siegel & Amon,
*Cell* 144:499–512, doi:10.1016/j.cell.2011.01.017) demonstrated its selectivity in
**primary, non-transformed trisomic mouse embryonic fibroblasts**, killing them by
**p53-mediated apoptosis**. A primary non-transformed aneuploid cell is a model of *this
child's own normal tissue*, not of his tumour. So the objection is not "there is no
euploid compartment to spare" (MVA is mosaic; there is one) — it is that this class is
aimed at the aneuploid fraction of his healthy tissue. That is a stronger
contraindication than the one withdrawn, and it is specific rather than borrowed.

## C3 — DNA-damaging agents are not "unaffected by this logic". **RETRACTED.**

The one published cytotoxic exposure in a biallelic-*BUB1B* patient was stopped by
toxicity. **Ochiai et al. 2019** (Pediatr Blood Cancer 66:e27804, doi:10.1002/pbc.27804) —
a 38-month-old with biallelic germline *BUB1B* and bilateral Wilms tumour: *"dactinomycin
monotherapy was administered for the left Wilms tumor; however, severe adverse reaction
prevented the patient from receiving further chemotherapy."* Dactinomycin is not an
antimitotic and sat in the row this workstream marked exempt. It is the only in-genotype
human pharmacology datapoint that exists, and it was absent from the file.

## C4 — Thesis B carries an unexamined tumour-promotion hazard. **ADDED.**

**Wan et al. 2012** (Cancer Res 72:5889–99, doi:10.1158/0008-5472.CAN-12-1991) — *"We
identified Bub1b as an essential element for the growth and survival of rhabdomyosarcoma
(RMS) cells ... Knockdown of Bub1b resulted in suppression of tumor growth in vivo,
including the regression of established tumors."* BubR1 is a FoxM1 transcriptional target
in RMS.

The lead proposes chronically **raising** BubR1 in a **rhabdomyosarcoma survivor**.
Cohen-Sharir adds a second line: aneuploid cells show *increased* sensitivity to genetic
SAC-component loss, so raising BubR1 may improve the fitness of the aneuploid
pre-malignant pool.

**C4 correction, same day — the first version of this entry was one-sided, which is the
same error as C1 and is recorded here rather than quietly fixed.** There is a direct
counterweight: Baker et al., *Nat Cell Biol* 15:96–102 (2013), doi:10.1038/ncb2643 —
*"sustained high-level expression of BubR1 preserves genomic integrity and **reduces
tumorigenesis**, even in the presence of genetic alterations that strongly promote
aneuploidization and cancer, such as oncogenic Ras,"* and it extends lifespan.

The two results are not in conflict once stated precisely, and the precise statement is
the useful one: **an established RMS tumour depends on BubR1 (Wan), while an organism with
sustained extra BubR1 forms fewer tumours (Baker).** So the hazard is narrow — it concerns
residual or recurrent RMS clones in a survivor, not raising BubR1 in general — and the
organism-level evidence for raising BubR1 is favourable. The lead's claim to lead on
safety needs this qualification, not a withdrawal.

This is also the sharpest unresolved tension in the file: the same gene is the germline
disease (too little BubR1) and the tumour's dependency (the tumour needs BubR1). One
systemic agent moves both.

## C5 — 4-PBA's HDAC activity points at the disease, not away from it. **RETRACTED as a supporting mechanism.**

MVA1's other name is **premature chromatid separation syndrome**.

- **Magnaghi-Jaulin et al. 2007** (Cancer Res 67:6360–67, doi:10.1158/0008-5472.CAN-06-3012)
  — title: *"Histone deacetylase inhibitors induce premature sister chromatid separation and
  override the mitotic spindle assembly checkpoint."* The effect was
  **transcription-independent**, with *"loss of the SAC component MAD2 from the kinetochore.
  Thus, HDAC inhibition renders the SAC ineffective."*
- **Dowling 2005** (above) — HDAC inhibition abrogates **BubR1** kinetochore localisation
  and phosphorylation.

4-PBA is an HDAC inhibitor and this workstream counted that activity as a third mechanism
*supporting* the thesis. Whether the activity is live at therapeutic exposure is a real and
open question (4-PBA is a weak, millimolar HDAC inhibitor). But the two outcomes are: the
activity is live and the drug partially phenocopies the disease, or it is not live and the
third mechanistic leg is inoperative. **There is no reading in which "HDAC inhibitor" is a
point in favour.**

**The symmetric half of our own rule, previously unwritten:** any chronic agent that
*degrades* SAC function is contraindicated in a SAC-deficient child. Applied honestly, it
convicts our own lead.

## C6 — The ~2–3× dose target is anchored on a separation-of-function allele. **RETRACTED.**

The target bracketed against patient MVA-41C at 35% residual BubR1. That patient's genotype
is **731X / Y155C**; 731X is transcript-null, so the entire 35% is Y155C protein, and
`bub1b-dosage-review/ESTIMATE.md:82` already records Y155C as **"not destabilising"** —
i.e. that patient has MVA at a normal-ish protein level, so their deficit is **functional,
not quantitative**. Matching their number does not reproduce their state. Protein level and
protein function are independent axes, and this bracket conflated them.

`ESTIMATE.md:42` had already written down the contradiction (*"Y155C is buried and scores
high, yet is measured neutral"*) and the estimate used the comparator anyway. The honest
ask is larger than 2–3× and is not currently well bounded; the verdict on magnitude moves
from *uncertain* to **probably insufficient on current evidence**.

## C7 — Arimoclomol is an approved paediatric drug. **CORRECTED, in our favour.**

Four documents described arimoclomol as *"phase 3 in ALS"* with *"thin paediatric
history"*. FDA approved **Miplyffa (arimoclomol)** on **20 Sep 2024** for Niemann–Pick
disease type C in adults and children **aged 2 years and older**, in combination with
miglustat. It is an HSF1 co-inducer — mechanism-matched to the HSF1/HSP90 deficiency of
aneuploid cells — and, unlike 4-PBA, it is not an HDAC inhibitor. It should be assessed as
the leading chaperone candidate rather than the second.

---

## What this costs and what it buys

Retracted: one flagship rule as stated, one refutation leg, one exemption row, one dose
target, one supporting mechanism, and the lead's unqualified safety claim.

Retained and unchanged: Track 1 (rank 1 of 20,104, 7/8 leave-one-out); the fragment-screen
negative (0/757 at 1% FPR, machinery validated by crystal re-docking); the two-class ΔΔG
split; the N1002K folding-determinant call; the readthrough arithmetic; and **surveillance
primacy** — all five audits independently agreed that well-executed tumour surveillance
outranks every pharmacological proposal here.

Gained: a window-and-function-conditioned replacement for the rule that explains why the
literature looks contradictory; the symmetric half of the rule; the only in-genotype
pharmacology datapoint; a named tumour-promotion hazard; and an approved paediatric
chaperone candidate.

## C8 — p53/p21 is protective in the tissue this child has a deficit in. **ADDED.**

Baker, Weaver & van Deursen, *Cell Rep* 3:1164–74 (2013),
doi:10.1016/j.celrep.2013.03.028: *"In response to BubR1 insufficiency, skeletal muscle,
fat, and lens tissue engage p19^Arf^ to attenuate senescence and age-related
deterioration ... p53 delays functional decline of skeletal muscle and fat in a
p21-dependent fashion by inhibiting p16^Ink4a^-mediated senescence of progenitor cells."*

This child has **skeletal muscle atrophy (HP:0003202)**. Two consequences, both
phenotype-specific rather than borrowed:

1. The aneuploidy-selective class kills by **p53-mediated apoptosis** (C2 refinement). It
   therefore acts against the axis that is protecting this child's muscle.
2. ~~**Senolytics are contraindicated for the same reason.**~~ **RETRACTED — see C14(a).
   I read this paper backwards.** The protective mechanism *is* senescence-suppression:
   p53/p21 protects muscle and fat *"by **inhibiting** p16^Ink4a^-mediated senescence of
   progenitor cells."* Clearing p16-positive cells therefore pushes the **same** way as the
   protective axis in those tissues, not against it. Point 1 above is unaffected, because
   it concerns p53-mediated killing of aneuploid cells rather than senescence.

Both are predictions from mouse genetics, not measured outcomes in a patient, and are
labelled as such.

## C9 — The cGAS–STING arm is refuted in direction; and the IL-axis candidate is wrong. **BOTH CHANGED.**

Hong et al., *Nature* 607:366–373 (2022), doi:10.1038/s41586-022-04847-2 —
*"cGAS-STING drives the IL-6-dependent survival of chromosomally instable cancers."*

**(a) The planned cGAS–STING arm is withdrawn, refuted in direction rather than untested.**
This workstream carried a pending arm treating cGAS–STING as a bridge between CIN and the
inflammatory axis, with the implicit idea that stimulating innate sensing would help clear
aneuploid cells. The paper shows the opposite: *"inactivation of cGAS–STING signalling
selectively impairs the survival of ... cells that display CIN"*, and it
*"demonstrates **pro-tumorigenic traits** of cGAS–STING signalling"* — which is also why
the pathway is rarely inactivated in primary tumours. Stimulating it in a child whose
cells are constitutionally CIN would be pushing the wrong way on a survival pathway.

**(b) Thesis A was aimed at the wrong interleukin.** Our adjunct arm was IL-1 blockade
(anakinra, canakinumab), rated `interesting_under_supported` because two human datasets
disagreed by cell type. The CIN-specific mechanism published here runs
cGAS–STING → non-canonical NF-κB → **IL-6–STAT3**, and the drug it nominates is
**tocilizumab**, an IL-6R blocker already approved in children **aged 2 and over** for
systemic and polyarticular JIA. On every axis that matters this is a stronger version of
the same idea than ours: the mechanism is CIN-conditioned rather than generic
senescence-associated, the selectivity is demonstrated in CIN cells specifically, the drug
has paediatric regulatory precedent, and the repurposing is proposed in the source itself.

**It is not promoted to the lead, for a reason that should be stated rather than buried.**
Blocking IL-6 cuts the tumour-survival arm *and* the immune-clearance arm of the same
system, on different timescales, with no published net effect in this setting — and in a
cancer-predisposed child the clearance arm is not expendable. It also carries the general
infection risk of IL-6R blockade in a child who has had cytotoxic therapy. So it replaces
the IL-1 candidate on the inflammatory axis and inherits its `interesting_under_supported`
verdict, with a named decisive experiment rather than a recommendation.

## C10 — The Track 1 pipeline is coding-only, and a genome-edited-proven cause of this disease is non-coding. **LIMITATION ADDED.**

Two papers, verified against PubMed, bound the generality of our variant-identification
method and open an alternative architecture for this child's second allele.

**Matsuura et al., *Am J Med Genet A* 140:358–67 (2006), doi:10.1002/ajmg.a.31069** —
*"**Monoallelic** BUB1B mutations were found in all seven [Japanese PCS] families studied
... **No mutation was found in the second alleles** in the seven families studied, but
RT-PCR of BUB1B and Western blot analysis of BubR1 indicated a modest decrease of their
transcripts."* Their conclusion also independently corroborates the dose threshold other
sections rely on: *"**>50% decrease** in expression (or activity) of BubR1 is involved in
the PCS syndrome."*

**Ochiai et al., *PNAS* 111:1461–6 (2013), doi:10.1073/pnas.1317008111** — the second
allele was found outside the gene: *"a unique single nucleotide substitution, G > A at
ss802470619, was identified in an **intergenic region 44 kb upstream** of a BUB1B
transcription start site, which cosegregated with the disorder."* Causality was then
demonstrated by **TALEN-mediated single-base editing**: *"The cell clones showed reduced
BUB1B transcripts, increased PCS frequency, and MVA, which are the hallmarks of the
syndrome."* A homozygous patient was also found.

### What this costs us

**1. A stated recall bound on the Track 1 method.** Our pipeline indexes merged CDS
intervals and filters to variants inside them. An intergenic variant 44 kb upstream of the
transcription start site is **invisible to it by construction** — not missed by a tuning
choice, but outside the search space. Applied to those seven families our pipeline would
have found one coding hit per family, failed the biallelic-compatibility test, and
**dropped *BUB1B* at stage 2** — returning a confident wrong answer of exactly the kind
the `genes_at()` bug produced earlier in this workstream. This is the honest answer to the
Scalability criterion: the method generalises to coding compound-heterozygous
architectures and not beyond, in a disease where a non-coding second allele is proven.

**2. An alternative architecture for this child that we never entertained.** We have
assumed p.Leu737Ter + p.Asn1002Lys *in trans* (itself an inference — the two sites are
10,911 bp apart and the callset carries no physical phasing). A third possibility now has
published precedent in this exact gene and disease: **p.Leu737Ter is causal,
p.Asn1002Lys is a passenger, and the second hit is regulatory and undetected.** The
passenger branch is not idle speculation: of six pseudokinase-domain substitutions
resolved in MVA patients by Suijkerbuijk 2010, **Q921H had wild-type abundance *and*
wild-type function** — a passenger in a patient with the disease. Our own
`bub1b-dosage-review/ESTIMATE.md` already cites Q921H, and used it only to bracket a
dosage estimate rather than as evidence that a pseudokinase-domain missense in an MVA
patient can be benign.

This does not overturn our Track 1 answer — *BUB1B* is the gene either way, and the
phenotype match is independent of which second lesion is operative. It does change what
Thesis B rests on, because stabilising allele 2 is category-wrong if allele 2 is a
passenger.

### What it implies

The decisive test is unchanged and cheap, and it is now better motivated: **parental
genotyping** settles phase, and if the variants prove to be in *cis* — or if allele 2
behaves like Q921H — the regulatory region around *BUB1B*, including the 44 kb upstream
interval, is where the second lesion should be sought. Reporting this is worth more than
asserting a clean compound heterozygote we have not phased.

## C11 — The first positive finding: vinorelbine may be genotype-privileged, not contraindicated. **ADDED.**

Every correction above is subtractive. This one is not, and it is the only candidate in
this workstream that points **with** the standard of care rather than against it.

**Klotz et al., *J Cell Sci* 125:887–95 (2012), doi:10.1242/jcs.091843** — title:
*"The microtubule poison vinorelbine kills cells **independently of mitotic arrest** and
targets cells lacking the APC tumour suppressor more effectively."* The abstract states
the premise and the result:

> *"APC-deficient cells have a **compromised spindle assembly checkpoint**, which renders
> them **less sensitive** to killing by microtubule poisons whose toxicity relies on the
> induction of prolonged mitotic arrest. Here, we describe the novel discovery that the
> clinically used microtubule-depolymerizing drug vinorelbine ... kills APC-deficient
> cells in culture and in intestinal tissue **more effectively** than it kills wild-type
> cells. This is due to the ability of vinorelbine to **kill cells in interphase
> independently of mitotic arrest**."*

**Why this matters here.** Vinorelbine is not a new proposal: with low-dose
cyclophosphamide it is the maintenance arm of the EpSSG RMS 2005 regimen, which moved
5-year overall survival from 73.7% to **86.5%** (HR 0.52; Bisogno et al., *Lancet Oncol*
20:1566–75, doi:10.1016/S1470-2045(19)30617-5). So the question is not whether to give it
but whether this genotype argues for or against it.

Our retracted rule (C1) implied against — SAC-routed killing should underperform. Klotz
inverts that specifically for this drug: vinorelbine's killing does **not** route through
arrest, and in a SAC-compromised background it killed *better*. If that transfers, the one
regimen component this child's genotype most obviously threatens is the one it may
actually favour, and the implication is to **retain** an established therapy rather than
to add or avoid anything.

**What this is not.** The SAC compromise in Klotz is a consequence of *APC* loss, not a
*BUB1B* lesion; the interphase death is p53- and BIM-dependent; the cells are colorectal.
No experiment has tested vinorelbine in a BubR1-hypomorphic background. This is therefore
a **mechanistic hypothesis with a named discriminating experiment** — vinorelbine
dose–response in isogenic *BUB1B*-hypomorphic versus wild-type cells, scored
clonogenically rather than at 72 h (C1) — not a claim about what this child should
receive. Nothing here is clinical advice.

**Also noted, unverified.** The same analysis cited Zasadil et al. 2014
(doi:10.1126/scitranslmed.3007965) for the claim that at clinically achieved
concentrations microtubule-targeting agents kill by missegregation rather than arrest.
That claim is consistent with Klotz and with C1, and it would strengthen this entry, but
**it has not been verified against the primary source** and is recorded here as pending
rather than used.

## C12 — KIF18A inhibition degrades BubR1 and phenocopies the disease. **STRENGTHENED, and it generalises.**

The KIF18A refutation (C2, reason 1) stands on SAC-dependence. A third and sharper reason
closes it, and it is mechanistically independent of the first two.

**Liu et al., *Genes Cancer* 1:26–39 (2010), doi:10.1177/1947601909358184** —
*"KIF18A silencing results in **degradation of CENP-E and BubR1**, which is accompanied by
**premature sister chromatid separation**. KIF18A physically interacts with BubR1 and
CENP-E."* The same paper reports *"complete sterility in male but not in female mice"* and
*"germinal cell aplasia"* from `Kif18a` disruption.

So in this child the most clinically advanced aneuploidy-selective class would:

1. **further deplete the protein he is already short of** — BubR1 is degraded on KIF18A
   loss, and his entire functional supply comes from one hypomorphic allele;
2. **reproduce the disease by its own mechanism** — premature sister chromatid separation
   is what MVA1's other name describes; and
3. carry germ-cell toxicity, in a paediatric patient, stacked on the subfertility already
   associated with BubR1 insufficiency.

### The general rule this makes explicit

C5 found that 4-PBA's HDAC activity induces premature chromatid separation and strips
BubR1 from kinetochores. C12 finds that KIF18A inhibition degrades BubR1 and induces
premature chromatid separation. **Two unrelated candidate classes — one our own lead, one
the field's — fail for the same reason: their mechanism reproduces the disease.**

That is a cheap, general screen this workstream did not apply and should have:

> **Before proposing any agent in a chromosome-missegregation syndrome, ask whether its
> mechanism of action is also a published cause of chromosome missegregation, loss of the
> deficient protein, or premature chromatid separation. If it is, the agent is
> contraindicated regardless of how well its headline indication matches.**

Applied retrospectively it would have caught 4-PBA (C5), KIF18A (C12), MPS1/Aurora-B
inhibitors, HSP90 inhibitors (C2 refinement — 17-AAG destabilises the hypomorph), and
griseofulvin, each before any effort was spent on it. It costs one literature query per
candidate and it is the most portable thing in this file.

## C13 — Three verification outcomes, one of them an error in how I built the evidence base

An independent pre-mortem review of the four open disagreements re-checked the citations
behind them. Three results, recorded because two of them are mine.

### (a) Zasadil 2014 is verified, and stronger than C11 allowed

C11 recorded it as *pending*. It verifies: **Zasadil et al., *Sci Transl Med* 6:229ra43
(2014), doi:10.1126/scitranslmed.3007965** —

> *"paclitaxel levels in primary breast tumors are **well below those required to elicit
> sustained mitotic arrest**. Instead, cells in these lower concentrations of drug proceed
> through mitosis without substantial delay and divide their chromosomes on **multipolar
> spindles**, resulting in chromosome missegregation and cell death ... we find that
> **mitotic arrest is dispensable for tumor regression in patients**."*

This is human in vivo data, and it undercuts the premise our original rule rested on more
directly than any cell-line result: if arrest is dispensable for efficacy at concentrations
actually achieved in tumours, then a patient who cannot sustain arrest has not thereby lost
the mechanism by which the drug works.

**With its correct narrowing.** It is paclitaxel, in breast cancer, and the death route is
missegregation on **multipolar spindles** — a spindle-pole phenomenon, not a checkpoint
one. It is evidence about which mechanism kills, not evidence about BubR1.

### (b) The "resistance" sources are real; my brief omitted their identifiers

The reviewing analysis could not locate three claims on the resistance side and labelled
them *untested*. They are not untested — **I summarised them in the brief without
identifiers**, so they were unfindable by construction. That is a defect in how I built the
brief, and left uncorrected it would have propagated a false "no such evidence" finding.

The principal source verifies: **Silva et al., *J Biomed Sci* 31:74 (2024),
doi:10.1186/s12929-024-01056-z** — *"BUB1B variants lead to **decreased BubR1 expression
and/or stability**, which promotes increased **premature chromatid separation** and,
consequently, triggers CIN, **driving resistance to Taxol-based therapies**."*

Note what it attributes resistance to: CIN arising from premature chromatid separation —
**not** failure to arrest. So Silva and Zasadil are compatible, and the compatibility is
the finding: reduced BubR1 can confer taxane resistance by a route that has nothing to do
with the arrest mechanism Zasadil shows is dispensable anyway.

### (c) The honest verdict on disagreement 2 is a non-resolution, and it should ship as one

Putting (a) and (b) together: the arrest-dependence premise is undermined in humans; the
resistance direction is real but mechanistically attributed to CIN-driven adaptation; and
**no source measures the direction of effect in a constitutionally BubR1-deficient human
host.** The sign is a position on a non-monotone missegregation curve, modulated by which
death route the drug actually uses and by p53 status.

So the correct output is not a verdict. A signed sentence here would be the most quotable
and least supported thing this workstream could emit, in a disease where
reduced-intensity practice is already in the literature and where error is irreversible in
**both** directions. C1 retracted the claim in one direction; C13 declines to assert it in
the other.

### A standing rule this produces

**Every claim in any internal brief carries its DOI or PMID at the point of use.** A
summarised claim without an identifier cannot be checked, and an unverifiable claim
reviewed in good faith comes back as absent evidence — which is worse than a wrong
citation, because it manufactures a negative finding.

## C14 — Three errors in my own evidence handling, found by independent review

Fifteen independent analyses were asked to adjudicate four open disagreements and to report
anything wrong in the brief they were given. Three errors were found by **three agents
independently each**, which is why they are recorded rather than quietly fixed. Two are
mine; all three were confirmed against the primary text before being written down.

### (a) I inverted Baker 2013 *Cell Rep*, and withdrew a research arm on the strength of it

The paper (doi:10.1016/j.celrep.2013.03.028) says:

> *"p53 delays functional decline of skeletal muscle and fat in a p21-dependent fashion
> **by inhibiting p16^Ink4a^-mediated senescence of progenitor cells**."*

I read the companion sentence — *"skeletal muscle, fat, and lens tissue engage p19^Arf^ to
**attenuate** senescence"* — and concluded that senescence was protective in those tissues.
It says the reverse: senescence is the damage, and the p19^Arf^/p53/p21 axis **opposes** it.
So suppressing or clearing senescent progenitors acts in the **same direction** as the
protective axis in muscle and fat, and C8's inference was backwards.

The paper's own title states the structure I missed: *"p21 both attenuates **and drives**
senescence and aging in BubR1 progeroid mice."* The genuine divergence is **lens-specific**
— there *"p21 [promotes] senescence of lens epithelial cells and cataract formation"* — so
this is a tissue-specific sign flip, not a contradiction.

**Consequence.** The senolytic arm is reinstated as *untested*, not contraindicated, with
its real open questions named: no clearance experiment exists in a germline
cancer-predisposed developing host; every cited experiment used **genetic ablation, not a
senolytic drug**; and whether SAC-arrested satellite cells are p16-high is unmeasured. This
is a reinstatement to the honest category, not a promotion.

### (b) Y155C is in the TPR domain, not the pseudokinase domain

I offered Y155C as a separation-of-function precedent while discussing a
**pseudokinase-domain** missense variant. Y155C is N-terminal, in the TPR domain
(Suijkerbuijk 2010 is explicit). It remains a valid example that an MVA allele can have
normal abundance — which is all C6 needed it for, and C6 stands — but it is **not** a
same-domain precedent for a pseudokinase-domain interface lesion, and I used it as one.

### (c) A DOI in my brief does not support the claim it was attached to

I cited `doi:10.1038/s41467-020-19876-6` for the pseudokinase domain's role in PP2A-B56
recruitment. Three reviewers independently resolved it to an unrelated paper on cohesin and
nuclear architecture. The underlying claim survives on Gama Braga et al. 2020
(doi:10.1016/j.celrep.2020.108397), verified verbatim by two reviewers; the DOI was simply
wrong. Every instance in this workstream is to be replaced with the Gama Braga citation.

### What these three have in common

None of them is a hard biology question. One is a reversed arrow, one is a domain
boundary, one is a mistyped identifier — and each took one careful reading of a source I
already had open. The pattern across C13 and C14 is that **my errors are concentrated in
sources I summarised rather than quoted.** The standing rule from C13 (every claim carries
its identifier at the point of use) is extended: **where a source's direction of effect is
load-bearing, quote the sentence rather than paraphrase it.**

## C15 — Two more: an asymmetry I introduced, and the first evidence that *favours* us

### (a) Disagreement 2 is a genuine head-to-head conflict, and my brief hid that

C1 retracted a one-directional rule. Reviewing the evidence I assembled afterwards, I then
over-corrected: I presented the "reduced BubR1 sharpens killing" side as if it had won,
giving it three citations and the other side none. Two problems.

**Lee 2004 and Dowling 2005 are the same laboratory** (Kao, Penn). Three citations were
two independent sources.

**And the opposing head-to-head study was omitted entirely.** Sudo et al.,
*Cancer Res* 64:2502–8 (2004), doi:10.1158/0008-5472.can-03-2013 —

> *"Suppression of Mad2 and **BubR1** in paclitaxel-treated cancer cells abolished
> checkpoint function, resulting in **paclitaxel resistance** that correlated with
> suppression of cyclin-dependent kinase-1 activity ... Thus, checkpoint function **is
> required** for paclitaxel sensitivity."*

Same year, same protein, same drug as Lee 2004, directly opposite conclusion. Note also
that Sudo's stated implication is precisely the claim this workstream originally made and
C1 retracted — so C1 was right to retract the *certainty* and wrong to let the opposite
direction stand unopposed in its place.

**Verdict, final form:** the direction of effect is **genuinely contested in the primary
literature at the level of direct BubR1-suppression-plus-taxane experiments.** Zasadil
(C13) shows the arrest-dependence premise is anyway undermined in patients, and
window-dependence (Cohen-Sharir) plus death-route differences explain how both results can
stand. It publishes as a non-resolution, as C13 concluded — but now with both sides cited
at equal strength rather than with my thumb on the scale.

### (b) The passenger architecture in C10 is less likely than I made it, on published phenotype data

C10 raised the possibility that p.Leu737Ter is causal, p.Asn1002Lys a passenger, and the
second hit regulatory and undetected — on the precedent of Matsuura/Ochiai. Two findings
weaken that branch, and this is the first point in today's review where the evidence moves
in our favour.

**The Q921H precedent does not say what I used it for.** Q921H was *in cis* with L844F on
the same allele, and the authors conclude L844F is causal with Q921H the spare. It is
therefore not an estimate of "a lone pseudokinase-domain missense is benign" — it is the
wrong reference class, and it inflated the passenger branch.

**And MVA stratifies by architecture in a way that fits this child.** García-Castillo
et al., *Am J Med Genet A* 146A:1687–95 (2008), doi:10.1002/ajmg.a.32315, reviewed 21 of 35
screened patients and found three distinct pictures:

| architecture | severity | hallmarks |
|---|---|---|
| **monoallelic** *BUB1B* (one coding hit + presumed cryptic second) | **severe** | Dandy-Walker 7/8, cataracts 6/6, **Wilms tumour 7/8** |
| **no** *BUB1B* mutation | **mild** | *"no evidence of cancer"*, no Dandy-Walker, no cataract |
| **biallelic** *BUB1B* | **moderate** | — |

This child has a malignancy, which excludes the no-mutation group. And the malignancy is
**rhabdomyosarcoma, not Wilms**, with no Dandy-Walker complex and no cataract in the
record — so the monoallelic-plus-cryptic picture, whose hallmarks are Wilms, Dandy-Walker
and cataract at 6–7 out of 8, fits poorly. A moderate presentation with a non-Wilms
embryonal tumour is the **biallelic** picture.

**So the passenger/regulatory branch is now the least supported of the three**, on
published phenotype-architecture data rather than on assumption — and, usefully, without
needing any new measurement. The abundance/stability reading of p.Asn1002Lys remains
favoured, parental genotyping remains the decisive test, and C10's recall bound on the
coding-only pipeline **stands unchanged**, because that is a statement about the method's
generality rather than about this child.

## C16 — "Not in ClinVar" is true of the nucleotide and false of the protein change

Two documents stated that p.Asn1002Lys is **not in ClinVar**. Verified against ClinVar
directly, that is correct only at the nucleotide level and misleading at the level that
matters for interpretation.

**ClinVar VCV004600147.1** — `BUB1B c.3006T>A`, **p.Asn1002Lys**, classified **Uncertain
significance**, last evaluated **19 Sep 2025**, submitted by Ambry Genetics, with the
submitter note that *"the clinical significance of this variant remains unclear"* on
inconclusive in-silico prediction at a conserved position.

Our proband's allele is `c.3006T>**G**`. Same codon, same amino-acid substitution, a
different third base. So:

- the **nucleotide** variant `c.3006T>G` is genuinely absent from ClinVar;
- the **protein** variant p.Asn1002Lys is **present and classified, as a VUS**.

**Why the distinction is load-bearing.** Any argument that leans on this change being
uncharacterised — novelty, absence of prior assessment, the need to classify it ourselves —
has to contend with an existing independent VUS call on the identical substitution, made by
a clinical laboratory, which reached *uncertain* rather than pathogenic. That is not a
contradiction of our analysis; the AlphaMissense score of 0.9229 stands as a prediction and
Ambry's note explicitly records in-silico evidence as inconclusive. But it means the honest
framing is *"an independent clinical laboratory classified this protein change as a VUS and
we agree the evidence is unresolved"*, not *"this change has never been assessed."* The
second framing would have overstated our contribution and understated the difficulty.

Both documents are corrected in place to carry the accession at the point of use, per the
C13 rule.

**Reported but not yet verified by me:** the same review states the exact allele appears in
gnomAD at allele count 1 of 1,461,878, and that *BUB1B* shows no missense depletion
(observed/expected 0.91, z 1.30), with the pseudokinase domain no more constrained than the
gene average. If those hold they further weaken any "rare missense in an important domain is
probably damaging" inference — which is a premise both sides of disagreement 1 lean on. I
have not checked them against the primary source and they are recorded here as pending
rather than relied upon.

## C17 — The non-coding second allele in *BUB1B* is a pattern, not an anecdote: four independent instances

C10 recorded that our coding-only pipeline could not have seen the TALEN-proven upstream
variant in Ochiai 2013, and stated that as a limitation. The limitation is larger and more
interesting than that, and it is the most useful thing to come out of this review. **Four
independent reports, spanning seventeen years, found the second *BUB1B* allele outside the
coding sequence** — each verified against PubMed:

| source | what coding analysis found | where the second allele actually was |
|---|---|---|
| Matsuura 2006, doi:10.1002/ajmg.a.31069 | **monoallelic** *BUB1B* in **all seven** Japanese PCS families | *"No mutation was found in the second alleles"*; a conserved haplotype and reduced transcript pointed elsewhere |
| Ochiai 2013, doi:10.1073/pnas.1317008111 | nothing further | **intergenic SNV 44 kb upstream** of the transcription start site, proven causal by TALEN single-base editing |
| Kato 2017, doi:10.1038/hgv.2017.21 | *"mutational analysis of the **entire coding region** ... failed to identify any causative mutations"* | an **upstream** mutation plus a novel **intronic insertion** |
| Kawakami 2023, doi:10.1038/s10038-023-01211-8 | exome found one intronic splice variant; *"**GS could not detect** another pathogenic variant"* | a paternal **3.0 kb insertion of Alu and SVA elements** in intron 2, found only via **RNA-seq** then **long-read adaptive sampling**; protein *"severely diminished"* |

### What follows, and why it is a contribution rather than a caveat

**1. The architecture is the norm often enough to design for.** In this gene, "two coding
hits" is one of several common architectures, and a coding-only search returning a single
heterozygous variant is **not** evidence against *BUB1B*. Our stage-2 biallelic-compatibility
filter would have discarded the gene in every one of the four cases above. That is a
systematic recall failure, not a tuning choice, and it is now quantified by four examples
rather than asserted.

**2. Short-read genome sequencing is not sufficient either.** The 2023 case is the sharp
one: genome sequencing missed a 3.0 kb mobile-element insertion that RNA-seq flagged
functionally and long reads resolved structurally. So the next-line test after a negative
coding search in this gene is **not deeper coding analysis** — it is transcript-level
evidence followed by long reads.

**3. It gives the method a defensible generalisation.** Stated honestly: our pipeline
recovers coding compound-heterozygous architectures and will under-ascertain *BUB1B*
specifically, in a known and now-enumerated way, with a named remedy. That is a stronger
Scalability answer than a clean claim would have been, and it is portable to the other MVA
genes.

**4. It sharpens, rather than supports, the passenger hypothesis.** This pattern is what
made C10's "allele 2 is a passenger and the real second hit is regulatory" branch
plausible. It remains the correct branch to name — but C15(b) showed the phenotype
stratification (García-Castillo) fits a **biallelic** architecture for this child, and the
Q921H base rate that inflated the branch was a *cis* passenger to a causal allele and never
a *trans* candidate. So: the architecture is well precedented in the gene, and the
phenotype evidence in this particular child points away from it. Both halves ship.

### The question this exposes in our own framing

An independent review observed that all four disagreements I drafted are posed about
*"reduced BubR1"* without ever specifying **reduced to what level** — while two
threshold-shaped dose–response series exist (~13% residual near-silent vs ~6%
catastrophic; and aneuploidy appearing below ~50%). Every one of the four answers changes
sign or magnitude across that axis. A disagreement about a quantity, posed without the
quantity, cannot resolve. That is a better description of why these four stayed open than
any of the evidence problems recorded above.

## C18 — A candidate contribution that outranks all four disagreements. **PROPOSAL, premises not yet sourced.**

This entry is forward-looking rather than corrective, and it is recorded with its
verification status open, per the C13/C14 rules.

**The question.** Guideline-level advice in this disorder group is to minimise ionising
radiation (Nakano et al. 2024, doi:10.1158/1078-0432.CCR-24-1098, verified: these disorders
show *"exquisite sensitivity to anticancer treatments such as ionizing radiation and
chemotherapy"*). A survivor therefore needs **radiation-sparing** surveillance. One
prominent radiation-free modality detects tumours by detecting **chromosomal imbalance in
cell-free DNA**.

This child's **non-malignant tissue is constitutionally chromosomally imbalanced** — that is
the diagnosis, not a tumour property. So the question is whether an aneuploidy-based cfDNA
readout has any usable signal-to-background in mosaic variegated aneuploidy, or whether the
constitutional mosaic fraction sits above the assay's detection floor and swamps it.

**Why it is the best candidate deliverable found today.**

- It serves a real and currently unserved decision — radiation-sparing surveillance in a
  survivor of the predicted tumour — rather than proposing a drug.
- It is **genotype-specific in a non-obvious direction**: the confounder is not a side
  effect, it is the disease mechanism colliding with the assay principle.
- It is answerable **from public data in a container**, with no patient data, no wet lab and
  no new consent.
- It carries **no advice surface**. It is a statement about an assay's detection limits, so
  it cannot be read as guidance about what to give a child — which, after today, is a
  property worth weighting explicitly.
- If the answer is "below the floor", that is a usable negative for every MVA family and
  for the other MVA genes; if "above the floor", it is a caution about a modality that
  would otherwise look obviously right.

**What is not yet established, and must be before any of this ships.**

1. That aneuploidy-based cfDNA detection is in fact a leading radiation-free surveillance
   modality for the relevant tumour types — I searched and did **not** retrieve a clean
   primary source, so this premise is currently **unsourced**.
2. The quantitative mosaic aneuploid fraction in this disorder, in blood specifically.
   A figure of roughly half of cultured lymphocytes is cited in the literature reviewed
   today (García-Castillo 2008, doi:10.1002/ajmg.a.32315, which reports *"around one half
   of the cultured lymphocytes ... had aneuploidies"*) — but cultured lymphocytes are not
   plasma cell-free DNA, and treating them as equivalent would be exactly the
   system-transfer error catalogued in C14.
3. Any published detection-floor figures for the assay class.

**Status: a well-posed question with two unsourced premises.** Day-one work is to source
premises 1 and 3 or abandon it. Recorded here so that it is not mistaken for a finding, and
so the decision to pursue it rests on whether those premises hold rather than on how good
the idea sounds.

## C19 — The evidence balance in disagreement 2 is the reverse of how I presented it; and two disagreements rest on one research programme

### (a) I had the citation asymmetry backwards

I wrote disagreement 2 with three citations on the "reduced BubR1 sharpens killing" side and
**none** on the "blunts" side, and flagged only the former's weakest member. Having had
fifteen independent reviews locate the missing sources, the balance is the opposite of what
I presented. All three now verified:

| "blunts" — reduced BubR1 → resistance | verified |
|---|---|
| **Sudo 2004**, doi:10.1158/0008-5472.can-03-2013 | *"Suppression of Mad2 and BubR1 ... resulting in paclitaxel resistance ... checkpoint function is required for paclitaxel sensitivity"* |
| **Fu 2007**, doi:10.1016/j.ygyno.2006.10.061 | a 27-fold paclitaxel-resistant ovarian line: *"weakened spindle checkpoint with reduced expression of **BubR1, but not Mad2**, is associated with acquired paclitaxel resistance"* — with *"increased rate of premature sister chromatid segregation"* in the same cells |
| **Silva 2024**, doi:10.1186/s12929-024-01056-z | *"decreased BubR1 expression and/or stability ... driving resistance to Taxol-based therapies"* |

Three independent groups, three tumour lineages, spanning twenty years.

Against that, the "sharpens" side is **two programmes, not three**: Lee 2004 and Dowling
2005 are the same laboratory (C15a), and Janssen 2009's untransformed-cell control — the
part I leaned on hardest — was run on **Mps1, not BubR1** (C13, C2 second amendment).

Note also that Fu 2007 is the closest thing in this literature to this child's cell biology:
low BubR1 **and** premature sister chromatid separation, which is the syndrome's defining
cytogenetic feature — and in those cells the drug worked *less* well. That does not settle
the question, because these are acquired-resistance tumour lines rather than constitutional
germline insufficiency, but it is the most phenotypically matched datum and it sits on the
side I had left uncited.

**The non-resolution verdict of C13 therefore stands, with the scales corrected.** What
changes is that nobody should read this file as leaning toward "sharpens".

### (b) Disagreements 3 and 4 are substantially one research programme

I presented D3 and D4 as weighing independent bodies of evidence. They do not. Of the
citations I verified directly today, **Baker 2013 *Nat Cell Biol*** (doi:10.1038/ncb2643)
and **Baker 2013 *Cell Rep*** (doi:10.1016/j.celrep.2013.03.028) share a senior author,
Jan M. van Deursen, and both derive from the same BubR1-hypomorphic mouse programme; a
reviewing analysis reports that five of the D3/D4 citations share that provenance, which is
consistent with the two author lists I checked.

That is not a criticism of the work — it is the founding programme for this biology, and
there may be no independent replication to cite. But it means **"two bodies of evidence
disagree" was the wrong description**: one programme, one mouse model, several papers, with
the apparent disagreement arising from marker choice (p16 / p19^Arf^ / p21) and tissue
within that programme. Which is precisely why D4 dissolved on a careful read (C14a) rather
than resolving on evidence weight.

### (c) A fifth disagreement I failed to pose, and it is more tractable than the four

Independently nominated by a reviewer, and it is the crux our own `NMD-FEASIBILITY.md`
already identifies: **allele 1 is a null at the RNA level because of transcript decay — but
would it make a functional protein if decay were bypassed?** A construct truncated just
before the pseudokinase domain was fully functional in rescue, while a truncation sixteen
codons later was not, and the literature does not explain the split.

That question is better posed than any of my four: it concerns a single, measurable,
binary property of one allele; it has a published disagreement with a named crux rather
than an inferred one; and it bears on whether allele 1 is a therapeutic target at all. It
should have been Disagreement 0 alongside phase.

## C20 — Final round: one support, one softening of my own correction, one new hazard

All fifteen independent adjudications are in. Three last items, each verified.

### (a) Absent microcephaly does not threaten the diagnosis

**Callier et al., *Am J Med Genet A* 137:204–7 (2005), doi:10.1002/ajmg.a.30783** — title:
*"Microcephaly is **not mandatory** for the diagnosis of mosaic variegated aneuploidy
syndrome"*, reporting *"the first case of MVA syndrome without microcephaly."*

This matters because this workstream once asserted microcephaly as part of this child's
phenotype, withdrew it, and then treated its absence as an open puzzle. It is neither: the
feature is not required for the diagnosis, and there is a published precedent for its
absence. (That case did have developmental delay, which this child also lacks, so the
precedent is partial.)

### (b) C15(b) was over-read, and I am softening it

C15(b) concluded that this child's presentation *"fits the biallelic picture"* in
García-Castillo's stratification. A more careful reading of the same paper does not support
that. Its three groups are distinguished by *BUB1B* genotype, and the reported sibs who
**lacked microcephaly** were the ones with **no *BUB1B* mutation and no cancer**. The
biallelic group is characterised only as *"moderate"*; the paper does not report whether
those cases had microcephaly.

So the honest statement is weaker and more interesting: **this child matches no published
MVA subtype cleanly** — cancer plus *BUB1B* variants places him outside the no-mutation
group, while the absence of microcephaly and developmental delay is the profile that paper
associates with that group. Combined with the ascertainment problem (the literature is
defined on features he lacks), the right conclusion is that the published subtype framework
does not accommodate him, not that he fits one of its cells.

C15(b)'s narrower claim stands: the monoallelic-plus-cryptic picture, whose hallmarks are
Wilms, Dandy-Walker and cataract at 6–7 of 8, fits poorly. What I withdraw is the positive
assignment to the biallelic group.

### (c) A second-order hazard for raising BubR1 that was absent from the file

**Komura et al., *Oncogene* 40:6210–22 (2021), doi:10.1038/s41388-021-02021-y** — title:
*"**Increased** BUB1B/BUBR1 expression contributes to aberrant DNA repair activity leading
to **resistance to DNA-damaging agents**."* Mechanism: cells with aberrant BubR1
*"dominantly exploit **mutagenic** nonhomologous end joining"*, ATM-dependent, with
**FOXM1** identified as the transcription factor driving the increase — the same axis Wan
2012 reports in rhabdomyosarcoma.

Three reasons this is the most relevant hazard datum yet for the raising-BubR1 question,
and one reason it is not decisive:

1. It concerns **high** BubR1 rather than low, so unlike Wan 2012 it is at least pointed in
   the direction a therapeutic lever would move.
2. The repair route it promotes is **mutagenic** — a concerning property in a constitutional
   chromosome-instability syndrome, independent of any tumour.
3. It predicts resistance to **DNA-damaging agents**, which is the class C3 originally
   marked *"unaffected by this logic"*. The exemption keeps failing.

**But the same logical caveat as C4 applies, and must be stated.** This is aberrant
overexpression in chemoradiation-recurrent bladder cancer cells, not restoration of a
deficient level in a patient. Essentiality and overexpression phenotypes constrain the ends
of a dose–response; neither tells you what happens when a hypomorph is brought toward
normal. Four independent reviews made this exact point about Wan 2012 and I am not going to
repeat the error one entry later: **raising BubR1 toward normal in this host remains
untested, not unsafe** — now with two named mechanisms worth testing rather than one.


## C21 — The allele-1 NMD call now rests on a calibrated model, not a hand-applied rule

Added 13 Oct 2026. See `NMD-PREDICTION-TRUNKITTEN.md` for the full run.

Every argument in this workstream about allele 1 (**p.Leu737Ter**) assumed its transcript
is degraded, and that assumption came from applying the **50–55 nt rule** by hand. C19(c)
identified the allele-1 question as the better-posed crux of the project, and an
independent review nominated it as the disagreement that should have been posed first.

We have now scored it with **TrunKitten**, the 8-feature reduced form of TrunCat
(doi:10.64898/2026.06.26.734884), trained on NMD measured directly in 10,306 TOPMed
genome/transcriptome pairs across 5,749 germline truncating variants:

> **escape probability 0.3163**, model threshold 0.4314 → **predicted to undergo NMD.**

**The rule gave the right answer, and the model says so with a magnitude.** 0.32 is
roughly a one-in-three predicted chance of escape, from a model whose own discrimination is
ROC-AUC ≈ 0.78 — so the defensible claim is now *"predicted to undergo NMD, with
meaningful residual probability of escape"*, not *"NMD-competent by the 50–55 nt rule"*.
The preprint's own headline is that the 50–55 nt rule explains only about half of the
observed variability, which is a direct caution against the way we had been using it.

**Validated before being believed.** No *BUB1B* variant appears in the authors' shipped
ClinVar, gnomAD or GREGoR prediction files, so no direct cross-check on this gene was
possible. Instead, 12 chr15 variants from their own ClinVar set were run through our
installation from scratch: **12/12 class agreement and Pearson r = 0.966** against their
published TrunCat values, across 0.118–0.810. Their test suite also passes 40/40, and all
annotation QC flags are clean.

**It also independently reproduced three of our own annotations** from GENCODE v26 rather
than our parsing: 23 exons with the PTC in exon 17 (we said "exon 17/23"), CDS length
3,153 nt = 1,050 residues plus stop (matching UniProt O60566), and the canonical transcript
ENST00000287598.

**What it does not do** is answer the second half of the crux — whether the 736-residue
product would be *functional* if decay were bypassed. That is the 731X-versus-753X split
`NMD-FEASIBILITY.md` calls "the real gap", and no NMD predictor addresses it.

**Two findings worth reporting upstream**, both recorded in the run document: a
reproducible crash in `minicat/halflife.py:61` under pandas 3.x (one null gene symbol in
13,921 aborts the pipeline, because the new `str` dtype does not render nulls as `"nan"`);
and the repository carries **no licence file**, so by default all rights are reserved. We
therefore use and cite the tool but do **not** vendor it — which matters because our
submission repository must be public under CC BY 4.0 and may be rerun by the organisers.

## C22 — Why only allele 1 was scored for NMD, and a splice prediction we never actually ran

Added 13 Oct 2026, prompted by the direct question "did you check both alleles?".

**Only allele 1 was scored, and that is correct by construction.** TrunCat/TrunKitten
predict nonsense-mediated decay for **protein-truncating** variants. Verified from hg38
plus GENCODE v26 directly, rather than from our own prior annotation:

| allele | codon | change | consequence |
|---|---|---|---|
| 1 — p.Leu737Ter | 737 | `TTA` → `TGA` | Leu → **stop**; the stop codon is **UGA** |
| 2 — p.Asn1002Lys | 1002 | `AAT` → `AAG` | Asn → Lys, **no stop created** |

Both variants land at exactly the expected codon number, which independently confirms our
coordinates, our transcript choice (ENST00000287598) and the reading frame. The computed
CDS is 3,150 nt = 1,050 codons, consistent with the pipeline's reported `cds_length` of
3,153 once the stop codon is counted, and with BubR1's length in UniProt O60566.

Allele 2 creates no premature termination codon, so there is nothing for an NMD model to
score. This also independently confirms the UGA identity of allele 1's stop, which several
reviewers computed separately — it is now checked against the reference sequence here.

**Allele 2 is additionally in the last exon, which settles the question twice over.**
From GENCODE v26: allele 2 falls in **exon 23 of 23**, 48 nt from the exon's 5′ boundary
and 524 nt from its 3′ end. A premature stop in a final exon escapes NMD by construction,
because there is no downstream exon-junction complex to trigger it. So even in the
counterfactual where this variant did create a stop, NMD would not be the consequence.
(Allele 1, by contrast, is in exon 17 of 23 — well upstream, which is why the question is
live for that allele and not this one.)

**The gap this exposed.** The only route by which a missense variant could reach NMD is by
creating a cryptic splice site and a downstream frameshift PTC. Our committed
`data/variants/pangolin_splice_scores.csv` contains **only the four known splice
variants** — `c.1288+5G>A`, `c.1402-5A>G`, `c.2386-11A>G` and `c.2009+1G>A`. **It does not
contain allele 2.** We never ran a splice prediction on p.Asn1002Lys.

A splice score for this variant was quoted to this workstream during review. It is not
ours, it is not in our files, and it is not recorded here as evidence. The honest status
is: **unscored**. Given that the variant sits 48 nt inside the final exon, a splice effect
is not the leading hypothesis, and any such effect could not produce NMD for the reason
above — but "not the leading hypothesis" is not the same as "excluded", and the file should
not imply otherwise. Scoring it is cheap and is now a named open item.

> **CLOSED 14 Oct 2026. Scored, and negative.** Pangolin gives allele 2 gain **+0.01**,
> loss **0.00** — stable at window widths of 50, 300 and 1000 nt and identical across all
> three overlapping gene models — against a positive control (`c.2386-11A>G`) that
> reproduces its committed score exactly at +0.76 / −0.71. `SPLICE-ALLELE2.md`,
> `scripts/mva/variants/splice_allele2.py`, raw output archived in
> `data/variants/pangolin_allele2.json`. The splice route to NMD for allele 2 is now
> excluded by measurement rather than by prior, which means **allele 2 is made as
> protein** and the open question narrows from three possibilities to two: abundance or
> function. Two defects in the instrument were found in the process — see C25.

## C23 — Our own verifier could not run from a clean checkout. Fixed.

Found 13 Oct 2026 by accident, in a fresh container, while committing other work.

`verify_report.py` is the instrument that proves the report's numbers match the committed
data. In a fresh container it died:

```
FileNotFoundError: apps/api/data/mva/gate1.json
```

**The cause is not a bug but a documentation gap.** `.gitignore:41` deliberately excludes
`gate1.json`, with a committed rationale: it is `universe.json` plus one derived field and
rebuilds in under a second. That reasoning is sound and I verified it — regeneration from
committed data takes **0.38 s, fully offline** — and the other four gate files are
committed. But nothing told a reader, or a fresh clone, that the step existed. The verifier
simply crashed.

**Why this mattered more than it looks.** The organisers state that submissions may be
rerun. An independent pre-mortem analysis of this workstream ranked *"headline numbers
don't reproduce on the organisers' rerun"* as its **number-one submission-failure
pathway**, at around 55% likelihood, and prescribed exactly this gate: a reproduce step
from a wiped container. That prediction was correct, and the failure was sitting in our
repository while we were busy adjudicating biology.

**The fix.** `verify_report.py` now regenerates `gate1.json` itself when it is absent,
printing what it is doing, and falls back to naming the exact command if that fails.
Verified by deleting the file and re-running: it rebuilds and all checks pass. A fresh
clone now needs one command rather than undocumented knowledge of the build order.

**The general lesson, which this workstream has now learned twice.** C13 established that
an unverifiable claim comes back as absent evidence. This is the same failure one layer
down: a *derived* file that is cheap to rebuild is still a hard dependency if nothing
rebuilds it. Gitignoring a derived artefact is correct; leaving the consumer to crash on it
is not. Any instrument that reads a gitignored file should either rebuild it or say how.

## C24 — Three defects in the thing we were about to publish, found by testing the export rather than reading it

Found 14 Oct 2026, while doing submission mechanics. None of the three is a scientific
error; all three are in the artifact a judge would actually open, and the third is a
privacy defect. The pattern is the one C13 and C23 already named — *an instrument nobody
runs is not an instrument* — applied this time to the export itself.

**C24a — eight of the ten commands in the public README pointed at files the export does
not contain.** The exporter's layout was corrected earlier so that the exported tree
mirrors the repository, because every script resolves its inputs with `parents[N]`
arithmetic and a flattened tree broke all of them. That fix was right and it is still in
place. But the generated README was not updated with it: it continued to tell a reviewer
to run `python3 scripts/gate1_approved.py`, and the file is at
`apps/api/scripts/mva/gate1_approved.py`. Of ten paths named in that README, **two
existed and eight did not** — the five gate scripts, the verifier, `data/universe.json`
and `docs/GATE4-ADVERSARIAL.md`. The organisers state that submissions may be rerun.
A reviewer following our own instructions would have had six consecutive commands fail
with `No such file or directory` before reaching any of our evidence.

Verified by enumerating every path the README names against the exported tree, which is
a check that takes one loop and had never been written. The README is now generated with
paths that exist, both invocation styles are confirmed to work from the export root, and
it states plainly which two gates are *not* re-runnable and why (gate 0 reads a molecule
list that is not redistributed; gate 4 is a literature pass, not a script).

**C24b — the Track 1 pipeline's entry point was not in the export.** The exporter copies
`**/*.py`. `run_pipeline.sh` is the only non-Python file under the script tree, and it is
the documented way to reproduce the Track 1 cascade — `TRACK1-REDISCOVERY.md` cites it by
name. So the public repository contained five stage scripts and no runner, while the
document explaining them pointed at a file that was not there. Fixed by adding `**/*.sh`.

This is the *same defect as the original non-recursive glob*, which shipped 20 of 47
scripts because `*.py` does not descend into subdirectories. That one was found and fixed;
the lesson — a copy pattern silently omits whatever it does not match — was not
generalised to the file *extension*. One wildcard was audited and the other was not.

**C24c — the Track 1 submission CSV still carried this child's read depths and allele
balances. This is the privacy defect, and it was live.** The per-sample values -- the two read depths and
the two allele balances, not restated here -- were removed from the four documents that
quoted them in an earlier pass. `track1_submission.py` was edited in that pass. **Its
output was never regenerated**, so `docs/mva/data/track1_submission.csv` still held the
original sentence — and that CSV is copied into the public export. The committed file and
the script that writes it had silently disagreed for days.

A derived file is not fixed by fixing its producer. The earlier pass checked the documents
by grep and the producer by eye, and never re-ran the producer or re-grepped its output.
The export scan that finally caught it is a grep over the *exported tree*, not the source
tree, which is the only place the question "what are we about to publish" can be answered.

Also narrowed in the same pass: a numeric `GQ` value remained in four published files while
`SUBMISSION-CHECKLIST.md` asserted that per-sample GQ was "deliberately NOT published —
see `PUBLICATION-AUDIT.md`". Two problems at once. The claim was false as written, and
the audit it cited **does not record that decision anywhere** — a dangling cross-reference
of the same kind as the `track1_verification.md` one already logged. That value is a
capped ceiling and close to uninformative, so the risk here is small; the inconsistency
is not. All five sites now read "at maximum genotype quality", which tells a reviewer exactly
what they need — confident germline hets, not mosaic calls — with no numeral measured from
this child's reads, and `PUBLICATION-AUDIT.md` now records the decision so the reference
resolves.

**What to take from this.** We spent this session adjudicating 23 corrections of biology
and nearly shipped a public repository whose instructions did not work and whose data
file leaked what our own checklist promised it did not. Every one of the three was found
by *running* something against the export, and none would have been found by reading it.
The export now has a test: enumerate the README's paths, diff the producer against its
committed output, and grep the exported tree rather than the source tree.

**Postscript, same day.** `audit_export.py` was written to make the three checks above
permanent. On its first run against a rebuilt export it failed one check — on *this
document*. The paragraph of C24c describing the leaked depths and allele balances had
quoted them verbatim, so the correction reporting the leak reproduced it, in a file that
exports to the public repository. Rewritten to describe the values without restating
them. An instrument that catches its own author's mistake in its first five seconds is
the cheapest evidence that it was worth writing.

## C25 — Closing two open items found two more defects, in a tool and in our own account of why it had failed before

14 Oct 2026. Both items were deliberately small — the brief was to close named gaps,
not open research fronts — and both turned up something.

### C25a — Our recorded explanation for an earlier Pangolin failure was wrong

`SPLICE-AXIS.md` records that three Pangolin jobs failed and attributes it to the two
*coding* variants added as negative controls: *"Pangolin is built for variants near splice
sites, and a control far from any site is not a null result, it is an error."* The
prescription that followed — diagnose by bisection — was right and is why this was found.
The cause was wrong.

Scoring allele 2 paired with a positive control failed again, in 33 s. Bisected: **each
variant alone completed in 29 s.** Allele 2 is 48 nt from a splice acceptor, which is not
"far from any site", so distance cannot be the explanation. The actual trigger is a
variant whose position carries a **multi-gene annotation**: Pangolin emits one
comma-bearing block per overlapping gene, unquoted, which breaks its own CSV writer and
fails the whole job. The operational rule is **one variant per job** in any overlap
region — which also makes the "Pangolin would take them in one job" plan for ClinVar's
456 intronic and 612 synonymous BUB1B records substantially more expensive than that file
assumed.

A wrong diagnosis that happens to prescribe the right next step is still a wrong
diagnosis, and it had been sitting in a committed file as settled.

### C25b — The output row is column-shifted, and inconsistently so

Allele 2 lies in a **triple overlap** (Ensembl REST): `ENSG00000156970` BUB1B,
`ENSG00000137843` PAK6, and `ENSG00000259288` **BUB1B-PAK6**, the readthrough. Pangolin's
row therefore shifts every column — `CHROM` reads `T`, `POS` reads `G` — and is not even
internally consistent: the first two genes come as pipe-delimited blocks, the **last
positionally in the trailing columns with no pipes**. A parser written for the pipe form
drops a gene silently. Ours did, and the gene-set assertion caught it on first run. That
assertion exists because of C24's lesson and it paid for itself within the hour.

**The readthrough is a repeat offender.** `ENSG00000259288` is the same transcript behind
one of the two Track 1 bugs, where first-match gene assignment split the causal variant
pair across BUB1B and its readthrough and filtered the correct answer out entirely. One
genomic overlap, two independent tools, two silent failures, found months apart. It now
carries a standing note in `SPLICE-ALLELE2.md` instead of waiting to be rediscovered a
third time.

### C25c — The HSP90 contraindication was in our prose and not in our gate

`ALLELE2-FOLDING-DOSSIER.md` states plainly that HSP90 inhibitors are contraindicated in
this child and that **"it should be added to Gate 3 as a refusal rule."** It never was.
The report's candidate table carried it as a "standing refusal", and `gate3_safety.py`
contained no mention of HSP90 at all. A refusal that lives in a sentence is not enforced
by anything; the gate is the instrument, and the organisers may rerun it.

Now implemented as a **genotype-conditional** rule rather than a drug blocklist, which is
the form that generalises. It refuses an inhibitory mechanism against HSP90/HSP70/HSF1
**when the patient's functional allele is a destabilised missense protein** — here, allele
1 is transcript-null, so the child's entire BubR1 supply is a destabilised missense allele
cleared by chaperone-dependent quality control, and Suijkerbuijk 2010 measured that HSP90
inhibition removes virtually all of it. For a patient with two truncating alleles there is
no destabilised protein to strip and the rule must not fire; `PATIENT_HAS_DESTABILISED_ALLELE`
is the switch. Evidence tiers are kept apart in the reason string: *measured* for HSP90,
*inferred* for HSP70/HSF1, where the direction is certain but nobody has measured it on
BubR1. An activator of the same targets is the therapeutic hypothesis, so only inhibitory
mechanisms are caught.

**It refuses nothing in the live funnel, and that is reported rather than left silent.**
No HSP90 inhibitor is approved, so Gate 1's approval tiering removes the class before Gate
3 sees it: 13 of 34 survive, unchanged. A rule that never fires is indistinguishable from
a rule that does not work, so `tests/test_gate3_chaperone.py` demonstrates it can — seven
cases covering the measured tier, the inferred tier, an activator of the same target
(must NOT refuse, or it would refuse our own lead), an unrecorded action (refused on the
precautionary side, because Open Targets leaves `actions` empty often enough that
treating empty as safe would void the rule), a non-chaperone drug, and the withdrawn
short-circuit. This follows standing rule 4: when an instrument reports no change,
establish that it could have reported one.

### What these two closures change about the answer

Nothing about the lead, and something about its shape. The splice null removes the last
route by which allele 2 might not be translated, so **allele 2 is made as protein** — and
the remaining uncertainty is no longer "what kind of lesion is this" across three options
but a two-way question, abundance versus function, which need opposite drugs. That is
narrowing by computation, which is the only kind available here, and it should be
presented as elimination rather than as having identified the mechanism.

## C26 — Re-examining the routes we closed for allele 2: the fragment-screen negative was narrower than we were using it, and is now broader than we could prove

14 Oct 2026. Prompted by a direct question — the agent rounds ranked three routes for
allele 2 and we closed the first by measurement; were the others actually closed, and had
the field solved this on other genes by a route we never considered? Full working in
`ALLELE2-ROUTES-REEXAMINED.md`; every number re-derives from
`scripts/mva/millet/degron_dockability.py` against committed structures.

**C26a — There IS a route we never considered, it has a fully worked published
precedent using our own tools, and it cannot be run on this protein.**

Friedreich ataxia is the same problem in a different gene: residual frataxin level sets
disease severity, frataxin is cleared by the ubiquitin–proteasome system, and there is no
fold-stabilising pocket. Rufini and co-workers built **ubiquitin-competing molecules** —
small molecules that bind the substrate and block its own ubiquitination, raising frataxin
and partially rescuing the aconitase defect in patient cells. The computational recipe is
published in full: MetaPocket consensus across eight pocket detectors (**LIGSITE** among
them), virtual screening with **AutoDock/Vina**, and — the decisive step — *site selection
concentrated near the ubiquitination lysine, Lys147*.

We have LIGSITE and Vina built and validated. The difference was entirely the site. We
looked for a non-functional allosteric pocket that could stabilise a fold; they looked for
any ligandable patch over the degron. **A UCM does not have to stabilise anything, so the
bar is much lower** — which is exactly why our 0-of-757 result did not close it.

So the fair objection is that we screened where the *mutation* is and not where the
*degradation* is. That objection is **correct about our reasoning and wrong about the
conclusion.** BubR1's degron lysines are K250 (acetylation shields it from APC/C) and
K668. From the committed full-length model: K250 sits at **pLDDT 47.5**, its ±10
neighbourhood at **41.8**; K668 at **30.2**, neighbourhood **31.5** — all "very low", which
is AlphaFold saying it does not know where these residues are. K250's side-chain nitrogen
has **10 protein atoms within 8 Å**: an exposed flexible loop, not a pocket. Frataxin's
K147 sits on the ordered surface of a small protein with NMR *and* crystal structures.
BubR1's degron lysines sit in its long intrinsically disordered middle, which is what
BubR1 is — a scaffold with disordered linkers. **There is no structure to dock against.**

**C26b — And that makes our central structural negative stronger than the version we were
asserting.** `MILLET-PROTOCOL.md` screened five boxes, all within residues 766–1050, and
found the one non-functional pocket was the best box for 0 of 757 fragments. Read
strictly, that is a claim about one domain. The report has been using it as if it closed
the structure-guided route for the whole protein, which it had not established — a scope
error of ours, not a wrong number.

It is established now, by a different argument: **the pseudokinase domain is the only part
of BubR1 that structure prediction models with any confidence, and inside it every good
pocket is a functional site. Everything else is disordered.** The negative generalises not
because we screened the rest but because the rest is not screenable. §3.4 of the report
now says this instead of implying the stronger claim without support.

**C26c — Our ATP-site exclusion is right for a reason we did not give.** The ATP site is
the one druggable pocket on the domain — best box for 364 of 757 fragments (48.1%) against
0 for the site we chose — and it was excluded in one line: *"the ATP pocket is intact in
this child and must stay that way"*, which presumes catalysis worth protecting. The
dominant view in the field does not support that premise: mammalian BubR1 is *"an untypical
pseudo-kinase"* whose kinase residues are conserved *"for structural reasons"*, and
*"catalytic activity of BubR1 is not required for any of its functions, at least in
mammalian cells"* (Marston & Wassmann 2017, citing Suijkerbuijk 2012). On that reading a
ligand in a structurally-conserved site is a candidate stabiliser, not an inhibitor.

**The opposing evidence is real, and flagging it is the C15/C19 lesson applied before the
fact rather than after.** Guo et al. 2012 found CENP-E stimulates BubR1 autophosphorylation
in vivo, and nonphosphorylatable BubR1 causes chromosome missegregation, failure of
Mad1/Mad2 to accumulate at unattached kinetochores, and incorrect spindle attachments.
The two sides then interlock, and that is what settles it: if BubR1's only functional
catalytic event is *CENP-E-stimulated* autophosphorylation, the ATP site and the CENP-E
interface are one functional unit — and MILLET excluded both. The exclusion stands, on
Guo rather than on the sentence we wrote. An ATP-site ligand for a pseudokinase would also
face a severe kinome-selectivity problem in a cancer-predisposed child.

**C26d — A decoy in our own screen is mislabelled, and the contradiction is internal.**
MILLET's decoy table calls the "C-terminal groove" *"real, functionally uninteresting"*.
It carries the **single best fragment score on the protein (−7.93)** and wins 164 of 757
fragments, so a genuinely non-functional pocket there would have been a *better* candidate
than the one we selected — "functionally uninteresting" is the eligibility criterion for a
pharmacological chaperone, not a disqualification. It is not non-functional: its centroid
is lined by residues **1041, 1046, 1047 and 1050**, inside the 1031–1050 CENP-E interface
that the same document excludes as functional. The label is wrong, the exclusion is right,
and no site was missed. The contradiction survived because nothing cross-checked the
site-selection step against the decoy table; `degron_dockability.py` now does.

**C26e — Route (b) is bounded, not open.** `BINDING-AND-STABILISING.md` §4(b) cites
ambroxol, found by screening 1,040 approved compounds with no structural insight, and we
never ran it. On this protein it is not a free option: the only druggable pocket is the
ATP site, so a blind approved-drug screen returns either ATP-site binders — the functional
site just argued to leave alone — or nothing.

**What none of this changes.** The abundance-versus-function question is untouched. Every
route above is about *how* you would raise BubR1; none says whether raising it is the right
thing to do. That still needs the measurement named in report §3.6. What did improve is
honest to report: one scope error of ours corrected, one exclusion re-grounded, one label
fixed, one route considered and closed with a reason, and the central negative made general.

## C27 — "A prior, not a result" was an under-description of a measured panel. The abundance thesis now carries a number.

14 Oct 2026, prompted by a flat assertion that raising abundance is the right move. Two
things were true at once: the assertion is well supported, and this workstream had been
describing the support as if it were merely a base rate. Both deserved fixing.
`scripts/mva/abundance_posterior.py` is the committed query.

**The number.** On the measured kinase-domain panel, **P(abundance) = 0.79, 95% CI
0.44–0.98** (Jeffreys-prior posterior predictive, 5 of 6 destabilising). Dropping the
sole exception gives **0.92, CI 0.62–1.00**. There is a real reason to drop it —
`ESTIMATE.md` records that Q921H "was on the same allele as L844F — the authors
concluded L844F was the causal one", so it was never tested as the only variant on an
allele, which makes it uninformative rather than a counterexample. **The 0.79 figure is
what ships.** Discarding the single inconvenient data point is not how a headline
number should be obtained, and both figures are printed so the choice is visible.

**Two axes that do not depend on the base rate, and I had underweighted both.**
`ESTIMATE.md` already said what separates Q921H from the destabilising set is not burial
but how conservative the substitution is. Computed:

- **Volume.** N1002K is **+54.5 Å³**. The destabilising set spans 20.2–64.9, so the
  proband sits *inside* it; Q921H is **9.4**, so the proband's change is **5.8×** the
  tolerated variant's.
- **Buried charge.** N1002K is the **only variant in the comparison that introduces a
  new formal positive charge**, at RSA 12.9% and pLDDT 91.1. Every charged panel member
  — R727C, R814H — *loses* charge instead. Burying an uncompensated positive charge in a
  confidently-folded core is a textbook destabilising substitution.

**A correction to my own framing two turns ago.** I wrote that the one tolerated variant
is more buried than allele 2, "so burial doesn't separate the classes" — and used that to
argue the prior is weak. The first clause is right and the inference was wrong. Burial
does not separate them; volume and buried charge do, and on those axes allele 2 groups
with the destabilising set rather than with the exception. Citing the axis that fails to
discriminate while omitting the two that do is the C15/C19 asymmetry pointed at my own
conclusion instead of someone else's.

**What does not change.** §3.6's claim that computation cannot settle abundance versus
function stands: a posterior over six comparators bounds a belief, it does not observe a
protein level, and the lower bound of the interval is 0.44. The in-disease precedent for
being wrong is specific and real — MVA-41C carries 35% residual BubR1, near-normal for a
single allele, and is affected (C6), so in this exact syndrome a patient can have enough
protein and still be ill. The falsifier is still one western blot.

What improved is the *form* of the claim. "Well supported but never measured" invited a
reviewer to supply their own number; "0.79, CI 0.44–0.98, from this panel, by this query"
does not.

## C28 — The two-class taxonomy I gave was one axis presented as the whole option space, and the in-syndrome evidence for high-risk intervention was already in our own repository

14 Oct 2026, prompted by a direct challenge: *are those really the only two options, and has
anyone tried a high-risk approach on an MVA gene and succeeded?* Both halves landed.

**C28a — The taxonomy was incomplete and I stated it as exhaustive.** I described the field
as having two classes — bind the target and stabilise it (migalastat, tafamidis, the
caftors) or raise folding capacity in *trans* (4-PBA, arimoclomol) — and concluded that
since our pocket is shut, class B is "the only class open to us". That is true **only of
the axis "make the existing protein fold better"**, which is not the same as the option
space. At least five further classes exist, and three are live concepts for this gene:

1. **Raise output rather than stability.** More transcript or more translation, not better
   folding. This is the *dominant* strategy in Friedreich ataxia, which I used as our
   closest analogy and then only described its degradation half. Directly relevant here:
   `Laberko 2019` records a group of patients with **monoallelic** *BUB1B* mutations
   hypothesised to cause MVA1 because they show **decreased *BUB1B* transcript and
   protein** — transcript level, not just protein stability, tracks the disease.
2. **Bypass the protein and deliver its function from another scaffold.** Verified:
   Herman et al. constitutively recruited PP2A-B56α to kinetochores using the
   **phosphomimetic BubR1 KARD fused to Mis12 (Mis12-KARD3D)**, and *"this protein fusion
   rescued"* chromosome alignment in BubR1-depleted cells. The KARD is a **15-residue
   linear motif (667–681, KKLSPIIEDSREATH)** in the disordered middle — we measured K668 at
   pLDDT 30.2 — so it is graftable precisely because it is not a folded domain. **The
   function is separable from the protein.** As therapy this is nothing: a plasmid-expressed
   fusion in cancer cells, with no delivery route to every dividing cell in a child. As a
   concept it belongs in the space, and it is what an mRNA or gene-therapy approach would
   exploit.
3. **Replace the cells** — HSCT, gene therapy, gene editing. See C28b; this has been tried.
4. **Treat the downstream consequence** — our own Thesis A (IL-1), and tumour-directed
   therapy. We ranked this second and then omitted it from the taxonomy entirely.
5. **Partner-mediated stabilisation** — raise a binding partner that stabilises the client
   rather than a chaperone. Untested for BubR1 and listed for completeness, not as a lead.

Why this matters beyond tidiness: a two-class framing makes the fragment-screen negative
look like it narrows the world to one answer. It narrows **one axis** to one answer. The
honest claim is that class A is closed *for BubR1*, not that the option space is.

**C28b — The answer to "has anyone tried a high-risk approach and succeeded" was already
in `MVA-THERAPEUTIC-EVIDENCE-BASE.md`, and it is more informative than my chat answer
implied.** That file tabulates every intervention reported in MVA and related aneuploidy
genes. The record splits cleanly, and the split is the finding:

**Worked — all of them removed or treated a *consequence*:**
- **Tamoxifen**, 12 months post-surgery, *MAD2L1BP* juvenile granulosa cell tumour —
  **complete remission, sustained.**
- **Surgery alone**, *MAD1L1* — 12 neoplasias by age 36, resected, **free of new pathology
  since 2014**.
- **Renal transplant at age 20** with ciclosporin, *BUB1B* MVA1 — reached 20-year follow-up.
  A solid-organ transplant under chronic immunosuppression was tolerated in this syndrome.

**Failed — all of them tried to fix or replace the *system*:**
- **HSCT in MVA1**, the same gene as our proband, and the most informative data point in
  the entire corpus. TCRαβ+/CD19+-depleted graft from a matched unrelated donor on
  treosulfan-based reduced-intensity conditioning. It **worked mechanistically**: engrafted,
  conditioning well tolerated, and it **cleared the monosomy 7 clone**. Then **graft
  rejection on day +47**, prolonged pancytopenia, multi-organ *Enterococcus faecium* sepsis,
  **death on day +156**. The authors' own conclusion: *"This fact needs to be taken into
  consideration for HSCT in other MVA patients."*
- **Growth hormone**, *CEP57* MVA2 — ineffective, with one report's authors writing *"Had
  this been known, growth hormone might have not been prescribed."*
- **G-CSF and romiplostim**, same MVA1 patient — *"no response."*
- **Valproate + levetiracetam**, *BUB1B* MVA1 — seizures continued.

**What the pattern says, and it is an empirical argument rather than a theoretical one.**
Our report rests surveillance primacy on LFS-style survival statistics — 59.6% → 88.9% —
which is borrowed from another syndrome. This table is **direct, in-syndrome evidence for
the same conclusion, and it is stronger**: in MVA, interventions that excised or treated a
consequence succeeded, and every intervention that attempted to repair the underlying
system failed. The HSCT case is the sharpest because it is not a story about a treatment
that did not work — it is a treatment that **achieved its stated mechanistic goal and the
patient died anyway**, of a complication belonging to the intervention rather than to the
disease.

That is the most important sentence available to us about aggressive intervention in this
child, and it was in our files while I was describing the option space from the drug
literature instead.

**C28c — A correction to how I reported this, separate from the science.** I initially told
the user this evidence was unnoticed in our corpus. It was not: `MVA-THERAPEUTIC-EVIDENCE-BASE.md`
already carried the full table with outcomes, and `STANDARD-OF-CARE.md:120` already cited
the HSCT case in its haematological-monitoring recommendation. The failure was in my
answer, which built a taxonomy from the pharmacology literature without consulting the
in-syndrome evidence file this workstream had already written. Reaching for the general
literature while a specific, better-matched source sits in the repository is the same error
as C24's — not running the instrument we already had.

---

## C29 — The eligibility map had never been tested against a label we did not generate. It now is, and one of the two tests is largely circular.

Found by running the `be-ambitious` skill against our own deliverable, on its fourth
question: *what, other than you or me, would show the result is right?*

**The deficiency.** Every validation in this workstream tested whether an instrument
REPRODUCES something. The sentinel gate reproduces committed Pangolin scores. The
TrunKitten self-test reproduces a prediction the upstream pipeline already made. The
export audit reproduces a working tree. Not one of them asked whether the map's calls
PREDICT an independent label. Those are different questions, and only the first was ever
being asked — across a fortnight of validator-building, which is why the gap survived.

`validate_map.py` adds two tests whose labels we did not produce.

**TEST 1 — held-out positive controls. PASS, and cleanly.** ClinVar flags 13 BUB1B
variants as canonical splice donor/acceptor. Four carry committed reference scores and are
used as in-sweep sentinels, so they are not independent. The other **12 are held out** —
known mechanism, nothing in this pipeline tuned against them. **12 of 12 are called.**

**TEST 2 — does a splice call predict a pathogenic ClinVar label? PASS on the arithmetic:**

```
              pathogenic  benign
  called              11       2
  not called           0     658
```

Fisher exact, one-sided, enrichment in the called group: **p = 2.7e-22**, OR infinite.

**C29a — and that p-value is worth much less than it looks.** The test was written before
the result was seen, with a stated pass criterion, so the number is not post-hoc. But the
number is not the claim either, and checking its composition is what matters: of the **11
pathogenic variants the map calls, 10 are canonical ±1/±2** splice positions. Only **one**
sits deeper — c.1402-5A>G, at −5, a variant we already held.

So what Test 2 mostly measures is *can Pangolin find a canonical splice site*, which is
easy, and which is also **why ClinVar called those variants pathogenic in the first
place**. The label and the prediction share a cause. The honest reading:

> The map recovers known canonical splice variants without exception, and the enrichment
> test is consistent with signal. It does **not** yet demonstrate that the map finds
> non-canonical mechanisms ClinVar has missed, because ClinVar contains essentially none
> to find: the deeper-variant evidence is **n = 1**.

That sentence travels with the result wherever the result goes. The test earns its keep by
ruling out the failure mode where the map is noise; it cannot carry the claim that the map
is novel, and nothing in the write-up may let it.

**C29b — Test 1's first run reported FAIL on 2 of 12, and the fault was mine, not the
map's.** `noncoding_eligibility.tsv` on disk had been generated when 129 variants were
scored and was being compared against a 725-variant scored set. A stale intermediate, the
same defect class as C24c — a producer fixed days before an output that was never
regenerated. Re-running `pangolin_sweep_report` → `eligibility_join` → `validate_map` in
order gave 12/12. Recorded because an external test that FAILS for an internal reason is
the most dangerous possible result: it would have been read as the map being broken, and
the real fault — our own ordering discipline — would have survived.

**C29c — the AlphaFold dependency was never a weakness, and we had never measured it.**
The report leans on an AlphaFold model for allele 2 without ever stating why an
experimental structure was not used. Parsing all five BUB1B PDB entries for modelled
residues settles it:

```
5JJA  modelled 23-30     (8 residues)    pseudokinase 766-1050: 0
3SI5  modelled 10-161    (152)           pseudokinase 766-1050: 0
5LCW  modelled 19-342    (277)           pseudokinase 766-1050: 0
5KHU  modelled 18-308    (219)           pseudokinase 766-1050: 0
6TLJ  modelled 19-345    (293)           pseudokinase 766-1050: 0
```

**Zero residues of the pseudokinase domain are modelled in any experimental structure of
this protein.** The best of them stops 421 residues short of p.Asn1002. A predicted model
was not a convenience, it was the only option, and the correction is that we never said so
— a documentation failure rather than a scientific one.

---

## C30 — Four failed sweep jobs had a single cause, and chasing it found two defects in the resume logic that were worse than the failures.

Four of 221 Pangolin jobs failed (plan indices 29–32, ~96 variants). The temptation was to
treat four failures in 221 as attrition and move on. Diagnosing them instead:

**C30a — the overlap boundary was wrong by about a kilobase, and it is the whole cause.**
C25a established the mechanism: a variant whose annotation spans two genes breaks
Pangolin's CSV writer and fails the entire job it rides in, so such variants must be
submitted alone. The constant implementing that was `OVERLAP_FROM = 40218500`, the start of
the BUB1B-PAK6 **readthrough**. PAK6 itself begins at **40,217,428**. Everything in between
was being batched when it should have been solo.

Every one of the four failed jobs contains at least one variant at or past 40,217,428, and
those four jobs contain every such variant in the corpus. Job 29 carried only **4** of them
among 26 variants and still failed outright, which is the mechanism behaving exactly as
C25a described. Corrected to `OVERLAP_FROM = 40217428`; 71 variants move from batched to
solo. The mechanism was right and the number implementing it was not — the kind of defect a
validator cannot see because nothing it measures changes.

**C30b — a failed job counted as a completed one, so its variants were lost silently and
permanently.** Resume keyed on `plan_index`, read from every archive row. A failed job
writes a row like any other. So on every subsequent run all four jobs were skipped as
"already archived", and those ~96 variants would have stayed `PENDING_not_yet_scored` in
the map forever while the sweep reported itself finished. Nothing in the pipeline would
have objected: the map has a legitimate pending state, so permanent silence looks like
ordinary progress.

**C30c — and the fix in C30a would have corrupted the archive, because `plan_index` is
positional.** Changing `OVERLAP_FROM` changes the plan (33 batched → 1, 188 solo → 259), so
index 50 in the new plan is a different job from index 50 in the archive. A job-keyed
resume would have skipped the wrong work and every count downstream would have described a
corpus that does not exist — standing rule 4's `--only` trap, arrived at from a different
direction. The correction to C30a could not ship without this one.

Both go away by keying resume on the **variant** rather than the job: a re-run replans only
variants carrying no score, so failed jobs retry by construction and a corrected plan
cannot misalign. The scored set is read with the report's own `parse_rows`, imported rather
than copied, so "scored" means one thing in this pipeline. A third defect falls out for
free: `parse_rows` drops rows eaten by the C25b multi-gene column shift, so a variant that
vanished from a job that *completed* is also pending again, which a job-keyed resume could
never express.

The dry run now reports the real state rather than a positional one:

```
725 variants already carry a score and are not replanned
1005 verified variants -> 260 jobs (1 batched, 259 solo)
```

**What this says about the four failures.** They were not attrition. They were a correct
mechanism with a wrong constant, sitting on top of a resume path that converted failures
into silent omissions — and the omission was the serious half. Four visible failures led to
one invisible defect that had already armed itself to misreport the finished sweep.

---

## C31 — 188 variants were scored, archived, and silently discarded. They are the 3' end of the gene, and eight of them are calls.

C30 fixed the resume path and the sweep then reported **725 of 1,005** variants scored
after 217 jobs had completed. That number is exactly 29 batches x 25, which means the
**188 completed solo jobs had contributed nothing at all**. Checking why, rather than
accepting a plausible total, is the whole of this entry.

**What the discarded rows actually contain.** Every solo job is a PAK6-overlap variant,
and in that region Pangolin emits one result block per overlapping gene -- three of them
(BUB1B `ENSG00000156970`, PAK6 `ENSG00000137843`, and the BUB1B-PAK6 readthrough
`ENSG00000259288`) -- which overflows the CSV's columns and drops CHROM and POS entirely:

```
CHROM,POS,REF,ALT,pangolin_gene,splice_gain_pos,splice_gain_score,splice_loss_pos,splice_loss_score
A,T,ENSG00000156970.13|3:0.25|-45:-0.61|Warnings:,ENSG00000137843.12|3:0.25|-50:0.0|Warnings:,ENSG00000259288.7,3,0.25,-50,0.0
```

`parse_rows` read position from the second field, got `T`, and dropped the row as
"shifted" (C25b). It was right to refuse — but the refusal was recorded as a *parse*
statistic while the map reported those variants `PENDING_not_yet_scored`, so a region
that had been **measured and paid for** looked like a region that had not been reached.
This is C30b's failure mode a second time, in a different component: a legitimate
"not yet" state absorbing a real loss.

**Eight of the 188 are calls at our threshold**, and they are not marginal:

```
chr15:40218563 G>A   loss -0.82      chr15:40218501 A>T   gain +0.25  loss -0.61
chr15:40218567 G>A   loss -0.82      chr15:40218538 G>A   loss -0.50
chr15:40220602 G>A   gain +0.63      chr15:40218502 A>G   loss -0.42
                                     chr15:40218526 A>G   loss -0.33
                                     chr15:40218503 G>T   loss -0.26
```

Two of them score **-0.82**, stronger than three of the four committed reference
variants (-0.73, -0.71, -0.69). The map's called set goes from **38 to 46**. And the
region is not an arbitrary 188: it is the **3' end of the coding sequence**, which is
precisely where the 50-55 nt rule decides NMD escape, so it is the part of the gene most
likely to produce a truncated protein that is actually present. The map was blind in the
one place its therapeutic question is most answerable.

**C31a — and the obvious fix is wrong one time in five.** The tempting one-line change is
to read the trailing plain columns, which parse as numbers. Those columns hold the **last**
gene's scores, not BUB1B's: they disagree with BUB1B's own block in **37 of 188** rows. So
the shortcut would have attributed PAK6's or the readthrough's splice score to BUB1B
across a fifth of the region — replacing "no answer" with "a confident wrong answer,"
which is strictly worse. Recorded because the shortcut is what a reasonable reader of the
file would try first.

**The fix, and why it is a recovery rather than a repair.** `recover_multigene` finds
BUB1B's block **by its Ensembl gene ID**, never by column position, and takes the variant's
position from the job's own submitted list — and only when that list holds exactly one
variant, so a row can never be mis-attributed. A multi-variant job with a shifted row is
still dropped, because a position that cannot be attributed is not a result.

Result: **725 -> 913 of 1,005 scored**, 188 recovered, and all four sentinels still
reproduce exactly (`+0.49/-0.73`, `+0.85/-0.69`, `+0.73/-0.89`, `+0.76/-0.71`). The gate
could have caught a regression here and did not fire, which is the condition rule 4 asks
for before believing an instrument that reports no change.

---

## C32 — Building the benchmark the ClinVar test could not be, and nearly publishing someone else's dataset to do it

C29a established that `validate_map.py`'s p-value of 2.7e-22 is close to meaningless:
easy positives (10 of 11 canonical) and free negatives (658 common variants far from any
splice site). The fix is a different data source, not a better statistic.

**The source.** MFASS (Chong et al., *Mol Cell* 2019, doi:10.1016/j.molcel.2018.10.037) —
a multiplexed splicing reporter assay over 27,733 ExAC variants in 2,198 human exons, each
with a **measured** exon-inclusion index. It fixes both margins at once: the positives are
measured rather than inferred from a clinical label, the negatives are variants **assayed
and found not to disrupt splicing in the same sequence contexts**, and the authors state
that these variants are *"difficult to predict a priori."*

Our reconstruction of their classes reproduces the paper's headline exactly — **1,050
splice-disrupting variants of 27,733 = 3.8%** — which is the external check on our own
parsing before any of it is used. By region:

| region | n | measured SDV rate |
|---|---|---|
| canonical (intronic 1-2) | 546 | **104/497 = 20.9%** |
| non-canonical intronic | 13,826 | 420/13,272 = 3.2% |
| exonic | 14,600 | 526/13,964 = 3.8% |

**90.1%** of the splice-disrupting variants are outside the canonical sites. The paper says
83%; the difference is a definition of "canonical site" the abstract does not give, and
ours (intronic offset 1-2 only) is stated rather than reconciled. The benchmark pool is
therefore **946 measured positives and 26,290 measured hard negatives**, all non-canonical.

The low prevalence is the part that matters for us. At a 3.2% base rate, specificity
dominates precision, and `CALL = 0.2` was never set from a measurement — it was set
because the four reference variants all score >= 0.49, which establishes a **floor, not a
threshold**. Pass criteria are fixed in `mfass_benchmark.py` and in its metadata **before
scoring**: sensitivity >= 0.70 passes and < 0.50 fails; specificity >= 0.80 passes and
< 0.60 fails. A specificity failure is named in the file as the expected result.

**C32a — I nearly committed the MFASS dataset into a CC BY 4.0 submission repository.**
The first run wrote a 27,236-row table of coordinate + ref + alt + measured outcome to
`docs/mva/data/nmd/`. That table **is** the MFASS dataset. The source repository
(`github.com/KosuriLab/MFASS`) carries **no licence file** — confirmed by 404 at both
`LICENSE` and `LICENSE.md` — so all rights are reserved and redistribution is not ours to
do, least of all into a repository that publishes under CC BY 4.0. This is the same finding
and the same treatment as `CobanAkdemirlab/NMDpredictionmodel`: **use and cite, never
vendor**. The per-variant sample now goes to an uncommitted path via `--out`, and only
aggregate counts are committed, because counts are facts about the data rather than the
data. Pangolin itself is GPL-3.0 and carries its licence, so running it locally is clean.

**C32b — two columns in the published table cannot be used as documented, and testing
beat assuming both times.**

- `rel_position_feature` looked like the offset from the exon boundary and would have
  given the canonical/non-canonical split for free. Tested against three candidate
  conventions, the best fitted **3,681 of 28,972 rows (13%)**. Had it been assumed, 87% of
  the benchmark would have been mislabelled by region — and nothing downstream would have
  objected, because the resulting numbers all look reasonable.
- The `strand` column **contradicts its own coordinates for 6 of the 2,198 exons**
  (`ENSE00000933530`, `ENSE00001002968`, `ENSE00001321140`, `ENSE00001339922`,
  `ENSE00001602316`, `ENSE00001768088`; 97 variants). Found because the geometry gate
  required `rel_position` to be recoverable from the coordinates on every row and refused
  to classify when 97 failed. Strand is now **derived per exon** from agreement across all
  of that exon's variants, and an exon where neither orientation fits every row is dropped
  rather than guessed. None had to be.

The gate refusing at 99.67% is the useful part of this entry. A threshold of "near enough"
would have passed it and mis-placed every variant in those six exons.

---

## C33 — The base rate behind the whole non-coding workstream, stated as a rate for the first time

C17 enumerated four independent reports in which the second *BUB1B* allele was found
outside the coding sequence, and called the architecture "a pattern, not an anecdote."
That is a numerator with no denominator, and it has been carrying the non-coding
workstream for weeks without one. The `be-ambitious` skill's second question — *check the
base rate* — is what surfaced it.

**The denominator exists and is in the same paper we were already citing.** Matsuura 2006
(doi:10.1002/ajmg.a.31069), verified against PubMed, is titled *"Monoallelic BUB1B
mutations ... in seven families with premature chromatid separation (PCS) syndrome"* and
states:

> *"Monoallelic BUB1B mutations were found in all seven families studied ... **No mutation
> was found in the second alleles in the seven families studied**, but RT-PCR of BUB1B and
> Western blot analysis of BubR1 indicated a modest decrease of their transcripts."*

So in the one cohort that reported it systematically, **coding analysis of *BUB1B* found
exactly one allele in 7 of 7 families.** The same abstract supplies a second, independent
cohort by citation: biallelic *BUB1B* mutations were reported in **5 of 8** MVA families,
leaving three unexplained — though that paper's three are not necessarily monoallelic
*BUB1B*, so they are reported and not added in.

**What ships, and what does not.** The claim is *"in the only series that reported it
systematically, coding analysis of BUB1B identified a single allele in 7 of 7 families
(Matsuura 2006)"*, with the four located non-coding alleles of C17 as the demonstration
that such alleles are findable. What does **not** ship is a pooled percentage across the
48 papers with "mosaic variegated aneuploidy" in the title: a proper denominator needs a
systematic review of all of them, that review has not been done, and a pooled rate
asserted without it would be the kind of number this ledger exists to catch. The 7/7 is a
**floor from one cohort**, in-syndrome, in the pre-genome-sequencing era, and it is
labelled as such.

**C33a — the same abstract carries the dose-response datum our therapeutic thesis needs,
and we had not used it.** Matsuura's conclusion is that *">50% decrease in expression (or
activity) of BubR1 is involved in the PCS syndrome"*, measured by RT-PCR and Western blot
in patients whose transcripts showed only a *"modest decrease"*. That is in-syndrome,
protein-level evidence for exactly the threshold our abundance argument rests on — a
partial reduction, in a monoallelic patient, producing full disease — and C17's own
closing paragraph had already flagged that we were arguing about "reduced BubR1" without
ever naming a level. The level was in the abstract of the paper the table cites.

---

## C34 — A third copy of the archive parser, in the file whose whole job is to report coverage honestly — and a correction to C30's own claim

After C31 recovered 188 variants upstream, `validate_map.py` returned **numbers identical
to the previous run**: the same 11 pathogenic, 2 benign, 658 not-called. A map that had
grown from 725 to 913 scored variants and from 38 to 46 calls cannot produce an unchanged
2x2. Chasing that is this entry.

**`eligibility_join.py` carried its own third copy of the archive parser.** Not an import
— a reimplementation, doing `int(f[1])` and discarding anything that failed, with a
comment correctly citing C25b. So every multi-gene row was dropped *there* too, the entire
PAK6 overlap was still marked `PENDING_not_yet_scored` in the map, and `validate_map`
excludes pending rows by design. The upstream recovery was real and the map never saw it.

**This is a correction to C30, not only to the code.** C30 stated: *"The scored set is read
with the report's own `parse_rows`, imported rather than copied, so 'scored' means one
thing in this pipeline."* That was true of the two files I had looked at and false of the
pipeline, because I asserted a property of the whole from the two components I happened to
be editing. The claim should have been checked by grepping for the third copy, which takes
one command. Fixed by importing: one definition, three callers.

**What it was costing.** With the join corrected:

| | before | after |
|---|---|---|
| non-coding scored | 725 | **934** |
| pending | 280 | **71** |
| map rows with DIRECT evidence | 790 (31.2%) | **999 (39.4%)** |
| pathogenic variants called (Test 2) | 11 | **12** |
| Fisher p | 2.723e-22 | **1.433e-24** |

**C34a — and the circularity caveat does NOT improve, which is the part that matters.**
The newly called pathogenic variant is `c.2896A>T`, and it cannot be counted as a
non-canonical win: ClinVar gives its molecular consequence as *intron variant* while its
HGVS carries no intronic offset at all, so the coordinate and the annotation contradict
each other. That is the same defect class as `c.2577+5G>A` in SPLICE-AXIS.md — a probable
transcript mismatch — and it is **unresolved**, not favourable. The composition is now:

```
  pathogenic variants called: 12
    canonical +/-1,2                                   10
    genuinely deep intronic                             1   (c.1402-5A>G, already held)
    annotation internally inconsistent, unresolved      1   (c.2896A>T)
```

So the deeper-variant evidence remains **n = 1**, and C29a's caveat ships verbatim and
undiminished: the enrichment test does not demonstrate that the map finds non-canonical
mechanisms ClinVar has missed. A bigger p-value on a larger easy set is not progress on
that question, and the MFASS benchmark (C32) exists because no amount of ClinVar will be.

---

## C35 — 200 of the 1,005 variants in the "non-coding" map are exonic on the canonical transcript. The map is right; its name over-claims.

Completing the sweep to 1,005/1,005 produced a false negative in Test 2 — a pathogenic
variant the map does not call — and the obvious move was to report it as the map's first
honest miss. Checking it instead found something about the whole set.

The missed variant is `c.2876T>G`, and one of the two variants counted as a *non-canonical*
call is `c.2896A>T`. Both carry ClinVar's molecular consequence **intron variant** while
their HGVS has no intronic offset at all. Tested against our own exon model, both sit
**inside CDS exon 22** (chr15:40,218,456–40,218,562).

**It is the consequence label that is borrowed, not our coordinates.** Of the 200
ClinVar-"intronic" variants that fall inside a CDS exon, the HGVS agrees with our CDS
numbering for **200 of 200**, and the model independently reproduces both of the proband's
alleles:

```
  c.2876T>G            chr15:40218481   our model CDS 2876   HGVS 2876   MATCH
  c.2896A>T            chr15:40218501   our model CDS 2896   HGVS 2896   MATCH
  allele 2 c.3006T>G   chr15:40220612   our model CDS 3006   HGVS 3006   MATCH
  allele 1 c.2210T>G   chr15:40209701   our model CDS 2210   HGVS 2210   MATCH

  of the 200: HGVS agrees with our CDS numbering  200
              HGVS disagrees                        0
```

> **MECHANISM WRONG, corrected in C36.** The sentence below attributes the mislabelling
> to an alternative *BUB1B* transcript. Tested, that holds for only **2 of 200**: the
> consequence actually comes from **PAK6**, an overlapping gene. Our transcript is
> Ensembl-canonical and correct. The scope correction in this entry is unaffected.

So *BUB1B* has transcripts on which these positions are intronic, ClinVar's consequence
field reports one of those, and its HGVS reports the canonical one. Our set was built by
querying `"intron variant"[Molecular consequence]`, so it inherited the mismatch 200 times
over. This is `c.2577+5G>A` from SPLICE-AXIS.md — one hand-mapped transcript mismatch — at
two hundred times the scale, found only because a single false negative was worth chasing.

**What this does and does not invalidate.**

*Scoring them was correct.* An exonic variant can disrupt splicing through an exonic
splicing element, and our own MFASS reconstruction (C32) measures that at **3.8% of exonic
variants** — a higher rate than non-canonical intronic ones. These variants belong in a
splice-eligibility map.

*Calling the map "non-coding" does not survive.* The composition of the 1,005:

| | n | status |
|---|---|---|
| synonymous | 563 | exonic by definition; deliberately in scope from the start |
| ClinVar-"intronic", inside a CDS exon | **200** | **exonic on the canonical transcript** |
| genuinely intronic, incl. canonical splice sites | 242 | the actually non-coding part |

So **763 of 1,005 are exonic**, and the honest description is *"1,005 ClinVar variants that
a protein-level predictor cannot score"* — which was always the real scope — not *"the
non-coding half."* The claim that a coding-only pipeline would miss these applies to the
**242**, not to the 1,005, and every use of the larger number for that argument is
corrected to the smaller one.

**C35a — and the circularity caveat is now confirmed rather than merely unimproved.** Both
variants that had looked like non-canonical progress are in the 200. The composition of the
13 pathogenic calls:

```
  canonical +/-1,2                                      11
  genuinely deep intronic                                1   c.1402-5A>G, already held
  exonic, mislabelled intronic by ClinVar                1   c.2896A>T
  --- and the one false negative, also in the 200 ---        c.2876T>G
```

The genuinely deep non-canonical evidence is **one variant**, the same one it was at 725
scored and at 913. Three successive expansions of the map have not added a single new deep
intronic pathogenic variant, because ClinVar does not contain them — which is precisely the
reason the MFASS benchmark exists, and is now an argument from three attempts rather than
from one inspection.

---

## C36 — C35's mechanism was wrong. The transcript is ours and correct; the mislabelling comes from a different GENE.

C35 stated that *"BUB1B has transcripts on which these positions are intronic, ClinVar's
consequence field reports one of those, and its HGVS reports the canonical one."* Prompted
by the reasonable objection that the transcript error could just as easily be **ours**,
that explanation was tested and it is **false**.

**First, our transcript is right, and the evidence is external rather than self-consistent.**
`ENST00000287598` is Ensembl's **canonical** transcript for *BUB1B* (`is_canonical: 1`), 23
exons, translation 1,050 aa. Our committed exon model sums to **3,153 nt = 1,050 aa + stop**,
matching UniProt **O60566** exactly, and it reproduces the HGVS of both of the proband's
alleles from genomic coordinates alone (`c.2210T>G` at chr15:40,209,701 and `c.3006T>G` at
chr15:40,220,612). Agreement with ClinVar's own HGVS was *not* sufficient evidence on its
own — if ClinVar and we had both chosen the same non-canonical transcript we would agree
and both be wrong — which is exactly why this needed the independent check.

**Second, C35's explanation fails on its own test.** Of *BUB1B*'s 31 annotated transcripts
(12 protein-coding), the number in which those 200 positions are intronic is **2 of 200**:

```
  intronic in at least one BUB1B transcript    2 / 200
  intronic in no BUB1B transcript            198 / 200
```

**Third, the real mechanism.** All 200 positions sit in CDS exons **22 and 23** — the last
two — and every one is at or past **chr15:40,217,428**, which is where **PAK6** begins.
Testing against PAK6 and the BUB1B-PAK6 readthrough:

```
  intronic in a PAK6 / readthrough transcript   200 / 200
    ENST00000453867  PAK6  protein_coding   explains 200
    ENST00000441369  PAK6  protein_coding   explains 200
    ENST00000559435  readthrough  NMD       explains  30
```

So ClinVar's molecular-consequence field for these records reports a consequence computed
on **PAK6**, an overlapping *gene*, not on an alternative *BUB1B* transcript. Our query was
`BUB1B[gene] AND "intron variant"[Molecular consequence]`, which does not require the
consequence and the gene to refer to the same feature — so 200 PAK6-intronic,
BUB1B-exonic variants entered a set described as BUB1B intronic variants.

**What stands and what is replaced.** C35's *scope* correction stands unchanged and is
unaffected by the mechanism: 763 of 1,005 are exonic on the canonical transcript, the set
is honestly described as *"ClinVar variants a protein-level predictor cannot score"*, and
the coding-pipeline-recall argument applies to the 242 genuinely intronic ones. What is
replaced is the explanation, and the replacement is more useful: the remedy is not to pick
a different transcript but to require the consequence and the gene to refer to the same
feature when the set is built. Until that query exists, the 200 are labelled
**BUB1B-exonic, PAK6-intronic** rather than either "intronic" or "mislabelled".

**The pattern worth keeping.** This is the **third** independent defect in our pipeline
caused by one genomic fact — that PAK6 overlaps BUB1B's last two exons. It failed four
Pangolin jobs outright (C30a), it mangled 259 result rows in two different column layouts
(C31, C35), and it contaminated the consequence annotation of 200 ClinVar records (here).
Every one presented as something else first: a batch failure, a parse statistic, a
transcript mismatch. The region is also where the 50–55 nt rule decides NMD escape, so it
is the part of the gene the therapeutic question most depends on, and it is the part our
instruments have been worst at.

---

## C37 — The query is fixed by not asking ClinVar the question. Region is now derived, gated on a selftest, and C35/C36's own counts are corrected.

C36 identified the cause — ClinVar's `[Molecular consequence]` filter does not require the
consequence and the gene to describe the same feature, so PAK6's intron annotation entered
a BUB1B set. The remedy is not a cleverer ClinVar filter. *Is this position exonic or
intronic on ENST00000287598* is a question we can answer exactly from committed data, so
the fix is to stop sourcing it from a third party's gene-agnostic field.

**`bub1b_regions.py`** derives the region for all 1,005 variants from the canonical
transcript and keeps ClinVar's consequence verbatim as provenance and as something to
disagree with, never as the classification. The full transcript model
(`docs/mva/data/bub1b_transcript.json`, ENST00000287598.11, 23 exons incl. UTRs) was
fetched fresh, and it **derives the committed CDS-only exon model identically** — a third
independent check on that model after UniProt O60566 and the two proband alleles.

**The selftest is what makes the output trustworthy, and it is deliberately hard.** The
four reference variants have intronic offsets in their names, and the module must
reproduce each offset *and which side of the exon it falls on*, from the coordinate alone
— then both proband alleles' CDS positions. Nothing is written unless all six pass:

```
  c.1288+5G>A    chr15:40196779  offset   +5  expected  +5  PASS
  c.1402-5A>G    chr15:40200239  offset   -5  expected  -5  PASS
  c.2386-11A>G   chr15:40212488  offset  -11  expected -11  PASS
  c.2009+1G>A    chr15:40206459  offset   +1  expected  +1  PASS   [canonical_splice_site]
  allele 1       chr15:40209701  cds_exonic  CDS 2210  expected 2210  PASS
  allele 2       chr15:40220612  cds_exonic  CDS 3006  expected 3006  PASS
```

**The derived composition, which supersedes the figures in C35 and C36:**

| region on ENST00000287598 | n |
|---|---|
| `cds_exonic` | 763 |
| `intronic` | 226 |
| `canonical_splice_site` | 15 |
| `utr3_exonic` | 1 |

**C37a — C35 and C36 said 200 conflicts and 242 non-coding. The correct figures are 201
and 241**, and the reason is instructive: those entries tested positions against the
**CDS-only** exon model, which has no way to distinguish a 3'UTR position from an intronic
one. The one `utr3_exonic` variant was therefore counted as intronic. It is exonic, it
conflicts with ClinVar's intronic label like the other 200, and the genuinely non-coding
count is 226 + 15 = **241**. An exon model missing its UTRs cannot answer the question
those entries were asking, and both of them used it to answer that question anyway.

**What the map now says.** `variant_class` was `non-coding/<ClinVar consequence>` — a
label that asserted the thing being got wrong, twice over, from the contaminated field.
It is now `splice-scored/<derived region>`, which claims only what was done and where the
variant is:

```
  splice-scored/cds_exonic              763
  splice-scored/intronic                226
  splice-scored/canonical_splice_site    15
  splice-scored/utr3_exonic               1
```

The join refuses to run without the derived regions rather than falling back to the
ClinVar field, and the two downstream counters plus `validate_map`'s population filter
were updated with it — `validate_map` measures every variant scored for a splice effect,
which is the right population for its question, and no longer describes that population
as "non-coding".

**The number the recall argument may use is 241**, not 1,005. The larger number is the set
a protein-level predictor cannot score, which is a true and different claim.

---

## C38 — The benchmark's pre-registered prediction was wrong in the opposite direction, and the file reporting it had a sampling bug. **INTERIM at 18% coverage.**

`mfass_score.py` was written with its expected outcome stated in the file before any
variant was scored: *"The result to expect, named in advance: a specificity failure.
CALL=0.2 was set because the four committed reference variants all score >= 0.49, which
establishes a FLOOR, not a threshold."*

**That prediction is wrong, and wrong in the direction that matters.** At 871 of 4,946
scored (18%, a random subset — the sample is shuffled with a fixed seed before writing, so
an interim read is unbiased rather than front-loaded):

```
                 called   not called
  measured SDV       58          118
  measured not        8          687

  sensitivity  0.330   (95% CI 0.264-0.402)   pass >= 0.70, fail < 0.50   FAILS
  specificity  0.988   (95% CI 0.977-0.994)   pass >= 0.80, fail < 0.60   passes
  ROC AUC      0.882
```

The sensitivity interval's upper bound is **0.402**, already clear of the 0.50 fail line,
so the verdict will not reverse on the remaining 82%. `CALL = 0.2` is not too permissive.
It is far too **strict**, and the floor-not-a-threshold reasoning was sound while the
inference drawn from it was backwards: a threshold set below four known-strong variants
turns out to sit well above the bulk of real disruption.

**Wrong threshold, not wrong approach — and the ROC is what separates those.** AUC 0.882
says Pangolin discriminates non-canonical splice disruption well; the operating point is
what is broken. The sweep:

```
  thr    sens   spec   precision(sample)
  0.1   0.517  0.971  0.820
  0.2   0.330  0.988  0.879   <- shipping
  0.3   0.199  0.996  0.921
  0.5   0.142  1.000  1.000
```

Even 0.1 reaches only 0.517 sensitivity, so clearing 0.70 requires going below 0.1. The
consequence for the deliverable is direct: **the map's 52 calls out of 1,005 are an
undercount**, and at sensitivity 0.33 the shortfall is on the order of two-thirds of the
real splice-disrupting variants rather than a rounding error.

**C38a — and the file reported precision wrongly, in the flattering direction.** It printed
0.879 labelled *"at the measured prevalence; the number a reader of the map needs."* The
benchmark sample deliberately takes **all 946 positives and only 4,000 negatives**, so its
prevalence is **19.1%**, not the 3.2-3.8% measured in our own reconstruction (C32).
Precision computed on that sample is inflated by the sampling design. Corrected via
sensitivity and specificity, which the sampling does not distort:

| true prevalence | corrected precision |
|---|---|
| 3.2% (non-canonical intronic) | **0.476** |
| 3.8% (exonic) | **0.521** |

So roughly **half** the calls would be wrong at the rate these variants actually occur —
not the 12% the enriched sample implied. The claim was wrong in the direction that made
our instrument look better, which is the direction to be most suspicious of. Both values
are now printed, the sample one labelled inflated, and the corrected one named as the
figure that decides whether a clinician could read this map.

**The caveat that is load-bearing for THIS result specifically.** The file states, written
before any result existed, that *"a sensitivity failure here is weaker evidence than a
specificity failure -- the negatives are the part the assay is least able to get wrong"*,
because MFASS is a minigene reporter in a cell line and measures exon recognition in a
construct rather than endogenous splicing at the native locus. Sensitivity is precisely
what failed, so that caveat now sits on the load-bearing number and must travel with it
rather than be dropped for being inconvenient. The honest statement:

> At its shipping threshold the map is highly specific and badly under-sensitive. The
> signal is real (AUC 0.88), so the operating point rather than the method is at fault,
> and some unknown part of the sensitivity gap belongs to the reporter assay rather than
> to the predictor.

Re-deriving the threshold waits for the full 4,946. These numbers are **interim** and the
completed run supersedes them.

---

## C39 — The threshold is re-derived from measured outcomes, on a held-out split, and the map now reports tiers. **INTERIM at 22% of scoring.**

C38 showed `CALL = 0.2` failing the pre-registered sensitivity bar (held-out 0.317 against
0.70) while passing specificity (0.985), with AUC 0.882 placing the fault in the operating
point. `mfass_threshold.py` re-derives it.

**It derives on half the benchmark and reports on the other half, and that mattered
immediately.** A threshold chosen on the same data it is scored against reports its own
best case. The gap is large enough to have misled us:

```
  CALL_SCREEN derived at 0.05   derive-split sensitivity 0.757
                               HELD-OUT     sensitivity 0.615     overfit gap +0.142
```

Naive tuning on the benchmark would have claimed 14 sensitivity points it does not have.

**The finding is not a better threshold. It is that no single threshold exists.** Held out,
at the 3.2% rate these variants actually occur:

| threshold | sensitivity | specificity | precision | wrong calls per right call |
|---|---|---|---|---|
| 0.20 | 0.317 | 0.985 | 0.417 | 1.4 |
| 0.10 | 0.481 | 0.961 | 0.289 | 2.5 |
| 0.05 | 0.615 | 0.910 | 0.184 | 4.4 |
| 0.03 | 0.683 | 0.897 | 0.180 | 4.6 |

Tripling sensitivity costs more than half the precision. That is the arithmetic of a low
base rate against AUC 0.88, not a tuning failure, and **the pre-stated 0.70 sensitivity bar
is not reachable**: the best held-out value is 0.683 (CI 0.588–0.764), which straddles it.
Reporting that the bar was missed, rather than moving it, is the point of having stated it.

**C39a — and `CALL = 0.2` turns out to have been a good threshold used for the wrong job.**
Held out it gives specificity 0.985 and the best precision available (~0.42). The error was
never the number; it was using one number for two incompatible jobs. So the map now reports
tiers, as the Fabry assay it keeps citing also does rather than a binary call:

```
  tier call       |score| >= 0.2     52 variants   held-out spec 0.985, precision ~0.42
  tier candidate  0.03 to 0.2       164 variants   precision ~0.18, about 4 wrong per
                                                   right -- by design, and labelled
  below 0.03                                       not called, and with sensitivity 0.68
                                                   that is a weak statement, not evidence
                                                   of no splice effect
```

The called set goes **52 -> 216**, and the therapeutically interesting count with it:
`HYPOMORPH_protein_made` **12 -> 36**, `NULL_pending_NMD` **40 -> 180**. Three times as
many candidate hypomorphs — variants predicted to leave protein behind to rescue — which is
the quantity the whole Track 2 thesis is about.

**C39b — two independent label sources agree the screening tier is mostly false positives.**
Re-running the ClinVar test at each tier:

```
  at 0.2    14 of 15 pathogenic called,   4 of 790 benign
  at 0.03   14 of 14 pathogenic called, 139 of 790 benign
```

ClinVar precision on the pathogenic-vs-benign margin at 0.03 is **0.092**; MFASS corrected
precision at the same cut is **0.180**. These differ by about twofold and should not be
reported as equal — ClinVar's benign set is enriched for common variants, a different
population. What they agree on is the conclusion: **the screening tier is majority false
positive**, from a clinical-assertion source and an assay source independently. Lowering
the cut also recovered the one pathogenic variant the map had missed, so ClinVar sensitivity
is now 14/14.

**C39c — and the Fisher p got WEAKER, which is the most useful thing it has ever done.**
It fell from 3.9e-24 to **4.958e-11**. Nothing broke: the test rewards separation, and we
deliberately traded separation for sensitivity. A summary statistic that moves in the
opposite direction to a deliberate, measured improvement is the wrong summary, and this is
the cleanest demonstration of C29a's point that the p-value was never the claim. The
pre-stated sensitivity and specificity, with precision corrected to the true prevalence,
are.

**Still interim.** These thresholds come from 1,025 of 4,946 scored (22%). They are
re-derived when scoring completes, and the committed values may move. The framework — derive
on one split, report on the other, correct precision to the true prevalence — does not.

---

## C40 — The benchmark is complete. The threshold is settled on a sealed split, the region split does NOT help, and C39's central claim was wrong.

All 4,946 benchmark variants scored. The same-instrument gate passes on the full set:
local Pangolin returns `+0.49/-0.73`, `+0.85/-0.69`, `+0.76/-0.71`, `+0.73/-0.89` for the
four committed reference variants, so this benchmark measures the map's own instrument.
4,946 of 4,946 returned a score; none skipped.

**The old threshold, judged against the pre-stated criteria.** At `CALL = 0.2`:

```
                 called   not called
  measured SDV      338          608
  measured not       55         3945

  sensitivity 0.357 (0.327-0.388)  FAIL   (pass >= 0.70, fail < 0.50)
  specificity 0.986 (0.982-0.989)  PASS
  ROC AUC     0.876
  precision, corrected to the true prevalence: 0.462 at 3.2%, 0.507 at 3.8%
```

C38's interim read holds exactly: a decisive sensitivity failure, specificity passing
easily, the fault in the operating point rather than the method.

**C40a — but C39's central claim was wrong.** C39 stated the pre-stated 0.70 sensitivity
bar *"is not reachable: the best held-out value is 0.683, CI 0.588-0.764"*. That was an
inference from 22% of the data and it does not survive. At the derived screening threshold
of **0.02**, sensitivity is **0.725** on validate and **0.793** on the sealed split — the
bar is cleared on both. The flattering direction turned out to be the true one this time,
which is not a reason to have believed it earlier.

**C40b — the interim thresholds were genuinely unstable, and the overfit gap proves it.**
At n=1,334 the derive-to-held-out sensitivity gap was **+0.142**. At n=4,946 it is
**+0.013 to +0.020**. So the interim numbers were noise around a real signal, and the
convergence log (`threshold_trajectory.log`) shows `CALL_HIGH` wandering 0.10 -> 0.19 ->
0.13 -> 0.16 before settling and Youden fixed at 0.02 from early on.

**The settled thresholds**, derived on 50% and reported on the sealed 25% that informed no
choice, opened once and recorded in `seal_openings.log`:

| tier | threshold | sealed sensitivity | sealed specificity | precision at 3.2% | wrong per right |
|---|---|---|---|---|---|
| `call` | **0.16** | 0.392 | 0.986 | 0.481 | 1.1 |
| `candidate` | **0.02** | 0.793 | 0.872 | 0.170 | 4.9 |

0.16 and 0.20 are statistically indistinguishable; the derivation prefers 0.16 as the most
sensitive cut still clearing specificity 0.98, so that is what ships.

**C40c — the region split does NOT help, and the reason is the interesting part.** The two
regions differ sharply in difficulty. At threshold 0.2:

```
  intronic  n=2414   sensitivity 0.471   specificity 0.981
  exonic    n=2532   sensitivity 0.266   specificity 0.992
```

Pangolin is nearly twice as sensitive on intronic variants as on exonic ones, which is
mechanistically unsurprising — it models splice sites, and an exonic variant usually acts
through a splicing regulatory element instead. The obvious inference is that each region
deserves its own threshold. **Properly powered, that inference is false:**

```
  exonic     region-derived 0.02 vs pooled 0.02   held-out J identical (+0.000)
  intronic   region-derived 0.05 vs pooled 0.02   held-out J WORSE by -0.024
```

The intronic region threshold looked better on the half that chose it and was worse on the
half that did not. That is overfitting, caught by the split rather than by judgement, and
it is the clearest vindication of building the derive/validate separation before looking.
**The regions differ in how hard they are, not in where the cut belongs.** Pooled ships.

**What the map now calls**, at `CALL_SCREEN = 0.02` with tiers:

```
  tier call       |score| >= 0.16    60
  tier candidate  0.02 to 0.16      227
  total                             287   (was 52 at the old single threshold)

  HYPOMORPH_protein_made             40   (was 12)
  NULL_pending_NMD_of_new_PTC       247   (was 40)
```

**40 candidate hypomorphs** — variants predicted to leave protein behind to rescue — against
12 before the benchmark existed. That is the quantity the Track 2 thesis rests on, and it
more than tripled because a threshold was measured instead of assumed.

**The caveat still travels.** MFASS is a minigene reporter: it measures exon recognition in
a construct, not endogenous splicing at the native locus. The sensitivity figures are the
ones that caveat bears on hardest, and it was written into `mfass_score.py` before any
result existed, so it is not available to be dropped now that the numbers are favourable.

---

## C41 — The two-class mechanism, tested on measured abundance: the charge axis survives, the volume axis does not, and allele 2 is both.

C15/C19's two-class finding is what licenses every statement we make about allele 2:
stability prediction separates pathogenic from benign at AUC 0.952 inside the folded core
and 0.364 across the interfaces, and `p.Asn1002Lys` sits at RSA 14%, inside the folding
class. That AUC rests on **5 pathogenic variants against 25 benign**. It carries a
burial-matched permutation null, which is more than most small results get, but the
mechanism it asserts had never been tested where the answer was measured.

`burial_dependence_test.py` tests it on measured **steady-state protein abundance** — the
quantity our thesis is about, not function and not fitness — in proteins that are not
BUB1B, with pass and fail fixed before looking.

**BUB1B itself has no such data, and that is now enumerated rather than assumed.** MaveDB's
**2,898** target genes contain no BUB1B, no BubR1, no BUB1, and nothing else in the spindle
checkpoint — no MAD2L1, MAD1L1, CENP\*, CDC20, AURK\*, PLK1. So allele 2 cannot be scored
against measured data, and there is no near homolog to borrow from. A predicted map is not
a shortcut here; it is the only instrument available, and that is a finding for the report.

**The result, on 4,907 buried and 2,211 exposed measured variants across three assays:**

```
                            rho buried   rho exposed    diff [95% CI]
  PTEN VAMP-seq
    |delta volume|            -0.102       -0.064     +0.037 [-0.037,+0.110]  FAIL
    buried charge introduced  -0.210       +0.037     +0.171 [+0.095,+0.233]  PASS
  TPMT VAMP-seq
    |delta volume|            -0.123       -0.123     -0.000 [-0.087,+0.090]  FAIL
    buried charge introduced  -0.209       -0.003     +0.179 [+0.108,+0.236]  PASS
  NUDT15 stability
    |delta volume|            -0.006       -0.198     -0.176 [-0.267,-0.083]  FAIL
    buried charge introduced  -0.140       +0.031     +0.096 [+0.006,+0.167]  INCONCLUSIVE

  |delta volume|             0 pass / 3 fail  ->  FAIL
  buried charge introduced   2 pass / 0 fail  ->  PASS
```

**Burying a charge costs abundance; doing it at the surface costs nothing** — replicated in
three independent proteins and assays, the exposed correlation sitting at zero each time.
That is exactly the mechanism the two-class finding asserts, and it now stands on measured
data rather than on five labels.

**C41a — the volume axis does not survive, and in NUDT15 it reverses.** `|delta volume|`
shows no burial dependence in PTEN or TPMT, and in NUDT15 it tracks abundance *more* at
exposed positions than buried ones, by -0.176 with a CI excluding zero. C27 named volume
and buried charge as "the two that succeed" where burial alone does not. On measured
abundance, one of those two fails.

**C41b — and allele 2 is both of them, which makes this decision-relevant rather than
academic.** `N1002K` is Asn -> Lys at RSA 14%:

- **a buried charge introduction** (Asn uncharged, Lys positive) — the axis that passed;
- **a volume increase** of +54.5 A^3 (114.1 -> 168.6) — the axis that failed.

So the measured data **supports the charge half of our allele-2 argument and withdraws
support from the volume half**. Every statement about N1002K's abundance should now rest on
buried-charge introduction, and any part of the argument leaning on packing volume has lost
its external support and must say so.

**What this does NOT do**, stated here because the temptation is obvious: it does not
transfer AUC 0.952 to BUB1B. Three assays, five proteins attempted, none a pseudokinase and
none in the spindle checkpoint. It supports the **mechanism**; the BUB1B-specific number
remains a five-positive result and must keep saying so.

**C41c — two assays were correctly refused, and the reason is worth keeping.** CYP2C9 and
CYP2C19 abundance returned only **8%** and **4%** reference-consistency against their
AlphaFold models — an isoform or numbering mismatch — leaving 5 and 4 buried variants. Both
were skipped by the `MIN_N = 30` floor rather than reported. Without the
reference-consistency check a naive run would have silently correlated scores against the
wrong residues and produced two more numbers that looked like evidence.

**C41d — and the first run of this test failed completely while looking orderly.** It
hardcoded AlphaFold's `-model_v4.pdb`; AlphaFold is on **v6**, so every fetch 404'd and
every assay printed `skipped, not assumed`. A total failure wearing the costume of careful
missing-data handling — the defensive error message is what hid it. The model URL is now
resolved through the AlphaFold API, which also returns the AlphaMissense annotation path.

---

## C42 — What N1002K actually breaks: not charge repulsion, but a buried hydrogen-bond acceptor. And a better experiment than the one we specified.

C41 narrowed the allele-2 mechanism to one axis — burying a new charge — and stopped
there. "Buries a charge" is a category, and a category cannot be falsified in a lab.
`n1002k_mechanism.py` asks which specific interaction a lysine at 1002 breaks, from the
model's own atoms.

**It is NOT a like-charge repulsion variant, and that was the expected answer.** Within
8 Å of the N1002 side chain there is exactly **one** charged group — Arg999, at 6.95 Å,
carrying +0.33 of a guanidinium's formal charge. The signed burden for a +1 at 1002 is
**+0.047 e/Å**, which is negligible. There are **zero** negative charges in the shell, so
a buried lysine would also have no counter-charge to pair with. The mechanism is
desolvation of an unpaired buried charge, not repulsion.

**What it does break is specific and chemical.** N1002's amide makes three hydrogen bonds:

```
  N1002:OD1  <-- TRP978:N    2.83 Å   (acceptor; Trp978 backbone amide donates to it)
  N1002:ND2  --> VAL998:O    2.83 Å
  N1002:ND2  --> TRP978:O    2.95 Å
```

Asn carries **both** a donor (ND2) and an acceptor (OD1). Lysine's NZ **donates only**. So
the two ND2 donations could in principle be satisfied by a lysine, and the
**OD1 ← Trp978:N contact cannot be** — a backbone amide left without its acceptor, buried
at RSA 13.7%.

**C42a — this is NOT the withdrawn W978 claim returning, and the distinction is the
point.** VUS-NOMINATION.md withdrew the argument that *"W978L is an independent prediction
because W978 packs against N1002"*, because the contact shell as a module carries no
predictive weight: 5 of its 10 residues sit above their burial-matched median and 5 below,
exactly chance. That claim ran from N1002 outward, to say something about W978. This one
runs inward, to say what N1002 loses, and names a single backbone hydrogen bond rather
than a packing neighbourhood. The shell's statistical emptiness does not bear on it.
(Internal check: this script's Shrake-Rupley gives W978 RSA 11.3%, reproducing
`w978_shell.py` exactly, and N1002 13.7% against the map's 14.0% at a different probe
density.)

**C42b — the mechanism was then tested against all 19 substitutions at 1002, and the
result is mixed.** Groups were defined from the structural mechanism *before* the scores
were read. AlphaMissense, which knows nothing of this reasoning:

| group (defined from mechanism) | n | mean | 
|---|---|---|
| donor only, buries positive (K, R) | 2 | **0.904** |
| no polar side chain | 9 | 0.885 |
| acceptor, buries negative (D, E) | 2 | 0.841 |
| **acceptor, neutral** (Q, N→S, T, Y, C, H) | 6 | **0.685** |

The ordering is exactly what the mechanism predicts, and the cleanest case is the extreme:
**N1002S scores 0.348 and is the only substitution at this position AlphaMissense does not
call likely-pathogenic** — serine keeps a small neutral acceptor and nothing else.

**Three things that cut against it, which the ordering must not be allowed to hide:**

1. **18 of 19 substitutions are likely-pathogenic.** The position is intolerant to almost
   everything, so the mechanism explains gradation *within* an intolerant site, not the
   intolerance itself.
2. **The three worst are Trp, Phe and Pro** — bulk and backbone, i.e. **sterics**. The
   dominant signal at 1002 is packing, and packing is precisely the axis that FAILED
   external validation in C41. That is awkward and it is reported rather than smoothed.
3. **N1002Q scores 0.907**, barely below K's 0.923, while keeping both donor and acceptor.
   So preserving an acceptor is not sufficient for tolerance, and the clean story is not
   clean.

And a limit that applies to the whole test: **AlphaMissense predicts pathogenicity, not
abundance.** C41 established abundance as the quantity this thesis is about. Agreement here
is not validation of the abundance claim.

**C42c — the deliverable is a better experiment than the one the report specifies.** The
report's settling experiment compares ectopic LAP-BubR1 N1002K against wild-type with
**Q921H** — a different residue — as the tolerated control. The substitution series supplies
a far stronger control at the **same position**:

> **N1002K vs N1002S vs wild-type.** Serine is the mechanism's own predicted-tolerated
> substitution at this exact residue, independently ranked most tolerant of 19 by
> AlphaMissense. If K is low and S is normal, the mechanism is confirmed and abundance is
> the right axis. If both are low, position 1002 is intolerant for reasons this mechanism
> does not capture, and the abundance framing is wrong.

A same-residue control removes the confound a different-residue control cannot: it holds
position, burial and neighbourhood fixed and varies only the chemistry the mechanism names.
That is the sharpest falsifiable test this workstream has produced, and it is cheap.

---

## C43 — The missense arm is now calibrated, and BOTH pre-stated tests FAILED. The allele-2 argument is weaker than the report claims.

`missense_arm.py` calibrates the half of the map the proband's allele 2 lives in — 1,494
missense variants that had never been calibrated at all while the splice arm was taken to
a sealed evaluation. Both tests had their criteria fixed in the file before any result
existed, and the file stated in advance that a FAIL was the outcome worth recording.

Both failed.

**TEST A — does C41's validated axis transfer to BUB1B's own labels? FAIL.**

```
                buried charge   not
  P/LP                      2    17        rate 10.5%
  B/LB                      2    98        rate  2.0%

  Fisher exact one-sided: OR = 5.76   p = 0.1193     FAIL (criterion p < 0.05)
```

The **direction is right and the effect is large** — a fivefold odds ratio — and it still
fails, because there are 19 pathogenic/likely-pathogenic missense variants in the whole
gene. That is not sampling bad luck: *BUB1B*'s pathogenic alleles are **55 of 69
truncating**, so the missense margin is small by the gene's own biology. The honest
statement is therefore not "the axis is wrong here" but **"the axis is not demonstrated
here"**, and the consequence is the same either way: every claim about N1002K's abundance
rests on **cross-protein transfer from PTEN, TPMT and NUDT15 alone.** The report must say
that, and now does.

**TEST B — is AlphaMissense usable on this protein? FAIL, and this one is worse.**

```
  measured 5-10x REDUCED        measured NORMAL
    I909T    0.4506               R550Q   0.0657
    R814H    0.2205               Q921H   0.4913
    L1012P   0.8720
    L844F    0.2917
    R727C    0.2381

  destabilising variants scoring above BOTH normals: 1 of 5   FAIL
```

**Q921H, measured normal, outscores four of the five measured-destabilising variants.**
R814H is measured at 5–10× reduced BubR1 and AlphaMissense gives it 0.22. So on this
protein's own measured panel the predictor points the wrong way four times out of five.

**C43a — and that lands directly on allele 2.** N1002K's AlphaMissense score is **0.9229**,
which reads as strong support and has been quietly doing work in our thinking. It comes
from a predictor that just failed its direction check on this very protein. **0.9229 is not
evidence and may not be cited as such.** C42b's substitution-series result is unaffected —
that test used AlphaMissense only for *relative ordering within one position*, which is a
weaker and different claim than ranking variants across the protein.

**C43b — the verdict hinges entirely on Q921H, and it still ships as a FAIL.** Drop Q921H
and the threshold becomes R550Q's 0.0657, where **all five** destabilising variants clear
it: 1/5 becomes 5/5. Q921H's "normal" label is already flagged in this ledger — it sat on
the same allele as L844F, the authors attributed causality to L844F, and it was never
tested as the only variant on an allele. So there is a real argument for excluding it.

It is not taken, and the reason is this ledger's own rule, written about this very variant:
*"The weaker figure is the one that ships, because discarding the one inconvenient data
point is not how a headline number should be obtained."* FAIL ships; the sensitivity is
reported beside it so a reader can see exactly how much rests on one variant.

**What the arm actually delivers.** The validated axis applies to **50 of 1,494** missense
variants — 3.3%. Every other row records *why* it does not apply rather than borrowing a
number from the volume axis that failed in C41a:

```
  AXIS_NA_no_new_charge                 1256
  AXIS_NA_not_buried                     188
  ABUNDANCE_RISK_buried_new_charge        50   <- includes N1002K, RSA 13.7%
```

A missense arm that returned an answer for all 1,494 would be the thing to distrust. This
one answers for 50 and says so.

**Net effect on the submission.** Allele 2's abundance case now rests on: a buried-charge
mechanism validated in three other proteins but **not** demonstrated in this one; a
specific lost hydrogen bond (C42) that is a hypothesis about a predicted structure; and a
pathogenicity predictor that is **not reliable on this protein**. That is a weaker case
than the report currently makes, and the fix is to say so rather than to find a fourth
argument. The experiment in C42c — N1002K vs N1002S vs wild-type — is now the only thing
that can settle it, which raises its value rather than lowering it.

---

## C44 — I said the Fabry map was "assay-determined over 1,386 variants." Wrong number.

**21 Oct 2026.** When I argued that our eligibility map had a precedent, I described the
Fabry one as "assay-determined over 1,386 variants." I did not source that figure, and it
does not survive checking. The real numbers, both verifiable:

- **600** Fabry-causing mutations were expressed in HEK-293 cells and **268** were found
  amenable — Benjamin ER et al., *Genet Med* 2017;19(4):430-438,
  [doi:10.1038/gim.2016.122](https://doi.org/10.1038/gim.2016.122).
- The **current** label's Table 2 lists **376** distinct amenable DNA-change entries,
  counted by `scripts/mva/fabry_precedent.py` off the prescribing information
  (sha256 `ca9b696f…`, retrieved 21 Oct 2026). The growth from 268 to 376 is the table
  being maintained as new variants are tested, which is a point in the precedent's favour
  and one I would have missed by keeping the invented number.

Where 1,386 came from, I cannot say — which is the whole problem with it. It is not in
the paper and not in the label. It was a number I produced while making a comparison I
believed, and belief is exactly when a number needs a source most.

**What it changes in the argument: nothing, and that is worth stating.** The precedent's
force never came from its size. It comes from three things that the label itself says,
all of which checked out and are now measured rather than asserted:

1. The **indication is a genotype gate.** Not "Fabry disease" but Fabry disease *and an
   amenable GLA variant based on in vitro assay data.*
2. **Every eligible allele makes protein.** Of 376 entries, 357 are plain missense, 4 are
   multi-variant missense alleles and 3 are small in-frame indels. The raw table contains
   no `Ter`, no `fs`, no `*`, no `splice` — `fabry_precedent.py` asserts this on the raw
   text and fails if it ever stops being true, because the finding rests on it.
3. **The drug does nothing in the ineligible.** Of 67 patients in Study 1, the 17 with
   non-amenable variants "had no change from baseline" at six months.

So the correction makes the comparison stronger, not weaker: a smaller table, more
precisely described, that says what we wanted it to say for a reason we can now point at.

**What the correction does NOT buy us.** Parity. The Fabry table is a GLP-validated
HEK-293 assay with a published criterion (≥20% relative and ≥3% of wild-type activity at
10 µM) and sensitivity, specificity and predictive values all ≥0.875 against in vivo
response. Ours is predicted. Every row of `allele_lookup.tsv` says so and carries the
experiment that would settle it. Any sentence of ours that implies otherwise is the error
this ledger exists to catch.

---

## C45 — I ranked a splice-modulating ASO above the NAD⁺ route on a count that proves nothing.

**21 Oct 2026.** In `PATIENT-LED-PRECEDENTS.md` I wrote that the splice-modulating ASO
route "moves ahead of the NAD⁺ route on fit," on the strength of this observation:

> And *BUB1B* has the substrate. Of its **31 annotated transcripts, 12 carry the
> `nonsense_mediated_decay` biotype**.

That is a true count and a worthless argument. A count of decay-biotype transcripts cannot
fail — transcripts acquire that biotype for many reasons, nearly none of which an ASO can
block. I had flagged "annotation is not flux" as the caveat, which was the wrong caveat:
the problem was not that the magnitude was unmeasured, it was that **the thing being
counted was not the thing that matters.**

The thing that matters is whether a specific, recurrent, **frame-disrupting**,
decay-exclusive cassette exon exists — the shape of SCN1A's exon 20N. Testing for that
(`splice_architecture.py`, with SCN1A as a positive control the method had to pass):

- **SCN1A:** one decay-exclusive cassette, **64 bp, frameshifting** — recovers the target
  of a Phase 3 drug from annotation alone, with no hint of where to look.
- **BUB1B:** one decay-exclusive cassette, **54 bp, divisible by 3, entering in frame +0,
  containing no stop codon.** It would insert 18 residues and leave the protein
  full-length. It cannot be a poison exon.

So *BUB1B* has **more** non-productive annotation than *SCN1A* (39% vs 20% of transcripts)
and **less** targetable structure (zero frameshifting cassettes vs one). The ranking is
reversed: the ASO route drops below the NAD⁺ precursor route.

**The near miss worth recording.** Before the terminal-exon filter, the top "recurrently
skipped exon" in *BUB1B* was **exon 1, absent from 9 of 10 decay isoforms** — which is four
different 5′ boundaries for the same first exon, i.e. annotation disagreement about where
transcription starts. Reported without that filter it would have looked like a dominant,
highly recurrent splicing defect. It is nothing. The filter exists because the unfiltered
version produced a spectacular false positive on the first run.

**What I should have done, and what the rule now is.** The previous entry's caveat named
the wrong risk. A structural claim needs a test whose *negative* is informative, and the
cheapest way to get one is a positive control the method must pass — here, a gene whose
answer is already known and already drugged. Any future claim of the form "gene X has
targetable feature Y" in this repo ships with the control that would have exposed it.

The error cost a day of ranking, not a conclusion: the therapeutic argument never depended
on the ASO route, and `DRUG-CANDIDATES.md` is updated rather than rewritten.

---

## C46 — I called a 56%-sensitive detector a general instrument.

**21 Oct 2026.** Presenting the splice work, I wrote:

> `splice_architecture.py` answers "does this gene have a zorevunersen-shaped target?"
> **for any gene**, carries its own control, and fails loudly when the control fails. For
> the submission that's arguably worth more than the candidate was.

The user asked me to check that claim. It does not survive.

Run blind over a panel fixed in advance — SR-protein genes and TRA2B as known positives,
housekeeping genes as negatives — the detector scores **sensitivity 5/9 (56%)** and
**specificity 1/2 (50%)**. It misses SRSF1, SRSF3, SRSF6 and TRA2B, and fires on ACTB.

"Carries its own control" was the part that misled me. One positive control constrains
almost nothing: a detector that fires on SCN1A and nothing else passes it identically. A
control licenses a negative only in proportion to the method's measured sensitivity, and
I never measured it.

**The flaw is specific.** The >70%-of-canonical-length filter on decay isoforms — which I
added to suppress a false positive on *BUB1B*'s first exon, and described approvingly in
the file — discards the short isoforms that carry SR-protein poison exons. Removing it
lifts sensitivity to 7/9 **and flips *BUB1B*'s own call to positive**, because *BUB1B*'s
124 bp cassette frameshifts and survives only the relaxed filter. So the instrument's
verdict on the gene we care about was a parameter choice, not a measurement. I reported it
as a finding.

**Why the conclusion still holds.** GTEx junction reads settle it without annotation:
*BUB1B*'s non-canonical share is **0.00% median** (max 0.17%) against SCN1A's **4.55%**,
and both *BUB1B* candidates measure at essentially zero — the 54 bp at **0.000%** PSI, the
124 bp at **0.371%** — while SCN1A's exon 20N runs at **44.2%** pooled across brain. The
relaxed filter's "positive" is measured at a third of a percent. The answer was right; the
instrument I credited for it was not what carried it.

**The rule this adds.** A detector is not reportable as a general instrument on one
positive control. It ships with a blind panel of known positives and negatives and its
measured sensitivity and specificity in the file, or it is described as what it is: a
cheap screen whose output needs confirming. `splice_architecture.py` now carries those
numbers at the top.

**What the screen was actually good for**, stated so the lesson isn't over-learned: it cost
minutes and named the two exact coordinates the RNA-seq then settled. A cheap screen that
narrows a measurement is worth running. It is just not worth believing.

## C47 — The HSP70 rescue precedent was uncited, and licenses less than the report claimed. CITED AND NARROWED.

Found 23 Oct 2026 by `check_grounding.py` on its first real run, against
`TRACK2-REPORT.md`. The claim, at §3.3:

> "HSP70-inducing treatment restored function to **17 of 18 (94%)** missense CBS mutants
> and 19 of 25 (76%) mutant p53 proteins."

It carried **no citation**, and the same 94% appeared again as 4-PBA's "magnitude
precedent" in the §3.4 verdict table, also uncited. Two things were wrong, in opposite
directions.

**The number is exactly right.** It is Singh et al. 2010, PLoS Genet
([PMID 20066033](https://doi.org/10.1371/journal.pgen.1000807)), verbatim from the
abstract: activity restored to "17 of 18 (94%) disease causing missense mutations in
human cystathionine beta-synthase", with the same treatments also rescuing mutant p53
and MTHFR. Both citations are now in place, together with Singh et al. 2007
([PMID 17540596](https://doi.org/10.1016/j.ymgme.2007.04.011)) for the chemical-chaperone
arm.

**The inference was wider than the source.** The three treatments that achieved the 94%
were **ethanol, proteasome inhibitors, or deletion of the *Hsp26* small heat-shock
gene**, and the paper states that Hsp70 induction is **"necessary but not sufficient"**
for rescue. Not one of the three is pharmacological HSF1 co-induction: two are not
givable to a child and the third is a yeast gene deletion. We transferred that magnitude
to **arimoclomol**, an HSF1 co-inducer, without the insufficiency clause.

**What survives, stated precisely.** The 94% establishes that *this mutation class is
rescuable by shifting the chaperone environment* — which is the load-bearing claim for
the whole fold-then-protect axis, and it stands. It does **not** establish that raising
Hsp70 alone achieves it. The arimoclomol lead keeps its mechanism and loses the borrowed
magnitude.

**One incidental finding worth keeping.** Singh 2007 reports that the rescuable CBS
mutants were those predicted to cause a *decrease* in solvent-accessible surface area.
Our allele 2 is a buried substitution at a position with 7.5% SASA. Whether that places
it inside or outside the rescuable class is now a stated, testable question rather than
an assumption in either direction.

**The rule this adds.** A number can be correct, verbatim, and still support a
conclusion its source does not license. Checking that a citation *exists* is not
checking that it *establishes the claim*. `review-provenance`'s brief now says so
explicitly, and it is the most common finding shape this room produces.

## C48 — The "waveform" constraint and the pure-dosage target were both overstated. NARROWED, from primary sources I had not read.

Found 23 Oct 2026 while triaging seven externally generated reports. The reports themselves were run **without the proband's genotype** (several say so) and filled the gap with the wrong variants, so none of their rankings is usable. But two of their citations are real, load-bearing, and point at claims of **mine**.

### 48a — "BubR1 must be destroyed at anaphase" is not what the proteomics shows

I have asserted throughout this workstream that BubR1 is a *waveform* which "must be destroyed at anaphase", and built from it the rule that an intervention must "raise the peak without filling the trough."

According to PubMed, Holder, Mohammed & Barr 2020, eLife
([PMID 32869743](https://doi.org/10.7554/eLife.59885)) measured proteolysis through mitotic exit and found **cyclin B1 and securin** to be the rapidly destroyed species. BubR1 is **not** among the proteins meeting their criterion for APC/C-mediated anaphase destruction, and BubR1 (with MAD2) remained **stable for at least two hours** while cyclin B1 fell.

**What is wrong, and what survives.** Wrong: the claim that BubR1's bulk protein is rapidly cleared at anaphase. What actually must happen at anaphase is **checkpoint silencing** — loss of kinetochore BubR1 and of MCC-mediated APC/C inhibition — which is a localisation and activity transition, not bulk proteolysis. Conflating the two was my error and it made the therapeutic constraint sound tighter and more exotic than it is.

What survives, and is unaffected: `ASSAY-DESIGN.md`'s finding that **bulk BubR1 abundance tracks cell-cycle composition** so strongly that it swamps pharmacology. That is a measurement confound about cycling-cell fraction, and it does not depend on anaphase proteolysis at all. The phase-matched readout requirement therefore stands on its own evidence.

### 48b — "Raise total abundance" may be the wrong target variable

`bub1b-dosage-review/` and the Track 2 report treat total BubR1 as the quantity to move. Sieben et al. 2019, J Clin Invest ([PMID 31738183](https://doi.org/10.1172/JCI126863)) — the van Deursen lab, who built the hypomorph — modelled the human **L1012P** allele in mouse as **L1002P** and concluded, in the abstract: *"BUBR1 allelic effects **beyond protein level and aneuploidy** contribute to disease heterogeneity in both MVA patients and heterozygous carriers."*

Three specifics that bear on us:
- `BubR1^H/L1002P` mice had **a reduction in total BUBR1 similar to `BubR1^H/H`** yet several progeroid pathologies were **attenuated**. Equal abundance, different phenotype.
- `BubR1^X753/L1002P` — truncation paired with kinase-domain missense, **this proband's allelic architecture** — **died prematurely**. The proband is alive, which is itself information about residual function and about how far the mouse transfers.
- The L1002P reduction is proteasomal with **transcript stability preserved**, which agrees with our folding/turnover account of allele 2.

**What this changes.** The dosage thesis is not refuted — Suijkerbuijk's overexpression rescue of I909T/L1012P stands, and remains the strongest evidence that abundance is sufficient for *those* alleles. But "total protein" is no longer safe as the sole target variable or the sole endpoint, and a report that ranks interventions purely by predicted abundance gain is measuring something the disease model says is incomplete. The honest endpoint pairs abundance with **kinetochore localisation and segregation fidelity**, which is what `ASSAY-DESIGN.md` already specifies and what the Track 2 report's §3.6 experiment does not.

### The rule this adds

Both of these were available in primary literature the whole time, and both were found by reading citations inside third-party output whose own conclusions were unusable. A report can be wrong about the patient and still point at a paper that corrects you. The lesson is not to trust such reports; it is that **our own central framing had never been checked against the proteomics of the thing we were framing.**

## C49 — The claim that would have lifted the SIRT2 demotion is untraceable; and "carrier level is validated" was my overstatement. ONE HELD, ONE CORRECTED.

From a large synthesis report triaged 23 Oct 2026. Two items were decision-relevant.

### 49a — The K250 mitigation does not check out, so the demotion stands

The report asserts that our reason for demoting the NAD⁺/SIRT2 arm is neutralised:

> "The concern that SIRT2 activation might also deacetylate the protective K250 site is
> mitigated by evidence that **HDAC2 and HDAC3, not SIRT2, are the primary deacetylases for
> K250** during mitotic exit, with their recruitment dependent on BRCA2
> [citing `park2017hdac23bindingand`]."

If true this would be important: the K250 hazard is exactly what §3.3's table cites to demote
SIRT2 activation. **I could not trace it.** Four PubMed formulations returned nothing, and the
*only* indexed paper matching `BubR1 HDAC3 deacetylation` is a different study —
Li et al. 2017, *Development* ([PMID 28935703](https://doi.org/10.1242/dev.153353)) — which
is about **α-tubulin**, not BubR1 K250, and which points the opposite way: HDAC3 knockdown
*dramatically increased* kinetochore BubR1 and blocked mouse oocytes at metaphase I with
impaired kinetochore–microtubule attachments.

**Stated precisely:** absence from my searches is not proof the paper does not exist; it may
be indexed under terms I did not hit. But an untraceable citation **cannot lift a verdict**
under rule 10 and the standing rule on third-party output. **The SIRT2 demotion is retained**,
and the K250 hazard remains on the ledger as stated. Anyone who later finds the Park paper
should reopen this entry rather than assume it was dismissed.

Two independent lines now also say HDAC3 inhibition would be the *wrong* direction here,
which matters because the report proposes exactly that to preserve K250: Li 2017's essential
mitotic role for HDAC3, and the DepMap bundle finding low-`BUB1B` models **more**
HDAC3-dependent (`TRIAGE-EDISON-BUNDLES.md`).

### 49b — "Carrier level is validated in humans" was too strong

`RECOMMENDATION.md` carried: *"The target level is validated in humans. Carrier level is
where ~610 gnomAD heterozygous LoF carriers live, with no severe early phenotype."* I have
repeated the shorter form — "50% is demonstrably safe" — many times in this workstream.

The report is right that this is an oversimplification, and the evidence against it is a paper
**we already cite**: heterozygous *Bub1b* truncating mice show mild aneuploidy, reduced
lifespan and increased carcinogen-induced tumour growth (Wijshake 2012,
[10.1371/journal.pgen.1003138](https://doi.org/10.1371/journal.pgen.1003138)); and parents of
affected children have been reported with mild mitotic abnormalities. Sieben 2019 (C48) adds
that monoallelic carriers were "prone to select MVA-related pathologies later in life."

**The defensible claim** is narrower and now stated at the point of use: carrier level is a
*ceiling observed in humans without a severe early phenotype*, in a database ascertained for
neither late nor mild phenotypes. It is not a safety validation. This weakens the "50% is
safe, so aim there" framing without changing the target, because 50% remains the arithmetic
ceiling of one functional allele regardless of how safe it is.

### Recorded as corroboration, not as new findings

- **Independent convergence on the N1002K mechanism.** The report derives that the
  substitution removes the asparagine OD1 acting as a **buried hydrogen-bond acceptor for the
  Trp978 backbone NH**. That is the same contact our own **C42** derived independently:
  `N1002:OD1 ← TRP978:N, 2.83 Å`. Two separate structural analyses, same chemistry, same
  partner residue. The strongest external agreement this project has received.
- **Residue 1002 is >18 Å from the CENP-E binding segment (1031–1050)** and from catalytic
  motifs, which supports "destabilising rather than function-disrupting" for this allele.
- **Pseudokinase ATP pocket druggability scored 0.006–0.071** in a pilot virtual screen, and
  a 20-compound shortlist yielded no validated tool compounds with public bioactivity.
  Consistent with our 0-of-757 fragment null and the failed pocket-scan control.

### New leads worth keeping, none actionable in the remaining time

- **DNAJC7 → UBE4A.** DNAJC7 (a confirmed BubR1 BioID proximity partner) directly binds the
  E3/E4 ligase **UBE4A** (Hatakeyama 2004), giving a specific candidate degradation route and
  a knockout test. Note the tension to resolve first: the DepMap bundle found DNAJC7 and
  UBE4A dependencies **negatively** associated, which is not what a shared-complex model
  predicts.
- **RNF5 / inh-2 in CFTR-F508del** is the cleanest precedent yet for *pharmacologically*
  inhibiting an E3 to raise an unstable mutant protein: RNF5 knockout raised intestinal
  current ~5× (0.34 → 1.7 µA), and inh-2 reduced mutant ubiquitination and raised current in
  primary cells from four F508del-homozygous donors.
- **Domperidone / ATP7B-H1069Q** — an approved drug raising an unstable mutant protein by
  disrupting HSP70-dependent degradation. Relevant as a template, not as a candidate.

## C50 — I asserted a treatment history the record does not contain, hours after logging the finding that names that exact error. CORRECTED.

The Review Room's `review-record` seat reported this morning (F1) that
`TRACK2-REPORT.md` attributes to the clinical record a fact the record does not hold:
*"The clinical record adds: this child has been **treated for** rhabdomyosarcoma."* The
record contains one oncological fact, **HP:0002859**, the presenting event. No therapy, no
agent, no course, no dates.

**Later the same day I wrote, in `SYSTEMIC-REPURPOSED-WHAT-SURVIVES.md`, that vinorelbine is
"already part of this child's own disease's regimen"** — and used "prior cytotoxic therapy",
"post-cytotoxic marrow reserve", "for a survivor" and "needs post-chemotherapy revaccination"
as established facts across two documents. The user caught it.

**Where it came from.** Vinorelbine with low-dose cyclophosphamide *is* the maintenance arm of
EpSSG RMS 2005. That is a fact about the protocol. Turning it into a fact about this child
requires three unstated steps: that the tumour was treated at all, that the child was
risk-stratified to maintenance (which is for high-risk disease), and that this protocol and
era applied. None is in the record.

**What changes.** The vinorelbine argument itself survives and is unaffected, because it never
depended on the regimen claim: Klotz 2012 says vinorelbine kills independently of mitotic
arrest and kills SAC-compromised cells *better*, so the genotype favours it. What changes is
the **form**: from *"retain what this child is already getting"* to *"if vinorelbine is on the
table, now or at relapse, the genotype argues for it rather than against it."* Conditional,
not asserted. The assumption is now declared once at the head of that file and used
explicitly rather than smuggled.

**Why this entry exists rather than a silent fix.** `PHENOTYPE-GROUNDING.md` already observed
that the corrective document itself reproduced the error class it was written to fix. This is
the third occurrence, by the author of the second. The lesson is not "be careful" — it is that
**clinical-record claims need a mechanical check, the way numbers have one.** Every number in
this corpus must trace to a committed query; no equivalent gate exists for sentences about the
patient, and three recurrences in one day is what that gap costs.

## C52 — N1002 is BURIED, not solvent-exposed. I inverted our own finding on the strength of a Kosmos figure caption.

Raised by the owner 24 Oct 2026: *"are you sure that the second allele is in an exposed
loop?"* No. It is not, and our own primary analysis says so in four places.

**What our work actually established.**

| source | statement |
|---|---|
| `N1002-STRUCTURAL-COUPLING.md:27` | N1002, secondary structure **loop**, **RSA 14.0%** |
| `N1002-STRUCTURAL-COUPLING.md:75` | *"Structurally it is a **buried staple**, not an interface residue."* |
| `N1002-STRUCTURAL-COUPLING.md` verdict | *"N1002 being **87% buried**"*; confidence that N1002K is a **pure dosage (stability) mutant** raised to **~85%** |
| `ALLELE2-FOLDING-DOSSIER.md:57` | *"a site with **only 14.0% solvent accessibility**"* |
| `ATLAS-AUDIT.md:65` | *"**more buried** than the benign median"* |
| **C42** | N1002K breaks a specific **buried** hydrogen bond — `N1002:OD1 <- TRP978:N`, 2.83 Å — leaving a backbone amide without its acceptor at RSA 13.7%. Mechanism is **desolvation of an unpaired buried charge** |

RSA 14% is *buried*. By the ordinary convention (<20–25% buried, >50% exposed) it is not
close to the boundary.

**Where the error came from.** The Kosmos run's Figure 1–2 caption reads *"N1002K resides
in a solvent-exposed loop (14.2%)"*. That is the same number our own Shrake-Rupley
calculation produces — the measurement replicated exactly — but the **label attached to it
is wrong**. I took the label, not the number, and propagated it into
`TRIAGE-KOSMOS-HACKATHON.md` §1, `THE-PICK.md` §1, the deck, and — worst — into
`VIDEO-SCRIPT.md`, where on 24 Oct I "corrected" the script **from** *"buried in that
domain's folded core"*, which was right, **to** *"a solvent-exposed loop"*, which is wrong.
I turned a correct sentence into an incorrect one and logged it as a correction.

**What this changes, and what it does not.**

It **reverses** the claim in `THE-PICK.md` §1 that allele 2 is not a destabilisation
variant and that the abundance-restoration logic therefore does not transfer. Our own
evidence says the opposite: N1002K is ~85% likely a pure dosage mutant, and its two
nearest structural analogues, R814H and **I909T**, are pure destabilisers — I909T being
one of the two Suijkerbuijk mutants where forced overexpression **fully restored
function**. The Suijkerbuijk logic transfers *better* to this allele than I said, not
worse.

It does **not** overturn the Aurora B thesis. The convergence argument runs through
how much functional BubR1 reaches the kinetochore, and a destabilised, scarce BubR1
delivers less PP2A-B56 just as a mislocalised one would. If anything the chain is simpler:
less protein, less KARD, less phosphatase, unopposed Aurora B.

It does **not** reopen the chaperone, SIRT2 or proteasome arms. Those closed on exposure
and on specific hazards (HSP90 strips the fragile pool; K250; micronuclei in survivors),
not on the burial question.

**Standing rule this breaks.** A third-party model's *label* on a number is not a finding,
even when its *number* reproduces ours exactly. The reproduction of 14.0 vs 14.2 made the
caption feel verified; it verified only the measurement. Where an external run and our own
corpus disagree on an interpretation, our corpus wins unless the run shows its work.

## C53 — The truncated allele KEEPS the KARD. We under-examined stabilising it, and the real barrier is different from the one we have been stating.

Raised by the owner 24 Oct 2026: *"the KARD domain is before the truncation, so
technically even the truncated product can be stabilized... did we give up too quickly?"*

**The observation is correct and we had not stated it plainly.** KARD is residues
**667–681**. The proband's stop is at **737**. A translated 1–736 product retains the
entire KARD, including all three regulatory phospho-sites (S670, S676, T680) and the whole
LxxIxE B56-binding motif.

**What the binding data actually say** — Wang *et al.*, *Cell Res / Protein Cell* 2016,
[PMID 27312108](https://doi.org/10.1007/s13238-016-0283-4), the paper that produced
**PDB 5JJA**, the structure already on our slide:

| measurement | value |
|---|---|
| 15-mer KARD peptide (667–681) + B56γ1, **unphosphorylated** | **Kd 2.8 µM** |
| 74-residue BubR1(647–720) + B56γ1 | Kd 2.9 µM — *"almost identical"* |
| effect of **pSer670** | **~11-fold tighter** |
| effect of **pSer676** | **~4-fold tighter** |
| effect of pThr680 | not significant |
| residues that abolish binding when mutated | **L669, I672, E674** — the LxxIxE motif |

Their conclusion: *"the short 15-mer segment of BubR1 is solely responsible for B56
binding."* So B56 binding is **not** gated by the pseudokinase domain, and it is **not**
strictly phosphorylation-dependent. Phosphorylation is an ~11× affinity enhancer on a Kd
that is already micromolar.

**So why does the truncation still fail? Two serial barriers, and only the second is
subtle.**

1. **NMD destroys the transcript.** The stop at 737 is 73 nt upstream of the next junction,
   comfortably past the 55-nt rule. No protein is made to stabilise. Every approved agent
   that might rescue it fails on exposure — amlexanox most of all, closed on its own
   registration data.
2. **If it were rescued, the product would be a poor recruiter, not a non-recruiter.**
   The 731X construct (residues 1–715, which also retains the full KARD) shows reduced
   KARD S670/S676 phosphorylation and weakened PP2A-B56 recruitment at matched kinetochore
   levels, because the pseudokinase domain exerts long-range control over KARD
   phosphorylation. Losing that costs the ~11× that pSer670 buys, against a micromolar
   starting affinity.

**What we got wrong in presentation.** The deck and the mechanism figure implied the
truncation removes the machinery that recruits PP2A-B56. It does not. It removes the
domain that *licenses* that machinery efficiently. The distinction matters because a judge
will spot the residue numbers.

**What is genuinely untested.** Every published truncation is shorter than this child's:
731X is 1–715, the 2010 construct is 1–715 despite its name. **Nobody has characterised
1–736.** It retains 21 more residues than any tested construct, and whether those change
KARD phosphorylation is unknown. That is a real gap, not a closed question, and it should
be stated as one.

**Standing correction.** Allele 1 is closed on **NMD plus exposure**, not on "it lacks the
machinery". Anywhere we have implied the latter, fix it.

---

## C54 — the 1,208x exposure ratio was TOTAL drug on an axis labelled FREE

Found 24 Oct 2026 by two independent external reviews of the deck, run on the
17-slide version. Both reproduced our arithmetic exactly and then separated the
number from its label.

| | |
|---|---|
| source | Dennis et al. 2012, PMID 22864876: barasertib-hQPA steady-state **226.8 ng/mL**, MW 507.57 |
| our figure | 446.8 nM / 0.37 nM = **1,208x**. Arithmetic confirmed by both reviewers |
| the defect | 226.8 ng/mL is **total** plasma concentration. `fig_exposure` labelled its x-axis *"achievable **free** plasma concentration"*, and the arms we CLOSED were scored on free concentration (e.g. "free Cmax @ 98% bound ~0.05 nM"). We applied a stricter standard to the candidates we rejected than to the one we picked |
| second defect | 0.37 nM is a **biochemical** IC50. It is not the concentration required for cellular rescue, so the ratio is not a therapeutic index and not a safety margin |

**Fixed.** The barasertib bar is now a RANGE, 12x to 1,208x: free at 99% protein
binding through to total. Its free fraction is unpublished, and the figure says so.
The axis no longer claims "free". The conclusion survives — at 99% bound the free
Css is still ~12x the biochemical IC50, and it remains the only arm above its
target rather than short of it — but it survives on a stated range, not on a
single flattering number.

## C55 — the "Xu rescue" marker plotted a different compound

`fig_window` carried a vertical anchor labelled "Xu rescue" at 15x on an axis of
*barasertib* free-IC50 multiples. Xu et al. 2013 used **ZM447439**, including 2 µM
in HeLa under an imposed metaphase block, and the patient-cell rescue there came
from BubR1 expression or artificial kinetochore targeting of PP2A-B56, not from a
dose of barasertib. The cross-compound conversion was never justified. The anchor
is removed; the remaining marker is relabelled "adult oncology, TOTAL drug", and
the axis now states that the curves are predicted rather than measured.

## C56 — "a dosage mutant" was stated as fact from burial alone

Slide 4 asserted that p.Asn1002Lys is "made, then degraded: a dosage mutant". 87%
burial predicts that; it does not establish it, which needs abundance, localisation
and function in patient cells. Softened to "PREDICTED", with the gap named on the
slide. Suijkerbuijk 2010's finding that MVA missense alleles near the kinase domain
are turnover mutants remains independent support for the class, not for this allele.

**Not changed, and worth saying:** both reviews independently flagged the J Clin
Invest / PMID 20972334 citation and the "mitotic competence" wording on the
Suijkerbuijk panel. We had already corrected both earlier the same day (C53 and the
13-slide rebuild) before seeing the reviews. One reviewer supplies the DOI,
10.1158/0008-5472.CAN-09-4319, and confirms PMID 20972334 is an unrelated
lung-cancer paper.
