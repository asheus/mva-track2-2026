# Which allele can actually be rescued, with drugs that are safe in a baby


> **SUPERSEDED IN PART, 14 Oct 2026.** This file ranks 4-PBA first, partly on its
> HDAC activity. That leg is **retracted**: HDAC inhibition induces premature sister
> chromatid separation and strips BubR1 from kinetochores, and MVA1's other name is
> premature chromatid separation syndrome. Arimoclomol (FDA-approved Sep 2024,
> children ≥ 2) carries the matched mechanism without it and is now the lead; 4-PBA
> is kept as a stated alternative with the hazard attached. See
> `CORRECTIONS-2026-10-06.md`, C5 and C7, and `TRACK2-REPORT.md` §3.3. The fold-class
> reasoning below is unaffected — only the ranking inside the chaperone class moved.

Constraint accepted: **no new experiments, no investigational compounds in an infant.**
Everything below is estimated from published data. Reproducible via
`apps/api/scripts/mva/ptc_context_and_arithmetic.py`.

---

## Answer

| route | ceiling | feasible in this child? |
|---|---|---|
| Allele 1 via **readthrough drug** | **+0.5 units** against a needed +18 | **No — dead on arithmetic** |
| Allele 1 via **NMD inhibition** | **+40 units** | High ceiling, blocked on safety and on one unresolved biology question |
| Allele 2 via **stabilisation** | needs ~2-fold | **The pragmatic route** |

---

## 1. Is 737X subject to NMD? Yes — as close to certain as prediction gets

- PTC 747 nt upstream of the last exon–exon junction, in exon 17 of 23. The 50–55 nt rule
  is exceeded thirteenfold.
- Flanked by two truncations *empirically confirmed* transcript-null in patients: 731X
  (766 nt) and 753X (700 nt).

NMD is never complete, so some transcript survives — typically a minority fraction. That
residue is the only substrate a readthrough drug could ever act on, which is the crux of
the next section.

## 2. Would a readthrough drug work? No. And this is now quantitative, not a hunch

Three independent things stack against it.

**(a) Readthrough drugs are far weaker than the field's rhetoric suggests.** Across ~5,800
pathogenic PTCs measured head-to-head for eight compounds, **median readthrough ranged from
0.08% (gentamicin) to 1.32% (SJ6986)**. Even the *top decile* of PTCs reached only 0.51%
(gentamicin) to **4.28% (DAP)**. Untreated, only 17 of 5,800 PTCs exceeded 1%.

**(b) This child's PTC is a poor substrate — on three of the three known context rules.**
Scored against the published determinants:

| feature | this child | verdict |
|---|---|---|
| stop codon identity | **UGA** | favourable — the best of the three |
| nucleotide at **+1** | **A** | unfavourable — cytosine promotes readthrough |
| nucleotide at **−1** | **G** | unfavourable — adenine promotes readthrough |
| upstream codon | **GAG** (Glu) | unfavourable — A-ending codons read through better |

And specifically for DAP, the UGA-selective agent that looked most promising: the data show
**GAA > GAG** upstream. This child has GAG — the weaker glutamate codon. **The one feature I
previously cited as favourable (UGA) is the only favourable feature there is.** I over-read it.

**(c) The substrate has already been destroyed.** Readthrough acts on the NMD survivors, not
the full transcript.

**The arithmetic**, taking one wild-type allele as 50 units of a 100-unit diploid normal,
current baseline ~17 units, and the target being the milder published comparator at 35:

| scenario | gain | needed |
|---|---:|---:|
| median drug, no NMD inhibition | **+0.10** | +18 |
| absolute best case (DAP, top-decile PTC) | **+0.53** | +18 |
| full NMD inhibition **plus** best-case readthrough | **+2.14** | +18 |

**Readthrough falls short by roughly 35-fold even under assumptions that flatter it.** This
is not "unproven" — it is quantitatively insufficient. Ataluren's clinical failure and the
EU withdrawal look, in this light, like exactly what the biochemistry predicts.

