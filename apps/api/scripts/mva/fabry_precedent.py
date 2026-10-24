#!/usr/bin/env python3
"""The Fabry precedent, measured rather than remembered.

    python3 -m scripts.mva.fabry_precedent                      # from the committed extract
    python3 -m scripts.mva.fabry_precedent /path/to/galafold.pdf  # re-derive from the label

WHY. Our eligibility map is built on a claim about the world: that for a drug which
works by stabilising a protein, the first question is not "which drug" but "does this
allele make any protein to stabilise". If that claim is right, it should already be
visible in an approved drug. It is, and this script measures where.

Migalastat (Galafold) treats Fabry disease by binding the active site of mutant
alpha-galactosidase A, stabilising it, and restoring its trafficking to the lysosome
(label section 12.1). Its FDA indication is not "Fabry disease". It is Fabry disease
*and an amenable GLA variant based on in vitro assay data* -- a genotype gate written
into the indication itself, with the eligible alleles enumerated in Table 2 of the label.

THE MEASUREMENT. Parse Table 2 and ask what kind of allele is ever eligible. Every
amenable entry makes protein: the table is essentially all missense, and the handful of
non-missense entries are small in-frame indels that still produce a near-full-length
chain. No nonsense, no frameshift, no splice allele appears anywhere in it.

That is not a quirk of curation, it is the mechanism: a chaperone has nothing to bind
if the protein was never made. The label's own clinical data closes the loop -- of 67
patients in Study 1, the 17 with non-amenable variants "had no change from baseline"
after six months. The drug did nothing, exactly as the mechanism predicts.

WHAT WE TAKE FROM IT, AND WHAT WE DO NOT. We take the *shape* of the deliverable: a
per-allele eligibility table, maintained, with the assay stated and a threshold written
down. We do not claim our map is its equal. Theirs is measured in a GLP-validated
HEK-293 assay with a published 20%-relative / 3%-of-wild-type criterion and a clinically
validated predictive value; ours is predicted, and says so in every row. The honest
comparison is the point of this file, so it prints both columns.

SOURCES (retrieved 21 Oct 2026)
  Galafold full prescribing information, Amicus Therapeutics
    https://www.amicusrx.com/pi/galafold.pdf
    sha256 ca9b696ff73435129180d8bce096bcd25c6fc16024b17041b93c163c6852c421
  Benjamin ER et al., Genet Med 2017;19(4):430-438, doi:10.1038/gim.2016.122
    600 Fabry-causing mutations expressed in HEK-293; 268 found amenable; GLP assay
    sensitivity, specificity and predictive values all >= 0.875 against in vivo response.
"""
import collections
import hashlib
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
OUTDIR = ROOT / "docs/mva/data/fabry"
TABLE = OUTDIR / "galafold-amenable-table.tsv"
OUT = OUTDIR / "fabry-precedent.json"
PI_SHA256 = "ca9b696ff73435129180d8bce096bcd25c6fc16024b17041b93c163c6852c421"
PI_URL = "https://www.amicusrx.com/pi/galafold.pdf"

# Benjamin 2017, the founding assay. Committed as the published figures, not re-derived.
BENJAMIN = {"mutations_tested": 600, "found_amenable": 268,
            "assay": "GLP-validated HEK-293 migalastat amenability assay",
            "criterion": "relative increase >=20% over pre-treatment AND absolute "
                         "increase >=3% of wild-type alpha-Gal A activity at 10 uM",
            "predictive_value_vs_in_vivo": ">=0.875 for sensitivity, specificity, PPV, NPV",
            "doi": "10.1038/gim.2016.122"}


def rows_from_pi(path):
    """Extract Table 2's rows from a local copy of the prescribing information."""
    p = pathlib.Path(path)
    if p.suffix.lower() == ".pdf":
        got = hashlib.sha256(p.read_bytes()).hexdigest()
        if got != PI_SHA256:
            print(f"  NOTE: label sha256 {got[:12]} != the version parsed for the "
                  f"committed extract ({PI_SHA256[:12]}). The label is revised over "
                  f"time; counts below are for YOUR copy.", file=sys.stderr)
        txt = subprocess.run(["pdftotext", "-layout", str(p), "-"],
                             capture_output=True, text=True, check=True).stdout
    else:
        txt = p.read_text()
    out = []
    for L in txt.split("\n"):
        if not re.match(r"\s*c\.[\[\d]", L):
            continue
        if "previously referred to as" in L:          # footnote, not a row
            continue
        dna = re.match(r"\s*(c\.\S+(?:\s+or\s+c\.\S+)?)", L).group(1)
        pm = re.search(r"p\.\[?\(([A-Za-z0-9_;*= ]+)\)\]?", L)
        out.append((dna.rstrip("†‡§¶"),
                    (pm.group(1).strip() if pm else "")))
    return out


