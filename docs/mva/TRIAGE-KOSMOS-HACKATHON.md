# Triage — Kosmos "Hackathon" run, 24 Oct 2026

Two uploads, one report: `Hackathon_report.md` (209 lines) and a 16-page typeset
PDF. Same prose. **The PDF is not a duplicate** — it carries seven figures that
exist nowhere in the markdown, and those figures are the most valuable part of
the run. Project ID 176a0ce8-ff98-4159-bb30-9f45bd1dd402.

Prompt used: the "gently guide, have it fact-check you" version.

## What it did not deliver

The brief asked for a ranked table of ten drugs, a single best candidate, and a
section naming which of our seven conclusions it could not reproduce. **None of
the three exists.** Trajectory r0 says why, in its own words:

> "I cannot justify calling ten drugs treatments for this child."

That is a refusal on evidentiary grounds, not a failure to follow format, and it
is the correct call. But it means the deliverable has to be assembled by hand
from three "discoveries" and twelve trajectory summaries.

`Dataset Description` is **empty** — same as the NAD+ run. No dataset was
analysed. This is a literature-plus-computation run.

## Citation discipline — the one hard rule it broke

The brief said every factual claim carries a PMID or DOI. The markdown body
cites almost entirely `[rN](platform.edisonscientific.com/.../trajectories/...)`
— internal links, unresolvable by us, dead to any reader. Some primary
citations do appear (sansregret2017, braga2020, suijkerbuijk2010, xu2013,
krivega2021, halliwell2020, shah2016), but **no PMIDs anywhere**. Every number
below is therefore UNVERIFIED by us and must be traced before it ships.

---

## 1 · The finding that changes our thesis — and it is convergent, not a refutation

Figures 1–3 are original in-silico work on N1002K. Three results:

| analysis | N1002K | I909T / L1012P |
|---|---|---|
| I-Mutant2.0 ΔΔG | +1.35 | both destabilising |
| DynaMut2 ΔΔG | **+0.01 (neutral)** | both destabilising |
| relative solvent accessibility | 14.2% — Kosmos labels this *"solvent-exposed"*; **the label is wrong, see C52** | buried β-strand / α-helix |
| REVEL vs AlphaMissense | 0.472 vs **0.923** — opposing ranks | consistent |

Trajectory r2: *"N1002K is plausibly deleterious, but my results do not establish
the strong protein-instability mechanism seen for I909T and L1012P. Both executed
stability methods rank N1002K as the least destabilizing substitution."*

**We computed 14.0% RSA for the same residue** (`ALLELE2-FOLDING-DOSSIER.md:57`)
and we have I909T at 3.6% (`N1002-STRUCTURAL-COUPLING.md:29`). Two independent
pipelines, 14.0 vs 14.2 — this is convergence, not contradiction.

