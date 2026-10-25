# Where we stand

## 1 · Is arimoclomol the recommendation now? No.

The ΔΔG result moves it up. It does not overturn the NAD⁺ route, for four reasons.

**A 1.5 kcal/mol destabilisation does not mean the protein misfolds.** Taking a typical
domain stability of ~8 kcal/mol as illustration (BubR1's own is unmeasured):

```
   wild type        fraction unfolded  2.3e-06
   N1002K (-1.51)   fraction unfolded  2.6e-05     11.5x more -- and still far below 1%
```

The protein still folds. What changes is how often it **visits** exposed states where
quality control can catch it. That is a kinetic argument, not a folding failure, and a
chaperone helps only if the protein is genuinely a chaperone client — which ΔΔG does not
establish.

**More HSP70 is not unambiguously good.** HSP70 partitions between refolding a client and
handing it to CHIP for degradation. Raising it could push either way. Nothing we measured
says which.

**NAD⁺ is hypothesis-agnostic; the chaperone route is not.** K668 deacetylation extends
BubR1's half-life regardless of *why* that half-life is short. Arimoclomol works only if
the folding story is right.

**The evidence asymmetry has not changed.** NMN raised BubR1 abundance *in vivo*, and SIRT2
overexpression extended lifespan in the BubR1-hypomorphic mouse — the accepted model of
this disease. Arimoclomol has no *BUB1B* evidence at all. **A predicted ΔΔG from a neural
network does not outweigh an in-vivo measurement in the right gene and the right model.**

They remain **co-leads**. What would settle it is one more cheap question: **is N1002K
BubR1 actually an HSP70 client?** Co-immunoprecipitation, or whether HSP70 induction
rescues abundance in patient cells. That is now the natural second lane.

---

## 2 · What we know about *BUB1B*

**The disease is a dosage problem, and the dose is known.**

- Reducing BubR1 in **graded** steps gives graded aneuploidy and senescence in mice
  (Baker 2004).
- Disease appears below **~50%** of normal — ">50% decrease in expression or activity"
  across seven families (Matsuura 2006).
- **50% is safe in humans.** ~**610** people in gnomAD carry one dead *BUB1B* allele and
  are not MVA patients; **zero** are homozygous in ~731,000.
- **Restoring dosage fixes the cell.** Transferring a chromosome 15 into patient cells
  restored BubR1 levels, p55cdc kinetochore localisation and the normal colcemid response
  (Matsuura 2006). That is the closest anyone has come to treating this disease, and it
  worked — in a dish, in 2006, and nobody followed it up.

**But the protein is a waveform, not a level.** BubR1 must be *destroyed* at anaphase for
division to proceed; an undegradable version markedly delays chromosome segregation
(Choi 2009). Any therapy must raise the amplitude without filling the trough.

**Nothing has ever been tried.** Zero registered trials under either disease name. No
treated patient. No failed attempt.

## 3 · What we established about this child

| | finding |
|---|---|
| **Allele 1** p.Leu737Ter | **UGA** stop, **748 nt** upstream of the last junction → canonical NMD substrate → contributes **zero** |
| **Allele 2** p.Asn1002Lys | makes protein; buried (**13.9%** RSA); loses an **acceptor** H-bond to Trp978 that no substitution can replace |
| **Ceiling** | 50% — *exactly* the disease threshold — so being affected means strictly below it |
| **Gap to close** | ~**1.43×**, if allele 2 retains 70%. A shortfall, not a doubling |
| **New** | N1002K predicted **+1.51 kcal/mol** destabilising — above **all 9** tolerated variants in the domain (z = +4.32); a benign variant two residues away scores **+0.14** |

## 4 · What we built, and what we killed

**The map.** 2,536 alleles, each with a transcript verdict, a protein verdict, an evidence
tier, and the experiment that would settle it. Rows with no named experiment: **0**.

**280 of 2,536 lose the transcript.** Of twenty approaches, the eight that could reach them
are all blocked by viability. That boundary has survived five changes of technology and a
viability gate that overturned our own top pick.

**Killed, with reasons:** splice-modulating ASO (junction flux 0.00% vs SCN1A's 4.55%),
neoantigen vaccine (germline — it would target the patient), circRNA payload (fills the
anaphase trough), APC/C inhibition (arrests every mitosis), pseudokinase chaperone (not
evaluable — no structure above 3.8 Å exists).

## 5 · How this gets solved

Not by picking a drug today. By the order of operations an n-of-1 at NIH has already
validated:

1. **One western blot in patient fibroblasts** — wild type, N1002K, **N1002R**, N1002S,
   plus a pT1008 lane. This does three things at once: tests whether the abundance thesis
   is right at all, **selects between the two co-lead drugs**, and tests a ΔΔG prediction
   written down in advance (K and R should be equally destabilising; "K unstable, R stable"
   falsifies it).
2. **Then test rescue in those same cells** — the agent the first step selected.
3. **Only then** consider a single-patient study with a mechanistic readout.
4. **Endpoint: aneuploid-cell fraction**, which is ongoing and has headroom — not
   microcephaly or growth, which are damage already accrued.

## 6 · The honest bottom line

**We cannot cure this child, and nothing here claims to.**

What this work does: it says which of 2,536 alleles any future therapy can reach and which
it cannot; it narrows twenty candidate approaches to two obtainable co-leads; and it
designs one cheap experiment that chooses between them while testing a number we committed
to in advance.

In a disease with no trial, no treated patient and no validated endpoint, that is the
useful thing — and it is the map, not the drug, that is the deliverable.
