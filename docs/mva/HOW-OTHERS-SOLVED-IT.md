# How other diseases solved "the protein is made and then destroyed"

14 Oct 2026. A deep read of the field around allele 2's lesion class: what arimoclomol
actually is, the two families of solution, the one disease that turned our open question
into a regulatory instrument, the n-of-1 precedents, and the platform answer that
generalises it.

**The single most important framing finding.** Our problem is not unusual — it is the
*most common* way missense variants cause rare disease. *"Reduced protein abundance is
the most frequent mechanism by which rare missense variants cause disease"*, with
large-scale surveys estimating **40–60% of pathogenic variants are explained by loss of
abundance** [1]. And the field has a stated two-step method for it, which is the method
we have been following without knowing it had a name: *"it is necessary to first assign
the molecular mechanism explaining all pathogenic variants, then measure the response to
the"* pharmacological chaperone [1].

---

## 1. What arimoclomol is

A **hydroxamic acid derivative of bimoclomol** and a **heat-shock protein co-inducer**.
Mechanism, in the field's own words: it *"amplifies HSP gene expression"* by
**stabilising the active phosphorylated trimer of heat shock factor 1 (HSF1)**,
increasing HSF1 phosphorylation and so amplifying expression of HSP70 and HSP90 [2].

**The word that matters is "amplifier".** It *"acts as an amplifier of HSP expression in
response to toxic misfolded proteins that aggregate during cellular stress"* [2] — it
does not switch the heat-shock response on in an unstressed cell, it increases the
response to stress that is already there. That is why it matters here specifically:
aneuploid cells are chronically proteostatically stressed and **lose HSF1 and HSP90**
(§3.3 of the report). An amplifier acting on a depleted system is a different
proposition from an amplifier acting on a normal one.

| | |
|---|---|
| Approval | **FDA, 20 Sep 2024, as Miplyffa**, for Niemann–Pick type C, in combination with miglustat [3] |
| Age | children **≥ 2 years** |
| Class | HSP co-inducer targeting HSP70 [3] |
| Crosses BBB | yes — detectable in CSF of treated ALS patients [4] |
| Prior history | phase II/III in SOD1-familial ALS [5]; did not reach approval there |

**Two honest caveats.** In Npc1-null mice arimoclomol reactivated the stress response in
brain and improved locomotor coordination **but gave no rescue in liver** [4] — the
effect is not uniform across tissues. And in a FUS-ALS model, arimoclomol reversed
cognitive deficits **"independent of heat shock protein induction"** [6], which means at
least some of its in vivo activity is not through the mechanism we are invoking. Neither
sinks the rationale; both belong next to it.

---

## 2. Two families of solution on the folding axis — and five other classes, because this
is not the whole option space

**Corrected 14 Oct 2026 (C28a).** This section originally said "everything the field does
for this problem falls into two classes" and concluded that class B is "the only class open
to us". That is true of **one axis — making the existing protein fold better** — and
stating it as the option space was wrong. The other classes are in §2c below; one of them
has been tried in this syndrome, on this gene, and the result is the most important
intervention datum we have (§6).

On the folding axis, the two families are real and the distinction is exactly the one our
fragment screen decided.

### Class A — bind the target and stabilise it directly

A **pharmacological chaperone**: a small molecule that binds the protein, raises its
thermostability, and so raises its steady-state level. Approved examples:

| disease | drug | what it binds |
|---|---|---|
| Fabry | **migalastat** (Galafold, 2016 EU / 2018 US) | the **active site** of α-Gal A — an iminosugar analogue of the substrate's terminal galactose; dissociates at lysosomal pH [7][8] |
| ATTR amyloidosis | **tafamidis** | transthyretin, a kinetic stabiliser [1] |
| Cystic fibrosis | **lumacaftor / tezacaftor / elexacaftor** + a potentiator | CFTR; effective for p.Phe508del and others [1] |
| (experimental) | PCs for **p53** | the most frequently mutated tumour suppressor [1] |

