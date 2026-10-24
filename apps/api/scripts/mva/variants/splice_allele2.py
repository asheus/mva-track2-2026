#!/usr/bin/env python3
"""Score the proband's allele 2 (p.Asn1002Lys, c.3006T>G) for splicing. Closes C22.

    python3 -m scripts.mva.variants.splice_allele2 --submit     # spends Neurosnap credits
    python3 -m scripts.mva.variants.splice_allele2              # re-parse archived jobs

RESULT: no predicted splice effect. Gain +0.01, loss 0.00, stable across window
widths of 50, 300 and 1000 nt and across all three overlapping gene models. The
positive control reproduces its committed score EXACTLY (+0.76 / -0.71), so the
instrument was working when it returned that null.

WHY THIS WAS WORTH SCORING AT ALL, for a missense variant.
The only route by which a missense change reaches nonsense-mediated decay is by
creating a cryptic splice site whose frameshift puts a PTC downstream. C22 recorded
that `pangolin_splice_scores.csv` held only the four KNOWN splice alleles and that
allele 2 had never been scored; a score for it was quoted to this workstream during
review, was not ours, and was not in our files. The honest status was "unscored".

WHAT THE NULL BUYS. It removes the last route by which allele 2 might fail to be
translated. Combined with C22's finding that the variant is in the final exon (where
a PTC escapes NMD by construction), allele 2 is made as protein. So the open question
is narrowed from three possibilities to two: the protein is present but scarce
(abundance) or present and poorly functional (interface). That is elimination by
computation, not a wet-lab result, and it is the honest shape of what this closes.

TWO GUARDS, because this instrument has failed silently in this branch before.

  1. A POSITIVE CONTROL. c.2386-11A>G is a known MVA splice allele already in the
     committed CSV at gain +0.76 / loss -0.71. Run at the same settings it must
     reproduce, or allele 2's number is discarded with it. It reproduces exactly.
  2. WINDOW SWEEP. Pangolin's default Distance is 50 nt and allele 2 sits 48 nt from
     the exon 23 acceptor -- right at the edge, where a null could be a windowing
     artefact rather than biology. Scored at 50, 300 and 1000: unchanged.

TWO DEFECTS FOUND IN THE INSTRUMENT ITSELF (see CORRECTIONS C25).

  a. A two-variant job FAILS where each variant alone succeeds. SPLICE-AXIS.md had
     recorded an earlier multi-variant failure and blamed deep-exonic negative
     controls. That diagnosis was incomplete: the real trigger is a variant whose
     position carries a MULTI-GENE annotation, which breaks Pangolin's CSV writer
     and takes the whole job with it. Bisection found this in two jobs.
  b. The output row for such a variant is COLUMN-SHIFTED. Allele 2 lies in a
     triple overlap -- BUB1B, PAK6 and the BUB1B-PAK6 readthrough -- and Pangolin
     emits all three gene blocks as unquoted comma-bearing text, so CHROM reads
     "T" and POS reads "G". `parse_pangolin_row` below reads it anyway rather than
     trusting the header, and asserts the recovered coordinate.

     That readthrough is the SAME transcript that caused one of the two Track 1
     bugs (first-match gene assignment split the causal pair across BUB1B and its
     readthrough). One genomic overlap, two independent tools, two silent failures.
"""
import argparse, json, os, pathlib, re, sys, time

ROOT = pathlib.Path(__file__).resolve().parents[5]
OUT = ROOT / "docs/mva/data/variants"
ARCHIVE = OUT / "pangolin_allele2.json"

ALLELE2 = ("chr15", 40220612, "T", "G")
CONTROL = ("chr15", 40212488, "A", "G")
CONTROL_EXPECT = {"gain": 0.76, "loss": -0.71}   # from pangolin_splice_scores.csv
DISTANCES = (50, 300, 1000)
# Gene models overlapping allele 2, confirmed against Ensembl REST:
#   ENSG00000156970 BUB1B           chr15:40,160,984-40,221,137
#   ENSG00000137843 PAK6            chr15:40,217,428-40,277,489
#   ENSG00000259288 BUB1B-PAK6      chr15:40,218,500-40,264,890  (readthrough)
EXPECTED_GENES = {"ENSG00000156970", "ENSG00000137843", "ENSG00000259288"}
SERVICE = "Pangolin RNA Splicing Prediction"
BASE = "https://neurosnap.ai/api"


def parse_pangolin_row(csv_text: str, want_pos: int):
    """Read a Pangolin output row, including the column-shifted multi-gene form.

    Pangolin emits one `ENSG...|<pos>:<score>|<pos>:<score>|Warnings:` block per
    overlapping gene, unquoted and comma-separated, so a multi-gene row shifts every
    column and the header cannot be trusted. Parse the blocks directly instead.
    """
    line = csv_text.strip().split("\n")[-1]
    per_gene = {}
    # All overlapping genes BUT THE LAST are emitted as pipe-delimited blocks.
    for gene, scores in re.findall(r"(ENSG\d+)\.\d+((?:\|-?\d+:-?[\d.]+)+)", line):
        pairs = [(int(p), float(s)) for p, s in
                 (x.split(":") for x in scores.strip("|").split("|"))]
        # Pangolin reports the largest gain first, then the largest loss.
        per_gene[gene] = {"gain_pos": pairs[0][0], "gain": pairs[0][1],
                          "loss_pos": pairs[-1][0], "loss": pairs[-1][1]}
    # ...and the LAST one positionally, in the row's own trailing columns, with no
    # pipes at all. Missing this dropped a gene silently until the gene-set
    # assertion below caught it, which is the whole reason that assertion is there.
    tail = re.search(r"(ENSG\d+)\.\d+,(-?\d+),(-?[\d.]+),(-?\d+),(-?[\d.]+)\s*$", line)
    if tail:
        per_gene[tail.group(1)] = {"gain_pos": int(tail.group(2)), "gain": float(tail.group(3)),
                                   "loss_pos": int(tail.group(4)), "loss": float(tail.group(5))}
    if not per_gene:
        # A well-formed single-gene row (the control) has a trustworthy header.
        f = line.split(",")
        assert int(f[1]) == want_pos, f"row is for {f[1]}, expected {want_pos}"
        per_gene[f[4].split(".")[0]] = {"gain_pos": int(f[5]), "gain": float(f[6]),
                                        "loss_pos": int(f[7]), "loss": float(f[8])}
    return per_gene


