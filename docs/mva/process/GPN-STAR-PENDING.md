# GPN-Star as a third, independent variant predictor — RESOLVED 11 Sep 2026

Raised by the owner 10 Sep 2026: Ye, Benegas, Albors, Li, Prillo, Fields, Clarke &
Song, **"Predicting genome-wide functional constraints with GPN-Star"**, *Nature*,
published **9 September 2026** — [DOI](https://doi.org/10.1038/s41586-026-11005-5),
CC BY 4.0. Metadata and abstract retrieved via Crossref; `www.nature.com` itself
redirects to an auth host that is blocked, so the article HTML/PDF was not read.

## Why it is worth using here

GPN-Star is a genomic language model with a **phylogeny-aware architecture** that
uses whole-genome alignments and species trees to model evolutionary relationships
explicitly, trained across vertebrate, mammal and primate timescales. Per the
abstract it "achieves state-of-the-art performance across a wide range of variant
effect prediction tasks in **both coding and non-coding regions**" and
"substantially outperforms previous methods in prioritizing pathogenic and
fine-mapped GWAS variants."

That makes it a genuinely **orthogonal third line** on our two variants:

| predictor | what it measures | our result |
|---|---|---|
| AlphaMissense | protein-level missense pathogenicity | N1002K = 0.9229, likely_pathogenic |
| AlphaGenome | regulatory / splicing effect | L737* above within-gene null on splice scorers |
| **GPN-Star** | **evolutionary constraint from cross-species alignments** | **done — see PREDICTOR-CALIBRATION.md** |

Three predictors trained on three different signals agreeing would be a much
stronger statement than any one of them. Disagreement would be equally informative
and is the kind of thing the adversarial channel exists to weigh.

The paper's own abstract also notes "task-dependent advantages of modelling more
recent versus deeper evolution", and three human models are published — so the
right analysis scores our variants on **all three timescales** rather than picking one.

## Exactly how to run it (no model inference needed)

The Song lab published **precomputed genome-wide log-likelihood ratios**, so the
variants can be looked up rather than the model run:

- dataset `songlab/gpn-star-scores` on Hugging Face
- per-chromosome parquet at
  `data/gpn-star-hg38-{m447,p243,v100}-200m/llr/llr_chr15.parquet`
  (~1.6 GB each) and equivalent bigWigs `bigwig/.../llr_{A,C,G,T}.bw`
- both our variants are `T>G`, so the value needed is the **G** LLR at
  chr15:40,209,701 and chr15:40,220,612, on each of the three models
- the repo's own `manifest/parquet-layout.json` documents remote **range** queries
  (~10 MB transferred per interval query), so a full download is unnecessary

Null distribution should be built the same way as the AlphaGenome run: random SNVs
inside BUB1B, so the two variants' scores are interpretable rather than free-floating.

## The blocker: Hugging Face moved to Xet storage

Small files from `huggingface.co` work (this document's manifest facts were fetched
that way). **Large files no longer serve from `cdn-lfs*`** — a `resolve` request now
302s to Hugging Face's Xet CDN, and every candidate host is blocked:

```
us.aws.cdn.hf.co          BLOCKED   <- the actual redirect target
cdn.hf.co                 BLOCKED
transfer.xethub.hf.co     BLOCKED
cas-server.xethub.hf.co   BLOCKED
cas-bridge.xethub.hf.co   BLOCKED
```

**This also corrects earlier allowlist advice in this repo's history.** The list
given previously named `cdn-lfs.huggingface.co` and `cdn-lfs-us-1.hf.co`, which are
the *old* LFS hosts. Any large Hugging Face download — including **the gated MVA
hackathon dataset itself** — needs the Xet hosts instead. That is likely to matter
more for the VCF than it does for GPN-Star.

Minimum addition to unblock both:

```
us.aws.cdn.hf.co
cas-bridge.xethub.hf.co
transfer.xethub.hf.co
```

## Status

Everything except the fetch is settled: the paper is identified and its relevance
established, the exact files and coordinates are known, and the null-distribution
method is the one already used for AlphaGenome. Add the hosts and this is a short run.


---

## RESOLVED, 11 Sep 2026

`us.aws.cdn.hf.co` — the actual redirect target named above — now answers **200**.
(`cas-bridge.xethub.hf.co` and `transfer.xethub.hf.co` still 403, and were never
needed.) All three models were read by HTTP **range request** against the published
parquet: **5.4 MB transferred per model, 3 requests**, versus a 1.6 GB download.

One implementation note worth keeping. `fsspec` and `requests` both **re-encode the
URL** when following Hugging Face's signed redirect — `~` becomes `%7E`, `''` becomes
`%27%27` — which invalidates the signature and returns 403. That reads exactly like a
blocked host and is not one. `apps/api/scripts/mva/hf_range_reader.py` drives `curl`
per range read to avoid it.

**This likely also unblocks the gated MVA hackathon dataset**, which was the larger
concern flagged above.

Scores and the calibration they fed are in `PREDICTOR-CALIBRATION.md`. The headline:
GPN-Star clearly outperforms AlphaMissense on this gene's known variants, but neither
predictor can separate loss-of-protein from loss-of-function, so neither settles the
dosage question.
