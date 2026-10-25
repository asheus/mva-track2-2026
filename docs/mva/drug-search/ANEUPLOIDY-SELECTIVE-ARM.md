# Aneuploidy-selective therapy: the arm that fails, and the rule that explains why

The idea is attractive enough that it should be tested properly: aneuploid cells carry
specific liabilities, so rather than fixing the checkpoint, **selectively kill the
chromosomally unstable cells** — the population from which this child's tumours arise.

**It fails here, for two independent reasons, and the first of them generalises into the
most useful rule this workstream has produced.**

---

## The candidate was real

**KIF18A** is the best-validated aneuploidy-selective target in oncology. Large-scale
genetic screens identified it as selectively essential in high-CIN cells, and its
inhibition *"robustly impairs the viability of cancer cells exhibiting CIN while sparing
nontransformed, chromosomally stable cells"* [1]. Inhibitors are **in clinical trials**
[2], and in preclinical osteosarcoma work the inhibitor AM-1882 *"prevented tumor growth
and, notably, did not show any toxicity when compared with chemotherapeutic drugs"* [3].

A CIN-selective agent, clinically advancing, low toxicity, aimed squarely at the
population that produces this child's malignancies. On its face, the best idea in the
file.

## Reason 1: the drug's killing mechanism is the exact thing this child lacks

KIF18A inhibition does not kill by some generic aneuploidy stress. It kills **through the
spindle assembly checkpoint**: *"Loss of KIF18A expression led to aberrant spindle
assembly and mitotic delay through the activation of spindle assembly checkpoint (SAC)
signaling"* [3].

And the same study ran the rescue experiment — **using BubR1 knockdown**:

> *"SAC deficiency reduces the KIF18A depletion-induced SPT1 cell death ... transfected
> with control, MAD2, or **BubR1 siRNA**"* [3, Fig. 3]
>
> *"we found that **SAC inactivation rescued the loss of KIF18A**, indicating that KIF18A
> depletion-induced mitotic delay and cell death are dependent on SAC signaling"* [3]

The published rescue for a KIF18A inhibitor **is this child's genotype**. Independently,
MAD2-depleted leukaemia cells showed that *"KIF18A deficiency did not induce chromosome
missegregation and cell death"* [3, citing Janssen et al.].

So the agent that looks tailor-made for chromosomal instability is predicted to be
**inert** in a child whose checkpoint cannot mount the arrest the drug depends on.

## Reason 2: RETRACTED 6 Oct 2026 — wrong axis

> **This section's argument is withdrawn.** See `CORRECTIONS-2026-10-06.md` C2. The axis
> that matters is **transformed vs untransformed**, not aneuploid vs euploid: Janssen 2009
> reports that *"untransformed human fibroblasts with reduced Mps1 levels could not be
> sensitized to sublethal doses of taxol"*. MVA is also mosaic, so a euploid fraction does
> exist. Reason 1 stands and is independently corroborated by Cohen-Sharir 2021. The
> original text is kept below for the record.

### Original text (retracted)

The entire therapeutic window for CIN-selective agents comes from a contrast: the tumour
is chromosomally unstable, the patient's normal tissue is not. **That contrast does not
exist in mosaic variegated aneuploidy.** This child's non-malignant tissues are aneuploid
too — that is the diagnosis, not a tumour property.

An agent whose selectivity *is* "kills CIN cells, spares stable cells" therefore has
nothing to spare. Even if reason 1 did not apply, the safety case that makes KIF18A
attractive in cancer evaporates in a germline CIN syndrome. **A selectivity argument
borrowed from oncology does not transfer to a constitutional disease, and we should be
suspicious of every oncology-derived arm for exactly this reason.**

---

## The rule, which is the actual finding

Reason 1 is not specific to KIF18A. Combined with `CHEMOSENSITIVITY-ARM.md`, it states a
single genotype-derived principle:

> **Any therapy whose cytotoxicity routes through SAC-dependent mitotic arrest is
> predicted to underperform in this child — and in each case the published rescue
> experiment is reduced BubR1 or SAC function.**