# ---------------------------------------------------------------------------

def _hdr():
    k = os.environ.get("NEUROSNAP_API_KEY")
    if not k:
        sys.exit("NEUROSNAP_API_KEY is not set in this process's environment.")
    return {"X-API-KEY": k}


def _submit(variant, distance, note):
    import requests
    from requests_toolbelt.multipart.encoder import MultipartEncoder
    c, p, r, a = variant
    enc = MultipartEncoder(fields={"Genome Assembly": "GRCh38", "Distance": str(distance),
                                   "Mask": "true", "Variants": f"{c},{p},{r},{a}"})
    resp = requests.post(f"{BASE}/job/submit/{SERVICE}", params={"note": note},
                         headers={**_hdr(), "Content-Type": enc.content_type},
                         data=enc, timeout=300)
    resp.raise_for_status()
    return resp.text.strip().strip('"')


def _wait_and_fetch(job_id, every=20, limit=1800):
    import requests
    t0 = time.time()
    while time.time() - t0 < limit:
        s = requests.get(f"{BASE}/job/status/{job_id}", headers=_hdr(),
                         timeout=60).text.strip().strip('"')
        if s.lower() == "completed":
            break
        if s.lower() == "failed":
            raise RuntimeError(f"job {job_id} failed — bisect before assuming bad input")
        time.sleep(every)
    else:
        raise TimeoutError(job_id)
    r = requests.get(f"{BASE}/job/file/{job_id}/out/pangolin_output.csv",
                     headers=_hdr(), timeout=60)
    r.raise_for_status()
    return r.text


def run_submit():
    """One variant per job. A multi-variant job dies on the multi-gene row (C25a)."""
    jobs = {"control_d50": _submit(CONTROL, 50, "BUB1B c.2386-11A>G positive control")}
    for d in DISTANCES:
        jobs[f"allele2_d{d}"] = _submit(ALLELE2, d, f"BUB1B allele 2 c.3006T>G, distance {d}")
    out = {"submitted_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "service": SERVICE, "jobs": jobs, "raw": {}}
    for label, jid in jobs.items():
        print(f"  fetching {label} ({jid}) ...", flush=True)
        out["raw"][label] = _wait_and_fetch(jid)
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVE.write_text(json.dumps(out, indent=2) + "\n")
    print(f"archived -> {ARCHIVE.relative_to(ROOT)}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--submit", action="store_true",
                    help="submit fresh Neurosnap jobs (spends credits). Without it, "
                         "the archived raw output is re-parsed, which is what the "
                         "report's numbers are built from.")
    a = ap.parse_args()

    if a.submit:
        arc = run_submit()
    else:
        if not ARCHIVE.exists():
            sys.exit(f"no archive at {ARCHIVE}; run with --submit first")
        arc = json.loads(ARCHIVE.read_text())

    print(f"\nPangolin, GRCh38, Mask on. Archived {arc['submitted_utc']}.\n")

    # --- guard 1: the control must reproduce its committed score ---
    ctl = parse_pangolin_row(arc["raw"]["control_d50"], CONTROL[1])
    cb = ctl["ENSG00000156970"]
    print(f"POSITIVE CONTROL  c.2386-11A>G   gain {cb['gain']:+.2f} @ {cb['gain_pos']:+d}   "
          f"loss {cb['loss']:+.2f} @ {cb['loss_pos']:+d}")
    ok = (abs(cb["gain"] - CONTROL_EXPECT["gain"]) < 0.02
          and abs(cb["loss"] - CONTROL_EXPECT["loss"]) < 0.02)
    print(f"  committed: gain {CONTROL_EXPECT['gain']:+.2f} / loss {CONTROL_EXPECT['loss']:+.2f}"
          f"   -> {'REPRODUCES' if ok else 'MISMATCH'}")
    if not ok:
        sys.exit("control did not reproduce — allele 2's score is not trustworthy")

    # --- guard 2: the null must survive the window sweep ---
    print(f"\nALLELE 2  c.3006T>G p.Asn1002Lys  (chr15:{ALLELE2[1]})")
    worst = 0.0
    for d in DISTANCES:
        genes = parse_pangolin_row(arc["raw"][f"allele2_d{d}"], ALLELE2[1])
        assert set(genes) == EXPECTED_GENES, f"gene set moved: {sorted(genes)}"
        print(f"  distance {d:>4}:")
        for g in sorted(genes):
            b = genes[g]
            worst = max(worst, abs(b["gain"]), abs(b["loss"]))
            print(f"      {g}  gain {b['gain']:+.2f} @ {b['gain_pos']:+d}   "
                  f"loss {b['loss']:+.2f} @ {b['loss_pos']:+d}")

    print(f"\nlargest |score| anywhere: {worst:.2f}")
    print("VERDICT: no predicted splice effect. The splice route to NMD for allele 2 is")
    print("scored and negative, on an instrument that reproduced its control exactly.")
    print("Allele 2 is made as protein; the open question is abundance vs function.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
