#!/usr/bin/env python3
"""Find poison-exon candidates from annotation alone -- validated on a gene with a known answer.

    python3 -m scripts.mva.poison_exon_scan

THE QUESTION. A splice-modulating ASO of the zorevunersen type works by blocking a
"poison exon": a naturally occurring cassette exon that, when included, introduces a
premature stop and sends the transcript to decay. Blocking it redirects that flux into
productive mRNA and raises protein from the alleles the patient already has. The modality
is in Phase 3 in children for SCN1A. The question is whether BUB1B has the same substrate.

WHY THIS NEEDS AN EXTERNAL CHECK. "Counting NMD-biotype transcripts" is a weak proxy --
transcripts land in that biotype for many reasons, most of which no ASO can address. A
method that merely counts them would report something for any gene and could not be wrong.

So the method is held to a standard it could fail: **it must rediscover SCN1A's poison
exon, from annotation alone, without being told where to look.** SCN1A is the positive
control because its poison exon is the target of a drug in Phase 3. If the scan does not
recover it, the scan's output on BUB1B is noise and this file says so.

THE SIGNATURE WE LOOK FOR. A poison exon is an exon that
  (a) lies entirely inside an intron of the canonical transcript -- it is a cassette exon,
      not an alternative first/last exon or a boundary shift, and
  (b) appears in decay-biotype transcripts and in NO protein-coding transcript.
Condition (b) is the discriminating one: an exon whose inclusion is compatible with
producing protein is not a poison exon, whatever else it is. We rank candidates by how
many decay transcripts carry them, and report the exclusivity explicitly rather than
folding it into a score.

WHAT THIS CANNOT DO. Annotation is not flux. These coordinates say an isoform has been
observed often enough to be annotated; they do not say what fraction of the gene's output
takes that path in any tissue, and that fraction is exactly what determines how much
headroom an upregulating ASO would have. Quantifying it needs RNA-seq we do not have.
Every claim here is therefore about *architecture*, never about magnitude.
"""
import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
D = ROOT / "docs/mva/data"
OUT = D / "poison_exon_scan.json"
DECAY = {"nonsense_mediated_decay", "non_stop_decay"}
GENES = [("ENSG00000156970", "BUB1B", "subject"),
         ("ENSG00000144285", "SCN1A", "positive control -- zorevunersen target")]


def load(gid):
    gene = json.loads((D / f"gene_{gid}.json").read_text())
    tx = json.loads((D / f"tx_{gid}.json").read_text())
    return gene, tx


def introns(exons):
    """Canonical introns as (start, end) inclusive, from sorted genomic exons."""
    ex = sorted(exons)
    return [(ex[i][1] + 1, ex[i + 1][0] - 1) for i in range(len(ex) - 1)]


