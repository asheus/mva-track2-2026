# Which approach is best — and five we had not considered

*Ranked against a stated decision, with a kill criterion for each. Two of the five new
approaches came out of one UniProt query that also weakened a third.*

*According to PubMed for the literature; UniProt O60566, Ensembl, GTEx and gnomAD for the
annotations, retrieved 21 Oct 2026.*

## First, the decision the ranking serves

"Best" is meaningless without a decision. Ours is narrow: **what should be done next, with
no wet lab and under two days, by people who cannot run a trial?** Under that decision the
ranking is dominated not by which approach is most likely to cure, but by **which claim
can be killed most cheaply** — because every candidate below rests on one unmeasured
assumption, and that assumption is the same for most of them.

## The verdict, in three parts

**Best approach on the merits: trans-splicing of the endogenous pre-mRNA.**
It is the only modality that reaches allele 1, because NMD destroys mature mRNA while
trans-splicing acts on pre-mRNA before export. It inherits the cell-cycle waveform rather
than having to manufacture it. It is mutation-agnostic, so one molecule serves the whole
map rather than this genotype alone. And the precedent is exact in shape: SMaRT applied to
*CTNNB1* haploinsufficiency, chosen explicitly because the gene is dosage-sensitive and
needs an approach that preserves endogenous regulation. The bar is **23–38% efficiency**,
which is demanding for SMaRT and is the reason it is not also the best bet today.

**Best bet today: the NAD⁺ precursor route.**
It is the only class with in-vivo evidence of raising *this* protein (NMN increases BubR1
abundance; SIRT2 overexpression extends lifespan in the BubR1-hypomorphic mouse), it is
already in humans including an n-of-1 in a germline cancer-predisposition syndrome, and
the K668 mechanism gives a reason to prefer it over a blunt HDAC inhibitor. It now carries
one extra obligation from the waveform analysis: because it works by slowing degradation,
and degradation is the timed event, **mitotic timing must be measured alongside
abundance.**

**Best next action, and the real answer: test whether the allele-2 thesis is even right.**
Everything above assumes p.Asn1002Lys reduces BubR1 *abundance*. One UniProt query put a
serious competing hypothesis on the table (below). The cheapest decisive move is not to
pursue any therapy — it is to add two lanes to experiment 1.

## Five approaches we had not considered

### 1 · N1002K sits six residues from a PLK1 phosphosite — the defect may be signalling, not abundance

UniProt annotates **Thr1008 as a phosphothreonine, phosphorylated by PLK1**. Our variant is
at 1002. A new buried positive charge six residues away could perturb that site or PLK1's
docking on it.

This is not a refinement of our thesis — it **competes with it**. If N1002K abolishes
T1008 phosphorylation while leaving abundance normal, then the defect is a signalling
defect, the entire abundance arm is misdirected, and every candidate ranked above is
aimed at the wrong variable for this allele.

**Kill criterion:** phospho-specific blot for T1008 in N1002K versus wild type. Normal
phosphorylation and reduced abundance → our thesis stands. Lost phosphorylation and normal
abundance → the thesis is wrong. Cost: one extra antibody on an experiment already
planned.

### 2 · A pharmacological chaperone against the pseudokinase pocket — the literal Fabry mechanism

Migalastat works by binding α-galactosidase A's **active site** and stabilising the fold.
BubR1's pseudokinase domain (766–1050) is usually described as catalytically dead, which
invites the assumption that it has no pocket. UniProt annotates **binding sites at 772–780
and 795** inside that domain — the pocket is annotated, not hypothetical, and pseudokinases
frequently retain nucleotide binding.

N1002K sits *inside* this domain, which is exactly the situation migalastat addresses: a
misfolded-but-present protein with a bindable pocket in the affected domain.

**Kill criterion:** pocket detection on the AlphaFold model restricted to 766–1050. A
pocket with no enclosed volume, or one that does not contact the 1002 neighbourhood, kills
it.

> **RUN 21 Oct 2026 — NOT EVALUABLE (`POCKET-SCAN.md`).** The first run passed the
> criterion: a pocket reaching residue 1002. It was an artifact — 12,879 Å³, lining more
> of the domain than the domain contains, because scanning the domain in isolation left
> its interface with the rest of the protein open to vacuum. With occlusion fixed and an
> artifact gate added, the positive control **fails** at every threshold. No validated
> detector is installable here, and no experimental structure of 766–1050 exists above
> 3.8 Å. The obstacle is harder than the criterion I wrote: it needs a structure that does
> not exist.

