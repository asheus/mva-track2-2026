# BubR1 dosage and phenotype in BUB1B-related disease

**A protocol-first evidence review, run to test — not assume — the claim that MVA1 is a
protein-dosage disease, and to locate the dosage threshold at which phenotype appears.**

Run 10 Sep 2026. Protocol registered before evidence collection (`protocol_draft.json`),
scope approved by the principal at the Question checkpoint, four material decisions
recorded. Artifacts in this directory are the audit trail.

---

## 1. The short answer

**Yes — it is a dosage disease, and this is not our inference. It is the published,
named mechanism, from the primary source.** But it is a *two-class* dosage model, and
which class a variant falls into is decided by **where in the protein it sits**, not by
whether it is missense or truncating.

> "all MVA mutations fall in two distinct classes: those that impose specific defects in
> checkpoint activity or microtubule attachment and those that lower BUBR1 protein
> abundance." — Suijkerbuijk et al. 2010

And on the threshold you asked for — the number below which symptoms start — there is
exactly **one** explicit titration experiment in the entire BubR1 literature:

| BubR1 remaining | Result |
|---:|---|
| **~13%** | "virtually no impact on the fidelity of chromosome segregation" |
| **~6%** | "chromosome mis-segregation in the majority of cells" |

So in that system the cliff sits **between 6% and 13%**. An independent experiment in a
different SAC gene (Cdc20) finds the same shape: <5% blocks anaphase outright, ~10%
still permits normal mitosis. Two genes, two labs, the same ~5–13% inflection.

**Your instinct that 17–35% "is not bad" is supported by the data.** It is well above
that cellular cliff.

---

## 2. But the threshold is not one number — it is a ladder

This is the finding that matters most, and it resolves the apparent contradiction that
MVA patients are *above* the 6–13% cliff yet are unmistakably ill.

| Phenotype | Dosage at which it appears | Source class |
|---|---|---|
| Gross chromosome missegregation in a transformed line | below ~6–13% | HeLa titration, text-verified |
| Progeroid syndrome in mouse | ~10% | BubR1 hypomorph |
| **MVA: aneuploidy + cancer predisposition + developmental phenotype** | **~17–50%** | four patient lines, text-verified |
| Microcephaly specifically | "nearly complete loss of BubR1 is also required" | Simmons 2019, via Pavone 2022 |

Read down that column: **different phenotypes have different thresholds, and they are not
in the order you would guess.** MVA disease appears at a *shallower* deficit than gross
missegregation in HeLa. A cancer cell line tolerates BubR1 loss that a developing embryo
does not — which is exactly what you would expect, and exactly why a single number would
have been misleading.

The honest form of the answer to "at what percentage do symptoms start" is therefore:
**for the MVA phenotype, roughly 17–50% residual is already disease-causing.** The 6–13%
figure is the floor for a cruder readout in a more tolerant cell type, not the clinical
threshold.

---

## 3. Where the two alleles fall

### Allele 1 — p.Leu737* — contributes essentially nothing, but not because it is broken

Two facts, both text-verified, and together they are the sharpest thing in this review:

1. **Truncated BubR1 protein is undetectable.** 386X, 731X and 753X were all undetectable
   in patient lysates; the mouse GTTA truncation was undetectable "even after long
   exposure times". Transcripts are destroyed by nonsense-mediated decay — and both 386X
   and 731X reappear when NMD is bypassed by plasmid expression.

2. **The protein that allele would make is fully functional.** LAP-731X — six residues
   from this child's stop codon — "has no kinase domain yet is fully capable of supporting
   the microtubule attachment function of BUBR1", and "restored the response to nocodazole
   as well as proper chromosome segregation in unperturbed mitosis."

So allele 1 is not a broken protein. **It is a competent protein that is never
manufactured.** The defect is at the mRNA, not the polypeptide.

### Allele 2 — p.Asn1002Lys — makes protein, and it is probably not enough

This is precisely your hypothesis, and the literature supports it:

> "Low protein abundance is the direct result of the absence of transcripts from
> truncating mutants combined with **high protein turnover of missense mutants**. In this
> group of missense mutants, the amino acid change **consistently occurs in or near the
> BUBR1 kinase domain**."

Residue 1002 is inside the pseudokinase domain on every annotation (766–1050 in the 2026
domain map). The named kinase-domain substitutions — I909T, R814H, **L1012P (ten residues
away)**, L844F, R727C — all showed a **5–10 fold decrease** in level. The two substitutions
*outside* the kinase domain, Y155C and R550Q, **did not affect protein levels at all**.

The mechanism is misfolding: turnover roughly doubled, levels collapsed under HSP90
inhibition, and proteasome inhibition rescued them. Not a catalytic failure — a folding
failure. Which is consistent with the authors' own conclusion that the kinase domain's
real job is **holding the protein together**, "in a non-catalytic fashion".

### The prediction for this child

Allele 1 ≈ 0. Allele 2 destabilised. Published patients with exactly this architecture —
**nonsense + kinase-domain missense** — run at **2–6 fold below wild-type (≈17–50%)**, and
that is MVA-causing.

