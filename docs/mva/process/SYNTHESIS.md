# BubR1, N1002K, and what the computation actually supports

Read this first. The other documents in `docs/mva/` are a working record with
corrections layered in as they were found; this is the settled state.

## 1. The disease is mostly truncation

Of 69 pathogenic or likely-pathogenic BUB1B alleles, **55 truncate** — 30 nonsense,
25 frameshift — spread evenly along the protein, which is what nonsense-mediated decay
predicts. Only 13 are missense, and they do not spread: they concentrate where there is
a folded domain to break.

This frames the proband. Allele 1 (`L737Ter`) is the ordinary kind of MVA allele. Allele
2 (`N1002K`) is the rare kind, and it is the one everything here is about.

## 2. Missense variants come in two mechanism classes

The single most useful finding. Pathogenic missense alleles split by *where* they sit,
and stability prediction only applies to one half:

| class | example alleles | ΔΔG AUC | what is actually broken |
|---|---|---|---|
| **binding interface** — TPR, GLEBS | R36Q, T40M, K400E | **0.364** — worse than chance | the partner contact (KNL1, BUB3) |
| **folded core** — pseudokinase | R814H, L844F, I909T, L1012P | **0.952** | the fold itself |

**T40M is pathogenic and predicted *stabilising*** (+0.54). That is not a predictor
failure; it is a predictor answering a question nobody asked it. Interface variants
lose a contact, not a fold.

This reproduces **Suijkerbuijk 2010's two-class model** — *"those that impose specific
defects in checkpoint activity or microtubule attachment and those that lower BUBR1
protein abundance"* — from structure alone, where the original came from westerns.

**Pooling the two classes destroys the signal** (whole-protein ΔΔG AUC 0.714, *below*
burial's 0.760). Every earlier number that looked unstable was this mixture.

## 3. Inside the folding class, stability prediction is real — and not just burial

The serious objection was that ΔΔG predictors read solvent accessibility, so a ΔΔG
result might be a burial result wearing a costume. Burial alone does reach AUC 0.844.

Tested directly, comparing each pathogenic variant only against benign variants of
similar RSA, with the permutation null shuffling labels *within* matched sets:

| matching window | ±5% | ±10% | ±15% | ±20% |
|---|---|---|---|---|
| ProteinMPNN-ddG AUC | 0.879 | 0.889 | 0.920 | 0.917 |
| permutation p | 0.0052 | 0.0046 | 0.0008 | **0.0006** |

Stable at every window, and logistic regression gives ΔΔG a slope of **−2.53** against
burial's **−0.22**. ΔΔG adds genuinely. *(Two other predictors, EvoEF2 and ThermoMPNN,
agree on ranks at Spearman 0.88–0.91, and one of them is a force field rather than a
network, so the agreement is not shared training data.)*

## 4. What this says about N1002K

**It is a folding-class variant, and it is destabilising.** Three independent methods
place it 2nd, 3rd and 4th worst of the eleven corpus variants in its domain.

**The mechanism is positional, not chemical.** Lysine is the **10th worst of 19**
substitutions at 1002 — glycine, alanine, glutamate, serine, proline and threonine are
all worse. The site is the 21st most intolerant of 285. So "this position cannot take
substitution" is supported; "lysine's charge clashes" is not.

**Magnitude is method-dependent** — near-catastrophic on ProteinMPNN-ddG, moderate on
ThermoMPNN. *Destabilising* is supported; *severely destabilising* is not.

The neighbouring-residue puzzle resolves cleanly: **N1004 ranks 256th of 285** with a
mean ΔΔG of +0.08. Two adjacent residues at opposite ends of the tolerance distribution.

## 5. Thirty VUS worth testing

The same calibration ranks 203 pseudokinase-domain missense VUS, thresholded by
specificity against 25 known benign controls: **30 nominations at a 4% empirical
false-positive rate**. Hypothesis-generating, not clinical, and folding-mechanism only.

The top nominations follow **the same pattern as N1002K**: ordinary substitutions at
extraordinarily intolerant positions. `W978L` is the 8th worst of 19 at a position
ranked 3rd of 285; `N1002K` is the 10th worst of 19 at a position ranked 21st.

## 6. What is NOT supported

- **The N1002 packing shell is not a constrained module.** 5 of its 10 residues are
  above their burial-matched median and 5 below — chance. It contains both the most and
  least tolerant positions in the neighbourhood. "Packs against N1002" predicts nothing.
- **N1002K does not change the pocket landscape.** Benign controls reproduced the
  apparent effect exactly; it was structure preparation. Clean negative.
- **N1002's absence from all 1,629 catalogued variants is not evidence of constraint.**
  62 of 285 domain positions have no recorded variant; absence is ~22% likely by chance.
- **The cryptic ATP pocket's geometry is not reproducible.** Two sampling methods agree
  that the ATP site carries cryptic druggable volume; they disagree on where and how
  much. Quote the claim, not the numbers.
- **Nothing here measures BubR1 abundance in a cell.** It predicts folding
  thermodynamics, which is one contributor among several.

## 7. Standing weaknesses

- Five pathogenic anchors in the folding class. Everything rests on them.
- Positives are source-confounded: 4 of 6 asserted by UniProt alone, 0 of 28 negatives.
  Mitigated because four carry direct functional measurements, not annotations.
- Negatives are annotations, not measurements.
- All of it is computed on a **predicted** structure; no experimental structure covers
  N1002 at the resolution these methods assume.
- The non-coding half of the gene — 456 intronic and 15 splice ClinVar records, including
  four known MVA-causing splice alleles — is **completely unscored**.

## 8. Source quality, which turned out to matter

The EBI Proteins aggregate carries seven distinct defect classes, all found by audit and
all now handled once in `apps/api/scripts/mva/variants/bub1b.py`:

| defect | scale | consequence if trusted |
|---|---|---|
| consequence type says missense, allele is a stop codon | 6 records | inflates pathogenic missense from 13 to 19 |
| wildType contradicts the reference sequence | 41 records | nucleotide letters in the amino-acid field; put a phantom variant on a nomination list |
| cDNA coordinates filed as protein positions | 84 records | positions up to 3131 in a 1050-residue protein |

Plus, outside the aggregate: reciprocal notation across databases (four codons, double-counts
on naive merge), LitVar conflating lab constructs with patient alleles, and full-text mining
running ~78% false positives before filtering.

**No single source is complete and none fail the same way.** ClinVar direct holds records
the protein-level aggregate cannot represent; the aggregate holds UniProt assertions
ClinVar lacks. Reconcile, never pick one.
