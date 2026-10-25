# Every BUB1B variant we can reach

Built to diagnose a specific problem. `STABILITY-AXIS.md` showed three stability
predictors separating four alleles with measured-reduced protein from the one allele
with measured-normal protein — and had to report **p = 0.20, not significant**, because
a single negative control cannot support a test. The fix was never a better predictor.
It was more negatives.

Rebuild with `apps/api/scripts/mva/variants/variant_atlas.py` and
`powered_calibration.py`; inputs are committed under `docs/mva/data/variants/`.

## Sources

| source | what it covers | reachable |
|---|---|---|
| **EBI Proteins API** (`O60566`) | aggregates ClinVar, UniProt/humsavar, dbSNP, COSMIC, gnomAD | yes — **1,629 variants** |
| **Paperclip** full-text mining | primary case reports, 60 papers across two sweeps | yes — **11 entries not in the aggregate** |
| **LitVar2** (NCBI) | variant→publication mapping | yes — 54 variants, 26 with a clinical record |
| **Europe PMC** full-text sweep | 854 open-access full texts | yes — **3 new patient alleles** after filtering |
| UniProt REST, gnomAD, COSMIC direct | — | **blocked by egress policy**; reached indirectly through EBI |

## The aggregate is wrong about six variants, and it matters

The EBI aggregate labels six genuine nonsense variants as `missense`. Their
`alternativeSequence` is `*`:

`p.R67*` · `p.R114*` · `p.R224*` · `p.Gln309Ter` · `p.R550*` · `p.Arg770Ter`

Taking the labels at face value gives 19 pathogenic missense variants. The truth is
**14** — a third of the missense count is nonsense variants in disguise. Every script
here corrects by allele, not by label.

**One of those six lands on our own corpus.** `VARIANT-TABLE.md` carries **R770Q** as
the "architectural match" to the proband — a missense allele that both predictors call
benign. The aggregate's pathogenic variant at that codon is **R770Ter** (`c.2308C>T`),
a nonsense allele. These are two different variants at one codon, and the interesting
one for the proband's architecture may be the nonsense. **This needs checking against
the primary source before the architectural-match argument is used again.**

## What the corpus looks like

**69 pathogenic or likely-pathogenic variants**, corrected:

| | count |
|---|---|
| stop gained | 30 |
| frameshift | 25 |
| **missense** | **14** |

**Truncation is the disease mechanism: 55 of 69.** That is the single clearest fact in
the atlas, and it frames everything about the proband — allele 1 (`L737Ter`) is the
common kind of MVA allele, allele 2 (`N1002K`) is the rare kind.

### By domain

| domain | P/LP total | missense | truncating |
|---|---|---|---|
| TPR (1–204) | 13 | 2 | 11 |
| KEN/ABBA + linker (205–340) | 10 | 1 | 9 |
| GLEBS/Bub3-binding (341–477) | 13 | 4 | 9 |
| middle / unassigned (478–765) | 14 | 1 | 13 |
| **pseudokinase (766–1050)** | **19** | **6** | 13 |

The pseudokinase domain carries the most pathogenic variants of any domain and the
largest share of the pathogenic missense — 6 of 14. Truncating variants are spread
almost evenly along the protein, which is what a nonsense-mediated-decay mechanism
predicts. Missense variants are not: they concentrate where there is a folded domain
to break.

## The calibration, redone properly

The atlas supplies **102 benign / likely-benign** variants, **27 of them (with Q921H
reclassified below) missense inside the pseudokinase domain with a stability score already computed** in the
saturation matrices. No new jobs were needed.

| method | AUC | z | median pathogenic | median benign |
|---|---|---|---|---|
| ProteinMPNN-ddG | **0.963** | **+3.24** | −4.83 | −0.83 |
| ThermoMPNN | **0.926** | **+2.98** | −2.00 | −0.27 |
| *(previous, n=1 negative)* | *1.00* | *p = 0.20* | — | — |

**5 pathogenic against 27 benign, and both methods are now significant.** This is the
result `STABILITY-AXIS.md` could not reach, and it did not need better predictions —
only a negative set that was not starved.

> **Qualified by `ATLAS-AUDIT.md`, and this qualification is load-bearing.** Relative
> solvent accessibility alone — one geometric number, no stability predictor — separates
> the same two groups at **AUC 0.875** (pathogenic median RSA 3.4%, benign 31.6%). ΔΔG
> methods read burial, so most of the 0.963 is available without them, and at n=5
> positives the increment is not distinguishable from zero. The defensible claim is that
> **pathogenic missense alleles here are buried and benign ones exposed, and ΔΔG recovers
> that** — not that the predictors are contributing the separation. There is also a source
> confound: 4 of 6 positives are UniProt-only, 0 of 28 negatives are. It is mitigated by
> four of the positives carrying direct functional measurements rather than annotations.

