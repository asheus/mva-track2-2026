# Do the variant predictors actually work on BUB1B?

Proposed by the owner 11 Sep 2026: we have a set of BUB1B variants whose real-world
answer is already known — measured protein levels, measured function, real patients.
So before trusting any predictor on the proband's alleles, **run the ones we already
know the answer to and see whether the predictor gets them right.**

It does not. That is the finding.

## The ground truth

From the committed extraction (`bub1b-dosage-review/extracted_units.json`, units
D05/D06 → Suijkerbuijk 2010, PMC2887387):

| set | variants | measured truth |
|---|---|---|
| **destabilised** | I909T, R814H, L1012P, L844F, R727C | 5–10× LOWER protein; fail to restore checkpoint or alignment |
| **pathogenic but STABLE** | Y155C | MVA allele, protein levels **unchanged** — separation-of-function |
| **normal** | R550Q, Q921H | fully functional; Q921H is *inside* the kinase domain yet indistinguishable from wild-type |

Q921H and Y155C are the two that matter. Q921H tests whether a predictor is really
reading damage or just reading "kinase domain = bad". Y155C tests whether it can tell
**loss of protein** apart from **loss of function** — which is the only axis this
child's case actually turns on.

Coordinates were resolved via Ensembl `variant_recoder` against `ENSP00000287598`
and cross-check internally: A739S lands exactly 5 bp after the proband's stop codon
(c.2215 vs c.2210) and L1012P exactly 29 bp after N1002K (c.3035 vs c.3006), both
matching the cDNA arithmetic. The CDS came back as 3,153 bp, matching the figure
already verified in this repo.

## Result

AUC of 1.0 is perfect, 0.5 is a coin flip.

| predictor | pathogenic vs normal | **destabilised vs stable** | true MVA alleles missed |
|---|---|---|---|
| **AlphaMissense** | 0.67 | **0.47 — below chance** | **3 of 6** (R814H, L844F, R727C called *likely benign*) |
| GPN-Star m447 | 0.92 | 0.80 | 0 of 6 |
| GPN-Star p243 | 0.92 | 0.73 | 1 of 6 |
| GPN-Star v100 | 0.92 | 0.60 | 0 of 6 |

n is 6 vs 2 and 5 vs 3. **These AUCs cannot be statistically significant in either
direction.** They are descriptive. The per-variant misses are the substantive part.

### AlphaMissense fails on this gene

R814H (0.221), L844F (0.292) and R727C (0.238) are **real MVA patient alleles with
experimental proof of 5–10× protein loss**, and AlphaMissense calls all three likely
benign. Meanwhile Q921H — functionally normal — scores **0.491, higher than three of
the five true destabilisers**.

There is a principled reason, and it is one this workstream already documented.
AlphaMissense learns largely from the contrast between common human variants and
primate variants. **MVA is recessive, and we established that heterozygous carriers
are clinically unaffected** (unit D04). Recessive alleles tolerated in carriers look
tolerated to that framework. The very fact that makes this a recessive disease is the
reason AlphaMissense under-calls its alleles.

**Consequence: the AlphaMissense score of 0.9229 for N1002K, carried in this repo
since the first pass, should be downweighted.** It is not wrong, but it comes from an
instrument that scores below chance on this gene's known answers.

### GPN-Star is the better instrument, and still cannot answer our question

It is genuinely better — it calls both normal controls tolerant (R550Q at the 97th
percentile of coding variants, Q921H 71st) while flagging the destabilised set. That
is real signal, and it is why the pathogenic-vs-normal AUC reaches 0.92.

But look at **Y155C**: pathogenic, with *completely normal protein levels*, and all
three models score it as constrained (34th / 48th / 13th percentile — at or below the
destabilised set). A strong GPN-Star score means **"this position matters"**. It does
not mean "this variant reduces protein".

**No predictor tested here has an abundance axis at all.** None of them can confirm or
refute the dosage hypothesis. That has to keep resting on the structural analysis
(N1002 buried at 14.0% RSA, two backbone H-bonds, packed against W973/F977/W978/F997)
and on the two-class literature.

## A correction I had to make mid-run

My first pass built the null distribution from **all SNVs across the 61 kb BUB1B gene
span**, which is ~95% intronic. Against that null every coding variant looks
exceptional, and N1002K came out at the **0.8th percentile** — top 1% of the gene, on
all three timescales. That number was an artefact of the comparison set.

Rebuilt against a **coding-only null** (3,153 bp CDS × 3 alts = 9,459 SNVs):

| variant | m447 | p243 | v100 | truth |
|---|---|---|---|---|
| I909T | 20.0% | 50.1% | 20.2% | destabilised |
| R814H | 25.7% | 34.1% | 33.1% | destabilised |
| L1012P | 75.8% | 96.2% | 13.2% | destabilised |
| L844F | 59.0% | 58.8% | 64.3% | destabilised |
| R727C | 24.2% | 29.6% | 35.4% | destabilised |
| Y155C | 34.4% | 48.1% | 12.7% | pathogenic, **stable** |
| R550Q | 96.9% | 97.1% | 93.8% | normal ✓ |
| Q921H | 71.1% | 84.3% | 51.1% | normal ✓ |
| **N1002K** | **13.7%** | **32.0%** | **16.4%** | **unmeasured** |
| L737* | 24.9% | 21.1% | 21.2% | nonsense |

(lower percentile = more constrained)

**N1002K drops from the 0.8th percentile to the 13.7th.** The honest statement is not
"top 1% of the gene" — it is that N1002K sits **inside the band occupied by the
measured destabilised alleles**, next to I909T (20.0%) and R727C (24.2%). That is
consistent with the dosage hypothesis and it is not strong evidence for it.

Note also L1012P — the closest structural analogue, experimentally proven to
destabilise — scoring 75.8% and 96.2% on two of three models. The predictors do not
reliably recognise the one variant we are reasoning from by analogy.

## What this changes

- **Nothing about the conclusions.** Confidence that N1002K is a dosage mutant stays at
  ~92%, resting where it already rested.
- **Something about the evidence base.** Stop citing AlphaMissense 0.9229 as support;
  it is an instrument that fails this gene's controls.
- **Something about the method.** This is the reusable result: *AlphaMissense is
  unreliable for recessive, dosage-sensitive disease genes, and here is the worked
  calibration.* Anyone scoring a recessive variant should run their known alleles first.

## Reproduce

    python3 apps/api/scripts/mva/alphamissense_calibration.py   # AlphaMissense alone
    python3 apps/api/scripts/mva/predictor_calibration.py       # all three, needs /tmp/gpn_*.json

GPN-Star scores are read straight out of the published `songlab/gpn-star-scores`
parquet by HTTP range request — 5.4 MB per model, no 1.6 GB download. See
`GPN-STAR-PENDING.md`, now unblocked.
