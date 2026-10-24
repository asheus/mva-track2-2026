# Would NMD inhibition alone work, and why has nobody tried it?

Written in response to four direct questions. It contains a correction to my own previous
conclusion, which was stated too confidently.

---

## 1. CORRECTION FIRST: I under-weighted a result that cuts against the NMD-alone idea

Last pass I said residues 1–736 contain every functional motif, so stabilising the
transcript should yield a working protein — citing LAP-731X, which "restored the response
to nocodazole as well as proper chromosome segregation".

**What I under-weighted: LAP-753X does NOT work.** In the same paper, 753X was among the
truncations that "were unable to sustain a mitotic delay in response to spindle
depolymerization and caused severe chromosome missegregations", and it was one of only two
truncations expressed at levels *lower* than wild-type.

So within 22 residues the field has one truncation that fully rescues (731X) and one that
fails (753X). **This child's stop at 737 sits between them.** The NMD-alone argument
depends entirely on which one 737X resembles, and I presented that as more settled than it is.

### A structural test of the anomaly

I first guessed that 731X truncates inside disorder while 753X truncates into folded
structure. **That is wrong** — the pLDDT profile shows 720–760 is uniformly ordered
(mean 76–87), so neither leaves a "clean" end.

The real picture is better. Residues ~725–765 form an **N-terminal extension that docks
onto the kinase domain** — 726, 727, 730, 731, 734, 736, 737, 740, 742, 743, 744, 746,
748–751, 753 all make contacts with residues ≥766. Truncating anywhere in that stretch
leaves part of that docking surface **orphaned**: a greasy interface with nothing to pack
against, which is a classic trigger for aggregation and degradation.

Quantifying the orphaned interface (SASA of each linker residue buried specifically by the
kinase domain, summed up to each stop):

| truncation | orphaned interface | relative | observed behaviour |
|---|---:|---:|---|
| **731X** | 500 Å² | 1.00× | stable, **fully rescues** |
| **737X — this proband** | **643 Å²** | **1.29×** | **unknown** |
| **753X** | 1252 Å² | 2.50× | unstable, **fails** |

The gradient is monotonic and it puts this child's truncation much closer to the working
one than to the failing one — 29% more orphaned surface than 731X, versus 753X's 150% more.

**This is a hypothesis with n=2 calibration points, not a validated predictor.** But it
explains an anomaly the original paper left unexplained, and it makes a falsifiable
prediction: express LAP-737X and it should behave like 731X.

---

## 2. Are there approved NMD inhibitors?

**No. Not one.** There is no drug approved anywhere as an NMD inhibitor for any indication.

What exists is one **approved drug with NMD-inhibitory activity discovered later**:

**Amlexanox** — an azoxanthone used for over 30 years for aphthous ulcers, and for asthma
in Japan. In 2012 a screen of 1,200 marketed drugs identified it as an NMD inhibitor. It
raised PTC-containing mRNA for *TP53*, *DMD* and *CFTR*, and — notably — also induced
full-length protein, suggesting it does **both** NMD inhibition and some readthrough.

Everything else is preclinical: SMG1 inhibitors, NMDI-1 (a new indole chemical class with
acknowledged development risk), NMDI-14, and the PI3K inhibitors wortmannin and caffeine,
which hit NMD indirectly through SMG1.

**So the honest status: the class does not clinically exist yet.** Amlexanox is the only
molecule you could put in a person tomorrow, and its approved use is topical paste or
short-course — not chronic systemic dosing at NMD-inhibiting exposure in a child.

## 3. Has anyone been treated this way?

**No patient has ever been treated with NMD inhibition alone as a therapy.**

But the *principle* has a direct precedent: in **Ullrich's disease**, inhibiting NMD with
wortmannin and caffeine restored truncated collagen VI in patient fibroblasts and
"partially rescues extracellular matrix function in vitro." That is exactly the logic
proposed here — stabilise the transcript, get a functional truncated protein — demonstrated
in human patient cells, for a different gene.

