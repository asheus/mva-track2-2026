# Running the Millet protocol on BubR1

Millet et al. rescued uroporphyrinogen III synthase in congenital erythropoietic
porphyria by docking an **allosteric surface site**, screening ~2,500 fragments
against it, validating hits by thermal shift and NMR, then searching approved drugs
for compounds resembling the best fragments — which returned **ciclopirox**, an
approved antifungal, that stabilised the enzyme in cells.

`DOCKING-AUDIT.md` diagnosed why our first structural attempt failed. This is the
same question asked with a protocol built around those failures.

| our failure, diagnosed | what this protocol does instead |
|---|---|
| blind dock — no box, so the greasiest patch wins | **a box** on one chosen site, and four decoy boxes |
| the site was **cryptic** (apo volume 0 Å³), unreachable by a rigid receptor | the site must be **open in apo**, and is picked on that |
| five drugs scored the **truncation scar** | every lining residue checked for contacts the cut deleted |
| whole drugs, dominated by size and greasiness | **rule-of-three fragments**, and scores taken as differences |
| no control — a raw score was read as a result | a **null built from the decoys themselves** |

## Step 1 — the site

Two independent detectors, chosen to disagree.

**Lacuna** (the cryptic-pocket sampler used previously) returns **nothing usable**, and
the reason is worth stating. Its one open, persistent, cross-method-reproducible pocket
(nma 2 / omm 3, lining-set Jaccard 0.80) is lined by **His880 and Phe912** — the HGD
histidine and the DFS phenylalanine, the degraded catalytic spine. Its other
high-druggability open pockets are lined by **Leu1031 and Leu1035**, the CENP-E
interface. **An inhibitor is not a chaperone**: the ATP pocket is intact in this child
and must stay that way, and CENP-E binding is a function we have no business blocking.
Both excluded.

Functional-site membership is tested by **lining-residue overlap**, not centroid
distance — a pocket *is* the ATP site if ATP-site residues line it. Cross-method
agreement is tested the same way, because `SYNTHESIS.md` records that the two backends
agree on *which* site carries cryptic volume and disagree on where its centroid is.

**LIGSITE** (Hendlich 1997; protein-solvent-protein counting on the static structure)
is the second instrument, and it is the right one here: Lacuna ranks by *cryptic*
character, which is precisely the wrong bias when a rigid dock needs a pocket that is
already open. It finds three pockets over 40 Å³. Two are the ATP site and the CENP-E
groove. **One passes.**

### The selected site

**134 Å³, centred (−41.85, −9.14, 4.71), lined by residues 814–820, 864–875, 891–893,
902–905.**

| test | result |
|---|---|
| open in apo | 134 Å³ (LIGSITE); 108 Å³ in both Lacuna backends |
| intact in full-length BubR1 | **0** contacts deleted by the truncation |
| ATP-site residues in lining | **none**; 20.4 Å from the ATP-site centre |
| CENP-E residues in lining | **none** |
| found by other instruments | Lacuna nma 3 (Jaccard 0.41), omm 7 (0.33) |
| surface groove, not buried cavity | median lining RSA **20.4%** (range 3–83%) |

**Native-state selective.** The walls come from **four separate sequence segments**;
59% of lining-residue pairs are >30 apart in sequence, median separation 37. The site
is a tertiary feature — it does not exist in an unfolded chain — so a ligand that binds
it binds the folded state only. That is the thermodynamic condition for the equilibrium
to shift toward folded.

**Proximity to N1002 is deliberately not a criterion.** Ligand binding to the native
state shifts folding by RT·ln(1+[L]/Kd) wherever it binds; tafamidis binds the
transthyretin tetramer interface, not the mutations it rescues. The distance (24.7 Å)
is recorded, not selected on. The assumption this carries is **cooperative unfolding** —
if the domain melted in independent subdomains, only the one containing the site would
be stabilised.

**Arg814 lines this pocket, and R814H is a known pathogenic folding-class allele** in
our corpus — a residue whose substitution destabilises the fold helps form the site.
The honest other half: **Asp818 also lines it and D818E is benign.**

## Step 2 — pipeline validation

Vina now runs **locally**, so there is a search box — the hosted service had none, which
is what made the first campaign blind.

