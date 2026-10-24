# Methods description — MVA Hackathon 2026, Track 2 (Drug Repurposing)

Answers to the organisers' `methods_description_form.xlsx`, Track 2 sheet. The
organisers note that submissions without a methods description may be judged less
favourably on **Scientific Rigor** and **Innovation**, "since the panel can't assess
what it can't see."

> **⚠️ ONE FIELD NEEDS THE TEAM TO FILL IT IN BEFORE SUBMISSION — Q3.** It is the only
> *required* question on the form. The provider and data-handling setting are known and
> stated below; the **plan or tier** is an account fact this analysis cannot verify
> about itself and must not guess.

---

### Q1. Team name

*To be completed by the submitting team.* Submitting HF account: `mk7790`. Track 2
accepts one submission per team; the panel reviews only the latest of up to three.

### Q2. Please describe your approach in detail (how you went from variant/mechanism to candidate medication(s))

A **six-gate funnel**, each gate a committed script that reports what it excluded as
well as what it passed, run over the mechanism the variants imply.

| Gate | Question | In → out |
|---|---|---|
| 0 | Is it a real, publishable molecule? | 5,202 → 4,945 |
| 1 | Is it an approved medicine? | 4,945 → 1,485 |
| 2 | Does it act on a target an MVA mechanism runs through? | 1,485 → 34 |
| 3 | Is it safe **in this child**? | 34 → 13 |
| 4 | Does the thesis survive adversarial attack? | 13 → 13 (one branch refuted) |
| 5 | Has it ever been given to a child? | 13 → 11 studied, **2 leads** |

Two mechanistic theses emerged and are **ranked**, which is the core of the approach:

- **Lead — raise the protein the child still makes.** Allele 2 (`p.Asn1002Lys`) is a
  folding-class variant: protein is made, misfolds, and is cleared by
  chaperone-dependent quality control. Candidate: **arimoclomol**, an HSF1 co-inducer
  (FDA-approved as Miplyffa, Sep 2024, children ≥ 2), which raises folding capacity
  *in trans* and never binds the target. Reached not by a database query but by first
  establishing the **fold class** of the variant, then asking which approved agents
  match that degradation route.

  **The ranking inside this class reversed during the work, and the reversal is
  method rather than noise.** The first candidate was sodium phenylbutyrate, chosen
  partly because it is an HDAC inhibitor — counted as a third supporting mechanism.
  HDAC inhibition in fact induces premature sister chromatid separation and strips
  BubR1 from kinetochores, and this child's syndrome is named for premature chromatid
  separation. The rule we had failed to write down is that **any chronic agent which
  degrades checkpoint function is contraindicated in a checkpoint-deficient child**,
  and it convicted our own lead. 4-PBA is retained as a stated alternative with that
  hazard attached, because it has selectivity evidence and paediatric depth that
  arimoclomol lacks, including use below age two. Documented as C5 and C7 of 24 logged
  corrections.
- **Adjunct — blunt the senescence-associated secretory phenotype.** **Anakinra** and
  **canakinumab**, reached by the funnel above, where three independent instruments
  (regulatory drug-warning data, an adversarial literature pass, a paediatric-exposure
  count from a trial registry) converged on the IL-1 axis without being tuned to agree.

The ranking flipped late and deliberately: the IL-1 arm treats a *downstream
consequence*, the stabilisation arm treats the lesion.

**Quantitative triage between alleles.** Before choosing a target we asked which allele
is reachable, using published effect sizes rather than intuition. Readthrough of allele
1's premature stop was **retired on arithmetic** — across ~5,800 measured pathogenic
PTCs, median readthrough is 0.08–1.32%, this PTC is an unfavourable substrate on three
of three published context rules, and it sits 747 nt upstream of the last exon–exon
junction so NMD has already removed most of the substrate. Best case falls ~35-fold
short of the needed dose increase. NMD inhibition has the only large ceiling and no
approved agent. That left allele 2.

### Q3. Generative AI disclosure *(required)*

**Provider:** Anthropic. **Interface:** Claude Code (cloud sessions on claude.ai/code).
**Models:** Claude Opus 5, with a short final segment on Claude Opus 5.5.
**Setting:** commercial terms, no training on customer content.
**Plan or tier: ⚠️ TO BE FILLED IN BY THE TEAM** — an account fact not verifiable from
inside the analysis.

**The format the organisers asked for (28 Aug 2026 update, recorded 23 Oct 2026).** They
require "the provider, the plan or tier, and the relevant data-handling setting" and say
**"A line is enough,"** giving this as their own example:

