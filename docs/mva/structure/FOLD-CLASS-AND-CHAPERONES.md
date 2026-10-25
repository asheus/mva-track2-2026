# Is it really just misfolding? What else has this fold? And is there a cure for any of them?


> **SUPERSEDED IN PART, 14 Oct 2026.** This file ranks 4-PBA first, partly on its
> HDAC activity. That leg is **retracted**: HDAC inhibition induces premature sister
> chromatid separation and strips BubR1 from kinetochores, and MVA1's other name is
> premature chromatid separation syndrome. Arimoclomol (FDA-approved Sep 2024,
> children ≥ 2) carries the matched mechanism without it and is now the lead; 4-PBA
> is kept as a stated alternative with the hazard attached. See
> `CORRECTIONS-2026-10-06.md`, C5 and C7, and `TRACK2-REPORT.md` §3.3. The fold-class
> reasoning below is unaffected — only the ranking inside the chaperone class moved.

Three questions from the owner. The second one turned out to be the productive one, because
it leads somewhere the rest of this workstream had not looked.

---

## 1. Do I really think N1002K is just not folding properly?

**~90%.** That is a small move *down* from the 92% carried previously, and the reason is
worth stating: the calibration work showed AlphaMissense's 0.923 is **not independent
evidence**. It tracks burial at −0.663, and we computed the burial ourselves — so it was
partly the same fact counted twice. Removing that double-count costs a couple of points.

What the estimate now rests on, in order of weight:

1. **The chemistry of the specific substitution.** A long positive charge plus +54 Å³ of
   bulk driven into a 14%-accessible pocket lined by W973, F977, W978. This is the
   canonical destabilising substitution and it is measured from structure, not predicted.
2. **The two-class literature.** Suijkerbuijk: MVA missense alleles in or near the kinase
   domain lower BubR1 abundance; the destabilised set is HSP90-dependent and
   proteasome-rescuable.
3. **L1012P as mechanistic precedent** — a different chemistry reaching the same outcome
   by the same route, measured at 5–10× reduced.
4. GPN-Star placing it in the destabilised band, weakly.

**What would refute it:** N1002K protein present at normal abundance but non-functional —
i.e. a Y155C-type separation-of-function allele. We cannot test that. It is the residual
10%, and it is not negligible: **Q921 is buried more deeply than N1002 (1.7%) and Q921H is
measured wild-type-like.** Burial is not destiny.

---

## 2. What else has this fold — and does that help?

BubR1's pseudokinase domain (766–1050) is a **protein kinase fold**, one of the best-studied
and most druggable folds in biology. Checking its catalytic machinery directly against the
sequence:

| motif | canonical | BubR1 | |
|---|---|---|---|
| β3 / VAIK | V-A-I-**K** | V793-I794-**K795** | **intact** |
| catalytic loop | **H-R-D** | H880-**G**881-D882 | degenerate (Arg→Gly) |
| Mg-binding | **D-F-G** | D911-F912-**S**913 | degenerate (Gly→Ser) |

That is the textbook pseudokinase signature: **keep the nucleotide pocket, lose the
catalysis.** And it is not an inference — it was measured:

> "BubR1kinase and Bub1kinase bound to mant-ATP with **similar dissociation constants**,
> strongly suggesting that BubR1kinase **has not lost its ability to bind ATP**"
> — Breit et al. 2015, PMC4675524

**BubR1 has a real, occupiable nucleotide pocket** with affinity comparable to a genuine
kinase, even though it cannot catalyse. Three further observations make this interesting
rather than merely tidy:

- **Breaking the pocket destabilises the protein.** The same paper reports that the
  ATP-site lysine mutant **K795R gave "dramatically reduced yields"**, which they attribute
  to "pervasive effects on kinase stability that transcend their potential deleterious
  effects on enzymatic activity." Pocket integrity contributes to BubR1 stability.
- **One of the measured MVA destabilisers lines that pocket.** Our own calculation puts
  **I909 among the residues within 12 Å of K795** — and **I909T** is one of Suijkerbuijk's
  5–10×-reduced alleles. The pocket-stability link shows up in patient alleles.
- **Small molecules demonstrably move BubR1's stability in living cells.** ChEMBL carries
  CETSA (cellular thermal shift) data against BUB1B from a 2025 oncology programme
  (*Eur J Med Chem*, doi 10.1016/j.ejmech.2025.117247): fold-changes of **2.19** and 1.33
  in BubR1 surviving a thermal challenge at 20 µM, alongside 0.65 and 0.29 in the other
  direction. Under the standard CETSA convention, >1 is ligand-induced **stabilisation**.

**The comparison class**, then, is other pseudokinases — JAK2 JH2, TYK2 JH2, MLKL, ILK,
VRK3, ROR1, SgK223 — and the relevant precedent is that **their degenerate pockets are
druggable**. The clinching example is **deucravacitinib (Sotyktu)**, FDA-approved in 2022,
which works by binding the **TYK2 pseudokinase domain**. A pseudokinase domain is not a
dead end for medicinal chemistry.

