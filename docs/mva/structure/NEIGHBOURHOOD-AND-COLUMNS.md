# What the columns mean, and why N1002K and N1004S are nothing alike

Two questions from the owner on `VARIANT-TABLE.md`. The second one turned out to be the
better question.

## 1. The columns

**AlphaMissense** — one number per missense variant, 0 to 1, "how likely is this variant
to cause disease". Higher = worse. Google DeepMind, trained largely on the contrast
between variants common in humans and variants seen in other primates. `LBen` / `Amb` /
`LPath` are its own labels (likely benign / ambiguous / likely pathogenic). It scores
**missense only** — it cannot touch a nonsense, splice or intronic variant.

**m447, p243, v100** — these are all **GPN-Star**, the same model run over three
different evolutionary depths:

| column | alignment | reads |
|---|---|---|
| m447 | 447 mammals | constraint over mammalian evolution |
| p243 | 243 primates | recent constraint — our close relatives |
| v100 | 100 vertebrates | deep constraint, back to fish |

They can disagree, and where they do that is information: a position constrained in
vertebrates but not primates has been under ancient pressure that has since relaxed.

**The numbers in those columns are percentiles, not the model's raw score.** The raw
output is a log-likelihood ratio — how surprised the model is to see this base swapped —
which is meaningless on its own. So each variant is ranked against a comparison set:

- a **coding** variant against all 9,459 possible coding changes in BUB1B
- an **intronic** variant against all intronic changes in the gene

**Lower percentile = more constrained = model thinks it matters more.** So `14%` means
"more constrained than 86% of all possible coding changes in this gene". This is the
opposite direction from AlphaMissense, which is confusing, and worth keeping in mind:
**low GPN and high AlphaMissense both mean "bad".**

(The matched null matters. Scored against the whole gene — which is ~95% intron — every
coding variant looks exceptional and N1002K reads as 0.8th percentile instead of 14th.
That error is recorded in `PREDICTOR-CALIBRATION.md`.)

## 2. N1002K vs N1004S — two residues apart, opposite worlds

The observation is exactly right and it has a clean structural answer. From AlphaFold
`AF-O60566-F1`:

| res | aa | RSA | | pLDDT | contacts | AlphaMissense | GPN m/p/v |
|---|---|---|---|---|---|---|---|
| 996 | F | 1.3% | buried | 94.9 | 12 | | |
| 997 | F | 1.3% | buried | 93.9 | 14 | | |
| 998 | V | 24.2% | partial | 92.2 | 7 | | |
| 999 | R | 21.0% | partial | 93.8 | 10 | 0.112 | 40/55/47 |
| 1000 | I | 0.9% | buried | 93.8 | 10 | | |
| 1001 | L | 4.6% | buried | 91.6 | 10 | | |
| **1002** | **N** | **14.0%** | **BURIED** | 91.1 | 7 | **0.923** | **14/32/16** |
| 1003 | A | 3.6% | buried | 88.0 | 7 | | |
| **1004** | **N** | **51.9%** | **EXPOSED** | 80.4 | 4 | **0.048** | **99/97/99** |
| 1005 | D | 66.3% | exposed | 82.2 | 3 | 0.152 | 47/36/64 |
| 1006 | E | 41.7% | exposed | 87.8 | 5 | | |
| 1007 | A | 52.6% | exposed | 91.1 | 4 | | |
| 1008 | T | 5.5% | buried | 92.1 | 9 | — | — |
| 1011 | V | 0.3% | buried | 94.7 | 9 | | |
| 1012 | L | 0.3% | buried | 95.3 | 12 | 0.872 | 76/96/13 |

RSA = relative solvent accessibility: 0% = completely buried in the protein core, 100% =
fully exposed to water.

**N1002 is buried at 14% and packed against an aromatic cluster:**

    N1002 contacts: W973, F977, W978, V998, R999, I1000, N1004

**N1004 is on the surface at 52%, with four contacts and nothing aromatic:**

    N1004 contacts: S946, Q950, N1002, E1006

They are two residues apart in sequence and in completely different environments, because
they sit in a **loop** (1000–1006). A loop turns; consecutive side chains alternate
between pointing into the core and pointing at solvent. Sequence adjacency says nothing
about spatial position.

So:

- **N1002K** buries a **long, positively charged lysine** where a small polar asparagine
  was wedged against three aromatic rings. Burying a charge in a hydrophobic pocket is
  one of the most destabilising things a substitution can do, and lysine is much bulkier
  than asparagine besides. This is a textbook destabilising substitution.
