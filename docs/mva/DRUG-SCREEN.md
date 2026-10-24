# Does any already-safe drug raise *BUB1B*? Four public datasets say no.

**Verdict: no credible candidate.** The one compound that replicates across independent
sources is an Aurora A kinase inhibitor, which raises *BUB1B* by arresting cells in
mitosis — the worst possible drug for a child with a chromosome-instability syndrome.

*Producer: `scripts/mva/bub1b_drug_screen.py`. Libraries from Enrichr, retrieved
22 Oct 2026.*

## The idea was good

We need roughly **1.4×** more BubR1. If some compound already given to humans raises
*BUB1B* — off-target, incidentally, as a side effect of something else — it would clear
the viability gate before we started. Public drug-perturbation data can be asked directly.

Four independent sources, because one is an anecdote:

| library | up-signatures | containing *BUB1B* |
|---|---|---|
| LINCS L1000 Chem Pert, consensus | 5,425 | 52 |
| **RummaGEO Drug Perturbations 2025** (GEO RNA-seq) | 2,678 | 183 |
| Sciplex (single-cell RNA-seq) | 2,302 | 68 |
| Drug Perturbations from GEO | 906 | 19 |

## The trap, and why a naive search is worthless

*BUB1B* is a cell-cycle gene. Its transcript rises whenever more cells sit in G2/M — which
is what happens with any compound that arrests mitosis, and with anything that raises
proliferation. **A plain search for "drugs that raise BUB1B" returns mitotic poisons.**

So every hit is scored against a mitotic module: for a set of size *N* from a ~20,000-gene
background, expected overlap is `panel_size × N / 20000`. Observed-over-expected near 1
means *BUB1B* came up **without** its module. Well above 1 means the compound moved the
cell cycle and *BUB1B* came along.

**Across the 322 *BUB1B*-containing signatures, median observed/expected is 3.36**, against
a background median of 1.0–2.9. The confound is real and it dominates.

## A methodological failure worth recording

My first pass used a hand-picked 20-gene mitotic panel and reported **50 "BUB1B-specific"
hits**, several at observed/expected of exactly 0.00.

That list was meaningless. For a 245-gene LINCS signature, a 20-gene panel gives an
expected overlap of **0.25** — so seeing zero panel genes has Poisson probability 0.78 and
carries no information at all. The threshold had **no statistical power**, and when a power
filter was added (expected ≥ 2), **zero of 322 sets qualified.**

Replacing the panel with MSigDB Hallmark **G2-M Checkpoint + Mitotic Spindle (360 genes)**
raised the expected overlap to 4.8 for a LINCS set and ~30 for a RummaGEO set, giving the
test power on all 322 — and **the hit list changed completely.**

This is the third instrument in this project whose first pass produced a confirming result
that did not survive its own control (C46, the pocket scan, now this). The pattern is
consistent enough to state as a rule: **a specificity test must be checked for power before
its negatives are believed.**

## What survived

**The only cross-library replication is MK-5108** — an Aurora A kinase inhibitor —
at observed/expected **7.36**. It raises *BUB1B* through mitotic arrest. It is exactly the
artefact the control exists to catch, and an investigational anticancer agent besides.

**38 of 322 signatures show *BUB1B* up without the module — and not one replicates across
libraries.** Recurrence within RummaGEO (palmitic acid ×6, dexamethasone ×4, talazoparib
×4) is several datasets from one compendium, not independent methods.

| compound | sets | obs/exp | why it is not the answer |
|---|---|---|---|
| Pioglitazone | 2 | 0.63–0.86 | lowest confound score; single compendium; no replication |
| Dexamethasone, flumethasone, hydrocortisone | 6 | 0.68–1.81 | glucocorticoids recur, but chronic steroids in a growth-restricted child are their own harm |
| **Nicotinamide** | 1 | 1.42 | see below |
| Talazoparib, trametinib, tazemetostat, azacitidine, nilotinib | 7 | 1.28–1.95 | cancer drugs; unsuitable here |
| Palmitic acid, cystine | 8 | 1.66–2.00 | metabolites, not drugs |

## About the nicotinamide hit

It is tempting, given that our lead candidate is an NAD⁺ precursor. **It should not be
counted as convergence**, for two reasons.

**Nicotinamide is a sirtuin product inhibitor** at the concentrations that matter, so its
effect on the SIRT2 axis could be *opposite* to NMN or NR. And this is a **transcript**
observation, whereas our NAD⁺ mechanism is post-translational — SIRT2 deacetylating K668 to
extend BubR1's half-life. Two different layers. The names rhyme; the mechanisms do not.

## The deeper reason this was always a long shot

**Our defect is post-translational.** p.Asn1002Lys makes mRNA normally and is predicted to
be destabilised after translation. Raising transcript would raise the synthesis term — and
steady state is synthesis over degradation, so it would genuinely help — but a transcript
screen was never aimed at the actual lesion.

