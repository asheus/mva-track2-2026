#!/usr/bin/env python3
"""Pangolin across every non-coding BUB1B variant. Resumable, control-gated.

    python3 -m scripts.mva.nmd.pangolin_sweep --submit      # spends Neurosnap credits
    python3 -m scripts.mva.nmd.pangolin_sweep               # collect / re-parse only

WHAT THIS IS FOR. Our therapeutic thesis is "raise the BubR1 the patient still makes".
That is only coherent for a patient who makes some. A variant-level call of
null-vs-makes-protein is therefore a THERAPEUTIC ELIGIBILITY call, not merely a
diagnostic one -- the same thing Fabry's amenability table does for migalastat, for a
gene that has no such table. This sweep supplies the non-coding half of that map.

DESIGN CONSTRAINTS, all learned the hard way in this repo:

  * ONE VARIANT PER JOB in the PAK6 overlap region (>= chr15:40,218,500). A multi-gene
    annotation breaks Pangolin's CSV writer and fails the entire job (C25a). Elsewhere
    batching is safe -- four splice variants in one job ran fine.
  * SMALL BATCHES anyway, so one bad variant costs one batch rather than the sweep,
    and a failed batch can be bisected.
  * POSITIVE CONTROLS IN EVERY BATCH. The 13 canonical splice donor/acceptor variants
    from ClinVar have a known mechanism. A sweep that does not flag them is broken, and
    without controls embedded a silent failure looks like a clean negative result.
  * RESUMABLE, keyed on the VARIANT not the job: a re-run replans only variants that
    carry no score yet, so a failed job retries and a corrected plan does not misalign
    against the archive. Each job's raw output is archived as it lands, so a crash or a rate
    limit costs the current job and not the sweep.
  * NEVER PIPE PROGRESS THROUGH tail/head. It buffers until completion and the run
    looks hung -- cost us a false alarm on the verification step.
"""
import argparse
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[5]
IN = ROOT / "docs/mva/data/nmd/clinvar_noncoding_verified.tsv"
ARCHIVE = ROOT / "docs/mva/data/nmd/pangolin_sweep.jsonl"
OVERLAP_FROM = 40217428
BATCH = 25
DISTANCE = 50          # Pangolin default; matches the committed reference run
SERVICE = "Pangolin RNA Splicing Prediction"
BASE = "https://neurosnap.ai/api"
# Reference values from pangolin_splice_scores.csv -- the sweep must reproduce these.
KNOWN = {
    (40196779, "G", "A"): ("c.1288+5G>A", 0.49, -0.73),
    (40200239, "A", "G"): ("c.1402-5A>G", 0.85, -0.69),
    (40212488, "A", "G"): ("c.2386-11A>G", 0.76, -0.71),
    (40206459, "G", "A"): ("c.2009+1G>A", 0.73, -0.89),
}


def hdr():
    import os
    k = os.environ.get("NEUROSNAP_API_KEY")
    if not k:
        sys.exit("NEUROSNAP_API_KEY is not set in this process's environment.")
    return {"X-API-KEY": k}


def load():
    lines = IN.read_text().strip().split("\n")
    cols = lines[0].split("\t")
    return [dict(zip(cols, L.split("\t"))) for L in lines[1:]]


