# Allele 1: the NMD and readthrough route for p.Leu737*

This allele is unusually favourable, for reasons specific to where the stop codon sits.
Three independent facts line up:

1. **The transcript is destroyed, not the protein.** The PTC is 747 nt upstream of the last
   exon–exon junction (exon 17 of 23) — NMD-competent by a wide margin — and the flanking
   truncations 731X and 753X are both confirmed transcript-null in real patients.
2. **The protein this allele encodes is fully functional.** LAP-731X, six residues shorter,
   "restored the response to nocodazole as well as proper chromosome segregation in
   unperturbed mitosis", and truncations other than 194X and 753X expressed at levels
   "comparable to or higher than wild-type" once NMD was bypassed.
3. **The stop is UGA** — verified against the reference CDS (codon 737 is TTA; c.2210T>G
   makes TGA) — which is the most readthrough-permissive stop codon and the one class of
   agent that is codon-selective targets.

## The consequence that matters most

**You may not need readthrough at all.**

Readthrough restores a full-length protein. But residues 1–736 already contain *every*
known functional element of BubR1 — TPR (59–219), KEN1, D1, ABBA1, KEN2, ABBA2, GLEBS,
the Bub1-binding motif, ABBA3, D2, and the KARD/LxxIxE PP2A-B56 site at 669–674. The stop
falls in the empty stretch between the last motif (674) and the kinase domain (766).

So **stabilising the transcript alone** would produce a stable, functional, kinase-domain-less
BubR1 — which is exactly the protein Suijkerbuijk showed rescues both checkpoint and
attachment functions. NMD inhibition is a *simpler* ask than readthrough, and for this
particular stop codon it is plausibly sufficient.

That is a genuine consequence of this child's specific breakpoint, not a general claim about
nonsense alleles. A stop 100 residues earlier would take the KARD with it and this argument
would collapse.

## The two mechanisms are separable, and most drugs only do one

A point that is easy to get wrong: **readthrough agents do not rescue NMD.** Ataluren's own
regulatory documentation states it "does not alter mRNA levels, and does not affect the
process of nonsense-mutation-mediated mRNA decay." DAP likewise "did not stabilize NMD
targeted TP53 mRNAs." Readthrough acts only on the transcript that *escapes* NMD — which is
never zero, but is a small pool.

This is why the field is converging on **combination**: an NMD inhibitor to raise the
substrate, plus a readthrough agent to act on it. For this child, the first half of that
combination may be the whole therapy.

## The landscape

| Agent | Class | Stop-codon selectivity | Stage | Relevance here |
|---|---|---|---|---|
| **Amlexanox** | NMD inhibitor | n/a | **approved drug** (aphthous ulcers; asthma in Japan) | most repurposable NMD-side agent |
| SMG1 inhibitors, NMDI-14 | NMD inhibitor | n/a | preclinical | more selective, less mature |
| **2,6-diaminopurine (DAP)** | tRNA modification inhibitor (FTSJ1) | **UGA only** | preclinical; efficacy in Calu-6 xenografts | **codon-matched to this child**; higher readthrough efficiency than G418 |
| **ELX-02 (NB124)** | designer aminoglycoside | broad | **phase 2** (CF, cystinosis); ~100× less antibacterial than gentamicin, 10× CFTR rescue | best-developed readthrough agent with a tolerable profile |
| Gentamicin, G418 | aminoglycoside | broad | old; oto/nephrotoxic | not viable chronically in a child |
| Ataluren | oxadiazole | broad | **EU authorisation not renewed (CHMP, 26 Jan 2024)**; never FDA approved | failed every primary endpoint |
| CC-90009, SJ6896, SRI-41315 | eRF1/eRF3a degraders | broad | preclinical | mechanism distinct from ribosomal agents |
| Suppressor tRNAs (engineered) | nucleic acid | **engineerable to the exact codon** | preclinical; ReCode RCT101, engineered Glu-tRNA | highest ceiling, earliest stage |
| NV848/NV914/NV930, NV2445 series | non-aminoglycoside TRIDs | UGA-focused (FTSJ1) | preclinical | same target as DAP |

## What DAP would actually do at residue 737

DAP works by inhibiting FTSJ1, the 2′-O-methyltransferase that modifies tRNA-Trp, so
readthrough "resulted in the exclusive insertion of a **tryptophan** residue at the PTC."

So DAP would produce BubR1 with **Leu737Trp**. Two reasons that is a tolerable substitution
here, and one caution:

