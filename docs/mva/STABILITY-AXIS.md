# The stability axis, measured at last

`PREDICTOR-CALIBRATION.md` established that the two predictors we had — AlphaMissense
and GPN-Star — carry no abundance axis, and that AlphaMissense scores *below chance*
on this gene's destabilisation axis. Every claim that N1002K is a folding defect
therefore rested on burial geometry and analogy, with no number behind it.

This closes that gap. Three independent stability predictors were run over the
BubR1 pseudokinase domain through Neurosnap, and scored against the corpus variants
whose protein levels were actually **measured** in the literature.

Reproduce with `apps/api/scripts/mva/neurosnap/stability_axis.py`; inputs are
committed under `docs/mva/data/neurosnap/`.

## What was run

The domain (766–1050, 285 residues, 2,343 heavy atoms) was carved from the AlphaFold
monomer model of O60566. Mean pLDDT 81.9, and **91.1 at N1002** — the neighbourhood
the argument depends on is well determined, not a floppy region.

| service | what it is | scope | job |
|---|---|---|---|
| ProteinMPNN-ddG | learned, unsupervised, inverse-folding | saturation: 285 × 19 | `6aa8bbe6bd4dd3655071b3ce` |
| ThermoMPNN | learned, supervised on megascale ΔΔG | saturation, cysteine off | `6aa8c0c3bd4dd3655071b3f3` |
| EvoEF2 | **physics force field**, not learned | the 11 corpus variants | `6aa8bbe6bd4dd3655071b3d0` |
| Lacuna | cryptic-pocket discovery, NMA sampling | wild-type domain | `6aa8bbb4bd4dd3655071b3cc` |

**Sign conventions were established empirically, not assumed — the three methods
disagree on direction and one of them backwards inverts the entire result.**
ProteinMPNN-ddG returns exactly `0.0000` for wild-type→wild-type at all 285
positions, which fixes it as a ΔΔG with negative = destabilising. ThermoMPNN is the
opposite: positive kcal/mol = destabilising. EvoEF2 reports mutant-minus-wild-type
total energy, so positive = destabilising. The script re-orients all three before use
and asserts the wild-type self-score is zero.

## The result

| variant | MPNN-ddG | ThermoMPNN | EvoEF2 | AlphaMissense | what is known |
|---|---|---|---|---|---|
| L1012P | −5.85 | 2.76 | 379.42 | 0.872 LPath | MEASURED 5–10× reduced |
| **N1002K** | **−5.47** | **1.29** | **15.72** | 0.923 LPath | *** PROBAND ALLELE 2 *** |
| L844F | −4.87 | 2.00 | 18.55 | 0.292 **LBen** | MEASURED 5–10× reduced |
| I909T | −4.83 | 2.13 | 5.20 | 0.451 **Amb** | MEASURED 5–10× reduced |
| R814H | −3.40 | 0.57 | 1.11 | 0.221 **LBen** | MEASURED 5–10× reduced |
| R893S | −1.47 | 0.55 | −2.76 | 0.579 | also in unaffected father |
| R999Q | −1.43 | 0.82 | 3.37 | 0.112 | neighbour |
| R770Q | −1.20 | 0.44 | 4.04 | 0.068 | architectural match |
| Q921H | −1.12 | 0.25 | −16.28 | 0.491 | MEASURED indistinguishable from WT |
| D1005E | −0.86 | 0.14 | −5.96 | 0.152 | neighbour |
| N1004S | −0.43 | 0.29 | −8.12 | 0.048 | neighbour |

The three methods agree on rank order at Spearman **0.882–0.909**, and one of them is
a physics force field rather than a neural network, so the agreement is not shared
training data.

## Calibration — stated honestly

| method | strict AUC | p | wide AUC | p |
|---|---|---|---|---|
| ProteinMPNN-ddG | 1.00 | 0.200 | 1.00 | **0.0079** |
| ThermoMPNN | 1.00 | 0.200 | 0.95 | **0.0159** |
| EvoEF2 | 1.00 | 0.200 | 0.95 | **0.0159** |
| AlphaMissense | **0.25** | 0.800 | 0.70 | 0.206 |