**The positive control the blind run failed now passes.** ATP docked into a box on its
own site scores **−5.97** with the pose contacting **Phe912 and Ser913**. Blind, the
same ligand scored −5.17 and finished **38 Å away**. The earlier failure was the
method, not the protein.

## Step 3 — the fragment library, and one inversion of Millet

Millet screened diverse commercial fragments and then searched approved drugs for
lookalikes. **We built the library by fragmenting the approved drugs themselves**
(BRICS decomposition of the 646 Gate-1 medicines with a resolvable structure, filtered
on Astex's rule of three): **757 unique fragments**, each carrying its parent drugs.

The inversion matters for a child. Millet's step 4 is a similarity search that can land
on nothing approved; fragmenting approved drugs makes the mapping **exact** and
guarantees every hit has a parent that already cleared this project's own safety gate.

*The cost, stated: this library inherits medicinal chemistry's historical bias toward
scaffolds that hit common target classes, and it is 757 fragments against Millet's
2,500. A novel allosteric groove may simply not be represented.*

## Step 4 — the screen, and why differences rather than scores

Every fragment is docked at the target **and at four decoy boxes**, and what is ranked
is the difference. The decoys are the protein's other real pockets, which makes the
test hard on purpose — the question is not "does this stick to BubR1" but "does it
prefer **this** box":

| decoy | why |
|---|---|
| ATP site | a genuine functional pocket — the hardest decoy |
| truncation scar | the known artifactual attractor from the failed campaign |
| C-terminal groove | real, functionally uninteresting |
| exposed surface | no pocket at all — the floor |

For each fragment, **δ = score(box) − mean(score at the other four)**, which cancels
that fragment's intrinsic greasiness. The **null is the decoys' own δ values**, each
decoy treated in turn as if it were the target: that is what "prefers this box" looks
like at a box nobody cares about. A hit must be an outlier against that null, and the
empirical false-positive rate is read straight off it.

---

# Results

## First: is the instrument trustworthy?

The receptor PDBQT is written by hand in `prep_receptor.py` — atom typing and charges I
wrote myself. A systematically mistyped receptor would be wrong at **every box equally**,
so no amount of decoy control would reveal it. Two checks, both prerequisites for
reading anything below.

**Re-docking crystal complexes** (`validate_docking.py`): strip the ligand, rebuild the
receptor through *our* prep, dock the ligand back from SMILES with a fresh conformer,
measure symmetry-corrected RMSD.

| case | heavy atoms | score | RMSD | |
|---|---:|---:|---:|---|
| 3PTB trypsin + benzamidine | 9 | −6.08 | **0.14 Å** | PASS |
| 1STP streptavidin + biotin | 16 | −6.33 | **0.71 Å** | PASS |
| 2HYY ABL kinase + imatinib | 37 | −11.48 | **1.03 Å** | PASS |
| 1M17 EGFR kinase + erlotinib | 29 | −6.98 | 2.61 Å | marginal |

**3 of 4 inside the conventional 2.0 Å**, in the normal published range for Vina, and the
two hardest and most relevant — a large flexible kinase inhibitor in an ATP site, and a
deeply buried ligand — both under 1.1 Å. *This validates the machinery, not the BubR1
model; a predicted structure can still be wrong about its own pockets.*

**Seed reproducibility** (`seed_variance.py`): re-docking library fragments under five
RNG seeds gives a median within-fragment SD of **0.012 kcal/mol**. The differences the
screen reads are ~60× that. The hit list is not the random number generator.

*(RCSB is refused by this environment's network policy — the proxy answers 403 to CONNECT
for `data.rcsb.org`. Structures and ligand definitions come from PDBe, which serves the
same wwPDB content and is permitted.)*

## The screen: 757 fragments × 5 boxes

### Site test — the allosteric groove is the second-worst box on the protein

| box | median | q1 | q9 | best |
|---|---:|---:|---:|---:|
| ATP site | **−4.88** | −5.73 | −4.16 | −6.89 |
| truncation scar | −4.84 | −5.74 | −3.63 | −6.83 |
| C-terminal groove | −4.79 | −5.80 | −3.85 | **−7.93** |
| **allosteric (target)** | **−4.13** | −4.88 | −3.40 | −6.45 |
| flat surface, no pocket | −3.98 | −4.68 | −3.18 | −5.54 |

**It ranks 4th of 5, 0.15 kcal/mol above a patch of flat protein with no pocket at all**,
and ~0.7 below all three real pockets.

The per-fragment view is starker. Counting which box wins for each fragment (chance
would be 20% each):

| box | fragments won | |
|---|---:|---:|
| ATP site | 364 | 48.1% |
| truncation scar | 229 | 30.3% |
| C-terminal groove | 164 | 21.7% |
| **allosteric** | **0** | **0.0%** |
| flat surface | 0 | 0.0% |

**The target site is the best box for zero of 757 fragments** — identical to the
no-pocket control. It beats that control 77% of the time, by a median of 0.20 kcal/mol.
Marginally better than flat protein, never better than a real pocket.

### Fragment test — nothing survives the null

δ = score(box) − mean(the other four), so each fragment's intrinsic greasiness cancels.
The null is the decoys' own δ, each decoy treated in turn as the target.

```
null (decoy deltas, n=3028):  median -0.23   1st percentile -1.17   best -1.93
allosteric deltas (n=757):    median +0.46   1st percentile -0.23   best -0.43
```

The single best fragment at the target scores **δ = −0.43, empirical FPR 0.34** — a third
of decoy deltas are at least that extreme, and it does not approach the null's 1st
percentile. **0 of 757 clear a 1% false-positive rate.** Step 4 therefore writes an empty
hit list: there is nothing to map to approved drugs, and mapping the best
non-significant fragment anyway would manufacture a lead out of a negative result.

*(The obvious objection — that a decoy's "other four" contains the weak target while the
target's does not, rigging its own null — was checked, not assumed. With M the mean of
all five boxes, s − mean(others) = 1.25·(s − M) for every box, verified to four decimals.
Pure rescaling; ranking and FPR are identical either way.)*

## What this means

**The site is geometrically real and not ligandable.** Three independent detectors find
it, it is intact in full-length BubR1, no functional residue lines it, and it is built
from four distant sequence segments so a ligand for it would genuinely be native-state
selective. It is also **shallow** — median lining RSA 20.4%, LIGSITE mean PSP 5.55, just
over threshold — and a shallow groove does not enclose a fragment well enough to generate
binding energy. Geometrically real ≠ druggable.

Combined with step 1, where every *good* pocket was excluded for lining either the
catalytic spine or the CENP-E interface, the conclusion is:

> **The BubR1 pseudokinase domain has no ligandable allosteric site that is not already a
> functional site.** Its only good pockets are the ATP site and the CENP-E interface, and
> a chaperone must not block either.

This is a much stronger statement than the first docking campaign produced. That one was
**void** — blind, rigid, and scoring its own truncation scar (`DOCKING-AUDIT.md`). This
one is a **measurement**, on a validated instrument, with controls that behaved exactly
as predicted: the scar scored near the top, as the earlier audit said it would.

## What it does not touch

- **4-PBA and the chaperone arm never needed a pocket.** They raise folding capacity in
  *trans* and never bind BubR1. `STABILISATION-STRATEGY.md` ranks that arm on mechanism
  match and paediatric safety, not affinity, and this result leaves it where it was.
- **The aneuploidy → HSF1/HSP90 finding is untouched** (`BINDING-AND-STABILISING.md`),
  and it is the argument that makes the chaperone arm specific to MVA.
- **What dies is the structure-guided version of the thesis** — for the second time, but
  this time on evidence rather than on a broken experiment.
- **DUBTACs become relatively more attractive**, since they need only *a* binder rather
  than a fold-stabilising one — though this result says even that will be hard here.

## Honest limits of this negative

- **757 fragments, not Millet's 2,500**, and the library is benzene-heavy (226 of 757
  share a benzene scaffold) because it inherits medicinal chemistry's historical bias. A
  novel groove may simply not be represented.
- **Rigid receptor.** Vina does not let the pocket adapt. A site that opens under ligand
  pressure would be missed — which is exactly the failure mode that made the *first*
  campaign uninformative, and it applies here too, only less severely because this
  pocket is already open.
- **One predicted structure.** No experimental structure covers this domain at the
  resolution these methods assume.
- **Docking scores correlate with enclosure**, so a shallow site is penalised by the
  scoring function in a way that partly restates its geometry rather than independently
  testing it. The per-fragment win-rate (0/757) is the more robust statement.
