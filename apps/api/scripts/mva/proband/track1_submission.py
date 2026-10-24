"""Emit the Track 1 (Variant Identification) submission CSV.

Track 1 and Track 2 are scored independently, and Track 1's answer is a by-product of
work Track 2 already required: the two causal alleles, confirmed against the proband's
own callset by confirm_variants.py.

The organisers' template is:
    proband_id,chrom_1,pos_1,ref_1,alt_1,chrom_2,pos_2,ref_2,alt_2,epcr,finding_type,notes
A single row carries a COMPOUND HETEROZYGOUS PAIR, which is exactly this case, and
scoring gives partial credit for recovering only one of the two.

Contig naming: the challenge VCF uses "15"; the organisers' template example uses the
"chr1" style, so this writes "chr15" to match the template. If the scorer normalises,
either is fine; if it does not, the template's own convention is the safer bet.

`epcr` is a confidence value. We submit 0.99 for the pair rather than 1.0: both alleles
are confirmed present and heterozygous at maximum genotype quality, but TRANS
configuration is not established by the callset (10,911 bp apart, no physical
phasing), so a sliver of uncertainty is honest.
"""
import argparse, csv, pathlib, sys

OUT = pathlib.Path(__file__).resolve().parents[5] / "docs/mva/data/track1_submission.csv"
HEADER = ["proband_id", "chrom_1", "pos_1", "ref_1", "alt_1",
          "chrom_2", "pos_2", "ref_2", "alt_2", "epcr", "finding_type", "notes"]

ROW = {
    "proband_id": "WGS_EX2312012",
    "chrom_1": "chr15", "pos_1": 40209701, "ref_1": "T", "alt_1": "G",
    "chrom_2": "chr15", "pos_2": 40220612, "ref_2": "T", "alt_2": "G",
    "epcr": 0.99,
    "finding_type": "primary",
    "notes": ("BUB1B compound heterozygous. Allele 1 c.2210T>G p.Leu737Ter (truncating, "
              "removes the entire pseudokinase domain; PTC 747 nt upstream of the last "
              "exon-exon junction. Predicted to undergo NMD, P(escape) 0.32, by a decay "
              "model calibrated on measured allele-specific expression rather than by "
              "the 50-nt rule alone). Allele 2 c.3006T>G p.Asn1002Lys "
              "(missense in the folded core, pLDDT 91.1; AlphaMissense 0.9229). Both "
              "confirmed in the submitted callset: heterozygous, FILTER=PASS, at "
              "maximum genotype quality and high depth, with allele balances "
              "consistent with germline heterozygosity. Consistent with MVA1 "
              "(MIM 257300). Trans configuration inferred from phenotype and parental "
              "recurrent pregnancy loss, not from phasing (sites 10,911 bp apart, no "
              "PGT/PID). Transcript ENST00000287598, GRCh38."),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(OUT),
                    help="where to write the CSV (default: the committed path). "
                         "audit_export.py uses this to diff the committed file "
                         "against a fresh run.")
    out = pathlib.Path(ap.parse_args().out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerow(ROW)
    print(f"wrote {out}")
    print(out.read_text())
    print("NOTE: no secondary or incidental findings are reported. This analysis was "
          "scoped\nto BUB1B and the MVA gene set and did not perform a genome-wide "
          "secondary-findings\nsweep, so 'none' here means 'not assessed', not "
          "'assessed and absent'. The methods\nform asks how incidental findings were "
          "handled; that is the honest answer.")


if __name__ == "__main__":
    main()
