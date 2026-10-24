# BubR1 is a waveform, not a level — and that is a harder problem than the one the field has solved

*Prompted by the right question: if BubR1 oscillates across the cell cycle, what does that
do to every therapy we have proposed, and how have other n-of-1 programmes handled
proteins that must stay in a window?*

*According to PubMed for the literature.*

## The constraint

BubR1 is not a protein whose level you set. It is a protein whose level **oscillates by
design**: low in G1, rising through S and G2, peaking at prometaphase when the spindle
checkpoint is active, and then **actively destroyed** so that anaphase can begin. Its
destruction is not incidental — it is the signal. APC/C–Cdc20 degrades BubR1, and the K250
acetylation switch gates that degradation, with turnover starting *before* anaphase onset
(Choi 2009, [10.1038/emboj.2009.123](https://doi.org/10.1038/emboj.2009.123)).

The same paper supplies the warning: the acetyl-mimetic K250Q, which resists degradation,
**markedly delayed chromosome segregation**. Too much BubR1 at the wrong moment does not
simply waste drug — it stalls mitosis in a cell that is already mis-segregating.

So this genotype has **two** deficits, and we had only been treating one:

- **amplitude** — the peak is too low, because one allele is dead and the other reduced
- **shape** — whatever we add must still fall away at anaphase

Everything we have proposed addresses amplitude. Only some of it preserves shape.

## How the field solved the adjacent problem

Dosage-sensitive genes where overshoot is harmful are not new, and the two best-developed
answers are worth copying exactly as far as they go.

**1 · Act on the endogenous transcript, and inherit its regulation for free.** This is the
approved version. Nusinersen corrects *SMN2* splicing rather than delivering SMN protein;
risdiplam does the same orally. The protein that results is made by the patient's own
gene, under the patient's own control (Hill & Meisler, Dev Neurosci 2021,
[10.1159/000517686](https://doi.org/10.1159/000517686)). Nothing has to be engineered to
reproduce the regulation, because the regulation was never removed.

**2 · Build a limiter into the vector.** Where protein must be supplied exogenously, the
MECP2 field engineered feedback. **miRARE** is a panel of miRNA binding sites placed in the
AAV genome, derived from miRNAs that rose after an in vivo overdose; adding it to
AAV9/miniMECP2 improved safety in wild-type mice while preserving efficacy in knockouts
(Brain 2021, [10.1093/brain/awab182](https://doi.org/10.1093/brain/awab182)), and a
human-ready construct followed. A related design, EXACT, puts a miRNA circuit inside a
single promoter-driven construct. The miRARE authors proposed the element could serve
other dose-sensitive genes.

The honest reading of that second line, which reviews of the field make themselves:
**miRARE does not restore natural regulation. It is a limiter on excessive accumulation.**

## Why that is not enough for BubR1

This is the distinction that matters, and it is the reason this gene is a harder case than
the canonical example:

> **MeCP2's constraint is a ceiling. BubR1's constraint is a waveform.**

A limiter solves a ceiling. It cannot solve a waveform. A construct could sit safely under
a cap at every moment and still be wrong, because the failure mode is **being present in
the trough** — occupying the phase where BubR1 must be absent for anaphase to proceed.
Flat-but-capped expression fills exactly the valley the cell uses as a signal.

So an exogenous BubR1 source — a circRNA payload, an AAV transgene — would need to
reproduce an *oscillation*, not merely respect a limit. Nobody has built that, and it is
not what miRARE or EXACT do.

## What follows for our candidate list

The cell-cycle constraint sorts the candidates more sharply than anything else we have
applied, because it is binary: either the approach inherits the native waveform or it must
manufacture one.

| approach | amplitude | **shape** | why |
|---|---|---|---|
| trans-splicing of endogenous pre-mRNA | yes | **inherited** | the corrected mRNA is still the gene's own, transcribed on the gene's own schedule |
| trans-RNA on endogenous mRNA | yes | **inherited** | acts on a message that is itself cycle-regulated |
| CRISPRa at the native promoter | yes | **inherited** | amplifies the endogenous programme |
| NAD⁺ / degradation route | yes | **partly** | raises abundance by slowing turnover — and turnover *is* the clock, so this one needs watching |
| circRNA or AAV encoding BubR1 | yes | **must be engineered** | constitutive source, no native timing |

Three of the five get the waveform free. That is the same conclusion we reached from the
modality-layer argument, arrived at independently — and it is a stronger reason, because
amplitude is a dose-finding problem while shape is a mechanism problem.

**The one that deserves a second look is the NAD⁺/degradation route.** It raises BubR1 by
slowing its destruction, and destruction is precisely the timed event. Choi 2009 showed
what happens when you block it too well. That does not disqualify the route — a partial,
reversible, pharmacological slowing is not the same as an undegradable mutant — but it
means the readout for that arm cannot be abundance alone. **Mitotic timing has to be
measured alongside it**, which is a specific addition to experiment 2 and is now recorded
as such.

## What this adds to the pitch

A challenge we can state precisely and have not dodged, plus a reason our preferred
modality is preferred that is independent of how well it works:

> We are not trying to raise a number. We are trying to restore an oscillation whose
> **collapse** is as functional as its peak. That is why the therapy has to act on the
> patient's own transcript — not because endogenous regulation is elegant, but because
> reproducing this particular waveform from outside is an unsolved engineering problem,
> and the field's best answer for dose-sensitive genes is a ceiling, which this gene
> does not need.

**What would make us wrong.** If BubR1's checkpoint function tolerates a raised trough —
if what matters is only the peak, and residual protein at anaphase is cleared by other
means or simply outcompeted — then a constitutive source is back on the table and the
argument above is too strict. The measurement that settles it is mitotic timing under
sustained expression, which is exactly what Choi's K250Q result begins to answer and what
a dose-ranging version would finish.