def plan(rows, scored=frozenset()):
    """Batch the safe region, solo the overlap, and seed controls into each batch.

    `scored` is excluded from the DATA slots but not from the sentinel pool: a sentinel
    is a control copy whose job is to be re-measured, so it stays available for as long
    as the sweep runs."""
    controls = [r for r in rows if r["consequence"].startswith("splice_")]
    # Every variant is scanned exactly once as data; sentinels are ADDITIONAL copies
    # appended to each batch, so a sentinel appears in its own data batch too. That is
    # intentional -- it gives an internal replicate of the same call.
    pending = [r for r in rows
               if (int(r["pos"]), r["ref"], r["alt"]) not in scored]
    safe = [r for r in pending if int(r["pos"]) < OVERLAP_FROM]
    solo = [r for r in pending if int(r["pos"]) >= OVERLAP_FROM]
    jobs = []
    # Only the four variants with COMMITTED reference scores can serve as sentinels:
    # a control whose expected value we do not already hold proves nothing. The other
    # nine canonical splice variants are scanned as ordinary data.
    sentinels = [c for c in rows
                 if (int(c["pos"]), c["ref"], c["alt"]) in KNOWN
                 and int(c["pos"]) < OVERLAP_FROM]
    if not sentinels:
        sys.exit("no reference-scored variant available as a sentinel -- refusing to "
                 "run a sweep with no verifiable control")
    for i in range(0, len(safe), BATCH):
        chunk = safe[i:i + BATCH]
        s = sentinels[(i // BATCH) % len(sentinels)] if sentinels else None
        jobs.append({"kind": "batch", "variants": chunk + ([s] if s else []),
                     "sentinel": (s["pos"] if s else None)})
    for r in solo:
        jobs.append({"kind": "solo", "variants": [r], "sentinel": None})
    return jobs, controls


def submit(variants):
    import requests
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    payload = "\n".join(f"{v['chrom']},{v['pos']},{v['ref']},{v['alt']}" for v in variants)
    enc = MultipartEncoder(fields={"Genome Assembly": "GRCh38",
                                   "Distance": str(DISTANCE), "Mask": "true",
                                   "Variants": payload})
    r = requests.post(f"{BASE}/job/submit/{SERVICE}",
                      params={"note": f"BUB1B non-coding sweep, n={len(variants)}"},
                      headers={**hdr(), "Content-Type": enc.content_type},
                      data=enc, timeout=300)
    r.raise_for_status()
    return r.text.strip().strip('"')


def collect(job_id, limit=900):
    import requests
    t0 = time.time()
    while time.time() - t0 < limit:
        s = requests.get(f"{BASE}/job/status/{job_id}", headers=hdr(),
                         timeout=60).text.strip().strip('"').lower()
        if s == "completed":
            r = requests.get(f"{BASE}/job/file/{job_id}/out/pangolin_output.csv",
                             headers=hdr(), timeout=120)
            r.raise_for_status()
            return "completed", r.text
        if s == "failed":
            return "failed", ""
        time.sleep(10)
    return "timeout", ""


def scored_keys():
    """Variants that ALREADY CARRY A SCORE, as (pos, ref, alt).

    Resume used to key on the job's position in the plan, which was wrong twice over.
    A FAILED job writes an archive row like any other, so its plan index counted as
    done and its variants were skipped on every later run -- 96 variants in four failed
    batches would have been dropped silently and the map would have reported them
    PENDING forever. And a plan index is positional, so correcting OVERLAP_FROM
    renumbers every job: index 50 in the new plan is a different job from index 50 in
    the archive, and resume would have skipped the wrong work.

    Both go away by keying on the variant instead of the job. The parser is imported
    from the report rather than copied, so "scored" means exactly one thing in this
    pipeline: a row the report would read a gain/loss out of.
    """
    if not ARCHIVE.exists():
        return set()
    from scripts.mva.nmd.pangolin_sweep_report import parse_rows
    out = set()
    # A row the multi-gene column shift ate is NOT scored even though its job completed
    # (C25b). parse_rows drops those, so they stay pending and get retried -- which is
    # the second thing a job-keyed resume could never do.
    for L in ARCHIVE.read_text().strip().split("\n"):
        if not L.strip():
            continue
        rec = json.loads(L)
        if rec.get("status") != "completed":
            continue
        good, _shifted, _rec = parse_rows(rec.get("raw") or "",
                                          rec.get("positions"))
        for pos, ref, alt, _gain, _loss in good:
            out.add((pos, ref, alt))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--submit", action="store_true", help="spend credits and run")
    ap.add_argument("--max-jobs", type=int, default=0, help="stop after N jobs (0 = all)")
    a = ap.parse_args()

    if not IN.exists():
        sys.exit(f"missing {IN}; run verify_refs.py first")
    rows = load()
    scored = scored_keys()
    jobs, controls = plan(rows, scored)
    if scored:
        print(f"{len(scored)} variants already carry a score and are not replanned",
              flush=True)
    n_var = sum(len(j["variants"]) for j in jobs)
    print(f"{len(rows)} verified variants -> {len(jobs)} jobs "
          f"({sum(1 for j in jobs if j['kind']=='batch')} batched, "
          f"{sum(1 for j in jobs if j['kind']=='solo')} solo), "
          f"{n_var} variant-slots incl. sentinels", flush=True)
    print(f"{len(controls)} canonical splice controls; "
          f"{len(KNOWN)} have committed reference scores to reproduce", flush=True)

    if not a.submit:
        print("\ndry run. re-run with --submit to spend credits.")
        return 0

    if not jobs:
        print("\nnothing pending -- every variant already carries a score.")
        return 0
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    ran = 0
    with ARCHIVE.open("a") as out:
        for idx, j in enumerate(jobs):
            if a.max_jobs and ran >= a.max_jobs:
                print(f"\nstopping at --max-jobs {a.max_jobs}", flush=True)
                break
            try:
                jid = submit(j["variants"])
            except Exception as e:
                print(f"  job {idx:4d} SUBMIT FAILED: {type(e).__name__} "
                      f"{str(e)[:120]}", flush=True)
                time.sleep(5)
                continue
            status, csv_text = collect(jid)
            rec = {"plan_index": idx, "kind": j["kind"], "job_id": jid,
                   "status": status, "n_variants": len(j["variants"]),
                   "positions": [v["pos"] for v in j["variants"]],
                   "sentinel": j["sentinel"], "raw": csv_text}
            out.write(json.dumps(rec) + "\n")
            out.flush()
            ran += 1
            print(f"  job {idx:4d}/{len(jobs)} {j['kind']:5s} n={len(j['variants']):2d} "
                  f"{status}", flush=True)
            time.sleep(1)
    print(f"\n{ran} jobs this run; archive -> {ARCHIVE.relative_to(ROOT)}")
    print("parse with: python3 -m scripts.mva.nmd.pangolin_sweep_report")
    return 0


if __name__ == "__main__":
    sys.exit(main())
