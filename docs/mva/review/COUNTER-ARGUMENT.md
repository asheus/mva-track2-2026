# The case against our own thesis

Written deliberately, as the strongest honest argument that our Track 2 submission is
wrong. Nothing here is a strawman and nothing is rebutted. Where we have an answer it is
given in one line and marked; where we do not, that is the point.

Our thesis, stated plainly so it can be attacked: *the proband makes some BubR1 from
allele 2 (`p.Asn1002Lys`, a missense in the folded pseudokinase core); that protein is
likely destabilised but present; and a proteostasis approach could raise its abundance
toward the threshold where the spindle checkpoint functions.*

---

## 1. Allele 2 may make no usable protein at all, and then there is nothing to rescue

Everything rests on N1002K being a **hypomorph** rather than a functional null. Our
evidence that it makes protein is entirely computational: RSA 14%, pLDDT 91, and a
two-class finding built on **5 pathogenic variants**. There is no western blot, no
abundance assay, and — now established — **no multiplexed data for BUB1B anywhere**: MaveDB's
2,898 target genes contain no BUB1B and nothing else in the spindle checkpoint (C41).

If N1002K is a null, the thesis is not weakened, it is void. We cannot presently exclude
that. The honest position is that a stabilisation strategy is conditional on a measurement
nobody has made, and the first experiment any sane programme runs is that western blot.

## 2. The threshold may be out of reach of what proteostasis drugs actually achieve

Matsuura 2006 concludes that a **>50% decrease** in BubR1 expression or activity is enough
to cause this syndrome, measured by RT-PCR and western in patients whose transcripts showed
only a *"modest decrease"* (C33a). The proband has a nonsense allele contributing ~nothing,
so the entire burden sits on one destabilised copy.

Fabry's amenability criterion — the precedent we lean on most — is **≥1.2-fold over baseline
AND ≥3% absolute increase** in wild-type activity. That is the bar a *registered* drug with
a *validated assay* clears, and **most variants are not amenable**. A 1.2–2× rise on a
single destabilised allele that starts far below 50% may simply not reach the threshold.
Nothing in our work shows that it would, because we have no baseline number to multiply.

## 3. The in-syndrome evidence is actively against system-level intervention

This is the strongest argument against us and it comes from our own files (C28). Splitting
every reported MVA intervention by what it targeted:

**Worked — all treated a *consequence*:** tamoxifen (complete sustained remission); surgery
alone (free of new pathology since 2014); renal transplant under ciclosporin (reached
20-year follow-up).

**Failed — all tried to fix the *system*:** HSCT in MVA1, the same gene as our proband —
engrafted, cleared the monosomy 7 clone, **then graft rejection at day +47 and death at day
+156**; growth hormone, ineffective, with the authors writing *"had this been known, growth
hormone might have not been prescribed"*; G-CSF and romiplostim, *"no response"*;
valproate + levetiracetam, seizures continued.

A proteostasis drug is a system-level intervention. The one case that achieved its stated
mechanistic goal in this syndrome **killed the patient with a complication belonging to the
intervention rather than the disease.** We have no in-syndrome example of a system-level
intervention helping anyone.

## 4. Arimoclomol's own clinical record does not support optimism

It is approved for Niemann-Pick type C and has **failed** in ALS and in sporadic inclusion
body myositis. Its mechanism amplifies an existing heat-shock response rather than creating
one, so in a cell that is not proteostatically stressed it may do nothing at all. We have
no evidence that a BUB1B-hypomorphic cell is stressed in the way the drug requires. Our own
C5 already retracted the 4-PBA reasoning once for counting HDAC activity as favourable.

## 5. The map is a prediction, and at the tier that finds most variants it is mostly wrong

Measured on 946 assayed splice-disrupting variants with a sealed evaluation (C40):

| tier | sensitivity | specificity | precision at the true base rate |
|---|---|---|---|
| `call` (0.16) | 0.392 | 0.986 | 0.48 |
| `candidate` (0.02) | 0.793 | 0.872 | **0.17** |

At the screening tier **roughly four of every five calls are wrong**, and at the confident
tier we catch under 40% of real disruption. Fabry's equivalent map is a **GLP-validated
assay**, run per variant — 600 expressed, 268 amenable, 376 on the current label —
used for actual drug eligibility. Ours is a shortlist. A
clinician handed the candidate tier would be reading mostly noise, and we say so, but
saying so does not make it more useful.

And the calibration itself is borrowed: MFASS is a **minigene reporter in a cell line**. It
measures exon recognition in a construct, not endogenous splicing at the native locus. The
sensitivity figures are the ones that caveat bears on hardest.

## 6. Part of our own structural reasoning has just lost its support

C41 tested the two-class mechanism on measured abundance. **Buried charge introduction
passed** in three independent assays. **Volume change failed in all three**, and reversed
in NUDT15. N1002K is both a buried charge introduction and a +54.5 Å³ volume increase, so
half of the structural case for it is now externally unsupported.

Then C43 calibrated the missense arm and **both of its pre-stated tests failed**. The
buried-charge axis does not reach significance in *BUB1B's own* labelled variants — 2 of 19
pathogenic missense against 2 of 100 benign, OR 5.76, p = 0.1193 — so it is validated in
other proteins and **not demonstrated in this one**. And AlphaMissense ranks only 1 of 5
measured-destabilising panel variants above both measured-normal ones, with `Q921H`
(normal) outscoring four of the five, so **N1002K's 0.9229 is withdrawn as evidence**.

What remains supporting allele 2: a mechanism validated in three other proteins, a single
lost hydrogen bond inferred from a predicted structure with zero experimental coverage, and
a posterior over six comparators whose lower bound is 0.44. That is thinner than it looked
a day ago, and we found all of it by testing our own claims.

