# Exposure dossier — the Kosmos leads, worked the way amlexanox was worked

24 Oct 2026. Every candidate surfaced by `TRIAGE-KOSMOS-HACKATHON.md` taken to a
measured human free Cmax and compared against the concentration at which its
effect is actually reported. Supply, marketing status and formulation are
deliberately ignored — this asks only whether the drug can reach its target in a
human at a tolerated dose.

Method is the one that closed amlexanox: **measured** total Cmax from a
registration document or label, **measured** plasma protein binding, free
Cmax = total × fu, compared against the reported active concentration and
against the drug's *other* targets. Predicted binding is labelled as predicted
and never used to clear a candidate.

---

## 1 · Perphenazine — CLOSED, and the originating lab closed it first

The most on-mechanism approved drug in the whole search: a genuine PP2A
activator, and PP2A-B56 is where both of this child's alleles converge. Kosmos
named it and set it aside without arithmetic. Here is the arithmetic.

**Target engagement.** Perphenazine binds the PP2A Aα scaffolding subunit;
knockdown of PP2A subunits attenuates its activity, so the mechanism is real
(Gutierrez 2014, [PMID 24401270](https://doi.org/10.1172/JCI65093)).

**Exposure.** US prescribing information, steady state:

| | |
|---|---|
| total Cmax | **984 pg/mL** (43% CV) |
| MW | 403.97 |
| **total Cmax, molar** | **2.44 nM** |
| plasma protein binding | "highly bound" — **no published percentage** |
| free Cmax @ 98% bound | **~0.05 nM** |

**The gap.** Phenothiazine PP2A activation is reported in the low-micromolar
range. Even at the most generous plausible figure:

| assumed active conc. | gap on **total** drug | gap on free @98% |
|---|---|---|
| 1 µM | **411×** | ~20,500× |
| 5 µM | **2,053×** | ~103,000× |
| 10 µM | **4,105×** | ~205,000× |

Note this closes on **total** drug alone — 411× short at the most favourable
assumption, before protein binding is applied at all. Binding only deepens it.
This is a far worse gap than amlexanox ever had.

**And the independent kill.** The Gutierrez group themselves state that
perphenazine inhibits dopamine D2 receptor in the basal ganglia, *"which causes
movement disorders at dosages less than those needed to kill T-ALL cells"* —
which is why they went looking for analogues without D2 activity. The
therapeutic window is **inverted**: the neurological toxicity arrives *before*
the PP2A effect. Same structural shape as amlexanox, where IKKε/TBK1 are hit
10–100× below the NMD range — the thing you want is the weakest thing the drug
does.

**The successor is worse.** The compound built to escape D2 liability — iHAP1,
Morita *et al.*, *Cell* 2020 — is **RETRACTED**
([PMID 32315619](https://doi.org/10.1016/j.cell.2020.03.051); PubMed article
type "Retracted Publication"). Nothing in that lineage can be cited.

**Verdict: closed on exposure, closed again on inverted window, and its
successor literature is retracted.**

## 2 · Penfluridol — CLOSED on unmeasurability

The other named PP2A activator (Wu 2019,
[PMID 31470848](https://doi.org/10.1186/s12929-019-0557-2); Chien 2015,
[PMID 25637283](https://doi.org/10.1016/j.molonc.2015.01.002)).

**There is no modern human pharmacokinetic dataset.** The only plasma-level
publication located is a 1975 gas-liquid chromatography method paper
([PMID 1140908](https://doi.org/10.1159/000468174)) which reports only that the
drug is still *detectable* seven days after 120 mg/week. No Cmax, no AUC, no
protein binding, no paediatric data.

Sources also **conflict on basic PK**: time-to-peak is given as ~2 hours in one
review and "several days" in another; half-life as 70 h or 2–5 days. A drug
whose Tmax is disputed by two orders of magnitude cannot carry an exposure
argument.

PP2A effects in the AML and pancreatic papers are reported in the micromolar
range, against which nothing can be compared because the human denominator does
not exist.

**Verdict: closed.** Not "insufficient evidence" — the measurement required to
evaluate it has never been made.

## 3 · Momelotinib — CLOSED on inverted selectivity

Kosmos's single best approved-drug lead: the only one of eight agents entering
the requested Aurora-B exposure band (R = 0.104–1.04).

**Exposure.** FDA label (OJJAARA, 200 mg = maximum recommended dose), steady
state:

| | |
|---|---|
| total Cmax | **479 ng/mL** (61% CV) |
| MW | 414.5 |
| total Cmax, molar | **1.156 µM** |
| plasma protein binding | **~91%** (measured, healthy volunteers) |
| **free Cmax** | **104 nM** |

This reproduces Kosmos's lower bound exactly (104 nM / 1 µM = 0.104), so their
arithmetic is sound. The problem is what the number sits next to.

**Free drug against every target, same scale:**

| target | IC50 | free Cmax / IC50 |
|---|---|---|
| ACVR1/ALK2 | 8.4 nM | **12.4** |
| JAK2 | 11 nM | **9.5** |
| JAK1 | 143 nM | 0.73 |
| TYK2 | 252 nM | 0.41 |
| JAK3 | 325 nM | 0.32 |
| Aurora B *(if 300 nM)* | 300 nM | 0.35 |
| Aurora B *(if 1 µM)* | 1000 nM | 0.10 |

**The structural objection.** To put *any* meaningful free drug on Aurora B you
must run **9–12× over the JAK2 and ACVR1 IC50s**. There is no dose at which
this drug is an Aurora B agent; there is only a dose at which it is a profound
JAK2/ACVR1 inhibitor that incidentally grazes Aurora B. In a child with a
cancer-predisposition syndrome and a prior rhabdomyosarcoma, chronic JAK2
blockade means chronic immunosuppression — removing immune surveillance from a
patient whose whole problem is arising transformed clones. The label's own
warnings are thrombocytopenia, anaemia, infections and hepatotoxicity.

**And the potency figure does not exist.** Kosmos flagged that its momelotinib
ratio used "single-point potency, not a fitted IC50." Confirmed: **no fitted
Aurora B IC50 for momelotinib could be located in the public literature.**
Vendor off-target panels list CDK2, JNK1, PKD and ROCK2 below 100 nM and do not
report Aurora B at all. The one approved drug that entered the band entered it
on a number nobody has measured.

**Verdict: closed.** Inverted selectivity, and the ratio that selected it rests
on an unmeasured potency.

## 4 · APC/C restraint — NOT closed on exposure, but the hazard is in its own source

Sansregret *et al.*, *Cancer Discov* 7(2):218–233, 2017
([PMID 28069571](https://doi.org/10.1158/2159-8290.CD-16-0645)) — Francis Crick,
Swanton lab. Traced and confirmed. The effect is real and the journal is
first-rank.

Exposure cannot be computed: proTAME, apcin and CP5V are research tools with no
human PK, and no approved drug does specific APC/C inhibition at achievable free
concentration. Under "supply is a later problem" this stays open as a *target*.

**But read the paper's actual thesis, which the Kosmos summary does not.** The
title is *"APC/C Dysfunction **Limits** Excessive Cancer Chromosomal
Instability."* The finding is that partial APC/C loss is how **tumours survive
their own instability** — and, in the authors' words, *"APC/C impairment caused
adaptation to MPS1 inhibitors, revealing a likely resistance mechanism to
therapies targeting the spindle assembly checkpoint."* Cancer somatic mutations
in the APC/C subunit **CDC27**, introduced by CRISPR, reduce segregation errors.

So the 90% → 34% rescue is real, and the state that produces it is a
**characterised cancer-driver adaptation**. Inducing it pharmacologically in a
child with a cancer-predisposition syndrome would install the exact tolerance
mechanism that lets an aneuploid clone survive what should kill it — and would
do so systemically, for life.

This does not close the route, but it reverses its sign for *this* patient and
it is the single most important thing the Kosmos report omitted. Any use of this
result must carry it.

**Verdict: mechanistically the best result in the project; oncologically the
most dangerous. Both, at once, from one paper.**

---

## 5 · Correction to C51 — the number that threatened our amlexanox closure cannot be found

C51 (`ALLELE1-APPROVED-DRUGS.md`) was raised because Kosmos cited "carrard2023"
for amlexanox NMD activity from **0.4 µM**, which would have made our free Cmax
only 1.4–3.6× short instead of 90–900×.

**That citation does not resolve.** Three PubMed searches — author+topic,
topic+year, and amlexanox+NMD unrestricted — return **no Carrard paper**. The
only amlexanox/NMD paper indexed is
[PMID 22938201](https://doi.org/10.1371/journal.pgen.1002840)
(Gonzalez-Hilarion 2012), which we already hold and which does not report
0.4 µM.

The cited source was a semanticscholar PDF link with no DOI and no PMID — the
exact failure mode the brief warned about ("an untraceable citation costs more
than a missing one").

**C51 is therefore downgraded, not withdrawn.** The possibility that amlexanox
has activity below 25 µM remains live and should be stated as an open
uncertainty; it is not established, and our 90–900× figure against the
50–100 µM Krivega benchmark stands as written. The honest position: *we could
not reproduce the 0.4 µM figure, and the source given for it does not resolve.*

---

## Where this leaves the drug search

Four of the five leads are closed on measured human numbers, and three of them
close for the **same structural reason**:

> In every case the effect we want is weaker than something else the drug does.
> Amlexanox hits TBK1/IKKε 10–100× below its NMD range. Perphenazine causes
> movement disorders below its PP2A range. Momelotinib inhibits JAK2 and ACVR1
> 9–12× before it touches Aurora B.

That is not three coincidences. It is what happens when you repurpose: a drug's
approved activity is, by construction, its most potent one, and the activity you
are borrowing is an off-target — which is to say, a weaker one. Repurposing into
a mechanism nobody optimised for means you are always fighting the drug's own
potency ranking.

**And this effect has been measured at population scale, independently of us.**
Gero's `ct-validation` benchmark (Kostiuk *et al.*, *Bioinformatics*, 20 Oct
2026, [PMID 42900515](https://doi.org/10.1093/bioinformatics/btag788)) finds
that pooling open clinical-trial registries compresses relative success from
~2.9 to **RS = 1.52**, with the loss *"primarily driven by the breadth of the
indication data rather than the genetic evidence"* — that is, by indications
listed for exploratory and **repurposing** trials, which are promiscuously
registered and progress at lower rates. Our three closures are the mechanistic
account of a penalty they quantified across ~2.2 million target–indication
pairs. See `GERO-CT-VALIDATION.md`.

Which is the same finding as the pitch opener, arrived at from the other end.
The pharmacopoeia was not built facing this direction, and the exposure
arithmetic is where that shows up as a number.

The one route that does not fail this way is **APC/C restraint** — because there
the molecule was built for the target. It fails differently, and worse: it
works, and the paper that proves it works also shows it is how tumours learn to
tolerate instability.