So this is not an exotic idea. It is an established principle that has never reached a
patient, and never been considered for MVA.

## 4. Why didn't anyone think of this? Are we missing something?

Four reasons, and the fourth is the real one.

**(a) For almost every nonsense allele, NMD inhibition alone is pointless.** The general
rule is that stabilising a PTC transcript yields a truncated, useless protein — which is
why the field built readthrough drugs instead. The field's default is correct in general
and happens to be wrong *for this particular stop codon*, because it falls in the one gap
in BubR1 between the last functional motif (KARD, 669–674) and the kinase domain (766).

**(b) The two facts you need were published together but framed as pathology, not therapy.**
Suijkerbuijk 2010 showed both that 731X transcripts are NMD-destroyed *and* that 731X
protein is fully functional. They were answering "why are these patients sick", not "what
would rescue them". The therapeutic reading requires putting their own two results side by
side with a therapeutic question in mind.

**(c) It is genotype-specific, and nobody stratifies an ultra-rare disease.** For an MVA
patient carrying 386X, NMD inhibition gives a fragment lacking the Bub3-binding domain that
cannot even reach kinetochores — useless. The strategy only works for truncations after the
KARD. Nobody is going to genotype-stratify a therapy for a disease with a prevalence below
1 in 1,000,000.

**(d) There is no research programme at all.** We established earlier in this workstream
that MVA has had **zero clinical trials, ever, worldwide.** There is no funded pipeline, no
patient registry driving trials, no commercial interest. The idea was not rejected — it was
never in front of anyone.

### So are we missing something? Yes — two things, and neither is fatal

1. **The 731X-versus-753X problem above.** This is the real gap, and it is a bench
   experiment away from being closed.
2. **Safety, which is the binding constraint.**

## 5. The safety picture, which is better than I expected — with one exception that matters

A purpose-built transgenic mouse expressing inducible dominant-negative UPF1 tested exactly
this question. Results:

- **Modest NMD inhibition for 1 month produced no discernible defects** in most tissues, and
  still "significantly enhance[d] in vivo PTC suppression".
- Moderate-to-strong inhibition produced only "modest immunological and bone alterations".
- Conclusion: "moderate global NMD attenuation is generally well tolerated in
  non-neurological somatic tissues."
- Supporting this, **NMD efficiency already varies 2–4 fold naturally across the general
  population**.

**The exception, and it lands precisely on this child:**

> "we observed a significant change in NMD substrate abundance in neurological tissues with
> very modest dnUPF1 expression, suggesting that neurological tissues might be particularly
> responsive to changes in NMD efficiency."

And separately: NMD factor nulls are embryonic lethal, and **copy-number variants of NMD
factors are associated with intellectual disability.**

So the tissue most sensitive to NMD inhibition is the brain, in a child whose phenotype is
of this age. (Earlier drafts attributed microcephaly and developmental delay to this
child; the record lists neither — see `PHENOTYPE-GROUNDING.md`.) That is not a reason to abandon
the route, but it is the question any protocol would have to answer first, and the mouse
work explicitly leaves it open: "further evaluation of neurological tissues will be
required."

## 6. What this changes about the plan

The NMD-alone route is **more plausible than the field's default and less certain than I
implied.** Ranked by what would move it:

1. **Express LAP-737X and test rescue** — settles 731X-vs-753X directly, needs no patient
   material, uses an assay that already exists. This is now the single highest-value
   experiment in the whole workstream, ahead of the western blot.
2. **NMD inhibitor on the child's cells, blot for the truncated band** — tests whether the
   transcript is rescuable at all.
3. Only then does the amlexanox-versus-newer-NMD-inhibitor question become worth asking.

If experiment 1 comes back looking like 753X, this route closes and readthrough becomes
mandatory rather than optional — which would also make the UGA-selectivity of DAP, and its
tryptophan insertion at a linker residue, considerably more important.
