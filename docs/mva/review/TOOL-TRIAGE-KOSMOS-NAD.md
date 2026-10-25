# Triage: "BubR1 Rescue Through NAD⁺ Modulation" (Edison Scientific / Kosmos)

**Verdict: nothing load-bearing is new.** Every claim in it that could move a decision, we
already hold — usually in a more quantitative form, and in two places with an uncertainty
the report does not notice. Two minor facts are genuinely new and one of those is moot.

*Assessed 22 Oct 2026. Delivered twice — a zip containing one markdown file, then an
18-page LaTeX PDF of the same four discoveries. Both extracted and read in isolated
directories.*

## What it is

A machine-generated "discovery report", Project ID `04f85bd3-32fd-4772-95b5-a90bb829b1ff`,
dated 2026-10-22. Four sections: the NAD⁺–SIRT2 axis, readthrough of c.2210 under NMD
constraint, degradation modulation (APC/C-Cdh1, proteasome, chaperones), and N1002K
destabilisation with chaperone dependency.

Three structural facts about the document decide how it can be used:

**1 · Its prompt was our own output.** The "Research Objective" section is a verbatim paste
of a previous answer in this session, headings included — `## Why arimoclomol doesn't take
the top spot`, `## Where we stand`, the +1.51 kcal/mol figure, the 1.43× gap, the waveform
argument, the 6-residue reasoning. Anything in the report that agrees with us may be
agreement or may be echo, and the document gives no way to tell the two apart.

**2 · "Dataset Description" is empty.** It analysed no primary data of its own.

**3 · There is no bibliography.** Every inline citation resolves either to a
`platform.edisonscientific.com/.../trajectories/...` URL — the generator's own internal
working, not a source — or to a publisher PDF link. Under rule 10's standard and the
standing rule that third-party model output is never a source of a verdict, score or
number, every figure in it is unusable until traced to the primary source itself.

## The load-bearing claims, traced

Three claims could have changed a decision. All three check out against the primary
literature, and all three were already in this repository.

