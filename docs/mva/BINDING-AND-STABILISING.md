# Can we bind BubR1 and stop it being degraded?

Four questions, answered in the order they actually depend on each other. This
supersedes nothing in `STABILISATION-STRATEGY.md`; it supplies the mechanism that
document was missing, and it adds one finding that changes how the chaperone arm
should be argued.

---

## 1. "Are we sure N1002K doesn't fold?"

**We never claimed it doesn't fold, and the distinction is the whole ballgame.**

Our evidence says *destabilising* — and explicitly not *severely* destabilising
(magnitude is method-dependent; ProteinMPNN-ddG calls it near-catastrophic,
ThermoMPNN calls it moderate). A protein that cannot fold at all is **not** a
pharmacological-chaperone target. A protein that folds, works, but spends more time
in the unfolded or partially-folded state than it should — and is therefore culled —
is *exactly* the target class. The field's own definition:

> "This property can be beneficial for curing diseases that are associated with
> protein mutants that are **intrinsically active but unstable**. The total activity
> of the affected proteins in the cell is lower than normal **because they are
> cleared by the quality control system**." [1]

So "does it fold?" is the wrong binary. The right question is *what fraction is
folded at steady state, and what does quality control do with the rest* — and a
chaperone works by shifting that equilibrium, not by rescuing a hopeless sequence.
Our N1002K profile — destabilising, positional rather than chemical, moderate on at
least one method — is the amenable profile, not the hopeless one.

**Still unmeasured:** nobody has run a western blot on this child's BubR1. Predicted
folding thermodynamics is not abundance in a cell.

## 2. "Is the ATP pocket fine?" — yes, and that is the eligibility criterion

The field excludes candidates on exactly this basis:

> "Pharmacological chaperones are **of no use if the active site is affected**." [1]

Measured directly on the structure (`dock_audit.py` geometry, ATP-site centre from
K795 + D911 + F912 + S913):

| residue | distance to ATP-site centre |
|---|---:|
| **N1002 (proband)** | **26.7 Å** |
| W978 (top VUS nomination) | 28.5 Å |
| L1012 (known pathogenic) | 18.7 Å |
| K795 (VAIK lysine) | 2.4 Å |
| D911 (DFG→DFS) | 2.3 Å |

N1002's closest approach to the catalytic lysine is **28.6 Å**. The nucleotide pocket
is untouched.

**This inverts how we were reading that result.** An intact ATP pocket had been
filed as a disappointment — nothing there to fix. It is the opposite: an intact
pocket 27 Å from the lesion is the *precondition* for chaperone amenability. The
lesion is in the fold, not the site, which is the one configuration this class of
drug is built for.

And the same criterion **excludes allele 1 outright**: pharmacological chaperones are
"not useful in all the cases, e.g., in which the protein is absent because the gene is
affected by ... a stop gain mutation" [1]. `L737Ter` is a stop gain. Independent
confirmation, from the field's own eligibility rule, of what
`WHICH-ALLELE-TO-TARGET.md` reached by dosage arithmetic: **allele 2 or nothing.**

## 3. "Is it destroyed by the proteasome?"

For BubR1 itself, the evidence is Suijkerbuijk 2010 — mutant levels collapse under
HSP90 inhibition, and proteasome inhibition rescues. That is the basis of the whole
arm and it is second-hand in this document; it is cited from primary source in
`FOLD-CLASS-AND-CHAPERONES.md`.

**Independent support, from the sister gene.** In patients with biallelic *BUB1*
mutations, mRNA is normal but protein is severely reduced, and full-length protein
becomes detectable **on treatment with the proteasome inhibitor marizomib** [2].

**The caveat matters and we state it rather than let the parallel run:** that patient's
lesion is a **start-codon** mutation, so the mechanism is translation initiation, not
misfolding. What it establishes is that a SAC-complex protein at low abundance is
proteasome-cleared and pharmacologically recoverable. It does **not** establish that a
misfolding *BUB1B* missense mutant is cleared the same way. Right family, right
outcome, different lesion.

---

## 4. "Why can't we bind it and help it fold?" — three routes, ranked by how much pocket they need

### (a) Allosteric pharmacological chaperone — the ideal recipe, and we ran it: it failed