- Residue 737 sits at the boundary of the long disordered linker (600–749 mean pLDDT 44.8),
  not inside a folded domain and not in any annotated motif.
- Leu→Trp is hydrophobic→hydrophobic. It is bulky (+61 Å³), but a disordered linker is the
  most forgiving place in the protein to absorb that.
- **Caution:** residue 737 has 7.5% solvent accessibility in the AlphaFold model, so it is
  not fully unstructured. A Trp there is an assumption to test, not a free pass.

The comparison worth making: readthrough inserting one substitution into a disordered linker
is a far smaller structural gamble than the *other* allele's N1002K, which sits in a packed
aromatic pocket in the folded core.

## Identity is favourable here; efficiency still is not

Added 22 Oct 2026, prompted by a third-party report that pointed at the primary source
without drawing this conclusion (`TOOL-TRIAGE-KOSMOS-NAD.md`).

The proband's allele-1 change is `TTA→TGA` — a single base at position 2 of the codon. So
the **wild-type residue at 737 is leucine**, and leucine is reached from UGA by exactly that
one-base near-cognate mispairing. According to PubMed, Xue 2017 measured the amino acids
actually inserted during G418-mediated suppression of the CFTR W1282X UGA and found
**leucine, cysteine and tryptophan**, with proportions that differed significantly from the
UGA at G542X — local sequence context, not the stop codon alone, selects the near-cognate
tRNA ([PMID 28575328](https://doi.org/10.1093/hmg/ddx196)).

That makes this PTC unusually favourable in *identity*, and it inverts the agent ranking on
that one axis:

| Agent | Residue inserted at 737 | Product |
|---|---|---|
| G418-class (Leu among the measured insertions at UGA-A) | leucine | **true wild-type BubR1** |
| DAP / NV-series (FTSJ1, tRNA-Trp) | tryptophan | Leu737Trp substitution |

A readthrough event that restores the wild-type residue produces wild-type protein, not a
variant — which would retire the Leu737Trp structural caution above entirely.

**This does not revive the route.** Two things still block it. Xue 2017's own headline is
that context determines identity, so leucine insertion in `GAG-UGA-AGU` is a hypothesis to
measure, not a property to assume. And the route was retired on **efficiency**, not on
identity: the measured best case is +0.53 percentage points of BubR1
(`WHICH-ALLELE-TO-TARGET.md`). Restoring the right residue 0.5% of the time is still 0.5%.
Logged because if the efficiency ceiling ever moves, the agent class to reach for at this
codon is the leucine-inserting one, and that is not the one the codon-matching logic picks.

## What disqualifies each route

**NMD inhibition** is the mechanistically elegant option and the hardest safety case. NMD is
a global surveillance pathway regulating a large fraction of the transcriptome and is
essential in development. Chronic systemic NMD inhibition in a growing child stabilises
every PTC-containing transcript, not only this one. Amlexanox's approved use is topical or
short-course; chronic systemic use at NMD-inhibiting exposure is not an established regimen.
**This is the binding constraint, not the mechanism.**

**Aminoglycoside readthrough** carries oto- and nephrotoxicity as a class. ELX-02 was
engineered specifically to escape that, and its phase 1 in healthy subjects showed
dose-proportional exposure with injection-site reactions as the main event — which is why
it is the most credible near-term candidate despite being unapproved.

**Ataluren** should be treated as a negative result, not an option. It never met a primary
endpoint and its conditional EU authorisation was not renewed.

**Everything here is off-label or pre-approval.** There is no approved therapy for MVA of any
kind, and nothing in this table has ever been given to an MVA patient. This is a map of a
development path, not a treatment plan.

## What Gate 3 should record

- **HSP90 inhibitors: REFUSE.** Mechanism-derived contraindication — they remove virtually
  all destabilised BubR1, which is this child's entire supply. (See
  `ALLELE2-FOLDING-DOSSIER.md`.)
- **Aminoglycosides as a class: REFUSE on chronic use**, allow ELX-02 as a
  distinct entity given its engineered separation from antibacterial and toxicity profiles.
- **Ataluren: REFUSE** — regulatory failure, not merely unproven.

## The cheapest decisive experiment

Before any of this, one experiment separates the two halves of the problem:

**Treat the child's cells with an NMD inhibitor and blot for BubR1.** If a ~85 kDa truncated
band appears and total functional BubR1 rises, allele 1 is rescuable by transcript
stabilisation alone and the readthrough question becomes secondary. If nothing appears, the
NMD model is wrong and the whole route closes.

That is a cell-culture experiment on material that would already have been collected for the
western blot the dosage estimate depends on.
