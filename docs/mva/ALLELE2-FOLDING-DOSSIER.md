# Is p.Asn1002Lys actually a folding problem?

You asked not to take this on trust. Here is the case for, the case against, what we
added that the field did not have, and the experiments that would settle it.

**Verdict up front: the folding hypothesis is well-supported as a class claim and is now
supported by a specific structural mechanism for this residue — but it has never been
tested on N1002K, and one competing explanation is not excluded.**

---

## 1. What the claim actually rests on

Suijkerbuijk 2010 established the "low abundance" class on four pillars, all measured on
*other* variants (I909T, R727C, L1012P):

| # | Observation | What it shows |
|---|---|---|
| 1 | mRNA levels unaffected for I909T, R727C, Y155C (Northern) | the defect is post-transcriptional |
| 2 | Cycloheximide chase: mutant turnover **~2-fold faster** than wild-type | the protein is cleared faster, not made less |
| 3 | HSP90 inhibition (geldanamycin): mutant levels **severely decreased**, wild-type "only minor changes"; CHX+GA together "removed virtually all mutant BUBR1" | the mutant *depends* on chaperone activity that the wild-type does not |
| 4 | MG132 **prevents** the GA-induced loss | the clearance route is the proteasome |

That is a clean chaperone-dependent triage signature. Pillar 3 is the load-bearing one,
because it is *differential*: the wild-type protein barely cares about HSP90 and the mutant
collapses without it.

## 2. The strongest objection — and why it fails

**Objection:** many kinases are constitutive HSP90/Cdc37 clients. If BubR1 were one, GA
sensitivity would say nothing about misfolding.

**It fails on two counts.** First, wild-type BubR1 showed "only minor changes" under GA —
a constitutive client would crash. Second, I searched the chaperone literature and **BubR1
is not a documented HSP90/Cdc37 client**. Cdc37 recruits clients through the kinase domain
of *active* kinases, and BubR1 is a pseudokinase. So the HSP90 dependence here is
**acquired by mutation**, which is precisely the misfolding prediction.

## 3. What was missing in 2010, and what we can now supply

The authors were explicit about their own limit:

> "As there is no information on structural properties of BUBR1, it is at present unclear
> why these specific mutations affect protein abundance."

They could only map orthologous residues onto the BUB1 kinase structure, as an
"unpublished observation". **We now have the structure.** Computing the local environment
of residue 1002 in AlphaFold `AF-O60566-F1` (v6) gives a specific mechanism:

- **N1002 makes two backbone hydrogen bonds**: side-chain ND2 → V998 backbone O (2.83 Å),
  and side-chain OD1 → W978 backbone N (2.83 Å). Asparagine is bridging two different
  backbone segments — the classic Asn staple, and a role Asn is almost uniquely able to
  play because its short bifunctional amide can both donate and accept.
- **The pocket is aromatic and hydrophobic**: W973, F977, W978, F997, V998, L1001, A1003.
- **Lysine cannot do this job.** A long aliphatic chain with a terminal ammonium can donate
  but not accept, and cannot span both partners. It also buries a formal positive charge in
  an aromatic box and adds **+54 Å³** at a site with only 14.0% solvent accessibility and
  pLDDT 91.1.

Contrast the one *tolerated* kinase-domain substitution, **Q921H**: Gln→His is +9 Å³ and
retains both H-bond donor and acceptor capacity. It preserves the chemistry; N1002K
destroys it.

**This is a testable, local prediction, not an appeal to authority.** It predicts that
N1002K loses two specific hydrogen bonds — which molecular dynamics or a ΔΔG calculation
could check, and which a thermal-shift assay on recombinant protein could measure.

## 4. What is NOT established — the honest gap

- **Nobody has assayed N1002K.** Not its level, not its turnover, not its chaperone
  dependence. Class membership is a prior, not a result — now a quantified one:
  **P(abundance) = 0.79, 95% CI 0.44–0.98** (`scripts/mva/abundance_posterior.py`,
  CORRECTIONS C27). 0.92 if Q921H is dropped as confounded, which is defensible but is
  not the figure that ships. Two axes independent of the base rate agree: N1002K's
  +54.5 Å³ volume change sits inside the destabilising range and is 5.8× the tolerated
  variant's, and it is the only variant in the panel that buries a new formal positive
  charge.
- **"Folding problem" and "degron exposure" are not cleanly separable**, and the data do
  not separate them. Misfolding usually *causes* degron exposure. What pillar 4 shows is
  that the proteasome does the clearing — not *why* it was selected.