> **STATUS, added after this document was written: we executed the protocol below and
> it returned a clean negative** (`MILLET-PROTOCOL.md`). The BubR1 pseudokinase domain
> has no ligandable allosteric site that is not already a functional site. Route (a)
> is **closed**. It is kept here in full because the recipe is sound and the reason it
> failed is a property of this protein, not of the method — and because routes (b) and
> (c) below are read differently once (a) is known to be shut.

> "It has been proposed ... to look for **allosteric ligands** that stabilize missense
> unstable mutants but do not bind the active site and do not inhibit the activity.
> **These molecules would be the ideal pharmacological chaperones.**" [1]

The worked precedent is the most directly copyable thing found in this search.
For congenital erythropoietic porphyria, Millet and co-workers:

1. used **in silico docking to identify an allosteric site on the enzyme's surface**;
2. screened **2,500 chemical fragments** against it;
3. validated binding by **thermal shift assay and NMR**;
4. searched a library of **approved drugs** for compounds similar to the best fragments;
5. found **ciclopirox — an approved antifungal — stabilised the enzyme in cells** [1].

That is a complete path from a computed site to an approved molecule, and it is what
our docking campaign should have been. Note what it avoids: it targets a **surface**
site that is open in the apo structure (not a cryptic one), it validates by
**thermal shift** rather than by docking score, and it screens **fragments** rather
than whole drugs. Every one of those choices dodges a failure mode that
`DOCKING-AUDIT.md` diagnosed in our own run.

**What happened when we ran it.** Site selection excluded every good pocket for cause —
the only open, reproducible one is lined by His880 and Phe912 (the catalytic spine), the
rest by Leu1031/Leu1035 (the CENP-E interface). One groove survived: 134 Å³ at residues
814–820 / 864–875 / 891–905, intact in full-length, built from four distant sequence
segments and so genuinely native-state selective. Against 757 fragments it was the best
box for **zero** of them — identical to a flat-surface control — and **0 of 757 cleared
a 1% empirical false-positive rate**. The site is geometrically real and **shallow**
(median lining RSA 20.4%); a shallow groove does not enclose a fragment well enough to
generate binding energy. **Geometrically real ≠ druggable.**

### (b) Brute-force repositioning over approved molecules

**Ambroxol**, now a serious Gaucher candidate, was found by screening a library of
**1,040 FDA-approved compounds** [1]. No structural insight required. For a child,
screening within the approved set is also the right safety class to be searching in.

### (c) DUBTAC — the route that does not need a stabilising pocket at all

This is the creative answer to "how did people solve this," and it inverts the problem.

A PROTAC recruits an E3 ligase to *destroy* a protein. Nomura's team asked what the
mirror image would be: they found **EN523, which selectively binds the deubiquitinase
OTUB1**, linked it to lumacaftor (a CFTR ligand) to make **NJH-2-057**, and that
chimera **inhibits ΔF508-CFTR degradation and raises protein levels beyond what
lumacaftor achieves alone** in cystic fibrosis donor cells [3].

**Why this matters for us specifically.** A pharmacological chaperone must bind *and*
thermodynamically stabilise the fold — a hard, site-specific requirement, and the one
our structure work could not deliver. A DUBTAC only needs a ligand that **binds**;
the stabilisation comes from stripping the K48 degradation chain, not from the
ligand's effect on folding. **The bar drops from "find a fold-stabilising site" to
"find any binding site."**

And it goes further than small molecules. Wei's TF-DUBTAC platform used a
**DNA motif** as the targeting arm to stabilise FOXO3A, p53 and IRF3 [3] — so the
targeting ligand need not be a drug-like molecule at all. BubR1 has several
well-characterised interaction motifs (GLEBS→BUB3, TPR→KNL1, the LxxIxE at 668–675
→PP2A-B56, 1031–1050→CENP-E). A peptide-armed DUBTAC is a real, if distant, design.

**Honest status:** no DUBTAC is approved anywhere, none has been made against BubR1,
and this is a research direction for an n-of-1 child, not a proposal. It belongs in
this document because it is where the field is going and because it is the only route
that survives the absence of a druggable pocket.

---

## 5. The finding that changes the argument: aneuploidy breaks the chaperone system itself

This was not what the search was for, and it is the most consequential thing in it.