What we did with it is the difference. `ALLELE2-FOLDING-DOSSIER.md:87` already
says *"RSA 14.0% is mostly, not fully, buried, so an interface role is not
excluded"* — and then the dossier goes on reasoning from destabilisation anyway.
Our ThermoMPNN ranking (`ASSAY-DESIGN.md:94-96`, N1002K +1.507 "most
destabilised") compared N1002K against **other substitutions at position 1002**
— a within-site ladder, which cannot say whether N1002K is destabilised relative
to the known MVA instability variants. Kosmos used the decision-relevant
denominator and we did not.

**Consequence — WITHDRAWN 24 Oct 2026 (C52).** RSA 14% is buried, not exposed; our own work calls N1002 a *buried staple*, 87% buried, and rates it ~85% a pure dosage mutant. The paragraph below was written on Kosmos's mislabel and is retained only as a record of the error. If allele 2 were an exposed-loop variant that disrupted
pseudokinase→KARD *communication* rather than fold integrity, then the
Suijkerbuijk abundance-restoration logic — derived on I909T and L1012P, both
buried — does not transfer to this allele. Raising the amount of a protein that
is present but miscommunicating buys nothing. The chaperone / E3 / "slow its
degradation" family loses its primary rationale for this patient.

This is a demotion of our own leading route, arrived at independently, from a
caveat we had already written and then walked past.

## 2 · The compensating idea — both alleles fail at the same node

Discovery 2's central claim, which we had not assembled:

- **Allele 1** (L737Ter, if translated): lacks the pseudokinase domain. The
  "731X" construct shows reduced KARD S670/S676 phosphorylation, weakened
  PP2A-B56 recruitment, delayed checkpoint silencing.
- **Allele 2** (N1002K): buried pseudokinase-domain variant (C52) reducing abundance, hence less
  control of the KARD — same downstream readout.

**Both alleles converge on insufficient PP2A-B56 at the kinetochore.** Not two
diseases needing two drugs. One node, reached two ways. That is a materially
better thesis than the one we are shipping, and it is the one sentence most
worth lifting into the report.

Direct support cited: in patient-derived MVA fibroblasts, ectopic BubR1 **or
enforced kinetochore recruitment of PP2A-B56** corrected alignment; PLK1
inhibition did not substitute (xu2013, braga2020).

## 3 · A real correction to the 731X story

The construct called "731X" in the 2010 work **actually contains residues
1–715**; the patient would retain 1–736. And later work at matched kinetochore
levels showed 731X *is* compromised in KARD/PP2A — the 2010 "truncation retained
function" result tested checkpoint *maintenance*, the later work tested efficient
*silencing*. Different functions, different answers. Our documents lean on the
2010 reading. **Trace and fix.**

## 4 · The best rescue data anyone has produced — Sansregret 2017

Non-transformed hTERT-RPE1 with a pharmacologically weakened checkpoint
(350 nM reversine — i.e. our disease model), plus 1.5–4 µM proTAME:

- NEB→anaphase 16 min → 22–35 min
- **segregation errors 90% → 34%**

Tetraploid RPE1, 3 µM proTAME: bipolar divisions 40% → 60% (p = 0.01); lagging
chromosomes 27% → 8% (p < 1e-4).

And the discriminating control, which is what makes it credible: **delay alone
is not enough.** 33 nM nocodazole and a Src inhibitor both lengthened mitosis
and made missegregation *worse*; 2 nM paclitaxel drove ~50% missegregation in
MPS1-reduced fibroblasts. So the benefit is specific to APC/C restraint, not to
"more time in mitosis."

This is the first result in the whole project that **rescues missegregation in a
checkpoint-weakened non-transformed human cell with a small molecule.** It is
exactly the mechanism our patient lacks: BubR1's job is restraining APC/C-Cdc20,
and proTAME restrains APC/C.

**The catch, stated honestly by Kosmos:** proTAME, apcin and CP5V are research
tools with no clinical PK. Trajectory r102 found no approved drug with specific
APC/C inhibition at achievable free exposure.

So: perfect mechanism, no drug. For a hackathon that may be the stronger finding
— a named target with quantitative proof-of-concept in the right cell model,
and a precise statement of the gap.

## 5 · Momelotinib — the only approved drug that enters the band

Figures 6–7: eight approved agents ranked by R = free Cmax / Aurora B IC50,
against a target band of 0.1–1.0.

| drug | R |
|---|---|
| **momelotinib** | **0.104 – 1.04** (only one in band) |
| pexidartinib | <0.321 (0.0642 on ChEMBL 643 nM; 0.265 on a 156 nM assay) |
| brigatinib | <0.224 |
| entrectinib | <0.0313 |
| sorafenib | 0.0278 |
| sunitinib | 0.00604 |
| dasatinib | 0.00104 |
| abemaciclib | <0.000969 |

Momelotinib is approved, oral, systemic (JAK1/2 + ACVR1, myelofibrosis).
**Caveat flagged in the figure itself:** its range is inferred from single-point
potency, not a fitted IC50. Soft, but it is the single best approved-drug lead
the run produced and it was reasoned from mechanism, not indication.

Figure 4 adds a caution that cuts the other way: **ZM447439 — the compound that
produced the 2 µM Aurora-B rescue — is dirty**, inhibiting many kinases at
submicromolar across a ~150-kinase panel. The rescue may not be pure Aurora B.

## 6 · The one genuine threat to a conclusion we shipped

**Conclusion 2 (amlexanox) is half-defeated and half-defeated-back.**

Kosmos (trajectory r5): *"the available human pharmacokinetic evidence does not
establish that 25 µM free amlexanox is unattainable at a tolerable oral dose;
nor does it rule out effects at lower concentrations."* Its source is `oral2017`
— the US trial. **It never found the PMDA interview form.** We have measured
Cmax 5.40 µg/mL (18.1 µM total) and measured 98.4–99.4% binding, non-saturating
to 168 µM → free Cmax 0.11–0.29 µM. On the first half, our primary-source dig
beats the agent and conclusion 2 stands.

**The second half does not.** It cites carrard2023 for amlexanox activity from
**0.4 µM**, not 25 µM. Against 0.4 µM our free Cmax of 0.11–0.29 µM is
**1.4–3.6× short, not 90–900× short.** Our dismissal
(`SYSTEMIC-REPURPOSED-WHAT-SURVIVES.md:24`) is computed against the top of the
reported range and reads as though it were computed against the whole of it.

That number appears in `SYSTEMIC-REPURPOSED-WHAT-SURVIVES.md`,
`ALLELE1-APPROVED-DRUGS.md` (×4) and `TRACK2-REPORT.md`. **This needs a
correction before anything ships.** The honest form: 90–900× short of the
concentration at which the TBK1/TFEB separation is reported (50–100 µM,
krivega2021), but only ~1.4–3.6× short of the lowest reported NMD-reporter
activity (0.4 µM, carrard2023) — a gap a dose change cannot close (fed
50→100 mg gives 1.47×) but which is **not** the order-of-magnitude wall we
described.

## 7 · Conclusion 5 is too strongly worded

Trajectory r51: *"The categorical claim that the human BUB1B/BubR1 C-terminal
region has no small-molecule-binding pocket is not supported"* — bubristatin-1
(BRT-1) associates with BubR1, maps to an αN1/αC interface, perturbs
BubR1-dependent CENP-E phosphorylation.

Our 0/757 fragment result bounds **our screen against the site we chose**. It
does not bound the protein. `ALLELE2-ROUTES-REEXAMINED.md:175` already concedes
this is "a result about the selected site in one domain, used as if general" and
then defends the generalisation. Reword to: *no approved ligand with quantified
human exposure and a co-structure exists.* That is true and survives.

## 8 · An internal inconsistency in their own report

Discovery 2 prose: azacitidine *"regulatory documents indicate low protein
binding (fu 0.88–0.94)."*
Trajectory r36: fu values are *"from two distinct, published **structure-based
models**: pkCSM and Deep-PK"* — predicted 0.715 and 0.8542.

The prose upgrades a QSAR prediction into a regulatory document, and shifts the
numbers. If we use the azacitidine NMD lead at all, it carries **predicted**
protein binding, not measured. (The lead itself is interesting: approved,
parenteral, systemic, NMD-inhibitory — becker2021. Killed for now by ~0.5 h
parent half-life and no washout-durability data, trajectory r71.)

## 9 · Confirmed, with better reasons than we had

- **Conclusion 1 (readthrough).** Ataluren measured 99.6% binding, fu ≈ 0.004,
  free Cmax ~0.10–0.20 µg/mL. Harder number than ours.
- **Conclusion 4 (HSP90).** Confirmed — HSP90i preferentially reduced I909T and
  L1012P, later linked to reduced KARD phosphorylation.
- **Proteasome route.** Better reason than ours: 25–100 nM bortezomib in
  hTERT-RPE1 produced attrition and **increased micronuclei in survivors** —
  the precise endpoint we are trying to reduce.
- **Palbociclib as STING activator.** Closed: active at 0.5–1 µM, free peak
  0.033–0.039 µM, 13–15× short.
- **Conclusion 6 (K250).** The unverifiable claim is **real**: HDAC2/3-mediated
  deacetylation at K250 promotes timely checkpoint silencing; K250Q mimic
  prolonged aligned metaphase ~45–55 min. But Kosmos adds that SIRT2 *can* also
  act at K250 in some contexts. So conclusion 6 is **softened, not refuted** —
  the hazard is real but no longer SIRT2-exclusive. Still untraceable without a
  PMID.

## 10 · Unexplored threads worth one hour each

- **Perphenazine and penfluridol** are named (trajectory r43) as the approved
  drugs that *do* increase PP2A activity experimentally. Both are approved
  antipsychotics. Given §2 says PP2A-B56 is the convergent node, this is the
  most on-mechanism approved-drug thread in the report and Kosmos set it aside
  without an exposure calculation. CNS liability in a child is serious, but the
  exposure arithmetic is one afternoon.
- **HSF1.** Aneuploid cells have *reduced* HSF1 and an impaired inducible
  heat-shock response; restoring HSF1 improves folding and tolerance
  (passerini2016). We withdrew arimoclomol's borrowed magnitude (C47) — but the
  *target* is reopened, and "proteotoxic stress ≠ constitutive HSF1 activation"
  is a distinction we did not have.
- **Nucleoside rescue.** Halliwell 2020: replication rescue needs 15 µM each of
  adenosine/guanosine/cytidine/uridine + 6 µM thymidine. Uridine triacetate
  (approved) exceeds 15 µM uridine; Kygevvi supplies deoxythymidine. Guanosine
  and adenosine have no established systemic route — so faithful reconstruction
  fails, but it is a genuinely non-obvious approved-drug angle we never
  considered.
- **Ceralasertib.** Clinical-stage, not approved, so out of scope for
  repurposing — but it carries the one explicit normal-cell therapeutic window
  in the report: 0.1 µM for 48 h reduced pCHK1-Ser345 in primary human
  conjunctival fibroblasts **without detectable apoptosis**, while 1 µM caused
  apoptosis.

## Verdict

The best Kosmos run we have had, by a distance, and the first whose structural
figures are original rather than borrowed. It behaved correctly where it
mattered — it refused the ten-drug format rather than padding, it reported
disagreement between its own predictors instead of averaging it away, and its
single most useful output is a demotion of our own leading route.

It is also unciteable as delivered. Before any of this ships: every number
above needs a PMID, and the amlexanox correction (§6) needs to be written into
the four files that carry the 90–900× figure.

Two things in it are worth more than a tenth candidate: **§2** (both alleles
fail at PP2A-B56) and **§4** (90% → 34% in the right cell model).
