# Every BUB1B variant in the corpus, scored

All 37 BUB1B variants this workstream has encountered in the literature, by domain,
with both predictors' scores against the proband's two alleles.

**Read the AlphaMissense column with the calibration in mind** — `PREDICTOR-CALIBRATION.md`
shows it scores *below chance* on this gene's destabilisation axis. It is shown for
completeness, not as evidence.

GPN-Star percentiles are against a **matched null**: coding variants against all 9,459
coding SNVs in the CDS, intronic variants against the intronic SNVs of the gene span.
Mixing the two inflates every coding variant by roughly tenfold. **Lower = more
constrained.** Three columns are three evolutionary timescales (m447 = 447 mammals,
p243 = 243 primates, v100 = 100 vertebrates).

† = the amino-acid change can arise from more than one single-nucleotide change and the
primary source does not say which; all candidates are shown.

| variant | pos | domain | AlphaMissense | m447 | p243 | v100 | what is known |
|---|---|---|---|---|---|---|---|
| R120Q | 120 | TPR | 0.607 LPath | 20% | 23% | 13% | prostate cancer predisposition, monoallelic |
| I147T | 147 | TPR | 0.498 Amb | 34% | 42% | 22% | prostate ca; in-silico 'greatly destabilising' |
| Y155C | 155 | TPR | 0.538 Amb | 34% | 48% | 13% | MVA-41C w/ 731X. PATHOGENIC, protein levels UNCHANGED |
| F175L † | 175 | TPR | 0.805 LPath | 31%/18%/21% | 24%/14%/21% | 28%/12%/14% | reference point: stable |
| F175G | 175 | TPR | 0.989 LPath | — | — | — | reference point: unstable [not a single-nucleotide change - GPN-Star n/a] |
| R194* | 194 | TPR | n/a | 10% | 4% | 28% | nonsense, biallelic w/ R770Q |
| R244C | 244 | linker / unassigned | 0.519 Amb | 12% | 14% | 15% | prostate ca; little effect in silico |
| K250R | 250 | linker / unassigned | 0.082 LBen | 69% | 66% | 76% | PCAF acetylation site. Mouse K243R homozygote EMBRYONIC LETHAL |
| E413K | 413 | GLEBS | 0.929 LPath | 6% | 7% | 3% | reference point: unstable |
| R416Q | 416 | GLEBS | 0.666 LPath | 12% | 15% | 9% | prostate ca; little effect in silico |
| R550Q | 550 | linker / unassigned | 0.066 LBen | 97% | 97% | 94% | MEASURED: fully functional |
| W722R | 722 | linker / unassigned | 0.903 LPath | 19% | 45% | 38% | recurrent pregnancy loss, PCS 13.79% |
| R727C | 727 | linker / unassigned | 0.238 LBen | 24% | 30% | 35% | MVA w/ 386X. MEASURED: 5-10x reduced |
| **L737*** | 737 | linker / unassigned | n/a | 25% | 21% | 21% | *** PROBAND ALLELE 1 *** NMD-competent |
| A739S | 739 | linker / unassigned | 0.074 LBen | 82% | 82% | 79% | recurrent pregnancy loss; 2 residues from proband stop |
| R770Q | 770 | pseudokinase | 0.068 LBen | 96% | 91% | 99% | biallelic w/ R194*; died 6mo. **VUS, causality disclaimed by its authors** — see note |
| R814H | 814 | pseudokinase | 0.221 LBen | 26% | 34% | 33% | MVA-12C w/ 753X. MEASURED: 5-10x reduced |
| L844F | 844 | pseudokinase | 0.292 LBen | 59% | 59% | 64% | MVA. MEASURED: 5-10x reduced |
| R893S | 893 | pseudokinase | 0.579 LPath | 40% | 31% | 36% | MVA1 monoallelic, also in unaffected father |
| I909T | 909 | pseudokinase | 0.451 Amb | 20% | 50% | 20% | MVA w/ null allele. MEASURED: 5-10x reduced |
| Q921H † | 921 | pseudokinase | 0.491 Amb | 71%/68% | 84%/84% | 51%/52% | MEASURED: indistinguishable from wild-type |
| R999Q | 999 | pseudokinase | 0.112 LBen | 40% | 55% | 47% | annotated neighbour of the proband's residue |
| **N1002K** | 1002 | pseudokinase | 0.923 LPath | 14% | 32% | 16% | *** PROBAND ALLELE 2 *** |
| N1004S | 1004 | pseudokinase | 0.048 LBen | 99% | 97% | 99% | annotated neighbour |
| D1005E † | 1005 | pseudokinase | 0.152 LBen | 47%/54% | 36%/41% | 64%/72% | annotated neighbour |
| L1012P | 1012 | pseudokinase | 0.872 LPath | 76% | 96% | 13% | MVA. MEASURED: 5-10x reduced. Closest structural analogue |
| c.1288+5G>A | — | intronic | n/a | 6% | 8% | 3% | splice, biallelic; MDS w/ monosomy 7 at 9y |
| c.1402-5A>G | — | intronic | n/a | 3% | 1% | 1% | splice, biallelic; neuroblastoma 8mo, survived to adulthood |
| c.2386-11A>G | — | intronic | n/a | 7% | 37% | 4% | splice, biallelic, same individual |
| c.2577+5G>A | — | intronic | n/a | — | — | — | splice, biallelic; embryonal rhabdomyosarcoma |