## 7. Surveillance already dominates, and it is standard of care

Intensive surveillance moves survival in comparable cancer-predisposition syndromes from
**59.6% to 88.9%**. That is a large, demonstrated, available effect. Every therapeutic idea
in our submission is, on present evidence, **worse in expectation than what this child
should already be receiving** — and the in-syndrome record in §3 says the successful
interventions were the ones that removed tumours rather than repaired the checkpoint.

A fair reading is that our contribution is a *map and a method*, not a treatment, and that
the treatment framing overstates what we have.

---

## What would change our mind, in order of decisiveness

1. A **western blot or abundance assay on N1002K** — settles §1 outright. Nothing else
   matters more, and nobody has done it.
2. A **dose–response curve for BubR1 abundance vs checkpoint function** in the patient's own
   cells — settles §2 by giving the baseline that the fold-change multiplies.
3. Any **in-syndrome system-level intervention that helped** — would weaken §3, which is
   currently one-sided against us.
4. An **assay rather than a predictor** for splice eligibility — would fix §5, and is what
   Fabry's precedent actually consists of.

## The one claim we would still defend

Not the treatment. The **calibration**: that a variant-eligibility map for a gene with no
functional data should state its own operating characteristics, and that the way to get
them is to benchmark against measured outcomes in other proteins and report the sealed
numbers including the unflattering ones. Both visible competitor submissions declined to
calibrate at all. That is the part of this work we would defend against anyone.

---

## Added 21 Oct 2026, from the Fabry precedent: single-allele rescue is unproven

We went looking for a precedent that would support the eligibility-map framing and found
one (`FABRY-PRECEDENT.md`). It also supplied the sharpest objection yet to the therapeutic
half of our argument, and it belongs here rather than in the part of the report that
makes our case.

Our proband is a compound heterozygote: one null allele (p.Leu737Ter, predicted to lose
its transcript) and one missense (p.Asn1002Lys). Any folding- or abundance-rescue argument
therefore acts on **one of two alleles**, with the other contributing nothing.

The nearest approved test of that situation is the heterozygous Fabry female, where
X-inactivation leaves a substantial fraction of cells expressing only the mutant enzyme.
In Study 1 of the migalastat programme, on the kidney GL-3 histology endpoint:

- males (hemizygous, one allele, all cells mutant): **5/7 (71%) vs 4/9 (44%)** placebo,
  median change −1.10 vs −0.03
- females (heterozygous, mosaic): **8/18 (44%) vs 5/11 (46%)** placebo — **no separation**

Taken at face value, the one approved drug of this class failed to separate from placebo
in the configuration closest to our proband's.

**The confound, stated and then declined as a defence.** Females in that study had much
lower baseline substrate burden — 21 of the 28 low-baseline patients were female — and the
drug showed no effect in the low-baseline stratum regardless of sex (38% vs 58%). So the
female null result may be a burden effect rather than a dosage effect. We are not entitled
to that reading as a rescue while also citing the high-baseline stratum (78% vs 25%) as
evidence the mechanism works. Either the stratification is informative or it is not.

**What survives.** Not that single-allele rescue fails — the evidence does not support
that either. What survives is that **it is untested at a clinical endpoint**, and that our
report must not imply otherwise. It also means the question *"is one rescued allele enough
to clear the disease threshold?"* is not a detail to be settled later; on this evidence it
is the central unknown of the therapeutic half, and it is upstream of any molecule.

The experiment already named in C42c — N1002K vs N1002S vs wild-type abundance — does not
answer it. It asks whether the allele's protein is reduced at all. The dosage question
needs a second experiment that nobody has designed for this gene, and we should say that
plainly rather than let the first experiment stand in for both.

---

## Added 21 Oct 2026: allelic effects beyond protein level

Our pitch treats BubR1 as a dosage problem. The strongest published evidence that this is
*incomplete* comes from the same paper we cite in support of it.

Sieben et al. engineered an allelic series mimicking real MVA genotypes and compared them
(J Clin Invest 2020, [10.1172/JCI126863](https://doi.org/10.1172/JCI126863)). The finding
that cuts against us:

> …although these mice had a reduction in total BUBR1 and spectrum of MVA phenotypes
> similar to that of BubR1^H/H mice, several progeroid pathologies were **attenuated in
> severity**…

Matched total BubR1. Similar aneuploidy. **Different severity.** Their conclusion is
explicit: "BUBR1 allelic effects beyond protein level and aneuploidy contribute to disease
heterogeneity."

**What this costs us.** The clean version of our argument — restore the amount of protein,
move the phenotype — is not what the best in vivo genetics of this gene shows. Two alleles
producing the same quantity of BubR1 can produce different disease. So raising abundance
from p.Asn1002Lys may not be equivalent to raising abundance generally, and the quantity
we would be measuring in the settling experiment is not guaranteed to be the quantity that
matters.

**What survives.** The dose–response itself is not in question: graded reduction gives
graded aneuploidy and senescence (Baker 2004). What Sieben adds is that dose is *not the
only* variable, not that it is the wrong one. Our hypothesis therefore needs a third step
it did not previously have, and which is now in the pitch: after measuring abundance, and
after showing the loss is degradation-dependent, **measure mis-segregation rather than
protein.** If allelic identity matters beyond level, only a functional readout will show
it, and we should not let a western blot stand in for one.

It also argues against a specific shortcut we might have been tempted by: using total
BubR1 as a surrogate endpoint. On this evidence total BubR1 is a poor surrogate, which
makes aneuploid-cell fraction the endpoint by elimination as well as by the Fabry
burden argument.
