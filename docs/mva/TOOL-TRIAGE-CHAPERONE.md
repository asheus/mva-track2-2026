# Triage: RosettaCommons/Chaperone — not for this problem

**Verdict: no.** It is a real and serious piece of work, and it answers a different kind of
question than ours.

*Assessed 21 Oct 2026 from the PDF itself, downloaded and read in an isolated directory.*

## What it is

**"Reliable and Efficient Agentic Protein Design with Toolset Harnessing"** — Butcher,
Chen et al., Institute for Protein Design, University of Washington (David Baker
corresponding; Neil King co-author). 21 pages, dated **19 Oct 2026**.

Chaperone is an **agent harness for de novo protein design**. It gives an LLM agent a
DataFrame-based interface over RFdiffusion3, AlphaFold3, ProteinMPNN, LigandMPNN and
50+ other tools, with parallel execution on HPC. Reported results: **86% fewer tokens, 64%
lower GPU cost** than baseline agents, low-nanomolar cortisol binders designed zero-shot in
a two-week campaign, a symmetric 12-subunit nanoparticle, and a crystalline-assembly linker.

## Why it does not fit

**1 · It designs new proteins. We need to score an existing one.**
Our open question is whether p.Asn1002Lys destabilises BubR1 — a **stability prediction**
about a point substitution. Searching the full text: **zero occurrences** of `ddG`,
`stability predict`, `point mutation`, `variant effect`, or `thermostab`. The toolset is
generative (RFD3, AF3, ProteinMPNN, LigandMPNN), not a variant-effect predictor. It is not
that Chaperone would do our job badly; it does not contain our job.

**2 · The one adjacent use needs a structure that does not exist.**
RFD3 could in principle design a **protein binder** that clamps and stabilises the
pseudokinase domain. But binder design needs a reliable target structure, and we
established there is **no experimental structure of BUB1B 766–1050 above 3.8 Å** — only
cryo-EM of the whole MCC. Designing against a low-confidence model of an unsolved domain is
precisely where this class of method fails.

**3 · Its output fails our own viability gate, harder than anything on the list.**
A de novo designed protein binder has no route to this child. We removed trans-splicing
from first place for having no molecule in a human; a designed binder is further from a
patient than that.

**4 · The infrastructure is not here.** Their agents ran with up to **five GPUs on a SLURM
cluster** for 12-hour autonomous sessions. This container has four CPU cores.

**5 · The timeline is wrong by an order of magnitude.** Their demonstration was a
**two-week** end-to-end campaign.

## The one useful thing it surfaces — a naming collision worth noticing

We have been pursuing a **pharmacological chaperone**: a small molecule that binds BubR1 and
stabilises its fold, as migalastat does for α-galactosidase A. This tool is *called*
Chaperone and does something close to the opposite — RFD3's small-molecule work designs a
**protein that binds a small molecule** (their cortisol binder), not a small molecule that
binds a protein.

What we would actually want from this corner of the field is a **ΔΔG predictor** — Rosetta
`cartesian_ddG`, FoldX, or ThermoMPNN — which would compute predicted stability changes for
**N1002K vs N1002R vs N1002S** and give a computational reading of the discriminator we
have been saying requires a bench. That is a genuinely different tool from this one, and it
is the right thing to have asked for.

## And the priority call, which matters more than the tool

**Computation is no longer the bottleneck for this submission.** The remaining blockers are
human-only: publishing the public repository (a hard Track 2 requirement), recording the
three-minute video, declaring the LLM plan and data handling, and diarising the deletion
email. Opening a new computational thread now — any new thread — competes with those for
the time that is left.

A ΔΔG run would be the right *next* piece of science. It is not the right next piece of
work before the deadline.
