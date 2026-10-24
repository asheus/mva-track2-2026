"""Could the Track 1 answer have been FOUND, rather than merely confirmed?

confirm_variants.py checks two positions we already believed in. That is confirmation,
and confirmation cannot tell you whether you would have arrived at the answer without
being told it. This script asks the harder question with a filter that uses no
knowledge of WHICH positions matter:

    inside the BUB1B gene span, keep calls that are
      - FILTER=PASS
      - heterozygous
      - located in a CDS exon (from the committed exon map)

and reports how many survive and whether they are our two.

WHAT THIS DOES AND DOES NOT ESTABLISH. It is an unbiased test WITHIN the gene: nothing
about position 40,209,701 or 40,220,612 enters the filter. It is NOT a genome-wide
rediscovery -- the gene itself is still assumed. A genuine Track 1 pipeline ranks
candidates across the whole callset from the VCF plus HPO terms, and this workstream
never built one, because the causal gene was established before the analysis began and
everything after was mechanism work for Track 2. That limitation is stated in the
Track 1 methods description rather than papered over.

    HF_TOKEN=... python3 track1_rediscovery.py
"""
import json, os, pathlib, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[5]
EXONS = ROOT / "docs/mva/data/cds_exons.json"
REPO = "SageBio/mva-hackathon-2026-data"
VCF = "WGS_EX2312012_HGWCNDSX7.vcf.gz"
BASE = f"https://huggingface.co/datasets/{REPO}/resolve/main"
GENE = ("15", 40_161_000, 40_221_000)      # BUB1B, GRCh38
ANSWER = {40_209_701, 40_220_612}


def main():
    token = os.environ.get("HF_TOKEN")
    if not token:
        sys.exit("HF_TOKEN is not set; the challenge dataset is gated.")
    import pysam

    spans = sorted((int(a), int(b)) for a, b in json.loads(EXONS.read_text()))
    print(f"{len(spans)} CDS exons, {spans[0][0]:,}-{spans[-1][1]:,}\n")

    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp)
        for name in (VCF, VCF + ".tbi"):
            r = subprocess.run(["curl", "-sL", "--fail", "-H",
                                f"Authorization: Bearer {token}",
                                "-o", str(d / name), f"{BASE}/{name}"],
                               capture_output=True)
            if r.returncode:
                sys.exit(f"fetch failed for {name} (curl {r.returncode})")
        v = pysam.VariantFile(str(d / VCF))

        stage = {"in gene span": 0, "PASS": 0, "heterozygous": 0, "in a CDS exon": 0}
        survivors = []
        for rec in v.fetch(*GENE):
            stage["in gene span"] += 1
            if list(rec.filter.keys()) not in ([], ["PASS"]):
                continue
            stage["PASS"] += 1
            gt = rec.samples[0].get("GT") or ()
            if len({g for g in gt if g is not None}) < 2:
                continue
            stage["heterozygous"] += 1
            if not any(a <= rec.pos <= b for a, b in spans):
                continue
            stage["in a CDS exon"] += 1
            survivors.append(rec.pos)

    print("filter cascade (no position is hard-coded):")
    for k, n in stage.items():
        print(f"   {k:16s} {n:4d}")
    print()
    for pos in survivors:
        print(f"   survivor {pos:,}  {'== our submitted allele' if pos in ANSWER else 'UNEXPECTED'}")

    got, extra = ANSWER & set(survivors), set(survivors) - ANSWER
    print(f"\nrecovered {len(got)}/2 of the submitted alleles, with {len(extra)} extra.")
    if got == ANSWER and not extra:
        print("The unbiased within-gene filter isolates EXACTLY the submitted pair.")
    print("\nStill assumed: the gene. This is not genome-wide rediscovery.")


if __name__ == "__main__":
    main()
