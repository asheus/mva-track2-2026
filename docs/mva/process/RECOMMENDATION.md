# The recommendation, with viability as a gate

**Everything we recommend has to be able to reach a patient.** Applying that as a hard gate
rather than as one criterion among eight changes the answer, and it overturns our own
previous ranking.

*Producer: `scripts/mva/viability_gate.py`, superseding the ranking in
`APPROACHES-ALL.md`.*

## Why the previous ranking failed

`approach_matrix.py` scored viability as one axis among eight and let a composite average
it away. It ranked **trans-splicing first**. The very next piece of work established that
trans-splicing has:

- no approved drug
- **no molecule in any clinical trial** — ClinicalTrials.gov returns one hit, a
  Huntington's skin biopsy for preclinical development
- **no RTM ever given to a patient, for any gene**, thirty years after the modality was
  demonstrated
- a required efficiency here of **23–38%**, above what published RTMs achieve

A ranking that puts a non-existent drug first is not a ranking, it is a preference. The
gate below fixes that.

## The gate

| | meaning | may be recommended |
|---|---|---|
| **3** | obtainable now — approved, in trials, or otherwise available | yes |
| **2** | in clinical trials — the molecule exists and is given to humans | yes |
| 1 | preclinical only — the class exists, no human has received it | **no** |
| 0 | no molecule at all | **no** |

## What survives

Of fifteen approaches, **seven** pass the gate. Of those seven, exactly **one** also
addresses the deficit this genotype has.

| | approach | viability | addresses deficit | evidence in *BUB1B* |
|---|---|---|---|---|
| **1** | **NAD⁺ precursor (NMN / NR)** | **obtainable now** | **2/2** | **2/2** |
| 2 | Prime editing, ex vivo | in trials | 1/2 | 0/2 |
| 3 | AAV gene replacement | in trials | 1/2 | 0/2 |
| 4 | Cancer-risk stratification from the map | obtainable now | 0/2 | 2/2 |
| 5 | mTORC1 inhibition / senolytics | obtainable now | 0/2 | 1/2 |
| 6 | Readthrough | obtainable now | 0/2 | 0/2 |
| 7 | HDAC inhibition | obtainable now | 0/2 | 0/2 |

## Blocked by the gate — directions, not options

The painful part: **the three approaches that best address the deficit are all blocked.**

| approach | addresses | why blocked |
|---|---|---|
| Trans-splicing (SMaRT) | **2/2** | no RTM has ever been given to a patient |
| trans-RNA initiation | **2/2** | published Nov 2025; no human has received one |
| CRISPRa at native promoter | **2/2** | not deliverable to a child |

Also blocked: checkpoint timing (cytotoxic, unknown window), pseudokinase chaperone (no
molecule, and not evaluable without a structure), APC/C inhibition (arrests mitosis),
splice ASO (killed by RNA-seq), neoantigen vaccine (would target the patient).

## The recommendation

**An NAD⁺ precursor is the only approach that is both obtainable and aimed at the right
variable.**

It is the recommendation **by elimination, not by enthusiasm.** Everything with a better
mechanism has no molecule in a human; everything else obtainable is aimed at something
else. That is a weaker endorsement than "best candidate" and it is the accurate one.

What it rests on:

- **Mechanism in this gene.** BubR1's decline is driven by falling NAD⁺; SIRT2 preserves
  BubR1 by keeping K668 deacetylated; **NMN raised BubR1 abundance in vivo**, and SIRT2
  overexpression extended median lifespan in the BubR1-hypomorphic mouse — the accepted
  model of this disease ([10.15252/embj.201386907](https://doi.org/10.15252/embj.201386907)).
- **The target level is a ceiling observed in humans — qualified 23 Oct 2026 (C49).**
  ~610 gnomAD heterozygous LoF carriers live at carrier level with **no severe early
  phenotype**, and no homozygote appears in 731k. That is the correct, narrow claim.
  It is **not** "carrier level is validated as safe", which this bullet used to imply:
  heterozygous *Bub1b* truncating mice show mild aneuploidy, reduced lifespan and increased
  carcinogen-induced tumour growth (Wijshake 2012,
  [10.1371/journal.pgen.1003138](https://doi.org/10.1371/journal.pgen.1003138)), and parents
  of affected children have been reported with mild mitotic abnormalities. Absence of a
  *severe early* phenotype in a population database is not absence of a late or mild one,
  and gnomAD is not ascertained for either.
- **The route exists.** NR was given to a single Li-Fraumeni patient at NIH after in-vitro
  rescue in that patient's own fibroblasts (NCT03789175) — a germline cancer-predisposition
  syndrome, n=1, mechanistic biomarker. That is the template, already executed.

## Three conditions, and they are not small

1. **It is conditional on an untested assumption.** Everything above assumes p.Asn1002Lys
   reduces BubR1 **abundance**. The N1002R lane and the pT1008 blot test that. If abundance
   is normal, this recommendation is aimed at the wrong variable too.
2. **Magnitude is unquantified.** North's abstract does not state how much NMN raised
   BubR1, the lifespan result came from genetic SIRT2 overexpression rather than NMN, and
   nobody has shown a misfolding-prone mutant responds like wild-type protein.
3. **It raises BubR1 by slowing degradation, and degradation is the timed event.** Mitotic
   timing must be measured alongside abundance, not after it.

**We are not proposing that anyone give this child anything.** The proposal is the order of
operations the Li-Fraumeni n=1 already validated: measure the deficit in patient-derived
cells, test whether the agent rescues it in those same cells, and only then consider a
single-patient study with a mechanistic readout. **Step one is a western blot.**

## What stays true regardless

The map does not depend on which candidate wins. **280 of 2,536 alleles lose the transcript,
and eight of fifteen approaches cannot reach them at all.** That boundary has survived five
changes of technology and now a viability gate that eliminated our own top-ranked approach.

The eligibility map is the only thing here that is both **useful and viable today** — which
is why it, and not a drug, is what we are submitting.
