# Re-examining the closed routes for allele 2, against how other genes were rescued

14 Oct 2026. Prompted by a direct question: the agent rounds produced three ranked
routes for allele 2 (`BINDING-AND-STABILISING.md` §4) and we closed the first by
measurement. Were the others actually closed, and is there a route the field has used
on other genes that we never considered?

**Answer: one new route exists, with a fully worked published precedent using the same
tools we already have — and it is not executable on this protein. Establishing that is
the useful result, because it converts our fragment-screen negative from a statement
about one domain into a statement about the whole protein.**

Three of our own claims were also checked. One survives on better grounds than we
stated, one is an internal inconsistency, one is bounded.

---

## 1. The new route: block ubiquitination at the degron, not the fold

### The precedent, in full

Friedreich ataxia is structurally the same problem as ours: *"The amount of residual
frataxin critically affects the severity of the disease; thus, attempts to restore
physiological frataxin levels are considered therapeutically relevant"* [1] — swap
frataxin for BubR1 and that is our §3.2 argument verbatim.

Two routes were taken. The one usually cited is the **E3 ligase**: an siRNA screen
across 600+ E3 ligases identified RNF126 as the ligase that ubiquitinates frataxin, and
RNF126 depletion raises frataxin in patient-derived cells [1].

The second is more interesting for us, and we had not considered it. Rufini and
co-workers built **ubiquitin-competing molecules (UCM)** — small molecules that *"directly
bind to frataxin protein and inhibit its ubiquitination"* [2], promoting frataxin
accumulation and partially rescuing the aconitase defect in patient cells [3]. The
computational recipe is specified in full [2]:

1. NMR and X-ray structures used to locate putative pockets on the **solvent-accessible
   surface**;
2. **MetaPocket** consensus across eight detectors — ConCavity, Fpocket, GHECOM,
   **LIGSITE**, PASS, POCASA, Q-SiteFinder, SURFNET;
3. *"concentrating the analysis on the areas near to **Lys147**"* — the ubiquitination
   lysine;
4. virtual screening with **AutoDock and AutoDock Vina**, MW < 500, logP < 5;
5. ~5,000 molecules docked → ~100 purchased → fluorescence validation;
6. hits predicted to bind proximal to K147.

**We already have steps 1, 2 (LIGSITE is one of the eight) and 4 built and validated.**
The one decisive difference is step 3. Our site selection sought a *non-functional
allosteric pocket capable of stabilising the fold*; theirs sought *any ligandable patch
over the degron lysine*. The bar is lower — a UCM does not have to thermodynamically
stabilise anything, it only has to sit where ubiquitin would.

### Why it does not work here

BubR1's degron lysine is **K250**, where acetylation is protective and shields BubR1
from APC/C-mediated degradation (`STABILISATION-STRATEGY.md`); the second candidate is
K668. Neither was in our docked construct, because we built it from residues 766–1050.

So the obvious objection is that we looked for a drug where the *mutation* is rather
than where the *degradation* is. That objection is correct about our reasoning and wrong
about the conclusion. From the committed full-length AlphaFold model:

| region | mean pLDDT | |
|---|---:|---|
| K250 ± 10 (the degron) | **41.8** | very low — unmodelled |
| K250 itself | **47.5** | very low |
| K668 ± 10 (SIRT2 site) | **31.5** | very low |
| 766–1050 (what we docked) | **81.9** | confident |
| 1–250 (TPR + N-term) | 75.2 | confident |

K250's side-chain nitrogen has **10 protein atoms within 8 Å** — an exposed flexible
loop, not a pocket. Frataxin's K147 sits on the ordered surface of a small, fully folded
protein with both NMR and crystal structures. BubR1's degron lysines sit in its long
intrinsically disordered middle, which is what BubR1 *is* — a scaffold with
disordered linkers. **There is no structure to dock against, so the UCM recipe cannot be
run, and no amount of compute changes that.**

