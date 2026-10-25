# BUB1B / MVA: what has been tried, what failed, what nobody has attempted

*Every row is cited. According to PubMed for the literature rows; ClinicalTrials.gov for
the trials row, queried 21 Oct 2026. Where we found nothing, the row says what was
searched, because "nothing found" and "nothing exists" are different claims.*

## The headline

**No clinical trial has ever been registered for mosaic variegated aneuploidy, or for
*BUB1B*.** ClinicalTrials.gov returns **0** studies for "mosaic variegated aneuploidy"
and **0** for *BUB1B*/BubR1, while returning 151 for "aneuploidy" generally — so the
zero is a fact about this disease, not a broken query.

There is no approved therapy, no failed trial, and no abandoned programme. The therapeutic
history of this disease is empty. That is unusual and it changes what a useful
contribution looks like: there is no failure to learn from, so the risk is not repeating
someone's mistake — it is starting in the wrong place.

## Tried in patients

| approach | status | evidence |
|---|---|---|
| any disease-modifying therapy | **never attempted** | 0 registered trials |
| cancer surveillance and supportive care | standard of care | the only established management; does not alter the molecular defect |

## Tried in model systems — and what each one established

These are the real experiments. None was a therapy attempt; all are genetics, and they
are the foundation any therapeutic argument has to stand on.

| what was done | result | why it matters | source |
|---|---|---|---|
| Mice engineered to express **low levels** of BubR1 | progressive aneuploidy plus progeroid features — short lifespan, dwarfism, cataracts, loss of subcutaneous fat, impaired wound healing; infertile | establishes that BubR1 insufficiency *causes* the phenotype | Baker 2004, [10.1038/ng1382](https://doi.org/10.1038/ng1382) |
| **Graded reduction** of BubR1 in mouse embryonic fibroblasts | aneuploidy and senescence increased *with the degree of reduction* | **the dose–response curve.** The phenotype tracks the amount of protein, so the amount of protein is the therapeutic variable | Baker 2004, as above |
| An **allelic series** mimicking real MVA genotypes: a truncating allele (X753), a low-wild-type hypomorph (H), and a missense allele (L1002P, modelling human L1012P) | **truncating + missense died prematurely**; **hypomorph + missense was viable** with MVA features including cancer predisposition, dwarfism, lipodystrophy, sarcopenia | the genotype architecture determines survival, and the viable combinations are the ones retaining partial-function protein | Sieben 2020, [10.1172/JCI126863](https://doi.org/10.1172/JCI126863) |
| Same study, comparing genotypes at matched total BubR1 | several progeroid pathologies were *attenuated* despite similar total protein and similar aneuploidy | **allele identity matters beyond protein level.** A pure dosage model is incomplete — this is the main caution against our own thesis | Sieben 2020, as above |
| Crossing BubR1 progeroid mice onto p53-null and p21-null backgrounds | p53 delays muscle and fat decline via p21; but p21 *promotes* lens senescence and cataract | the downstream senescence response is tissue-specific and bidirectional, so blanket senescence-targeting would help some tissues and harm others | Baker 2013, [10.1016/j.celrep.2013.03.028](https://doi.org/10.1016/j.celrep.2013.03.028) |
| Mapping BubR1's own degradation control | BubR1 is acetylated at **K250** by PCAF; acetylation **blocks ubiquitin-dependent degradation**; **APC/C-Cdc20** is the ligase. Acetyl-mimetic K250Q is stabilised; acetyl-dead K250R is unstable | **names a control point for BubR1 abundance.** Also names its cost: K250Q markedly *delayed* chromosome segregation | Choi 2009, [10.1038/emboj.2009.123](https://doi.org/10.1038/emboj.2009.123) |

**Nothing in this table is a failed therapy.** Every entry is a genetic experiment that
worked and told us something. The thing that has never been done is use any of it.

## Not tried — ranked by how much of the required evidence already exists

**1 · Raising the abundance of protein made by a missense allele.**
The dose–response is established (Baker 2004). The degradation route is named, with a
validated switch (Choi 2009). What is missing is any attempt to move it pharmacologically
in a *BUB1B* context, and any evidence about what the right amount is. The cost is also
already visible: over-stabilisation delays mitosis, so this is a dose-finding problem, not
a switch to flip.

**2 · Readthrough of *BUB1B* premature termination codons.**
Never attempted for this gene. The modality is real and partly in humans: ataluren has
conditional approval elsewhere for Duchenne, and works by competitively inhibiting the
release factor complex; aminoglycoside G418 and anticodon-edited aa-tRNAs act by
orthogonal mechanisms. Critically, Bhat 2025 shows **the PTC's own identity and adjacent
sequence determine whether ataluren will work** — patients whose context promotes strong
release-factor interaction are predicted resistant
([10.1093/nar/gkaf216](https://doi.org/10.1093/nar/gkaf216)). So readthrough eligibility
is sequence-computable, per allele, and nobody has computed it for this gene.

**3 · Any multiplexed functional assay of *BUB1B* variants.**
MaveDB holds no *BUB1B* dataset — none for any spindle-checkpoint gene. There is no
equivalent of the Fabry amenability assay, which is why every eligibility statement for
this gene, ours included, is predicted rather than measured.

**4 · Targeting the downstream consequence rather than the defect.**
Senolytics, mTORC1 inhibition (sarcopenia in the allelic series correlated with mTORC1
hyperactivity), p53/p21 modulation. All plausible, none tried in MVA, and all share one
property: they treat the damage rather than the dosage, so they cannot prevent
mis-segregation. Worth saying out loud because they are the easiest things to propose and
the furthest from the cause.

## What this table changes about our own plan

Two things.

First, **the empty trials column is the opportunity and also the warning.** Nobody has
failed here because nobody has started, which means there is no validated endpoint, no
natural-history dataset sized for a trial, and no regulatory precedent. Any proposal that
assumes those exist is wrong.

Second, **Sieben 2020 is the strongest published objection to a pure dosage thesis** —
matched total BubR1 gave different severity depending on which alleles produced it. We
cite it against ourselves in `COUNTER-ARGUMENT.md` rather than only where it helps.