**The caveat that governs it:** these negatives are *annotations*, not measurements.
That is weaker evidence per variant than the westerns behind the four positives. The
honest summary is that the stability axis separates clinically-annotated pathogenic
from clinically-annotated benign missense in this domain at AUC 0.83–0.90.

### Q921H: the databases are wrong, and the primary source says why

UniProt asserts Q921H **Pathogenic** for MVA1, PCS and colorectal cancer, which appeared
to put our whole negative control in doubt. It does not. Suijkerbuijk 2010 measured the
variant directly (PMC2887387, retrieved from NCBI — the paper is not in the Paperclip
corpus, so an earlier "no matches" grep was a false negative, not evidence):

> *"In striking contrast, the Q921H mutation was **indistinguishable from wild-type
> LAP-BUBR1, both on protein level and functionality**."*

The preceding sentence explains the bad annotation:

> *"of the two substitution mutations that were reported to occur **within one allele**
> (L844F and Q921H) … L844F was poorly expressed and unable to restore any of the
> defects … This suggests that **the L844F substitution is the likely cause** of mitotic
> defects in the patient."*

**Q921H and L844F sit on the same allele in one patient. Q921H is the passenger and
L844F is the driver.** The pathogenic annotation is passenger mis-attribution — the
variant was catalogued from an MVA patient without separating it from the allele it
travelled on. A direct measurement of both protein level and function beats a database
assertion with an identifiable failure mode, so `powered_calibration.py` scores Q921H
**benign**, and says so in its docstring rather than burying the override.

Doing that strengthens the result: **AUC 0.963 (z +3.24)** and **0.926 (z +2.98)**,
5 pathogenic against 27 benign.

`R550Q` still has an unresolved conflict of the same shape — our corpus says measured
fully functional, the aggregate says Pathogenic for MVA1 — but it is outside the
pseudokinase domain and does not enter this test.

`R550Q` has the same shape of conflict: our corpus says *measured fully functional*, the
aggregate says Pathogenic for MVA1.

## N1002 is absent from all 1,629 — and that is NOT evidence

The proband's second allele appears nowhere in the aggregate: not as pathogenic, not as
a VUS, not as a population variant. The tempting reading is that the position is so
constrained it is never seen.

**That reading is wrong.** 62 of the 285 pseudokinase-domain positions have no recorded
variant of any kind. Absence at any one position is **~22% likely by chance**. It is a
coverage gap, not a constraint signal, and it must not be presented as one.

What *does* carry signal is the ΔΔG evidence already in `STABILITY-AXIS.md`: position
1002 is the 21st most substitution-intolerant of 285.

## Recovered from the literature, not in the aggregate

Eleven entries, each cited to the paper it was read from — see
`data/variants/literature_addendum.json`.

- **p.Ser802Cysfs\*29** (`c.2405_2406del`) with `c.2577+5G>A` — embryonal
  rhabdomyosarcoma, karyotype-confirmed mosaicism and PCS. PMC10545765.
- **AluYa5 insertion** in the intron 8 polypyrimidine tract, with an upstream
  regulatory `G>A` — a structural allele no missense predictor can see. PMC5462940.
- **p.Ser738fs\*753** (`c.2211insGTTA`) — the allele modelled in `BubR1+/GTTA` mice;
  truncated protein **undetectable** by western. PMC3531486.
- **p.Glu391del** — monoallelic, prostate cancer, and **measured**: strong reduction of
  BubR1 abundance in mitotic cells, impaired SAC, taxol resistance. PMC11251299. This
  is a genuine measured-reduced allele, but an in-frame deletion outside the
  pseudokinase domain, so no ΔΔG method here can score it.
- Four further monoallelic cancer alleles: `p.Thr237Glnfs*8`, `p.Gln827Hisfs*13`,
  `c.2009+1G>A`, `p.Pro378_His385del` (engineered, not a patient allele).
- `p.Ile82Asn`, `p.Pro334Leu` — in-silico screens only, **no patient**. Do not treat as
  disease alleles.

### Two literature traps

**W722R and A739S must not be counted as measured.** PMC13349884 reports both in
recurrent pregnancy loss with western blots — but the authors state the result is "a
**trend toward** decreased" abundance and "should be interpreted as preliminary
evidence rather than definitive quantification". The unaffected father shows the same
trend. Adding these to the measured-reduced set would have manufactured two positives.

**A notation conflict at codon 349.** PMC5024654 reports `p.Gln349Arg` (rs1801376) as a
gastric-cancer polymorphism; UniProt curates `p.Arg349Gln` at the same codon as
**Benign**. Reciprocal notation — the reference allele assignment differs between
sources. They are one variant, not two, and must be reconciled before either is used.

## Four indexes, four different failure modes

Paperclip does not index PMC2887387 — the one paper that measures the dosage axis — so
one literature source is not enough. Three more were added. None of them is complete and
**none of them fails in the same way**, which is the argument for reconciling all four
rather than picking a winner.

