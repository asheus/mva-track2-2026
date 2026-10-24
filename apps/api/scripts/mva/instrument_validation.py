#!/usr/bin/env python3
"""Does the poison-exon scan work on genes other than the one it was built for?

    python3 -m scripts.mva.instrument_validation

We claimed splice_architecture.py "answers the question for any gene". That claim rested
on one positive control, which establishes nothing about sensitivity: a method that fires
on SCN1A and nothing else would look identical from one test.

So the detector is run blind over a panel chosen before seeing any result.

  EXPECTED POSITIVE -- the SR-protein family (SRSF1,2,3,5,6,7,11) and TRA2B. These
  autoregulate their own abundance by splicing in a frame-disrupting cassette exon that
  sends their message to decay; it is the textbook example of the mechanism, independent
  of SCN1A and discovered decades apart. If the detector cannot see poison exons here, our
  BUB1B negative is worthless.

  EXPECTED NEGATIVE -- housekeeping genes with no poison-exon literature. These test
  whether the detector fires on anything with enough annotated transcripts. GAPDH has 81
  transcripts, more than BUB1B's 31, so a detector driven by transcript count alone would
  light up here.

The criterion is the one that matters mechanistically: an intronic cassette exon, absent
from every protein-coding transcript, whose length is not divisible by three -- so that
including it frameshifts everything downstream. (A length-divisible-by-three cassette can
still poison via an internal stop; that needs sequence and is checked case by case in
splice_architecture.py. Counting only frameshifters here makes this test strictly
conservative: it can understate sensitivity, never overstate it.)
"""
import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
D = ROOT / "docs/mva/data"
OUT = D / "instrument_validation.json"
EXPECT = {"SRSF1": "+", "SRSF2": "+", "SRSF3": "+", "SRSF5": "+", "SRSF6": "+",
          "SRSF7": "+", "SRSF11": "+", "TRA2B": "+", "SCN1A": "+",
          "GAPDH": "-", "ACTB": "-", "RPL13A": "-", "TUBB": "-",
          "BUB1B": "?"}


def detect(gid):
    gf, tf = D / f"gene_{gid}.json", D / f"tx_{gid}.json"
    if not (gf.exists() and tf.exists()):
        return None
    gene, tx = json.loads(gf.read_text()), json.loads(tf.read_text())
    canon = next((t for t in gene["Transcript"] if t.get("is_canonical")), None)
    if canon is None or canon["id"] not in tx:
        return None
    cex = sorted((e["start"], e["end"]) for e in tx[canon["id"]]["Exon"])
    clen = tx[canon["id"]]["length"]
    cintr = [(cex[i][1] + 1, cex[i + 1][0] - 1) for i in range(len(cex) - 1)]
    cset = set(cex)

    decay, coding = [], []
    for t in gene["Transcript"]:
        (decay if t["biotype"] in {"nonsense_mediated_decay", "non_stop_decay"}
         else coding if t["biotype"] == "protein_coding" else []).append(t)
    coding_exons = set()
    for t in coding:
        if t["id"] in tx and tx[t["id"]]:
            coding_exons |= {(e["start"], e["end"]) for e in tx[t["id"]]["Exon"]}
    nearfull = [t for t in decay
                if t["id"] in tx and tx[t["id"]] and tx[t["id"]]["length"] > 0.7 * clen]

    cas = collections.Counter()
    for t in nearfull:
        for e in tx[t["id"]]["Exon"]:
            k = (e["start"], e["end"])
            if k in cset or k in coding_exons:
                continue
            if any(i0 <= k[0] and k[1] <= i1 for i0, i1 in cintr):
                cas[k] += 1
    fs = [k for k in cas if (k[1] - k[0] + 1) % 3 != 0]
    return {"transcripts": len(gene["Transcript"]), "decay": len(decay),
            "near_full_decay": len(nearfull), "cassettes": len(cas),
            "frameshifting": len(fs),
            "sizes": sorted((k[1] - k[0] + 1) for k in fs)[:5]}


def main():
    ids = json.loads((D / "panel_ids.json").read_text())
    print(f"{'gene':<9}{'exp':>4}{'tx':>5}{'decay':>7}{'cassettes':>11}"
          f"{'frameshift':>12}{'call':>7}   frameshifting cassette sizes")
    print("-" * 86)
    rows, tp = [], collections.Counter()
    for sym, gid in ids.items():
        r = detect(gid) if gid else None
        if r is None:
            print(f"{sym:<9}{EXPECT.get(sym,'?'):>4}   (not fetched)")
            continue
        call = "+" if r["frameshifting"] else "-"
        exp = EXPECT.get(sym, "?")
        if exp in "+-":
            tp[f"{exp}{call}"] += 1
        flag = "" if exp == "?" or exp == call else "   <-- MISS" if exp == "+" else "   <-- FALSE +"
        print(f"{sym:<9}{exp:>4}{r['transcripts']:>5}{r['decay']:>7}{r['cassettes']:>11}"
              f"{r['frameshifting']:>12}{call:>7}   "
              f"{', '.join(str(s)+'bp' for s in r['sizes']) or '-'}{flag}")
        rows.append({"gene": sym, "expected": exp, "call": call, **r})

    sens_n, sens_d = tp["++"], tp["++"] + tp["+-"]
    spec_n, spec_d = tp["--"], tp["--"] + tp["-+"]
    print("-" * 86)
    print(f"\nSENSITIVITY on known poison-exon genes: {sens_n}/{sens_d}"
          + (f"  ({sens_n/sens_d:.0%})" if sens_d else ""))
    print(f"SPECIFICITY on housekeeping genes:      {spec_n}/{spec_d}"
          + (f"  ({spec_n/spec_d:.0%})" if spec_d else ""))
    b = next((r for r in rows if r["gene"] == "BUB1B"), None)
    if b:
        print(f"\nBUB1B: {b['transcripts']} transcripts, {b['decay']} decay-biotype, "
              f"{b['cassettes']} cassette(s), {b['frameshifting']} frameshifting -> "
              f"call '{b['call']}'")
    print("\nHOW TO READ THIS. A miss on an SR-protein gene means the detector lacks the")
    print("sensitivity to make BUB1B's negative meaningful, and the negative must be")
    print("reported as inconclusive rather than as absence. A false positive on a")
    print("housekeeping gene means the detector fires on transcript diversity rather than")
    print("on mechanism, and BUB1B's zero would then be the only trustworthy thing in it.")

    OUT.write_text(json.dumps({"sensitivity": [sens_n, sens_d],
                               "specificity": [spec_n, spec_d], "panel": rows},
                              indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
