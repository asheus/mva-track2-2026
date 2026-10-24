# Suijkerbuijk et al. 2010, Cancer Res 70:4891-900 (PMC2887387)
All quotations verbatim from the PMC full text retrieved via PubMed.

## C1 - The two-class model of MVA mutations
> "all MVA mutations fall in two distinct classes: those that impose specific defects in
> checkpoint activity or microtubule attachment and those that lower BUBR1 protein abundance."

## C2 - Biallelic MVA architecture is missense + truncating
> "In patients with biallelic mutations, a missense mutation pairs with a truncating mutation."
> "In four families with individuals that carried biallelic mutations, a truncating mutation was
> combined with one amino acid substitution, often in the kinase domain."

## C3 - Kinase-domain substitutions destabilise; distal substitutions do not
> "All mutant proteins with substitution mutations in or near the kinase domain showed a
> 5-10 fold decrease in levels compared to wild-type BUBR1 in HeLa and U2OS cells."
> "the two substitution mutations located away from the kinase domain, Y155C and R550Q,
> did not affect protein levels when compared to wild-type BUBR1."
> "BUBR1 protein abundance was most severely decreased when mutations occurred in or near
> the kinase domain, but less by a mutation in the N-terminal TPR domain."

## C4 - Residual abundance in actual patient lines
> "abundance of full-length substitution mutant BUBR1 protein in all patient lines
> (absent/I909T, 386X/R727C, 753X/R814H or 731X/Y155C) was decreased 2-6 fold compared to
> wild-type alleles."
2-6 fold decrease == roughly 17-50% of wild-type. TEXT-VERIFIED, and it independently
corroborates the figure-only values (35%, 17%) read from Xu 2013 Fig 4A.
Carrier parents sat between patients and controls:
> "levels of full-length BUBR1 in the parent cell lines, carrying one mutant allele, were
> consistently in between those of patients and unrelated healthy controls."

## C5 - THE DOSAGE THRESHOLD (text-verified, the answer to "at what % do symptoms start")
> "BUBR1 abundance was reduced to different levels by titration of doxycyline to a HeLa cell
> line stably carrying inducible expression of an shRNA to BUBR1. Whereas saturating amounts
> of doxycyline reduced BUBR1 protein to ~6% and caused chromosome mis-segregation in the
> majority of cells, low amounts of doxycyline, while still significantly reducing BUBR1
> levels to ~13%, had virtually no impact on the fidelity of chromosome segregation."
Threshold for chromosome missegregation in HeLa lies between ~6% and ~13% of wild-type.

## C6 - Mechanism of the low abundance
Truncating alleles: transcript loss (NMD).
> "mRNA from the 386X allele could not be detected ... suggested that transcripts from the
> 731X allele were also absent ... in agreement with a previous suggestion that expression of
> truncated BUBR1 proteins may be prevented by nonsense-mediated mRNA decay (NMD)"
> "both 386X and 731X are expressed when NMD is circumvented by plasmid-driven expression"
Missense alleles: misfolding, HSP90-dependence, proteasomal clearance.
> "protein turnover of the substitution mutant proteins I909T and R727C was increased ~2-fold"
> "combined treatments of CHX and GA removed virtually all mutant BUBR1 protein"
> "inhibition of proteasomal degradation with MG132 prevented the enhanced protein turnover
> caused by HSP90 inhibition"

## C7 - 731X IS FUNCTIONALLY COMPETENT when NMD is bypassed  [decisive for this proband]
> "LAP-731X has no kinase domain yet is fully capable of supporting the microtubule attachment
> function of BUBR1. Furthermore, LAP-731X restored the response to nocodazole as well as
> proper chromosome segregation in unperturbed mitosis, suggesting that, at least in our assays
> and in these cells, the kinase domain of human BUBR1 is not required for the mitotic
> checkpoint nor for stable microtubule attachments."
> "neither the kinase activity nor the 265 amino-acid kinase domain are required for
> establishing mitotic checkpoint activity or stable microtubule attachments."

## C8 - Restoring BUBR1 rescues patient cells
> "restoration of high levels of BUBR1 by transient expression of ... cDNA induced a 2-fold
> increase in the response to nocodazole in patient cells"
> "mitotic checkpoint activity was almost fully restored to parental levels upon re-expression
> of BUBR1 in the patient cells"
> "forced overexpression of the poorly expressed substitution mutants I909T and L1012P to
> levels comparable to wild-type BUBR1 fully restored the response to nocodazole"

## C9 - The kinase domain's actual job is stability, non-catalytically
> "the integrity of the kinase domain needs to be preserved in order for chromosome segregation
> to be free of errors. This opens the possibility that the kinase domain is involved in
> regulating BUBR1 protein stability in a non-catalytic fashion, perhaps through ATP binding
> or cofactor association."

## C10 - Cancer epidemiology
> "37% of patients develop cancers including rhadomyosarcoma, Wilms tumor and leukemia,
> mostly within the first 3 years of life, not seldom even in utero"

## DISCREPANCY LOGGED
Suijkerbuijk text names the patient line genotype **731X/Y155C**; the Xu 2013 Figure 4A image
label read **731X/Y115C**. Primary source wins: Y155C, which is consistent with Suijkerbuijk
describing it as "located in the amino-terminal TPR domain" (TPR = 59-219; 155 is inside, 115
is also inside, but the text spelling is authoritative). Recorded, not silently reconciled.

## C11 - Q921H is WT-like, and is a PASSENGER on the L844F allele
Added 15 Sep 2026. The line below previously annotated Q921H as "(benign, WT-like)" with
no quotation behind it, while every other claim in this file was quoted - so the claim
could not be checked from this file, even though it is load-bearing in
PREDICTOR-CALIBRATION.md and STABILITY-AXIS.md. Verified at source, verbatim:
> "of the two substitution mutations that were reported to occur within one allele
> (L844F and Q921H) (2), L844F was poorly expressed and unable to restore any of the
> defects in BUBR1-depleted cells. In striking contrast, the Q921H mutation was
> indistinguishable from wild-type LAP-BUBR1, both on protein level and functionality.
> This suggests that the L844F substitution is the likely cause of mitotic defects in
> the patient carrying the doubly mutated allele."
Two consequences. The measured-normal claim is CONFIRMED, on both protein level and
function. And Q921H is a passenger sharing an allele with L844F, which explains why
ClinVar/UniProt assert it Pathogenic: it was catalogued from an MVA patient without
being separated from the allele it travelled on.
Note also that C3's "all ... in or near the kinase domain showed a 5-10 fold decrease"
does NOT contradict this; the paper marks Q921H out as the striking exception.

## Kinase-domain substitutions named in this paper
I909T, R814H, L1012P, L844F, Q921H (measured WT-like - see C11), R727C ("near" the
domain), plus non-kinase-domain Y155C (TPR) and R550Q - both of which did NOT
destabilise.
