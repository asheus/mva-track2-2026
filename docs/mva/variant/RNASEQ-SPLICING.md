# The RNA-seq answer, and the instrument that didn't deserve the claim I made for it

Two things were checked: whether the poison-exon detector works on genes other than the
one it was built for, and what actual RNA-seq says about non-productive splicing in
*BUB1B*. **The instrument failed. The conclusion survived anyway, via the measurement.**

*Junction data: GTEx v8 median junction read counts, retrieved 21 Oct 2026. Producers:
`instrument_validation.py`, `junction_flux.py`.*

## Part 1 — I overstated the instrument, and a blind panel showed it

I wrote that `splice_architecture.py` "answers 'does this gene have a zorevunersen-shaped
target?' for any gene." That rested on **one** positive control, which establishes nothing
about sensitivity: a detector that fires on SCN1A and nothing else looks identical from one
test.

So it was run blind over a panel fixed before any result was seen. Expected positives: the
SR-protein family and TRA2B, which autoregulate by splicing in a frame-disrupting cassette
that sends their own message to decay — the textbook example, discovered decades apart from
SCN1A. Expected negatives: housekeeping genes, including GAPDH with **81** annotated
transcripts, more than *BUB1B*'s 31, to catch a detector driven by transcript count alone.

```
gene      exp   tx  decay  cassettes  frameshift   call
SRSF1       +   17      6          0           0      -   <-- MISS
SRSF2       +   20      6          2           1      +
SRSF3       +   38     14          1           0      -   <-- MISS
SRSF5       +   66     10          3           3      +
SRSF6       +   14      6          0           0      -   <-- MISS
SRSF7       +   83     54          5           3      +
SRSF11      +   90     58          8           6      +
TRA2B       +   29      8          0           0      -   <-- MISS
SCN1A       +   30      6          1           1      +
BUB1B       ?   31     12          1           0      -
GAPDH       -   81     15          0           0      -
ACTB        -   64     14          1           1      +   <-- FALSE POSITIVE

SENSITIVITY  5/9  (56%)        SPECIFICITY  1/2  (50%)
```

**It misses four of nine known poison-exon genes and fires on ACTB.** At 56% sensitivity a
negative call is close to a coin flip, so *BUB1B*'s annotation-based negative was never
worth what I claimed for it.

**The cause is diagnosable.** The filter requiring decay isoforms to be >70% of canonical
length — added to suppress a false positive on *BUB1B*'s first exon — is what breaks it.
SR-protein genes are short and their poison-exon isoforms fall below that bar, so they are
discarded before the frame test ever runs:

```
gene     decay  near-full  cassettes   dropping the near-full filter
SRSF3       14          1          1   9 cassettes, 4 frameshifting
SRSF6        6          0          0   4 cassettes, 3 frameshifting
SRSF1        6          0          0   0  (missed for a different reason)
TRA2B        8          0          0   2 cassettes, 0 frameshifting
```

Dropping it would lift sensitivity to 7/9 — **and flip *BUB1B* to positive**, because
*BUB1B*'s second cassette (124 bp, chr15:40,166,359-40,166,482) frameshifts and survives
only the relaxed filter. So the annotation detector's verdict on our own gene is
**parameter-dependent**: strict filter says no, relaxed filter says yes. That is not a
result, it is a choice, and no amount of care in writing it up would have made it one.

## Part 2 — RNA-seq settles it, independently of all that

GTEx publishes median exon-exon junction read counts per tissue. A junction read is a
molecule that made a splicing decision, so the share of a gene's reads on non-canonical
junctions is the fraction of flux leaving the productive path — the headroom an
upregulating ASO would redirect. No annotation, no filters.

**The control, measured.** SCN1A's poison exon 20N, pooled across 9 brain tissues:
**19 inclusion reads vs 24 skipping — PSI 44.2%.** Roughly half of SCN1A's brain
transcripts include the poison exon and are destroyed. That is why zorevunersen works and
why blocking it can nearly double productive output. (Per-tissue medians are only a few
reads deep, so individual rows reading 100% rest on 2 reads against 0 and are not quoted;
the pooled figure is.)

**Non-canonical share of junction reads, across tissues where each gene is expressed:**

| | BUB1B | SCN1A |
|---|---|---|
| median | **0.00%** | **4.55%** |
| range | 0.00 – 0.17% | 2.70 – 6.56% |
| expressed tissues | 15 | 13 |

*BUB1B*'s entire non-canonical signal is **single digits of reads out of 7,270** summed
across 54 tissues.

**And both annotation candidates are measured at zero:**

| candidate | inclusion reads | skipping reads | PSI |
|---|---|---|---|
| 54 bp, in-frame (strict filter keeps) | 0 | 204 | **0.000%** |
| 124 bp, frameshifting (relaxed filter only) | 1 | 268 | **0.371%** |
| *SCN1A exon 20N, for scale* | *19* | *24* | ***44.2%*** |

So the parameter-dependence in Part 1 doesn't matter: **the relaxed filter's "positive" is
measured at 0.371%.** RNA-seq overrules both settings and returns the same answer.

**On the obvious objection** — that bulk post-mitotic tissue is the wrong place to look for
a mitotic gene — GTEx contains two proliferating sample types, EBV-transformed lymphocytes
and cultured fibroblasts, and they are exactly where *BUB1B* is best expressed (3,478 and
623 median junction reads). They show 0.2% and 0.0%. That is the right place to look, and
it is where we looked.

## What stands

**There is no usable non-productive splicing flux in *BUB1B* to redirect.** SCN1A diverts
~44% of its brain message through a poison exon; *BUB1B* diverts essentially none. The
39% decay-biotype annotation that made this idea attractive is not visible in reads at all.

The splice-modulating ASO route is **closed on the evidence available**, now for a measured
reason rather than an annotational one. What would reopen it: deep RNA-seq of the patient's
own proliferating cells, where a private or condition-specific event could exist that bulk
GTEx medians cannot resolve. That is a real experiment, and it is cheap, but it is not a
reason to carry the candidate forward today.

## What this says about the submission

The instrument I offered as the durable artefact is **not fit to be offered that way**, and
`splice_architecture.py` now carries its measured sensitivity and specificity at the top of
the file so nobody reuses it believing otherwise. Corrected as **C46**.

What is worth presenting is the pairing: a cheap annotation screen whose answer was
parameter-dependent, and a measurement that resolved it in one query. The screen was wrong
to trust and right to run — it cost minutes and pointed at exactly the two coordinates the
RNA-seq then settled.
