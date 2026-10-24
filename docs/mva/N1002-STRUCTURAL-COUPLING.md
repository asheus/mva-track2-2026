# Is N1002 mechanically coupled to the Plk1 site or to the outer surface?

The worry was concrete: N1002K sits in a functionally busy neighbourhood — the pseudokinase
domain binds CENP-E, and T1008 is an annotated Plk1 phosphosite six residues away. If the
substitution propagates to either, N1002K is a *functional* mutant and the whole
allele-2 stabilisation strategy is aimed at the wrong mechanism.

Computed from AlphaFold `AF-O60566-F1` v6. Reproducible via
`apps/api/scripts/mva/n1002_structural_coupling.py`.

## A method note first

**AlphaFold is not a mutation-effect predictor.** It is driven largely by the multiple
sequence alignment, and a single substitution barely perturbs that, so folding the mutant
sequence would very likely return a near-identical structure — which would read as "no
effect" when it actually means "the method cannot see it". The informative analysis is of
the *wild-type* structure: what the residue does, and what it is mechanically coupled to.

## Result 1 — N1002 and L1012 are not structurally equivalent

They are ten residues apart in sequence and in **different structural elements**. N1002 sits
in the loop spanning ~1000–1006. T1008 is the first residue of the *next* helix (1008–1017),
which contains L1012.

| site | secondary structure | RSA | contacts T1008? |
|---|---|---:|---|
| **N1002 — proband** | **loop** | 14.0% | **no — 11.6 Å** |
| L1012P | helix | 0.3% | **YES — 4.5 Å** |
| I909T | loop | 3.6% | no — 13.1 Å |
| L844F | helix | 0.9% | no — 19.4 Å |
| **R814H** | **loop** | **16.4%** | no — 13.3 Å |
| R727C | helix | 6.2% | no — 18.2 Å |

**The closest structural analogue to N1002 is R814H, not L1012P** — same loop context, nearly
identical burial, same absence of contact with the Plk1 site.

That matters twice over, because **R814H is the missense in MVA-12C, the patient line
measured at 17%.** The structural analogue and the phenotypic comparator are the same
variant, arriving from independent directions.

## Result 2 — the Plk1 site concern belongs to L1012P, not to us

N1002 and T1008 share only the intervening backbone (1000, 1003, 1004) and are 11.6 Å apart
at the side chains. **L1012 packs directly against T1008** at 4.5 Å, i→i+4 within the same
helix.

So the one variant in the calibration set that would genuinely perturb the Plk1 site is
L1012P — and it is structurally unlike ours.

Two further reasons to down-weight T1008 generally:
- **T1008 has RSA 5.5% — it is buried.** A kinase cannot phosphorylate a buried threonine in
  this conformation, so the site either requires local unfolding to be presented or the model
  does not capture the phospho-competent state.
- The published annotation lists T1008's consequence as *"BubR1 kinase activity"* — inherited
  from the era when BubR1 was believed to be an active kinase. It is not. That annotation is
  probably a relic.

## Result 3 — N1002 is an internal staple, not an interface residue

Its side chain makes two backbone hydrogen bonds, tying the 978 segment to the 998 segment
(both confirmed as direct contacts at 3.5 Å and 4.4 Å). Its contact set — W973, F977, W978,
F997, V998, R999, L1001, A1003, N1004 — is a local cluster it holds together.

On propagation outward: 6 of its 23 neighbours within 8 Å are solvent-exposed above 40% RSA
(W973 42%, N1004 52%, S976 51%). So the packing it maintains does position some exposed
residues — but they are **scattered, not a contiguous interface patch**, and none is an
annotated functional site. That is the signature of a folding determinant, not a binding
residue.

## Verdict

Confidence that N1002K is a **pure dosage (stability) mutant** rather than a functional one
moves from ~75–80% to **~85%**:

1. Structurally it is a buried staple, not an interface residue.
2. Its two nearest structural analogues, R814H and I909T, are both pure destabilisers that
   do not touch the Plk1 site — and I909T is one of the two mutants where forced
   overexpression **fully restored function**, proving normal-but-scarce for this class.
3. The variant that does threaten the Plk1 site is structurally unlike ours.

**What holds it below 95%:** CENP-E binds the pseudokinase domain (residues 705–1050 are
sufficient) and that interface has never been mapped to residues. N1002 being 87% buried
makes it an unlikely contact, but "unlikely" is carrying real weight there.

---

# ADDENDUM — the CENP-E interface has been mapped, and N1002 is not on it

The caveat above ("CENP-E binds the pseudokinase domain and that interface has never been
mapped to residues") is now resolved. It **has** been mapped — by Legal et al. 2020, which
I had not found on the first pass.

## What they showed

- BubR1 **705–1050** binds the CENP-E kinetochore-targeting domain with **Kd = 318 ± 90 nM**,
  1:1 stoichiometry, no post-translational modification required.
- BubR1 **705–1030** — lacking only the last 20 residues — **does not bind at all.**
- So the interface is the **basic C-terminal helix, residues 1031–1050** (pI 10.30),
  which pairs with an acidic patch on CENP-E (E2313, E2316, E2318, E2319; mutating those
  four glutamates abolishes binding).
- The helix is necessary but not sufficient on its own.

## Structural check against our residue

Measured on AlphaFold `AF-O60566-F1` v6:

| | distance from the CENP-E helix (1031–1050) |
|---|---:|
| **N1002 — proband** | **closest approach 26.9 Å, mean 36.2 Å — NO CONTACT** |
| L1012P | 19.1 Å — no contact |
| I909T | 17.2 Å — no contact |
| L844F | 8.9 Å — no contact |
| R814H | 28.6 Å — no contact |
| R727C | 28.8 Å — no contact |

The helix sequence in the model is `LNKALWKVGKLTSPGALLFQ` — three basic residues, zero
acidic, matching Legal's description of a basic helix complementary to CENP-E's acidic patch.

**N1002 is roughly 27 Å from the nearest residue of the CENP-E interface.** It is not a
CENP-E-binding residue, and neither is any of the five calibration destabilisers — which is
itself consistent with all of them being stability mutants rather than interface mutants.

## And even if it were on that interface

Legal tested it: BubR1^1–1030^, which cannot bind CENP-E, still formed a metaphase plate
with PP2A-B56 targeting intact, but showed significantly more misaligned chromosomes —
phenocopying CENP-E depletion. So losing the CENP-E interaction is a **partial alignment
defect, not a collapse.** The downside case was bounded even before we ruled it out.

## One structural caveat worth recording

Querying the PDB for BubR1 (O60566) returns nine entries, but **none resolves the
pseudokinase domain**: the X-ray structures are short TPR-domain and KARD fragments
(9–176 residues), and the full-length entries (5KHU, 5LCW, 6TLJ) are 3.8–4.8 Å cryo-EM
of MCC-APC/C in which the middle and C-terminal regions are unresolved.

**There is no experimental structure of the BubR1 pseudokinase domain.** AlphaFold is the
only structural model available — which is exactly why Suijkerbuijk could not do this
analysis in 2010, and why every structural statement here carries model uncertainty.

## Revised verdict

Confidence that N1002K is a **pure dosage (stability) mutant**: **~85% → ~92%.**

Both named functional features of the pseudokinase domain are now excluded on distance:
the Plk1 site T1008 (11.6 Å, different structural element) and the CENP-E interface
(26.9 Å, different end of the domain).

What remains, and cannot be closed from literature: **nobody has assayed N1002K itself.**
The prediction rests on class membership, structural context and the two nearest analogues
being proven normal-but-scarce. That is a strong inference. It is not a measurement.