### Where N1002 sits relative to that pocket

Measured on the AlphaFold model: **N1002 is 28.6 Å from K795**, and 14.7 Å from the nearest
pocket-lining residue. **It is not in the pocket.** A nucleotide-site ligand would not
contact the mutation directly; it would have to work by stabilising the *whole domain's*
folded state.

That is a real limitation, but it is not disqualifying — it is exactly how the approved
drugs in this class work. Tafamidis does not touch the mutated residue in TTR; it stabilises
the fold globally.

---

## 3. Are there cures for misfolded proteins?

**Yes — this is a mature, FDA-approved drug class.** Five approved examples, all working by
stabilising a protein that would otherwise misfold and be degraded:

| drug | disease | protein | how |
|---|---|---|---|
| **Tafamidis** | ATTR amyloidosis | transthyretin | binds the natural ligand pocket, stabilises the fold |
| **Migalastat** | Fabry disease | α-galactosidase A | **active-site** pharmacological chaperone |
| **Sapropterin** | phenylketonuria | phenylalanine hydroxylase | cofactor-analogue chaperone; **paediatric** |
| **Elexacaftor/tezacaftor/ivacaftor** | cystic fibrosis | CFTR F508del | correctors; now licensed **from age 2** |
| **Deucravacitinib** | psoriasis | TYK2 **pseudokinase** domain | allosteric pocket binder |

**Migalastat is the closest analogue to our situation and the most instructive**, because it
comes with a hard lesson. It works **only for "amenable" mutations** — roughly a third of
Fabry variants — and the FDA required an *in vitro amenability assay*, mutation by mutation,
to decide who gets it. Chaperone rescue is **allele-specific and cannot be predicted from
structure alone.** That is precisely the test we cannot run for N1002K.

---

## The conclusion, and the tension in it

**The scientifically correct answer to this child's allele 2 is a small molecule that binds
the BubR1 pseudokinase pocket and stabilises the fold.** Every element of that argument now
has evidence behind it: the pocket exists and binds nucleotide, breaking it destabilises the
protein, a patient allele sits in it, cellular thermal stabilisation of BubR1 has been
demonstrated, the fold class is druggable, the drug class is approved five times over.

**It does not exist, and nothing in this analysis brings it into existence.** Building a
BubR1 pharmacological chaperone is a multi-year discovery programme. It is not available to
a baby now, and no amount of mechanistic elegance changes that.

So the two tracks stay separate and should not be confused:

- **For this child, now:** 4-PBA / chaperone induction remains the lead — generic rather
  than targeted, but approved, paediatric, and mechanism-adjacent. Unchanged by today.
- **For the field:** a BubR1 pocket binder is the right target, and this is the most
  publishable thing in the workstream. It is a proposal, not a treatment.

### A safety inversion worth recording

**Every existing chemical programme against BubR1 is trying to inhibit or destabilise it**,
because BUB1B is an oncology target — the 2025 paper above is titled *"BUB1B inhibitors for
the treatment of clear cell renal cell carcinoma."* Two of its four compounds cut BubR1
thermal stability to 0.29 and 0.65.

For a child who already has **~17% BubR1** and a **cancer-predisposition syndrome**, a BubR1
inhibitor would be actively dangerous. The chemical matter that exists points the wrong way,
and any future screen of these libraries must be explicitly inverted — selecting for
stabilisation, with destabilisers treated as a hazard. **Logged as a standing refusal,
alongside the HSP90-inhibitor refusal.**

## Provenance

- ATP binding: Breit et al. 2015, PMC4675524 (mant-ATP titration, Fig 1C).
- Motif degeneracy: computed directly from `ENSP00000287598`.
- N1002↔K795 distance and pocket lining: AlphaFold `AF-O60566-F1`, `neighbourhood_structure.py`.
- CETSA data: ChEMBL target CHEMBL4295998, document CHEMBL6121040.
- **No high-resolution structure of the BubR1 pseudokinase domain exists.** PDBe returns 12
  structures for O60566; the pseudokinase domain appears only in 3.8–4.8 Å cryo-EM MCC
  models (6tlj, 5khu). Every structural statement here rests on the AlphaFold model, which
  is high-confidence in this region (pLDDT 91) but is a model.
- The 2.19× CETSA compound (CHEMBL1995703) is a **research compound, not an approved drug** —
  a 2,4-dianilinopyrimidine of the fedratinib chemotype but **not fedratinib** (N-methyl-
  piperazine in place of the pyrrolidinylethoxy group; InChIKey JVDOKQYTTYUYDV). Checked
  explicitly, because the scaffold is suggestive enough to be misread.
