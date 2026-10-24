# MVA Hackathon 2026 — Track 2 (Drug Repurposing)

Submission for *Rare Disease, Real Kid: The MVA Hackathon 2026*, organised by Sage
Bionetworks with the MVA Society, Hugging Face and BEACON.

**These are hypotheses for follow-up, not evidence that any medicine works.**
Nothing here is clinical advice. No patient data is redistributed in this
repository: what is committed is the *query*, never the data it read.

## Start here

| | |
|---|---|
| `mk7790_track2_report.md` | the submission report (same file as `docs/mva/TRACK2-REPORT.md`) |
| `docs/mva/CORRECTIONS-2026-10-06.md` | 23 numbered corrections to our own earlier conclusions, each traced to a primary source. Seven are retractions. Read this to see what we got wrong and how we found out. |
| `docs/mva/METHODS-DESCRIPTION.md` | the organisers' methods form, answered |
| `docs/mva/SUBMISSION-CHECKLIST.md` | what is and is not complete |

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