| route | yield | how it fails |
|---|---|---|
| **EBI aggregate** | 1,629 variants | mislabels consequence type (6 caught); only carries what was deposited |
| **Paperclip** | 60 papers, good extraction | corpus gaps — missed the key paper entirely |
| **LitVar2** | 54 variants | conflates lab constructs with patient alleles; cross-gene bleed |
| **Europe PMC full text** | 854 texts scanned | proximity is not association; ~78% false positives |

### LitVar2: split the clinical half from the text-mined half

26 of its 54 BUB1B variants carry a ClinVar record; **28 are text-mined only, and that is
where the lab constructs hide** — `K243R` (the mouse acetylation mutant), `K250Q/R`,
`S670A/D`, `I672A`, `D513K`, `Y141A`, `W125A`. `Y259C` is not even BUB1B; it is a *BUB1*
variant that bled across because papers discuss both. Use the clinical half; read the
source before believing the other.

It did settle one thing: `rs1801376, p.Q349R, benign, 66 papers` — the codon-349
reciprocal-notation conflict is **one variant, not two**. It also lists **Q921H as
`uncertain-significance`**, so UniProt's Pathogenic call is a lone outlier, which
independently supports the reclassification above.

**Reciprocal notation is a systematic hazard, not a typo.** Four codons disagree on which
residue is reference between sources: `Q349R`/`R349Q`, `M40T`/`T40M`, `D10A`/`A10D`,
`S10A`/`A10S`. Merge two databases naively and you double-count every one.

### Europe PMC: 854 full texts, and why filtering is most of the work

The sweep pulled every open-access full text from five queries and regexed HGVS notation
within ±350 characters of a BUB1B/BubR1 mention. 249 protein notations came back. Then:

| filter | removed |
|---|---|
| position beyond residue 1050 | 24 — `p.R2106C`, `p.Val1822Asp` … |
| reference residue ≠ BUB1B sequence | 171 — including `p.V600E` (**BRAF**) and `p.R337H` (**TP53**) |
| already in the EBI atlas | 25 |
| **surviving** | **29** |

**Proximity is not association.** In a paper with a large variant table every gene is
within 350 characters of every other. The reference-residue check removes most of it but
not all: `p.I941T` survived every automated filter and is a **KIAA1804** variant — it
passed only because residue 941 happens to be isoleucine in BUB1B too. Every surviving
hit needs a human to read its sentence.

**And the regex erred in the other direction too.** It truncated `p.Trp803Hisfs*10` to
`p.Trp803His` and `p.Glu213GlyfsTer15` to `p.Glu213Gly`, which made two genuine
frameshifts look like missense. Reading the sentences corrected the type.

Net yield after adjudication — **three new patient alleles and one confirmation**:

- **`p.Trp803Hisfs*10`** (`c.2405_2406insCC`), maternally inherited, fetal structural
  anomalies — PMC11535759. Absent from ClinVar. Note it hits the **same codon pair** as
  the `c.2405_2406del` allele from PMC10545765: one hotspot, two different events.
- **`p.Glu213Glyfs*15`** (`c.638del`), lung cancer, Colombian germline programme —
  PMC12229586, which also independently reports `p.(Arg67Ter)` in breast/ovarian cases.
- **`p.Val870Ala`** (`c.2609T>C`), pseudokinase domain — PMC11352340. The atlas carries
  V870M at that codon but not V870A.
- **`p.Arg770Ter`** (`c.2308C>T`, rs750364303) confirmed independently as causing PCS —
  PMC5894988. **This is a second source for the R770 nonsense allele, and it sharpens the
  flag above: our architectural-match argument is built on R770Q and needs re-checking at
  its primary source.**

The honest summary — **corrected by `ATLAS-AUDIT.md`**: the EBI aggregate is near-complete
for **protein-altering** variants only. ClinVar directly holds 2,493 BUB1B records against
its 1,629, and the difference is largely **612 synonymous and 456 intronic** records a
protein endpoint cannot represent. Protein-altering records reconcile (~1,592 vs 1,629),
but the aggregate is **blind to the non-coding half of ClinVar** — including splice alleles
that are real MVA alleles — while carrying UniProt assertions ClinVar does not. It is
neither a superset nor a subset. Full-text mining earns its keep only for undeposited
variants; it found three in 854 papers and cost more verification than every other source.

## Standing limits

- gnomAD, COSMIC and UniProt REST are blocked here; everything from them arrives
  second-hand through the EBI aggregate and inherits its labelling errors — six of
  which are documented above, which is reason to expect more.
- ClinVar significance is an assertion, not an experiment, and the submitting labs are
  not independent of each other.
- The literature sweep covered 60 papers over two searches. It is not exhaustive, and
  case reports in non-indexed journals are certainly missed.
- Only 14 pathogenic missense variants exist across the whole protein, and only 6 in
  the domain with a structure. Every stability claim rests on those 6.
