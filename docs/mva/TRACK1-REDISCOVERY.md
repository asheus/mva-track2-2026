# Reaching the answer without being told it

The Track 1 answer in this repository was, until now, **confirmed rather than
discovered**: the causal gene was established before the analysis began and everything
after was mechanism work for Track 2. This is the pipeline that closes that gap. It
starts from the callset and the phenotype and reaches the gene on its own.

**The discipline: no stage of this pipeline names a gene.** Not the index, not the
filters, not the ranker. Every step is a general rule applied to all 20,104
protein-coding genes. If any stage carried a candidate list the exercise would be
worthless.

Run it: `HF_TOKEN=... run_pipeline.sh <workdir> "<comma-separated HPO ids>"`

---

## The cascade

| stage | rule | survivors |
|---|---|---|
| — | CDS index over every protein-coding gene (Ensembl GFF3 116) | **20,104 genes** |
| 0 | all records in the callset | 5,012,204 variants |
| 1a | `FILTER=PASS`, non-reference genotype | 4,740,790 |
| 1b | inside a protein-coding CDS interval | 29,299 in 10,965 genes |
| 2 | gene shows a recessive-compatible pattern (≥1 hom-alt, or ≥2 het) | 26,917 in **8,188 genes** |
| 3a | VEP impact HIGH or MODERATE | −16,600 |
| 3b | rare: max gnomAD AF < 1% (absent counts as 0) | −10,027 |
| 3c | re-test the biallelic pattern on what survived | 83 in **31 genes** |
| 5 | rank by information-content phenotype similarity (HPO) | **rank 1 of 31** |

**Result: the causal gene ranks first**, carrying exactly the pair submitted in
`track1_submission.csv` — a `stop_gained` and a `missense_variant`, both heterozygous.
Score 14.78 against 11.38 for the runner-up.

Most of the reduction is at 3c, not 3a or 3b. Thousands of genes look
compound-heterozygous on raw coding calls; almost none still do once common and silent
variants are removed. That re-test is the workhorse and it is easy to leave out.

## Robustness: leave one phenotype term out

Each of the proband's eight HPO terms was dropped in turn and the pipeline re-ranked.

| term dropped | resulting rank |
|---|---|
| Rhabdomyosarcoma `HP:0002859` | **2** |
| each of the other seven | **1** |

**Seven of eight hold at rank 1.** The single term the result leans on is the presenting
malignancy — which is also the highest information content of the eight (IC 5.53, and
directly annotated to the gene in the public HPO file). That is the honest shape of the
finding: *the tumour is what makes this gene findable*, and a child presenting with the
growth and renal features but no malignancy would be a materially harder case for this
method.

## Two bugs that cost the right answer, and are worth recording

**1. Overlapping genes.** A first draft assigned each variant to the *first* CDS
interval containing it. One of the two causal positions falls inside both the gene and a
readthrough transcript that shares its start coordinate, so the two variants were
credited to two different gene names. Each then held a single heterozygous call, neither
looked recessive-compatible, and **the causal gene was filtered out at stage 2** — the
pipeline returned a clean, confident, wrong answer. Variants are now credited to *every*
gene containing them (`cds_lookup.py`).

**2. Pruning the interval scan by start coordinate alone.** Sorting by start does not
bound the backward search, because a long interval beginning far upstream can still
contain the query. The lookup now walks back using a running maximum of end coordinates,
which is exact.

Both failures were silent. Neither would have been caught by anything except checking
whether the known answer survived each stage — which is exactly why a pipeline like this
should be built against a case whose answer is already known.

## What this does and does not establish

**Does:** the answer is reachable from the callset and the phenotype by general rules,
with no gene named anywhere in the pipeline, and the result survives dropping any single
phenotype term but one.

**Does not:** this is *not* novel-gene discovery. It ranks first partly because the
gene–disease association is already in the public HPO annotation file, including the
tumour term. That is how clinical diagnostics legitimately work — and it means a genuinely
novel gene would not be found this way. The pipeline also scores only protein-coding CDS
variants: **structural variants, deep-intronic and regulatory variants, repeat expansions
and mitochondrial variants are out of scope**, so a negative from it would be weak
evidence of absence.

## Incidental findings — deliberately not published

The ranking's lower reaches contain **30 other genes** with rare, predicted-damaging,
biallelic-compatible calls, several in genes where such findings would be medically
actionable. Those are **potential secondary findings in a living child**, they were not
clinically assessed, and the hackathon DTA forbids resharing the data through any
channel.

So: the cascade counts and the rank-1 result are reported here; **the other genes are
deliberately not named**, and the pipeline's intermediate files (`stage2.json`,
`stage3.json`, `stage5_ranked.json`, `vep_cache.json`) are gitignored and blocked by name
in the public exporter. When the methods form asks how incidental findings were handled,
the answer is: surfaced by the pipeline, not assessed, not reported, not published.
