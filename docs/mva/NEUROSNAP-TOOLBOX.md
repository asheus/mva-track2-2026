# The Neurosnap toolbox, ranked against this hypothesis

157 services are available. This is not all of them — it is the ones that could change
what we believe about **N1002K destabilises the BubR1 pseudokinase domain, and a
cryptic ATP-site pocket might be drugged to stabilise it**.

Descriptions are quoted from the service catalogue. Already-run jobs are marked.

## What we have already established, and what is still soft

| claim | evidence | strength |
|---|---|---|
| N1002K is destabilising | 3 ΔΔG methods, Spearman 0.88–0.91 | **solid** |
| the stability axis calibrates on this gene | AUC 0.904, z +3.04 (6 vs 26) | **solid** |
| it is positional fragility, not lysine chemistry | K ranks 10/19 at the site | **solid** |
| the ATP site carries cryptic druggable volume | 2 sampling methods agree qualitatively | **moderate** — geometry not reproducible |
| N1002K changes the pocket landscape | controls killed it | **refuted** |
| a ligand there would stabilise the fold | — | **untested** |
| the protein is degraded rather than misfolded-and-retained | — | **untested** |

The three soft rows are what the tools below are for.

## Tier 1 — would directly move the hypothesis

**`Boltz-2 (AlphaFold3)`** — *"Open-source AlphaFold3-class model with built-in affinity
prediction."* The single highest-value untried job. Co-fold the domain **with ATP**,
wild-type versus N1002K. This tests Breit 2015's claim that this pseudokinase binds ATP
*and* whether the mutation degrades the site, in one experiment — and the affinity head
gives a number rather than a pocket geometry. Lacuna already exported Boltz pocket
constraints, so the binding site can be restrained rather than guessed.

**`OpenFE Absolute Binding Free Energy`** — *"Compute an OpenFE absolute binding free
energy from a positioned SDF ligand."* Alchemical free energy is the real answer to
"would a ligand bind that cryptic pocket", as opposed to a docking score. Expensive, and
only worth running once a ligand pose exists.

**`AlphaFlow`** — *"Generate protein structures that closely reflect experimental and
physiological conditions."* A third, independent conformational sampler. The cryptic
pocket currently rests on normal modes and one MD run that disagreed on geometry. A
method that is neither would settle whether the pocket is real.

**`Aggrescan3D`** — *"Structure-based aggregation profiling."* Tests a mechanism nothing
here has touched. If N1002K raises predicted aggregation, the cellular fate is
aggregation rather than proteasomal degradation — and that changes the therapeutic
target completely, because 4-PBA in `STABILISATION-STRATEGY.md` is a chemical chaperone
aimed at exactly that.

**`Pangolin RNA Splicing Prediction`** — *"Predict splice site strength and the impact
of genetic variants on RNA splicing in multiple tissues."* The atlas turned up
**four splice alleles** we have never scored: `c.2577+5G>A`, `c.1402-5A>G`,
`c.2386-11A>G`, `c.2009+1G>A`, plus the Alu insertion. These are real MVA alleles that
every missense predictor is blind to. Cheap, and it widens the corpus.

## Tier 2 — would strengthen what we have

**`StaB-ddG`**, **`Protein Fold Stability Prediction`** (ESM-IF), **`ProSST`**,
**`SaProt`**, **`ESMC Mutation Scoring`** — four more orthogonal ΔΔG / mutation-effect
methods. With 6 pathogenic against 26 benign now in hand, each one is a cheap
independent replication of the AUC 0.904 result. `ProSST` and `SaProt` use structure
*and* sequence, so they are not simply more of the same.

**`GROMACS`** / **`OpenMM Molecular Dynamics`** + **`MDAnalysis Trajectory Analysis`** —
*"post-process trajectories into stability, flexibility, exposure, contact and
secondary-structure CSV outputs."* Run wild-type and N1002K to convergence and measure
whether the mutant actually unfolds locally. This is the direct test of the folding
claim, rather than a predictor's opinion of it. **Prepare both structures identically**
— the preparation artefact that killed the pocket comparison applies here too.

**`AF2Bind`** / **`ScanNet`** — independent binding-site predictors. If either
nominates the same ATP-site residues Lacuna found, the pocket stops depending on one
tool's ensemble.

**`TemStaPro`**, **`NetSolP-1.0`**, **`Prot2Prop`** — sequence-level thermostability and
solubility. Weak individually, but they need no structure, so they can score the
truncating and out-of-domain alleles that ΔΔG methods cannot reach.

## Tier 3 — only after a pocket is confirmed

`AutoDock Vina (smina)` (Lacuna already exported its search boxes) · `GNINA` ·
`DiffDock-L` · `DynamicBind` · `PocketFlow` and `GenMol` for generating ligands into the
pocket · `ChemBounce` · `Free Wilson Analysis` · `ADMET-AI` and `eTox` for filtering
anything generated · `gmx_MMPBSA` for endpoint energetics.

**Do not start here.** Docking into a pocket whose geometry two sampling methods
disagree about produces confident numbers about nothing.

## Not useful for this problem

The protein-design half of the catalogue — `NeuroBind`, `RFdiffusion`/`RFantibody`,
`BindCraft`, `BoltzGen`, `ProteinMPNN`/`LigandMPNN` — designs *new* binders. A
pharmacological chaperone for a paediatric patient needs an approved small molecule,
which is the funnel in `TRACK2-REPORT.md`, not a designed protein. `AllMetal3D`,
`Prodigy`, the antibody tools and the multi-omics tools do not apply.

## Already run

| service | job | outcome |
|---|---|---|
| ProteinMPNN-ddG | `6aa8bbe6bd4dd3655071b3ce` | saturation ΔΔG, 285 × 19 |
| ThermoMPNN | `6aa8c0c3bd4dd3655071b3f3` | saturation ΔΔG, cysteine off |
| EvoEF2 Mutant Stability | `6aa8bbe6bd4dd3655071b3d0` | physics ΔΔG + mutant structures |
| Lacuna (normal modes) | `6aa8bbb4bd4dd3655071b3cc` | 10 pockets, cryptic ATP site |
| Lacuna (openmm MD) | `6aa8c0c4bd4dd3655071b3f5` | corrected the geometry claims |
| Lacuna N1002K + 2 controls | `…b406`, `…b413`, `…b415` | **null** — controls killed it |

Total spend: well under one credit. Cost is not the constraint on what we run next;
experimental design is.

## The sequencing that follows from this

1. **Pangolin** on the four splice alleles — cheap, and they are currently invisible.
2. **Aggrescan3D** wild-type versus N1002K — cheap, and it discriminates two different
   therapeutic strategies.
3. **Boltz-2** with ATP, wild-type versus N1002K — the real test of the pocket.
4. The four extra ΔΔG methods as replication of AUC 0.904.
5. MD only if steps 2–3 still point at folding.