| therapy class | killing mechanism | published rescue | predicted here |
|---|---|---|---|
| Vinca alkaloids (**vincristine** — in RMS regimens) | SAC-dependent mitotic arrest | *BUB1B* knockdown → ~10× IC50 shift [4]; germline *BUB1B* variants → taxane resistance [5] | **underperforms** |
| Taxanes | SAC-dependent mitotic arrest | as above | **underperforms** |
| **KIF18A inhibitors** | SAC activation after loss of spindle tension | **BubR1 siRNA rescues the killing** [3] | **inert** |
| MPS1/TTK inhibitors | abolish the SAC outright | — | mechanism already absent |
| DNA-damaging / alkylating / topoisomerase agents | SAC-independent | — | **unaffected by this logic** |

Two things follow that are worth more than another hopeful candidate.

**It is predictive, not retrospective.** The rule was derived from the chemotherapy arm
and then correctly predicted that the best-looking aneuploidy-selective agent would fail
— before we looked for the rescue experiment. Finding BubR1 siRNA as the published
rescue was a confirmation, not the premise.

**It gives the lead a third rationale.** If SAC-dependent killing is the common failure
mode, then raising BubR1 is not only disease-modifying and potentially chemosensitising
(`CHEMOSENSITIVITY-ARM.md`) — it is the step that would make an entire class of
otherwise-inert agents available. That is a mechanistic argument for sequencing: restore
checkpoint capacity first, then the checkpoint-dependent agents become usable.

## Honest limits

- **Mechanistic prediction, not measured outcome.** No KIF18A inhibitor has been tested
  in a *BUB1B*-deficient background, let alone in MVA. The rescue experiments are siRNA
  and shRNA in cancer lines.
- **The rule predicts direction, not magnitude.** "Underperforms" is not "fails";
  degree-of-SAC-impairment almost certainly matters, and this child retains partial
  function from one allele.
- **Mitotic slippage still kills sometimes.** Cells that exit arrest with unsegregated
  chromosomes can die later, and the KIF18A paper itself notes that most of its cells
  *"successfully completed division"* yet growth was still inhibited [3] — so
  SAC-independent consequences of induced CIN may matter more than the arrest.
- **Aneuploidy has other liabilities we did not test**, including the proteotoxic and
  HSF1/HSP90 axis in `BINDING-AND-STABILISING.md`. The rule retires *SAC-dependent*
  approaches, not aneuploidy-selective approaches in general — though reason 2 applies to
  all of them.
- **Nothing here is a treatment recommendation.** It is a falsifiable prediction about
  drug classes, offered because it follows from the genotype and names its own
  disconfirming experiment.

--------
REFERENCES

[1] Mennie, A. K., Dhital, B. & Ly, P. "Impact of Chromosomal Instability and Aneuploidy
    in Cancer Development." (2025). https://citations.gxl.ai/papers/PMC13170371#L51

[2] Mallick, S., Choi, Y., Taylor, A. M. & Cosper, P. F. "Human Papillomavirus-Induced
    Chromosomal Instability and Aneuploidy in Squamous Cell Cancers." (2024).
    https://citations.gxl.ai/papers/PMC11053578#L41

[3] Yan, Q. et al. "KIF18A inhibitor prevents chromosomally unstable osteosarcoma growth
    by activating spindle assembly checkpoint." *Cancer Biol. Ther.* (2026).
    doi:10.1080/15384047.2026.2689181
    https://citations.gxl.ai/papers/PMC13290091#L10,L29,L45,L46

[4] Mondal, P., Alyateem, G., Mitchell, A. V. & Gottesman, M. M. "A whole-genome CRISPR
    screen identifies the spindle accessory checkpoint as a locus of nab-paclitaxel
    resistance in a pancreatic cancer cell line." (2024).
    https://citations.gxl.ai/papers/PMC11236977#L45-L46

[5] Silva, M. P. et al. "BUB1B monoallelic germline variants contribute to prostate cancer
    predisposition by triggering chromosomal instability." (2024).
    https://citations.gxl.ai/papers/PMC11251299#L18,L134
