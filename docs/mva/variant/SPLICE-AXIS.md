# The non-coding half, scored at last

Every analysis in this branch until now scored **protein**. The atlas audit found that
ClinVar holds **456 intronic and 15 splice-site** BUB1B records the protein-level
aggregate cannot even represent, and that four of the corpus's established MVA alleles
are splice variants that no missense predictor can see. This closes that gap for the
four.

Reproduce with `splice_coords.py` (coordinates) and the committed
`data/variants/pangolin_splice_scores.csv`.

## Result

| variant | splice **loss** | at offset | cryptic **gain** | what is known |
|---|---|---|---|---|
| `c.1288+5G>A` | −0.73 | **−5** | 0.49 | biallelic; MDS with monosomy 7 at 9y |
| `c.1402−5A>G` | −0.69 | **+5** | 0.85 | biallelic; neuroblastoma at 8mo, survived |
| `c.2386−11A>G` | −0.71 | **+11** | 0.76 | biallelic, same individual |
| `c.2009+1G>A` | **−0.89** | **−1** | 0.73 | canonical donor; breast + gastric cancer |

All four are predicted splice-disrupting. The canonical donor variant scores strongest,
as it must.

**The internal validation was not designed for and is the most convincing part.**
Pangolin is given only a genomic coordinate and an allele — it never sees the HGVS
notation. Yet the offset at which it places the splice loss reproduces the intronic
offset in each variant's name exactly: −5 for `+5`, +5 for `−5`, +11 for `−11`, −1 for
`+1`. Four independent agreements between a sequence model and a coordinate mapping
built by hand.

Each variant also creates a **cryptic site nearby** (gain 0.49–0.85), so the likely
consequence is not clean exon skipping but use of an alternative site — frameshift
territory, consistent with these being loss-of-function alleles in a gene where
55 of 69 pathogenic alleles truncate.

## Two things that had to be fixed first, both of which would have produced garbage

**A transcript mismatch.** `c.2577+5G>A` is in the corpus as an MVA splice allele, and it
**cannot be interpreted against our CDS model**: position 2577 sits inside exon 20
(CDS 2536–2678), not at a boundary, so a "+5 intronic" offset is meaningless. The
coordinate it produced carries a **T** in GRCh38 where the notation claims **G**. The
source (PMC10545765) used `NM_001211.5`; our exon model is a different transcript. It is
**dropped**, not scored, until the transcript is resolved. `splice_coords.py` now asserts
that every variant lands on a real exon boundary before it will emit anything.

**Unverified reference alleles.** The first submission was built without checking that the
computed positions actually carry the claimed reference base. Checking against Ensembl
caught the `c.2577+5` mismatch — 1 of 7. The mapping is now validated two ways: against a
variant whose genomic coordinate is known independently (the proband's `L737Ter`,
`c.2210T>G` = `chr15:40,209,701`, exact match) and base-by-base against GRCh38.

## A self-inflicted failure worth recording

> **PARTLY WRONG, corrected 14 Oct 2026.** The diagnosis below blames the deep-exonic
> coding controls. The real trigger is a **multi-gene annotation** at the variant's
> position, which breaks Pangolin's CSV writer and fails the whole job; distance from a
> splice site is not the cause. Scoring allele 2 — 48 nt from an acceptor, so *not* far
> from a site — failed when paired and succeeded alone. The prescription below
> ("diagnose by bisection") was right and is how this was found. See
> `SPLICE-ALLELE2.md` and `CORRECTIONS-2026-10-06.md` C25a. Operational rule: **one
> variant per job** in any overlap region.


Three Pangolin jobs failed before this one. The cause was **not** the coordinates or the
format — it was the two *coding* variants I added as negative controls. A single variant
ran fine; all four splice variants together ran fine; adding the deep-exonic controls
killed the job. Pangolin is built for variants near splice sites, and a control far from
any site is not a null result, it is an error. Diagnose by bisection before assuming the
input is wrong.

## What is still unscored

Four variants is not the non-coding half. ClinVar holds 456 intronic and 612 synonymous
BUB1B records, none of which has been scored by anything here. The obstacle is coordinate
mapping at scale — **and, since 14 Oct 2026, the one-variant-per-job constraint above**,
which is what this file previously got wrong when it said "Pangolin would take them in one
job". For a gene with an overlapping readthrough across its 3′ end, that is 1,068 jobs,
not one.

The proband's **allele 2 is now scored** and is a clean negative: gain +0.01, loss 0.00,
control reproducing exactly. `SPLICE-ALLELE2.md`.
