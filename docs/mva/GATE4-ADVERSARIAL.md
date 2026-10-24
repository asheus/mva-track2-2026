# Gate 4 — adversarial evidence pass on the surviving thesis

Run 10 Sep 2026 over the 13 Gate 3 survivors. Sources retrieved via PubMed.
This is the channel that tries to KILL the thesis rather than support it; a
thesis that survives an honest attack is worth more than one that was never
attacked.

## The attack: senescence is tumour-suppressive, so suppressing it should be harmful

The strongest argument against Arm A is not the immunosuppression worry Gate 3
already caught. It is mechanistic and it is worse:

> Cellular senescence is a tumour-suppressive barrier. A child whose cells
> continuously missegregate chromosomes depends on that barrier. Any drug that
> suppresses senescence biology in such a child could remove a standing defence
> and INCREASE tumour risk — making the whole arm backwards.

The attack has real support. Li et al., *Oncotarget* 2016
([DOI](https://doi.org/10.18632/oncotarget.7864)) conclude that "the direct role
of p53-mediated cell cycle arrest, senescence and apoptosis is to control genomic
stability in vivo," and show cells that cannot arrest accumulate high levels of
aneuploidy after DNA damage. That is precisely the vulnerability an MVA child has.

## Why the thesis survives it: arrest and secretome are separable

The attack conflates two things that the pharmacology separates.

**Senescence ARREST** is the tumour-suppressive part — the damaged cell stops
dividing. **The SASP** is the paracrine inflammatory output of cells that have
already arrested, and it is tumour-*promoting* in the surrounding tissue. Coppé
et al., *PLoS Biology* 2008 ([DOI](https://doi.org/10.1371/journal.pbio.0060301))
show that SASP from **genotoxic-stress-induced** senescence drives
epithelial-mesenchymal transition and invasiveness in premalignant epithelial
cells "by a paracrine mechanism that depended largely on the SASP factors
interleukin (IL)-6 and IL-8." Genotoxic-stress-induced senescence is the state
chronically aneuploid cells occupy, so this is the relevant SASP, not a general one.

An anti-IL-1 or anti-IL-6 antibody does not stop a damaged cell entering arrest.
It blunts what the arrested cell secretes. **The barrier stays; the tumour-promoting
signal is reduced.** Li and Coppé are therefore not in conflict — they describe the
two halves, and the surviving candidates act only on the second.

## The distinction this produces, which is the useful output

| Intervention | Effect on the barrier | Verdict for MVA |
|---|---|---|
| **SASP blockade** (anti-IL-1, anti-IL-6) | arrest intact, paracrine signal reduced | **survives attack** |
| **Senolysis** (clearing senescent cells) | barrier removed | **REFUTED for MVA** |

Senolytics — navitoclax, dasatinib+quercetin, BCL-2-family inhibition — delete
the arrested cells. In a child generating aneuploid, damaged genomes continuously,
that removes a standing tumour-suppressive barrier. **This is a positive refutation,
not an absence of support**, and it is a stronger statement than Gate 3 could make:
Gate 3 refused venetoclax as an antineoplastic and never saw navitoclax (tier C,
unapproved). Both refusals were right, but for shallower reasons than this one.

Recording a refuted branch matters. It is the part of the search space a reader
can now stop exploring.

## Direct clinical counter-evidence on the remaining worry

Gate 3's concern was that blunting inflammation removes immunosurveillance and
raises cancer risk. For the IL-1 axis specifically, the largest randomised test
went the other way. Ridker et al., *Lancet* 2017 — CANTOS, n=10,061
([DOI](https://doi.org/10.1016/S0140-6736(17)32247-X)) — report that canakinumab
produced dose-dependent reductions in incident lung cancer (HR 0.61 at 150 mg,
**HR 0.33 at 300 mg**) and in lung cancer mortality (HR 0.23 at 300 mg).

That does not transfer to a child with MVA and must not be presented as if it
does — different population, different cancer, different mechanism of risk. What
it does is defeat the general claim that IL-1β blockade is cancer-permissive.
The direction of the only large randomised evidence is protective.

**The cost is real and must travel with the claim:** in the same trial "fatal
infections or sepsis were significantly more common in the canakinumab groups than
in the placebo group," and all-cause mortality did not differ (HR 0.94, 95% CI
0.83–1.06). An IL-1 proposal for this child trades an infection risk for a
hypothesised oncological benefit. That trade is the substance of the proposal and
should be stated as the central question a clinician would have to answer, not
buried.

## Coverage, reported separately from the verdict

Every finding above is **literature-only**. There is no MVA patient expression
data, no MVA cohort, and no trial of any of these agents in a chromosomal
instability syndrome. Per Phoenix's convention, missing channels lower coverage
and never raise the score:

- mechanism channel: observed
- literature / endpoint channel: observed
- adversarial refutation channel: observed, thesis survived
- tissue / expression channel: **absent**
- trial-forensics channel: **absent**

Two of five channels absent. The honest adjudication for the SASP-blockade thesis
is therefore **interesting_under_supported**, not `prioritize_for_validation`. The
senolysis branch is **do_not_rescue**, and that one is well supported.

## What this changes for the report

1. Lead with the refuted branch. "We found the senolytic branch is contraindicated
   for this genotype" is a harder, more useful claim than another list of candidates.
2. The IL-1 axis is the surviving proposal, and the infection/oncology trade is
   its central question rather than a limitation paragraph.
3. Do not claim CANTOS transfers. Claim only that it defeats the general
   cancer-permissive objection.
4. Paediatric evidence is still unestablished for every survivor — unchanged from
   Gate 3 and still the largest gap.
