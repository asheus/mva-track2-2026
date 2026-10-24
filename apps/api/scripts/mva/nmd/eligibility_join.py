#!/usr/bin/env python3
"""Join every known BUB1B variant into one therapeutic-eligibility map.

    python3 -m scripts.mva.nmd.eligibility_join

THE QUESTION. Our therapeutic thesis is "raise the BubR1 the patient still makes". That
is only coherent for a patient who makes some. So for each variant the operative
question is not "is it pathogenic" but **does it leave protein behind to rescue** -- a
therapeutic eligibility question. Fabry has exactly this map for migalastat,
assay-determined across 1,386 variants and used for per-patient drug eligibility.
BUB1B has nothing of the kind. This is the first version for an MVA gene, and it is
PREDICTED, not assayed, which every output states.

WHAT IS JOINED, and the coverage is reported honestly rather than smoothed over:

  nonsense (37)     a calibrated NMD escape probability per variant -> null vs truncated
  non-coding (1005) Pangolin splice call -> frame consequence -> null vs hypomorph
  missense (1494)   structural context for all; computed stability deltas for only 30

THE HONEST LIMIT, stated as a column rather than a footnote. For missense we hold
energetic calls on 30 of 1,494 variants. For the rest we can say which EVIDENCE CLASS
applies -- whether the abundance question is even answerable at that position -- and
nothing more. `evidence_status` carries that distinction on every row:

  direct    a model scored this variant (NMD probability, Pangolin score, or ddG)
  context   structural context only; no per-variant energetic call
  none      the position is modelled too poorly for structure to say anything

That last class is not padding. Our own two-class finding is that stability prediction
separates pathogenic from benign at AUC 0.952 inside the folded core and 0.364 -- worse
than chance -- across binding interfaces. So a confident eligibility call at an
interface would be an abuse of our own measured instrument, and the map refuses to make
one. The gap it leaves is exactly what a deep mutational scan would fill.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[5]
D = ROOT / "docs/mva/data"
NONSENSE = D / "nmd/bub1b_ptc_stratified.tsv"
MISSENSE = D / "nmd/clinvar_missense.tsv"
NONCODING = D / "nmd/noncoding_eligibility.tsv"
NC_ALL = D / "nmd/clinvar_noncoding_verified.tsv"
SWEEP = D / "nmd/pangolin_sweep.jsonl"
REGIONS = ROOT / "docs/mva/data/nmd/bub1b_regions.tsv"
DDG = D / "variants/vus_nominations.json"
RSA = D / "rsa_all.json"
FULL_PDB = D / "neurosnap/bubr1_fulllength.pdb"
OUT = D / "nmd/eligibility_map.tsv"

# RSA bands. Below 20% is conventionally "buried"; our own panel shows burial does not
# by itself separate the mechanism classes, so this is context, not a verdict.
BURIED, EXPOSED = 20.0, 50.0
# AlphaFold's own band: below 50 pLDDT the position is not modelled.
PLDDT_FLOOR = 50.0
# The proband's own alleles, so the map can be checked against the case it came from.
PROBAND = {737: "allele 1 p.Leu737Ter", 1002: "allele 2 p.Asn1002Lys"}


def read_tsv(p):
    if not p.exists():
        return []
    lines = p.read_text().strip().split("\n")
    if len(lines) < 2:
        return []
    cols = lines[0].split("\t")
    return [dict(zip(cols, L.split("\t"))) for L in lines[1:]]


def plddt_by_residue():
    out = {}
    for line in FULL_PDB.read_text().splitlines():
        if line.startswith("ATOM"):
            try:
                out[int(line[22:26])] = float(line[60:66])
            except ValueError:
                pass
    return out


def main():
    for p in (NONSENSE, MISSENSE, NC_ALL, RSA, FULL_PDB):
        if not p.exists():
            sys.exit(f"missing input: {p}")

    rsa = {int(k): v for k, v in json.loads(RSA.read_text()).items()}
    plddt = plddt_by_residue()
    ddg = {d["variant"]: d for d in json.loads(DDG.read_text())} if DDG.exists() else {}

    rows = []

    # ---- nonsense: a calibrated NMD call per variant ----
    for r in read_tsv(NONSENSE):
        esc = float(r["escape_prob"])
        decays = r["escape_pred"].strip().lower() != "escape"
        rows.append({
            "variant_class": "nonsense",
            "variant": f"p.{r['residue']}Ter",
            "residue": int(r["residue"]),
            "clinvar_significance": r.get("clinvar", ""),
            "metric": f"P(escape)={esc:.3f}",
            "eligibility": "NULL_no_protein" if decays else "TRUNCATED_protein_present",
            "evidence_status": "direct",
            "basis": "calibrated NMD model on a measured decay training set",
        })

    # ---- non-coding: splice call -> frame consequence ----
    # A variant that has not been through Pangolin yet is NOT a variant with no splice
    # effect. Conflating the two would turn an unfinished sweep into a wall of false
    # negatives, so the set actually scored is read from the sweep archive and anything
    # outside it is reported as pending.
    # Region comes from OUR canonical transcript, never from ClinVar's consequence
    # field. That field is gene-agnostic: PAK6 overlaps BUB1B's last two exons, so 201
    # variants that are exonic on ENST00000287598 carry a PAK6-derived "intron variant"
    # consequence (C35, C36). bub1b_regions.py derives the region from coordinates and
    # gates itself on reproducing the four reference variants' intronic offsets AND
    # sides, so a mislabelled region cannot reach this file silently.
    regions = {}
    if REGIONS.exists():
        rl = REGIONS.read_text().strip().split("\n")
        rc = rl[0].split("\t")
        for L in rl[1:]:
            d = dict(zip(rc, L.split("\t")))
            regions[(d["chrom"], d["pos"], d["ref"], d["alt"])] = d["tx_region"]
    else:
        sys.exit(f"missing {REGIONS}; run bub1b_regions.py first -- refusing to label "
                 f"variants from ClinVar's gene-agnostic consequence field")

    # The parser is IMPORTED, not reimplemented. This file carried its own third copy
    # until C34, which silently dropped every multi-gene row and so reported the entire
    # PAK6 overlap as pending for as long as it existed -- including after C31 had
    # recovered those 188 variants upstream. One definition, three callers.
    from scripts.mva.nmd.pangolin_sweep_report import parse_rows
    scored = set()
    if SWEEP.exists():
        for L in SWEEP.read_text().strip().split("\n"):
            if not L.strip():
                continue
            rec = json.loads(L)
            if rec.get("status") != "completed":
                continue
            good, _shifted, _recovered = parse_rows(rec.get("raw") or "",
                                                    rec.get("positions"))
            for pos, ref, alt, _g, _l in good:
                scored.add(("chr15", pos, ref, alt))
    nc_called = {}
    for r in read_tsv(NONCODING):
        nc_called[(r["chrom"], r["pos"], r["ref"], r["alt"])] = r
    for r in read_tsv(NC_ALL):
        key = (r["chrom"], r["pos"], r["ref"], r["alt"])
        if (r["chrom"], int(r["pos"]), r["ref"], r["alt"]) not in scored:
            rows.append({
                "variant_class": "splice-scored/" + regions.get(
                    (r["chrom"], r["pos"], r["ref"], r["alt"]),
                    "REGION_UNKNOWN"),
                "variant": r.get("hgvs_c", "") or f"{r['chrom']}:{r['pos']}",
                "residue": "",
                "clinvar_significance": r.get("clinvar_significance", ""),
                "metric": "",
                "eligibility": "PENDING_not_yet_scored",
                "evidence_status": "none",
                "basis": "awaiting its Pangolin job; absence of a call is not a null call",
            })
            continue
        hit = nc_called.get(key)
        if hit:
            frameshift = hit["skip_consequence"] == "frameshift"
            rows.append({
                "variant_class": "splice-scored/" + regions.get(
                    (r["chrom"], r["pos"], r["ref"], r["alt"]),
                    "REGION_UNKNOWN"),
                "variant": r.get("hgvs_c", "") or f"{r['chrom']}:{r['pos']}",
                "residue": "",
                "clinvar_significance": r.get("clinvar_significance", ""),
                "metric": f"gain={hit['gain']} loss={hit['loss']}",
                "eligibility": ("NULL_pending_NMD_of_new_PTC" if frameshift
                                else "HYPOMORPH_protein_made"),
                "evidence_status": "direct",
                "basis": "Pangolin splice call + exon frame arithmetic",
            })
        else:
            rows.append({
                "variant_class": "splice-scored/" + regions.get(
                    (r["chrom"], r["pos"], r["ref"], r["alt"]),
                    "REGION_UNKNOWN"),
                "variant": r.get("hgvs_c", "") or f"{r['chrom']}:{r['pos']}",
                "residue": "",
                "clinvar_significance": r.get("clinvar_significance", ""),
                "metric": "no splice effect called",
                "eligibility": "NO_SPLICE_MECHANISM",
                "evidence_status": "direct",
                "basis": "Pangolin, below call threshold",
            })

    # ---- missense: context for all, energetics for the few we computed ----
    for r in read_tsv(MISSENSE):
        res = int(r["residue"])
        pl = plddt.get(res)
        rs = rsa.get(res)
        d = ddg.get(r["variant"])
        if pl is None or rs is None:
            elig, status, basis, metric = ("CONTEXT_UNAVAILABLE", "none",
                                           "residue absent from the model", "")
        elif pl < PLDDT_FLOOR:
            elig, status = "CONTEXT_UNAVAILABLE", "none"
            basis = f"pLDDT {pl:.0f} -- position not modelled"
            metric = f"pLDDT={pl:.0f}"
        elif rs < BURIED:
            metric = f"RSA={rs:.1f}% pLDDT={pl:.0f}"
            if d:
                metric += (f" ddG(ProteinMPNN)={d['proteinmpnn_ddg']:.2f}"
                           f" ddG(ThermoMPNN)={d['thermompnn_ddg']:.2f}")
                elig, status = "ABUNDANCE_candidate", "direct"
                basis = "buried in a confidently folded core, with computed ddG"
            else:
                elig, status = "ABUNDANCE_question_answerable", "context"
                basis = ("buried in a confidently folded core; ddG not computed for "
                         "this variant")
        elif rs > EXPOSED:
            metric = f"RSA={rs:.1f}% pLDDT={pl:.0f}"
            elig, status = "FUNCTION_class_suspected", "context"
            basis = ("solvent-exposed: our stability instrument is worse than chance "
                     "across interfaces (AUC 0.364), so no abundance call is made")
        else:
            metric = f"RSA={rs:.1f}% pLDDT={pl:.0f}"
            elig, status = "AMBIGUOUS_partially_buried", "context"
            basis = "partially buried; neither class is supported"
        rows.append({
            "variant_class": "missense",
            "variant": r["variant"],
            "residue": res,
            "clinvar_significance": r.get("clinvar_significance", ""),
            "metric": metric,
            "eligibility": elig,
            "evidence_status": status,
            "basis": basis,
        })

    cols = ["variant_class", "variant", "residue", "clinvar_significance", "metric",
            "eligibility", "evidence_status", "basis", "proband_allele"]
    for r in rows:
        r["proband_allele"] = PROBAND.get(r["residue"], "") if r["residue"] != "" else ""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w") as f:
        f.write("\t".join(cols) + "\n")
        for r in rows:
            f.write("\t".join(str(r.get(c, "")).replace("\t", " ") for c in cols) + "\n")

    pending = sum(1 for r in rows if r["eligibility"] == "PENDING_not_yet_scored")
    print(f"{len(rows)} variants joined -> {OUT.relative_to(ROOT)}")
    nc_total = sum(1 for r in rows if r["variant_class"].startswith("splice-scored"))
    print(f"non-coding sweep coverage: {nc_total - pending}/{nc_total} scored, "
          f"{pending} pending\n")
    print("BY VARIANT CLASS")
    by = {}
    for r in rows:
        by[r["variant_class"]] = by.get(r["variant_class"], 0) + 1
    for k, v in sorted(by.items()):
        print(f"  {k:28s} {v:5d}")

    print("\nBY ELIGIBILITY CLASS")
    be = {}
    for r in rows:
        be[r["eligibility"]] = be.get(r["eligibility"], 0) + 1
    for k, v in sorted(be.items(), key=lambda x: -x[1]):
        print(f"  {k:36s} {v:5d}")

    print("\nBY EVIDENCE STATUS -- the coverage this map actually has")
    bs = {}
    for r in rows:
        bs[r["evidence_status"]] = bs.get(r["evidence_status"], 0) + 1
    for k, v in sorted(bs.items(), key=lambda x: -x[1]):
        print(f"  {k:12s} {v:5d}  ({v/len(rows):.1%})")

    print("\nTHE PROBAND'S OWN ALLELES, as the map sees them")
    for r in rows:
        if r["proband_allele"]:
            print(f"  {r['proband_allele']}")
            print(f"      {r['eligibility']}  [{r['evidence_status']}]  {r['metric']}")

    print("\nPREDICTED, NOT ASSAYED. Fabry's equivalent map is determined by a")
    print("GLP-validated assay over 1,386 variants and is used for drug eligibility.")
    print("This is a shortlist and a coverage statement, not an amenability call.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
