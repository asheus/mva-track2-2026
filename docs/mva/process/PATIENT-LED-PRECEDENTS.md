# What the patient-led cancer movement can and cannot lend us

*Prompted by a 21 Oct 2026 thread describing six people running self-directed personalized
therapy for their own or a family member's cancer. According to PubMed for the literature;
ClinicalTrials.gov queried 21 Oct 2026; transcript annotation from Ensembl.*

## The modality does not transfer, and the reason is not a detail

Every case in that thread is the same move: sequence the tumour, find **neoantigens**
(mutations present in the tumour and absent from the rest of the body), build a
personalized vaccine, teach the immune system to destroy cells displaying them.

That works because the mutations are **somatic**. The patient has a healthy baseline, and
the tumour is the only thing carrying the target.

Our variant is **germline**. p.Asn1002Lys is in every cell the child has had since
conception. A vaccine raised against mutant BubR1 would be an instruction to attack the
patient's entire body. This is not a difficulty to engineer around — it is the wrong sign.
Any proposal that reaches for a neoantigen vaccine in a germline loss-of-function disease
has confused "there is a mutant protein" with "there is a foreign protein."

There is one place the thread's modality would genuinely apply: **MVA is a
cancer-predisposition syndrome.** If this child develops a tumour, that tumour will carry
somatic mutations, and personalized neoantigen vaccination becomes exactly as relevant as
it is for anyone else. That is oncology for a complication, not therapy for the disease.

## What does transfer: the operating model

Three things from that thread are real and worth copying.

1. **Sequence first, design second.** Molecular diagnosis drives the therapeutic choice
   rather than the diagnosis category. That is what our per-allele map is for.
2. **Cell-first proof before anything in a person.** Several of these efforts test in the
   patient's own cells before committing.
3. **n-of-1 is a legitimate path, and families drive it.** Funding and urgency come from
   outside the usual trial machinery.

But for a **germline, pediatric** disease the canonical precedent is not a cancer vaccine.
It is milasen.

## The right precedent: milasen

A child with a rare fatal neurodegenerative disease; genome sequencing identified the
causal splice defect; a **splice-modulating antisense oligonucleotide** was rationally
designed for that one patient; **proof-of-concept experiments in cell lines from the
patient** justified an n-of-1 study launched **within one year** of first contact. No
serious adverse events, objective reduction in seizures. The authors state it plainly:
*"This study offers a possible template for the rapid development of patient-customized
treatments"* (NEJM 2019, [10.1056/NEJMoa1813279](https://doi.org/10.1056/NEJMoa1813279)).
The same programme later produced **atipeksen** for ataxia-telangiectasia — a genome
instability and cancer-predisposition syndrome, which is our disease's near neighbour.

This is the thread's spirit executed correctly for our disease class: same urgency, same
patient-specificity, same cell-first order — and a modality that *restores* rather than
destroys.

## What milasen points at, and that we had missed

Milasen was **splice-modulating**. That opens a mechanism our candidate list did not have.

**Upregulation by blocking non-productive splicing.** Many genes divert a fraction of
their pre-mRNA into isoforms that are degraded rather than translated. An ASO that blocks
that diversion redirects the flux into productive mRNA and **raises protein output from
the alleles the patient already has**.

This is not speculative as a modality. Zorevunersen (STK-001), which works this way on
*SCN1A*, has completed Phase 1/2 **in children and adolescents** and is now in **Phase 3**
(EMPEROR, 170 patients, 61 sites — NCT06872125, NCT04442295, NCT04740476).

**And *BUB1B* has the substrate.** Of its **31 annotated transcripts, 12 carry the
`nonsense_mediated_decay` biotype** — a substantial share of the locus's annotated output
is non-productive by design:

```
  protein_coding                   12
  nonsense_mediated_decay          12   <- the flux an upregulating ASO would redirect
  retained_intron                   5
  protein_coding_CDS_not_defined    2
```

**Why this fits our genotype better than anything else on the list.** Our dosage model
says the gap to close is a shortfall, not a doubling — **about 1.43× if allele 2 retains
70%**. Redirecting non-productive flux is an effect of roughly that size. It is also
gene-specific, so it avoids the systemic consequences of raising NAD⁺ or inhibiting a
deacetylase everywhere. And it acts on allele 2 — the allele we independently identified
as the only reachable one — because allele 1's transcript is destroyed regardless.

## What this is not, yet

**An annotation is not a finding.** Ensembl's NMD biotype says these isoforms are
annotated, not that they carry meaningful flux in any relevant tissue, and not that a
discrete, ASO-targetable poison exon exists. Quantifying that flux is a real piece of
computational work — and one our splice pipeline is already built to do. Until it is done
this is a lead, not a result.

Three further limits, stated now rather than discovered later:

- **Upregulation delivers more *mutant* protein.** It helps only if N1002K retains partial
  function. The mouse allelic series suggests the viable MVA genotypes are the ones
  retaining partial-function protein, but that is an argument by analogy, not a
  measurement of this allele.
- **Delivery is the hard problem.** Milasen and zorevunersen are delivered to the central
  nervous system. MVA is systemic — the growth phenotype and the cancer risk are
  whole-body. ASO biodistribution outside the CNS and liver is a genuine obstacle and we
  should not pretend the precedent carries over intact.
- **More BubR1 is not monotonically better.** The acetyl-mimetic that stabilised BubR1
  markedly delayed chromosome segregation. The window is bounded on both sides.

## Where this leaves the candidate ranking

> **SUPERSEDED 21 Oct 2026 — see `SPLICE-ARCHITECTURE.md` and correction C45.** The
> ranking below rested on *BUB1B* having an SCN1A-like target. It does not. *BUB1B*'s only
> decay-exclusive cassette exon is 54 bp, divisible by three, enters in frame +0 and
> carries no stop codon — it cannot be a poison exon. The same method recovers SCN1A's
> 64 bp frameshifting exon 20N from annotation alone, so the negative is interpretable.
> **The ASO route drops below the NAD⁺ route.** It is not removed: an RNA-seq search could
> still find what annotation cannot, and that is now future work rather than a candidate.

| | candidate | required effect size | gene-specific | in children | reaches allele 2 |
|---|---|---|---|---|---|
| ~~1~~ → 2 | splice-modulating ASO (upregulation) | ~1.4× — would match | yes | Phase 3 | **no target found** |
| ~~2~~ → 1 | NAD⁺ precursor (NMN/NR) | unquantified | no — systemic | some trials | yes |
| 3 | readthrough | n/a | — | — | no, 44 other alleles |

**The honest summary of what that thread gave us:** not a therapy, and not a vaccine. It
gave us the reminder that n-of-1 is a real path for a child, which sent us to the
precedent that actually fits — and that precedent's modality turns out to match our
genotype's arithmetic better than the candidate we had.