Migalastat's mechanism is worth stating precisely because it is the closest thing to an
existence proof: reversible binding **stabilises the mutant protein, prevents its
degradation in the ER, and allows delivery through the secretory pathway to lysosomes**,
where the drug dissociates and the enzyme works [7].

**Class A is closed for BubR1, and we closed it by measurement.** It requires a binding
site, and 0 of 757 fragments preferred the only non-functional pocket on the one domain
that structure prediction models with confidence (`MILLET-PROTOCOL.md`,
`ALLELE2-ROUTES-REEXAMINED.md`).

### Class B — raise folding capacity in *trans*, never touching the target

A **proteostasis regulator**. Does not bind the target at all; increases the cell's
chaperone capacity so the client folds. 4-PBA and arimoclomol are the two with human
exposure.

**On this axis it is the only class available to us, and it is available *because* the
pocket is shut.** That is the one respect in which our structural negative is load-bearing
in a useful direction rather than merely disappointing: it does not weaken the class-B
argument, it is what selects it. It says nothing about the classes below.

### 2c — The classes the folding axis leaves out

| class | what it does instead | status for *BUB1B* |
|---|---|---|
| **Raise output, not stability** | more transcript or more translation | **Live concept.** The dominant strategy in Friedreich ataxia, and directly supported here: patients with *monoallelic BUB1B* mutations show **decreased transcript and protein** [19], so output tracks disease, not only folding |
| **Bypass the protein** | deliver its function from another scaffold | **Proven in cells.** Phosphomimetic BubR1 **KARD fused to Mis12** (Mis12-KARD3D) recruits PP2A-B56α to kinetochores and *"rescued"* chromosome alignment in BubR1-depleted cells [20]. The KARD is a **15-residue linear motif (667–681)** in the disordered middle, graftable *because* it is not a folded domain — **the function is separable from the protein**. No delivery route to a child's dividing cells, so a concept, not a therapy |
| **Replace the cells** | HSCT, gene therapy, gene editing | **Tried in MVA1. Failed. See §6** |
| **Treat the consequence** | downstream pathology rather than the lesion | Our own Thesis A (IL-1), and tumour-directed therapy — **the only class with in-syndrome successes** (§6) |
| **Partner-mediated stabilisation** | raise a binding partner that stabilises the client | Untested; listed for completeness, not as a lead |

---

## 3. Fabry turned our open question into a regulatory instrument. This is the most useful thing in this document.

Our §3.6 says the abundance-versus-function question is the load-bearing assumption and
that computation cannot settle it. **Fabry has had a formal, regulator-sanctioned answer
to that exact question for a decade, and it is an assay.**

The concept is **"amenability"**. A variant is amenable to chaperone therapy if it
produces *"abnormally folded or less stable proteins with retained enzymatic activity"*
[9] — which is word-for-word our abundance-versus-function distinction. Amenable
variants are *"missense mutations with normal α-Gal A catalytic activity, but ... a
reduction in overall enzymatic activity due to strongly decreased stability"* [10].

**How it is decided — and the numbers are specified:**

- A **GLP-validated in vitro assay**: HEK-293 cells transfected with the specific
  mutation, incubated with 10 μM migalastat [11][12].
- Amenable if the transfected cells show a **≥1.2-fold increase above baseline AND a
  ≥3% absolute increase in wild-type activity** [12].
- **600** mutant forms expressed in HEK-293, **268** amenable (Benjamin 2017, Genet Med
  19:430-438); **376** distinct amenable entries on the current label, counted by
  `fabry_precedent.py`. ("1,386" was unsourced and is retracted — C44.)
- The classification is published in the FDA and EMA product information and in a public
  amenability table [9].

**Three things follow for us, and the third is uncomfortable.**

1. **Our framing is right and has a name.** Abundance-class = amenable. We should use the
   field's term.
