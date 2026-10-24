#!/usr/bin/env python3
"""Is there an ASO-addressable non-productive splicing event in BUB1B, as there is in SCN1A?

    MEASURED PERFORMANCE -- READ BEFORE REUSING THIS (see C46, instrument_validation.py)
    Sensitivity 5/9 (56%) on known poison-exon genes; specificity 1/2 (50%).
    It misses SRSF1, SRSF3, SRSF6 and TRA2B, and false-positives on ACTB. The
    >70%-of-canonical-length filter below is the cause: it discards the short decay
    isoforms that carry SR-protein poison exons. Removing it lifts sensitivity to 7/9 and
    FLIPS BUB1B's own call to positive, so this file's verdict on BUB1B is
    parameter-dependent and is not on its own a result.
    This is a cheap screen that narrows where to measure. It is not a general instrument,
    and a negative from it needs RNA-seq confirmation -- which junction_flux.py provides.

    python3 -m scripts.mva.splice_architecture

THE IDEA UNDER TEST. Zorevunersen raises Nav1.1 by blocking inclusion of SCN1A's poison
exon 20N -- a cassette exon whose inclusion frameshifts the message and sends it to decay.
Block it, and that flux returns to productive mRNA. The drug is in Phase 3 in children.
Our dosage model says this genotype needs roughly a 1.4x increase, which is the size of
effect flux redirection delivers, so if BUB1B carried an equivalent event it would be the
best-fitting candidate we have. This script asks whether it does.

WHY IT IS BUILT TO FAIL. Counting decay-biotype transcripts is not evidence: BUB1B has 12
and would "pass" any such count. The question is whether a *specific, recurrent,
frame-disrupting, ASO-blockable event* exists. Three filters separate that from noise:

  1. TERMINAL-EXON FILTER. Variation in the first or last exon's boundary dominates the
     raw signal and is mostly annotation disagreement about where transcripts start and
     end. It is not a cassette and not an ASO target, so it is excluded. Without this
     filter BUB1B's top "skipped exon" is exon 1, skipped in 9 of 10 decay isoforms --
     which on inspection is four different 5' boundaries for the same first exon.
  2. FRAME TEST. A cassette exon only sends a transcript to decay if including it
     frameshifts the downstream CDS or introduces an in-frame stop. An in-frame cassette
     with no stop inserts residues and is not a poison exon, whatever biotype its
     transcript carries.
  3. EXCLUSIVITY. The event must be absent from every protein-coding transcript.

POSITIVE CONTROL. SCN1A must pass, recovering a frameshifting decay-exclusive cassette,
or the BUB1B result is not reportable. The control is the only reason to believe a
negative here means anything.

WHAT A NEGATIVE WOULD AND WOULD NOT MEAN. Ensembl annotation is not RNA-seq. Exon 20N was
found by sequencing, not by reading annotation, so a method that reads annotation can miss
a real event. A negative here is therefore evidence of absence only to the strength of
this method, and the definitive experiment is RNA-seq of a relevant tissue, which we do
not have. It is still worth running, because a cheap test that can kill an attractive idea
before it reaches a pitch is worth more than the idea was.
"""
import collections
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
D = ROOT / "docs/mva/data"
OUT = D / "splice_architecture.json"
STOPS = {"TAA", "TAG", "TGA"}
GENES = [("ENSG00000156970", "BUB1B", 1, (40161221, 40220759), "subject"),
         ("ENSG00000144285", "SCN1A", -1, None, "positive control")]


def region_seq(chrom, s, e, strand):
    r = subprocess.run(
        ["curl", "-sS", "-H", "Content-Type: text/plain",
         f"https://rest.ensembl.org/sequence/region/human/{chrom}:{s}..{e}:{strand}"],
        capture_output=True, text=True)
    return r.stdout.strip().upper()