It was still worth running. It is cheap, it could have returned a safe approved drug, and
the negative is now documented rather than assumed. What it mainly establishes is that
***BUB1B*'s transcript signal is dominated by cell-cycle state**, which makes transcript-level
screening a poor instrument for this gene — a useful thing to know before anyone else
spends time on it.

---

# Part 2 — the same question at the protein level

**Also no.** Of eleven drugs that raise BubR1 protein in public mass spectrometry, **zero
do it without also raising the mitotic module.**

*Producer: `scripts/mva/bub1b_proteomics_screen.py`. Source: Proteomics Drug Atlas 2023 via
Enrichr — 1,747 drug signatures by mass spectrometry, 8,220 proteins measured.*

## Why this was the better question

The transcript screen was aimed past the lesion. p.Asn1002Lys makes mRNA normally and is
destabilised **after** translation, so protein abundance is where the defect lives.
Drug-perturbation proteomics asks it directly.

Two corrections the transcript screen taught us were applied here from the start: the
background is the number of proteins the assay **measured** (8,220), not a nominal 20,000
genes, and the mitotic panel is intersected with that background first — 283 of the 360
module genes are detectable in this assay. With ~148-protein signatures that gives an
expected overlap of ~5, so a low observed count is genuinely informative.

## The asymmetry, which is a result on its own

```
   BubR1 protein DOWN in 52 drug signatures
   BubR1 protein UP   in 11
   -> 4.7x easier to lower than to raise
```

A protein that is easy to lower and hard to raise is exactly what the biology predicts —
BubR1 is actively degraded on a schedule — and it sets the expectation for any therapy
aimed at raising it.

## Every drug that raises BubR1 protein, and why none of them helps

| drug | mitotic observed | expected | obs/exp | reading |
|---|---|---|---|---|
| GW 501516 | 10 | 5.1 | 1.96 | mixed — and banned, carcinogenic in animals |
| Gliclazide | 10 | 4.9 | 2.03 | cell-cycle signature |
| LY 344864 | 23 | 5.0 | 4.58 | cell-cycle signature |
| **Ro-3306** | 27 | 5.1 | **5.26** | **CDK1 inhibitor — see below** |
| Acamprosate | 30 | 5.0 | 5.97 | cell-cycle signature |
| Olaparib | 32 | 5.1 | 6.28 | cell-cycle signature |
| GSK 650394 | 33 | 5.1 | 6.43 | cell-cycle signature |
| Formestane | 43 | 5.1 | 8.50 | cell-cycle signature |
| Betamethasone | 46 | 5.0 | 9.15 | cell-cycle signature |
| PDE-9i | 48 | 5.0 | 9.62 | cell-cycle signature |
| GR79236 | 54 | 5.1 | 10.67 | cell-cycle signature |

**0 of 11 are BubR1-specific.**

## The control validated itself

**Ro-3306 is a CDK1 inhibitor.** It arrests cells at the G2/M boundary, so it is the one
compound on this list we could predict *a priori* must be flagged as a cell-cycle artefact.
The control flags it at **5.26**. A test that failed to catch Ro-3306 would be worthless;
this one catches it without being told.

That matters because the three superficially attractive names here — **acamprosate**,
**gliclazide** and **betamethasone**, all approved, all with long human safety records,
gliclazide used even in neonatal diabetes — would otherwise have looked like exactly the
answer we were hoping for. Acamprosate sits at **5.97** and betamethasone at **9.15**. They
raise BubR1 because they moved the cell cycle in these cells, not because they act on BubR1.

## What both screens establish together

| layer | sources | *BUB1B*-specific hits |
|---|---|---|
| transcript | 4 libraries, 322 signatures | **0 replicating** |
| **protein** | 1,747 MS signatures | **0** |

**The repurposing shortcut is closed on public data**, and for one structural reason:
BubR1's abundance tracks the cell cycle so strongly that it swamps any specific
pharmacological effect in bulk perturbation data.

That is a useful negative. It means a repurposing hit for this gene will not be found by
querying public compendia — it would have to come from an assay that **controls for
mitotic index**, measuring BubR1 per cell at a fixed cell-cycle stage. Nobody has run that,
and it is a cheap thing to specify.

## What it does not rule out

- **Magnitude was never measured.** These are direction calls. Nothing here says whether
  any effect approaches the ~1.4× this genotype needs.
- **One dataset, cell lines, no replication** of any single drug.
- Most importantly: **a drug that raises wild-type BubR1 need not raise a destabilised
  mutant**, which is degraded for a different reason. Our candidates — arimoclomol and the
  NAD⁺ route — are aimed at the mutant's specific defect, and would not be expected to
  appear in a wild-type screen at all.
