# 3-minute pitch video — script

**Audience:** researchers, clinicians and **patient advocates**. Pre-recorded, **no live
Q&A** — so this has to stand alone and answer the obvious objection before it is asked.

**Length is a hard constraint and this script is budgeted to it.** Read at **158 wpm** (468 words = 2:58); the named cuts below take it to 444, which is 2:55 at 152.
Per-slide second budgets below total 177 s; the deck is 13 slides.

Rewritten 24 Oct 2026 against the final 13-slide deck, which is organised as a problem
statement, four questions, and the answers in order. Earlier drafts are superseded.

**What wins here:** not the drug name — the panel will hear drug names from every team.
What they will hear rarely is a team that posed its questions first, ruled things out
quantitatively, reported the result that went against it, and named the one experiment
that would kill its own pick.

**If the read comes in slow, cut in this order** (−24 words, buys ~10 s): in §8 the
clause *"and the whole up-regulating universe holds no phosphatase at all"*; in §12 the
sentence *"Delivery is the unsolved half."* Never cut §7 or §11.

Re-count: `awk '/^> /{gsub(/^> /,"");n+=NF}END{print n}' VIDEO-SCRIPT.md`

---

### 1 · Title — 11 s
> Every cell-cycle drug in clinical use was built to break the cell cycle. Not one was
> built to make it work better. Oncology paid for all of it. This is a case for one child
> who needs the opposite.

### 2 · The problem — 15 s
> Every cell division can get the chromosome count wrong. Each chromosome must grip both
> poles, and of the four ways it can attach, three are wrong. A checkpoint holds the cell
> until every one is right. In this child that checkpoint is weak.

### 3 · The questions — 16 s
> We answered four questions in order. What do these two alleles leave behind. Is the
> deficit reversible. Is there any drug that raises BubR1 or its phosphatase. And if not,
> what else sits on the same node, at what dose.

### 4 · The alleles — 13 s
> Leucine 737 to a stop, seven hundred and forty-seven nucleotides upstream of the last
> junction, far past the fifty-five rule, so that transcript is destroyed. Asparagine 1002
> to lysine, eighty-seven percent buried — made, then degraded.

### 5 · Scalability — 13 s
> We scored every BUB1B allele the same way: consequence, the fifty-five-nucleotide rule,
> two predictors, then the literature for abundance. Suijkerbuijk reached the same two
> classes experimentally.

### 6 · The mechanism — 15 s
> A kinase writes a mark, a phosphatase erases it. Plk1 puts three phosphates in BubR1's
> KARD, and those phosphates are the docking site for PP2A-B56. BubR1 is not a kinase —
> it is the delivery vehicle. Both alleles converge on that one failure.

### 7 · It is reversible — 16 s
> We are not guessing. Suijkerbuijk took patient cells of exactly this shape — one
> truncating allele, one missense — and put BubR1 back. Checkpoint arrest doubled;
> controls did not move. But it doubled from fifteen percent of normal to thirty-one, and
> no drug raises BubR1.

### 8 · Rigor — 16 s
> So we tried everything that could. Readthrough, NMD inhibition, chaperones,
> degradation, binding BubR1 directly, activating PP2A. Across a hundred thousand curated
> drug-target pairs nothing raises it, and the whole up-regulating universe holds no
> phosphatase. Every arm died needing more drug than a person can be given.

### 9 · How we worked — 12 s
> Several evidence engines generated hypotheses. One human chose what to test. No claim
> rests on a single paper, and fifty-three numbered corrections are in the repository.

### 10 · The answer — 16 s
> If the phosphatase cannot be raised, lower the kinase it opposes. Barasertib. Aurora B
> at zero-point-three-seven nanomolar, thirty-seven-hundred-fold selective. Human steady
> state, total drug, sits twelve hundred times the biochemical IC-fifty; even at ninety-
> nine percent protein binding it is still twelvefold above. It is the only candidate
> needing a dose decrease, not an increase.

### 11 · The dose — 15 s
> And the dose is the hypothesis, so we commit to it. One to five nanomolar free,
> titrated in the child's own fibroblasts to thirty to fifty percent loss of Aurora B
> substrate phosphorylation. Never ablation. And we score missegregation, not alignment,
> because better alignment can hide worse segregation.

### 12 · The moonshot — 12 s
> A 2025 Nature Biotechnology method makes translation programmable: a separate capped
> RNA hands the ribosome a start codon of our choosing, on the native message. Delivery
> is the unsolved half. That is the general answer to every dosage disease.

### 13 · Close — 7 s
> One prediction: partial Aurora B inhibition rescues congression before it costs
> checkpoint competence. If it does not, we are wrong.
