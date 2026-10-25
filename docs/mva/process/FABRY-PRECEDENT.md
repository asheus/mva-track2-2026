# The Fabry precedent: what an eligibility map looks like when it is real

*Every number here is produced by `apps/api/scripts/mva/fabry_precedent.py` from the
Galafold prescribing information (sha256 `ca9b696f…`, retrieved 21 Oct 2026) or cited to
Benjamin ER et al., Genet Med 2017;19(4):430-438,
[doi:10.1038/gim.2016.122](https://doi.org/10.1038/gim.2016.122). The script asserts its
own central claim on the raw table text and fails if it stops being true.*

We claim that for a drug which works by stabilising a protein, the first question is not
*which drug* but *does this allele make any protein to stabilise*. If that is right it
should already be visible in an approved drug. It is. This file is what we found when we
checked, including the two places the precedent argues **against** us.

## How the drug works

Migalastat (Galafold) is a small molecule that binds the active site of
α-galactosidase A. Certain *GLA* variants produce an enzyme that is abnormally folded and
unstable **but still catalytically competent**. Migalastat binds and stabilises that
mutant enzyme, restoring its trafficking to the lysosome; at lysosomal pH and high
substrate concentration it dissociates, freeing the enzyme to clear its substrates
(label §12.1). It is 123 mg orally every other day — a pill, not an infusion, which is
why it matters commercially as well as clinically.

The mechanism contains its own limit. **A chaperone has nothing to bind if the protein
was never made.**

## How eligibility is determined

Six hundred Fabry-causing mutations were expressed in HEK-293 cells and assayed for
α-Gal A activity with and without 10 µM migalastat. A variant was called **amenable** on
a written, quantitative, two-part criterion: a relative increase of **≥20%** over
pre-treatment activity **and** an absolute increase of **≥3% of wild-type**. Two hundred
and sixty-eight of the 600 passed. Against in vivo white-blood-cell response in phase II
and III patients, the assay's sensitivity, specificity and positive and negative
predictive values were all **≥0.875** (Benjamin 2017).

That assay is GLP-validated and is named in the label as the GLP HEK/Migalastat
Amenability Assay. The eligible alleles are enumerated in **Table 2** of the label.

## How it is used

The indication is not "Fabry disease". It is:

> adults with a confirmed diagnosis of Fabry disease **and an amenable galactosidase
> alpha gene (GLA) variant based on in vitro assay data**

A genotype gate, written into the indication, with the eligible alleles listed. Three
details of how the label handles that gate are worth copying exactly:

- **Amenability is not pathogenicity, and the label says so twice.** "The in vitro assay
  did not test whether a GLA variant causes Fabry disease or not," and inclusion in
  Table 2 "does not reflect interpretation of their clinical significance." A clinician
  must separately judge the variant pathogenic before treating.
- **Absence from the table means two different things, and the label refuses to collapse
  them.** "If a GLA variant does not appear in Table 2, it is either non-amenable (if
  tested) **or has not been tested**." This is the same absence-vs-ignorance discipline we
  are held to; it is reassuring to find it enforced on a drug label.
- **The table is maintained.** 268 amenable at publication; **376** distinct entries in
  the current label.

## What kind of allele is ever eligible

This is the measurement we came for. Of the **376** entries in Table 2:

| kind | n |
|---|---|
| plain missense | 357 |
| multi-variant alleles (all missense) | 4 |
| small in-frame indels — protein still made | 3 |
| rows whose protein column wrapped in the PDF | 12 |
| **truncating — nonsense, frameshift, splice** | **0** |

A scan of the raw table text finds no `Ter`, no `fs`, no `*`, no `splice`, no `X`+digit.
**Every allele eligible for the one approved folding-rescue drug makes protein.** Not as
a curation preference — as a consequence of the mechanism.

