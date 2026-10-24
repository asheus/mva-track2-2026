> **Correction, 6 Oct 2026.** The direction of effect asserted in this document is
> **contested** and the one-directional rule derived from it is retracted. Lee 2004,
> Janssen 2009 and Dowling 2005 report that reduced BubR1 *sensitises* to
> microtubule-targeting drugs; Cohen-Sharir 2021 shows the sign flips with the observation
> window (short-term resistance, long-term sensitivity) in aneuploid cells specifically.
> Read with `CORRECTIONS-2026-10-06.md` C1. Nothing here is clinical advice, and the
> earlier prescribing-adjacent phrasing is withdrawn.

# The arm we missed: this genotype predicts how the child's tumours respond to chemotherapy

Every earlier arm in this workstream asked *what new drug could we add*. None asked the
question the clinical record makes unavoidable: **this child has already had a
rhabdomyosarcoma, will face relapse surveillance, and rhabdomyosarcoma is treated with
vincristine.** The genotype makes a direct prediction about that.

---

## The mechanism, in one line

**Antimitotic chemotherapy kills by triggering spindle-assembly-checkpoint-dependent
mitotic arrest. This child's spindle assembly checkpoint is genetically crippled. That is
the diagnosis.**

Vinca alkaloids and taxanes both work by perturbing microtubule dynamics so that
kinetochores cannot satisfy the checkpoint; the resulting sustained arrest is what kills.
Vinca alkaloids destabilise and taxanes stabilise, but both depend on the same downstream
machinery — and *BUB1B* encodes a core component of it [1,2].

So a checkpoint that cannot hold an arrest is a checkpoint that cannot execute the drug's
mechanism. Cells exit mitosis early instead of dying in it.

## The evidence, strongest first

**1. Germline *BUB1B* variants that reduce BubR1 levels drive taxane resistance — and the
mechanism is the one our whole thesis is about.** Silva et al. studied rare germline
*BUB1B* variants in prostate cancer predisposition and report that they *"lead to
decreased BubR1 expression and/or stability, which promotes increased premature chromatid
separation and, consequently, triggers CIN, **driving resistance to Taxol-based
therapies**"* [3]. Their edited cells exit mitosis in **10.8–11.6 h against 14.9–15.4 h**
for wild-type — premature mitotic exit, measured directly — and the SAC impairment was
*"as severe as the acute SAC disruption obtained upon Mps1 inhibition"* [3].

This matters more than a generic SAC result, because the causal step is **reduced BubR1
expression and stability**. That is precisely this child's lesion: a null allele plus a
destabilised missense allele.

**2. Direct *BUB1B* knockdown produces a ~10-fold shift in antimitotic potency.** A
whole-genome CRISPR screen identified the SAC as a locus of nab-paclitaxel resistance, and
validation by *BUB1B* shRNA knockdown raised the IC50 **roughly tenfold, from ~1 nM to
~10 nM** [4]. Gene-specific, not a pathway inference.

**3. The same relationship appears from the resistance direction.** Acquired
paclitaxel-resistant ovarian lines show depletion of checkpoint genes [5], and the taxane
resistance literature names BUBR1 among the effectors whose loss weakens the arrest [6].

**4. Vincristine is a backbone of rhabdomyosarcoma therapy**, acting as a microtubule
destabiliser causing metaphase arrest [1,7].

Four independent lines — a CRISPR screen, targeted knockdown, germline variant editing,
and acquired resistance models — converge.

## What this changes

**It reframes repurposing for this child.** The question stops being *"what can we add?"*
and becomes *"given this genotype, which approved drugs will and will not work, and
which should be preferred?"* That is pharmacogenomics of the checkpoint, it uses only
approved agents, and it speaks to what has already happened to this patient rather than
what might.

**It gives the stabilisation thesis a second, independent rationale.** Our lead
(§3, `TRACK2-REPORT.md`) aims to raise BubR1 to reduce aneuploidy. If reduced BubR1 also
blunts SAC-dependent chemotherapy, then raising it is **potentially chemosensitising** —
the same intervention, a second endpoint, and a far more measurable one. A BubR1-raising
agent would be testable as an adjunct to standard therapy, not only as a chronic
disease-modifier.

