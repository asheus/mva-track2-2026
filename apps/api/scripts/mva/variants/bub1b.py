"""One loader for the BUB1B variant corpus, with every known defect handled once.

Six scripts previously parsed the EBI Proteins aggregate independently and each
re-discovered (or missed) the same defects. This module is the single place that
knows how the source is broken. Scripts import it; they do not parse the JSON.

Defects handled, all found by audit and each documented in ATLAS-AUDIT.md:

  D1  consequenceType says "missense" for alleles whose alternativeSequence is "*".
      Six records. Believing the label inflates the pathogenic missense count from
      14 to 19 and turns the nonsense p.Arg770Ter into an apparent missense at the
      codon where our corpus carries R770Q.

  D2  wildType contradicts the reference sequence. Forty-six records, and the bad
      values are C, G, A and T -- nucleotide letters leaking into the amino-acid
      field. Invisible without a sequence check because all four are also valid
      amino-acid codes. One reached a nomination list before this was caught.

  D3  positions beyond residue 1050, up to 3131 -- cDNA coordinates mis-filed into the
      protein position field. Eighty-four records, and the same root cause as D2:
      nucleotide-level data leaking into protein-level fields. Only three carry any
      clinical significance.

  Multi-residue wildType is NOT a defect. Indel records legitimately carry several
  residues (p.Glu736_Leu737insTer has wildType "EL"), and a naive single-residue check
  rejects them -- which discarded a real pathogenic variant at the proband's own L737
  codon before this was fixed.

Nothing is silently dropped: `load()` returns the rejects with reasons, and
`report()` prints the tally so the defect counts stay reproducible.
"""
import json, pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[5]
SOURCE = ROOT / "docs/mva/data/variants/ebi_proteins_O60566_variation.json"
LENGTH = 1050

DOMAINS = [(1, 204, "TPR"), (205, 340, "KEN/ABBA"), (341, 477, "GLEBS"),
           (478, 765, "middle"), (766, 1050, "pseudokinase")]
# Mechanism classes, established in VUS-NOMINATION.md: ddG scores AUC 0.364 in the
# binding-interface domains (worse than chance) and 0.952 in the folded core, because
# interface variants act by losing a partner, not by unfolding.
INTERFACE_DOMAINS = {"TPR", "KEN/ABBA", "GLEBS"}
FOLDED_DOMAINS = {"pseudokinase"}

# Measured WT-like on protein level AND function (Suijkerbuijk 2010, PMC2887387), and a
# passenger on the L844F allele -- which is why databases mis-assert it pathogenic.
MEASURED_BENIGN = {"Q921H"}


def domain(pos):
    return next((n for a, b, n in DOMAINS if a <= pos <= b), "?")


def load():
    raw = json.load(open(SOURCE))
    raw = raw[0] if isinstance(raw, list) else raw
    seq = raw["sequence"]
    kept, rejected = [], []
    for x in raw["features"]:
        if not x["begin"].isdigit():
            rejected.append((x, "non-numeric position")); continue
        pos, wt, mt = int(x["begin"]), x.get("wildType"), x.get("mutatedType")
        if not (1 <= pos <= LENGTH):
            rejected.append((x, "D3 position outside 1-1050")); continue
        if not wt or seq[pos - 1:pos - 1 + len(wt)] != wt:
            rejected.append((x, "D2 wildType contradicts reference sequence")); continue
        # D1: trust the allele, not the label
        consequence = x.get("consequenceType")
        if x.get("alternativeSequence") == "*" or mt == "*":
            consequence = "stop gained"
        sig = sorted({c["type"] for c in x.get("clinicalSignificances", [])})
        name = f"{wt}{pos}{mt}"
        kept.append(dict(
            name=name, pos=pos, wt=wt, mt=mt,
            consequence=consequence, raw_consequence=x.get("consequenceType"),
            mislabelled=consequence != x.get("consequenceType"),
            significance=sig,
            sources=sorted({s for c in x.get("clinicalSignificances", []) for s in (c.get("sources") or [])}),
            diseases=sorted({a.get("name", "") for a in x.get("association", []) if a.get("name")}),
            ftId=x.get("ftId"), domain=domain(pos),
            pubmed=sorted({e.get("source", {}).get("id") for e in x.get("evidences", [])
                           if e.get("source", {}).get("name") == "pubmed"}),
        ))
    return kept, rejected, seq


def label(v):
    """Clinical class, with the one evidence-based override.

    MEASURED_BENIGN beats a database assertion: a direct measurement of protein level
    and function outranks a curator's call that has an identifiable failure mode.
    """
    if v["name"] in MEASURED_BENIGN:
        return "benign"
    if set(v["significance"]) & {"Pathogenic", "Likely pathogenic"}:
        return "pathogenic"
    if set(v["significance"]) & {"Benign", "Likely benign"}:
        return "benign"
    if v["significance"] == ["Variant of uncertain significance"]:
        return "vus"
    return None


def report():
    kept, rejected, seq = load()
    print(f"BUB1B variant corpus: {len(kept)} usable, {len(rejected)} rejected "
          f"of {len(kept) + len(rejected)}")
    for reason, n in Counter(r for _, r in rejected).most_common():
        print(f"   rejected: {n:4d}  {reason}")
    print(f"   D1 consequence corrected in place: {sum(1 for v in kept if v['mislabelled'])}")
    cls = Counter(label(v) for v in kept)
    print(f"   labels: {dict(cls)}")
    mis = [v for v in kept if v["consequence"] == "missense"]
    print(f"   missense: {len(mis)}  "
          f"(pathogenic {sum(1 for v in mis if label(v)=='pathogenic')}, "
          f"benign {sum(1 for v in mis if label(v)=='benign')}, "
          f"vus {sum(1 for v in mis if label(v)=='vus')})")


if __name__ == "__main__":
    report()
