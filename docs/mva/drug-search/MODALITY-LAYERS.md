# Which molecule does the drug act on? The layer decides who it can reach

*Prompted by three questions in sequence: can the locus be regulated, can trans-splicing
help, and can trans-RNA/circRNA solve this. The answers turn out to be the same answer,
and it is the one our eligibility map was built to give.*

*According to PubMed for the literature. Regulatory annotation from Ensembl, retrieved
21 Oct 2026. Producers: `transsplice_model.py`, `dosage_headroom.py`.*

## The organising idea

Every therapeutic modality acts on **one molecule in the chain** — DNA, pre-mRNA, mRNA, or
protein. Which molecule it acts on decides which alleles it can possibly reach, before any
question of potency or delivery. For this proband:

| layer | modality | reaches allele 1 (p.Leu737Ter) | reaches allele 2 (p.Asn1002Lys) |
|---|---|---|---|
| DNA / transcription | CRISPRa, enhancer modulation | yes | yes |
| **pre-mRNA** | **trans-splicing (SMaRT)** | **yes** | yes |
| mRNA | trans-RNA, readthrough, ASO | **no** | yes |
| protein | NAD⁺/degradation, chaperone | **no** | yes |

**Allele 1's transcript is destroyed, so everything downstream of pre-mRNA is blind to
it.** That single fact, which our map computes for all 2,536 catalogued alleles, survives
every change of modality. The eligibility boundary does not move when the technology does
— which is the strongest argument we have that the map is the durable deliverable.

## 1 · Can the locus be regulated?

Yes, and the elements have coordinates. Ensembl's regulatory build gives *BUB1B*:

- **Promoter region at the TSS** — `ENSR15_9KXDL` (chr15:40,160,577-40,161,079, 502 bp,
  spanning the TSS at 40,161,023) and `ENSR15_C5ZL7` (40,161,080-40,162,462, 1,382 bp).
- The strongest distal eQTL, **+114 kb**, falls inside `ENSR15_9KZLM`, an annotated
  **promoter** at chr15:40,274,827-40,275,225, flanked by **three CTCF binding sites**.
  CTCF anchors loops, which is a coherent mechanism for a 114 kb contact.

**The catch, and it is the same catch as before.** That distal element sits at the 3′ end
of **PAK6** (40,217,428-40,277,489) and overlaps a novel transcript annotated antisense to
PAK6. This is the third time the *BUB1B*–PAK6 overlap has mattered in this project — it
previously corrupted 200 of our splice-sweep jobs. **Any perturbation of the distal element
is likely to move PAK6 as well**, so the TSS-proximal promoter is the cleaner target.

For a therapy this is weak: CRISPRa is not deliverable to a whole child today. For an
**experiment** it is strong, and that is the honest use — CRISPRa at the proximal promoter
in patient-derived cells answers *"if we raise BUB1B, does the aneuploidy fall?"*, which is
the question every other candidate on our list presupposes and none of them tests.

## 2 · Trans-splicing — the only modality that reaches the dead allele

We had written allele 1 off. For readthrough that was right; for trans-splicing it is
wrong, and the reason is precise:

> **NMD acts on mature mRNA**, after export and a pioneer round of translation.
> **Trans-splicing acts on pre-mRNA, in the nucleus, before any of that.**

Allele 1's pre-mRNA is made normally; only its spliced product is destroyed. A pre-mRNA
trans-splicing molecule that replaces the 3′ segment carrying the PTC yields an mRNA with
**no PTC at all**, which then escapes decay entirely.