| Claim | Primary source | Verdict | We already had it |
|---|---|---|---|
| Lifespan extension in `Bub1b^H/H` is from **SIRT2 overexpression**; NMN only raised BubR1 *abundance*, with **no** NMN/NR-treated survival cohort | North 2014, EMBO J — [PMID 24825348](https://doi.org/10.15252/embj.201386907) | **Confirmed** from the abstract | Yes — this is exactly the distinction our own text (pasted into its prompt) already drew |
| Kinase-domain BUBR1 missense mutants are **HSP90-dependent**; wild-type is not; MG132 prevents the loss | Suijkerbuijk 2010, Cancer Res — [PMID 20516114](https://doi.org/10.1158/0008-5472.CAN-09-4319) | **Confirmed** verbatim in the full text | Yes — `ALLELE2-FOLDING-DOSSIER.md` row 3, with the same quote |
| G418 readthrough at a UGA-A premature stop inserts leucine, cysteine and tryptophan, in context-dependent proportions | Xue 2017, Hum Mol Genet — [PMID 28575328](https://doi.org/10.1093/hmg/ddx196) | **Confirmed** (abstract names the three residues and the context-dependence) | Partly — `ALLELE1-NMD-READTHROUGH.md` works the identity question at residue 737 for DAP |

Everything else — the GTEx co-expression sweep, the BioPlex CompPASS-Plus scores, the FZR1
2.2×, the proteasome-inhibitor fold-changes, the palbociclib percentages — cites only
internal trajectories. Not citable.

## Where we were already ahead

**Readthrough.** The report calls the c.2210 UGA "technically addressable" and designs a
four-part combination around it. We retired readthrough for this child on measured
distributional data: `WHICH-ALLELE-TO-TARGET.md` puts the realistic best case at **+0.53
percentage points** of BubR1 (DAP, top-decile PTC), against 17 of 5,800 PTCs exceeding 1%
untreated. A combination strategy built on an agent that cannot clear one percentage point
is not a strategy. The report never quantifies the efficiency it needs.

**The truncated allele.** The report treats allele 1 as reachable only by readthrough.
`bub1b-dosage-review/REPORT.md` and `WHICH-ALLELE-TO-TARGET.md` already carry the sharper
observation from the same 2010 paper — LAP-731X, lacking the whole kinase domain, *fully*
restored checkpoint and alignment — and, unlike the report, carry the uncertainty with it:
753X **fails** where 731X rescues, our 737X sits between them, and we called it **~70/30**
off a two-point calibration rather than asserting it.

**The threshold.** `bub1b-dosage-review/extracted_units.json` D01/D02 hold the only explicit
titration in the BubR1 literature (~13% residual near-silent, ~6% grossly missegregating),
flagged as the single such experiment and corroborated independently in Cdc20. The report
does not mention it.

## Where it is weaker than it reads

**Its own trajectories disagree, and the synthesis smoothed it.** Discovery 4's summary says
"independent proteomics support co-purification and proximity of BubR1 with HSP70-family
members." Trajectory r27's own conclusion, printed in the PDF's appendix, is: *"I did not
find convincing evidence that BUB1B is a cytosolic HSPA1A/HSPA8 client."* Association (r97)
and dependency (r27) are different findings; leading with the first and appending the second
is the failure mode that makes this class of output unsafe to cite.

**The chaperone screen could not have answered its own question.** Discovery 4 surveys bulk
proteomics for changes in **wild-type** BUB1B after HSP90/HSP70 perturbation, and finds
nothing consistent. That is the expected result, not a negative one: Suijkerbuijk 2010 showed
wild-type BubR1 is *unaffected* by geldanamycin while the kinase-domain mutants collapse. The
client is the mutant. A wild-type survey is blind to the hypothesis by construction — and the
affirmative answer had been in print since 2010.

**The GTEx co-expression is circular, and its one relevant tissue points the other way.**
BUB1B is a proliferation marker; correlating it with anything across bulk tissue is dominated
by proliferating-cell fraction. The report concedes this in a clause and then reports 516
significant associations as plausibility. Note which tissue breaks the pattern: cultured
fibroblasts, ρ = **−0.665** — the strongest correlation in the set, negative, in the exact
cell type a patient assay would use.

**The human NAD⁺ trial data is a measurement floor, not a result.** No BUB1B mRNA change
after NR or NMN — with BUB1B at zero normalised counts in 20 of 24 samples and a median of 3
raw reads. The report says so itself. It cannot bear weight in either direction.

## What is actually new

Two items, both small:

1. **ORC-13661**, an otoprotectant reported not to interfere with aminoglycoside
   antibacterial activity (Chowdhury 2018). Not in our docs. **Moot** — it de-risks a route
   we retired on efficiency, not on toxicity.
2. **CDK4/6 inhibitors lower BUB1B** (palbociclib, reported 89.4% mRNA / 71.1% protein in
   T-47D). Untraced to a primary source, so not citable as a number, but directionally it
   belongs on an *avoid* list for any cell system meant to raise BubR1. Worth confirming.

One refinement for the record, derived from our own verified codon context plus Xue 2017
rather than from the report: because the proband's allele-1 mutation is `TTA→TGA`, the
wild-type residue at 737 **is leucine**, and leucine is a major near-cognate insertion at
UGA-A. A G418-class agent would therefore restore the *true* wild-type residue at this
codon, where DAP — inserting tryptophan via tRNA-Trp — gives Leu737Trp. That makes this PTC
unusually favourable in *identity*. It remains retired on *efficiency*, and identity does
not rescue a +0.53 pp ceiling.

## The rule this reinforces

A report whose prompt was our own output, whose dataset section is empty, and whose
citations resolve to its own working is not independent evidence, however calibrated its
prose. The three things in it worth having were already in the repository, and the way we
established that was by pulling each primary source and reading it. That is the only
operation that distinguished agreement from echo — and it is cheap. Do it before, not after,
letting a document like this move anything.

---

## Addendum, 23 Oct 2026 — seven further reports, run blind to the genotype

Seven more externally generated reports were triaged (kinase inhibitors/bosutinib; a four-agent
readthrough ranking; nephrocalcinosis causation; HSP90 inhibitors; genotype–phenotype
concordance; allele-directed modalities; proteasome inhibitors; NMD inhibitors).

**The decisive defect: they were run without the proband's genotype.** Several state it
outright — *"the child's exact BUB1B variants ... were not provided"*, *"reports r1–r7 were
unavailable"*. They then filled the gap by inference, and got it wrong in the same way
repeatedly:

| They assumed | Actually | Why it matters |
|---|---|---|
| `p.Trp737*` | **`p.Leu737Ter`** (c.2210T>G, TTA→TGA) | A Trp stop favours DAP (inserts Trp via tRNA-Trp); a **Leu** stop favours a Leu-inserting agent. The recommendation inverts. |
| "the patient-associated missense variant **L1012P**" | **`p.Asn1002Lys`** | L1012P is a *different* published allele 10 residues away that we carry as the closest measured analogue. Asn→Lys is a charge introduction at a buried site; Leu→Pro is a helix break. Different lesion, different rescue logic. |
| "p.Leu1002Pro is the mouse equivalent of human L1012Pro" — implying 1002 is a mouse coordinate | Human residue **1002 is asparagine** and **1012 is leucine**, both verified against UniProt O60566 (`K F F V R I L N A N D E A T V S V L G E L` for 995–1015) and against our own ThermoMPNN table (`Wildtype AA = N` at 1002) | The species warning is a false alarm for us. Sieben 2019 *did* model human L1012P as mouse L1002P, which is probably the source of the confusion — but it says nothing against N1002K. |

Everything in those reports conditional on allele identity is therefore unreliable, which is
most of their content. Their shared conclusion — that no agent can be recommended — happens to
match ours, but it is reached without the facts that would decide it, so it is agreement by
coincidence rather than corroboration.

**What they were nonetheless worth.** Two of their citations corrected *our* central framing,
and both are logged as **C48**: Holder 2020 shows BubR1 is not among the proteins rapidly
destroyed at anaphase, which narrows the "waveform" constraint I had asserted throughout; and
Sieben 2019 concludes that BUBR1 allelic effects operate *beyond protein level*, which
unseats total abundance as a sole target variable and endpoint.

That is the pattern worth recording: **a report can be wrong about the patient and still point
at a paper that corrects you.** The value was in the reference lists, not the reasoning, and
extracting it required pulling every primary source rather than reading the summaries.