### What this buys, and it is not small

`MILLET-PROTOCOL.md` screened five boxes, all inside 766–1050, and reported that the one
non-functional pocket was the best box for **0 of 757 fragments**. Read strictly, that is
a statement about one domain. Our report has been using it as though it closed the
structure-guided route for the protein, which it did not establish.

It does now, by a different argument: **the pseudokinase domain is the only part of
BubR1 that current structure prediction models with any confidence, and within it every
good pocket is a functional site.** Everywhere else is disordered. So the negative
generalises — not because we screened the rest, but because the rest is not screenable.

That is a stronger and more honest claim than the one we were making, and it is reached
entirely computationally.

---

## 2. Our ATP-site exclusion: right answer, wrong reason

`select_site.py:26` and `MILLET-PROTOCOL.md` exclude the ATP site because *"the ATP
pocket is intact in this child and must stay that way"* and *"an inhibitor is not a
chaperone"*. That reasoning assumes catalysis worth protecting. It is **the one
druggable pocket on the domain** — the best box for 364 of 757 fragments (48.1%),
against 0 for the site we chose — so the exclusion deserves more than one line.

**The dominant view in the field does not support the stated reason.** Mammalian BubR1
is *"an untypical pseudo-kinase, which is thought to have maintained conserved residues
for a kinase domain throughout evolution **for structural reasons**"*, and *"**catalytic
activity of BubR1 is not required for any of its functions**, at least in mammalian
cells"* [4]. On that reading there is no catalysis to preserve, and a ligand occupying a
site conserved *for structural reasons* is a plausible fold stabiliser rather than an
inhibitor.

**But the opposing evidence is real and we should not repeat the citation asymmetry of
C15/C19.** Guo et al. found that CENP-E stimulates BubR1 autophosphorylation in vivo,
and cells expressing nonphosphorylatable BubR1 missegregate chromosomes, fail to
accumulate Mad1/Mad2 at unattached kinetochores, and form incorrect spindle attachments
[5]. The same source notes no cellular substrates have been identified and purified
BubR1 shows little activity in vitro except on itself [5] — so the pro-activity case is
autophosphorylation, not trans-substrate kinase activity.

**The two sides interlock, which is what settles it.** If BubR1's only functional
catalytic event is *CENP-E-stimulated* autophosphorylation, then the ATP site and the
CENP-E interface are one functional unit — and `MILLET-PROTOCOL` excluded both, for
cause. Our exclusion stands. It stands on the Guo evidence, not on the sentence we
wrote, and in a child whose syndrome is checkpoint failure the precautionary direction
is the same one.

Worth stating plainly: an ATP-site ligand for a pseudokinase would also face a severe
selectivity problem against the real kinome, in a cancer-predisposed child.

## 3. The "C-terminal groove" is mislabelled in our own decoy table

`MILLET-PROTOCOL.md` lists it as *"real, functionally uninteresting"* and uses it as a
decoy. It carries the **single best fragment score on the protein (−7.93)** and wins
164 of 757 fragments, so if it were genuinely non-functional it would be a better
candidate than the site we chose — "functionally uninteresting" is the *eligibility
criterion* for a pharmacological chaperone, not a disqualification.

It is not non-functional. Computed from the committed structure, the box centroid
`(-15.420, -2.660, -3.670)` is lined by residues **1041, 1046, 1047 and 1050** — inside
the 1031–1050 CENP-E interface the same document excludes as functional. The label is
wrong; the exclusion is right. It is also 34.3 Å from N1002, further than the ATP site.

A decoy described as non-functional while the document's own site-selection step
excludes it as functional is a contradiction that survived because nothing cross-checked
the two sections. No site was missed.

## 4. Route (b), brute-force repositioning, is bounded rather than open

