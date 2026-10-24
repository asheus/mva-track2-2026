# I ran the pocket scan. It confirmed my hypothesis, and the confirmation was an artifact.

**Verdict: the pseudokinase-pocket chaperone idea is neither supported nor killed. It is
untestable with the structures and tools available, and the kill criterion I published
cannot be evaluated.**

*Producer: `scripts/mva/pocket_scan.py`. Structure: AlphaFold AF-O60566-F1. PDB coverage
from UniProt O60566 and RCSB, retrieved 21 Oct 2026.*

## What I claimed I would do

In `APPROACH-RANKING.md` I proposed a pharmacological chaperone against BubR1's
pseudokinase domain — the literal migalastat mechanism — and published the kill criterion
before running anything:

> A pocket with no enclosed volume, or one that does not contact the 1002 neighbourhood,
> kills it.

## What happened first

LIGSITE-style buriedness detection on the domain (766–1050), with UniProt's annotated
binding sites (772–780, 795) as a positive control the method had to find unaided.

```
 rank  volume A^3   lining residues
    1       12879   [766, 767, 768, ...]   <= CONTROL   <= REACHES 1002
    2           7   [896, 897, 898, 899, 900, 1032]
    3           2   [928, 933, 934, 937]
```

Control passed. Pocket reaches 1002. **The idea survived its kill criterion** — and that
result was wrong.

## How it was wrong

A druggable enclosed pocket is typically **200–800 Å³**. Rank 1 was **12,879 Å³**, and the
distribution was pathological: one enormous blob and then nothing above 7 Å³. Its lining
residues ran consecutively from 766 — that is a *surface*, not a cavity.

**The control had passed vacuously.** A blob covering the whole domain necessarily touches
the annotated binding site and residue 1002 and every other residue. A control that a
degenerate result also passes is not a control.

The cause was occlusion: scanning the domain in isolation left its interface with the rest
of the 1,050-residue protein open to vacuum, so that entire face read as enclosed.

## What happened after the fix

Occupancy rebuilt from the **whole chain**, plus an explicit gate flagging any pocket
larger than 3,000 Å³ or lining more than 40% of the domain as a surface artifact:

```
  PSP>=5 : rank 1 = 16,420 A^3, lines 116% of the domain -> ARTIFACT
  PSP>=7 : rank 1 =  7,367 A^3, lines 104% of the domain -> ARTIFACT
  (>100% because whole-chain occupancy lets non-domain residues line it)

  With artifacts excluded, at every threshold tested:
  CONTROL: FAIL -- no pocket at the annotated binding site.
  THE TEST: not reportable.
```

The blob survives maximum strictness because the AlphaFold model of full-length BubR1 is
largely extended — **whole-protein mean pLDDT 63.6** — so the detector is measuring the
concavity of a sprawling, partly disordered model rather than finding ligand pockets.

## Why I did not just use a better tool

**No validated detector is available here.** fpocket is not installed and not installable
in this environment, and hand-rolling a replacement is exactly what produced the artifact
above.

**And no adequate structure exists.** Every experimental structure of BubR1 covers the
wrong part of the protein or is too coarse:

| PDB | method | resolution | residues |
|---|---|---|---|
| 2WVI, 3SI5 | X-ray | 1.8–2.2 Å | 57–220 (TPR) |
| 5JJA | X-ray | 2.35 Å | 647–720 |
| 5K6S, 5SWF | X-ray | 2.8 Å | 663–681 (KARD) |
| 5LCW | EM | 4.0 Å | 1–560 |
| **5KHU, 6TLJ** | **EM** | **3.8–4.8 Å** | **1–1050** |

The only structures covering the pseudokinase domain are **cryo-EM at 3.8–4.8 Å** — too
coarse for side-chain placement or cavity geometry.

**That absence is itself worth stating: nobody has solved BubR1's pseudokinase domain at
high resolution.** It is part of why this domain is underexplored as a target, and it is a
real obstacle for anyone pursuing the chaperone idea — not a gap in our effort.

## Where this leaves the idea, and the ranking

**Unchanged in rank, downgraded in status.** It was ranked 4th, below trans-splicing, the
NAD⁺ route and trans-RNA. It stays there, but its kill criterion is now marked
**not evaluable** rather than passed. The honest line in the ranking is "needs a structure
that does not exist," which is a harder obstacle than the one I wrote down.

Two things would change that: a validated pocket tool run on the AlphaFold model with
parameters chosen by someone who uses them routinely, or a high-resolution structure of
766–1050. The second is the real blocker and is nobody's weekend project.

## The pattern this is the third instance of

- **C46** — a splice detector validated on one positive control; 56% sensitivity on a blind
  panel, and its verdict on *BUB1B* flipped with a filter parameter.
- **Here** — a pocket detector validated on one positive control; the control passed
  vacuously and the result confirmed the hypothesis that motivated building it.

The common failure is not carelessness, it is that **a hand-rolled detector checked against
a single positive control will confirm whatever it is pointed at.** A control earns its
name only if a degenerate or null result would fail it. Both instruments now carry their
measured behaviour in the file; this one carries a refusal.

What saved it both times was the same cheap habit: **look at whether the number is
physically plausible before believing what it supports.** 12,879 Å³ is not a pocket, and
that was visible in one line of output.