**Conclusion: cross readthrough off for this child.** That also retires DAP, ELX-02 and the
tryptophan-insertion argument I made last turn.

## 3. NMD inhibition has the only large ceiling — and two blockers

If the transcript is stabilised and the 1–736 protein is stable and functional, allele 1
returns toward a full wild-type allele's output: **+40 units**, more than twice what is
needed. Nothing else on the table is in that league.

**Blocker 1 — will the 1–736 protein work?** Unresolved. 731X rescues fully; 753X fails.
Best available estimate, from orphaned hydrophobic interface left exposed when the kinase
domain is absent:

| truncation | orphaned hydrophobic surface | outcome |
|---|---:|---|
| 731X | 332 Å² (1.00×) | stable, rescues |
| **737X** | **451 Å² (1.36×)** | **unknown — closer to the working one** |
| 753X | 871 Å² (2.63×) | unstable, fails |

737X adds two leucines (L731, L734) to 731X's orphaned surface. 753X adds five more
hydrophobics including a methionine burying 108 Å². **My estimate: 737X more likely behaves
like 731X than 753X — perhaps 70/30.** That is a judgement from a two-point calibration,
and it is the single largest unresolved item in this workstream.

**Blocker 2 — there is no safe drug.** No NMD inhibitor is approved anywhere. Amlexanox is
approved for aphthous ulcers and (in Japan) asthma, as topical paste or short course — not
chronic systemic dosing in an infant. And the mouse data place the risk exactly where this
child is vulnerable: modest NMD inhibition was well tolerated in non-neurological somatic
tissues, but **neurological tissues were the most responsive to NMD change**, in a child
of this age. **Corrected:** this previously read "whose phenotype is dominated by
microcephaly and developmental delay" — neither feature is in the clinical record, and
the claim came from the MVA literature rather than from this patient
(`PHENOTYPE-GROUNDING.md`). The concern rests on the mouse tissue data and on chronic
infant dosing alone.

**So allele 1 has the best ceiling and no safe way to reach it today.**

## 4. Therefore: allele 2 is the route

Not because it is better — its ceiling is lower — but because it is the only one where
mechanism and an acceptable safety profile currently coincide. It needs a **~2-fold**
increase in BubR1, and the mechanism is a destabilised protein cleared by the proteasome
after chaperone triage, which is a druggable axis with approved agents.

**Sodium phenylbutyrate (4-PBA)** is the leading candidate on safety grounds alone:
- Approved for chronic management of **urea cycle disorders** — a paediatric, often
  neonatal-onset indication — with decades of use and multiple approved formulations
  (Buphenyl, Pheburane, Olpruva, and glycerol phenylbutyrate as Ravicti).
- Acts as a chemical chaperone *and* an HSP70 inducer *and* an HDAC inhibitor, all three of
  which point the right way for a destabilised, proteasome-cleared protein.
- **Caveat to carry, not bury:** the FDA review of Ravicti flagged "potential neurotoxicity
  in pediatric patients under two years of age" and required post-marketing PK studies in
  infants. Age matters here.

**Arimoclomol**, an HSF1 co-inducer **approved by FDA as Miplyffa on 20 Sep 2024 for NPC in children ≥2** (C7), is now the leading candidate — it rescues
glucocerebrosidase in Gaucher fibroblasts and prevents aggregation of a destabilised
rhodopsin mutant.

**And the standing refusal:** HSP90 inhibitors remain contraindicated. They remove virtually
all destabilised BubR1 — this child's entire supply.

## 5. What would change this conclusion

- If the 1–736 protein were shown non-functional, allele 1 closes entirely and allele 2
  becomes the *only* route rather than the preferred one.
- If a selective NMD inhibitor with paediatric safety data emerged, allele 1's 40-unit
  ceiling would immediately outrank everything here.
- If N1002K turns out **not** to be a folding mutant — still unresolved — then chaperone
  amplification is aimed at the wrong mechanism and 4-PBA's rationale collapses with it.

That last point is why the folding question is not academic: **it is the premise of the only
route currently open.**
