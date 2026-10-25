# Every reported *BUB1B* nonsense variant, scored two ways — and why allele 1 is alone

**Run 13 Oct 2026.** Reproduce with
`apps/api/scripts/mva/nmd/stratify_bub1b_ptc.py`; inputs and outputs in
`data/nmd/`.

`NMD-FEASIBILITY.md` argued that NMD inhibition is a coherent idea for allele 1 and
incoherent for most *BUB1B* truncating alleles, because it depends on **two** independent
things being true at once:

1. the transcript has to survive — otherwise there is nothing to rescue; and
2. the truncated product has to retain the functional motifs — otherwise rescuing the
   transcript yields a useless protein.

That file also predicted the strategy would be **genotype-specific**, and said *"nobody is
going to genotype-stratify a therapy for a disease with prevalence below 1 in 1,000,000."*
This document does exactly that stratification, for the first time as far as we can tell,
and the result is sharper than we expected.

## Method

All *BUB1B* nonsense records were pulled from ClinVar via E-utilities (50 hits for
`BUB1B[gene] AND nonsense`), filtered to **single-nucleotide variants producing a
p.XxxNNNTer** with a GRCh38 position — **37 variants**, residues 34 to 978. Each was scored
with **TrunKitten** (see `NMD-PREDICTION-TRUNKITTEN.md` for the model, its validation at
12/12 class agreement and *r* = 0.966 against the authors' published TrunCat values, and
its limits).

Each was then placed in a band by **what the truncated product retains**, using this
repository's own documented motif coordinates rather than new ones: KARD/PP2A-B56 at
**669–674** (the last functional motif), residues **748–753** which contact the kinase
domain, and the pseudokinase domain from **766**.

## The result

| band | what it means | n | predicted to escape NMD | median P(escape) |
|---|---|---|---|---|
| 1 — truncates through the motifs (≤674) | loses KARD and everything after | **25** | 3 | 0.261 |
| 2 — the clean gap (675–747) | **retains every known functional motif** | **1** | 0 | **0.316** |
| 3 — kinase-contact zone (748–753) | removes residues contacting the kinase domain | **0** | — | — |
| 4 — pre-kinase (754–765) | after the contact zone, before the domain | **0** | — | — |
| 5 — within the pseudokinase domain (≥766) | partial domain | **11** | 1 | 0.300 |

**The single variant in band 2 is this proband's allele 1, p.Leu737Ter.** Of 37 reported
*BUB1B* nonsense variants, it is the only one that truncates after the last functional
motif and before the kinase domain begins.

ClinVar classifies it **Pathogenic/Likely pathogenic** — which independently confirms what
our files already recorded about allele 1.

## What this actually establishes

**The allele-1 rationale is close to unique among reported truncating alleles, and that
cuts both ways.** It explains why no one has pursued NMD inhibition in this disease — with
n = 1, there is no cohort to pursue it for. And it makes the reasoning specific to this
child rather than a general claim about MVA, which is a stronger and narrower statement
than the one we were making.

**The model reproduces a known rule we did not put into it.** The three earliest
truncations — residues 34, 57 and 67 — are the ones predicted to *escape* (P = 0.65, 0.66,
0.50), while the middle of the gene sits at 0.18–0.32. Start-proximal PTCs escaping NMD is
established biology, and nothing in our banding told the model about it. That it falls out
of the predictions is mild evidence the model is doing more than re-deriving the 50–55 nt
rule, which is the preprint's own central claim.

**Bands 3 and 4 are empty, so our sharpest open question cannot be answered from ClinVar.**
The 731X-versus-753X split that `NMD-FEASIBILITY.md` calls "the real gap" — a construct
truncated just before the kinase domain rescued fully, one sixteen codons later did not —
sits precisely in the 748–765 window, and **no reported *BUB1B* nonsense variant lands
there.** That crux remains a bench question, and now we can say why no amount of variant
curation will settle it.

## Limits, stated plainly

- **n = 1 in the band that matters.** Nothing statistical can be built on one variant. The
  finding is a structural observation about where reported variants fall, not an effect.
- **The two VUS split 1 escape / 1 NMD**, against 1 of 26 for Pathogenic. The direction is
  consistent with the preprint's claim that VUS escape NMD more often than pathogenic
  variants, but **n = 2 is not evidence** and is reported only so the comparison is not
  silently omitted.
- **These are predictions, not measurements**, with the model's ROC-AUC ≈ 0.78 applying to
  every row.
- **ClinVar classifications are not independent observations** — submitters share evidence
  and literature, so the classification axis is weaker than its counts suggest.
- **Band membership is a claim about retained sequence, not retained function.** A product
  that keeps every motif may still misfold; that is exactly the 731X/753X question above.
- Frameshift and splice alleles are **excluded** — the model is for PTC-producing SNVs —
  so this is not a complete picture of *BUB1B* truncating variation.
