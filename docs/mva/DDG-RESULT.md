# ΔΔG predictions for N1002K, N1002R and N1002S

**The folding hypothesis now has quantitative, independent support for the first time.
N1002K is predicted to destabilise BubR1 by +1.51 kcal/mol — more than every ClinVar-benign
variant in the same domain, including one two residues away.**

*Tool: **ThermoMPNN**, a GNN trained by transfer learning for point-mutant stability, PNAS
2024 ([10.1073/pnas.2314853121](https://doi.org/10.1073/pnas.2314853121)), weights shipped
by its authors. Producer: `scripts/mva/ddg_analysis.py`. Structure: AlphaFold AF-O60566-F1.*

## Why a published tool and not another of mine

Twice in this project I built a detector, validated it on a single positive control, and it
confirmed whatever I pointed it at — the splice scan (**C46**, 56% sensitivity on a blind
panel) and the pocket scan (a 12,879 Å³ "pocket" that was the protein's surface). So this
uses a peer-reviewed tool with published benchmark performance, which is its authors' to
report, not ours to re-derive.

## Three checks before reading anything

**1 · Mapping.** The tool indexes from 0. The check is that its own wild-type letters match
ours at three positions we identified independently: **1002 = N**, **978 = W** (the
hydrogen-bond partner), **999 = R** (the like-charged neighbour). All three match; the
script exits if any does not.

**2 · Sign, determined rather than assumed.** Reading ΔΔG backwards would invert every
conclusion. Proline and glycine substitutions are near-universally destabilising,
conservative swaps near-neutral:

```
   to proline  +1.817     to glycine  +1.260     conservative I<->V, L<->M  +0.424
   => POSITIVE = DESTABILISING
```

**3 · Robustness to structural context** — the choice that broke the pocket scan. Run on
the isolated domain and on the full-length model:

```
   N1002K   domain +1.507   full-length +1.506   difference 0.001
   N1002R   domain +1.419   full-length +1.417   difference 0.001
   N1002S   domain +0.944   full-length +0.943   difference 0.001

   agreement across all 5,700 shared predictions:  Pearson 0.941, Spearman 0.950
```

## The control: what this protein actually tolerates

ClinVar gives only **one** likely-pathogenic missense in *BUB1B* — too few for a
pathogenic-versus-benign control. It gives 34 benign or likely-benign, **nine inside this
domain**, which answer a better question: *is N1002K an outlier against substitutions
humans carry without disease?*

| tolerated variant | ΔΔG |
|---|---|
| A784T | +0.260 |
| F977L | +0.179 |
| F822L | +0.155 |
| **N1004S** | **+0.138** ← two residues away |
| D818E | +0.124 |
| T859A | +0.081 |
| K1040R | +0.025 |
| T1042I | −0.447 |
| G1013R | −0.814 |
| **mean / max** | **−0.033 / +0.260** |

**N1002K = +1.507 — above all nine, z = +4.32.**

The single most informative comparison is **N1004S at +0.138**: the immediate neighbourhood
tolerates substitution perfectly well. Position 1002 does not, at eleven times the
predicted cost.

## The decomposition, which corroborates our structural work independently

| | ΔΔG | reading |
|---|---|---|
| **N1002S** | **+0.944** | cost of losing the asparagine, adding no charge and no bulk |
| **N1002K** | **+1.507** | +0.56 more for charge and bulk on top |
| **N1002R** | **+1.419** | same charge, slightly more bulk — indistinguishable from K |

That split lands exactly where our geometry said it would. We found that Asn1002 donates an
**acceptor** contact through OD1 to the backbone nitrogen of Trp978 at 2.83 Å, and that
**no substitution can replace an acceptor with a donor**. So a cost is paid for losing the
asparagine whatever replaces it (+0.94, visible in serine), and burying a charge with no
counter-charge nearby costs more on top (+0.56).

Two methods that share no assumptions — hand geometry on one side, a GNN trained on
megascale stability data on the other — produce the same decomposition.

## What the experiment now tests

**N1002K (+1.507) and N1002R (+1.419) differ by 0.088 kcal/mol.** The folding model says
arginine should be as destabilising as lysine.

So the N1002R lane is no longer an open-ended look. It is a **test of a stated quantitative
prediction**:

- **both unstable** → consistent with folding, as predicted
- **K unstable, R stable** → **contradicts this prediction** and points to ubiquitination at
  the new lysine, which arginine cannot accept

## What this does and does not establish

**Does:** gives hypothesis A its first quantitative support from outside our own reasoning,
and sharpens the discriminating experiment into a falsification test.

**Does not:**
- **ΔΔG is thermodynamic; abundance is not.** A destabilised protein is degraded only if
  quality control recognises it. Destabilisation is necessary for the folding hypothesis,
  not sufficient.
- **It does not exclude hypothesis B.** A protein can be both destabilised *and* carry a
  new ubiquitin acceptor. These are not mutually exclusive.
- **It says nothing about hypothesis C** (lost PLK1 phosphorylation at T1008).
- **+1.51 kcal/mol is moderate**, not a fold-breaker. Consistent with reduced steady-state
  abundance; not with a protein that cannot fold.
- ThermoMPNN was benchmarked on **experimental** structures. Ours is predicted — locally
  high-confidence (pLDDT 91.5 over 990–1015) but predicted. And nine controls is a small set.

## Consequence for the recommendation

The candidates split by mechanism: **NAD⁺ targets degradation; arimoclomol and 4-PBA target
folding.** This result supports the **folding** side — which, on its own, moves arimoclomol
up relative to NAD⁺.

It does not settle it. A chaperone helps a protein that misfolds; this says the protein is
predicted to be less stable, which is evidence for that and not proof of it. The bench
result still decides, and now it decides against a number we have written down in advance.