**And it suggests a preference ordering among drugs already in use.** Agents whose killing
does **not** route through checkpoint-dependent mitotic arrest are unaffected by this
logic: the alkylating and DNA-damaging components of standard rhabdomyosarcoma regimens,
and the topoisomerase inhibitors used in relapse, kill by mechanisms orthogonal to the
SAC. This analysis does not rank them — that is a clinician's call with the treatment
history in hand — but it identifies *why* the distinction matters here.

## What would refute it, and what we cannot claim

This is the part earlier arms in this workstream got right and we hold to here.

- **The direct drug evidence is taxane, not vincristine.** The bridge is mechanistic —
  both require checkpoint-dependent arrest — but no experiment pairs *BUB1B* loss with
  vincristine that we found. **This is the single biggest gap**, and it is a cheap
  experiment: vincristine dose–response in *BUB1B*-deficient versus corrected cells.
- **All of it is cell lines and engineered loss.** No patient tumour-response data exists
  for *BUB1B*-MVA, and an IC50 shift in PANC-1 is a long way from a clinical outcome in a
  child.
- **Premature mitotic exit is not survival.** Cells that slip out of arrest with
  unsegregated chromosomes can still die, by mitotic catastrophe or in the subsequent
  interphase. "Resistant" in a viability assay is a shift, not immunity — and a tenfold
  IC50 change may or may not cross a clinically meaningful threshold at achievable doses.
- **MVA patients are treated, and some respond.** Any claim of outright resistance is
  contradicted by clinical experience. The defensible claim is *reduced efficacy of
  SAC-dependent agents is mechanistically predicted and worth measuring*, not *these drugs
  will fail*.
- **It cuts both ways on toxicity.** Every cell in this child is checkpoint-deficient, not
  only the tumour, so the same logic that predicts reduced tumour kill may predict altered
  normal-tissue toxicity. We have no evidence on direction and do not guess.

**Nothing here is a treatment recommendation, and nothing here should change any child's
therapy.** It is a mechanistic prediction with a named experiment attached, offered
because the prediction is specific, falsifiable, and follows from the genotype the
organisers gave us.

--------
REFERENCES

[1] Yamada, H. Y. & Gorbsky, G. J. "Cell-based expression cloning for identification of
    polypeptides that hypersensitize mammalian cells to mitotic arrest."
    *Cell Cycle* (2006). https://citations.gxl.ai/papers/PMC1455480#L9-L11

[2] Tischer, J. & Gergely, F. "Anti-mitotic therapies in cancer."
    *J. Cell Biol.* (2019). https://citations.gxl.ai/papers/PMC6314557#L7-L9

[3] Silva, M. P. et al. "BUB1B monoallelic germline variants contribute to prostate cancer
    predisposition by triggering chromosomal instability." (2024).
    https://citations.gxl.ai/papers/PMC11251299#L18,L134,L135

[4] Mondal, P., Alyateem, G., Mitchell, A. V. & Gottesman, M. M. "A whole-genome CRISPR
    screen identifies the spindle accessory checkpoint as a locus of nab-paclitaxel
    resistance in a pancreatic cancer cell line." (2024).
    https://citations.gxl.ai/papers/PMC11236977#L45-L46

[5] Chong, T. et al. "Deregulation of the spindle assembly checkpoint is associated with
    paclitaxel resistance in ovarian cancer." (2018).
    https://citations.gxl.ai/papers/PMC5885411#L94

[6] Maloney, S. M., Hoover, C. A., Morejon-Lasso, L. V. & Prosperi, J. R. "Mechanisms of
    Taxane Resistance." *Cancers* (2020).
    https://citations.gxl.ai/papers/PMC7697134#L99

[7] Zarrabi, A. et al. "Rhabdomyosarcoma: Current Therapy, Challenges, and Future
    Approaches to Treatment Strategies." (2023).
    https://citations.gxl.ai/papers/PMC10650215#L77-L85