2. **The settling experiment has acceptance criteria.** "A western blot" is vague;
   "≥1.2-fold over baseline and ≥3% absolute, in transfected cells ± drug" is a protocol
   with a precedent of regulatory acceptance.
3. **The company that commercialised this strategy built an assay, not a predictor.**
   Amenability is *"evaluated through an in vitro assay"* [9], per variant, hundreds of times.
   That is the field's own verdict on whether computation settles this question, and it
   agrees with §3.6 rather than with any wish to the contrary.

---

## 4. The n-of-1 precedents, and why the famous one does not apply to us

**Milasen** is the landmark: a 22-nucleotide 2′-MOE phosphorothioate ASO designed for
**one six-year-old**, Mila Makovec, with CLN7 Batten disease. Her second allele was an
**SVA retrotransposon insertion** disrupting splicing of MFSD8; seven ASOs were
synthesised and tested in **her own fibroblasts** to target the cryptic splice site, and
the lead went from **diagnosis to dosing in one year** [13][14]. It reduced seizure
frequency and duration with a favourable safety profile [15].

It catalysed the **n-Lorem Foundation**, which systematises personalised ASO development
for "nano-rare" patients [16], and an emerging regulatory framework for N-of-1 to
N-of-few [14].

**Why it is not our route.** Milasen is **splice correction**. Our allele 2 is a missense
change in the final exon with **no predicted splice effect at all** — we measured it:
gain +0.01, loss 0.00, across three window widths, control reproducing exactly
(`SPLICE-ALLELE2.md`). There is no mis-splicing to correct. The modality that saved Mila
has nothing to act on here.

Two adjacent oligonucleotide ideas are worth naming honestly rather than silently
skipping:

- **Transcript lowering** (as Jacifusen/ION363 does for FUS-ALS [16]) is the wrong
  direction — we want more BubR1, not less.
- **Upregulating output from allele 2** would raise the level of a *misfolded* protein.
  If the lesion is purely quantitative that could help; if the protein is
  non-functional it adds nothing. **It is downstream of the same unanswered question**,
  which is the recurring structure of this entire arm.

Mila's case does carry one directly transferable lesson: the decisive experiments were
run **in the patient's own fibroblasts**. That is the tissue our §3.6 experiment wants.

---

## 5. The platform answer — and it is the scalability case for this submission

The Fabry approach assays one variant at a time. The modern version assays all of them at
once, with the drug in the experiment.

**Deep mutational scanning** couples each variant in a pooled library to a selectable
readout and reads the whole library by sequencing [17]. The relevant lineage measures
*"variant effects **and protein-ligand interactions**"* in one assay, using cellular
transcriptional assays with DNA-barcoded reporters — developed for GPCRs and since
applied to TYK2 [18].

**The proof that this solves our question at scale** is a 2025 study of the vasopressin
2 receptor, where loss-of-function variants cause nephrogenic diabetes insipidus [1]:

- a multiplexed assay quantified the effect of **all possible variants** on cell-surface
  expression;
- **more than half** of known pathogenic variants were poorly expressed — loss of
  stability is the major mechanism;
- treatment with the stabiliser **tolvaptan rescued expression of 87% of destabilised
  variants**;
- and the **non-rescued variants identified the drug's own binding site** — an internal
  control that falls out of the design for free.

Their conclusion is the generalisable claim: *"proof-of-principle that small molecule
binding can rescue destabilising variants throughout a protein's structure"* [1].

### What that implies for MVA, stated as a proposal and not a result

**A BUB1B deep mutational scan with an abundance readout, run ± a chaperone co-inducer,
would answer for every BUB1B variant at once what we can currently only put a posterior
on for one.** It would classify each of the gene's VUS as amenable or not, and test the
drug in the same experiment. That is the generalisation of this child's question, and it
is the form in which an n-of-1 finding becomes useful to the next family.

