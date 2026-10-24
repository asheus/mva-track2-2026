#!/usr/bin/env python3
"""Resolve a BUB1B coding variant to its exact molecular identity.

    python3 -m scripts.mva.ptc_context

WHY. The pitch rests on two facts about the proband's alleles that are easy to assert and
easy to get wrong: that allele 1's stop codon is UGA, and that it sits far enough from the
last exon-exon junction to be a canonical NMD substrate. Both decide which therapeutic
modality can reach the allele at all, so neither should be quoted from memory.

This derives them from the canonical CDS and the committed exon structure, and refuses to
write anything unless the reference base at each position matches the transcript -- which
is the check that would catch a coordinate or numbering slip.

WHAT IT ESTABLISHES
  allele 1  c.2210T>G  TTA -> TGA   a UGA (opal) stop, context CCAGAG|TGA|AGTGCC
            748 nt upstream of the last exon-exon junction -> canonical NMD substrate
  allele 2  c.3006T>G  AAT -> AAG   p.Asn1002Lys, not a stop

The 50-55 nt rule of thumb is the usual boundary for NMD escape; 748 nt is not a
borderline call, which is why this one can be stated without a probability.

Stop-codon identity matters because readthrough agents do not treat all three stops
alike, and the immediately adjacent sequence modulates release-factor activity and
therefore ataluren's effectiveness (Bhat et al., Nucleic Acids Res 2025,
doi:10.1093/nar/gkaf216). We record the context; we do NOT score it, because no
calibrated per-context predictor exists that we have validated.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
OUT = ROOT / "docs/mva/data/ptc_context.json"
TX = ROOT / "docs/mva/data/bub1b_transcript.json"
ENSEMBL = "https://rest.ensembl.org/sequence/id/ENST00000287598?type=cds"

ALLELES = [(2210, "T", "G", 737, "allele 1"), (3006, "T", "G", 1002, "allele 2")]
CODE = {
    'TTT':'F','TTC':'F','TTA':'L','TTG':'L','CTT':'L','CTC':'L','CTA':'L','CTG':'L',
    'ATT':'I','ATC':'I','ATA':'I','ATG':'M','GTT':'V','GTC':'V','GTA':'V','GTG':'V',
    'TCT':'S','TCC':'S','TCA':'S','TCG':'S','CCT':'P','CCC':'P','CCA':'P','CCG':'P',
    'ACT':'T','ACC':'T','ACA':'T','ACG':'T','GCT':'A','GCC':'A','GCA':'A','GCG':'A',
    'TAT':'Y','TAC':'Y','TAA':'*','TAG':'*','CAT':'H','CAC':'H','CAA':'Q','CAG':'Q',
    'AAT':'N','AAC':'N','AAA':'K','AAG':'K','GAT':'D','GAC':'D','GAA':'E','GAG':'E',
    'TGT':'C','TGC':'C','TGA':'*','TGG':'W','CGT':'R','CGC':'R','CGA':'R','CGG':'R',
    'AGT':'S','AGC':'S','AGA':'R','AGG':'R','GGT':'G','GGC':'G','GGA':'G','GGG':'G'}


def cds():
    raw = subprocess.run(
        ["curl", "-sS", "-H", "Content-Type: text/x-fasta", ENSEMBL],
        capture_output=True, text=True, check=True).stdout
    return "".join(l.strip() for l in raw.split("\n") if l and not l.startswith(">"))


def cds_blocks():
    """CDS-only exon blocks, in transcript order, with their CDS coordinates."""
    t = json.loads(TX.read_text())
    assert t["strand"] == 1, "plus-strand logic only"
    cs, ce = t["cds_start"], t["cds_end"]
    out, cum = [], 0
    for a, b in t["exons"]:
        s, e = max(a, cs), min(b, ce)
        if e < s:
            continue
        L = e - s + 1
        out.append({"cds_from": cum + 1, "cds_to": cum + L, "g_start": s, "g_end": e})
        cum += L
    return out, cum


def main():
    seq = cds()
    blocks, total = cds_blocks()
    if len(seq) != total:
        sys.exit(f"CDS length {len(seq)} != exon-derived {total}; refusing to write")
    last = blocks[-1]
    recs = []
    for pos, ref, alt, res, label in ALLELES:
        if seq[pos - 1] != ref:
            sys.exit(f"c.{pos} reference is {seq[pos-1]}, not {ref}; refusing to write")
        start = (pos - 1) // 3 * 3
        codon = seq[start:start + 3]
        if start // 3 + 1 != res:
            sys.exit(f"c.{pos} lies in codon {start//3+1}, not {res}; refusing to write")
        mut = list(codon); mut[(pos - 1) % 3] = alt; mut = "".join(mut)
        g = next(b["g_start"] + (pos - b["cds_from"]) for b in blocks
                 if b["cds_from"] <= pos <= b["cds_to"])
        is_stop = CODE[mut] == "*"
        d = last["cds_from"] - pos
        rec = {"label": label, "hgvs_c": f"c.{pos}{ref}>{alt}",
               "hgvs_p": f"p.{CODE[codon]}{res}{'Ter' if is_stop else CODE[mut]}",
               "genomic": f"chr15:{g}", "codon_ref": codon, "codon_alt": mut,
               "is_premature_stop": is_stop,
               "stop_codon": mut if is_stop else None,
               "context_6_3_6": f"{seq[start-6:start]}|{mut}|{seq[start+3:start+9]}",
               "plus4_nucleotide": seq[start + 3],
               "nt_upstream_of_last_junction": d,
               "nmd_verdict": ("canonical NMD substrate" if is_stop and d > 55
                               else ("may escape NMD" if is_stop else "not a stop"))}
        recs.append(rec)
        print(f"\n{label}: {rec['hgvs_c']}  {rec['hgvs_p']}   {rec['genomic']}")
        print(f"  codon {res}: {codon} -> {mut}"
              f"{'   STOP TYPE ' + mut if is_stop else ''}")
        print(f"  context (6|codon|6): {rec['context_6_3_6']}   +4 = {rec['plus4_nucleotide']}")
        if is_stop:
            print(f"  {d} nt upstream of the last exon-exon junction"
                  f" (last CDS exon starts at c.{last['cds_from']})")
            print(f"  => {rec['nmd_verdict']}")

    OUT.write_text(json.dumps(
        {"transcript": "ENST00000287598", "cds_nt": total, "cds_exons": len(blocks),
         "last_cds_exon_starts_at_cds": last["cds_from"], "alleles": recs,
         "nmd_boundary_used_nt": 55,
         "note": "Context is recorded, not scored: no per-context readthrough predictor "
                 "has been validated here. Stop identity and adjacent sequence modulate "
                 "release-factor activity (Bhat 2025, doi:10.1093/nar/gkaf216)."},
        indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
