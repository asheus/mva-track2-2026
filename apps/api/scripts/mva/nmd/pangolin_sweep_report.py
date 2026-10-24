#!/usr/bin/env python3
"""Turn the Pangolin sweep into a therapeutic-eligibility call per variant.

    python3 -m scripts.mva.nmd.pangolin_sweep_report

THE QUESTION THIS ANSWERS, and why it is a Track 2 question rather than a diagnostic one.
Our therapeutic thesis is "raise the BubR1 the patient still makes". That is only
coherent for a patient who makes some. So for every variant the operative question is
not "is it pathogenic" but **"does it leave protein behind to rescue"**:

    no splice effect                  -> not a splice mechanism; eligibility undecided here
    splice effect, IN-FRAME skip      -> internally deleted protein IS made -> HYPOMORPH,
                                         potentially eligible for a proteostasis approach
    splice effect, FRAMESHIFT -> PTC  -> ask the NMD model:
          PTC decays                  -> NULL allele, nothing to rescue -> NOT eligible
          PTC escapes                 -> truncated protein present -> separate question

Fabry has exactly this map, assay-determined, for 1,386 variants, and it is used for
per-patient drug eligibility. BUB1B has nothing of the kind. This is a PREDICTED map and
must be labelled as such everywhere it is used -- a prediction is not an amenability
assay, and the Fabry precedent is the reason to say so plainly: the company that
commercialised that strategy built an assay rather than a predictor.

GATE. The sweep embeds variants with committed reference scores as sentinels. If they do
not reproduce, this script refuses to emit a map, because a scan whose control failed
cannot distinguish a true negative from a broken instrument.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
ARCHIVE = ROOT / "docs/mva/data/nmd/pangolin_sweep.jsonl"
VARIANTS = ROOT / "docs/mva/data/nmd/clinvar_noncoding_verified.tsv"
EXONS = ROOT / "docs/mva/data/cds_exons.json"
OUT = ROOT / "docs/mva/data/nmd/noncoding_eligibility.tsv"

# CALLING THRESHOLDS, derived from measured outcomes on a held-out split
# (mfass_threshold.py, C38/C39). The single CALL = 0.2 this file used to carry was
# justified as "deliberately permissive for a screen", on the reasoning that the four
# committed reference variants all score >= 0.49 so 0.2 sits well below known-true.
# Benchmarked against 946 measured splice-disrupting variants, that reasoning was
# backwards: 0.2 is highly specific (held-out 0.985) and badly under-sensitive
# (held-out 0.317). A floor under four known-strong variants sits ABOVE most real
# disruption, not below it.
#
# The deeper finding is that no single threshold can do both jobs. At the 3.2% rate
# these variants actually occur, held out:
#
# Final numbers, from the SEALED quarter of the benchmark -- a split that informed no
# threshold, no tier boundary and no region decision, opened once (seal_openings.log):
#
#     thr    sens    spec    precision(3.2%)   wrong calls per right call
#     0.16   0.392   0.986       0.481              1.1
#     0.02   0.793   0.872       0.170              4.9
#
# Tripling sensitivity costs more than half the precision. That is the arithmetic of a
# low base rate with AUC 0.88, not a tuning failure, so the map reports TIERS -- as the
# Fabry assay this workstream keeps citing also does (amenable / not / indeterminate)
# rather than one binary call.
CALL_HIGH = 0.16     # act on these:   sealed sensitivity 0.392, specificity 0.986
CALL_SCREEN = 0.02   # candidates:     sealed sensitivity 0.793, specificity 0.872
CALL = CALL_SCREEN   # the set the map enumerates; tier is carried per variant
KNOWN = {
    (40196779, "G", "A"): ("c.1288+5G>A", 0.49, -0.73),
    (40200239, "A", "G"): ("c.1402-5A>G", 0.85, -0.69),
    (40212488, "A", "G"): ("c.2386-11A>G", 0.76, -0.71),
    (40206459, "G", "A"): ("c.2009+1G>A", 0.73, -0.89),
}
TOL = 0.03


def num(s):
    """Pangolin leaves a field EMPTY when it predicts no gain (or no loss) -- that is a
    result, not a parse error, and treating it as 0.0 is correct."""
    s = (s or "").strip()
    if not s:
        return 0.0
    try:
        return float(s)
    except ValueError:
        return 0.0


# BUB1B's Ensembl gene ID. In the PAK6 overlap a row carries THREE gene blocks --
# BUB1B, PAK6 (ENSG00000137843) and the BUB1B-PAK6 readthrough (ENSG00000259288) -- and
# the gene the score belongs to must be chosen by ID, never by column position.
BUB1B_GENE = "ENSG00000156970"


def recover_multigene(fields, positions):
    """Recover BUB1B's own scores from a row whose CHROM/POS were eaten (C25b).

    A multi-gene row looks like:

        REF,ALT,<gene>|<gainpos>:<gain>|<losspos>:<loss>|Warnings:,<gene>|...,<gene>,...

    so REF and ALT survive in the first two fields, each gene's result is a pipe-delimited
    block, and CHROM/POS are gone. Two things make this recoverable rather than a guess:

      * the gene is identified by its Ensembl ID inside the block, so BUB1B's score is
        read from BUB1B's block;
      * the position comes from the job's own submitted variant list, and ONLY when that
        list holds exactly one variant, so the row cannot be mis-attributed.

    THE OBVIOUS SHORTCUT IS WRONG, which is the reason this function exists rather than
    a one-line change. The trailing plain columns of such a row hold the LAST gene's
    scores, not BUB1B's, and they disagree with BUB1B's block in 37 of 188 overlap rows.
    Reading them would have silently attributed PAK6's or the readthrough's splice score
    to BUB1B in a fifth of the region -- a wrong answer where we previously had none.
    """
    if not positions or len(positions) != 1:
        return None
    block = next((x for x in fields
                  if x.startswith(BUB1B_GENE) and "|" in x), None)
    if block is None:
        return None
    parts = block.split("|")
    if len(parts) < 3:
        return None
    try:
        gain = num(parts[1].split(":")[1])
        loss = num(parts[2].split(":")[1])
    except (IndexError, ValueError):
        return None
    # REF and ALT are found by SHAPE, not by offset, because the offset varies.
    # The number of fields the shift eats depends on how many genes overlap the variant:
    # with three gene blocks (BUB1B + PAK6 + the readthrough) both CHROM and POS are
    # consumed and REF lands at index 0; with two blocks only CHROM goes and REF lands at
    # index 1. Any fixed offset is therefore right in one region and wrong in the other --
    # the first version of this function assumed the three-gene layout and silently
    # dropped all 71 two-gene rows. So: take the single-base A/C/G/T fields that precede
    # the first gene field, and use the last two of them.
    first_gene = next((i for i, x in enumerate(fields) if x.startswith("ENSG")), None)
    if first_gene is None or first_gene < 2:
        return None
    bases = [x.strip() for x in fields[:first_gene]
             if len(x.strip()) == 1 and x.strip() in "ACGT"]
    if len(bases) < 2:
        return None
    ref, alt = bases[-2], bases[-1]
    return int(positions[0]), ref, alt, gain, loss


def parse_rows(raw, positions=None):
    """Yield (pos, ref, alt, gain, loss) from one job's CSV.

    Well-formed single-gene rows are read directly. A row mangled by the multi-gene
    column shift (C25b) is recovered through `recover_multigene` when the job submitted
    exactly one variant; otherwise it is counted as shifted and dropped, because a
    position that cannot be attributed is not a result.
    """
    good, shifted, recovered = [], 0, 0
    for line in raw.strip().split("\n")[1:]:
        f = line.split(",")
        if len(f) < 9:
            shifted += 1
            continue
        try:
            pos = int(f[1])
        except ValueError:
            rec = recover_multigene(f, positions)
            if rec is None:
                shifted += 1       # CHROM/POS eaten and not attributable (C25b)
            else:
                good.append(rec)
                recovered += 1
            continue
        good.append((pos, f[2], f[3], num(f[6]), num(f[8])))
    return good, shifted, recovered


def load_exons():
    ex = json.loads(EXONS.read_text())
    out, seen = [], 0
    for i, (s, e) in enumerate(ex, 1):
        length = e - s + 1
        out.append({"n": i, "start": s, "end": e, "cds_len": length,
                    "cds_from": seen + 1, "cds_to": seen + length})
        seen += length
    return out


def nearest_exon(pos, exons):
    """The exon whose boundary the variant sits closest to -- the one a disrupted site
    would most plausibly cause to be skipped."""
    best, bd = None, None
    for ex in exons:
        d = 0 if ex["start"] <= pos <= ex["end"] else min(abs(pos - ex["start"]),
                                                          abs(pos - ex["end"]))
        if bd is None or d < bd:
            best, bd = ex, d
    return best, bd


def main():
    for p in (ARCHIVE, VARIANTS, EXONS):
        if not p.exists():
            sys.exit(f"missing {p}")

    lines = VARIANTS.read_text().strip().split("\n")
    cols = lines[0].split("\t")
    meta = {}
    for L in lines[1:]:
        r = dict(zip(cols, L.split("\t")))
        meta[(int(r["pos"]), r["ref"], r["alt"])] = r

    scored, shifted_total, jobs, failed = {}, 0, 0, 0
    recovered_total = 0
    sentinel_checks = []
    for L in ARCHIVE.read_text().strip().split("\n"):
        if not L.strip():
            continue
        rec = json.loads(L)
        jobs += 1
        if rec["status"] != "completed":
            failed += 1
            continue
        rows, shifted, recovered = parse_rows(rec["raw"], rec.get("positions"))
        shifted_total += shifted
        recovered_total += recovered
        for pos, ref, alt, gain, loss in rows:
            key = (pos, ref, alt)
            if key in KNOWN:
                lab, eg, el = KNOWN[key]
                sentinel_checks.append(
                    (lab, gain, loss, eg, el,
                     abs(gain - eg) < TOL and abs(loss - el) < TOL))
            # A sentinel appears in several jobs; keep the strongest call seen.
            prev = scored.get(key)
            if prev is None or max(abs(gain), abs(loss)) > max(abs(prev[0]), abs(prev[1])):
                scored[key] = (gain, loss)

    print(f"jobs archived: {jobs}   failed: {failed}")
    print(f"variants scored: {len(scored)} of {len(meta)}")
    if recovered_total:
        print(f"rows recovered from the multi-gene column shift by gene ID: "
              f"{recovered_total}")
    if shifted_total:
        print(f"rows dropped to multi-gene column shift (C25b): {shifted_total}")

    print("\nSENTINEL GATE")
    if not sentinel_checks:
        print("  no reference-scored variant present yet -- gate cannot be evaluated")
    for lab, g, l, eg, el, ok in sentinel_checks:
        print(f"  {lab:14s} got {g:+.2f}/{l:+.2f}  expected {eg:+.2f}/{el:+.2f}  "
              f"{'PASS' if ok else 'FAIL'}")
    if sentinel_checks and not all(c[5] for c in sentinel_checks):
        sys.exit("\nA sentinel did not reproduce its committed score. Refusing to emit "
                 "an eligibility map: a scan whose control failed cannot tell a true "
                 "negative from a broken instrument.")

    exons = load_exons()
    hits = []
    for key, (gain, loss) in scored.items():
        if max(abs(gain), abs(loss)) < CALL:
            continue
        pos, ref, alt = key
        ex, dist = nearest_exon(pos, exons)
        frameshift = (ex["cds_len"] % 3) != 0
        tier = ("call" if max(abs(gain), abs(loss)) >= CALL_HIGH else "candidate")
        hits.append({**meta.get(key, {}), "tier": tier,
                     "pos": pos, "ref": ref, "alt": alt,
                     "gain": gain, "loss": loss,
                     "nearest_exon": ex["n"], "exon_cds_len": ex["cds_len"],
                     "dist_to_exon": dist,
                     "skip_consequence": "frameshift" if frameshift else "in_frame",
                     "eligibility": ("candidate_null_pending_NMD" if frameshift
                                     else "candidate_hypomorph_protein_made")})

    hits.sort(key=lambda h: -max(abs(h["gain"]), abs(h["loss"])))
    outcols = ["tier", "chrom", "pos", "ref", "alt", "hgvs_c", "consequence",
               "clinvar_significance", "gain", "loss", "nearest_exon",
               "exon_cds_len", "dist_to_exon", "skip_consequence", "eligibility"]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        f.write("\t".join(outcols) + "\n")
        for h in hits:
            f.write("\t".join(str(h.get(c, "")) for c in outcols) + "\n")

    n_call = sum(1 for h in hits if h["tier"] == "call")
    print(f"\nvariants with |score| >= {CALL} (CALL_SCREEN): {len(hits)}")
    print(f"  tier call       |score| >= {CALL_HIGH}: {n_call:4d}   sealed sens 0.392 spec 0.986, precision 0.481 at a 3.2% base rate")
    print(f"  tier candidate  {CALL} to {CALL_HIGH}: {len(hits)-n_call:4d}   sealed sens 0.793 spec 0.872, precision 0.170 -- ~5 wrong per right")
    by = {}
    for h in hits:
        by[h["eligibility"]] = by.get(h["eligibility"], 0) + 1
    for k, v in sorted(by.items()):
        print(f"  {k:36s} {v}")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    print("\nNOTE: this is a PREDICTED eligibility map. Fabry's equivalent is")
    print("assay-determined over 1,386 variants and is used for drug eligibility; a")
    print("prediction is a shortlist, not an amenability call.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