And the clinical arm closes the loop. Of 67 patients in Study 1, the **17 with
non-amenable variants had no change from baseline** in kidney GL-3 inclusions after six
months. The drug did nothing in the ineligible, exactly as predicted. Eligibility triage
is not bookkeeping; it is the difference between a treatment and six months of nothing.

## Mapping it onto BUB1B

| | Fabry / *GLA* | MVA / *BUB1B* (ours) |
|---|---|---|
| alleles classified | 376 on the label | 2,536 in `allele_lookup.tsv` |
| basis | GLP-validated HEK-293 assay | predicted, per-row experiment named |
| threshold | ≥20% relative **and** ≥3% of wild-type | splice tier calibrated on a sealed split; folding axis validated in 3 other proteins, **not** in BUB1B |
| eligible alleles make protein | 376 / 376 | **44** predicted to leave protein; **280** predicted to lose the transcript |
| predictive value | ≥0.875 vs in vivo | unmeasured — no BUB1B multiplexed assay exists anywhere |
| used for | prescribing decisions | shortlisting experiments |

The structural claim transfers cleanly. The confidence does not, and we say so in every
row: ours is predicted, theirs is measured.

## Where the precedent argues against us

Two findings cut the other way. They are the most useful things in this file.

**1. The drug separated from placebo in hemizygous males, not in heterozygous females.**
Study 1, ≥50% reduction in GL-3 inclusions: males **5/7 (71%) vs 4/9 (44%)**, median
change −1.10 vs −0.03. Females **8/18 (44%) vs 5/11 (46%)** — no separation at all.

Our proband is a compound heterozygote with one null allele (p.Leu737Ter) and one
missense (p.Asn1002Lys). A chaperone-style argument reaches **one** of their two alleles.
The nearest approved precedent for "rescue one allele of two" is the Fabry female, and
on the histology endpoint it did not work.

That reading is confounded, and the label shows the confounder itself: females had far
less substrate to clear (21 of the 28 low-baseline patients were female). But we do not
get to use the confounder as a rescue and not as a limit. The honest statement is that
**single-allele rescue is unproven in the one place it has been tried at this endpoint**,
and that is now in the counter-argument document.

**2. The effect existed only where there was burden to reverse.** Stratified by baseline
GL-3: high burden (≥0.3) **78% vs 25%**; low burden (<0.3) **38% vs 58%** — nothing, or
worse. The drug worked where there was accumulated substrate to clear and showed nothing
where there was not.

This chooses the endpoint for any MVA trial, and it rules out the obvious one. Microcephaly
and growth restriction are damage already accrued during development — the low-baseline
case, with no headroom, where even an approved drug showed nothing. **Ongoing
mis-segregation is the high-baseline case**: aneuploid-cell fraction in dividing cells is
continuously generated, measurable, and has headroom. Any honest MVA endpoint is
prospective and cellular, not developmental — which is harder to explain to a family and
is the right thing to say anyway.

## What a BUB1B equivalent would require

Not a drug. The precedent's order of operations was: assay → threshold → table →
predictive validation → indication. The table came **before** the indication, and the
validation came before both.

*GLA* also had an advantage BUB1B does not: a monomeric lysosomal enzyme with a direct
activity readout in cell lysate. BubR1 is a checkpoint scaffold in a multiprotein complex
with no single enzymatic number to measure, so a BUB1B amenability assay would have to
pick its readout — abundance by western, kinetochore localisation, or aneuploidy rate —
and defend it. That choice is the first real experiment, and nobody has made it.

So the deliverable our map is a candidate for is the **first** step, not the last: the
shortlist that says which alleles are worth putting in an assay, and which question each
one answers. On the Fabry timeline that step preceded an approved drug by years.

**The one-sentence version.** The only approved folding-rescue drug in a lysosomal disease
is prescribed off a per-allele eligibility table in which not one of 376 eligible alleles
is truncating, and in which the 17 ineligible patients got nothing — and for *BUB1B*, a
gene where 280 of 2,536 catalogued alleles are predicted to lose the transcript outright,
no such table exists until this one.