- **A specific E3 exists.** Pellino 1 (Peli1) directly ubiquitinates BubR1 and degrades it;
  Peli1-transgenic mice show 50% aneuploid splenocytes and 18% premature sister chromatid
  separation — an MVA-like cellular phenotype from the degradation side alone. The E3 that
  performs the K668-acetylation-dependent interphase degradation of BubR1 "remains unknown".
- **A third possibility is untested:** N1002K might disrupt a stabilising protein–protein
  interaction rather than the fold itself. The residue sits in an ordered surface-proximal
  position (RSA 14.0% is *mostly*, not fully, buried), so an interface role is not excluded.
  Burial does not settle it either way: in the measured panel below, the one **tolerated**
  kinase-domain variant (Q921H) is *more* buried than N1002K.
- **What IS now excluded, 14 Oct 2026: the variant failing to produce protein at all.**
  Pangolin scores allele 2 at gain +0.01 / loss 0.00, stable across three window widths,
  with its control reproducing exactly — so there is no cryptic splice site and, with
  C22's final-exon finding, no route to NMD. **Allele 2 is made.** The question is
  therefore two-way (abundance vs interface), not three-way. `SPLICE-ALLELE2.md`.

## 5. Why this distinction changes what you would do

| If the mechanism is… | Then… |
|---|---|
| Global misfolding, chaperone-dependent | chaperone amplification is on-target: 4-PBA, arimoclomol (HSF1 co-inducer, **FDA-approved as Miplyffa 20 Sep 2024 for NPC in children ≥2**, rescues glucocerebrosidase in Gaucher fibroblasts), HSF1 activators |
| Degron exposure via a specific E3 | inhibit that E3 — Peli1 is named and druggable in principle; far more selective than proteostasis-wide intervention |
| Lost partner interaction | neither of the above helps; you would need to restore the interaction or bypass BubR1 entirely, as MIS12-KARD-3D did |

### A safety finding that belongs in the funnel

**HSP90 inhibitors are contraindicated in this child.** They are a large, well-developed
oncology drug class, and Suijkerbuijk showed directly that HSP90 inhibition *removes
virtually all* destabilised BubR1. In a patient whose entire BubR1 supply comes from a
destabilised missense allele, that is a drug class that would deepen the exact deficit
driving the disease.

This is the same shape as the Gate 3 finding that a real MVA team withheld taxanes because
of the diagnosis — a mechanism-derived contraindication that would not show up in any
standard interaction check. **It should be added to Gate 3 as a refusal rule.**

> **DONE 14 Oct 2026** — and it had not been, for weeks, while this sentence sat here and
> the report carried it as a "standing refusal". `gate3_safety.py` now implements it as a
> *genotype-conditional* rule (`CHAPERONE_TARGETS`, `PATIENT_HAS_DESTABILISED_ALLELE`)
> rather than a drug blocklist, so it generalises to any gene whose patient depends on a
> destabilised missense allele, and refuses nothing for a patient with two truncating
> alleles. It refuses nothing in the live funnel either, because no HSP90 inhibitor is
> approved — which is why `tests/test_gate3_chaperone.py` exists to show it can fire.
> See `CORRECTIONS-2026-10-06.md` C25c.

## 6. The experiments that would settle it, in order of value

1. **Western blot + cycloheximide chase on the child's own cells.** Gives the level *and*
   the turnover rate. Settles both the estimate and pillar 2 in one experiment.
2. **GA / MG132 panel on those same cells.** Directly replicates pillars 3 and 4 for
   N1002K. If the mutant collapses under GA and is rescued by MG132, the folding
   mechanism is confirmed for this variant.
3. **Ectopic LAP-BUBR1 N1002K vs wild-type vs Q921H**, the assay already built in 2010.
   Places N1002K in the destabilising or tolerated class directly. Q921H is the ideal
   internal negative control because it is the one kinase-domain variant known to behave.
4. **Thermal shift / ΔΔG on recombinant kinase domain** — tests the specific two-H-bond
   prediction above rather than the downstream consequence.

Experiment 3 needs no patient material at all. It is a plasmid, a transfection and a blot,
and it would convert the single largest inference in this workstream into a measurement.

---

**Bottom line for your question.** It is very probably a folding problem, the structure now
says *why* in atomic detail, and the differential HSP90 dependence rules out the main
alternative reading of the original data. But "folding" versus "degron exposure" is not yet
resolved, no one has touched N1002K itself, and the answer changes which drug class you
would reach for. Treating it as settled would be exactly the error you asked me to avoid.
