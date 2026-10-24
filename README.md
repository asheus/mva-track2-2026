# MVA Hackathon 2026 — Track 2 (Drug Repurposing)

Submission for *Rare Disease, Real Kid: The MVA Hackathon 2026*, organised by Sage
Bionetworks with the MVA Society, Hugging Face and BEACON.
Submitting username: **mk7790**.

**These are hypotheses for follow-up, not evidence that any medicine works.**
Nothing here is clinical advice. No patient data is redistributed in this
repository: what is committed is the *query*, never the data it read.

---

## The problem

Proband `WGS_EX2312012` carries two BUB1B alleles: **p.Leu737Ter** (c.2210T>G) and
**p.Asn1002Lys** (c.3006T>G). BubR1 is a dosage protein at the kinetochore. Too little
of it and chromosomes missegregate, which is what mosaic variegated aneuploidy is.

The awkward fact about this target: **every cell-cycle drug in clinical use was built to
break the cell cycle.** Oncology and transplant medicine paid for all of it. Nobody ever
needed a drug that makes segregation work *better*, so the chemical matter points the
wrong way.

## The four questions

We made the work answer these in order, and would not let ourselves pick a compound
until each had closed.

| | Question | Answered in |
|---|---|---|
| **Q1** | What do these two alleles actually leave behind — not "pathogenic", but how much protein, with which domains? | `BUB1B-MUTATION-ATLAS.md`, `NMD-STRATIFIED-BUB1B.md`, `N1002-STRUCTURAL-COUPLING.md` |
| **Q2** | Is the deficit reversible at all? If restoring BubR1 does nothing, no drug can work. | `MECHANISM.md`, `MVA-THERAPEUTIC-EVIDENCE-BASE.md` |
| **Q3** | Is there *any* drug that raises BubR1, or its phosphatase? | `APPROACHES-ALL.md`, `GERO-DRUGGABILITY-MINING.md`, `TRIED-AND-FAILED.md` |
| **Q4** | If not, what else sits on the same node — and at what dose? | `THE-PICK.md`, `EXPOSURE-DOSSIER-KOSMOS-LEADS.md`, `DOSAGE-HEADROOM.md` |

## The answer, in one paragraph

Both alleles converge on a single failure: the KARD motif (residues 667–681) that
recruits the phosphatase **PP2A-B56** is never delivered in sufficient quantity. Allele 1
is destroyed by nonsense-mediated decay (73 nt upstream of the last junction); allele 2
is 87% buried and is made, then degraded. With no phosphatase arriving, **Aurora B is not
more active — it is unopposed.** Nothing in the druggable universe raises BubR1 or
activates PP2A, so we propose lowering the opposing kinase instead: **partial Aurora B
inhibition**, with barasertib-hQPA as the characterised tool compound. It is the only
candidate in the whole search whose human exposure sits *above* what the effect needs
(~1,200× IC50), so it is the only one that calls for a dose **decrease**.

**The risk we are not hiding:** this child's checkpoint is already at 15–26% of normal,
and partial Aurora B inhibition synergises with a weak checkpoint. What we propose is a
titration window measured on phospho-Hec1, not a dose.

## Check it in 30 seconds

    python3 apps/api/scripts/mva/verify_report.py

Standard library only, no network. 20 checks, each re-deriving a number the report states
from the committed records rather than from any gate's own summary field.

---

## How the work is organised — six evidence channels

114 committed scripts and 148 data files. No number in the report or the deck exists
without the query that produced it. `docs/mva/INDEX.md` maps all 81 documents; the
channels are:

| Channel | What it establishes | Where |
|---|---|---|
| **1 · Variant interpretation** | Every BUB1B allele scored the same way: consequence call, the 55-nt NMD rule, AlphaMissense + GPN-Star, then the literature for abundance. 2,536 alleles. | `apps/api/scripts/mva/nmd/`, `BUB1B-MUTATION-ATLAS.md`, `PREDICTOR-CALIBRATION.md` |
| **2 · Structure and stability** | Why allele 2 is a dosage mutant and not an interface mutant: burial, ΔΔG, pocket scans, docking controls. | `apps/api/scripts/mva/neurosnap/`, `apps/api/scripts/mva/millet/`, `WHY-BURIED-IS-WORSE.md` |
| **3 · Mechanism from the literature** | What the KARD does, which kinases write it, which phosphatase reads it, and the published proof that restoring BubR1 rescues patient cells. | `MECHANISM.md`, `MVA-THERAPEUTIC-EVIDENCE-BASE.md` |
| **4 · Drug space** | A six-gate funnel over the approved universe, plus an independent mining pass over 107,407 curated gene–drug pairs. Ten therapeutic arms, four themes. | `apps/api/scripts/mva/gate*.py`, `apps/api/scripts/mva/gero/`, `APPROACHES-ALL.md` |
| **5 · Exposure and safety** | Every surviving arm closed on a *measured human number* — achievable free plasma concentration against the concentration the effect needs — and on paediatric safety. | `EXPOSURE-DOSSIER-KOSMOS-LEADS.md`, `DOSAGE-HEADROOM.md`, `gate3_safety.py` |
| **6 · Adversarial review** | Deliberate attempts to refute our own conclusion, and the record of where they succeeded. | `COUNTER-ARGUMENT.md`, `GATE4-ADVERSARIAL.md`, `GATE4-ROUND2-SELF-REFUTATION.md`, `REVIEW-ROOM-SESSION-01.md` |

