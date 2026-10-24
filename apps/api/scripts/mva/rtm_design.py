#!/usr/bin/env python3
"""Where would a trans-splicing molecule have to bind on BUB1B, and how big would it be?

    python3 -m scripts.mva.rtm_design

THERE IS NO TRANS-SPLICING DRUG. Not approved, and not in trials: ClinicalTrials.gov
returns exactly one study mentioning trans-splicing, and it is a Huntington's disease skin
biopsy for preclinical development, not a molecule given to anyone. So this cannot show
"drugs that would work". What it can do is specify the molecule that would have to be
built, using the transcript structure we have already verified, and state the design
constraints the field has published.

WHAT AN RTM IS. A 3' pre-mRNA trans-splicing molecule has three parts:
  1. a BINDING DOMAIN, antisense to a chosen intron of the target pre-mRNA, which tethers
     the molecule to the nascent transcript;
  2. a SPLICE DOMAIN -- branch point, polypyrimidine tract and 3' AG -- which competes with
     the intron's own 3' splice site;
  3. a CODING CASSETTE carrying the corrected sequence from that point to the stop codon.
The spliceosome then joins the target's upstream exons to the cassette, and everything
downstream of the binding site is replaced -- including whatever mutation it carried.

WHY THAT GEOMETRY IS GOOD FOR THIS GENOTYPE. Allele 1's PTC is at c.2210 and allele 2's
missense at c.3006. **One RTM binding any intron upstream of c.2210 replaces both.** It
does not need to know which allele it landed on, which is what "mutation-agnostic" means
here and why the same molecule would serve most of the 2,536 catalogued alleles.

DESIGN CONSTRAINTS, from the groups who have actually built these:
  - Efficiency is the whole problem, and RTMs are selected EMPIRICALLY, not designed.
    Huttner 2016 screened pools of randomly generated variants with a fluorescence reporter
    to find the efficient ones (doi:10.3390/ijms17101609).
  - Co-delivered antisense RNAs that mask competing splicing elements significantly raise
    efficiency (Koller 2015, doi:10.3390/ijms16011179) -- the same trick the CTNNB1 group
    used in 2025, with a 5' ribozyme for nuclear retention.
  - A longer intron gives more room for a binding domain that does not collide with the
    intron's own branch point, so very short introns are poor targets.

So the output below is a shortlist of target introns and cassette sizes. It is a
specification, not a molecule, and the molecule would still have to be screened.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
D = ROOT / "docs/mva/data"
OUT = D / "rtm_design.json"
CDS_S, CDS_E = 40161221, 40220759
ALLELE1_CDS, ALLELE2_CDS = 2210, 3006


def blocks():
    t = json.loads((D / "bub1b_transcript.json").read_text())
    out, cum = [], 0
    for a, b in t["exons"]:
        s, e = max(a, CDS_S), min(b, CDS_E)
        if e < s:
            continue
        L = e - s + 1
        out.append({"cds_from": cum + 1, "cds_to": cum + L, "g_start": s, "g_end": e})
        cum += L
    return out, cum


def main():
    ex, total = blocks()
    print(f"BUB1B canonical CDS: {total} nt in {len(ex)} coding exons\n")

    def exon_of(c):
        return next(i for i, b in enumerate(ex) if b["cds_from"] <= c <= b["cds_to"])
    e1, e2 = exon_of(ALLELE1_CDS), exon_of(ALLELE2_CDS)
    print(f"  allele 1  c.{ALLELE1_CDS} (p.Leu737Ter)  lies in coding exon {e1+1}"
          f"  (c.{ex[e1]['cds_from']}-{ex[e1]['cds_to']})")
    print(f"  allele 2  c.{ALLELE2_CDS} (p.Asn1002Lys) lies in coding exon {e2+1}"
          f"  (c.{ex[e2]['cds_from']}-{ex[e2]['cds_to']})")
    print(f"\n  A 3' RTM binding any intron BEFORE coding exon {e1+1} replaces everything")
    print(f"  downstream and therefore corrects BOTH alleles with one molecule.")

    print("\n" + "=" * 92)
    print("CANDIDATE TARGET INTRONS  (those upstream of allele 1)")
    print("=" * 92)
    print(f"  {'intron':>7}{'genomic span':>26}{'length':>9}{'cassette nt':>13}"
          f"{'cassette aa':>13}   note")
    print("  " + "-" * 88)
    cands = []
    for i in range(len(ex) - 1):
        istart, iend = ex[i]["g_end"] + 1, ex[i + 1]["g_start"] - 1
        ilen = iend - istart + 1
        if i + 1 > e1:            # intron must precede the exon carrying allele 1
            continue
        cassette = total - ex[i + 1]["cds_from"] + 1
        room = "short - poor target" if ilen < 500 else (
            "workable" if ilen < 5000 else "ample")
        cands.append({"intron_after_coding_exon": i + 1, "g_start": istart,
                      "g_end": iend, "intron_len": ilen,
                      "cassette_nt": cassette, "cassette_aa": cassette // 3,
                      "room": room})
        print(f"  {i+1:>7}   chr15:{istart}-{iend}{ilen:>9}{cassette:>13}"
              f"{cassette//3:>13}   {room}")

    best = [c for c in cands if c["room"] != "short - poor target"]
    best.sort(key=lambda c: (-c["intron_len"]))
    print("\n" + "=" * 92)
    print("SHORTLIST")
    print("=" * 92)
    print("  Ranked by binding-domain room, which is the constraint the field reports.")
    for c in best[:5]:
        print(f"    intron after coding exon {c['intron_after_coding_exon']:>2}: "
              f"{c['intron_len']:>6} nt of intron, cassette {c['cassette_nt']:>4} nt "
              f"({c['cassette_aa']} codons)")
    print("\n  Trade-off: binding further upstream gives a bigger intron to bind but a")
    print("  longer cassette to deliver; binding closer to allele 1 gives a short cassette")
    print("  and less room. Nothing here resolves it -- a screen does.")

    # the allele-2-only option
    lastint = len(ex) - 2
    istart, iend = ex[lastint]["g_end"] + 1, ex[lastint + 1]["g_start"] - 1
    cass = total - ex[lastint + 1]["cds_from"] + 1
    print(f"\n  If only allele 2 mattered, the last intron (chr15:{istart}-{iend}, "
          f"{iend-istart+1} nt)")
    print(f"  needs a cassette of just {cass} nt ({cass//3} codons) -- but it would leave")
    print(f"  allele 1 untouched, which is the reason to prefer trans-splicing at all.")

    print("\n" + "=" * 92)
    print("WHAT THIS IS NOT")
    print("=" * 92)
    print("  Not a drug, and not a molecule anyone has made. Efficiency is the whole")
    print("  problem, RTMs are selected by screening rather than designed, and our dosage")
    print("  model puts the bar at 23-38% to reach carrier level. No published RTM for any")
    print("  gene has been given to a patient.")

    OUT.write_text(json.dumps({
        "no_trans_splicing_drug_exists": True,
        "clinicaltrials_hits": 1,
        "clinicaltrials_note": "the single hit is a Huntington's skin-biopsy study for "
                               "preclinical development, not a molecule given to anyone",
        "allele1_coding_exon": e1 + 1, "allele2_coding_exon": e2 + 1,
        "one_rtm_corrects_both": True,
        "candidate_introns": cands, "shortlist": best[:5],
        "required_efficiency": "23-38% to reach carrier level (dosage_model.py)",
        "design_constraints": [
            "RTMs are selected empirically from pools, not rationally designed "
            "(Huttner 2016, doi:10.3390/ijms17101609)",
            "co-delivered antisense RNAs masking competing splice elements raise "
            "efficiency (Koller 2015, doi:10.3390/ijms16011179)",
            "short introns leave little room for a binding domain"],
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