### 3 · The mutation installs a lysine — a candidate ubiquitin acceptor

Asparagine → **lysine** is not only a charge change. Lysine is the residue ubiquitin
conjugates to, and position 1002 sits in a lysine-rich stretch (K979, K988, K995). If an
E3 uses the new lysine, abundance falls for a reason unrelated to folding.

**Status, stated honestly: the external check did not support this.** UniProt annotates
**no ubiquitination sites anywhere on BubR1**, despite Choi 2009 demonstrating APC/C–Cdc20
ubiquitinates it — so the annotation is incomplete rather than contradicting us, and the
hypothesis is unsupported rather than refuted. It earns its place only because the
discriminator is nearly free.

**Kill criterion:** add an **N1002R** lane. Arginine matches lysine's +1 charge and bulk
but cannot accept ubiquitin. If K is unstable and R is stable, the defect is
ubiquitination. If both are unstable, it is the buried charge, as we assume. One extra
construct.

### 4 · Mosaic selection means partial correction compounds

Our efficiency arithmetic assumes a correction must be *held* at 23–38%. But MVA is mosaic
and aneuploid cells are less fit — which is plausibly why these children survive at all. A
corrected cell has a **proliferative advantage over its aneuploid neighbours**, so a
partial correction is a seed, not a ceiling.

This changes the trans-splicing bar from "maintain a third of transcripts corrected" to
"correct enough cells to start an expanding population," which is a materially easier
target and is how corrected haematopoietic cells behave in other gene therapies.

**Where it fails, and this is most of the body:** selection needs division. It helps blood,
gut and skin; it does nothing in post-mitotic tissue, and the brain phenotype is already
accrued. So this lowers the bar for cancer risk and marrow function, not for microcephaly.

**Kill criterion:** measure whether euploid cells actually outgrow aneuploid ones in
patient-derived cultures. If the aneuploid fraction is stable over passages, there is no
selection to exploit.

### 5 · Give the weak checkpoint more time instead of more protein

Every approach above raises BubR1. The checkpoint fails because its signal is too weak to
hold anaphase — but that is a race, and the other side of a race is **duration**.
Lengthening prometaphase lets an insufficient signal accumulate past threshold.

This touches BubR1 not at all, which is its one decisive advantage: **it is the only
approach on any of our lists that could help the 280 alleles that make no protein.**
Every other candidate is blind to them by construction.

**Why it is ranked last anyway:** agents that modulate mitotic duration are cytotoxics, the
therapeutic window in a growing child is unknown and plausibly absent, and in a
cancer-predisposition syndrome a drug that perturbs mitosis carries obvious risk. It is
listed because it is the only idea that escapes the eligibility boundary, and because an
approach that is conceptually sound and practically dangerous should be written down and
argued against rather than quietly omitted.

**Kill criterion:** in patient-derived cells, does modest prometaphase lengthening reduce
mis-segregation? If aneuploidy is unchanged when mitosis is slowed, the race model is wrong
for this genotype.

## The ranking

| | approach | reaches allele 1 | inherits waveform | serves all alleles | cheapest kill |
|---|---|---|---|---|---|
| 1 | trans-splicing (SMaRT) | **yes** | **yes** | mutation-agnostic | pre-mRNA quantification |
| 2 | NAD⁺ precursor | no | partly | protein-making only | abundance + mitotic timing |
| 3 | trans-RNA on endogenous mRNA | no | yes | transcript-making only | — |
| 4 | pseudokinase chaperone *(new)* | no | yes | missense only | pocket detection, runnable now |
| 5 | checkpoint timing *(new)* | **yes** | n/a | **all 2,536** | aneuploidy under slowed mitosis |

And above all of them, not as a therapy but as the next thing to do: **the T1008
phospho-blot and the N1002R lane.** Two additions to an experiment already designed, either
of which can invalidate the ranking above before anyone spends a year on it.

That is the honest answer to "which is best": the best approach is trans-splicing, the best
bet today is the NAD⁺ route, and the best *action* is the cheap test that could show both
are aimed at the wrong variable.
