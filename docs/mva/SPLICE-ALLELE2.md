# Allele 2 scored for splicing: a clean negative, and two instrument defects

Closes the open item named in `CORRECTIONS-2026-10-06.md` C22. Run 14 Oct 2026.
Reproduce with `python3 -m scripts.mva.variants.splice_allele2`; raw output archived
in `data/variants/pangolin_allele2.json`.

## The result

| | gain | loss |
|---|---|---|
| **Allele 2** `c.3006T>G` `p.Asn1002Lys` | **+0.01** | **0.00** |
| Positive control `c.2386-11A>G` | +0.76 | −0.71 |

**No predicted splice effect.** Largest |score| anywhere is 0.01, against a control
that reproduces its committed value exactly. Stable across window widths of 50, 300
and 1000 nt, and identical across all three overlapping gene models.

## Why a missense variant was scored for splicing at all

C22 established that allele 2 creates no stop codon, so there is nothing for an NMD
model to predict — and that it sits in exon 23 of 23, where a PTC would escape NMD by
construction anyway. The one remaining route by which a missense change could still
reach decay is by **creating a cryptic splice site** whose frameshift puts a PTC
downstream.

That route had never been scored. `pangolin_splice_scores.csv` held only the four
known splice alleles. A splice score for allele 2 was quoted to this workstream
during review; it was not ours and was not in our files, so C22 recorded the status
as **unscored** rather than let someone else's number stand in. This closes it.

## What the null actually buys

It is elimination, not discovery, and that is worth stating precisely. Allele 2 could
have failed to produce protein three ways: NMD (excluded by C22, twice over),
cryptic splicing (excluded here), or not at all. **Allele 2 is made as protein.**

So the remaining question narrows from three to two:

| | the protein is… | what a drug would have to do |
|---|---|---|
| **Abundance** | present but scarce — misfolds, cleared by chaperone-dependent QC | raise folding capacity |
| **Interface** | present in normal amount but poorly functional | raising the amount achieves nothing |

Those need opposite interventions, and nothing computational we have separates them.
The nearest thing to a discriminator is the measured precedent in
`bub1b-dosage-review/ESTIMATE.md`: within the kinase domain, **5 of 6 variants whose
protein level was measured are destabilising (83%)**, which is a strong prior for
abundance and not a result. Note also that burial does **not** separate the classes
in that panel — the one tolerated variant, Q921H, is *more* buried than allele 2.

## Two defects in the instrument

### A multi-variant job fails where each variant alone succeeds

The first submission paired allele 2 with its control and **failed** in 33 s.
Bisected: allele 2 alone completed, control alone completed, both at 29 s.

`SPLICE-AXIS.md` had recorded an earlier multi-variant failure and blamed *deep-exonic
negative controls* — "Pangolin is built for variants near splice sites, and a control
far from any site is not a null result, it is an error." **That diagnosis was
incomplete.** Allele 2 is 48 nt from a splice acceptor, not far from one, and it still
killed the job when paired. The real trigger is a variant whose position carries a
**multi-gene annotation**, which breaks Pangolin's CSV writer and takes the whole job
with it. The earlier conclusion was right that bisection is the diagnosis and wrong
about the cause.

So: **one variant per job** for anything in an overlap region.

### The output row for such a variant is column-shifted

Allele 2 sits in a **triple overlap**, confirmed against Ensembl REST:

| gene | span (GRCh38) |
|---|---|
| `ENSG00000156970` **BUB1B** | chr15:40,160,984–40,221,137 |
| `ENSG00000137843` **PAK6** | chr15:40,217,428–40,277,489 |
| `ENSG00000259288` **BUB1B-PAK6** (readthrough) | chr15:40,218,500–40,264,890 |

Pangolin emits a block per overlapping gene, unquoted and comma-bearing, so every
column shifts: `CHROM` reads `T` and `POS` reads `G`. Worse, the format is not even
internally consistent — the first two genes come as pipe-delimited blocks, the **last
one positionally in the row's trailing columns with no pipes at all**. A parser
written for the pipe form silently drops a gene. Ours did, until the gene-set
assertion caught it; that assertion is in the committed script for this reason.

**The readthrough is not a new acquaintance.** `ENSG00000259288` BUB1B-PAK6 is the
same transcript that caused one of the two Track 1 bugs — a first-match gene
assignment split the causal variant pair across BUB1B and its readthrough and
filtered the right answer out entirely (`TRACK1-REDISCOVERY.md`). One genomic
overlap, two independent tools, two silent failures, found months apart. A locus that
breaks tooling twice is worth a standing note rather than a second rediscovery.

## What is still unscored

ClinVar holds 456 intronic and 612 synonymous BUB1B records, none scored by anything
here. Pangolin would take them; the obstacle is coordinate mapping at scale, not
compute — **and now also the one-variant-per-job constraint above**, which makes a
batch sweep of a gene with an overlapping readthrough considerably less cheap than
`SPLICE-AXIS.md` assumed.
