#!/usr/bin/env python3
"""Where does the new PTC land when a non-coding variant forces an exon skip?

    python3 -m scripts.mva.nmd.frameshift_ptc

This closes the chain Pangolin -> frame arithmetic -> PTC position. It deliberately
stops short of attaching a calibrated NMD probability, and the reason is the point of
this file.

WHY THE CALIBRATED MODEL IS *NOT* RUN HERE.
TrunKitten's eight features describe the mutant transcript's PTC context -- distance to
the last exon junction, relative PTC location, the mutated exon, conservation over the
NEW 3'UTR, plus gene-level terms. Mechanistically that is encouraging: NMD surveillance
acts on the transcript, not on the DNA lesion that produced the PTC, so a
frameshift-derived PTC is not obviously out of the model's reach.

The blocker is not model domain, it is feature construction. Those features are computed
against a REFERENCE transcript annotation. An exon skip produces a DIFFERENT transcript:
the exon count changes, the junction the PTC is measured against changes, and the
sequence downstream of the PTC changes. Scoring it properly needs a synthetic mutant
transcript pushed through the annotation pipeline, which that pipeline does not support.

The tempting shortcut is to score a hypothetical point-PTC at the same CDS position in
the reference transcript. That substitutes one transcript's geometry for another's and
would return a calibrated-looking probability that does not describe the variant. This
workstream has spent a fortnight removing numbers of exactly that kind, so it is not
added here.

So: the PTC POSITION is computed exactly -- that is the new information, and nobody has
it for these variants -- and the decay call is made by the established 50-55 nt rule and
labelled `rule_based`. Synthetic-transcript feature construction is named as the next
step rather than faked.

The rule, applied honestly: a PTC more than ~50-55 nt upstream of the last exon-exon
junction is NMD-sensitive; one downstream of that boundary escapes by construction,
because there is no downstream junction complex to trigger decay.
"""
import json
import pathlib
import sys
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[5]
D = ROOT / "docs/mva/data"
ELIG = D / "nmd/noncoding_eligibility.tsv"
EXONS = D / "cds_exons.json"
OUT = D / "nmd/frameshift_ptc.tsv"
CDS_CACHE = D / "nmd/bub1b_cds.txt"
TX = "ENST00000287598"
EJC_RULE = 55          # nt upstream of the last junction; the permissive end of 50-55
STOPS = {"TAA", "TAG", "TGA"}


def cds_sequence():
    if CDS_CACHE.exists():
        return CDS_CACHE.read_text().strip()
    url = (f"https://rest.ensembl.org/sequence/id/{TX}"
           f"?type=cds;content-type=text/plain")
    for attempt in range(4):
        try:
            s = urllib.request.urlopen(url, timeout=120).read().decode().strip()
            break
        except Exception as e:
            if attempt == 3:
                sys.exit(f"could not fetch CDS: {e}")
            time.sleep(2 ** attempt)
    CDS_CACHE.parent.mkdir(parents=True, exist_ok=True)
    CDS_CACHE.write_text(s + "\n")
    return s


def exon_table():
    out, seen = [], 0
    for i, (s, e) in enumerate(json.loads(EXONS.read_text()), 1):
        length = e - s + 1
        out.append({"n": i, "start": s, "end": e, "len": length,
                    "cds_from": seen + 1, "cds_to": seen + length})
        seen += length
    return out


def first_stop(seq, frame_start):
    """Index (0-based, in `seq`) of the first in-frame stop at or after frame_start."""
    for i in range(frame_start, len(seq) - 2, 3):
        if seq[i:i + 3].upper() in STOPS:
            return i
    return None


def main():
    if not ELIG.exists():
        sys.exit(f"missing {ELIG}; run pangolin_sweep_report.py first")
    cds = cds_sequence()
    exons = exon_table()
    total = exons[-1]["cds_to"]
    last_junction = exons[-1]["cds_from"]       # CDS coord where the final exon starts
    print(f"CDS {len(cds)} nt ({total} from the exon model), {len(exons)} CDS exons")
    print(f"last exon-exon junction at CDS {last_junction}; the NMD boundary is "
          f"{last_junction + EJC_RULE} nt\n")

    lines = ELIG.read_text().strip().split("\n")
    if len(lines) < 2:
        print("no called variants yet -- nothing to do")
        return 0
    cols = lines[0].split("\t")
    rows = [dict(zip(cols, L.split("\t"))) for L in lines[1:]]
    fs = [r for r in rows if r.get("skip_consequence") == "frameshift"]
    print(f"{len(fs)} of {len(rows)} called variants cause a frameshifting skip\n")

    out = []
    for r in fs:
        n = int(r["nearest_exon"])
        ex = exons[n - 1]
        # Excise the skipped exon from the CDS and re-read the frame from its start.
        mutant = cds[:ex["cds_from"] - 1] + cds[ex["cds_to"]:]
        stop_i = first_stop(mutant, ex["cds_from"] - 1)
        if stop_i is None:
            call, note, ptc_cds, dist = ("NO_DOWNSTREAM_STOP", "frame runs to the "
                                         "transcript end without a stop", "", "")
        else:
            ptc_cds = stop_i + 1
            # Junction coordinates shift by the excised exon's length.
            mut_last_junction = last_junction - ex["len"]
            dist = mut_last_junction - ptc_cds
            if dist > EJC_RULE:
                call = "PTC_decay_expected"
                note = f"{dist} nt upstream of the last junction in the mutant transcript"
            else:
                call = "PTC_escape_expected"
                note = (f"{dist} nt from the last junction -- inside the "
                        f"{EJC_RULE} nt boundary, so no downstream junction complex")
        out.append({**r, "skipped_exon": n, "skipped_exon_len": ex["len"],
                    "ptc_cds_pos": ptc_cds, "nt_upstream_of_last_junction": dist,
                    "decay_call": call, "basis": "rule_based (50-55 nt rule)",
                    "note": note})
        print(f"  {r.get('hgvs_c') or r['pos']:>16s}  exon {n:2d} "
              f"({ex['len']:3d} nt, skip shifts frame)  -> PTC at CDS {ptc_cds}  "
              f"{call}")
        if note:
            print(f"      {note}")

    cw = ["chrom", "pos", "ref", "alt", "hgvs_c", "consequence",
          "clinvar_significance", "gain", "loss", "skipped_exon", "skipped_exon_len",
          "ptc_cds_pos", "nt_upstream_of_last_junction", "decay_call", "basis", "note"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        f.write("\t".join(cw) + "\n")
        for r in out:
            f.write("\t".join(str(r.get(c, "")).replace("\t", " ") for c in cw) + "\n")
    print(f"\nwrote {len(out)} rows -> {OUT.relative_to(ROOT)}")
    print("\nEVERY CALL HERE IS RULE-BASED, not model-based. Attaching a calibrated")
    print("probability needs the mutant transcript's own feature annotation, which the")
    print("model's pipeline does not support; see this file's header for why the")
    print("obvious shortcut was refused.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
