# Gero / ct-validation — what it can and cannot do for this case

24 Oct 2026. Assessed at the user's request from Fedichev's launch post and the
peer-reviewed paper.

**Paper.** Kostiuk, Igumnov, Fedichev, Feizi. *ct-validation: an open framework
for benchmarking target-indication evidence against clinical trial outcomes.*
Bioinformatics, 20 Oct 2026 — four days old.
[PMID 42900515](https://doi.org/10.1093/bioinformatics/btag788). GERO PTE. LTD.,
Singapore. Code `gero-science/ct-validation`; archived at
[Zenodo](https://doi.org/10.5281/zenodo.22901497); interfaces in Python, CLI and
MCP.

## First, the thing that has to be said plainly

**Gero's target-discovery platform is not accessible.** The substack describes
it at a high level only — generative models over "biological and clinical data",
plus a "gerophysics" stability framing — and names no architecture, no cohort
and no route to access. There is no API, no commercial offering and no
collaboration path described. We cannot run Gero on this child's genotype.

What is open is the **benchmark**, not the discovery engine.

## Second, ct-validation cannot be pointed at this problem

It evaluates whether an **evidence source** — a whole corpus of
target–indication pairs — is enriched for progression through clinical phases.
It needs many pairs and it needs trial outcomes for them.

We have **one target and one ultra-rare disease with essentially no trials.**
Feeding BUB1B-MVA to a tool whose unit of analysis is population enrichment over
~2.2 million pairs returns an empty or uninterpretable table. Asking it to score
our single target is a category error, not a hard run. Installing it was blocked
by the sandbox in any case, and that cost us nothing worth having.

## Third — and this is why it was worth the hour — it supplies two things we need

### 1. An external prior on our evidence class

The benchmark's whole point is that evidence classes are not equal. Per the
launch post, on curated trials **ClinVar Mendelian evidence was the strongest
predictor of clinical progression (~4.4×) and common-variant GWAS the weakest
(~1.9×)**.

This child's target rests on **ClinVar-grade Mendelian evidence**: a defined
pathogenic compound-heterozygous genotype in a gene with an established
Mendelian disease. That is the top evidence tier in the benchmark.

What that buys us is a clean separation our own report has been blurring:

| question | answer | evidence |
|---|---|---|
| Is this the right target? | **Yes** — top evidence tier by the strongest external criterion available | ct-validation / Minikel |
| Can an approved drug reach it? | **No** | our own exposure dossier |

Our problem was never target validity. It is druggability and exposure — which
ct-validation explicitly does not measure. Saying so with an external benchmark
behind it is stronger than asserting it.

> **CAUTION.** The 4.4× / 1.9× split is from the **substack post**, not from the
> paper abstract, which reports only the 3×3 source-comparison figures. It is
> **unverified** against the full text. Do not ship it without checking the
> paper's supplementary data. Same discipline that downgraded C51.

### 2. An independent, population-scale confirmation of our repurposing finding

This is the part that genuinely strengthens the submission.

The paper's own headline caveat, quoted from the abstract: aggregating open
clinical trial registries **compresses relative success from ~2.9 to RS = 1.52**,
and *"this loss is primarily driven by the breadth of the indication data rather
than the genetic evidence."* The launch post is more explicit about the cause —
inflated base rates from indications listed for **exploratory and repurposing
trials**.

Read that against what we found by hand today:

- amlexanox hits TBK1/IKKε 10–100× below its NMD range
- perphenazine causes movement disorders below its PP2A range
- momelotinib inhibits JAK2 9.5× before it touches Aurora B

We derived a **mechanism** for why repurposing underperforms: the activity being
borrowed is an off-target, and therefore by construction weaker than the one the
drug was approved for. Gero, independently and from 2.2 million target–indication
pairs, measured the **population statistic** of the same phenomenon — repurposing
indications are listed promiscuously and progress at materially lower rates.

That converts our structural claim from "we noticed this three times in one
afternoon" into a mechanistic account of an effect someone else has quantified
at scale, in a peer-reviewed paper, four days old.

**This is the citation to carry into the report**, next to the closed-routes
table and the pitch opener.

## Fourth, one framing worth noting and not over-claiming

Gero's "gerophysics" premise — that aging and chronic disease are a system
losing stability, and that good targets act on the **underlying dynamics rather
than the symptoms** — maps onto MVA unusually well. MVA *is* a stability-loss
disease, at the level of the chromosome rather than the organism, and every
route we closed was a symptom-level intervention while the one node that
survived (PP2A-B56 recruitment / APC-C restraint) is a dynamics-level one.

That is a resonance, not a result. It is worth one sentence in a talk and no
weight in an argument.

## Verdict

Cannot be run on this problem, and should not be. Supplies one external prior
that strengthens our target choice, and one peer-reviewed quantitative backing
for the structural finding that was already our best idea. Net: a citation and a
framing, acquired cheaply, with the 4.4×/1.9× figure flagged as unverified.
