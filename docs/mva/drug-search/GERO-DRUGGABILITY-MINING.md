# Mining Gero's benchmark deposit — the whitespace, quantified

24 Oct 2026. Follow-on to `GERO-CT-VALIDATION.md`, which concluded the benchmark
*tool* cannot score a single target. That conclusion stands. But the deposit it
ships is something else: a curated, five-source **drug–target–indication table**,
and that can be mined directly for chemical matter.

**Source.** `ct-validation` benchmark data, Zenodo
[doi:10.5281/zenodo.22901451](https://doi.org/10.5281/zenodo.22901451),
accompanying Kostiuk *et al.*, *Bioinformatics*, 20 Oct 2026
([PMID 42900515](https://doi.org/10.1093/bioinformatics/btag788)). We used the
**data only** — their package was never installed, so nothing here depends on
their code being correct. Queries: `apps/api/scripts/mva/gero/`.

**Universe.** 107,407 gene–drug pairs over 6,316 genes, from five independent
sources:

| source | rows | genes |
|---|---|---|
| DGIdb | 77,174 | 5,026 |
| STITCH | 62,124 | 2,994 |
| OpenTargets | 17,002 | 1,516 |
| ChEMBL | 10,172 | 1,372 |
| TrialPanorama | 3,895 | 767 |

---

## Finding 1 — the convergent node has no chemical matter at all

Every APC/C subunit and coactivator queried — **CDC20, FZR1 (CDH1), CDC27,
ANAPC1, ANAPC2, ANAPC4, ANAPC5, ANAPC7, ANAPC10, ANAPC11, ANAPC13, ANAPC15,
ANAPC16, CDC16, CDC23, CDC26** — returns **zero drug annotations in all five
sources.** Not sparse. Not low-confidence. Absent.

This is the hardest version of a claim we have been making softly all project.
The node where both of this child's alleles converge, and where the only
validated rescue in the literature acts (Sansregret 2017, 90% → 34%
missegregation), has **no annotated chemical matter in the union of five curated
drug–target databases.** proTAME and apcin are real, and they are absent from
every one of these resources.

For the report this replaces "no approved drug does specific APC/C inhibition"
— which was an argument — with a count.

## Finding 2 — the PP2A axis has eight named drugs, and the real one points backwards

Filtering the whole PP2A axis (catalytic, scaffold, all five B56 regulatory
subunits, PTPA, SET, CIP2A) to annotations that actually **name a compound**:

| gene | drug | source | annotated action |
|---|---|---|---|
| PPP2CA | **LB-100** | DGIdb & OpenTargets | **inhibitor** |
| PPP2CB | **LB-100** | DGIdb & OpenTargets | **inhibitor** |
| PTPA | **LB-100** | DGIdb | — |
| PPP2R5D | fluorouracil | DGIdb | — |
| PPP2R5D | cyclophosphamide | DGIdb | — |
| PPP2R5D | epirubicin | DGIdb | — |
| CIP2A | gemcitabine | DGIdb | — |
| SET | molibresib | ChEMBL | — |

Read it honestly and only one row is a real drug–target relationship: **LB-100,
and it is a PP2A *inhibitor*.** The others are cytotoxic chemotherapeutics with
untyped DGIdb associations — almost certainly downstream expression effects, not
target engagement — plus one BET inhibitor against SET.

**So the single genuine clinical-stage PP2A-directed compound has the wrong
sign for this disease.** A naive "find a PP2A drug" search returns LB-100 and
would be pointed exactly backwards: this child needs *more* PP2A-B56 activity at
the kinetochore, not less. There is **no PP2A activator anywhere in the table.**

That is the trap this dataset catches, and it is worth more than a candidate.

## Finding 3 — the interpretation trap, which nearly caught us

On a first pass the aggregated table appeared to show **CIP2A with 11 drugs, 10
of them "inhibition", max_phase 4** — which would have been a thrilling lead,
since CIP2A is an endogenous PP2A inhibitor and blocking it de-represses PP2A.

It is an artifact. Two mechanisms, both severe:

1. **STITCH rows carry no drug name: 0 of 31,419 (0.0%).** Across the whole
   aggregated table, only 70.7% of rows name a compound. Ten of CIP2A's eleven
   "drugs" were nameless STITCH co-occurrence associations. The eleventh was
   gemcitabine.
2. **`max_phase` is a gene-level attribute, not a target-level one.** It is the
   highest phase reached by *any* drug loosely annotated to that gene, for *any*
   indication. CIP2A's "phase 4" rows are gemcitabine's own oncology approvals.
   **Nobody ever ran a trial against CIP2A.**

Any pipeline that counted rows and read `max_phase` as evidence of target
validation would have produced a confident, wrong, repurposing hit here — and
the same trap is live for SET, whose "phase 4" indications include *torsades de
pointes* and *peripheral arterial disease*.

This is the same failure mode as the cell-cycle confound that has shaped this
whole project: a number that measures something adjacent to what you want, read
as though it measured the thing itself.

---

## What this adds, and what it does not

**It did not find a drug.** Mined honestly, the table contains no repurposing
candidate for this child that survives inspection.

**It did something more useful.** It converts our central negative from an
argument into a measurement:

> Across five curated drug–target databases spanning 107,407 gene–drug pairs,
> the APC/C — the node where both of this child's alleles converge — has zero
> annotated compounds, and the one clinical-stage PP2A-directed molecule is an
> inhibitor, which is the wrong direction.

That is a defensible, reproducible, externally-sourced statement of exactly
where the whitespace is. Combined with Sansregret's 90% → 34% it gives the
submission its strongest single pairing: **a node with quantified therapeutic
proof-of-concept and quantified zero chemical matter.**

Which is the honest shape of this project's answer. Not "here is a drug." Here
is the target that should be drugged, the evidence that drugging it would work,
the measurement showing nobody has, and — from the exposure dossier — the
arithmetic showing why every borrowed alternative fails.
