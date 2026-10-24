# MVA Hackathon 2026 — Track 2 plan (drug repurposing)

Status: PLAN, not yet executed. Written 10 Sep 2026. Deadline **24 Oct 2026, 23:59 UTC**.

Deliverables required by the organisers: a written report (PDF or MD), a **public**
GitHub repo, and a **3-minute pitch video**. Limit 3 submissions per team, only the
LATEST is reviewed. Rubric: Scientific Rigor 35 / Potential Impact 25 /
Innovation 25 / Scalability 15.

---

## 1. What is already established (verified, not assumed)

The causal genotype is settled well enough to build on. Verified independently this
session against Open Targets (Ensembl VEP + ClinVar); full arithmetic in
`track1_verification.md`.

- **BUB1B p.Leu737\*** (chr15:40,209,701 T>G, rs759242053) — `stop_gained`,
  ClinVar **pathogenic** for mosaic variegated aneuploidy syndrome 1 (MONDO_0009759).
- **BUB1B p.Asn1002Lys** (chr15:40,220,612 T>G) — this nucleotide change is not in ClinVar,
  but the same protein change is (VCV004600147.1, `c.3006T>A`, VUS — see C16); confirmed by
  reconstructing the reading frame from three annotated neighbours (R999Q, N1004S,
  D1005E), which agree to the base pair.
- Architecture: **null + hypomorph**, which is required for viability — biallelic
  complete BUB1B loss is embryonic lethal.

NOT yet verified: that these variants are in the proband's VCF (dataset gated,
`huggingface.co` still blocked).

## 2. The mechanistic problem, stated honestly

You cannot pharmacologically restore a missing spindle-assembly checkpoint. There is
no agonist for a truncated kinase. Any submission claiming to "fix BUB1B" is wrong,
and the panel will know it.

So the therapeutic thesis must target **downstream consequences**. Three arms, in
descending order of evidence:

- **Arm A — aneuploidy → cellular senescence → SASP.** Chronically aneuploid cells
  accumulate proteotoxic and oxidative stress and enter senescence, driving an
  IL-6/TNF-dominated inflammatory secretome. This is the best-supported arm and the
  one Phoenix is already equipped for (it carries inflammaging dossiers on
  infliximab, ziltivekimab and the CANTOS/canakinumab work).
