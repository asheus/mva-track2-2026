# The proband's actual phenotype, and the claim it corrects

**Privacy.** The organisers' phenotype document is marked *Confidential · Do not
redistribute*, and requires that nothing arising from the challenge add
re-identifying detail beyond what the family has already made public themselves.
This page therefore uses **HPO terms only** — the de-identified standard the
organisers supplied for exactly this purpose — and deliberately omits the granular
figures (gestational age, birth weight) that would sharpen identifiability in
combination. The source document is **not committed** and is excluded from the
public export. *Whether even the HPO list belongs in a public repository is a call
for the team to make before export, not a call this analysis should make silently.*

---

## What the record actually says

| Feature | HPO |
|---|---|
| **Rhabdomyosarcoma** — the presenting oncological event that triggered urgent investigation | HP:0002859 |
| **Nephrocalcinosis** — present from birth | HP:0000121 |
| **Short stature** | HP:0004322 |
| **Failure to thrive** | HP:0001508 |
| **Skeletal muscle atrophy** | HP:0003202 |
| **Premature birth** | HP:0001622 |
| **Small for gestational age** (intrauterine growth restriction) | HP:0001518 |
| **Parental recurrent spontaneous abortion** | HP:0200067 |

The organisers frame the analytic task explicitly: *no single feature is diagnostic*,
and the significance lies in the **co-occurrence** of cancer predisposition, growth
restriction, renal anomaly, adverse perinatal history and parental reproductive loss.

## The correction

Three documents in this workstream stated that this child's *"phenotype is dominated
by microcephaly and developmental delay"* — `TRACK2-REPORT.md`, `NMD-FEASIBILITY.md`
and `WHICH-ALLELE-TO-TARGET.md`.

**Neither feature appears in the record.** The claim was imported from the general
*BUB1B*/MVA literature and the BubR1 hypomorph mouse, and then written as though it
described this patient. It was never checked against the document the organisers
provided, because that document was never opened.

**What it was load-bearing for.** It supplied the safety argument against NMD
inhibition: mouse data place NMD sensitivity highest in neurological tissue, and the
argument ran that this is where *this child* is most vulnerable. That inference is now
unsupported. The concern itself survives on its own terms — chronic systemic NMD
inhibition in an infant, with no approved agent — but **the argument is weaker than it
was written**, and the honest version says so rather than keeping a convenient reason.

## What the real phenotype changes

**1. Cancer risk is realised, not prospective — and this is the biggest reframing.**
The report treats tumour risk as a predisposition to be surveilled. This child has
**already had the index malignancy**. Three consequences the deliverable did not carry:

- **The genotype–phenotype link is confirmed rather than inferred.** Yost 2017 places
  rhabdomyosarcoma in the embryonal spectrum specific to biallelic *BUB1B*/*TRIP13*
  with severe SAC impairment. The predicted tumour type is the observed tumour type.
- **Surveillance changes character.** `STANDARD-OF-CARE.md` argues surveillance
  outperforms any repurposed drug on expected benefit. That argument *strengthens*
  here, but its content shifts from prophylaxis to **survivor surveillance** — relapse
  and second primaries — which is a different protocol and a different evidence base.
- **Treatment history is now a live interaction.** A child treated for
  rhabdomyosarcoma has had cytotoxic therapy. That bears directly on the IL-1 arm's
  infection risk (§4.2's `caution_immunosuppression`) and on anything touching DNA
  damage or marrow reserve. The report reasons as if the therapeutic field were clear.

**2. Nephrocalcinosis is unengaged and touches drug choice.** A renal finding present
from birth matters for any chronic agent in a small child, and specifically for the
**sodium load** 4-PBA carries — a caveat `STABILISATION-STRATEGY.md` raises for
palatability and dosing but not against a kidney phenotype.

**3. Parental recurrent miscarriage partially closes the phasing gap.** The callset
cannot phase the two alleles (10,911 bp apart, no `PGT`/`PID`), so *trans*
configuration was an inference from the diagnosis alone. Parental reproductive loss is
independent evidence consistent with a heritable biallelic mechanism — each parent
carrying one allele — which is what *trans* predicts and *cis* does not. Still not
proof; parental genotyping remains the decisive test, and it is now clearly the single
highest-value cheap experiment available.

**4. The growth phenotype corroborates the dosage thesis.** IUGR, short stature,
failure to thrive and muscle atrophy are the growth-restriction picture BubR1
hypomorph mice show, and `ESTIMATE-BUB1B-DOSAGE` reasons from exactly that dose–
phenotype relationship. The clinical record independently supports the report's central
framing of MVA as a dosage disease — a corroboration that was available all along and
went uncollected.

## The process failure worth recording

The organisers supplied a phenotype document. It sat unread while 5,000 lines of
analysis were written about the patient it describes, and a claim about that patient
was asserted three times from the wrong source. **Nothing in the funnel, the
verifier, or the adversarial passes could catch this**, because every instrument was
pointed at the genomics and the literature, and none at the one document that
described the child. `verify_report.py` asserts every number against committed data;
it has no check that the clinical claims match the clinical record.