> "Anthropic API, Claude Sonnet, commercial terms, no training on customer content."

So a single line satisfies the requirement, and the expanded block above is more than is
asked — keep both: the line for the form field, the block for the report body. The
paste-ready line, with the one gap the team must close:

> `Anthropic, Claude Code (claude.ai/code cloud sessions), <PLAN OR TIER>, commercial terms, no training on customer content.`

Note that the organisers' example names a model as well as a plan. Their stated
requirement does not demand it, and the block above already records which models were
used; **the plan or tier is the only genuinely missing element**, and it is the only
mandatory question on the form. Confirm it against the account that ran the sessions
rather than inferring it — a wrong tier is worse than a blank one.

The AI's role was substantive and should be stated plainly: it wrote every script,
performed the literature synthesis, and drafted the documents. It also generated the
errors listed under limitations and, in several cases, the controls that caught them.
Every quantitative claim is backed by a committed script a reviewer can re-run.

### Q4. Was candidate identification automated, or primarily manual literature review and expert curation?

**Automated, with adversarial literature review layered on top — and the automation is
auditable.** Gates 0–3 and 5 are parameterised scripts over public APIs; no candidate
was hand-picked into the list. `verify_report.py` re-derives every count the report
states *from the raw records rather than the gates' own summary fields*, so a gate
disagreeing with its own summary shows up. Gate 4 is the non-automated layer: a
deliberate attempt to refute our own thesis from the literature.

### Q5. Please describe any manual literature review or expert curation in detail

Three passes, all adversarial by design:

1. **Gate 4, round 1** — attack the senescence thesis. The strongest objection
   (senescence is a tumour-suppressive barrier a chromosomally unstable child depends
   on) was answered by separating senescence *arrest* from the *secretory* output.
2. **Gate 4, round 2** — attack our own conclusion. It **refuted us**: our claim that
   senolytics were contraindicated was overstated, and is now recorded as unresolved
   rather than settled.
3. **A variant-literature sweep** to build a *BUB1B* mutation atlas independent of any
   single database, then an audit of that atlas against primary sources — which
   refuted one of our own claims and qualified a headline result.

Curation was also applied to the phenotype: the organisers' clinical document was read
and **corrected a claim we had asserted three times** (see limitations).

### Q6. Public sources only, or proprietary too?

**Solely public.** No proprietary drug, target, or patient data source was used. The
only gated input is the organisers' own challenge dataset, used under the DTA.

### Q7. Please describe the public data sources used in detail

- **Drug / target:** Open Targets (queried in *both* directions — target→drug and
  drug→mechanism), ChEMBL identifiers, WHO ATC, centralised EMA approval tables, FDA
  labelling and review documents, ClinicalTrials.gov (paediatric eligibility ages).
- **Variant / clinical:** ClinVar, the EBI Proteins variant aggregate, UniProt
  (`ENSP00000287598`), Ensembl VEP against `ENST00000287598`, gnomAD, OMIM/MONDO.
