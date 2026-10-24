"""Confirm the proband's two BUB1B alleles in the challenge VCF.

    HF_TOKEN=... python3 confirm_variants.py

WHY THIS EXISTS. Every claim in TRACK2-REPORT.md rests on two alleles that, until this
script ran, had only ever been derived -- Ensembl VEP against ENST00000287598, plus an
independent reading-frame reconstruction from three annotated neighbours. Neither is the
same as reading the child's own data. The report carried "we have not confirmed these
variants in the proband's own VCF" as a standing limitation because huggingface.co was
blocked by this environment's network policy when the work began.

WHAT IT DELIBERATELY DOES NOT DO. It prints ONLY the two target loci. It does not dump
the BUB1B region, other genes, or anything genome-wide, and it writes no extract to
disk. The hackathon DTA forbids resharing the data through any channel, and the
submission repository is destined to be public, so the reproducible artifact here is
the QUERY, not the data. Anyone with their own accepted access can re-run it; nobody
without access learns anything from the committed file.

The VCF is ~315 MB with a tabix index. This streams it to a temporary path, queries,
and deletes it, so no copy of the callset outlives the process.
"""
import os, pathlib, subprocess, sys, tempfile

REPO = "SageBio/mva-hackathon-2026-data"
VCF = "WGS_EX2312012_HGWCNDSX7.vcf.gz"
BASE = f"https://huggingface.co/datasets/{REPO}/resolve/main"

# The two alleles the report is built on. GRCh38, contig named "15" in this callset.
TARGETS = {
    40_209_701: ("T", "G", "c.2210T>G  p.Leu737Ter   truncating (allele 1)"),
    40_220_612: ("T", "G", "c.3006T>G  p.Asn1002Lys  missense   (allele 2)"),
}


def fetch(dest: pathlib.Path, name: str, token: str):
    r = subprocess.run(["curl", "-sL", "--fail", "-H", f"Authorization: Bearer {token}",
                        "-o", str(dest / name), f"{BASE}/{name}"], capture_output=True)
    if r.returncode:
        sys.exit(f"fetch failed for {name}: curl {r.returncode}. "
                 "Check HF_TOKEN and that you have accepted the dataset's terms.")


def main():
    token = os.environ.get("HF_TOKEN")
    if not token:
        sys.exit("HF_TOKEN is not set. This dataset is gated; access must be accepted "
                 "on Hugging Face first.")
    try:
        import pysam
    except ImportError:
        sys.exit("pysam is required: pip install pysam")

    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp)
        for name in (VCF, VCF + ".tbi"):
            fetch(d, name, token)
        v = pysam.VariantFile(str(d / VCF))
        sample = list(v.header.samples)[0]
        contig = "chr15" if "chr15" in v.header.contigs else "15"
        print(f"callset sample: {sample}")
        print(f"reference: GRCh38 (per VCF header), contig naming: {contig!r}\n")

        ok = 0
        for pos, (ref, alt, label) in sorted(TARGETS.items()):
            rec = next((r for r in v.fetch(contig, pos - 1, pos) if r.pos == pos), None)
            if rec is None:
                print(f"ABSENT    {contig}:{pos:,}  {label}")
                continue
            s = rec.samples[sample]
            gt, ad, dp = s.get("GT"), s.get("AD") or (), s.get("DP")
            ab = sum(ad[1:]) / sum(ad) if ad and sum(ad) else float("nan")
            het = gt is not None and len(set(g for g in gt if g is not None)) > 1
            match = rec.ref == ref and alt in (rec.alts or ())
            ok += bool(match and het)
            print(f"{'CONFIRMED' if match else 'MISMATCH '} {contig}:{pos:,} "
                  f"{rec.ref}>{','.join(rec.alts or ())}  {label}")
            print(f"    GT={'/'.join(str(g) for g in gt)} "
                  f"{'(heterozygous)' if het else '(NOT heterozygous)'}  "
                  f"DP={dp}  GQ={s.get('GQ')}  allele balance={ab:.2f}  "
                  f"QUAL={rec.qual:.0f}  FILTER={','.join(rec.filter.keys()) or 'PASS'}")
            # Physical phasing, if the caller emitted any for this site.
            if s.get("PGT") or s.get("PID"):
                print(f"    PHASED: PGT={s.get('PGT')} PID={s.get('PID')}")

        sep = max(TARGETS) - min(TARGETS)
        print(f"\n{ok}/{len(TARGETS)} alleles confirmed present and heterozygous.")
        print(f"The two sites are {sep:,} bp apart. GATK physical phasing spans only a "
              "local\nhaplotype block, so TRANS configuration is NOT established by this "
              "callset:\ncompound heterozygosity remains an inference from the phenotype "
              "and from the fact\nthat a cis arrangement would leave one intact allele. "
              "Parental genotypes or\nlong reads would settle it.")


if __name__ == "__main__":
    main()
