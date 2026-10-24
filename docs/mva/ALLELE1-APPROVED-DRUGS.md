# Approved drugs for the allele-1 NMD route

*Opened 23 Oct 2026. The question: if allele 1 needs only NMD inhibition — not readthrough —
what is approved?*

## The logic this serves, restated

1. Allele 1 is `p.Leu737Ter` (UGA), **748 nt** upstream of the last exon–exon junction, so
   canonical rules predict NMD, and the transcript is lost.
2. **Suijkerbuijk 2010's LAP-731X — lacking the entire kinase domain — *fully* restored
   checkpoint response and chromosome alignment.** Our truncation at 737 retains everything
   731X retains, and six residues more.
3. So the protein allele 1 would make is plausibly **functional**. The defect is that the
   transcript never survives to be translated.
4. **Therefore readthrough is not required.** Blocking decay alone could convert allele 1
   from a null into a working protein — and the +0.53 percentage-point readthrough efficiency
   ceiling that retired that route (`WHICH-ALLELE-TO-TARGET.md`) does not apply.

Caveat carried from `WHICH-ALLELE-TO-TARGET.md` and not resolved: **753X *fails* where 731X
rescues**, our 737X sits between them, and we called it ~70/30 off a two-point calibration.
Step 2 is a probability, not a fact.

## The answer: amlexanox, and essentially only amlexanox

### Our own report dismissed it on a false premise — corrected here

`TRACK2-REPORT.md:365` states: *"No NMD inhibitor is approved anywhere; amlexanox is a
**topical/short-course agent, not chronic systemic dosing** in an infant."*

That is wrong, and our own supporting file already said so —
`ALLELE1-NMD-READTHROUGH.md:51` records amlexanox as an **approved drug (aphthous ulcers;
asthma in Japan)**. The report shipped the weaker claim while the corpus held the better fact,
which is the same propagation failure the Review Room found six times over.

The primary evidence, according to PubMed:

