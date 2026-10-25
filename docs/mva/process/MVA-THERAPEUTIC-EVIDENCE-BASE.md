# Every therapy ever reported in MVA — a compiled evidence base

Swept 10 Sep 2026 with Paperclip across 3.4M+ papers and 1.08M+ registered trials.
Extraction was run as a structured per-paper read over the MVA cohort, then reviewed.
This compilation did not previously exist in our work and, as far as this sweep can
tell, is not collected anywhere in one place.

## The hardest finding: there has never been a clinical trial in MVA

An **exhaustive** scan for `variegated aneuploidy` across every registry Paperclip
indexes — ClinicalTrials.gov, ChiCTR, UMIN/JRCT, EudraCT/CTIS/ISRCTN and WHO ICTRP —
returns **zero matches**. A topical search returns only IVF/embryo-screening studies,
which use "aneuploidy" and "mosaicism" in an unrelated sense.

Consequences for this submission:
- Any proposal here is necessarily **n-of-1 or compassionate use**. There is no trial
  to join and no precedent trial design to copy.
- The entire therapeutic record for MVA is **case reports**. That is the ceiling on
  the evidence, and it should be stated as such rather than implied.

## Everything that has actually been given to an MVA patient

| Intervention | Genotype / context | Outcome |
|---|---|---|
| **HSCT** (TCRαβ/CD19-depleted, MUD) after treosulfan/fludarabine/thymoglobulin RIC | *BUB1B* MVA1 with MDS + monosomy 7 | Engrafted, **cleared the monosomy 7 clone**; conditioning well tolerated; then **graft rejection day +47, death day +156** [1] |
| **Rituximab** 375 mg/m² ×4 | same patient | Reduced platelet-transfusion frequency; patient **remained cytopenic** [1] |
| **G-CSF (filgrastim)** and **romiplostim** | same patient | **"no response"** [1] |
| **Tamoxifen** 12 months after surgery | *MAD2L1BP* juvenile granulosa cell tumour | **Complete remission, sustained** [2] |
| **Growth hormone** | *CEP57* MVA2 (multiple patients) | **Ineffective.** "growth hormone treatment is ineffective in such patients"; initial velocity gain then secondary decline, height still <P3 at 9 [3] |
| **Leuprolide + GH + metformin** | *CEP57* MVA2 | Given for precocious puberty / short stature / acanthosis nigricans; authors reflect "**Had this been known, growth hormone might have not been prescribed**" [4] |
| **Valproate + levetiracetam** | *BUB1B* MVA1 | Seizures **continued**; historical MVA1 cases describe "drug unresponsive" seizures [5] |
| **Surgical excision** (neuroblastoma at 8 mo), **renal transplant** at 20 with ciclosporin | *BUB1B* MVA1, 20-year follow-up | Tumour excised; transplant required immunosuppression [6] |
| **Reduced-intensity chemotherapy** | PCS/MVA with rhabdomyosarcoma | Reported without detailed outcome [7] |
| Surgery only — orchiectomy, hemithyroidectomy, polypectomy, resections | *MAD1L1*; 12 neoplasias by age 36 | Tumours resected; free of new pathology since 2014 [8] |

## The decision that corroborates our safety gate

Gate 3 refused mitotic-machinery agents on the reasoning that further perturbing
mitosis in a checkpoint-deficient child is the wrong direction. A clinical team
reached the same conclusion in practice. In a *CDC20* MVA patient with uterine
endometrial carcinoma:

> "we diagnosed the patient with MVA syndrome and **decided not to administer adjuvant
> chemotherapy using taxanes** after surgery" [9]

Taxanes are spindle poisons. **A real clinical team withheld one specifically because
of the MVA diagnosis.** That is independent corroboration of the funnel's safety
reasoning from actual practice, not from theory — and it is the single most citable
sentence found in this sweep.

## Two findings that cut against our own leads

**1. Two of our Gate 2 candidates have already failed in an MVA1 patient.**
`filgrastim` and `romiplostim` both survived into the 34-candidate set. In the one
MVA1 patient in whom they were tried, there was **"no response"** [1]. That is not a
refutation of their mechanism, but it is direct negative evidence in the right
genotype, and it should be recorded against them.

**2. The MAD1L1 authors propose the OPPOSITE of immunosuppression.** Having found
systemic inflammation and clonal γδ T-cell expansion in their SAC-deficient patient,
they conclude:

> "**Exploiting the enhanced immune response associated to aneuploidy** could provide
> new opportunities for the clinical management of these patients" [8]

