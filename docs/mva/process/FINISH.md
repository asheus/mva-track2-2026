# Finishing the submission — 5 days out

Everything scientific is done, committed and reproducible. What remains is mechanical and
only you can do it. In priority order.

## 1. Publish the public repo (HARD REQUIREMENT for Track 2)

Rebuild and publish in one go from a fresh session:

    python3 docs/mva/export_public.py --out /tmp/mva-public
    python3 docs/mva/audit_export.py /tmp/mva-public      # must print 11/11 pass
    cd /tmp/mva-public && git init && git add -A && git commit -m "MVA Hackathon 2026 Track 2 submission"
    git remote add origin <new-public-repo-url> && git push -u origin HEAD

**354 files, 83 MB** on a clean build, CC BY 4.0, no patient data, no git history from this repo.
(Was "223 files, 19 MB"; SUBMIT-RUNBOOK.md separately said 178. Both were stale, and
two documents disagreeing meant the count could no longer catch the omission class it
was written for — which is exactly how 23 broken scripts and a missing tests/ tree
shipped unnoticed. Re-measured 23 Oct 2026 from a clean build.) Re-run the
audit against the **published** tree too: the point of C24 was that the export is what
ships, not the working copy.

## 2. Record the video

`VIDEO-SCRIPT.md`, 444 spoken words, 2:52 at 155 wpm against a hard 3:00 limit. Four
on-screen numbers only: **35×**, **0.952 (n = 5 vs 25) / 0.364 (n = 3 vs 11)**, **0 of 757**,
**59.6 → 88.9**. The AUC never appears without its n.

Say "hypothesis for follow-up", never "treatment". Deliver the three failures flat — they
are the strongest evidence of method, not damage control.

## 3. Declare the plan/tier and LLM data handling on the form

Required by the rules. State the provider, the plan, and that no challenge data left the
environment.

## 4. Diarise the deletion email

Confirm deletion to **`cnb@sagebase.org` by 23 Nov 2026** (settled 23 Oct 2026 by
organiser announcement; it is neither of the two addresses previously on file). **This
releases the prize money** — prizes are held until the confirmation is received and tax
documentation and sanctions screening are complete.

---

## What to say the submission is

Not a treatment. The claim that survived every test we ran at it:

> A variant-eligibility map for a gene with no functional data should state its own
> operating characteristics. We measured ours against 946 assayed splicing outcomes on a
> sealed split — sensitivity 0.392 and specificity 0.986 at the confident tier, 0.793 and
> 0.872 at the screening tier, precision 0.48 and 0.17 at the rate these variants actually
> occur. Both visible competitor submissions declined to calibrate at all.

## What NOT to claim

- **Not** that allele 2's abundance is established. C43: the buried-charge axis fails to
  transfer to BUB1B's own labelled variants (OR 5.76, p = 0.1193), and AlphaMissense fails
  its direction check on this protein, so N1002K's 0.9229 is **not evidence**.
- **Not** that the map finds non-canonical mechanisms ClinVar missed. Deep intronic
  evidence is still **n = 1**, unchanged across three expansions.
- **Not** a cure, and not a treatment recommendation. `COUNTER-ARGUMENT.md` concedes
  surveillance dominates every therapeutic idea here, and that the in-syndrome record is
  one-sided against system-level intervention.

## The one experiment worth handing over

**N1002K vs N1002S vs wild-type**, ectopic LAP-BubR1, abundance by western. Serine is the
mechanism's own predicted-tolerated substitution at the same residue and the only one of 19
AlphaMissense does not call likely-pathogenic. If K is low and S is normal, the mechanism
holds and abundance is the right axis. If both are low, position 1002 is intolerant for
reasons our mechanism does not capture and the abundance framing is wrong.

A same-residue control holds position, burial and neighbourhood fixed and varies only the
chemistry. It is the sharpest falsifiable test this work produced, and it is cheap.
