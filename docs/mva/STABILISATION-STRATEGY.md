# Stabilising allele 2: what the biology actually supports


> **SUPERSEDED IN PART, 14 Oct 2026.** This file ranks 4-PBA first, partly on its
> HDAC activity. That leg is **retracted**: HDAC inhibition induces premature sister
> chromatid separation and strips BubR1 from kinetochores, and MVA1's other name is
> premature chromatid separation syndrome. Arimoclomol (FDA-approved Sep 2024,
> children ≥ 2) carries the matched mechanism without it and is now the lead; 4-PBA
> is kept as a stated alternative with the hazard attached. See
> `CORRECTIONS-2026-10-06.md`, C5 and C7, and `TRACK2-REPORT.md` §3.3. The fold-class
> reasoning below is unaffected — only the ranking inside the chaperone class moved.

Target: raise BubR1 from an estimated ~17% toward ~50% (carrier-equivalent), where the MVA
syndrome does not appear. That is a **~3-fold** ask. Partial benefit is expected between
~35% and ~50%, since that is where the phenotype resolves.

**Nothing here is a treatment recommendation.** It is mechanism-led hypothesis generation
for a single child, built entirely from published preclinical work, with no possibility of
experimental confirmation in this workstream. Any use would be off-label and n-of-1, and
the decision belongs to treating clinicians.

---

## 1. A sequence check that changes the SIRT2 arm

The literature disagrees about the SIRT2 site on BubR1: Bloom & North say **K668**;
Jing & Lin and Qiu et al. say **K688**. Checked directly against `ENSP00000287598`:

- residue **668 = K** ✓, and **668–675 = `KLSPIIED`** — an exact match to the published
  LxxIxE PP2A-B56 binding motif.
- residue **688 = S**. Not a lysine. **The "K688" papers have the number wrong.**

This matters because it places the SIRT2 site **inside the B56-binding motif itself**.
Bloom & North list K668 as one of four residues that physically contact PP2A-B56. So
acetylation at K668 does two things at once: it blocks phosphatase recruitment *and* flags
BubR1 for ubiquitination. SIRT2 reverses both.

Elegant — but note what it is: a regulator of **physiological** BubR1 turnover, the pathway
behind the age-related decline in BubR1.

## 2. The argument that decides the ranking: which degradation route are we in?

Our child's problem is a **misfolded** protein. Suijkerbuijk showed how those are cleared:
levels collapse under HSP90 inhibition, cycloheximide plus geldanamycin removes virtually
all of the mutant, and proteasome inhibition rescues it. That is **chaperone-dependent
quality control**.

The SIRT2/K668 axis is a different route — CBP acetylation driving ubiquitination of the
*normally folded* protein.

**These are not the same pathway.** SIRT2 activation or NAD+ repletion targets physiological
turnover; our problem is quality-control triage. That is a mechanism mismatch, and it is the
strongest reason to rank the chaperone arm above the sirtuin arm — despite SIRT2 being where
this workstream was heading.

## 3. A hazard on the SIRT2 arm specifically

SIRT2 also deacetylates **K250**, where acetylation is *protective* — it shields BubR1 from
APC/C-mediated degradation. So SIRT2 activation has one arm pointing each way.

How dangerous is the wrong arm? The knock-in mouse answers it. BubR1 K243R (mouse
equivalent of human K250R, acetylation-defective):

> "We monitored 339 live animals from BubR1K243R/+ intercrosses and **failed to identify any
> homozygous mutant newborn pups**."

**Homozygous loss of K250 acetylation is embryonic lethal.** Heterozygotes survive but
develop aneuploidy and spontaneous tumours. This is not a residue to perturb in a child
whose disease is already chromosomal instability plus cancer predisposition.

Net in-vivo evidence for SIRT2 is still positive — SIRT2 overexpression extends lifespan in
BubR1 hypomorphic mice — but that was measured in a hypomorph (low levels of *normal*
protein), not a misfolding mutant. **Wrong model for this child.**

