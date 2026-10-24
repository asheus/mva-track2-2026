# Review Room — session 01

**Target:** `TRACK2-REPORT.md`, the Track 2 deliverable.
**Run:** 23 Oct 2026, `review-provenance` seat only (built first, run first).
**Outcome:** one finding, which changed a shipped claim. Logged as **C47**.

## What was built

A scientific adaptation of `roast-room` (MIT, github.com/nateherkai/roast-room), which
seats twelve simulated public figures to debate a business decision. Kept: the chair,
the ruin-risk cap, the forced argument on premature consensus, and the mechanical
grounding check. Replaced: the personas.

**Personas do not transfer to science.** They are not citable in a methods section, they
lend borrowed authority to reasoning that has not earned it, and simulating named living
scientists to critique a real child's care would be unusable even if it were accurate.
So a seat here is a **methodological jurisdiction with a veto and a named failure
history** — one seat per class of error this project actually produced, each citing the
correction that motivates it. Seven seats, listed in
`.claude/skills/review-room/SKILL.md`.

The seat that did not previously exist is `review-record`, whose jurisdiction is
fidelity to the primary clinical document. A fabricated phenotype survived three
documents and every automated pass because every instrument pointed at genomics and
literature and none at the record describing the child
(`PHENOTYPE-GROUNDING.md`).

## The finding

`check_grounding.py` flagged `17 of 18 (94%)` and `94%` as quantitative claims with no
grounding token anywhere near them. Both are load-bearing: the first is the magnitude
evidence for the HSP70/HSF1 axis, the second is 4-PBA's "magnitude precedent" cell in
the verdict table.

Tracing it found the number **exactly correct** — Singh 2010, verbatim — and the
**inference wider than the source**: the rescues came from ethanol, proteasome
inhibitors and a yeast deletion, and Hsp70 induction is "necessary but not sufficient."
We had transferred that magnitude to arimoclomol, an HSF1 co-inducer. Full reasoning in
**C47**.

This is the finding shape worth naming: **a true number supporting a conclusion it does
not license.** Checking that a citation exists is not checking that it establishes the
claim.

## What the screen is, honestly

It is a screen. It matches grounding tokens near a claim and never reads the source.

**Its headline percentage is not reportable**, and finding that out was the second
useful result of the session. On this file:

| `--window` | ungrounded |
|---|---|
| 3 | 48/60 (80%) |
| 6 | 37/60 (62%) |
| 12 | 19/60 (32%) |
| 25 | 7/60 (12%) |

The rate is dominated by a free parameter chosen arbitrarily. "80% of the report's
claims are ungrounded" was one `--window` default away from being stated, and it would
have been alarming and false — C46's failure mode, reproduced inside the instrument
built to prevent it. **Use the stable core instead:** run at a generous window and work
the claims that still flag. At `--window 25` seven survive; one of them was C47.

Its selftest reports 100% sensitivity and 100% specificity on a 10-case panel. That is
near-meaningless: the same author wrote the regex and the panel. It is printed so the
number can never be mistaken for validation.

## Not yet run

Six seats are defined but unrun: `direction`, `basis`, `completeness`,
`reproducibility`, `record`, `safety`. The `record` and `safety` seats are the ones
most likely to find something, since `record` covers the class that has already
produced the project's worst error and `safety` holds the only veto.