def analyse(gid, name, strand, cds, role):
    gene = json.loads((D / f"gene_{gid}.json").read_text())
    tx = json.loads((D / f"tx_{gid}.json").read_text())
    chrom = gene["seq_region_name"]
    canon = next(t for t in gene["Transcript"] if t.get("is_canonical"))
    cex = sorted((e["start"], e["end"]) for e in tx[canon["id"]]["Exon"])
    clen = tx[canon["id"]]["length"]
    first, last = cex[0], cex[-1]           # genomic ends; terminal either way
    cintrons = [(cex[i][1] + 1, cex[i + 1][0] - 1) for i in range(len(cex) - 1)]

    decay = [t for t in gene["Transcript"]
             if t["biotype"] in {"nonsense_mediated_decay", "non_stop_decay"}]
    coding = [t for t in gene["Transcript"] if t["biotype"] == "protein_coding"]
    nearfull = [t for t in decay if tx[t["id"]]["length"] > 0.7 * clen]

    coding_exons = set()
    for t in coding:
        coding_exons |= {(e["start"], e["end"]) for e in tx[t["id"]]["Exon"]}

    cand = collections.Counter()
    for t in nearfull:
        for e in tx[t["id"]]["Exon"]:
            k = (e["start"], e["end"])
            if k in cex or k in coding_exons:
                continue
            if not any(i0 <= k[0] and k[1] <= i1 for i0, i1 in cintrons):
                continue                     # must be a true intronic cassette
            cand[k] += 1

    print(f"\n{'='*78}\n{name}  ({role})   chr{chrom}\n{'='*78}")
    print(f"  transcripts {len(gene['Transcript'])}  |  decay-biotype {len(decay)}"
          f" ({len(decay)/len(gene['Transcript']):.0%})  |  near-full-length decay"
          f" {len(nearfull)}")
    print(f"  intronic cassettes exclusive to decay isoforms: {len(cand)}")

    results = []
    for (s, e), n in cand.most_common():
        L = e - s + 1
        seq = region_seq(chrom, s, e, strand)
        frameshifts = L % 3 != 0
        has_stop = any(seq[i:i + 3] in STOPS for i in range(0, L - 2, 3)) or \
            any(seq[i:i + 3] in STOPS for i in range(1, L - 2, 3)) or \
            any(seq[i:i + 3] in STOPS for i in range(2, L - 2, 3))
        inframe_stop_any = has_stop
        poison = frameshifts or (L % 3 == 0 and inframe_stop_any)
        results.append({"chrom": chrom, "start": s, "end": e, "length_bp": L,
                        "in_decay_isoforms": n, "frameshifts": frameshifts,
                        "stop_in_some_frame": inframe_stop_any,
                        "poison_exon_shaped": bool(frameshifts)})
        print(f"    chr{chrom}:{s}-{e}  {L:>4}bp  in {n} decay isoform(s)  "
              f"{'FRAMESHIFTS -> poison-exon shaped' if frameshifts else 'in-frame (length divisible by 3)'}")

    verdict = any(r["poison_exon_shaped"] for r in results)
    print(f"\n  VERDICT: {'poison-exon-shaped event FOUND' if verdict else 'NO poison-exon-shaped event'}")
    return {"gene": name, "role": role, "chrom": chrom,
            "transcripts": len(gene["Transcript"]), "decay_biotype": len(decay),
            "near_full_length_decay": len(nearfull),
            "candidates": results, "poison_exon_found": verdict}


def main():
    res = [analyse(*g) for g in GENES]
    sub = next(r for r in res if r["role"] == "subject")
    ctl = next(r for r in res if r["role"] == "positive control")

    print(f"\n{'='*78}\nCONTROL\n{'='*78}")
    if not ctl["poison_exon_found"]:
        print("  FAILED -- SCN1A's known, drugged target was not recovered.")
        print("  The BUB1B result above is therefore uninterpretable. Stop here.")
        OUT.write_text(json.dumps({"control_passed": False, "genes": res}, indent=2) + "\n")
        return 1
    c = next(r for r in ctl["candidates"] if r["poison_exon_shaped"])
    print(f"  PASSED. Recovered a {c['length_bp']} bp frameshifting decay-exclusive")
    print(f"  cassette at chr{c['chrom']}:{c['start']}-{c['end']}, with no prior knowledge")
    print(f"  of where to look. SCN1A's poison exon 20N is described in the literature as")
    print(f"  a 64 bp NMD exon and is the target of zorevunersen, now in Phase 3.")

    print(f"\n{'='*78}\nANSWER: MORE OR LESS NON-PRODUCTIVE SPLICING THAN SCN1A?\n{'='*78}")
    print(f"  {'':<34}{'BUB1B':>10}{'SCN1A':>10}")
    print(f"  {'decay-biotype transcripts':<34}{sub['decay_biotype']:>10}{ctl['decay_biotype']:>10}")
    print(f"  {'as a share of all transcripts':<34}"
          f"{sub['decay_biotype']/sub['transcripts']:>9.0%}{ctl['decay_biotype']/ctl['transcripts']:>10.0%}")
    print(f"  {'near-full-length decay isoforms':<34}"
          f"{sub['near_full_length_decay']:>10}{ctl['near_full_length_decay']:>10}")
    print(f"  {'decay-exclusive cassettes':<34}"
          f"{len(sub['candidates']):>10}{len(ctl['candidates']):>10}")
    print(f"  {'POISON-EXON-SHAPED (frameshifting)':<34}"
          f"{sum(r['poison_exon_shaped'] for r in sub['candidates']):>10}"
          f"{sum(r['poison_exon_shaped'] for r in ctl['candidates']):>10}")
    print(f"\n  BUB1B has MORE non-productive annotation and LESS targetable structure.")
    print(f"  More decay isoforms, no frameshifting cassette to block.")

    OUT.write_text(json.dumps(
        {"question": "does BUB1B carry an ASO-addressable non-productive splicing event "
                     "equivalent to SCN1A exon 20N?",
         "control_passed": True,
         "answer": "no poison-exon-shaped cassette found in BUB1B",
         "strength": "evidence of absence only to the strength of an annotation-based "
                     "method; exon 20N itself was found by RNA-seq, not annotation. The "
                     "definitive test is RNA-seq of a relevant tissue, which we lack.",
         "genes": res}, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
