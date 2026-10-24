# Document index

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
| `BUB1B-MUTATION-ATLAS.md` | every BUB1B allele we could find, scored the same way |
| `VARIANT-TABLE.md` | the proband's two alleles, resolved to HGVS |
| `ATLAS-AUDIT.md` | what the atlas gets wrong, measured |
| `NMD-STRATIFIED-BUB1B.md` | the 55-nt rule applied per position |
| `NMD-STRATIFIED-MVA-GENES.md` | the same, across the other MVA genes |
| `NMD-FEASIBILITY.md` | whether NMD is addressable at all |
| `NMD-PREDICTION-TRUNKITTEN.md` | an independent NMD predictor, cross-checked |
| `PREDICTOR-CALIBRATION.md` | AlphaMissense and GPN-Star against known answers |
| `SPLICE-AXIS.md`, `SPLICE-ALLELE2.md`, `SPLICE-ARCHITECTURE.md` | the splice question, asked three ways |
| `RNASEQ-SPLICING.md` | transcript-level evidence |
| `apps/api/scripts/mva/poison_exon_scan.py`, `apps/api/scripts/mva/ptc_context.py` | context around the premature stop |
| `VUS-NOMINATION.md` | what we would nominate for reclassification |

## 2 · Structure and stability

| File | What it establishes |
|---|---|
| `N1002-STRUCTURAL-COUPLING.md` † | why allele 2 is buried, and what it couples to |
| `WHY-BURIED-IS-WORSE.md` | burial as the discriminator, tested |
| `ALLELE2-FOLDING-DOSSIER.md` | the folding case against allele 2 |
| `DDG-RESULT.md` | ΔΔG, with its controls |
| `STABILITY-AXIS.md` | stability as a scored axis |
| `FOLD-CLASS-AND-CHAPERONES.md` | whether a chaperone could rescue it |
| `POCKET-SCAN.md`, `DOCKING-AUDIT.md` | is there a pocket, and is the docking trustworthy |
| `NEIGHBOURHOOD-AND-COLUMNS.md`, `T1008-N1002R.md` | local structural context |
| `BINDING-AND-STABILISING.md` | could a small molecule bind and stabilise BubR1 directly |

## 3 · Mechanism from the literature

| File | What it establishes |
|---|---|
| `MECHANISM.md` | kinase, phosphatase, and what BubR1 actually does |
| `MVA-THERAPEUTIC-EVIDENCE-BASE.md` | the published evidence that the deficit is reversible |
| `DOSAGE-TIMING.md`, `DOSAGE-HEADROOM.md` | how much BubR1, and when |
| `HOW-OTHERS-SOLVED-IT.md` | precedents from adjacent dosage diseases |
| `FABRY-PRECEDENT.md` | the closest approved precedent, and why it does not transfer |
| `PHENOTYPE-GROUNDING.md` | tying mechanism to this child's presentation |
| `STANDARD-OF-CARE.md` | what is actually done for MVA today |

## 4 · Drug space

| File | What it establishes |
|---|---|
| `APPROACHES-ALL.md` | all ten therapeutic arms, before filtering |
| `APPROACH-RANKING.md` | how they were ranked |
| `MODALITY-LAYERS.md` | small molecule, biologic, oligo, gene — what each could reach |
| `DRUG-SCREEN.md`, `DRUG-CANDIDATES.md` | the funnel's output |
| `GERO-DRUGGABILITY-MINING.md` | an independent pass over 107,407 curated gene–drug pairs |
| `GERO-CT-VALIDATION.md` | whether that method's benchmark holds up |
| `ALLELE1-NMD-READTHROUGH.md` †, `ALLELE1-APPROVED-DRUGS.md` | the readthrough arm, and why it closed |
| `ALLELE2-ROUTES-REEXAMINED.md` | the allele-2 arms, re-opened and re-closed |
| `STABILISATION-STRATEGY.md` | the chaperone and degradation arms |
| `ANEUPLOIDY-SELECTIVE-ARM.md`, `CHEMOSENSITIVITY-ARM.md` | arms that target the consequence rather than the cause |
| `DIRECTION-G0-CILIA.md` | a direction considered and dropped |
| `SYSTEMIC-REPURPOSED-WHAT-SURVIVES.md` | what is left after every filter |
| `TRIED-AND-FAILED.md` | the negative record, kept deliberately |

## 5 · Exposure and safety

| File | What it establishes |
|---|---|
| `EXPOSURE-DOSSIER-KOSMOS-LEADS.md` | each candidate closed on measured human exposure |
| `TRIAGE-KOSMOS-HACKATHON.md` † | an earlier automated triage, and where it went wrong |
| `TRIAGE-EDISON-BUNDLES.md` | the cell-cycle confound in bulk readouts |
| `TOOL-TRIAGE-CHAPERONE.md`, `TOOL-TRIAGE-KOSMOS-NAD.md` | third-party tool output, assessed rather than trusted |
| `ASSAY-DESIGN.md` | the experiment we propose, and the risk it must measure |
| `MILLET-PROTOCOL.md` | the fragment-docking protocol and its controls |

## 6 · Adversarial review

| File | What it establishes |
|---|---|
| `COUNTER-ARGUMENT.md` | the strongest case against our own conclusion |
| `GATE4-ADVERSARIAL.md` | gate 4, where arms were attacked rather than scored |
| `GATE4-ROUND2-SELF-REFUTATION.md` | a second pass, attacking what survived the first |
| `REVIEW-ROOM-SESSION-01.md` | structured review, one methodological jurisdiction per seat |
| `CORRECTIONS-2026-10-06.md` | the 52 corrections those passes produced |
| `PHOENIX-HEADTOHEAD.md` | our agent pipeline against the hand-built funnel |

## Process and planning

`TRACK2-PLAN.md` · `SYNTHESIS.md` · `RECOMMENDATION.md` · `DECISION.md` ·
`STATUS.md` · `FINISH.md` · `SUBMIT-RUNBOOK.md` · `PITCH.md` ·
`WHICH-ALLELE-TO-TARGET.md` · `PATIENT-LED-PRECEDENTS.md` ·
`NEUROSNAP-TOOLBOX.md` · `GPN-STAR-PENDING.md` · `RTM-DESIGN.md` ·
`TRACK1-REDISCOVERY.md` (the causal-gene cascade, Track 1)