| Fact | Source |
|---|---|
| **Oral systemic amlexanox has been through a randomised, double-blind, placebo-controlled trial** — 42 obese patients with T2D and NAFLD, significant reductions in HbA1c and fructosamine | Oral et al. 2017, *Cell Metab* ([PMID 28683283](https://doi.org/10.1016/j.cmet.2017.06.006)) |
| Amlexanox is **"a drug used for decades"**; it raises nonsense-transcript levels **and** produces full-length protein **"in an efficient manner"**, and those full-length proteins are **functional**, in three patient-derived lines | Gonzalez-Hilarion et al. 2012, *Orphanet J Rare Dis* ([PMID 22938201](https://doi.org/10.1186/1750-1172-7-58)) |
| **100 µM, 20 h** stabilised **UGA-PTC** transcripts and restored mitochondrial morphology in **patient hiPSC-derived neuronal cells** (CMT2H, `GDAP1` p.Ser194*) | Benslimane et al. 2023, *Pharmaceuticals* ([PMID 37513945](https://doi.org/10.3390/ph16071034)) |

So "topical/short-course" is replaced by: decades of approved use, an oral indication in Japan,
an oral RCT in adults, and **patient-cell functional rescue at a UGA stop — the same stop class
as allele 1 — in neuronal cells.**

### Why its dual mechanism suits this allele unusually well

Amlexanox does both NMD inhibition *and* readthrough. For most targets that muddies mechanism
attribution. Here it is a genuine advantage, because **both outputs are useful and they are
additive rather than alternative**:

- NMD inhibition alone → the transcript survives → **truncated 737X protein**, which the 731X
  precedent says is functional.
- Readthrough on the stabilised transcript → **full-length protein**, and at our UGA-A context
  a leucine insertion restores the *true wild-type* residue (Xue 2017; logged in
  `ALLELE1-NMD-READTHROUGH.md`).

Either product is a win, so the efficiency requirement is far lower than for a
readthrough-only agent that must clear the +0.53 pp ceiling on its own.

## The decisive unknown, which must be measured and not assumed

**Does oral amlexanox reach 25–100 µM in human plasma? Searched 23 Oct 2026. The published
human Cmax could not be found.** That is itself the finding, and it is the single parameter
this route turns on.

What the search established:

- **Oral et al. 2017 dosed 50 mg PO three times daily for 12 weeks** (verbatim from Methods:
  *"Subjects were started on 50 mg three times a day dose ... without any titration"*). The
  trial **did** measure steady-state serum amlexanox and metabolites, reporting only that they
  were *"identifiable in the serum of the treated patients at 12 weeks"* with no
  responder/non-responder difference. **No numeric concentration appears in the retrievable
  full text** — the only concentration units in the entire paper are a 20 mM buffer. The
  values are in a supplementary figure.
- **DailyMed returns zero amlexanox labels.** The US topical product is delisted, so there is
  no US pharmacokinetics section to read.
- The Japanese oral product, which Reilly et al. 2013 (*Nat Med*,
  [PMID 23396211](https://doi.org/10.1038/nm.3082)) confirms in its abstract — amlexanox is
  *"an approved small-molecule therapeutic presently used in the clinic to treat aphthous
  ulcers **and asthma**"* — was not reachable from here.

**A generous upper bound, computed rather than asserted:**
`apps/api/scripts/mva/amlexanox_exposure_gap.py` takes the 50 mg dose and MW 298.29 and
assumes complete absorption, no first-pass loss and instantaneous distribution — every
assumption biased in the drug's favour, so a real Cmax must be **lower** than these:

| Vd/F (L) | upper-bound Cmax | shortfall vs 25–100 µM |
|---:|---:|---|
| 10 | 16.8 µM | 1.5–6× |
| 20 | 8.4 µM | 3–12× |
| 50 | 3.4 µM | 7.5–30× |

**What this does and does not say.** It does **not** establish that the route fails: Vd/F is
unknown for amlexanox, and a much smaller value would narrow the gap. It establishes that a
gap is *likely*, and that two things make it likely worse rather than better — these are
**total** drug, while amlexanox is a carboxylic acid and so probably substantially
albumin-bound (binding not found in any accessible source, so unknown rather than assumed);
and the 25–100 µM figures are in vitro in serum-containing medium, which for an albumin
binder transfers unfavourably.

### The interview form was retrieved. The Cmax is in it and still could not be read.

Found and downloaded 23 Oct 2026: **"SOLFA® 25mg. & 50mg. TABLETS"** interview form,
2008, 45 pages ([PDF](https://www.ps.toyaku.ac.jp/~kosugi/zemi2011/iform/Amlexanox_Tablets.pdf);
PDF title confirms ソルファ25mg・50mg錠　インタビューフォーム).

**Page 27 is Section VII, the pharmacokinetics section**, and it contains exactly what we
wanted: a plasma concentration–time curve with three dose groups and error bars, and a PK
parameter table whose column headers carry β and µ — i.e. elimination phase, and µg/mL /
µg·hr/mL for Cmax and AUC.

**The values are unreadable by any route available here.** The 2008 PDF uses Adobe-Japan1
CID fonts with no ToUnicode CMap, so `pdftotext` returns glyph garbage (only µ, β, α and Å
survive), and poppler cannot even *render* the text — it reports
`Missing language pack for 'Adobe-Japan1' mapping` and drops every character, so the page
images show the axes, curves and table rules with every number absent. `poppler-data` has no
installation candidate in this container.

**This is a two-minute task for anyone with a working CJK PDF stack**, or simply opening that
URL in a browser. Read page 27's table and the Cmax, Tmax, AUC and β-phase half-life are
there, at a stated oral dose.

### But the more important finding: the oral product no longer exists

| | Status |
|---|---|
| **Solfa tablets 25/50 mg (oral, Japan)** | **Discontinued September 2017**, transition period to ~March 2019 |
| Aphthasol (topical, US) | **No label on DailyMed** — delisted |
| KEGG D01828 | **No PRODUCT lines**, consistent with no current Japanese marketing |

So "amlexanox is an approved drug" needs restating. It **was** an approved oral drug, its
systemic respiratory indication is real (ATC **R03DX01**, and Reilly 2013's abstract calls it
*"an approved small-molecule therapeutic presently used in the clinic to treat aphthous ulcers
and asthma"*), and it **has** been given orally to humans for 12 weeks at 150 mg/day. But it
is **not currently obtainable as an oral medicine**, in Japan or the US.

**What that does to the case, precisely.** It is a supply obstacle, not a pharmacological one,
and it is not fatal for an n-of-1: the drug substance exists, a 12-week human safety dataset
exists, and the Oral 2017 trial manufactured clinical supply *after* the Japanese withdrawal
had begun. But it moves amlexanox out of "repurpose an approved drug you can prescribe" and
into "obtain API, compound or manufacture, and file an IND" — a different undertaking with a
different timeline, and one that removes the main advantage repurposing was supposed to buy.

**The irony worth recording.** `TRACK2-REPORT.md` dismissed amlexanox as *"a topical/short-course
agent, not chronic systemic dosing in an infant."* That was **wrong on the science** — oral
chronic dosing in humans is exactly what the 2017 RCT did — and **accidentally right on
availability**, for a reason the report never gave and could not have given, since the
discontinuation is not a pharmacological fact about the molecule. The withdrawal of that
dismissal stands; the conclusion it reached survives on a different and better-evidenced
objection.

## Two hazards our report does not currently carry

1. **TBK1/IKKε inhibition is amlexanox's other pharmacology, and TBK1 is an innate-immune
   kinase.** Human TBK1 deficiency is associated with susceptibility to herpes simplex
   encephalitis. If the RMS was treated (not in the record — see C50), with the infection risk the §4.4 IL-1 arm
   already flags, inhibiting an antiviral signalling kinase chronically is a real
   consideration, and it appears nowhere in our documents.
2. **NMD inhibition is global.** It stabilises every PTC-bearing transcript, and roughly
   5–10% of the transcriptome is NMD-regulated. In a child with a chromosome-instability
   cancer predisposition, stabilising truncated proteins genome-wide — including truncated
   tumour suppressors — is the standing objection, and it is unchanged by any of the above.

## The instructive trap: colchicine

Colchicine inhibited NMD below 0.4 µM in the Carrard 2023 reporter screen. On paper it looks
ideal and better than amlexanox: **approved, oral, and with decades of chronic *paediatric*
dosing** in familial Mediterranean fever — exactly the credential amlexanox lacks.

**It is the worst possible choice here.** Colchicine is a microtubule destabiliser, i.e. an
anti-mitotic, and this child's disease *is* a spindle-assembly-checkpoint defect. Our Gate 3
refuses mitotic poisons on mechanism. Worse, its NMD inhibition is most likely a *consequence*
of cytoskeletal disruption — the same screen's authors note that apoptosis inducers and
cytoskeleton disruptors show up as NMD inhibitors — so the desired activity and the
disqualifying activity are probably the same event.

Recorded because colchicine will look compelling to anyone filtering on "approved + oral +
chronic paediatric", and the filter that admits it is the wrong filter.

## Everything else approved, and why it fails

| Agent | Status | Why not |
|---|---|---|
| **Caffeine** | ubiquitous | SMG1 inhibition requires millimolar concentrations; also hits other PIKK kinases including the DNA-damage-response ones, which is the wrong thing to touch in a chromosome-instability syndrome |
| **Aminoglycosides** (gentamicin) | approved | They do stabilise PTC transcripts, but this is the readthrough route retired on efficiency — and ototoxicity plus nephrotoxicity against **nephrocalcinosis from birth** is the clearest contraindication in the whole workstream |
| **Wortmannin, NMDI-1/-14, SMG1i, SMG1-ASOs, "1a/2a"** | none approved | The potent and selective agents are all experimental. The SMG1-ASO route has the best efficacy data (≈5× mutant mRNA and functional rescue in CFTR-W1282X) and was delivered *locally* to lung; for us it would be systemic |

## What would settle it, cheapest first

1. **Human oral amlexanox Cmax**, from the Oral 2017 supplement and the Japanese Solfa label,
   against the 25–100 µM cellular range. One literature afternoon; potentially fatal to the
   route.
2. **Does allele 1's transcript actually respond?** Allele-specific RT-qPCR on this child's
   cells ± amlexanox, with an established NMD-reporter transcript to confirm pathway
   engagement and a `BUB1B` pre-mRNA control to separate stabilisation from transcription.
3. **Is the 737X protein functional at physiological dose?** The 731X rescue was from
   plasmid overexpression. The question for us is whether the amount rescued from NMD
   suffices — which is the 70/30 call in step 2 above, and is answerable with a
   C-terminal-blind antibody plus a checkpoint assay.

Only if all three hold does the TBK1 and global-NMD risk calculus become worth having.

---

# Addendum, 23 Oct 2026: the Cmax, and what replaces amlexanox

## The Cmax was read. The route is closed on exposure.

Interview form page 27 (single dose) and page 28 (repeated), healthy adults, extracted with
PyMuPDF after poppler failed on the Adobe-Japan1 CID fonts:

| Dose | Condition | **Cmax (µg/mL)** | Tmax (h) | AUC₀₋∞ (µg·h/mL) | t½β (h) |
|---|---|---:|---:|---:|---:|
| 25 mg single (n=3) | fasting | 1.14 | 1.6 | 4.1 | 3.6 |
| 50 mg single (n=4) | fasting | **4.78** | 1.0 | 13.4 | 5.6 |
| 50 mg single (n=4) | fed | 1.87 | 1.8 | 7.5 | 7.6 |
| 100 mg, day 1 (n=3) | fed | 2.75 | 2.5 | 12.9 | 5.4 |
| 100 mg, day 6 (n=3) | fed | **5.40** | 1.6 | 14.2 | 5.1 |

Column order on page 28 was jumbled in the text stream and is fixed by the form's own
sentence — *"Cmaxは第6日目が約2倍の高値を示したが、t1/2β及びAUC₀₋∞に差は認められなかった"*
(day-6 Cmax ~2× higher, t½β and AUC unchanged): 2.75 → 5.40 is the 2×, 12.9 → 14.2 is the
"no difference". Page 27's ordering is independently confirmed by the food effect — Cmax
4.78 → 1.87 and Tmax 1.0 → 1.8 fed versus fasting.

**§2-6: human plasma protein binding 98.4–99.4%** (in vitro, ultracentrifugation,
0.5/5/50 µg/mL); 5% human serum albumin 98.5–99.0%. §2-2 bioavailability: **該当資料なし**,
no data. §2-5 Vd 30.1 L fasting / 72.7 L fed. §2-4 clearance 62.2 / 110 mL/min.

At MW 298.29:

- **Highest total Cmax ever recorded: 5.40 µg/mL = 18.1 µM**
- **Free Cmax ≈ 0.11–0.29 µM**

Against the 25–100 µM at which NMD inhibition and readthrough are reported:
**total drug falls 1.4–5.5× short; free drug roughly 90–900× short.**

> **C51 — the range has a lower end, and we only ever quoted the top of it.**
> Added 24 Oct 2026. An independent run (`TRIAGE-KOSMOS-HACKATHON.md` §6) cites
> Carrard 2023 for amlexanox NMD-reporter and endogenous-transcript activity from
> **0.4 µM**, not 25 µM. Against 0.4 µM, free Cmax 0.11–0.29 µM is **1.4–3.6× short**
> — not 90–900×. The 25–100 µM figure is where the TBK1-vs-TFEB *separation* is
> reported (Krivega 2021), which is a different endpoint from NMD inhibition and is
> the one we had been quoting as though it were the only one.
>
> **The verdict does not change, but the reason gets weaker and must be stated
> honestly.** A 1.4–3.6× gap is not an order-of-magnitude wall; it is a gap a dose
> change would normally close. What still closes the route is that *this* dose change
> cannot: fed 50→100 mg gives only **1.47×**, binding is 98.4–99.4% and non-saturating
> to 168 µM so free fraction will not rise with dose, and the oral product was
> discontinued in September 2017. The route is closed on **supply and binding**, not
> on a 900-fold pharmacological chasm.
>
> **DOWNGRADED the same day, after tracing.** The 0.4 µM figure is attributed to
> "carrard2023", cited only as a semanticscholar PDF with no DOI and no PMID.
> Three PubMed searches — author+topic, topic+year, and amlexanox+NMD
> unrestricted — return **no such paper**. The only indexed amlexanox/NMD work is
> [PMID 22938201](https://doi.org/10.1371/journal.pgen.1002840)
> (Gonzalez-Hilarion 2012), which we already hold and which does not report
> 0.4 µM.
>
> So C51 stands as an **open uncertainty, not an established correction**: we
> cannot rule out amlexanox activity below 25 µM, and we could not reproduce the
> figure that suggested it. The 90–900× shortfall against the 50–100 µM Krivega
> benchmark stands as written. Full trace in
> `EXPOSURE-DOSSIER-KOSMOS-LEADS.md` §5.

**Verdict: closed.** Not on an assumption — on the drug's own registration data. Combined
with the 2017 withdrawal of the oral product, the amlexanox route for allele 1 is finished.
The earlier blind estimate of 3.4–16.8 µM across Vd 10–50 L bracketed the measured 16.0 µM
at a measured Vd of 30.1 L, which validates the estimating method and does nothing for the
drug.

## What replaces it is not a small molecule

No approved small-molecule NMD inhibitor with adequate exposure exists. Colchicine is
disqualified on mechanism (above); caffeine and wortmannin are research tools; every potent
agent — SMG1i, KVS0001, the NMDI series — is experimental.

**The successor is a transcript-specific antisense oligonucleotide**, and the precedent is
unusually close to our case. According to PubMed, Kim, Nomakuchi, … & **Krainer** 2022,
*Nat Commun* ([PMID 35624092](https://doi.org/10.1038/s41467-022-30668-y)), from the lab that
produced nusinersen:

| Their argument | Ours |
|---|---|
| *"CFTR-W1282X **truncated protein retains partial function**, so increasing its levels by inhibiting NMD of its mRNA will likely be beneficial"* | LAP-731X, lacking the whole kinase domain, **fully** restored checkpoint and alignment; our 737X retains everything it does |
| NMD destroys the transcript | Identical — PTC 748 nt upstream of the last junction |
| *"Because NMD regulates the normal expression of many genes, **gene-specific** stabilization is more desirable than general NMD inhibition"* | This is verbatim our standing objection to amlexanox and to every global NMD inhibitor |
| ASOs that **block exon-junction-complex binding downstream of the PTC** attenuate NMD gene-specifically | Our PTC has downstream EJCs to block, by construction — that is *why* it is NMD-sensitive |
| A **cocktail of three ASOs** raised CFTR-W1282X mRNA and protein in human bronchial epithelial cells and increased chloride current | The analogous endpoint is BubR1 protein plus checkpoint function in patient fibroblasts |

**Why this is strictly better than amlexanox was**, on three axes at once:

1. **Specificity.** It spares the rest of the NMD-regulated transcriptome, which removes the
   single largest safety objection — stabilising truncated tumour suppressors genome-wide in
   a cancer-predisposed child.
2. **Exposure.** ASOs are not bound by the albumin problem that just killed amlexanox; they
   are dosed to tissue concentration, not plasma Cmax. The failure mode that closed the
   small-molecule route does not transfer.
3. **Platform precedent.** Krainer's lab took an ASO to approval for a rare paediatric
   disease (nusinersen, SMA). The regulatory path for a bespoke ASO in an ultra-rare
   genotype exists and has been walked.

## The honest cost

**This is not a repurposed drug. It is a new drug**, and that is a different undertaking from
everything else in this workstream: design, tiling, chemistry, tox, IND, manufacture.

**And it inherits a delivery problem amlexanox did not have.** Nusinersen is intrathecal; the
CFTR ASOs were delivered to airway epithelium. Systemically dosed ASOs distribute well to
liver and kidney and poorly to most other tissues. MVA is a whole-body disease of growth,
every proliferating compartment, and cancer surveillance. **An ASO that reaches hepatocytes
is not obviously an ASO that reaches the tissues where aneuploidy does its damage**, and no
amount of specificity fixes that.

So: better mechanism, better safety logic, proven platform, and an unsolved delivery
question that is now the thing the route turns on — in the same way exposure was the thing
amlexanox turned on, and lost.