Our Arm A proposes to **blunt** IL-1/IL-6 signalling. They propose to **harness** the
immune response. If the inflammation is partly protective immunosurveillance against
aneuploid clones — which is precisely what Gate 3 worried about — then anakinra or
canakinumab could remove a defence. This is the strongest argument against the leads
found so far, and it comes from the same paper that supplies Arm A's best supporting
evidence. Both readings are in one dataset.

## Corrections this forces

**The gene list is out of date.** The report names *BUB1B*, *CEP57* and *TRIP13*. The
MVA/SAC-deficiency spectrum now also includes **MAD1L1** [8], **MAD2L1BP** (p31comet)
[2], **CDC20** [9] and **CEP192** [10]. This matters for scalability: a method keyed
to three genes is narrower than the disease.

**Surveillance has a published cadence.** Two independent groups give concrete
protocols — "regular abdominal ultrasound surveillance, to particularly look for Wilms
tumor" [6], and "abdominal ultrasound, fundus examination, and hematological checkup
are advised **every 3 months**" [5]. The report should cite these rather than say
surveillance "continues regardless".

**Genotype stratifies risk, including for treatment.** *CEP57* patients are not
thought to carry increased cancer risk [7], and none in the reviewed series developed
malignancy [3] — while *TRIP13* carries the highest Wilms risk [7]. GH is both
ineffective *and* cautioned on cancer grounds in *CEP57* [3]. Treatment decisions in
MVA are already genotype-specific in practice.

**Correction of a prior candidate mechanism.** iPSC reprogramming of BubR1-hypomorphic
mouse fibroblasts **did not correct** the aneuploidy [11] — worth knowing before
anyone proposes a reprogramming-based approach.

--------
REFERENCES
[1] Laberko A, et al. "Hematopoietic stem cell transplantation in a patient with type 1 mosaic variegated aneuploidy syndrome." (2019).
    https://paperclip.gxl.ai/citations/papers/PMC6500003#L12,L30,L31,L33,L39
[2] Abdel-Salam GMH, et al. "Biallelic MAD2L1BP (p31comet) mutation is associated with mosaic aneuploidy and juvenile granulosa cell tumors." (2023).
    https://paperclip.gxl.ai/citations/papers/PMC10721328#L37
[3] Feng B, et al. "A novel CEP57 variant associated with mosaic variegated aneuploidy syndrome..." *Mol Genet Genomic Med* (2022).
    https://paperclip.gxl.ai/citations/papers/PMC9184657#L14,L46,L48
[4] Brightman DS, Ejaz S, Dauber A. "Mosaic variegated aneuploidy syndrome caused by a CEP57 mutation diagnosed by whole exome sequencing." (2018).
    https://paperclip.gxl.ai/citations/papers/PMC6099013#L14,L21
[5] Pavone P, et al. "Pathogenic correlation between mosaic variegated aneuploidy 1 (MVA1) and a novel BUB1B variant." (2022).
    https://paperclip.gxl.ai/citations/papers/PMC9616775#L30,L35,L41
[6] Lin SM, et al. "Prenatal diagnosis and long-term follow-up of a Chinese patient with mosaic variegated aneuploidy." (2020).
    https://paperclip.gxl.ai/citations/papers/PMC7455400#L19,L20,L26
[7] Wolfe Schneider K, et al. "Germline predisposition to genitourinary rhabdomyosarcoma." (2020).
    https://paperclip.gxl.ai/citations/papers/PMC7658107#L26,L27,L95
[8] Villarroya-Beltri C, et al. "Biallelic germline mutations in MAD1L1 induce a syndrome of aneuploidy with high tumor susceptibility." *Sci Adv* (2022).
    https://paperclip.gxl.ai/citations/papers/PMC9629740#L25,L56,L60
[9] Fujita H, et al. "Premature aging syndrome showing random chromosome number instabilities with CDC20 mutation." (2020).
    https://paperclip.gxl.ai/citations/papers/PMC7681047#L20,L22
[10] Guo J, et al. "Mosaic variegated aneuploidy syndrome with tetraploid, and predisposition to male infertility triggered by mutant CEP192." (2023).
    https://paperclip.gxl.ai/citations/papers/PMC10716027#L8,L54
[11] Akutsu SN, et al. "Applications of Genome Editing Technology in Research on Chromosome Aneuploidy Disorders." (2020).
    https://paperclip.gxl.ai/citations/papers/PMC7016705#L28,L30,L32