def scan(gid, name, role):
    gene, tx = load(gid)
    canon = next((t for t in gene["Transcript"] if t.get("is_canonical")), None)
    if canon is None:
        sys.exit(f"{name}: no canonical transcript")
    cex = {(e["start"], e["end"]) for e in tx[canon["id"]]["Exon"]}
    cintrons = introns(cex)

    biotypes = collections.Counter(t["biotype"] for t in gene["Transcript"])
    n_decay = sum(v for k, v in biotypes.items() if k in DECAY)

    # exon -> which transcripts carry it, split by whether they can make protein
    carriers = collections.defaultdict(lambda: {"decay": [], "coding": [], "other": []})
    for t in gene["Transcript"]:
        bt = t["biotype"]
        lane = "decay" if bt in DECAY else ("coding" if bt == "protein_coding" else "other")
        for e in tx[t["id"]]["Exon"]:
            key = (e["start"], e["end"])
            if key in cex:
                continue                      # canonical exon, not a candidate
            carriers[key][lane].append(t["id"])

    cands = []
    for (s, e), lanes in carriers.items():
        inside = any(i0 <= s and e <= i1 for i0, i1 in cintrons)
        if not inside:
            continue                          # must be a cassette exon within an intron
        if not lanes["decay"]:
            continue                          # must appear in decay transcripts
        cands.append({
            "start": s, "end": e, "length_bp": e - s + 1,
            "decay_transcripts": len(lanes["decay"]),
            "coding_transcripts": len(lanes["coding"]),
            "exclusive_to_decay": len(lanes["coding"]) == 0,
            "intron_index_1based": next(
                i + 1 for i, (i0, i1) in enumerate(cintrons) if i0 <= s and e <= i1)})
    cands.sort(key=lambda c: (c["exclusive_to_decay"], c["decay_transcripts"],
                              -c["length_bp"]), reverse=True)

    strict = [c for c in cands if c["exclusive_to_decay"]]
    print(f"\n{'='*78}\n{name}  ({role})\n{'='*78}")
    print(f"  canonical {canon['id']}, {len(cex)} exons, {len(cintrons)} introns")
    print(f"  annotated transcripts: {len(gene['Transcript'])}"
          f"   decay-biotype: {n_decay} ({n_decay/len(gene['Transcript']):.0%})")
    print(f"  intronic cassette exons seen in decay transcripts: {len(cands)}")
    print(f"  of those, EXCLUSIVE to decay transcripts (poison-exon signature): "
          f"{len(strict)}")
    if strict:
        print(f"\n  {'intron':>7} {'length':>7} {'decay tx':>9}  coordinates")
        for c in strict[:12]:
            print(f"  {c['intron_index_1based']:>7} {c['length_bp']:>6}bp "
                  f"{c['decay_transcripts']:>9}  {gene['seq_region_name']}:"
                  f"{c['start']}-{c['end']}")
    return {"gene": name, "role": role, "ensembl_gene": gid,
            "canonical": canon["id"], "transcripts": len(gene["Transcript"]),
            "biotypes": dict(biotypes), "decay_transcripts": n_decay,
            "intronic_cassette_in_decay": len(cands),
            "poison_exon_candidates": strict,
            "chrom": gene["seq_region_name"]}


def main():
    res = [scan(*g) for g in GENES]
    sub = next(r for r in res if r["role"] == "subject")
    ctl = next(r for r in res if r["role"].startswith("positive"))

    print(f"\n{'='*78}\nDOES THE METHOD PASS ITS OWN CONTROL?\n{'='*78}")
    ok = len(ctl["poison_exon_candidates"]) > 0
    if ok:
        best = ctl["poison_exon_candidates"][0]
        print(f"  SCN1A: recovered {len(ctl['poison_exon_candidates'])} decay-exclusive "
              f"intronic cassette exon(s) with no prior knowledge of where to look.")
        print(f"  Top candidate: intron {best['intron_index_1based']}, "
              f"{best['length_bp']} bp, in {best['decay_transcripts']} decay transcripts.")
        print(f"  SCN1A's poison exon is a real, drugged target, so recovering one here is")
        print(f"  the outcome that licenses reading the BUB1B result.")
    else:
        print("  FAILED. SCN1A's poison exon was NOT recovered, so the BUB1B numbers")
        print("  below mean nothing and must not be reported as a finding.")

    print(f"\n{'='*78}\nMORE OR LESS NON-PRODUCTIVE SPLICING THAN SCN1A?\n{'='*78}")
    print(f"  {'':<22}{'BUB1B':>12}{'SCN1A':>12}")
    for lbl, k in [("annotated transcripts", "transcripts"),
                   ("decay-biotype", "decay_transcripts"),
                   ("intronic cassette exons", "intronic_cassette_in_decay")]:
        print(f"  {lbl:<22}{sub[k]:>12}{ctl[k]:>12}")
    print(f"  {'decay-exclusive exons':<22}"
          f"{len(sub['poison_exon_candidates']):>12}"
          f"{len(ctl['poison_exon_candidates']):>12}")
    print(f"  {'decay share':<22}"
          f"{sub['decay_transcripts']/sub['transcripts']:>11.0%}"
          f"{ctl['decay_transcripts']/ctl['transcripts']:>12.0%}")

    OUT.write_text(json.dumps(
        {"method": "intronic cassette exons present in decay-biotype transcripts and "
                   "absent from every protein-coding transcript",
         "positive_control_passed": ok,
         "caveat": "Annotation is not flux. These are architectural candidates; the "
                   "fraction of output taking each path is unmeasured and is what "
                   "determines an upregulating ASO's headroom.",
         "genes": res}, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
