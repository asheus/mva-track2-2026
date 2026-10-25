# Document index

Documents are grouped into `variant/`, `structure/`, `drug-search/`, `review/` and
`process/`. Seventeen stay at this level because scripts resolve them by path
(`verify_report.py`, the gate scripts and the export audit) or because they are
submission deliverables; moving those would break the checks that re-derive our numbers.

Every document in this repository, grouped by the evidence channel it belongs to.
The README explains the channels. Within each group, documents are listed roughly in
the order the work happened.

Documents marked **†** record a conclusion we later changed; they are kept because the
change is the evidence, and `CORRECTIONS-2026-10-06.md` says what moved and why.

## Start here

| File | What it is |
|---|---|
| `TRACK2-REPORT.md` | the submission report |
| `THE-PICK.md` | the candidate, and the arithmetic behind it |
| `CORRECTIONS-2026-10-06.md` | 52 numbered corrections to our own work |
| `METHODS-DESCRIPTION.md` | the organisers' methods form, answered |
| `SUBMISSION-CHECKLIST.md` | what is and is not complete |
| `FIGURE-CREDITS.md` | every reproduced figure, with its own licence |
| `VIDEO-SCRIPT.md` | the 3-minute pitch, with per-slide second budgets |

## 1 · Variant interpretation

| File | What it establishes |
|---|---|
| `variant/BUB1B-MUTATION-ATLAS.md` | every BUB1B allele we could find, scored the same way |
| `VARIANT-TABLE.md` | the proband's two alleles, resolved to HGVS |
| `variant/ATLAS-AUDIT.md` | what the atlas gets wrong, measured |
| `variant/NMD-STRATIFIED-BUB1B.md` | the 55-nt rule applied per position |
| `variant/NMD-STRATIFIED-MVA-GENES.md` | the same, across the other MVA genes |
| `NMD-FEASIBILITY.md` | whether NMD is addressable at all |
| `NMD-PREDICTION-TRUNKITTEN.md` | an independent NMD predictor, cross-checked |
| `PREDICTOR-CALIBRATION.md` | AlphaMissense and GPN-Star against known answers |
| `variant/SPLICE-AXIS.md`, `variant/SPLICE-ALLELE2.md`, `variant/SPLICE-ARCHITECTURE.md` | the splice question, asked three ways |
| `variant/RNASEQ-SPLICING.md` | transcript-level evidence |
| `apps/api/scripts/mva/poison_exon_scan.py`, `apps/api/scripts/mva/ptc_context.py` | context around the premature stop |
| `variant/VUS-NOMINATION.md` | what we would nominate for reclassification |

## 2 · Structure and stability

| File | What it establishes |
|---|---|
| `structure/N1002-STRUCTURAL-COUPLING.md` † | why allele 2 is buried, and what it couples to |
| `structure/WHY-BURIED-IS-WORSE.md` | burial as the discriminator, tested |
| `structure/ALLELE2-FOLDING-DOSSIER.md` | the folding case against allele 2 |
| `structure/DDG-RESULT.md` | ΔΔG, with its controls |
| `STABILITY-AXIS.md` | stability as a scored axis |
| `structure/FOLD-CLASS-AND-CHAPERONES.md` | whether a chaperone could rescue it |
| `structure/POCKET-SCAN.md`, `structure/DOCKING-AUDIT.md` | is there a pocket, and is the docking trustworthy |
| `structure/NEIGHBOURHOOD-AND-COLUMNS.md`, `structure/T1008-N1002R.md` | local structural context |
| `structure/BINDING-AND-STABILISING.md` | could a small molecule bind and stabilise BubR1 directly |

## 3 · Mechanism from the literature

| File | What it establishes |
|---|---|
| `process/MECHANISM.md` | kinase, phosphatase, and what BubR1 actually does |
| `process/MVA-THERAPEUTIC-EVIDENCE-BASE.md` | the published evidence that the deficit is reversible |
| `drug-search/DOSAGE-TIMING.md`, `drug-search/DOSAGE-HEADROOM.md` | how much BubR1, and when |
| `process/HOW-OTHERS-SOLVED-IT.md` | precedents from adjacent dosage diseases |
| `process/FABRY-PRECEDENT.md` | the closest approved precedent, and why it does not transfer |
| `process/PHENOTYPE-GROUNDING.md` | tying mechanism to this child's presentation |
| `process/STANDARD-OF-CARE.md` | what is actually done for MVA today |