- **N1004S** swaps one small polar residue for another, on the surface, pointing at
  water. Nothing is packed against it. There is very little for it to disrupt.

**On this pair, both predictors are exactly right** — AlphaMissense 0.923 vs 0.048,
GPN-Star 14% vs 99%. Worth saying plainly given how much of this file set is about where
they fail.

Note also **N1004 has the lowest pLDDT in the whole neighbourhood (80.4)**, with D1005 at
82.2. AlphaFold is itself least confident exactly where the chain is most exposed and
flexible — the confidence signal and the burial signal agree.

### The neighbours

- **R999** (21% RSA, partial) — AM 0.112 benign, GPN ~40–55%. Half-buried, and both
  predictors read it as tolerable. No reason from the structure to disagree.
- **D1005** (66% RSA, exposed) — AM 0.152, GPN 36–64%. Surface. D→E is a conservative
  swap of one acidic residue for a slightly longer one. Harmless-looking, and predicted
  harmless.
- **T1008** (5.5% RSA, buried) — the **Plk1 phosphosite**. Two things follow. First, it
  confirms the earlier finding by a second route: **T1008 does not appear in N1002's
  contact list**, consistent with the 11.6 Å separation measured before. N1002K does not
  reach the phosphosite, so the Plk1 arm is unaffected and the strategy does not change.
  Second, a *buried* phosphosite is itself interesting — Plk1 cannot reach a residue at
  6% exposure, so either this model is a closed conformation or the site needs local
  unfolding to be phosphorylated. Flagged, not resolved; it does not bear on this case.
- **L1012** (0.3% RSA, the most buried residue in the region) — L1012P is measured to
  reduce protein 5–10×, and proline in a helix is a classic helix-breaker. Structurally
  obvious. **GPN-Star still calls it 76% and 96% on two of three timescales.** The clearest
  single miss in the table, on the variant closest to our own.

## A correction made during this analysis

The first run of this used a **sequence window** (residues ±14) as the context for the
solvent-accessibility calculation. That silently drops packing partners that are far in
sequence but close in space — W973 for N1002, and the entire packing face of L1012 — and
it produced badly wrong numbers: L1012 at **54% (exposed)** when it is actually **0.3%
(the most buried residue in the region)**, and N1002 at 15.8% instead of 14.0%.

Rebuilt with a **spatial** context (every atom within 20 Å). The corrected figures agree
with those recorded earlier in this repo from an independent run.

The figures were then taken to **convergence** (`/tmp` run, method in
`burial_vs_constraint.py`): varying the spatial context from 15 Å to 30 Å changes nothing
at all, and sphere density converges by ~960 points. The settled values are **N1002 14.0%,
T1008 5.5%, L1012 0.3%**, and every document in this set has been updated to them. The
earlier figures (12.9 / 4.7 / 0.2) came from a different max-ASA reference table; the gap
is under one and a half points and no conclusion turned on it. The *truncation* bug was
the one that mattered, and it would have reversed the reading of L1012 entirely.

## Scorecard: does GPN-Star actually capture these alleles?

Counting only variants where something is actually known:

| | AlphaMissense | GPN-Star (m447) |
|---|---|---|
| measured destabilised (5) | **1 / 5** — misses R727C, R814H, L844F | **3 / 5** — misses L844F, L1012P |
| measured normal (3) | 2 / 3 — wrongly elevates Q921H | **3 / 3** |
| splice / intronic (4) | **cannot score any** | 3 scored, all strongly constrained |
| K250R (lethal in mouse) | **missed** (0.082) | **missed** (69%) |
| R770Q (causality disclaimed) | benign — consistent | benign — consistent |

**GPN-Star is the better instrument on this gene**, clearly: it gets every negative
control right, catches three of five destabilisers, and can score the splice variants
that AlphaMissense structurally cannot reach. AlphaMissense calls three proven MVA
patient alleles *likely benign*.

**Neither is reliable enough to decide anything on its own here**, and both share one
blind spot that matters for our strategy: **K250R is called benign by both, and it is
embryonic-lethal in the mouse.** Neither model can see a post-translational modification
site being deleted. Our acetylation arm lives entirely in that blind spot.

Reproduce with `python3 apps/api/scripts/mva/neighbourhood_structure.py`.