> Aneuploid human cells show **consistently lower HSF1 protein levels**, downregulation
> of **HSP90**, and "a profound defect in the ability to trigger the HSF1-dependent"
> heat-shock response. Overexpression of constitutively active HSF1 **rescued the
> protein-folding defect** of aneuploid cells [4].

And:

> Aneuploid human cells were "**significantly more sensitive to HSP90 inhibition** than
> cognate diploids" [4].

Three consequences, in order of importance:

**(i) There is a feed-forward loop, and the disease attacks its own rescue system.**
Destabilised BubR1 → weakened checkpoint → aneuploidy → **HSF1 and HSP90 down** →
less folding capacity → more BubR1 cleared. This child's cells are chronically
aneuploid by definition of the diagnosis, so the chaperone capacity that would
otherwise buffer a destabilised protein is itself depleted *by the phenotype the
destabilised protein causes*.

**(ii) It re-founds the chaperone arm on a better argument.**
`STABILISATION-STRATEGY.md` justified 4-PBA's HSP70-inducing arm as "raises
quality-control capacity" — a generic claim, true of any cell. The specific claim is
stronger: in an aneuploid cell that capacity is **measurably reduced**, so a
co-inducer is **restoring a depleted system rather than augmenting a normal one**.
That is a mechanism match to *this* disease, not a mechanism-class analogy, and it is
the first argument in this workstream that is specific to MVA rather than borrowed
from another protein.

**(iii) It confirms the HSP90-inhibitor refusal from a new direction.**
We refused HSP90 inhibitors because they would remove this child's entire supply of
destabilised BubR1. Independently: aneuploid cells are *already hypersensitive* to
HSP90 inhibition. The refusal now rests on two unrelated lines of evidence.

**What it does not settle — and this cuts both ways.** If folding capacity is
depleted, a capacity-restoring drug might deliver more than the generic 1.5–3×
chaperone range. Or a depleted system might be precisely why it would underdeliver.
**Both readings are available and we are not choosing between them.** It is a reason
to measure HSF1 and HSP90 in patient cells, not a reason to claim a bigger effect.

---

## What this changes in the deliverable

| | before | after |
|---|---|---|
| does N1002K fold? | treated as binary, unstated | wrong question; amenable profile is "folds but unstable" |
| intact ATP pocket | filed as a disappointment | **the eligibility criterion, and it passes at 26.7 Å** |
| allele 1 exclusion | dosage arithmetic | **also excluded by the field's own PC eligibility rule** |
| 4-PBA's HSP70 arm | generic "raises capacity" | **restores capacity the aneuploidy has depleted** |
| HSP90 refusal | one line of evidence | two, independent |
| binding a pocket | blocked by our failed dock | **measured shut: no ligandable non-functional site (0 of 757 fragments)** |
| the route that remains | pharmacological chaperone, if a site turns up | **proteostasis in *trans* (4-PBA); DUBTAC needs a binder, not a stabiliser — but this result says even a binder will be hard** |

--------
REFERENCES

[1] Liguori, L. et al. "Pharmacological Chaperones: A Therapeutic Approach for
    Diseases Caused by Destabilizing Missense Mutations." *Int. J. Mol. Sci.* 21,
    489 (2020). doi:10.3390/ijms21020489
    https://citations.gxl.ai/papers/PMC7014102#L10,L40,L50

[2] Carvalhal, S. et al. "Biallelic BUB1 mutations cause microcephaly, developmental
    delay, and variable effects on cohesion and chromosome segregation."
    *Sci. Adv.* 8, eabk0114 (2022). doi:10.1126/sciadv.abk0114
    https://citations.gxl.ai/papers/PMC8769543#L75

[3] Xie, X. et al. "Recent advances in targeting the 'undruggable' proteins: from drug
    discovery to clinical trials." *Signal Transduct. Target. Ther.* 8, 335 (2023).
    doi:10.1038/s41392-023-01589-z
    https://citations.gxl.ai/papers/PMC10480221#L499

[4] Donnelly, N. & Storchová, Z. "Aneuploidy and proteotoxic stress in cancer."
    *Mol. Cell. Oncol.* 2, e976491 (2015). doi:10.4161/23723556.2014.976491
    https://citations.gxl.ai/papers/PMC4904904#L11,L13-L14