`BINDING-AND-STABILISING.md` §4(b) cites ambroxol, found by screening 1,040 FDA-approved
compounds with no structural insight required, and we never ran it. It is now bounded:
on this protein the only druggable pocket is the ATP site (§2), so a blind approved-drug
screen either returns ATP-site binders — the functional site we just argued to leave
alone — or nothing. It is not a free option.

## 5. What the field says about the shape of our answer

Two findings support the mechanism-class argument rather than any specific molecule.

**Reduced protein abundance is the usual way missense variants cause rare disease**, and
variant-agnostic rescue is real: a single small-molecule stabiliser rescued surface
expression of **87% of destabilised variants** across a GPCR's mutational landscape [6].
That is the strongest available answer to "why propose a class rather than a molecule" —
one stabiliser can cover nearly a whole variant spectrum, which is exactly the regime an
n-of-1 patient needs.

And arimoclomol's precedent is broader than our C7 recorded: it rescues
glucocerebrosidase in Gaucher fibroblasts *"both in terms of quantity and in terms of
maturation"* and prevents aggregation of the rhodopsin P23H missense mutant [7].

---

## What changes

| | before | after |
|---|---|---|
| the 0/757 negative | a result about the selected site in one domain, used as if general | **general, and for a stated reason**: the pseudokinase domain is the only confidently modelled part of BubR1, and all its good pockets are functional |
| ATP-site exclusion | one line, on a premise the field contradicts | stands on Guo 2012; the ATP site and CENP-E interface are one functional unit |
| C-terminal groove | "real, functionally uninteresting" | mislabelled — it is the CENP-E interface; no site was missed |
| route (b) repositioning | untried and open | bounded: the only druggable pocket is one we exclude |
| route (e) UCM at the degron | not considered | **considered, precedent in hand, and not executable** — degron lysines at pLDDT 42 and 32 |
| why a class and not a molecule | asserted | supported: 87% variant-agnostic rescue precedent [6] |

**Nothing here changes the lead or the ranking.** The abundance-versus-function question
is untouched: every route above concerns *how* you would raise BubR1, and none of them
tells you whether raising it is the right thing to do. That still needs the measurement
named in §3.6 of the report.

---

REFERENCES

[1] Benini, M. et al. "E3 Ligase RNF126 Directly Ubiquitinates Frataxin, Promoting Its
    Degradation: Identification of a Potential Therapeutic Target for Friedreich
    Ataxia." *Cell Rep* (2017).
    https://citations.gxl.ai/papers/PMC5329121#L8,L14,L18
[2] Rezaei Makhouri, F. & Ghasemi, J.B. "In Silico Studies in Drug Research Against
    Neurodegenerative Diseases." (2018).
    https://citations.gxl.ai/papers/PMC6080098#L33
[3] Rufini, A. et al. "Highly specific ubiquitin-competing molecules effectively promote
    frataxin accumulation and partially rescue the aconitase defect in Friedreich ataxia
    cells." (2015). https://citations.gxl.ai/papers/PMC4358773#L22
[4] Marston, A.L. & Wassmann, K. "Multiple Duties for Spindle Assembly Checkpoint
    Kinases in Meiosis." *Front Cell Dev Biol* (2017).
    https://citations.gxl.ai/papers/PMC5733479#L71
[5] Short, B. "BubR1 shows self-control." *J Cell Biol* (2012), reporting Guo, Y. et al.
    doi:10.1083/jcb.201202152. https://citations.gxl.ai/papers/PMC3410415#L7-L8
[6] Mighell, T.L. & Lehner, B. "A small molecule stabilizer rescues the surface
    expression of nearly all missense variants in a GPCR." (2025).
    https://citations.gxl.ai/papers/PMC12700812#L12-L14
[7] Liguori, L. et al. "Pharmacological Chaperones: A Therapeutic Approach for Diseases
    Caused by Destabilizing Missense Mutations." *Int J Mol Sci* (2020).
    https://citations.gxl.ai/papers/PMC7014102#L56
