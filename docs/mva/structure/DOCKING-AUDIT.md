# We tried to drug the pocket. The experiment was void, and here is why

Reproduce: `python3 apps/api/scripts/mva/neurosnap/dock_audit.py`

## The question

`STABILITY-AXIS.md` concluded N1002K is a folding-class variant, and two sampling
methods agree the BubR1 pseudokinase ATP site carries **cryptic druggable volume**.
If a small molecule could occupy that site, a pharmacological chaperone becomes a
structure-guided proposal rather than a mechanism-class analogy. So: dock a library
and see.

## The design, and the mistake inside it

Ten ligands, PubChem-resolved, AutoDock Vina with vinardo scoring, against
AlphaFold `AF-O60566-F1` **residues 766–1050** — the pseudokinase domain carved out
of the 1,050-residue chain. Vina takes no search box in the Neurosnap wrapper, so
the dock was **blind**: the ligand may land anywhere on the receptor.

That was chosen deliberately. A blind dock that converges on the ATP site without
being told it exists is independent corroboration from a method that is not a
pocket-finder. The library was built to make that test sharp — ATP itself as the
positive control, metformin as the negative, deucravacitinib because it binds the
TYK2 **pseudokinase** domain and is the closest clinical precedent there is.

**Zero of ten landed within 12 Å of the ATP site.** ATP itself finished 38 Å away.

A positive control that misses by 38 Å does not refute the target. It says the
instrument is not measuring what you think.

## Two artifacts, both diagnosable

**1. The truncation scar.** Carving a domain out of a longer chain exposes the face
that used to pack against the rest of the protein. That face is hydrophobic and
concave — precisely what a docking score rewards. Counting, for each pose, the
contacts within 6 Å that exist in full-length BubR1 and were deleted by the cut:

| ligand | score (kcal/mol) | d(ATP site) Å | deleted contacts | lining |
|---|---:|---:|---:|---|
| imatinib | **−8.80** | 18.2 | 30 | 828, 833, 826, 794 |
| crizotinib | −7.52 | 18.8 | 33 | 766, 826, 835, 828 |
| everolimus | −7.36 | 18.1 | 35 | 826, 835, 824, 766 |
| larotrectinib | −7.24 | 33.6 | 1 | 1036, 898, 1040, 897 |
| ruxolitinib | −7.18 | 18.3 | 42 | 826, 828, 833, 825 |
| deucravacitinib | −7.15 | 20.0 | 39 | 828, 833, 826, 830 |
| selumetinib | −6.20 | 23.5 | 0 | 1007, 1009, 949, 874 |
| tafamidis | −5.52 | 32.5 | 0 | 1004, 976, 1002, 977 |
| ATP | −5.17 | 38.0 | 0 | 989, 988, 1026, 1024 |
| metformin | −3.59 | 12.7 | 1 | 778, 779, 798, 777 |

Five structurally unrelated drugs converged on one site — residues **824–835** — and
every residue of it is occluded in full-length BubR1 by the linker at **737–764**,
209 deleted contacts across the site. It is not a binding site. It is the scar left
by our own construct, and it captured the entire top of the score distribution.

On surface that survives intact, **nothing scores better than −7.24**, and the best
of those (larotrectinib) is 33.6 Å from the ATP site on a different face.

**2. A rigid receptor cannot enter a cryptic pocket.** This is the deeper error.
Lacuna reports the ATP-site pocket's **apo volume as 0 Å³** — cryptic means closed in
the apo coordinates and open only under sampling. Vina holds the receptor rigid. The
experiment asked a rigid structure to admit a ligand into a pocket that, in that
structure, has no volume. It could not have succeeded.

*(ATP's own behaviour is the third tell: it finished on residues 1022–1026, adjacent
to the basic C-terminal helix, pI 10.30. A tetra-anion on a rigid surface finds the
positive patch. That is electrostatics, not recognition.)*

## Verdict

**The run is uninformative about the ATP site, not evidence against it.** We report it
because the shape of the failure is the useful part: a blind dock into a carved-out
domain scores its own truncation, and reporting the −8.80 imatinib pose as a hit —
which is what this run would have looked like without the occlusion check — would
have been a fabricated lead in a document about a real child.

Doing it properly needs one of: docking into an **open conformer** from the sampling
ensemble rather than the apo structure (the Neurosnap job does not expose the
ensemble, and probing for it returned nothing); an **induced-fit or flexible-receptor**
protocol; or **full-length or linker-extended receptor** so the 824–835 face is
covered as it is in vivo.

## What it changes upstream — which is the point

Nothing about the folding thesis, and one thing about the route to it.

The pocket-occupancy idea was the *structure-guided* version of the stabilisation
arm: find the site, dock the chaperone, show the pose. That version is not currently
executable with the tools available, and we should stop implying it is.

**The arm that survives does not need a pocket at all.** 4-PBA does not work by
occupying a site on BubR1 — it raises folding capacity and quality-control throughput
in *trans*, and it never touches the target. That is why `STABILISATION-STRATEGY.md`
ranks it on mechanism match and paediatric safety rather than on affinity, and why a
failed docking campaign leaves it exactly where it was. Tafamidis is the cautionary
half of the same coin: it is in this library as a **concept control, not a candidate**,
and its pose near 976–1004 — three of the six lining residues are in N1002's own
packing shell — is a −5.52 score from one ligand on a rigid structure. `SYNTHESIS.md`
already records that shell as unconstrained. It is a coincidence, and we are naming it
here so that nobody later mistakes it for a finding.

## Credit where the design was right

The occlusion test is the only reason this is a documented artifact rather than a
reported lead. The general lesson is cheap to reuse: **when you dock into a construct,
first ask what the construct deleted.**