**One design constraint, which the precedents hide.** Every success above — V2R, CFTR,
α-Gal A — is a **membrane or secreted protein with a trafficking checkpoint**, so surface
expression or lysosomal delivery gives a clean readout to sort on. **BubR1 is a nuclear
kinetochore scaffold.** There is nothing to stain on the cell surface. A BubR1 scan needs
a different readout — a tagged-abundance reporter, or a mitotic/checkpoint phenotype —
and choosing it is real experimental design, not a detail. Saying so is the difference
between a proposal and a gesture.

---

## 6. The question that matters most: has a high-risk approach been tried on an MVA gene?

**Yes. The record is in `MVA-THERAPEUTIC-EVIDENCE-BASE.md` and it splits by what the
intervention aimed at, not by how aggressive it was.**

**Interventions that removed or treated a consequence — these worked:**

| intervention | gene / context | outcome |
|---|---|---|
| **Tamoxifen**, 12 months post-surgery | *MAD2L1BP* juvenile granulosa cell tumour | **complete remission, sustained** |
| **Surgery alone** | *MAD1L1*, 12 neoplasias by age 36 | resected; **free of new pathology since 2014** |
| **Renal transplant at 20** + ciclosporin | *BUB1B* MVA1 | tolerated; 20-year follow-up reached |

**Interventions that tried to repair or replace the system — these failed:**

| intervention | gene / context | outcome |
|---|---|---|
| **HSCT** | ***BUB1B* MVA1 — the same gene as our proband** | engrafted, well tolerated, **cleared the monosomy 7 clone** — then **graft rejection day +47**, pancytopenia, multi-organ *E. faecium* sepsis, **death day +156** [21] |
| Growth hormone | *CEP57* MVA2 | ineffective; authors wrote *"Had this been known, growth hormone might have not been prescribed"* |
| G-CSF + romiplostim | same MVA1 patient | *"no response"* |
| Valproate + levetiracetam | *BUB1B* MVA1 | seizures continued |

**Why the HSCT case is the most important sentence available to us.** It is not a story
about a treatment that did not work. The transplant **achieved its stated mechanistic
goal** — it cleared the aneuploid clone driving the myelodysplasia — and the patient died
anyway, of a complication belonging to the intervention rather than to the disease. The
authors say so themselves: this *"needs to be taken into consideration for HSCT in other
MVA patients."*

Our report had been resting surveillance primacy on LFS-style survival statistics borrowed
from another syndrome. **This is direct, in-syndrome evidence for the same conclusion and
it is stronger.** In MVA, treating the consequence has worked and repairing the system has
not.

---

## What this changes in the submission

Nothing about the lead or the ranking. Four things about how it is argued:

| | before | after |
|---|---|---|
| our problem's status | a hard n-of-1 case | **the most common mechanism in rare disease** — 40–60% of pathogenic variants [1] |
| arimoclomol's mechanism | "HSF1 co-inducer" | an **amplifier** of a stress response, acting on a system this disease has depleted — with the tissue-heterogeneity and HSP-independent caveats stated [4][6] |
| why class B rather than class A | a consequence of our failed screen | the **structural negative is what selects** the only route with human exposure |
| the settling experiment | "a western blot" | **amenability**, as Fabry defines it: ≥1.2-fold over baseline, ≥3% absolute, in transfected cells ± drug — a protocol regulators have accepted for hundreds of variants (376 on the current label) |
| the scalable version | not stated | a **BUB1B DMS ± co-inducer**, on the V2R template, with its readout problem named |

---

REFERENCES

[1] Mighell, T.L. & Lehner, B. "A small molecule stabilizer rescues the surface
    expression of nearly all missense variants in a GPCR." (2025).
    https://citations.gxl.ai/papers/PMC12700812#L8,L13,L16
[2] Sitarska, D. et al. "Treatment trials in Niemann-Pick type C disease." (2021).
    https://citations.gxl.ai/papers/PMC8580890#L34-L37
[3] Hiwot, T. et al. "2025 Consensus Clinical Management Guidelines for Niemann-Pick
    Disease Type C." https://citations.gxl.ai/papers/PMC13110917#L244