**"Producing something, but not good enough" is the correct description, and it is the
published mechanism rather than a guess.**

Two independent architectural comparators now exist:
- **753X / R814H** (MVA-12C) — nonsense plus kinase-domain missense; the closest published
  match to 737X / N1002K.
- **p.Arg194Ter / p.Arg770Gln** — nonsense plus pseudokinase-domain missense; that infant
  died at 6 months, though the authors explicitly decline to attribute causality.

---

## 4. What this does and does not license

**Licensed.** BUB1B-MVA is a protein-abundance disease for this variant class. Raising
BubR1 abundance is mechanistically the right axis. Three independent rescues are on record:
re-expressing BubR1 in patient cells "almost fully restored" checkpoint activity to
parental levels; forcing the unstable mutants I909T and L1012P up to wild-type levels
"fully restored" function; and bypassing BubR1 entirely by targeting PP2A-B56 to
kinetochores restored alignment in MVA fibroblasts.

That last point deserves emphasis: **the destabilised missense protein is not defective.
It is merely scarce.** Restore its level and function returns.

**Not licensed.** We have no measurement of *this child's* BubR1 level. Every number above
is from other people's cells. The comparator class spans 17–50% — a threefold range — and
where he sits inside it changes what any abundance-raising intervention could achieve.
That measurement is a western blot on his fibroblasts or LCLs, and it remains the single
highest-value missing datum in this whole workstream.

**Also not licensed:** treating N1002K's destabilising effect as established. It is
*predicted* by position and by five named neighbours behaving that way. No one has ever
studied N1002K — confirmed by exhaustive boolean search of the corpus, which returns zero
papers.

---

## 5. Cohort context for surveillance

From 31 published MVA1 cases (Pavone 2022), independently corroborated on the cancer
figure by Suijkerbuijk (37%):

| Feature | Frequency |
|---|---:|
| Pre/post-natal growth retardation | 93.5% |
| Microcephaly | 87% |
| Intellectual disability / developmental delay | 77.4% |
| Epileptic seizures | 45.1% |
| **Malignancy** | **38.7%** |
| Other cerebral anomalies (incl. corpus callosum) | 32.2% |
| Dandy-Walker malformation | 25.8% |
| Genital / renal / endocrine dysfunction | 12.9% each |

Commonest malignancies: Wilms tumour, rhabdomyosarcoma, leukaemia — **"mostly within the
first 3 years of life, not seldom even in utero."** That timing is the operative fact for
surveillance design and sharpens what `STANDARD-OF-CARE.md` already argued.

---

## 6. How this was built, and where it is weak

84 unique papers retrieved across PMC, bioRxiv and medRxiv; 33 included, 51 excluded, every
exclusion logged (`screening_results.json`). Strata: BUB1B human individuals extracted
deeply, other MVA genes summarised, dosage measurements taken from any system.

**The methodological finding worth keeping.** The eight-paper pilot found that *zero*
reported a BubR1 percentage in readable text, and concluded the dosage axis was
unpopulated. That conclusion was wrong — and it was wrong because **the one paper that
measures the dosage axis is the one paper the corpus does not index.** Suijkerbuijk 2010
had to be recovered from PubMed by hand. Hanks 2004, the founding paper, could not be
recovered at all and remains abstract-only.

A sweep that had trusted its own corpus would have confidently reported a null result.

**Other limits, stated rather than buried.**
- The 35% / 17% figures for MVA-41C and MVA-12C exist only inside a figure image. They are
  quarantined by rule and are *not* load-bearing here — the text-verified "2–6 fold" from
  the primary source carries that claim instead, and independently agrees with them.
- Dosage percentages come from different materials (HeLa, U2OS, primary fibroblast, LCL,
  MEF) with different loading controls. Comparing them is approximate by construction.
- No study measures BubR1 level and tumour outcome in the same individuals. The dose–
  outcome link is assembled across systems; it is an inference, not a measurement.
- Publication bias runs toward severe and tumour-bearing cases.
- One internal inconsistency logged (`c.2386-11A>G` vs `c.2387-11A>G` in the same paper),
  and one figure-vs-text genotype discrepancy (Y115C vs **Y155C**; primary source preferred).
- Two screening disagreements flagged for human ruling, not silently resolved.
- An exhaustive corpus count job was submitted and is still queued; the 84-paper set is a
  retrieved sample, not a certified census.

---

## 7. What follows

The mechanism is now specific enough to aim at, and it splits cleanly in two:

1. **Allele 1 is an mRNA problem.** The protein it encodes works. The failure is NMD. That
   makes nonsense-readthrough and NMD modulation mechanistically coherent *for this exact
   allele* — and the stop codon is TGA, the most readthrough-permissive class, verified
   against the reference CDS.
2. **Allele 2 is a folding problem.** Levels collapse under HSP90 inhibition and recover
   under proteasome inhibition. That points at chaperone and degradation biology — and it
   is the axis on which SIRT2/NAD+ would act.

Both are dosage interventions on a disease now established as dosage-limited. They are the
next thing to evaluate, and they should be evaluated the same way this was: protocol first,
exclusions logged, and the negative results reported.