## Where a human decided

Several engines generated hypotheses. The choices below were made by a person, and each
one is recorded with its reasoning because each could reasonably have gone the other way:

1. **Treat the two alleles as one dosage problem** rather than two separate rescue
   problems. (`WHICH-ALLELE-TO-TARGET.md`)
2. **Re-open Aurora B** after an earlier automated pass closed it. That pass had filtered
   to *approved* agents before evaluating potency, which excluded the clinical-stage
   dedicated inhibitors on a procedural criterion rather than a scientific one.
   (`TRIAGE-KOSMOS-HACKATHON.md`)
3. **Accept a candidate that needs a dose decrease**, inverting the usual repurposing
   logic, once the exposure arithmetic pointed that way. (`THE-PICK.md`)
4. **Publish the checkpoint risk** as a headline rather than a limitation. (`ASSAY-DESIGN.md`)

## What we got wrong

`docs/mva/CORRECTIONS-2026-10-06.md` carries **52 numbered corrections** to our own
earlier conclusions, each traced to a primary source. Several are outright retractions.
Two were found in the final 24 hours by re-reading a figure legend instead of the figure.

This file is the one we would most like a reviewer to read. A pipeline that never
contradicts itself has not been checked.

## Reproducing the numbers

One command re-derives every count the report states, from the raw committed
records rather than from each gate's own summary fields. Python 3.9+, standard
library only, no network access needed:

    python3 apps/api/scripts/mva/verify_report.py

It prints one line per claim and exits non-zero if any count in the report
disagrees with the data. 20 checks.

### Dependencies

`verify_report.py` and the six gates need **no third-party packages**. 17 of the other
scripts do, and `requirements.txt` lists them:

    pip install -r requirements.txt

Four are needed only by the fragment-docking arm (`rdkit`, `vina`, `meeko`) and the
GPN-star reader (`pyarrow`); the statistical scripts need `numpy`, `scipy` or `pandas`.
Installing nothing at all still reproduces every number the report states, because that
is what `verify_report.py` covers.

### Re-running the funnel itself

The gates run in order. Each is standard-library-only and queries public APIs
(Open Targets, Ensembl VEP, ClinicalTrials.gov), so counts can drift as those
sources update; the committed JSON in `apps/api/data/mva/` is the result of
record. Add `--write` to overwrite it.

    python3 apps/api/scripts/mva/gate1_approved.py      # approval tiering
    python3 apps/api/scripts/mva/gate2_mechanism.py     # target -> drug
    python3 apps/api/scripts/mva/gate2b_reverse.py      # drug -> mechanism
    python3 apps/api/scripts/mva/gate3_safety.py        # paediatric safety
    python3 apps/api/scripts/mva/gate5_paediatric.py    # paediatric exposure
    python3 apps/api/scripts/mva/verify_report.py       # check report vs data

Two gates are not re-runnable here, by design:

- **Gate 0** (`gate0_universe.py`) reads a molecule list that is not
  redistributed. Its published output, `apps/api/data/mva/universe.json`, is
  committed, and every later gate runs from that.
- **Gate 4** is an adversarial literature pass rather than a script — see
  `docs/mva/GATE4-ADVERSARIAL.md` and `docs/mva/GATE4-ROUND2-SELF-REFUTATION.md`.

### Track 1 — the causal-gene cascade

Reproduces the gene call from the callset and HPO terms with no gene named at any
stage. Requires the challenge data, which is not redistributed, so this will not
run from a clean clone; it is published so the method can be read and audited.

    bash apps/api/scripts/mva/track1/run_pipeline.sh

See `docs/mva/TRACK1-REDISCOVERY.md`, including the two bugs that each produced a
confident wrong answer before they were found.

### Nonsense-mediated decay

`apps/api/scripts/mva/nmd/` scores premature-termination variants for escape from
mRNA decay and stratifies them by which protein domains a truncation would keep.
`stratify_ptc.py` is gene-agnostic and driven by UniProt feature records, so it
runs on any gene. Outputs are in `docs/mva/data/nmd/`; the reading is in
`docs/mva/NMD-PREDICTION-TRUNKITTEN.md`, `NMD-STRATIFIED-BUB1B.md` and
`NMD-STRATIFIED-MVA-GENES.md`.

The decay predictor itself (TrunCat / TrunKitten, Coban-Akdemir lab) is **not
vendored here**: that repository carries no licence, so it is cited and used, not
redistributed. The scripts above read it from a local checkout.

## Layout

    apps/api/scripts/mva/        the gates, plus millet/ neurosnap/ nmd/
                                 proband/ track1/ variants/
    apps/api/data/mva/           committed gate outputs (universe.json et al.)
    docs/mva/                    report, methods, and the supporting documents
    docs/mva/data/               committed query outputs cited by those documents

## Licence

Released under CC BY 4.0, per the hackathon submission terms.