**"Strict" is four measured-reduced alleles against the single measured-normal one
(Q921H), and it is NOT significant.** Perfect separation with one negative control
happens by chance one time in five — p = 0.20 for all three methods. This is the same
error as the retracted "zero inversions" claim on the eIF3d branch and must not be
repeated. All three methods getting it is mildly reassuring, nothing more.

"Wide" adds the four inferred-benign variants as negatives and reaches p < 0.02 — but
four of those five negatives are **inferred** benign from predictor scores and
pedigree, not measured. The truth is between the two columns, and what the experiment
really needs is more measured negatives.

What does survive either way is the **head-to-head**. On the four alleles with
measured reduced protein, AlphaMissense returns 0.221 likely-benign, 0.292
likely-benign, 0.451 ambiguous, and only scores L1012P correctly — an AUC of 0.25,
below chance, exactly as `PREDICTOR-CALIBRATION.md` predicted. Three stability methods
do not do that.

## Where N1002K lands

- ProteinMPNN-ddG: −5.47, more destabilising than **90.6%** of all 5,415 substitutions
  in the domain; **2nd worst** of the 11 corpus variants.
- ThermoMPNN: +1.29 kcal/mol, more destabilising than **73.3%** of 5,139; **4th worst**.
- EvoEF2: +15.72; **3rd worst**.

(The denominators differ legitimately: ThermoMPNN was run with cysteine disabled, on
the service's own advice about disulfide artefacts, so its alphabet is 19 letters
without C.)

All three place it above every variant known or believed benign, and inside or
adjacent to the measured-reduced band. The magnitude is method-dependent —
ProteinMPNN-ddG calls it near-catastrophic, ThermoMPNN merely moderate — so
**"N1002K is destabilising" is supported; "N1002K is severely destabilising" is not.**

### It is the position, not the lysine

| position | mean ΔΔG over substitutions | rank of 285 |
|---|---|---|
| N1002 (proband) | −5.30 | **21st most intolerant** |
| L1012 (analogue) | −5.07 | 29th |
| Q921 (measured-normal) | −1.51 | 163rd |
| N1004 (benign neighbour) | **+0.08** | 256th |

Lysine ranks only **10th of 19** substitutions at 1002 — glycine, alanine, glutamate,
serine, proline and threonine are all worse there. So the mechanism is positional
fragility in a tightly packed site, not a specific clash contributed by lysine's
charge. That supports the packing account and rules out a charge-specific story.

It also settles the N1004S puzzle: two adjacent residues sit at opposite ends of the
tolerance distribution, 21st and 256th of 285.

### The consistent miss

All three methods rank **R814H** weakest of the four measured-reduced alleles
(50th percentile on ThermoMPNN, +1.11 on EvoEF2, essentially neutral). Either the
measurement is softer than reported, or R814H reduces protein by a route that is not
folding thermodynamics. Worth resolving before the calibration is leaned on hard.

### One force-field artefact, flagged

EvoEF2 returns **379.42** for L1012P against 5–18 for everything else. That is a
rigid-backbone proline clash the force field cannot relax, not a real energy. EvoEF2's
absolute values are not comparable across substitution types here; only its ranks were
used.

## The ATP pocket is cryptic

Lacuna returned 10 pockets on the wild-type domain. Two of them (ranks 5 and 8) line
**K795, the β3 VAIK lysine, and D911/F912/S913, the degraded DFG→DFS** — 7.0 Å and
6.9 Å from those residues. Pocket 8 is the notable one:

- **apo volume 0 Å³** — entirely closed in the static AlphaFold model
- opens to **401 Å³** under motion
- **crypticity 0.90**, the highest of all ten pockets
- druggability 0.80, peaking at 0.90

This is the structural precondition a pharmacological chaperone needs, and it explains
why static inspection concluded there was no pocket. It is consistent with Breit 2015
reporting that this pseudokinase binds ATP.

**The honest limit: no pocket lies on N1002 itself.** A ligand at the ATP site could
only act as a global thermodynamic stabiliser of the domain, never as a local patch on
the mutation. That is how tafamidis and migalastat work, so the analogy in
`FOLD-CLASS-AND-CHAPERONES.md` survives — but the distance belongs in the claim.