**The precedent is exact in shape.** Maruna et al. applied SMaRT to *CTNNB1*
haploinsufficiency, choosing it because the gene has "a wide variety of mutations" and is
**dosage sensitive**, so what is needed is "a mutation-independent therapeutic approach
that **preserves endogenous gene regulation**" (Mol Ther Nucleic Acids 2025,
[10.1016/j.omtn.2025.102680](https://doi.org/10.1016/j.omtn.2025.102680)). They used
antisense RNAs masking splicing regulatory elements and a 5′ self-cleaving ribozyme for
nuclear retention, and trans-spliced the **endogenous** transcript. Every clause of their
rationale applies here.

**What efficiency would this genotype need?** Trans-splicing is mutation-agnostic, so one
molecule acts on both alleles at efficiency *e*:

```
  total = 0.5 * (2e + (1-e) * f2)        e >= (1 - f2) / (2 - f2)  to reach 50%
```

| if allele 2 delivers | total today | efficiency needed |
|---|---|---|
| 85% | 42.5% | **13.0%** |
| 70% | 35.0% | **23.1%** |
| 55% | 27.5% | **31.0%** |
| 40% | 20.0% | **37.5%** |

**Roughly 23–38%.** Demanding — SMaRT's chronic difficulty is exactly the trans- to
cis-splicing ratio — but a number, and not 90%. Two features of this genotype lower the
bar: allele 1 sits at zero, so corrected copies are pure gain rather than replacement; and
one molecule acts on both alleles, so the contributions add.

**What would falsify it:** if allele 1's locus is transcriptionally silenced rather than
merely NMD-targeted, the allele-1 term is zero at every efficiency. Allele-specific
**pre-mRNA** quantification in patient cells settles that and should precede any design.

## 3 · trans-RNA, and what it does and does not do here

**Jia et al., *Nature Biotechnology*, 21 Nov 2025 — "Programmable initiation of mRNA
translation by trans-RNA"** ([10.1038/s41587-025-02897-1](https://doi.org/10.1038/s41587-025-02897-1)).
Capped trans-RNAs direct ribosomes to chosen initiation sites on an individual mRNA,
facilitating ribosome loading and scanning through alternative cap recognition. They work
on **endogenous genes in vivo in mouse liver**, and — this is the circRNA connection —
they act **independently of the cap on the target**, enabling **translation of circular
RNAs that lack an IRES**.

**Where it fits for us.** Steady-state protein is synthesis ÷ degradation. If N1002K is a
degradation defect, raising initiation on its transcript raises steady state
proportionally — so a trans-RNA aimed at *BUB1B*'s own start codon targets the right
variable, on the endogenous, cell-cycle-regulated message.

**Where it does not.** It acts on mRNA, so **it cannot reach allele 1** — the transcript
isn't there. Same boundary, new technology. And it is very new: published weeks ago,
patent filed (PCT/US2024/17174, Cornell), with a founder-linked company. No human data.

## 4 · Why circRNA-encoded BubR1 is the wrong shape for *this* gene

A circRNA encoding BubR1 — now translatable without an IRES, per the trans-RNA work —
would supply protein directly and durably. **Durably is the problem.**

Choi 2009 showed that stabilising BubR1 beyond its normal window **markedly delays
chromosome segregation** ([10.1038/emboj.2009.123](https://doi.org/10.1038/emboj.2009.123)).
BubR1 is a checkpoint protein: it has to rise and fall with the cell cycle, not simply be
present. A constitutive exogenous source decouples it from the cycle in a cell that is
already mis-segregating.

So for *BUB1B*, "preserves endogenous gene regulation" — the phrase the CTNNB1 authors use
as a design preference — **is a safety requirement, not an elegance.** That single
consideration orders the whole family:

| approach | preserves cell-cycle regulation | reaches allele 1 |
|---|---|---|
| trans-splicing of endogenous pre-mRNA | **yes** | **yes** |
| trans-RNA on endogenous mRNA | **yes** | no |
| CRISPRa at the endogenous promoter | yes | yes |
| circRNA encoding BubR1 | **no** | n/a (bypasses both) |

circRNA is not useless here — it is a good **vector** for a trans-splicing molecule or a
trans-RNA, where stability and nuclear persistence are advantages and the regulation stays
with the endogenous gene. It is the *payload-as-protein* version we would argue against.

## What this does to the submission

It strengthens the central claim rather than replacing it. Three modalities were proposed
in three questions — promoter regulation, trans-splicing, trans-RNA/circRNA — and all three
sorted themselves on **the same boundary our map already computes**: does this allele leave
a transcript, and does it leave a protein.

**280 of 2,536 alleles lose the transcript.** No mRNA-level or protein-level modality
reaches them, however new. Only the pre-mRNA and DNA layers can, and of those only
trans-splicing is a plausible therapy today.

That is the map earning its keep for the fourth time: the technology keeps changing and the
eligibility boundary does not.