## 4. Why 4-PBA leads, and it is not close

Sodium phenylbutyrate hits **three mechanisms that all point the same way here**:

1. **Chemical chaperone** — assists folding directly, which is the actual lesion.
2. **HSP70 inducer** — raises quality-control capacity. Precedent is strong: HSP70-inducing
   treatments restored function to **17 of 18 (94%)** missense CBS mutants and 19 of 25 (76%)
   mutant p53 proteins.
3. **HDAC inhibitor** — HDAC2/3 are what *remove* the protective K250 acetylation, so
   inhibiting them **preserves** it. Opposite direction to the SIRT2 hazard above.

And it has the selectivity profile you would want. In RPE65 missense disease, PBA
*"expression levels of WT RPE65 were not significantly changed by treatment with PBA...
whereas expression levels of the three mutant RPE65s were significantly increased."*
**It raises the unstable allele without over-raising normal protein** — which matters when
the protein in question is also an oncogene-adjacent mitotic regulator.

Track record across destabilising missense disease: ABCC6 (pseudoxanthoma elasticum),
dysferlin, ABCB11 (PFIC2), OCT3, RPE65, SLC6A1 encephalopathy.

**Safety is the real reason it leads.** Approved for chronic management of urea cycle
disorders — a neonatal-onset paediatric indication with decades of use and multiple
formulations. That is not a theoretical safety profile; it is babies, for years.

**Carried, not buried:** the FDA review of Ravicti (glycerol phenylbutyrate) flagged
"potential neurotoxicity in pediatric patients under two years of age" and required
post-marketing PK studies in infants. Sodium load and palatability are also real issues in
chronic paediatric dosing.

## 5. Ranked

| | mechanism match | magnitude precedent | paediatric safety | verdict |
|---|---|---|---|---|
| **4-PBA** | **folding + quality control + K250 preservation — all correct** | 94% rescue of CBS missense; mutant-selective | **approved, neonatal indication** | **lead** |
| Arimoclomol / HSF1 co-inducers | correct (chaperone amplification) | rescues glucocerebrosidase, destabilised rhodopsin | **FDA-approved (Miplyffa, 20 Sep 2024), children ≥2**; not an HDAC inhibitor | **first** (C7) |
| SIRT2 activation / NAD+ | **wrong degradation route**, plus K250 hazard | strong — but in a hypomorph, not a folding mutant | precursors widely used, not in this indication | **demoted** |
| Proteasome inhibition | correct route, but | rescues in vitro | not viable chronically in a child | no |
| HSP90 inhibitors | **actively harmful** | — | — | **REFUSE** |

## 6. What this does not establish

- **Nobody has ever tested 4-PBA, or any chaperone inducer, on BubR1.** Not once. Every
  precedent above is a different protein. This is a mechanism-class argument.
- **The magnitude is at the edge.** Chemical chaperones typically deliver 1.5–3× rescue of
  destabilised mutants. We need ~3×. That is the optimistic end of the observed range, not
  the middle.
- **It rests on N1002K being a folding mutant** — now ~92% confident, but still inference.
  If it is not, 4-PBA's rationale collapses entirely.
- **4-PBA's HDAC inhibition is broad**, and broad epigenetic modulation in a
  cancer-predisposed infant carries its own questions that this analysis does not answer.

## 7. The thing that should not get lost

`STANDARD-OF-CARE.md` established that **expected benefit from surveillance done well is
almost certainly greater than expected benefit from any repurposed drug we can currently
propose** — LFS-style surveillance moves 5-year survival from 59.6% to 88.9%, and MVA
tumours cluster in the first three years of life.

Nothing in this document changes that. A mechanistically satisfying drug hypothesis is not
a substitute for the intervention that actually has outcome data behind it. If only one
thing is acted on, it should be surveillance.