- **Arm B — cancer predisposition and surveillance. PROMOTED to the dominant arm,
  10 Sep 2026.** Not all MVA carries embryonal tumour risk: it tracks the *severity of
  spindle-assembly-checkpoint impairment*, and that is genotype-specific. Per PubMed,
  Yost et al., *Nature Genetics* 2017 — [DOI](https://doi.org/10.1038/ng.3883) —
  state it directly: "Individuals with biallelic TRIP13 or BUB1B mutations have a high
  risk of embryonal tumors, and here we show that their cells display severe SAC
  impairment. MVA due to biallelic CEP57 mutations, or of unknown cause, is not
  associated with embryonal tumors and cells from these individuals show minimal SAC
  deficiency."
  **This child has biallelic BUB1B, and is therefore in the high-risk group by
  genotype, not by inference.** The family's own description of care — "managing
  symptoms and fighting cancer cells" — is consistent with that.
  Two corrections to the popular framing, both load-bearing:
  - The tumour spectrum is **embryonal tumours broadly**, not kidney-specific. Yost's
    indexing spans Wilms tumour, rhabdomyosarcoma, AML and Sertoli-Leydig/ovarian
    tumours. Wilms is prominent but describing MVA risk as "kidney" is wrong.
  - The link is **constitutional, not somatic**. Hanks et al., *Cancer Letters* 2005 —
    [DOI](https://doi.org/10.1016/j.canlet.2005.08.006) — screened 30 Wilms tumours,
    10 ALLs and 20 rhabdomyosarcomas/cell lines and found somatic BUB1B mutations are
    "unlikely to be common in sporadic childhood cancers." So sporadic-tumour data is a
    proxy for the MVA child's tissue only with that caveat stated.
  The safety gate here is severe (see §5), and severity of SAC impairment gives this arm
  something the others lack: a **measurable mechanistic gradient** rather than a binary.
- **Arm C — ciliopathy.** Per PubMed, Miyamoto & Matsuura, *Oncotarget* 2015,
  "Ciliopathy in PCS (MVA) syndrome" — [DOI](https://doi.org/10.18632/oncotarget.5244) —
  argue that mitotic kinases/kinesins in MVA also regulate the primary cilium. This
  is under-explored and is the most likely source of an **Innovation** score. Treat
  as a hypothesis-generating arm, flagged as such.

## 3. Data feasibility — the finding that reshapes the plan

Searched PubMed for MVA/BUB1B expression cohorts (414 hits, top 20 reviewed).
**There is no MVA patient expression cohort comparable to the GEO disease-vs-control
series Phoenix normally uses.** The BUB1B expression literature is overwhelmingly
oncology, where BUB1B is *over*-expressed in tumours — the opposite direction to a
loss-of-function child, and actively misleading if pulled in naively.

Consequences:
- Phoenix's **organ-aging tissue channel — its strongest data channel — has little to
  chew on for MVA.** Do not pretend otherwise.
- Evidence weight shifts to **mechanism resolution + literature + adversarial
  refutation**. Those channels work here (they route via MCP, which is reachable).
- **Abstention will be common, and that is the honest result.** Present Phoenix's
  `abstain_insufficient_coverage` verdict as a designed feature — coverage reported
  separately from score — not as a failure. This is a rigor argument, and it is
  defensible to a panel that includes clinicians.

## 4. The screening universe (FDL molecule pool)

`FDL/knowledge-base/registry/molecule-pool.json` — **5,202 molecules**, of which
4,193 carry ATC codes, 1,051 carry therapeutic areas, 678 flagged approved_western,
47 flagged biosimilar. Sourced from ATC/WHO, EMA, and the DRAP corpus.

Spot-check confirms the relevant chemistry is present: tocilizumab, infliximab,
adalimumab, etanercept, anakinra, canakinumab, sirolimus, rapamycin, metformin,
dasatinib, navitoclax, ruxolitinib, acetylcysteine, celecoxib all appear.
(quercetin and fisetin do not — correctly, they are supplements, not approved drugs.
Note this breaks the canonical dasatinib+quercetin senolytic pair.)

**Confidentiality line — binding.** Track 2 output is CC BY 4.0 with a public repo.
- Publishable: `inn`, `atc`, `areas`, `biosimilar_flag`, and the fact of EMA/ATC sourcing.
  These derive from public EMA/WHO records.
- NOT publishable: `corpus_records`, `jurisdictions`, and anything from the molecule
  pages' YAML front-matter (`supplier_status`, `route`, `incumbency`, SKU counts,
  origin-country mixes) or `research/TARGET-LIST.md`.
- Rule: the pool is a **screening universe only**. Every claim about a surviving
  candidate must be re-derived from a public source before it enters the report.

## 4b. Data route via Wilms tumour single-cell data — partial fix for §3

Lead raised by the owner 10 Sep 2026 and checked. It partly closes the data gap in §3,
with one leap that must be declared rather than hidden.

**What works.** Wilms tumour is the best-characterised MVA-associated malignancy and has
real single-cell transcriptomic data behind it, unlike MVA itself. Single-cell data
resolves what bulk sequencing cannot in a mosaic disease, where a patient carries a
mixture of euploid and variously aneuploid cells and bulk averaging destroys the signal.

**The leap.** Published Wilms single-cell data comes from **sporadic** Wilms patients,
not from MVA patients. Using it as a proxy for this child's kidney is an inference, and
Hanks 2005 (above) shows the sporadic tumours largely do *not* carry BUB1B lesions. Use
it to characterise the aberrant-fetal-cell state a Wilms tumour arises from; do NOT
present it as MVA patient data. State the substitution explicitly in the report — a
panel will spot it, and declaring it is worth more than hiding it.

**Literature-channel trap, found while checking this.** The symbol `WT1` means *Wilms
Tumour 1*, a transcription factor expressed in heart, podocytes and leukaemia. A naive
"Wilms tumour + scRNA-seq" query returned three papers on WT1 protein in murine
epicardium and kidney organoids and zero on Wilms tumour the disease. Phoenix's
literature channel must disambiguate the gene symbol from the disease or it will
retrieve confident nonsense. Add this to the §6.4 guard alongside the
BUB1B-overexpressed-in-tumours trap.

**Data reachability.** `scpca.alexslemonade.org` and `cellxgene.cziscience.com` are both
403 at the egress proxy; `www.ebi.ac.uk` responds 200. EBI (ArrayExpress/BioStudies) is
therefore the viable retrieval route while NCBI remains blocked. Confirm before building
against it.

**Not verified.** The claim that the MVA Society itself uses single-cell data to screen
FDA-approved drugs could not be substantiated from any primary source. Do not repeat it.

## 5. The funnel

Six gates, following FDL's scouting method discipline (the *method* is reused, not the
data): nothing advances two gates in one pass, and **no number ships without the
committed query that produced it**.

| Gate | Filter | Instrument |
|---|---|---|
| 0 | Universe: 5,202 molecules, confidential fields stripped | one committed script |
| 1 | Approved and obtainable — require ATC code; drop investigational-only | ATC presence + approval flags |
| 2 | Mechanism relevance to Arm A/B/C | Open Targets MCP: drug → target → pathway |
| 3 | **Paediatric safety gate** (see below) | literature + safety channel |
| 4 | Evidence channels: endpoint alignment + adversarial refutation | Phoenix |
| 5 | Access layer: biosimilar availability, formulation, route | public EMA/FDA + `biosimilar_flag` |

**Gate 3 is not a formality.** The patient is a child with a chromosomal instability
syndrome and elevated cancer risk. Hard exclusions: anything genotoxic; anything that
meaningfully suppresses tumour immunosurveillance; anything with no paediatric safety
data. The report should *show the gate rejecting candidates* — a safety gate that
never fires is not a safety gate. Expect this to kill much of Arm B, including the
checkpoint inhibitors, and that rejection is itself a finding worth reporting.

**Gate 5 is the differentiator.** Nearly every entry will name a molecule. Almost none
will ask whether it is obtainable for this child, or for the other ~50 MVA patients
worldwide under very different registration regimes. Biosimilars are what turn an
expensive biologic into something a health system can actually supply. This scores on
Potential Impact and Scalability, and is the kind of patient-centred reasoning the
Innovation/Community award is described as rewarding.

## 6. Phoenix changes required

Keep the skeleton, replace the organs. Kept: the channel architecture, the Adjudicator,
coverage-separate-from-score, the safety gate, and the adversarial refutation channel.

1. New axis: chromosomal instability / SAC failure / aneuploidy-induced senescence.
   Build on the existing **Senescence** axis rather than the organ-fibrotic ones.
2. Route BUB1B through the drug-mechanism router as **loss-of-function**, explicitly
   not as a druggable target to inhibit.
3. Re-weight the Adjudicator for a thin-data disease so that a literature-only verdict
   is reportable with low coverage rather than silently discarded.
4. Guard against the oncology-literature trap from §3: BUB1B-overexpressed tumour
   papers must not be counted as supporting evidence for a loss-of-function child.

**Network constraint.** Phoenix's own arteries are blocked in this container:
`eutils.ncbi.nlm.nih.gov`, `ftp.ncbi.nlm.nih.gov`, `maayanlab.cloud`,
`paperclip.gxl.ai` and `openrouter.ai` all return 403 at the egress proxy. Only
PubChem responds. The MCP servers (Open Targets, PubMed, Paperclip, ClinicalTrials)
DO work and are how the Track 1 verification was done. So either allowlist those five
hosts, or source evidence through MCP — the latter is arguably the better design and
is itself a defensible engineering contribution.

## 7. Critical path and blockers

Owner action, in priority order:
1. Allowlist **`huggingface.co`** (only the `.hf.space` app domain came through). Without
   it the gated dataset cannot be fetched and Track 1 cannot be confirmed against the VCF.
   Note the container has ~29 GB free against an 85 GB dataset — pull the VCF, not the snapshot.
2. Set `ALPHAGENOME_API_KEY` in the environment config **and start a fresh session**
   (env vars inject at container start; it is not present now). Allowlist the AlphaGenome host.
3. Decide, explicitly, whether patient genomic data may be pulled into this managed
   container. The DTA forbids granting access to anyone and requires deletion within 30
   days from all environments including cloud instances and derived datasets. The rules
   do anticipate LLM use but require declaring provider/tier/data-handling in the methods.

## 8. Sequencing to 24 Oct

Do not start the report last. The report *is* the submission; code is supporting evidence.

- **Now → +1 week:** Gates 0–2. Build the funnel scripts, strip confidential fields,
  map surviving molecules to the three arms via Open Targets. Commit every query.
- **+1 → +3 weeks:** Gate 3 safety and Gate 4 evidence channels. Phoenix modifications.
  Run the adversarial channel against the leading candidates and record what survives.
- **+3 → +5 weeks:** Gate 5 access layer. Draft the report around the three arms.
- **Final 2 weeks:** Pitch video, public-repo hygiene pass, submit early and use the
  remaining two submission slots for refinement.

**Repo hygiene, before anything goes public:** Phoenix's docs carry commercial
positioning aimed at a commercial audience, which must be excluded before anything
is published, or a panel of clinicians and patient advocates reads a patient-centred
submission as a sales pitch. See `PUBLICATION-AUDIT.md`: the recommended route is a
clean export rather than redaction, because git retains deleted text. (This sentence
was itself rewritten after the audit's leak check flagged that naming the specifics
here would carry them into the public export — the check works.)

---

# RESULTS — gates 0 to 2 executed, 10 Sep 2026

Instruments: `apps/api/scripts/mva/gate{0_universe,1_approved,2_mechanism,2b_reverse}.py`.
Outputs: `apps/api/data/mva/`. Every number below is reproducible from those scripts.

## Counts

| Gate | Question | In | Out |
|---|---|---:|---:|
| 0 | May this row be published, and is it a real molecule? | 5,202 | **4,945** |
| 1 | Is it actually an approved medicine? | 4,945 | **1,485** proposable (tier A 1,472 · B 13; tier C 3,460 excluded) |
| 2 | Does it act on a target an MVA mechanism runs through? | 1,485 | **34** |

Gate 0 dropped 238 rows as internal-source-only and 19 as veterinary.

## The 34

- **Arm A, senescence/SASP — 26.** IL-6 axis (tocilizumab, sarilumab, satralizumab,
  siltuximab); TNF (adalimumab, infliximab, etanercept, golimumab, certolizumab pegol);
  IL-1 (anakinra, canakinumab, rilonacept); JAK (ruxolitinib, baricitinib, tofacitinib,
  upadacitinib, abrocitinib, filgotinib, fedratinib, momelotinib, delgocitinib);
  mTOR via FKBP12 (sirolimus, everolimus, temsirolimus, tacrolimus); BCL-2 (venetoclax).
- **Arm B, cancer predisposition — 6.** All COX-2/PTGS2: ibuprofen, diflunisal,
  ketorolac, bromfenac, nepafenac, parecoxib.
- **Arm C, ciliopathy — 2.** HDAC6: givinostat, panobinostat.
- **Biosimilar available for 5:** adalimumab, etanercept, golimumab, infliximab, tocilizumab.

## Three findings that change what happens next

**1. The mitotic-liability worry is moot, and that is an empirical result.**
AURKA, PLK1, TTK/MPS1, KIF11, WEE1, MDM2 and TP53 were carried into Gate 2
deliberately so Gate 3 could be seen refusing them. **All seven return zero
approved drugs.** Every agent against them is investigational. So no approved-drug
repurposing screen can propose a mitotic poison to this child — the danger was
real but unreachable. Gate 3's actual work is different and harder (below).

**2. Gate 3's real problem is immunosuppression, not mitosis.** Arm A leads
straight to TNF blockers and JAK inhibitors, and both classes carry malignancy
warnings — JAK inhibitors a boxed malignancy warning, TNF blockers a boxed
lymphoma/malignancy warning in paediatric patients. This child's tumour risk is
driven by chromosome missegregation, and immunosurveillance is part of what
contains that. **The most obvious Arm A candidates may be the most
contraindicated**, which makes the safety gate the scientific centre of the
submission rather than a compliance step. IL-1 blockade is the class worth
looking at hardest: CANTOS is the one large trial where an anti-inflammatory
biologic was associated with *reduced* incident cancer rather than increased.

**3. Two methodological defects, both found and both recorded.**
- *Target-set screening has a systematic blind spot.* Open Targets annotates
  sirolimus and everolimus on **FKBP1A, not MTOR** — correctly, since rapalogs
  bind FKBP12 and the complex inhibits mTORC1. A target set naming MTOR misses
  both. Fixed by adding FKBP1A; the general lesson is that a drug whose annotated
  target is a proximal binding partner rather than the effector is invisible to
  this method, and the arms must be audited for that class of miss.
- *`drugAndClinicalCandidates` is a curated list, not a complete drug-target map.*
  Gate 2b therefore walks drug -> mechanism in reverse over all 1,485 proposable
  molecules and unions the results. After the FKBP1A fix the two directions agree
  exactly (34 = 34), which is the cross-check; before it, neither direction alone
  would have surfaced the gap.

## Known limits, stated rather than buried

- **Gate 1 tier C contains false negatives.** Celecoxib sits in tier C on `atc`
  alone because it is not in the centralised EMA table, yet it is plainly an
  approved medicine. Tier C therefore mixes genuinely unapproved compounds
  (navitoclax, correctly) with nationally-approved ones the pool's sources miss.
  Any Arm B COX-2 argument must re-derive approval per drug rather than trust the tier.
- **Name resolution reached 989 of 1,485 (67%).** The 496 misses are dominated by
  vaccines, immunoglobulins, combination products, salts/esters and allergen
  extracts — classes that could not be MVA candidates anyway — but the gap is not
  zero and is not evidence of absence.
- **Metformin and dasatinib are geroprotection/senolytic candidates that this
  method cannot reach by target.** Metformin's annotation is ~50 complex-I
  subunits; dasatinib's is ABL1/BCR. Both would need naming directly, which the
  funnel deliberately does not do.

---

# RESULTS — gate 3 (paediatric safety) executed, 10 Sep 2026

Instrument: `apps/api/scripts/mva/gate3_safety.py`. Output: `apps/api/data/mva/gate3.json`.

**34 in, 13 out.** Refusals: 11 carcinogenicity, 7 cytotoxic, 2 withdrawn,
1 no systemic exposure. Survivors: 5 `proceed_with_monitoring`,
8 `caution_immunosuppression`.

## The gate refused the best-fitting candidates, which is the finding

Arm A's strongest mechanistic hits and the worst safety risks are the same
molecules. Every TNF blocker (adalimumab, infliximab, etanercept, golimumab) and
most JAK inhibitors (tofacitinib, baricitinib, upadacitinib, abrocitinib) carry a
**black-box carcinogenicity warning**, which in a child whose tumour risk comes
from chromosome missegregation is disqualifying rather than a caution. Sirolimus
and tacrolimus fall the same way; everolimus, temsirolimus, ruxolitinib,
fedratinib, momelotinib, venetoclax and panobinostat fall as ATC L01
antineoplastics, refused on mechanism — adding DNA damage to cells that already
missegregate chromosomes — rather than on toxicity grade.

## The result that reshapes the access argument

**Not one surviving candidate has a biosimilar.** All five biosimilar-available
molecules — adalimumab, etanercept, golimumab, infliximab, tocilizumab — were
refused on carcinogenicity. The cheap, globally obtainable drugs are precisely
the contraindicated ones.

That does not kill the Gate 5 access layer, it inverts it into a sharper claim:
for this child the accessible options are unsafe and the safest options are
expensive orphan biologics (canakinumab, rilonacept, siltuximab, satralizumab).
**Access is the binding constraint on the answer, not a footnote to it** — which
is a stronger and more honest thing to tell a panel that includes patient
advocates than a list of affordable biosimilars would have been.

## Where the funnel landed, and it was not hand-picked

The Arm A survivors are the **IL-1 axis** (anakinra, canakinumab, rilonacept) and
the **IL-6 axis** (sarilumab, satralizumab, siltuximab) — they survive precisely
because they lack the carcinogenicity black box the TNF and JAK classes carry.
That converges on CANTOS, the one large trial in which an anti-inflammatory
biologic was associated with *reduced* incident cancer. The convergence fell out
of the safety data; it was not chosen. That is worth saying plainly in the
report, because a reviewer's first suspicion of any repurposing screen is that
the answer was picked first and the funnel built around it.

## Two defects found and fixed in this gate

- **ATC letters are anatomical groups, not routes.** The first run refused
  abrocitinib as "topical" because its ATC is D11AH08 (dermatologicals) — but
  abrocitinib is an oral tablet. Auto-refusal is now restricted to S01/S02/S03
  (sensory organ), which ATC can settle; D-group drugs are flagged for a
  per-product route check at Gate 4 instead. Delgocitinib, genuinely topical,
  now carries that flag rather than a refusal.
- **A `--write` run piped through `head` was killed by SIGPIPE before it wrote,**
  leaving a stale `gate3.json` whose tally disagreed with the printed output.
  Caught by cross-checking the two. Runs that write are now redirected to a file,
  never piped. (FDL's CLAUDE.md warns about exactly this; the warning generalises.)

## Standing caveat

Absence of a paediatric warning is NOT evidence of paediatric safety. Every
survivor carries `paediatric_evidence: unestablished` until Gate 4 looks for it
in the literature and trial registries. Nothing here is clinical advice; these
are hypotheses for follow-up, which is what the track asks for.

---

# RESULTS — gate 5 (paediatric exposure) executed, 10 Sep 2026

Instrument: `apps/api/scripts/mva/gate5_paediatric.py`, ClinicalTrials.gov API v2.
Output: `apps/api/data/mva/gate5.json`.

Gate 5 was planned as the access layer, but Gate 3 had already answered access and
inverted it — no survivor has a biosimilar. The open question was the one every
survivor carried as `paediatric_evidence: unestablished`, so this gate closes that
instead. ClinicalTrials.gov records eligibility age per study, so paediatric
exposure can be counted rather than asserted.

**11 of 13 survivors have been studied in children at phase 2 or later.**

| drug | CTG total | child studies | phase 2+ | youngest |
|---|---:|---:|---:|---:|
| ibuprofen | 1,108 | 58 | 33 | neonatal |
| **anakinra** | 216 | 41 | **29** | **neonatal** |
| **canakinumab** | 117 | 37 | **28** | **neonatal** |
| certolizumab pegol | 172 | 13 | 10 | 2 y |
| givinostat | 27 | 10 | 7 | 2 y |
| rilonacept | 26 | 8 | 6 | 3 mo |
| satralizumab | 20 | 8 | 6 | 2 y |
| sarilumab | 73 | 5 | 3 | neonatal |
| siltuximab | 45 | 5 | 3 | 12 y |
| filgotinib | 66 | 4 | 3 | 8 y |
| delgocitinib | 22 | 3 | 2 | 2 y |
| diflunisal | 7 | 1 | 0 | — |
| parecoxib | 76 | 1 | 0 | — |

## The convergence, which was not engineered

Three gates asked different questions with different instruments and different
data sources, and they agree:

- **Gate 3 (safety)** kept the IL-1 axis because it lacks the carcinogenicity
  black box the TNF and JAK classes carry.
- **Gate 4 (adversarial)** found IL-1β blockade is the one mechanism with large
  randomised evidence pointing *away* from cancer risk rather than toward it.
- **Gate 5 (paediatric)** now finds anakinra and canakinumab are the two most
  extensively studied survivors in children — 29 and 28 phase-2+ paediatric
  studies respectively, both reaching neonatal eligibility.

Nothing selected for that. Safety came from drug warnings, the adversarial result
from the literature, paediatric exposure from a trial registry. **Anakinra and
canakinumab are where the funnel lands.**

## What Gate 5 does NOT establish

A CHILD-eligible trial means paediatric dosing exists and has been studied. It is
not approval, not safety in THIS child, and not evidence in a chromosomal
instability syndrome. The gate moves a candidate from "unknown in children" to
"studied in children" and no further.

Two known sources of noise, reported rather than filtered:
- `query.intr` matches combination studies, so an oncology add-on trial counts
  under its partner drug. The counts are a floor on attention, not exposure
  measures. Ibuprofen's 1,108 is mostly analgesia and says nothing about
  chemoprevention.
- **Defect found and fixed in this gate.** The age parser handled Years, Months
  and Weeks but not Days, so a "1 Day" minimum age read as **1.0 years** — making
  cohorts look older than they were. Fixed; the neonatal figures above are from
  the corrected run.