### In the corpus, scoreable by neither predictor

| variant | pos | domain | why not | what is known |
|---|---|---|---|---|
| Q386X | 386 | linker / unassigned | exact cDNA unknown | truncating; MVA w/ R727C. Exact cDNA not in our corpus |
| L731X | 731 | linker / unassigned | exact cDNA unknown | truncating; MVA w/ Y155C. Reported to RESCUE when re-expressed |
| L753X | 753 | linker / unassigned | exact cDNA unknown | truncating; MVA w/ R814H. Reported to FAIL. 22 residues from 731X |
| p.Glu391del | 391 | linker / unassigned | indel / structural | in-frame deletion; prostate ca; reduces stability |
| c.498_505del | — | — | indel / structural | 8 bp deletion, biallelic; MDS |
| c.2405_2406del | 802 | pseudokinase | indel / structural | p.Ser802Cysfs*29; embryonal rhabdomyosarcoma |
| Alu ins intron 8 | — | — | indel / structural | structural variant - missed by exome SNV calling |

---

## How to read this

### Where the predictors agree with reality

| variant | AM | GPN m447 | truth |
|---|---|---|---|
| R550Q | 0.066 | 97% | measured **normal** ✓ |
| Q921H | 0.491 | 70% | measured **normal** ✓ |
| N1004S | 0.048 | 99% | neighbour, presumed tolerated ✓ |
| E413K | 0.929 | 6% | reference point: **unstable** ✓ |

Both predictors get the clear negatives right, and GPN-Star gets them right decisively
(R550Q and N1004S sit in the most tolerant few percent of the whole coding sequence).
That is real signal and it is why the calibration AUC is not zero.

The splice variants are GPN-Star's clearest win, because AlphaMissense cannot score them
at all: `c.1402-5A>G` lands at the **1st–3rd percentile** on all three timescales, and
`c.1288+5G>A` at 3–8%. A protein-only predictor is blind to a third of the pathogenic
alleles in this table.

### Two failures that matter more than the averages

**K250R — called benign by everything, and lethal in the animal.** AlphaMissense 0.082
(*likely benign*), GPN-Star 69%/66%/76% (*tolerant*). The mouse knock-in of the
equivalent residue produces **no homozygous pups in 339 live animals**, and
heterozygotes develop aneuploidy and spontaneous tumours.