- **Sequence / structure:** AlphaFold `AF-O60566-F1`; PDBe for crystal complexes used
  in docking validation (RCSB is refused by our compute environment's network policy).
- **Predictors:** AlphaMissense, AlphaGenome, GPN-Star, ProteinMPNN-ddG, ThermoMPNN,
  EvoEF2, Pangolin, plus Lacuna cryptic-pocket sampling and AutoDock Vina run locally.
- **Literature:** PubMed / Europe PMC / PMC full text, LitVar. Every literature claim
  in the report cites a primary source; claims were verified against full text, not
  abstracts.
- **Expression:** GEO (`GSE22206`).

### Q8. Please describe any proprietary data sources used

None.

### Q9. How did you characterize the variant's mechanism?

**Loss of function**, established on four independent axes, and then refined into a
finding we did not expect.

*Direction.* Compound heterozygous *BUB1B*. Allele 1 (`c.2210T>G`, `p.Leu737Ter`)
truncates 314 of 1,050 residues, stopping immediately upstream of the pseudokinase
domain and removing all of it on every domain annotation. Allele 2 (`c.3006T>G`,
`p.Asn1002Lys`) substitutes a residue at pLDDT 91.1 inside the folded core. **Both
alleles were confirmed in the proband's own callset** — heterozygous, PASS, at maximum genotype quality —
by `proband/confirm_variants.py`. The sites are 10,911 bp apart with no physical
phasing, so *trans* remains an inference supported by the phenotype and by parental
recurrent pregnancy loss.

*Pathway.* The spindle assembly checkpoint. Loss permits anaphase with mis-attached
chromosomes, producing constitutional mosaic aneuploidy.

*Downstream consequence — and it is observed, not predicted.* Yost 2017 assigns
embryonal tumour risk specifically to biallelic *BUB1B*/*TRIP13* with severe SAC
impairment. The proband's presenting event was **rhabdomyosarcoma**, inside that
spectrum. The genotype's prediction is realised.

*The finding that changed the analysis.* Pathogenic *BUB1B* missense alleles split into
**two mechanism classes**, and stability prediction applies to only one: ΔΔG separates
pathogenic from benign at **AUC 0.952** inside the folded pseudokinase core and **0.364
— worse than chance** across the TPR/GLEBS binding interfaces. Pooling them destroys
the signal (0.714, *below* burial alone at 0.760). This reproduces Suijkerbuijk's
two-class model from structure alone, where the original came from westerns. Inside the
folding class the axis survives a **burial-matched permutation null** (AUC 0.879–0.920,
p ≤ 0.0052 at every matching window; logistic ΔΔG slope −2.53 against burial's −0.22),
which is the control that stops the result being "buried residues" relabelled as
prediction.

### Q10. Estimate of time or effort

**10–27 September 2026**, 60 commits, **48 committed scripts / ~4,700 lines**, 30
documents. Compute was modest and mostly local: the largest single job was a
757-fragment × 5-box docking screen (3,785 docks, ~1 h on 4 cores). External API cost
was negligible; structure prediction and pocket sampling used a metered third-party
service at low volume.

### Q11. Method abstract (≤500 words)

We treat drug repurposing for a single child as a problem of **choosing which allele is
reachable**, then matching an approved agent to that allele's specific failure mode —
and we report the negatives, because for an n-of-1 proposal what has been ruled out
matters as much as what survives.

The proband is compound heterozygous for *BUB1B*: a truncating allele removing the
entire pseudokinase domain, and a missense allele inside its folded core. Both were
confirmed in the proband's own callset. We first asked which allele any drug could
reach. Readthrough of the truncating allele was retired quantitatively — published
readthrough efficiencies, three unfavourable sequence-context rules, and NMD having
already consumed the substrate leave it ~35-fold short. NMD inhibition has the only
large ceiling and no paediatrically acceptable agent. That leaves the missense allele,
whose protein is made and then cleared.

To test whether it is genuinely a folding lesion we built a *BUB1B* variant atlas from
reconciled public sources — an exercise that surfaced seven distinct defect classes in
the protein-level aggregate, including stop-codon alleles typed as missense and
nucleotide letters occupying an amino-acid field — and discovered that pathogenic
missense alleles fall into two mechanism classes. Stability prediction works inside the
folded core (AUC 0.952) and is worse than chance across binding interfaces (0.364);
pooling them destroys the signal. Within the folding class the axis survives a
burial-matched permutation null, so it is not solvent accessibility in disguise. The
same calibration nominates 30 of 203 domain VUS at a 4% empirical false-positive rate.

The lead is therefore a **chemical chaperone / proteostasis regulator** — sodium
phenylbutyrate — acting *in trans*. One finding makes this specific to MVA rather than
borrowed: aneuploid human cells lose HSF1 and HSP90 and cannot mount a heat-shock
response, so the aneuploidy depletes the very folding capacity that would buffer the
destabilised protein causing it. An IL-1 blocker (anakinra, canakinumab) is retained as
an adjunct, reached by a six-gate funnel over 5,202 molecules in which three
independent instruments converged.

**Strengths.** Every number has a committed script behind it and a verifier that
re-derives it from raw records. Controls are load-bearing: four results exist only
because a control was run, including a pocket effect that benign controls reproduced
exactly and a docking campaign whose best pose sat on our own truncation artifact. We
ran an adversarial pass that refuted our own headline claim, and we report it.

**Limitations.** No chaperone inducer has ever been tested on BubR1 — this is a
mechanism-class argument. The magnitude ask (~2–3×) sits at the edge of the precedent.
A 757-fragment screen found **no ligandable allosteric site** on the pseudokinase
domain outside its functional sites, closing the structure-guided route. Everything
structural rests on a predicted model. And we asserted a phenotype feature
(microcephaly) three times from the literature before reading the clinical document,
which lists neither it nor developmental delay — a correction we foreground rather than
bury, because it is the clearest evidence of how the rest was checked.