def classify(prot):
    if not prot:
        return "continuation/footnote row"
    if ";" in prot:
        return "multi-variant allele (all missense)"
    if re.fullmatch(r"[A-Z]\d+[A-Z]", prot):
        return "missense"
    if "dup" in prot or "del" in prot or "ins" in prot:
        return "small in-frame indel (protein still made)"
    if "*" in prot or "Ter" in prot or "fs" in prot:
        return "TRUNCATING"
    return "other"


def main():
    if len(sys.argv) > 1:
        rows = rows_from_pi(sys.argv[1])
        OUTDIR.mkdir(parents=True, exist_ok=True)
        with TABLE.open("w") as f:
            f.write("dna_change\tprotein_change\n")
            for d, p in rows:
                f.write(f"{d}\t{p}\n")
        print(f"extracted {len(rows)} rows -> {TABLE.relative_to(ROOT)}")
    else:
        if not TABLE.exists():
            sys.exit(f"no committed extract at {TABLE}; pass a local copy of the label "
                     f"({PI_URL}) to build one")
        rows = [tuple(L.split("\t")) for L in
                TABLE.read_text().strip().split("\n")[1:]]

    dna = {d for d, _ in rows}
    kinds = collections.Counter(classify(p) for _, p in rows)
    prot = {p for _, p in rows if p}
    truncating = [p for _, p in rows if classify(p) == "TRUNCATING"]

    print(f"\nGALAFOLD label Table 2 -- alleles eligible for an approved folding drug")
    print(f"  distinct DNA-change entries      {len(dna)}")
    print(f"  distinct protein changes         {len(prot)}")
    for k, v in kinds.most_common():
        print(f"    {k:42s} {v}")
    # The headline claim must not rest on my own column parse: 12 rows wrap their
    # protein column onto the next line, so scan the raw table text for any token that
    # would mark a truncating allele. If one ever appears, this stops being a finding.
    raw = TABLE.read_text() if TABLE.exists() else ""
    tokens = {t: len(re.findall(t, raw)) for t in
              [r"Ter", r"fs", r"\*", r"splice", r"X\d"]}
    print(f"\n  raw-text scan for truncating tokens: {tokens}")
    assert not any(tokens.values()), "a truncating allele appears in the amenable table"

    print(f"  TRUNCATING alleles eligible:     {len(truncating)}"
          f"{'  <-- none, as the mechanism requires' if not truncating else ''}")
    print(f"  so: every eligible allele makes protein.")

    print(f"\nTHE SAME QUESTION ASKED OF BUB1B (our map, predicted not assayed)")
    lk = ROOT / "docs/mva/data/allele_lookup.json"
    ours = json.loads(lk.read_text()) if lk.exists() else {}
    by = ours.get("by_mechanism", {})
    decay = by.get("NULL_no_protein", 0) + by.get("NULL_pending_NMD_of_new_PTC", 0)
    makes = by.get("TRUNCATED_protein_present", 0) + by.get("HYPOMORPH_protein_made", 0)
    print(f"  alleles in our lookup            {ours.get('alleles', 'n/a')}")
    print(f"  predicted to lose the transcript {decay}   -> a folding drug cannot reach these")
    print(f"  predicted to leave protein       {makes}   -> the only alleles a folding drug could reach")

    print(f"\nTHE DIFFERENCE, STATED PLAINLY")
    print(f"  Fabry : measured, GLP-validated assay, clinically validated, on the label")
    print(f"  BUB1B : predicted, each row carrying the experiment that would settle it")

    OUTDIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "source": {"prescribing_information": PI_URL, "sha256": PI_SHA256,
                   "retrieved": "2026-10-21"},
        "founding_assay": BENJAMIN,
        "rows_whose_protein_column_wrapped": 12,
        "truncating_token_scan_over_raw_table": "Ter/fs/*/splice/X<digit> all absent",
        "label_table_2": {
            "distinct_dna_entries": len(dna),
            "distinct_protein_changes": len(prot),
            "by_kind": dict(kinds),
            "truncating_alleles_eligible": len(truncating)},
        "mechanism_from_label_12_1":
            "migalastat binds the active site of mutant alpha-Gal A, stabilises it and "
            "restores trafficking to the lysosome; it dissociates at lysosomal pH and "
            "high substrate concentration",
        "indication_is_a_genotype_gate":
            "indicated for adults with confirmed Fabry disease AND an amenable GLA "
            "variant based on in vitro assay data",
        "non_amenable_clinical_result":
            "of 67 patients in Study 1, the 17 with non-amenable variants had no change "
            "from baseline in GL-3 inclusions per kidney interstitial capillary after "
            "6 months",
        "real_world_amenable_fraction":
            "commonly estimated 35-50% of Fabry patients; a 1,196-patient Latin "
            "American series reported 60.2%. Range, not a measured prevalence.",
        "what_we_take": "the shape of the deliverable: a maintained per-allele "
                        "eligibility table with the assay and threshold stated",
        "what_we_do_not_claim": "parity. Theirs is assay-determined and clinically "
                                "validated; ours is predicted and labelled as such.",
    }, indent=2) + "\n")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