Lysine→arginine conserves charge, size and burial. It looks innocuous to any model
reasoning from physicochemistry or from structure, and largely innocuous to one
reasoning from alignments. What it actually does is **delete an acetylation site**.
**Neither predictor can see a post-translational modification being ablated** — and this
workstream's entire acetylation arm (K250, K668, SIRT2) sits in exactly that blind spot.
Any conclusion there has to come from the biology; the scores are inert.

> **Corrected 15 Sep 2026 after reading the primary source (PMC11306263).** R770Q is
> `c.2309G>A`, rs1422532977, and the aggregate's pathogenic allele at this codon is
> `R770Ter`, `c.2308C>T`, rs750364303 — **two different variants at adjacent nucleotides
> of one codon**, so our transcription was right. But the case does not support the weight
> put on it. The child presented with **sudden unexpected postnatal collapse**, not MVA,
> and died of sepsis following hypoxic-ischaemic encephalopathy. The authors classify
> R770Q a **VUS (ACMG class 3)**, note it "is not reported in scientific literature", and
> state plainly: *"it is not possible to demonstrate the causal effect of this mutation"*.
> Treat it as an architecture-shaped coincidence, not a matched case.

**R770Q — our "architectural match" is called benign by both.** H02 is the child who
looked like the closest published parallel to this proband: a nonsense allele plus a
pseudokinase-domain missense, biallelic, dead at six months. AlphaMissense gives R770Q
**0.068 (likely benign)**; GPN-Star gives **96%/91%/99% — among the least constrained
positions in the gene.**

That is two independent predictors agreeing, and agreeing with the source paper, which
declined to assert causality and said only that the variant *"could play a causal or
concausal role"*. **H02 should be downgraded as a precedent for this case.** It is the
one place in this table where the predictors change a conclusion, and they weaken ours
rather than strengthen it.

### The proband's own alleles

**N1002K** — AlphaMissense 0.923, GPN-Star 14%/32%/16%. Consistently in the constrained
band on every timescale, sitting between I909T (20%) and R727C (24%) — both measured at
5–10× reduced protein. Consistent with the dosage hypothesis. Not proof of it.

**L737\*** — 25%/21%/21%. Modest, and that is expected: a nonsense variant's damage is
not an evolutionary-constraint phenomenon at the single-base level, and no missense
predictor scores it at all. The NMD argument does not rest on these numbers.

### The honest caveat, restated

Look at **L1012P**: 76% / 96% / 13%. Measured, published, proven to reduce protein 5–10×,
and the closest structural analogue to our variant — and GPN-Star calls it tolerant on
two of three timescales. And **Y155C** at 34%/48%/13%, pathogenic with *completely normal
protein levels*, scoring as constrained as the destabilised set.

So the two errors run in both directions: a proven destabiliser looking tolerable, and a
non-destabiliser looking constrained. **No predictor in this table has an abundance
axis.** They rank how much a position matters. They do not say whether a variant
destroys the protein or merely stops it working — and that distinction is the whole case.

## Provenance

Coordinates resolved via Ensembl `variant_recoder` against `ENST00000287598` /
`ENSP00000287598`, and they cross-check: A739S lands exactly 5 bp after the proband's
stop codon, L1012P exactly 29 bp after N1002K, the CDS totals 3,153 bp, the proband's PTC
falls in exon 17 of 23, and the last exon–exon junction is at c.2957 — every one matching
the figures independently recorded elsewhere in this repo.

**One discrepancy logged.** `c.2577+5G>A` (PMC10545765) **cannot be correct for this
transcript**: c.2577 falls 101 bases inside exon 20, not at a splice boundary. The other
three splice variants all land exactly on real boundaries (c.1288, c.1401→1402, c.2385→2386),
so the exon model is right and this one citation is not. It is left unscored. This joins
the Y155C-vs-Y115C and K668-vs-K688 discrepancies already on the record.

Reproduce with `python3 apps/api/scripts/mva/variant_table.py`.
