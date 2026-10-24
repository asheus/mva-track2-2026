# "If L1012 isn't exposed, how is it so deleterious?"

The question assumes buried means protected. For protein structure it is the **other way
round**: buried residues are the ones you cannot touch. This is the single idea that
explains both L1012P and our own N1002K, so it is worth doing properly rather than
asserting.

## Why burial makes a substitution worse, not safer

**1. The core is full.** Protein interiors are packed at roughly the density of a solid —
there is no slack. A larger side chain has nowhere to go and forces the surrounding
structure apart; a smaller one leaves a cavity that collapses. On the surface, a residue
sticks into water, and water rearranges around anything.

**2. The core is greasy.** Buried positions are surrounded by hydrophobic side chains.
Putting a **charged** residue there means stripping away its shell of water molecules and
burying the charge with nothing to stabilise it. Energetically this is one of the most
expensive things a single substitution can do.

**3. Buried residues are load-bearing.** A surface residue holds up only itself. A core
residue is a contact point for a dozen others; disturbing it propagates.

The consequence is not that the protein works badly. It is that **the protein does not
fold properly, and the cell destroys it** — which is precisely the low-abundance
(Suijkerbuijk class 2) mechanism this whole case turns on.

## The proof, in this protein

Measured across all 285 residues of the pseudokinase domain — burial by Shrake–Rupley on
AlphaFold, impact averaged over every possible substitution at each position:

| burial band | n | mean AlphaMissense | mean GPN-Star LLR |
|---|---|---|---|
| **core (0–5%)** | 95 | **0.640** | **−5.270** |
| buried (5–20%) | 69 | 0.437 | −4.906 |
| partial (20–40%) | 56 | 0.314 | −4.562 |
| **exposed (>40%)** | 65 | **0.291** | **−4.493** |

(AlphaMissense higher = worse; GPN-Star more negative = more constrained. Both worsen
monotonically with burial.)

Spearman correlation of RSA against mean impact: **−0.663** for AlphaMissense, **+0.243**
for GPN-Star. Both point the same way. Buried residues are, on average, more than twice as
damaging to substitute as exposed ones.

## L1012P: two hits at once

**RSA 0.3% — the most buried residue in the neighbourhood.** And the substitution is to
**proline**, which is the worst possible choice for a second reason: proline cannot donate
a backbone hydrogen bond and it kinks the main chain. L1012 sits inside the helix
1008–1017. Proline **breaks helices**.

So L1012P simultaneously (a) breaks a helix and (b) does it at the most deeply buried
position around. Being buried is not in tension with being deleterious — it is *why* it is
deleterious. The measured result is the expected one: **protein reduced 5–10×.**

## N1002K: the same mechanism, a different chemistry

**RSA 14.0%, buried**, wedged against an aromatic cluster:

    N1002 contacts: W973, F977, W978, V998, R999, I1000, N1004

The substitution puts a **lysine** there — long, flexible, and **positively charged** —
in place of a small polar asparagine packed against three aromatic rings. That is
mechanism 2 above in its purest form: burying a charge in a greasy pocket, with added
bulk (+54 Å³) in a space that has none to give.

**This is why L1012P is the right comparator**, and the reason is worth stating precisely.
The chemistry is not similar at all — one is a helix-breaking proline, the other a buried
charge. What is shared is the **route**: disrupt a buried position → the domain cannot
fold → quality control degrades it → low abundance. L1012P is the measured end of that
route at 5–10× reduced. N1002K enters it by a different door.

That is a structural argument for the dosage hypothesis, independent of any predictor.

## One nuance this analysis forces, and it cuts against us

AlphaMissense tracks burial strongly (**−0.663**). Our two variants of interest are buried.
So AlphaMissense scoring them high (N1002K 0.923, L1012P 0.872) is **largely restating the
burial we computed ourselves** — it is correlated with our structural analysis, not
independent confirmation of it.

And burial alone does not discriminate. **Q921 is buried at 1.7%**, more deeply than
N1002, and **Q921H is measured indistinguishable from wild-type**. **I909 is buried at
3.4%** and I909T *is* destabilising. Same burial band, opposite outcomes. Burial says a
position is *capable* of mattering; it does not say a given substitution there *does*
matter. What separates N1002K from Q921H is the nature of the substitution — a buried
charge plus bulk, versus a conservative glutamine-to-histidine swap of similar size and
polarity.

So the argument stands on structure, but it stands on **burial plus the chemistry of the
specific change**, not burial alone.

## An anomaly, flagged not explained

**L1012 is the most buried residue in the region (0.3%) and GPN-Star's mean score there is
−0.94 — the *least* constrained of any residue we examined**, against −6.68 for N1002 and
−6.55 for I909. A deeply buried, helix-internal, experimentally-validated position reads
as evolutionarily free. That is GPN-Star's single worst failure in this gene and we have
no account of it. Recorded as a known defect of the instrument rather than glossed.

## Numbers settled

Solvent accessibility was taken to convergence: varying the spatial context from 15 Å to
30 Å changes nothing, and sphere density converges by ~960 points.

| residue | RSA | earlier figure in this repo |
|---|---|---|
| N1002 | **14.0%** | 12.9% |
| T1008 | **5.5%** | 4.7% |
| L1012 | **0.3%** | 0.2% |

The gaps are under 1.5 points and come from a different max-ASA reference table. Every
document in this set now carries the converged values. The error that actually mattered
was the sequence-window truncation corrected in the previous commit, which had put L1012
at 54% — exposed — and would have inverted this entire argument.

Reproduce with `python3 apps/api/scripts/mva/burial_vs_constraint.py`.
