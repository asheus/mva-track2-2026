# Submission runbook

Written 14 Oct 2026. **Deadline 24 Oct 2026, 23:59 UTC — 10 days.**

Everything that could be done without a human account is done. Four things remain
and all four need you. They are ordered so that nothing waits on anything else.

---

## 0. Before anything: rebuild and audit the export (2 minutes)

Never publish without both commands. The second exists because three defects reached
the export surface and none was visible by reading it (`CORRECTIONS-2026-10-06.md`, C24).

    cd /path/to/Phoenix
    python3 docs/mva/export_public.py --out /tmp/mva-public
    python3 docs/mva/audit_export.py  /tmp/mva-public

Expect `all checks passed — export is safe to publish` and **354 files, 83 MB** on a clean build (356 after the audit, which
itself leaves the two artefacts named below)
(re-measured 23 Oct 2026; the previous 178 and FINISH.md's 223 were both stale).

Note: the audit runs `verify_report` inside the export, which leaves a regenerated
`gate1.json` and `__pycache__/` behind. Delete both before `git add -A`, or the public
repo carries build artefacts:

    find <EXPORT> -name __pycache__ -type d -prune -exec rm -rf {} + If the audit
fails, stop; it names the file and the line.

---

## 1. Publish the public repository — **hard requirement, do this first**

Track 2 cannot be submitted without a GitHub URL, and the repo must be public after
close. It may stay private during the hackathon; publishing now is simpler and costs
nothing, since the audit has confirmed there is no patient data in it.

    cd /tmp/mva-public
    git init -b main
    git add -A
    git commit -m "MVA Hackathon 2026 — Track 2 submission"

Then create an empty repository on GitHub under your own account — **not** under an
organisation that could restrict visibility — and push:

    git remote add origin https://github.com/<you>/mva-hackathon-2026-track2.git
    git push -u origin main

Set the description to something a judge can parse in one line, e.g. *"Track 2 drug
repurposing for a child with compound-heterozygous BUB1B (MVA1) — report, six-gate
funnel, and 24 logged corrections."*

**Why a fresh repo and not a branch of this one:** git retains deleted text. A redacted
history leaks under `git log -S`. The export carries no history at all, which is the
only safe form. See `PUBLICATION-AUDIT.md`.

**Check after pushing:** open the repo in a logged-out browser window. If it 404s it is
still private.

---

## 2. Fill the plan/tier field — the only required field left

`METHODS-DESCRIPTION.md` §Q3 is the form's one mandatory question and wants
**provider + plan or tier + setting**. Provider and setting are filled in:

> Provider: Anthropic. Interface: Claude Code (cloud sessions on claude.ai/code).
> Setting: commercial terms, no training on customer content.
> **Plan or tier: ⚠️ TO BE FILLED IN BY THE TEAM**

Replace that line with your actual plan. It is a fact about your account, not about the
analysis, which is why it was left blank rather than guessed. One line, then this
document is complete.

---

## 3. Record the video — the only item with irreducible human cost

`VIDEO-SCRIPT.md` is final and **measured**: 450 spoken words, 2:54 at 155 wpm against
a hard 3:00 limit. Read at 155–160, not slower. The script names the two clauses to cut
if your read comes in long.

Four on-screen numbers, nothing else: **35×**, **0.952 (n = 5 vs 25) / 0.364 (n = 3 vs 11)**, **0 of 757**,
**59.6% → 88.9%**.

Before recording, re-check that no number drifted:

    sed -n 's/^> //p' docs/mva/VIDEO-SCRIPT.md | wc -w     # expect 444
    grep -c '^## C' docs/mva/CORRECTIONS-2026-10-06.md     # expect 24

Upload to YouTube or Vimeo. **Unlisted is fine; private is not** — the judges have to be
able to open it. Paste the URL straight into the form; do not shorten it.

---

## 4. Submit, keeping slots in reserve

Three Track 2 submissions are allowed and **only the latest is reviewed**. So submit as
soon as 1–3 are done, and keep two slots for corrections.

| Field | Value |
|---|---|
| Display / team name | yours |
| GitHub URL | from step 1, must start with `https://github.com/` |
| Video URL | from step 3 |
| Report file | `mk7790_track2_report.md` — at the root of the export, already named for the account |

**Track 1 is scored separately and the answer is already in hand.** Submit it too:
`docs/mva/data/track1_submission.csv`, one row, compound-heterozygous pair. It costs one
upload and is independently ranked. On the incidental-findings field, the honest answer
is *not assessed* rather than *none* — the cascade surfaced 30 other genes with rare
biallelic-compatible damaging calls and deliberately did not look at them.

---

## 5. After close: the deletion email — diarise it now

The DTA requires written confirmation that all challenge data is deleted within 30 days
of close, from every environment including notebooks, cloud instances, private repos and
derived datasets. *"If you do not contact us, we may contact you directly in 30 days."*

**SETTLED 23 Oct 2026: send it to `cnb@sagebase.org`, by 23 Nov 2026.** An organiser
announcement gave the address directly. It is **neither** of the two we had on file
(`RarediseaserealkidMVAhackathon2026@synapse.org`, rules page;
`MVAHackathon2026@synapse.org`, dataset card), so the earlier "address it to both"
workaround would have reached nobody. Send to `cnb@sagebase.org`; copying the other two
costs nothing if you want belt and braces.

**It gates payment.** Prizes "are released once this confirmation is received and any
required tax documentation and sanctions screening are complete." Treat it as the last
deliverable of the project, not an afterthought.

What is already true, and worth stating in that email: the VCF and the clinical
phenotype document are deleted, gitignored, and blocked by name in the exporter; what is
committed is the query, never the data. The one residual is any copy in your own local
clones and any cloud session container — those die with the container, but say so
explicitly rather than implying it.

Put a calendar entry at **close + 7 days**, not close + 29.

---

## What is NOT on this list, and why

- **No further science.** The report is final on every number. The corrections ledger is
  closed at 24.
- **No new analysis to strengthen the submission.** Ten days is enough time to break
  something; the verifier and the export audit are the only things that should run again.
- **Do not reshare the data** in any form, through any channel, including to a teammate
  who has not separately accepted the terms.
