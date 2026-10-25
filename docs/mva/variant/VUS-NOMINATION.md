# Ranking BUB1B variants of uncertain significance

`ATLAS-AUDIT.md` found that relative solvent accessibility alone separated pathogenic
from benign missense at AUC 0.875 against ΔΔG's 0.963, and set a gate: **no VUS
nomination until ΔΔG is shown to add something beyond burial**, or we would be ranking
buried residues and calling it prediction.

This is that test, and then the nomination it licenses.

Reproduce with `burial_control.py` and `vus_nomination.py`.

## The burial test — and the thing it uncovered

Run on the **whole protein** (a new full-length saturation scan, 1,050 residues,
restricted to pLDDT ≥ 70), the pooled answer looked bad:

| | AUC |
|---|---|
| burial alone | 0.760 |
| ProteinMPNN-ddG | **0.714** — *worse than burial* |
| ThermoMPNN | 0.678 |

ΔΔG underperforming a single geometric number would have killed the whole idea. It was
pooling two populations that behave oppositely:

| mechanism class | n | ΔΔG AUC | burial AUC |
|---|---|---|---|
| **binding interface** — TPR (binds KNL1), GLEBS (binds BUB3) | 3P vs 11B | **0.364** — worse than chance | 0.682 |
| **folded core** — pseudokinase | 5P vs 25B | **0.952** | 0.844 |

**T40M is pathogenic and scores +0.54 — predicted *stabilising*.** So does R36Q at −0.83
and K400E at −0.50, both near zero. These are interface residues; their mechanism is lost
binding, not lost folding, and no stability predictor should be expected to see them.

This reproduces **Suijkerbuijk 2010's two-class model from structure alone** — *"all MVA
mutations fall in two distinct classes: those that impose specific defects in checkpoint
activity or microtubule attachment and those that lower BUBR1 protein abundance"* — which
was derived from westerns, not computation.

### Inside the folding class, ΔΔG passes cleanly

Burial-matched: each pathogenic variant is compared only against benign variants of
similar RSA, and the permutation null shuffles labels **within** each matched set, so
burial is held fixed by construction.

| | ±5% | ±10% | ±15% | ±20% |
|---|---|---|---|---|
| ProteinMPNN-ddG AUC | 0.879 | 0.889 | 0.920 | 0.917 |
| permutation p | 0.0052 | 0.0046 | 0.0008 | **0.0006** |
| ThermoMPNN AUC | 0.879 | 0.889 | 0.860 | 0.833 |
| permutation p | 0.0057 | 0.0042 | 0.0046 | 0.0094 |

**Stable across every matching window** — unlike the pooled version, which swung between
p = 0.0093 and p = 0.059 and should not have been trusted. Logistic regression puts the
ΔΔG slope at **−2.53** against RSA's **−0.22**: inside the folding class ΔΔG dominates
burial rather than echoing it.

**Gate passed, for the pseudokinase domain only.**

## The nomination

204 pseudokinase-domain missense VUS have a reliable structure. Thresholds are set by
**specificity against the 25 known benign variants in the same domain**, not by the
weakest pathogenic anchor — anchoring on the weakest (Q950E, asserted by Ensembl alone)
nominated 36% of all VUS, which cannot be right when most VUS are benign.

**HIGH confidence: both methods beyond the 4%-specificity cut — 30 of 203 VUS (15%),
empirical false-positive rate 1/25 = 4%.** Top of the list:

| variant | MPNN-ddG | ThermoMPNN | RSA% | why it is interesting |
|---|---|---|---|---|
| F912S | −7.11 | +2.14 | 1.9 | **the DFG→DFS motif phenylalanine** |
| V1038G | −7.01 | +2.07 | 1.2 | |
| **W978L** | **−6.93** | **+2.14** | 11.3 | position ranks **3rd of 285** in intolerance — see the correction below |
| W803R | −6.87 | +2.23 | 2.3 | codon already carries a pathogenic frameshift (`W803Hfs*10`) |
| F805S | −6.73 | +2.54 | 3.8 | |
| L936P | −6.40 | +2.38 | 2.5 | |
| L963P | −6.12 | +3.12 | 2.2 | |
| I956T | −6.11 | +2.13 | 0.0 | fully buried |

Full list in `data/variants/vus_nominations.json`.

### Correction: the packing-shell framing was wrong

This document first presented W978L as "an independent prediction from the same
structural argument" as N1002K, because W978 packs against N1002. **That claim does not
survive testing and is withdrawn.** `w978_shell.py` computed N1002's contact shell from
the structure (W973, F977, W978, F997, V998, R999, I1000, L1001, A1003, N1004) and
compared each member against burial-matched positions elsewhere in the domain:

**5 of 10 shell residues are above their burial-matched median, 5 below — exactly
chance.** The shell holds both the most intolerant positions (W978 at rank 3 of 285,
F997 at 11, L1001 at 12) and some of the most tolerant (F977 at 233, N1004 at 223,
V998 at 217). It is not a constrained module, and "packs against N1002" carries no
predictive weight on its own.

**W978 survives on its own merits, not the shell's.** It is more intolerant than
**100% of 21 burial-matched positions** and ranks 3rd of 285 in the domain — so it is
not explained by burial, at a moderate RSA of 11.3%. And W978L is a genuine ClinVar VUS,
which is what makes it actionable rather than merely interesting.

Two honest deflations go with it. W978L is the **8th worst of 19** substitutions at that
codon, so the leucine is not the problem — the position is. And W978 is **not even the
most intolerant tryptophan** in the domain; W993 (−6.94) and W803 (−6.68) score worse.

That pattern is the point, and it unifies the branch: **N1002K is the 10th worst of 19
at a position ranked 21 of 285; W978L is the 8th worst of 19 at a position ranked 3 of
285.** Both are ordinary substitutions at extraordinarily intolerant positions. The
signal is positional, not chemical, in both cases.

**F912S** hits the phenylalanine of the degraded DFG→DFS motif, which
`NEUROSNAP-TOOLBOX.md` separately identifies as lining the cryptic ATP pocket.

## What this is, and is not

- **Hypothesis-generating, not clinical.** No variant here has been reclassified. These
  are ranked candidates for functional testing, on one mechanism, in one domain.
- **Folding mechanism only.** A VUS that acts by losing a binding interface will not
  appear, and the interface result above shows those exist and score near zero or
  stabilising.
- **The 4% false-positive rate is measured against 25 benign controls**, so it is
  precise to about one variant. Do not read it as 4.0%.
- **Pseudokinase domain only.** The other 1,290-odd missense VUS in this gene are not
  addressed, and should not be scored this way.
- The positives remain source-confounded (4 of 6 UniProt-only, see `ATLAS-AUDIT.md`),
  mitigated by four carrying direct functional measurements.

## A seventh defect class in the aggregate

Building this caught something the earlier audits missed. **46 of 1,629 EBI records carry
a `wildType` that contradicts the reference sequence** — for example a `C→T` at position
863, where the residue is isoleucine.

The pattern names the cause: the bad values are `C`, `G`, `A`, `T` — **nucleotide letters
leaking into the amino-acid field**. It is invisible without a sequence check precisely
because C, G, A and T are all valid amino-acid codes too. One of these (`C863T`) reached
the nomination list before the filter was added.

`vus_nomination.py` now validates every `wildType` against the reference sequence and
drops the mismatches. Any future use of this aggregate should do the same.
