# Drug candidates for raising BubR1, ranked by how much evidence already exists

*According to PubMed for the literature; ClinicalTrials.gov for trial counts, queried
21 Oct 2026. Numbers from our own work come from `dosage_model.py` and `ptc_context.py`.
No dose, route or schedule appears here; this is a mechanism argument, not a protocol, and
nothing in it is advice about any individual.*

## First: has anyone ever solved MVA?

**No — and nobody has tried.** ClinicalTrials.gov returns **0** studies for mosaic
variegated aneuploidy and **0** for *BUB1B*. We searched the literature for a treated
patient under both names the disease carries (MVA and premature chromatid separation
syndrome) and for any case report of a disease-modifying intervention, and found none. We
state that as a search result rather than a proof of absence, but across that many
phrasings the conclusion is safe: **there is no treated patient, no n-of-1, and no failed
attempt.**

**The closest anyone has come is a cell, and it worked.** Matsuura et al. took cells from
patients with this disease and transferred in a chromosome 15 carrying *BUB1B*. That
**restored normal BubR1 levels, restored kinetochore localisation of p55cdc, and restored
the normal response to colcemid** (Am J Med Genet A 2006,
[10.1002/ajmg.a.31069](https://doi.org/10.1002/ajmg.a.31069)).

That single experiment is the foundation of everything below. It says the defect behaves
as a **dosage defect**, and that putting the dosage back puts the cell back. Nobody has
since asked whether a drug can do what the chromosome did.

## How much dosage is missing

From the same paper: **"> 50% decrease in expression (or activity) of BubR1 is involved in
the PCS syndrome."** Disease appears below roughly half of normal.

Now the proband's arithmetic (`dosage_model.py`). Allele 1 (p.Leu737Ter) contributes
**zero**, and that is fixed rather than assumed: its PTC sits 748 nt upstream of the last
exon–exon junction, so the transcript is a canonical NMD substrate, and even transcript
that escapes decay would make a protein terminating at residue 737 of 1,050 — missing the
entire pseudokinase domain (766–1050) and the CENP-E interface (1031–1050). Both routes
give zero.

So allele 2 is the only source, and **the genotype's ceiling is 50% — exactly the
threshold.** The child is affected, so allele 2 must deliver less than a full wild-type
allele's worth, and the true figure is strictly below it:

| if allele 2 delivers | total functional BubR1 | fold-increase needed to reach 50% |
|---|---|---|
| 100% | 50.0% — *at* threshold | 1.00× |
| 85% | 42.5% | 1.18× |
| **70%** | **35.0%** | **1.43×** |
| 55% | 27.5% | 1.82× |
| 40% | 20.0% | 2.50× |
| 25% | 12.5% | 4.00× |

**We do not claim a point estimate.** Allele 2's output is unmeasured — it is precisely
what experiment 1 measures — so publishing "35%" as a finding would be inventing the one
input the whole model turns on. What the table establishes is the thing that actually
chooses a modality: **the gap to close is a shortfall, not a doubling.** Even pessimistic
values need only a small multiple. That is in range for a drug that raises abundance, and
it means nothing has to invent a new allele.

If experiment 1 finds abundance **normal**, this genotype sits at 50%, the defect is
function rather than abundance, and everything below is retired in favour of a
checkpoint-activity assay. The model is built so that outcome is visible.

---

## 1 · NAD⁺ precursors — nicotinamide mononucleotide, nicotinamide riboside

**The lead candidate, and the only one with in-vivo evidence in this gene.**

North et al. asked why BubR1 declines with age and found the answer is **declining NAD⁺**.
Mechanism: **SIRT2 keeps BubR1's lysine-668 deacetylated**, a state that preserves BubR1
abundance, and the acetyltransferase **CBP** opposes it. Two results matter to us
(EMBO J 2014, [10.15252/embj.201386907](https://doi.org/10.15252/embj.201386907)):

- **Treating mice with the NAD⁺ precursor NMN increased BubR1 abundance in vivo.**
- **Overexpressing SIRT2 in BubR1-hypomorphic mice increased median lifespan**, with a
  greater effect in males. Those hypomorphic mice are the accepted model of this disease —
  BubR1 insufficiency "induces progeroid phenotypes in both mice and children with mosaic
  variegated aneuploidy syndrome."

So there is a drug class that raises the exact protein we need to raise, in a living
animal, and a genetic version of the same intervention extended life in the mouse model of
this disease.

**The non-obvious corollary: do not reach for an HDAC inhibitor.** The two acetylation
sites on BubR1 pull in opposite directions. Acetylation at **K250** by PCAF *stabilises*
BubR1 by blocking APC/C–Cdc20 degradation (Choi 2009,
[10.1038/emboj.2009.123](https://doi.org/10.1038/emboj.2009.123)). Acetylation at **K668**
by CBP *destabilises* it, which is why SIRT2's deacetylation preserves it. A drug that
raises acetylation broadly therefore pushes both switches at once and the net effect on
BubR1 is unpredictable — it could lower it. The NAD⁺/sirtuin route acts on K668
specifically. This is the single clearest reason to prefer one mechanism over the obvious
one, and it is only visible if you read both papers.

**Used in rare disease before? Yes, including in a cancer-predisposition syndrome, and
including at n=1.** Of 153 registered NAD⁺-precursor trials:

| trial | disease | design |
|---|---|---|
| NCT03789175 | **Li-Fraumeni syndrome** (germline *TP53*) | NR, Phase 1/2, **n=1**, NIH/NHLBI, completed |
| NCT07572825 | DHDDS-CDG (congenital disorder of glycosylation) | NMN, Phase 1, n=8, off-label, Mayo |
| NCT06280482 | Smooth muscle dysfunction syndrome | NR, Phase 1, n=15, UTHealth |
| NCT05344404 | Parkinson's (NR-SAFE) | high-dose safety |

**NCT03789175 is the template for what we would propose, and it has already been run.**
Its logic: a patient with a rare germline cancer-predisposition syndrome had a measurable
cellular deficit; **NR rescued that deficit in the patient's own fibroblasts in vitro**;
that in-vitro rescue justified a single-patient in-vivo study at NIH, read out on a
quantitative mechanistic biomarker rather than a clinical endpoint. Same drug class, same
category of disease, same cell-first order of operations.

**What we are not claiming.** North's abstract does not state the magnitude of the NMN
effect on BubR1, and the lifespan result came from genetic SIRT2 overexpression, not from
NMN. The abundance effect was shown in aged wild-type animals, not in an MVA genotype.
Most importantly, **it is unknown whether a misfolding-prone mutant responds like
wild-type protein** — a mutant degraded for reasons unrelated to K668 may not respond at
all. That is exactly the question experiment 2 asks, and it is the reason this is a
candidate rather than a recommendation.

## 2 · APC/C–Cdc20 inhibition — on-target, unusable

Mechanistically the most direct option: APC/C–Cdc20 is the ligase that degrades BubR1
(Choi 2009), so inhibiting it would raise BubR1. Research tools exist.

**Rejected, with a reason.** APC/C–Cdc20 is required for every mitosis. Inhibiting it
arrests dividing cells, which is the opposite of what a child with a growth-restricted,
proliferation-dependent phenotype needs. We list it because it is the obvious
mechanism-first answer and it should be visibly considered and visibly discarded.

The same caution scales down to the lead candidate: Choi showed the acetyl-mimetic K250Q
**markedly delayed chromosome segregation.** Too much BubR1 stalls mitosis. This is a
dose-finding problem in both directions, not a switch to flip.

## 3 · Readthrough agents — right class, wrong allele for this child

Ataluren (conditional approval elsewhere for Duchenne), aminoglycosides such as G418, and
anticodon-edited tRNAs each raise protein from nonsense alleles by orthogonal mechanisms.

For allele 1 they are handicapped by construction: readthrough needs a transcript, and
this transcript is destroyed 748 nt from the last junction. Rescuing it also requires
attenuating NMD, which is essential — the dangerous half. And Bhat et al. showed ataluren
works by competitively inhibiting the release factor complex, with **the stop codon's own
identity and adjacent sequence determining whether it works at all**
([10.1093/nar/gkaf216](https://doi.org/10.1093/nar/gkaf216)).

**But this class is the right answer for 44 other alleles** — the ones in our map whose
transcript survives a truncating lesion. That is the map earning its keep: it tells you
which children belong in which modality.

## 4 · Senolytics, mTORC1 inhibition, p53/p21 modulation — downstream

Sieben 2020 found sarcopenia predisposition correlating with **mTORC1 hyperactivity** and
senescence-secretory involvement in muscle. Baker 2013 showed p53 delays muscle and fat
decline via p21 — while **p21 promotes lens senescence and cataract**
([10.1016/j.celrep.2013.03.028](https://doi.org/10.1016/j.celrep.2013.03.028)).

So the downstream response is tissue-specific and **bidirectional**: blanket senescence
targeting would help some tissues and harm others. And none of it prevents
mis-segregation. These treat the damage, not the dosage. Worth naming because they are the
easiest things to propose and the furthest from the cause.

---

## The ranking, and why

| | candidate | in-vivo evidence in *BUB1B* | in humans | reaches this genotype |
|---|---|---|---|---|
| **1** | NAD⁺ precursor (NMN/NR) | NMN raises BubR1 abundance; SIRT2 extends hypomorph lifespan | extensively, incl. rare disease and n=1 | **yes, via allele 2** |
| 2 | APC/C–Cdc20 inhibition | ligase identified | no | yes, but arrests mitosis |
| 3 | Readthrough | none for this gene | ataluren conditionally approved | no — 44 other alleles |
| 4 | Senolytic / mTORC1 | pathways implicated | yes, other diseases | treats consequence only |
| — | Splice-modulating ASO (upregulation) | **no target found** — see below | zorevunersen in Phase 3 | **not on current evidence** |

### Why the splice-modulating ASO route is listed but not ranked

It was briefly our lead candidate: the required effect size (~1.4×) matches what flux
redirection delivers, it is gene-specific, and it would act on allele 2. We tested it and
it failed (`SPLICE-ARCHITECTURE.md`, correction **C45**).

Zorevunersen works by blocking *SCN1A*'s poison exon 20N — a cassette whose inclusion
**frameshifts** the message. *BUB1B*'s only decay-exclusive cassette exon is **54 bp,
divisible by three, enters in frame +0 and contains no stop codon**: including it would
insert 18 residues and leave the protein full-length. It cannot poison anything. The same
method recovers SCN1A's 64 bp frameshifting exon from annotation alone, with no hint of
where to look, so the negative is interpretable rather than merely absent.

*BUB1B* has **more** non-productive annotation than *SCN1A* (39% vs 20% of transcripts) and
**less** targetable structure (zero frameshifting cassettes vs one). The route stays on
the list because annotation is not RNA-seq and exon 20N was itself found by sequencing —
an RNA-seq search of a relevant tissue could still find what we cannot. That is future
work, not a candidate.

**The recommendation.** Not "give this child NMN" — nobody has measured whether allele 2's
protein responds, and the dose window is bounded on both sides. The recommendation is the
order of operations that the Li-Fraumeni n=1 already validated: **measure the deficit in
patient-derived cells, test whether an NAD⁺ precursor rescues it in those same cells, and
only then consider a single-patient study with a mechanistic readout.** Step one is a
western blot.

That is a cheap, fast, falsifiable path to an answer in a disease where, at present, there
is no path at all.