### Corrected by the MD run

The normal-mode screen completed in 5 seconds and is not evidence on its own. The
implicit-solvent MD backend (40 conformers) was run afterwards on the same wild-type
structure, and it **changes two of the statements above**:

- Normal modes put the nearest pocket **21.7 Å** from N1002, which this document
  originally reported as "most are 30–40 Å away". Under MD the nearest is **12.0 Å**
  (crypticity 0.89, druggability 0.81). Still a separate site, not a pocket on the
  residue — but the earlier distances were an artefact of thin sampling and should not
  be quoted.
- The *specific* numbers for the cryptic ATP pocket — 401 Å³, persistence 0.38 — are
  normal-mode-specific. MD finds no pocket at that exact centroid (nearest is 9.1 Å
  away, crypticity 0.67) but does find **two fully-closed, druggable pockets within
  5 Å of D911** (ranks 2 and 4: apo volume 0, opening to 691 Å³ and 320 Å³,
  crypticity 0.78 and 0.88).

So the qualitative claim survives two sampling methods — **the ATP site of this
pseudokinase carries cryptic, druggable volume that is shut in the static model** —
while the precise geometry does not. Quote the claim, not the numbers.

One deflation: **7 of 10 MD pockets have apo volume 0**, against 3 of 10 under normal
modes. "Fully closed in the static structure" is therefore much less remarkable under
richer sampling than it first appeared.

## The mutation does not change the pocket landscape

N1002K was run through Lacuna with settings matched to wild-type, against two benign
controls: **N1004S**, the adjacent residue and the 256th most tolerant of 285, and
**Q921H**, the one corpus allele with measured-normal protein.

| structure | crypticity | druggability | max volume | persistence |
|---|---|---|---|---|
| wild-type (raw AlphaFold) | 0.90 | 0.80 | 401 | 0.38 |
| **N1002K** | 0.90 | 0.80 | **573** | 0.29 |
| N1004S (benign) | 0.90 | 0.80 | **573** | 0.29 |
| Q921H (benign) | 0.90 | 0.80 | **573** | 0.24 |

Taken alone, N1002K looks like it opens the pocket from 401 Å³ to 573 Å³. **The
controls show it does not.** A harmless neighbour reproduces the proband's numbers
exactly. The shift is structure preparation — every mutant was rebuilt by EvoEF2 while
wild-type was the raw AlphaFold carve — and not the mutation.

**Result: null.** There is no detectable mutation-specific effect on the pocket
landscape, which is unsurprising when the site sits 30 Å away. Had the controls been
skipped, this would have been reported as a positive. Any future comparison must
prepare wild-type and mutant through the identical pipeline.

Reproduce with `apps/api/scripts/mva/neurosnap/pocket_controls.py`.

## Superseded in part by the atlas audit

`ATLAS-AUDIT.md` re-derived this document's central comparison against relative solvent
accessibility and found that **burial alone separates pathogenic from benign missense in
this domain at AUC 0.875**, against 0.963 for ProteinMPNN-ddG. ΔΔG predictors read burial.
So the sentence "three stability methods do not do that" remains true of AlphaMissense,
but must not be read as the predictors carrying the result — a solvent-accessibility
calculation carries most of it.

What survives untouched is the part built on measurement rather than annotation: four
alleles with **measured 5–10× reduced protein** versus one measured normal, and the
head-to-head where AlphaMissense returns two likely-benign and one ambiguous on those four.

## Standing limits

- One measured-normal allele. The strict calibration cannot reach significance with
  n = 1 on the negative side, whatever the AUC says.
- Four of five "wide" negatives are inferred, not measured — partly from the very
  predictors under test, which is circular and is why both columns are reported.
- All of this is computed on a **predicted** structure. No experimental structure
  covers N1002 at the resolution these methods assume.
- ΔΔG is interpretable only inside the folded domain, so the 26 corpus variants
  outside 766–1050 get no stability score and none should be invented for them.
- Nothing here measures BubR1 abundance in a cell. It predicts folding
  thermodynamics, which is one contributor among several.