[4] Las Heras, M. et al. "Understanding the phenotypic variability in Niemann-Pick
    disease type C (NPC): a need for precision medicine." (2023).
    https://citations.gxl.ai/papers/PMC10421955#L82-L84
[5] McAlary, L. et al. "Emerging Developments in Targeting Proteotoxicity in
    Neurodegenerative Diseases." (2019).
    https://citations.gxl.ai/papers/PMC6776490#L48-L49
[6] Pelaez, M.C. et al. "Reversal of cognitive deficits in FUS-R521G ALS mice by
    arimoclomol and a class I HDAC inhibitor independent of heat shock protein
    induction." (2024). https://citations.gxl.ai/papers/PMC11579874#L11-L13
[7] Živná, M. et al. "Lysosomal Storage-Independent Fabry Disease Variants..." (2025).
    https://citations.gxl.ai/papers/PMC12121966#L30-L31
[8] Nowicki, M. et al. "A review and recommendations for oral chaperone therapy in adult
    patients with Fabry disease." (2024).
    https://citations.gxl.ai/papers/PMC10797794#L24
[9] Lerario, S. et al. "Fabry disease: a rare disorder calling for personalized
    medicine." (2024). https://citations.gxl.ai/papers/PMC11405476#L66-L67
[10] Muntean, C. et al. "Clinical Characteristics, Renal Involvement, and Therapeutic
    Options of Pediatric Patients With Fabry Disease." (2022).
    https://citations.gxl.ai/papers/PMC9198369#L201-L202
[11] Germain, D.P. et al. "Safety and pharmacodynamic effects of a pharmacological
    chaperone on α-galactosidase A activity..." (2012).
    https://citations.gxl.ai/papers/PMC3527132#L77
[12] Bichet, D.G. et al. "Consensus recommendations for the treatment and management of
    patients with Fabry disease on migalastat: a modified Delphi study." (2023).
    https://citations.gxl.ai/papers/PMC10505750#L41-L43
[13] Dhuri, K. et al. "Antisense Oligonucleotides: An Emerging Area in Drug Discovery
    and Development." (2020). https://citations.gxl.ai/papers/PMC7355792#L65
[14] Bou-Jaoudeh, M. et al. "Toward an Extensible Regulatory Framework for N-of-1 to
    N-of-Few Personalized RNA Therapy Design." (2025).
    https://citations.gxl.ai/papers/PMC12018499#L29-L38
[15] Singh, J. et al. "Evidence Synthesis of Gene Therapy and Gene Editing from
    Different Disorders." (2023).
    https://citations.gxl.ai/papers/PMC10219055#L127-L129
[16] Goel, H. "Beyond Coding Variants: RNA-Level Mechanisms in Human Disease and
    Precision Therapeutics." https://citations.gxl.ai/papers/PMC13409656#L94
[17] Maes, S. et al. "Deep mutational scanning of proteins in mammalian cells." (2023).
    https://citations.gxl.ai/papers/PMC10694495#L17-L18
[18] Howard, C.J. et al. "Deep mutational scanning reveals pharmacologically relevant
    insights into TYK2 signaling and disease."
    https://citations.gxl.ai/papers/PMC13252953#L14
[19] Laberko, A. et al. "Hematopoietic stem cell transplantation in a patient with type 1
    mosaic variegated aneuploidy syndrome." *Orphanet J Rare Dis* (2019), on monoallelic
    BUB1B patients with reduced transcript and protein.
    https://citations.gxl.ai/papers/PMC6500003#L19
[20] Herman, J.A. et al. "Hyper-active RAS/MAPK introduces cancer-specific mitotic
    vulnerabilities." (2022), Mis12-KARD3D fusion rescue.
    https://citations.gxl.ai/papers/PMC9565228#L24
[21] Laberko, A. et al., as above — the HSCT course and outcome.
    https://citations.gxl.ai/papers/PMC6500003#L12,L14
