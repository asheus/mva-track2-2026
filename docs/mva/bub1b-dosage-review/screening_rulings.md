# Rulings on the three items left open at the Evidence checkpoint

Dated 11 Sep 2026. Each was flagged in `screening_results.json` rather than silently
resolved, and each is ruled here on evidence, not by fiat.

## Ruling 1 — SLF2/SMC5 is NOT Stratum B. The screener was right; my flag was wrong.

The disagreement was that PMC9636423 (SLF2/SMC5) was excluded while PMC12691382 (SMC5)
was included. Reading the primary source resolves it, because **the authors draw the
distinction themselves**:

> "Unlike MVA, which typically involves the loss/gain of small numbers of chromosomes, the
> cytogenetic abnormality observed in SLF2 and SMC5 patient cells predominantly involved
> huge chromosomal gains. Therefore, we have termed this cytogenetic abnormality **mosaic
> variegated hyperploidy (MVH)**, i.e., chromosome number >46."

They name it a separate disorder — **Atelís Syndrome** — and elsewhere list MVA as a
distinct subgroup "caused by variants in the spindle assembly checkpoint genes BUB1B,
CEP57 and TRIP13". Mechanism differs too: Atelís arises from replication stress,
G-quadruplex resolution failure and cohesion loss, not from checkpoint dosage.

**RULING: adopt the causal-mechanism criterion, not the clinical label.** Stratum B is
MVA arising from a chromosome-segregation/SAC defect.
- PMC9636423 (SLF2/SMC5, Atelís) — stays excluded from Stratum B.
- PMC12691382 (SMC5, 2025) — **RECLASSIFIED out of Stratum B for consistency**, despite
  that paper self-labelling as MVA. Same gene, same mechanism; the label differs between
  two author groups and the mechanism does not.
- Both are **retained in a new category: PHENOCOPY COMPARATORS.**

Why the phenocopy category earns its place rather than being a tidy-up: these patients
have microcephaly and short stature — the same headline features as MVA — from a
completely different mechanism. That is a standing warning against attributing this
child's neurodevelopmental phenotype to BubR1 dosage merely because the two co-occur.

## Ruling 2 — PMC3613689 demoted to a reference-mining seed.

Ricke & van Deursen 2013, "Aneuploidy in health, disease, and aging", was screened
INCLUDE on the basis of dosage content. It is a narrative review, and protocol eligibility
excludes reviews as evidence sources while retaining them as seeds.

**RULING: demoted.** No value is extracted from it. Its references are mined instead —
which is how the Baker 2004 hypomorph dosage figure entered this review, correctly
attributed to the primary source rather than to the review restating it.

Consistency check applied to the rest of the included set: PMC4213761 (Lee 2014, BubR1
mouse models) is also a review and is **likewise demoted**. No other included record is a
review. Included count falls 33 → 30.

## Ruling 3 — the exhaustive corpus count did not return.

Durable job `38fcaeec-96b0-444b-a357-6aed518d2705`, submitted 10 Sep 2026, remains
`queued` with `queue=13` after ~24 hours. It has not run.

**RULING: the review ships without a certified corpus census, and says so.** The 84-paper
candidate set is a retrieved sample from six ranked searches plus one boolean grep. It is
not a proven-complete enumeration of the BUB1B literature, and no claim in the report
depends on it being one. The job is left queued; if it returns, the count is recorded as
an addendum.

## Net effect on the review

| | before | after |
|---|---:|---:|
| Included | 33 | 30 |
| Stratum B (MVA, other genes) | 9 | 7 |
| New category: phenocopy comparators | 0 | 2 |
| Reviews demoted to seeds | 0 | 2 |

No conclusion in `REPORT.md` changes. The dosage ladder, the two-class model and the
proband placement all rest on Stratum A and Stratum C records, none of which are touched
by these rulings.