## 4 · Drug space

| File | What it establishes |
|---|---|
| `drug-search/APPROACHES-ALL.md` | all ten therapeutic arms, before filtering |
| `drug-search/APPROACH-RANKING.md` | how they were ranked |
| `drug-search/MODALITY-LAYERS.md` | small molecule, biologic, oligo, gene — what each could reach |
| `drug-search/DRUG-SCREEN.md`, `drug-search/DRUG-CANDIDATES.md` | the funnel's output |
| `drug-search/GERO-DRUGGABILITY-MINING.md` | an independent pass over 107,407 curated gene–drug pairs |
| `drug-search/GERO-CT-VALIDATION.md` | whether that method's benchmark holds up |
| `ALLELE1-NMD-READTHROUGH.md` †, `drug-search/ALLELE1-APPROVED-DRUGS.md` | the readthrough arm, and why it closed |
| `drug-search/ALLELE2-ROUTES-REEXAMINED.md` | the allele-2 arms, re-opened and re-closed |
| `drug-search/STABILISATION-STRATEGY.md` | the chaperone and degradation arms |
| `drug-search/ANEUPLOIDY-SELECTIVE-ARM.md`, `drug-search/CHEMOSENSITIVITY-ARM.md` | arms that target the consequence rather than the cause |
| `drug-search/DIRECTION-G0-CILIA.md` | a direction considered and dropped |
| `drug-search/SYSTEMIC-REPURPOSED-WHAT-SURVIVES.md` | what is left after every filter |
| `drug-search/TRIED-AND-FAILED.md` | the negative record, kept deliberately |

## 5 · Exposure and safety

| File | What it establishes |
|---|---|
| `drug-search/EXPOSURE-DOSSIER-KOSMOS-LEADS.md` | each candidate closed on measured human exposure |
| `review/TRIAGE-KOSMOS-HACKATHON.md` † | an earlier automated triage, and where it went wrong |
| `review/TRIAGE-EDISON-BUNDLES.md` | the cell-cycle confound in bulk readouts |
| `review/TOOL-TRIAGE-CHAPERONE.md`, `review/TOOL-TRIAGE-KOSMOS-NAD.md` | third-party tool output, assessed rather than trusted |
| `drug-search/ASSAY-DESIGN.md` | the experiment we propose, and the risk it must measure |
| `structure/MILLET-PROTOCOL.md` | the fragment-docking protocol and its controls |

## 6 · Adversarial review

| File | What it establishes |
|---|---|
| `review/COUNTER-ARGUMENT.md` | the strongest case against our own conclusion |
| `GATE4-ADVERSARIAL.md` | gate 4, where arms were attacked rather than scored |
| `GATE4-ROUND2-SELF-REFUTATION.md` | a second pass, attacking what survived the first |
| `review/REVIEW-ROOM-SESSION-01.md` | structured review, one methodological jurisdiction per seat |
| `CORRECTIONS-2026-10-06.md` | the 52 corrections those passes produced |
| `review/PHOENIX-HEADTOHEAD.md` | our agent pipeline against the hand-built funnel |

## Process and planning

`process/TRACK2-PLAN.md` · `process/SYNTHESIS.md` · `process/RECOMMENDATION.md` · `process/DECISION.md` ·
`process/STATUS.md` · `process/FINISH.md` · `process/SUBMIT-RUNBOOK.md` · `process/PITCH.md` ·
`variant/WHICH-ALLELE-TO-TARGET.md` · `process/PATIENT-LED-PRECEDENTS.md` ·
`structure/NEUROSNAP-TOOLBOX.md` · `process/GPN-STAR-PENDING.md` · `process/RTM-DESIGN.md` ·
`TRACK1-REDISCOVERY.md` (the causal-gene cascade, Track 1)
