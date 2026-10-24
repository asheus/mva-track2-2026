# Eligibility precedes therapy

### A per-allele mechanism map for *BUB1B*, and what it says to do for one child

---

## The claim

Mosaic variegated aneuploidy is a **dosage disease**. In mice, reducing BubR1 in graded
steps produces aneuploidy and senescence in graded steps (Baker 2004,
[10.1038/ng1382](https://doi.org/10.1038/ng1382)). The amount of functional BubR1 is
therefore the therapeutic variable, and the first question about any *BUB1B* allele is not
*which drug* but **how much protein does this allele leave behind**.

Nobody has asked that question systematically. We asked it for all **2,536** catalogued
*BUB1B* alleles, and the answer splits them into groups that need completely different
modalities. **280 lose the transcript entirely.** For those, every folding-, stabilising-
or chaperone-style approach is mechanically inert — not unlikely, *inert*.

That is not a hypothesis. It is the operating principle of the one approved drug that
works this way, and its label proves it: of **376** alleles eligible for migalastat in
Fabry disease, **zero are truncating**, and the 17 patients in its pivotal study who
carried ineligible alleles had **no change from baseline** after six months
(`FABRY-PRECEDENT.md`). Giving a protein-stabilising drug to a patient whose allele makes
no protein is not a long shot. It is six months of nothing.

So the deliverable is the map, and the map has a verdict for this child.

---

## The two alleles, resolved

**Allele 1 — p.Leu737Ter (c.2210T>G).** We resolved its exact molecular identity against
the canonical CDS:

- the codon is `TTA` → `TGA`: a **UGA (opal)** stop, in the context `CCAGAG|TGA|AGTGCC`
- it sits **748 nucleotides upstream of the last exon–exon junction** — far past the
  ~50 nt boundary, so it is a **canonical nonsense-mediated decay substrate**

Prediction: **the transcript is degraded. This allele contributes no protein.**

**Allele 2 — p.Asn1002Lys (c.3006T>G).** A missense change in the pseudokinase domain.
Asn1002 is **buried** (relative solvent accessibility 13.7%) and donates a hydrogen bond
through OD1 to the backbone nitrogen of Trp978 — an acceptor contact that lysine cannot
replace. It also buries a new positive charge at a buried position, the one axis we
validated against measured abundance in three other proteins.

Prediction: **protein is made, and its abundance is the open question.**

One allele makes nothing. One allele makes something. That asymmetry decides everything
that follows.

---

## How much protein is left, and how much we need back

The literature gives the threshold. Matsuura et al. studied seven families with this
disease and concluded that **"> 50% decrease in expression (or activity) of BubR1 is
involved in the PCS syndrome"** — disease appears below roughly half of normal
([10.1002/ajmg.a.31069](https://doi.org/10.1002/ajmg.a.31069)).

The arithmetic then follows, and it is unusually clean. Allele 1 contributes **zero** —
fixed, not assumed, because its transcript is a canonical NMD substrate *and* a protein
ending at residue 737 of 1,050 would lack the whole pseudokinase domain either way. So
allele 2 is the only source, and **this genotype's ceiling is 50% — precisely the
threshold.** The child is affected, so allele 2 delivers less than a full allele's worth
and the true value sits strictly below it (`dosage_model.py`):

| if allele 2 delivers | total functional BubR1 | fold-increase needed to reach 50% |
|---|---|---|
| 100% | 50.0% — *at* threshold | 1.00× |
| 85% | 42.5% | 1.18× |
| **70%** | **35.0%** | **1.43×** |
| 55% | 27.5% | 1.82× |
| 40% | 20.0% | 2.50× |

**We publish no point estimate.** Allele 2's output is unmeasured — it is what experiment 1
measures — so quoting "35%" as a finding would be inventing the one input the model turns
on. What the table settles is the question that actually chooses a modality: **the gap to
close is a shortfall, not a doubling.** A small multiple suffices, which is within reach
of a drug that raises abundance and requires inventing no new allele.

And the dosage frame itself is not ours. In the same 2006 paper, transferring a
chromosome 15 carrying *BUB1B* into patient cells **restored normal BubR1 levels, restored
kinetochore localisation of p55cdc, and restored the normal response to colcemid.** Put
the dosage back and the cell comes back. Nobody has since asked whether a drug can do what
the chromosome did.

---

## The obvious move is backwards

Faced with a nonsense allele beside a missense allele, the instinct is to chase the
nonsense one. Readthrough is the celebrated modality, a stop codon looks like a cleaner
target than a fold, and the agents exist: ataluren has conditional approval elsewhere,
and aminoglycoside G418 and anticodon-edited tRNAs act through orthogonal mechanisms.

For this child, that instinct is wrong, and the reason is specific rather than general.
**Readthrough needs a transcript to read through.** Allele 1's PTC is 748 nt from the last
junction, so the message is destroyed before any readthrough agent can act on it.
Rescuing it means attenuating NMD as well — and NMD is essential, which makes that the
systemically dangerous half of the combination.

There is a second reason, and it is the sharper one. Bhat 2025 showed that ataluren works
by **competitively inhibiting the release factor complex**, and that **the PTC's own
identity and immediately adjacent sequence determine whether it will work at all** —
patients whose context promotes strong release-factor interaction are predicted to be
*resistant* ([10.1093/nar/gkaf216](https://doi.org/10.1093/nar/gkaf216)). Readthrough
eligibility is therefore allele-specific and computable, exactly like amenability in
Fabry. It has never been computed for this gene.

So readthrough is not a dead end — it is **the right modality for a different 44
children.** Our map finds the alleles whose transcript survives a truncating lesion:
**44 of 2,536**. Those are the readthrough-eligible subset, and allele 1 is not among
them.

**The nonsense allele is the one that looks druggable and isn't. The missense allele is
the one that looks hard and is reachable.**

---

## The lever: degradation, not folding

If allele 2 makes an unstable protein, there are two places to intervene: help it fold, or
stop it being destroyed. Folding would require discovering a BubR1-binding chaperone that
does not exist. Degradation is already mapped.

BubR1 is acetylated at **lysine 250** by PCAF, and that acetylation **blocks
ubiquitin-dependent degradation**. The ligase is **APC/C-Cdc20**. The acetyl-mimetic
K250Q is stabilised against degradation; the acetyl-dead K250R is unstable (Choi 2009,
[10.1038/emboj.2009.123](https://doi.org/10.1038/emboj.2009.123)).

So BubR1 abundance has a published, validated control point — a switch with a known
writer, a known ligase, and mutants in both directions. That is a far better starting
position than a fold with no ligand.

**The therapeutic hypothesis, stated so it can be killed:**

> If p.Asn1002Lys reduces BubR1 abundance rather than its checkpoint activity, then
> reducing the rate at which that protein is degraded will raise functional BubR1 toward
> the threshold — and because the phenotype is graded with dose, partial restoration from
> a single allele should produce partial benefit.

**And a candidate exists for exactly this.** North et al. found that BubR1's decline with
age is caused by declining NAD⁺, that **SIRT2 preserves BubR1 by keeping lysine-668
deacetylated**, and — the two results that matter — that **treating mice with the NAD⁺
precursor NMN increased BubR1 abundance in vivo**, and that **overexpressing SIRT2 in
BubR1-hypomorphic mice increased median lifespan**
([10.15252/embj.201386907](https://doi.org/10.15252/embj.201386907)). Those hypomorphic
mice are the accepted model of this disease.

The non-obvious corollary is a warning: **do not reach for an HDAC inhibitor.** BubR1's
two acetylation sites pull opposite ways — K250 acetylation *stabilises* it, K668
acetylation *destabilises* it — so a drug raising acetylation broadly pushes both switches
and could lower BubR1 on net. The NAD⁺/sirtuin route acts on K668 specifically. Full
ranking and limits in `DRUG-CANDIDATES.md`.

The genetics support the second clause. In the engineered allelic series, the combinations
that survived were the ones retaining partial-function protein: truncating + missense died
prematurely, while low-wild-type + missense was **viable** with MVA features
(Sieben 2020, [10.1172/JCI126863](https://doi.org/10.1172/JCI126863)). Partial protein is
what keeps these children alive, which is the strongest available argument that more of it
helps.

---

## The cost, stated up front

Stabilising BubR1 is not free, and the same paper that names the switch names the price:
**K250Q markedly delayed chromosome segregation.** BubR1 is a checkpoint protein; too much
stalls mitosis. This is a dose-finding problem, not a switch to flip, and any proposal
that ignores that is not serious.

Two further objections we carry rather than rebut, both in `COUNTER-ARGUMENT.md`:

- **Allele identity matters beyond dose.** At matched total BubR1 and matched aneuploidy,
  severity still differed by which alleles produced it (Sieben 2020). A pure dosage model
  is incomplete.
- **Single-allele rescue is unproven at a clinical endpoint.** Migalastat separated from
  placebo in hemizygous males but not in heterozygous females — the configuration closest
  to a compound heterozygote.

And the endpoint is constrained by the same precedent. Migalastat worked only where there
was burden to reverse (78% vs 25% at high baseline; nothing at low baseline). Microcephaly
and growth restriction are damage already accrued — no headroom. **Ongoing
mis-segregation is the only endpoint with headroom**: continuously generated, measurable
as aneuploid-cell fraction in dividing cells. That is harder to explain to a family than a
promise about growth, and it is the honest one.

---

## What settles it

Three experiments, in order, each one cheap enough to run and capable of returning the
answer we don't want.

1. **Is allele 2 an abundance defect at all?** Express N1002K, N1002S and wild-type
   BubR1; blot for protein. N1002S is the internal control — same residue, charge-neutral.
   If N1002K's abundance is normal, the whole thesis for this allele is dead and the
   defect is functional instead.
2. **Is the loss degradation-dependent?** Repeat with the degradation route blocked. If
   abundance recovers, the lever is real; if not, it is a folding or synthesis problem and
   the K250 route is irrelevant.
3. **Does restoring abundance restore the checkpoint — without stalling mitosis?**
   Measure aneuploid-cell fraction, not protein. Protein is the mechanism; mis-segregation
   is the disease. **And measure mitotic timing alongside it**, because the NAD⁺ route
   raises BubR1 by slowing its destruction, and destruction is the timed event that lets
   anaphase begin (`DOSAGE-TIMING.md`).

Every row of our map carries its own version of step 1, which is what makes it a map and
not a list.

---

## The constraint that orders the candidates

BubR1 is not a protein whose level you set. It **oscillates by design** — low in G1,
rising through S and G2, peaking at prometaphase, then **actively destroyed** so anaphase
can begin. The destruction is the signal, and Choi 2009 showed the cost of blocking it: an
acetyl-mimetic BubR1 that resists degradation **markedly delayed chromosome segregation**.

So this genotype has **two** deficits and most proposals treat one. The **amplitude** is
too low, and whatever we add must still **fall away** at anaphase.

> **MeCP2's constraint is a ceiling. BubR1's constraint is a waveform.**

That decides the modality, and the adjacent problem has been solved twice with only one
answer that transfers. Where protein must be supplied exogenously, the Rett field
engineered a limiter into the vector — miRARE, a panel of miRNA binding sites capping
accumulation ([10.1093/brain/awab182](https://doi.org/10.1093/brain/awab182)); reviews are
candid that it limits excess rather than restoring natural regulation. Where the gene can
be acted on in place, nothing needs engineering: nusinersen and risdiplam raise SMN by
correcting *SMN2* splicing, so the protein is made by the patient's own gene on the
patient's own schedule ([10.1159/000517686](https://doi.org/10.1159/000517686)).

| approach | amplitude | shape |
|---|---|---|
| trans-splicing of endogenous pre-mRNA | yes | **inherited** |
| trans-RNA on endogenous mRNA | yes | **inherited** |
| CRISPRa at the native promoter | yes | **inherited** |
| NAD⁺ / degradation route | yes | **partly — it slows the clock itself** |
| circRNA or AAV encoding BubR1 | yes | **must be engineered; nobody has** |

We are not trying to raise a number. We are trying to restore an oscillation whose
collapse is as functional as its peak — which is why the therapy has to act on the
patient's own transcript. Not because endogenous regulation is elegant, but because
reproducing this waveform from outside is an unsolved engineering problem.

---

## Why this scales

The same pipeline that answered this for two alleles answered it for **2,536**, and
assigns every one a transcript-level verdict, a protein-level verdict, an evidence tier,
and the experiment that would settle it. **Rows with no named experiment: 0.**

| | |
|---|---|
| lose the transcript — no protein to stabilise | **280** |
| keep protein despite a truncating lesion — readthrough-eligible | **44** |
| missense, abundance answerable with existing structure | **326** |
| missense, structural context insufficient — assay required | **916** |
| scored for a splice effect, none detected — assess as coding | **718** |
| missense, abundance likely normal — defect expected in function | **252** |
| **total** | **2,536** |

Hand us any *BUB1B* allele and we return its predicted mechanism and the experiment that
would confirm it. On the Fabry timeline, that table preceded an approved drug by years —
and the table came **before** the indication, not after.

---

## What we are not claiming

We are not prescribing a drug. We name NAD⁺ precursors as the lead *candidate* because
they are the only class with in-vivo evidence of raising this protein — but nobody has
measured whether allele 2's mutant protein responds like wild type, the lifespan result
came from genetic SIRT2 overexpression rather than from NMN, and too much BubR1 delays
mitosis. So the proposal is the order of operations, not the molecule: measure the deficit
in patient-derived cells, test rescue in those same cells, and only then consider a
single-patient study with a mechanistic readout. That exact sequence has already been run
for a rare germline cancer-predisposition syndrome — NR in Li-Fraumeni, **n=1**, at NIH
(NCT03789175).

Our map is **predicted, not assayed** — every row says so. MaveDB holds no *BUB1B*
dataset and none for any spindle-checkpoint gene, so no measured ground truth exists for
this gene, which is precisely why the shortlist has value and precisely why it is not a
verdict. No row is an eligibility call for any person, and nothing here is advice about
any individual.

What we are claiming is narrower and we think it is right: **for this genotype the
reachable allele is the missense one, the lever is degradation rather than folding, the
first experiment is a western blot, and 280 of 2,536 children carrying other alleles
cannot be helped this way at all** — which is worth knowing before anyone spends a decade
finding out.
