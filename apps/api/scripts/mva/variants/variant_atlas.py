"""Every BUB1B variant we can reach, normalised into one table.

Sources, all committed under docs/mva/data/variants/:
  ebi_proteins_O60566_variation.json  EBI Proteins API, which aggregates ClinVar,
                                      UniProt/humsavar, dbSNP, COSMIC and gnomAD
  literature_addendum.json            variants recovered from primary papers via
                                      Paperclip that the aggregate does not carry

One correction is applied on load. The EBI aggregate labels five genuine nonsense
variants as "missense" -- their alternativeSequence is "*". Trusting the label
inflates the missense count by a third and turns p.Arg770Ter into a benign-looking
missense at the codon where our own corpus carries R770Q.
"""
import json, pathlib, sys
from collections import Counter

DATA = pathlib.Path(__file__).resolve().parents[5] / "docs/mva/data/variants"
DOMAINS = [(1, 204, "TPR"), (205, 340, "KEN/ABBA + linker"), (341, 477, "GLEBS/Bub3-binding"),
           (478, 765, "middle / unassigned"), (766, 1050, "pseudokinase")]


def domain(p):
    for a, b, n in DOMAINS:
        if a <= p <= b:
            return n
    return "?"


def consequence(x):
    """The aggregate's consequenceType, corrected against the actual allele."""
    if x.get("alternativeSequence") == "*" or x.get("mutatedType") == "*":
        return "stop gained"
    return x.get("consequenceType", "?")


def load_ebi():
    d = json.load(open(DATA / "ebi_proteins_O60566_variation.json"))
    d = d[0] if isinstance(d, list) else d
    out = []
    for x in d["features"]:
        if not x["begin"].isdigit():
            continue
        sigs = sorted({c["type"] for c in x.get("clinicalSignificances", [])})
        prot = next((l["loc"] for l in x.get("locations", []) if l.get("loc", "").startswith("p.")), None)
        out.append(dict(
            pos=int(x["begin"]),
            protein=prot or f"{x.get('wildType','?')}{x['begin']}{x.get('mutatedType','?')}",
            consequence=consequence(x),
            raw_consequence=x.get("consequenceType"),
            significance=sigs,
            diseases=sorted({a.get("name", "") for a in x.get("association", []) if a.get("name")}),
            ftId=x.get("ftId"),
            pubmed=sorted({e.get("source", {}).get("id") for e in x.get("evidences", [])
                           if e.get("source", {}).get("name") == "pubmed"}),
            domain=domain(int(x["begin"])),
        ))
    return out


def main():
    ebi = load_ebi()
    lit = json.load(open(DATA / "literature_addendum.json"))["variants"]
    print(f"EBI aggregate: {len(ebi)} variants across the 1,050-residue protein")
    print(f"Literature addendum: {len(lit)} entries, "
          f"{sum(1 for v in lit if v['novel_to_corpus'])} not in the aggregate\n")

    fixed = [v for v in ebi if v["consequence"] != v["raw_consequence"]]
    print(f"consequence-type corrections applied: {len(fixed)}")
    for v in fixed:
        print(f"    {v['protein']:16s} aggregate said '{v['raw_consequence']}', allele is a stop codon")

    plp = [v for v in ebi if any(s in ("Pathogenic", "Likely pathogenic") for s in v["significance"])]
    print(f"\npathogenic / likely pathogenic: {len(plp)}")
    print("  corrected consequence mix:", dict(Counter(v["consequence"] for v in plp)))
    print("  uncorrected would have been:", dict(Counter(v["raw_consequence"] for v in plp)))

    print("\n  by domain:")
    for _, _, name in DOMAINS:
        d = [v for v in plp if v["domain"] == name]
        if not d:
            continue
        mis = [v for v in d if v["consequence"] == "missense"]
        print(f"    {name:22s} {len(d):3d} total, {len(mis):2d} missense, {len(d)-len(mis):2d} truncating")

    mis = sorted([v for v in plp if v["consequence"] == "missense"], key=lambda v: v["pos"])
    print(f"\n  the {len(mis)} pathogenic MISSENSE variants -- the only ones a stability")
    print("  predictor can be scored against, and the reason the pseudokinase domain matters:")
    for v in mis:
        print(f"    {v['protein']:16s} {v['domain']:22s} {'/'.join(v['significance'])}")

    ben = [v for v in ebi if any(s in ("Benign", "Likely benign") for s in v["significance"])]
    print(f"\nbenign / likely benign: {len(ben)}  "
          f"({len([v for v in ben if v['domain']=='pseudokinase'])} in the pseudokinase domain)")
    curated = [v for v in ebi if v["ftId"]]
    print(f"UniProt-curated with literature evidence: {len(curated)}")

    # the constraint question: is N1002 special, or is absence common?
    seen = {v["pos"] for v in ebi}
    pk_missing = [p for p in range(766, 1051) if p not in seen]
    print(f"\npositions in the pseudokinase domain with NO recorded variant of any kind: "
          f"{len(pk_missing)} of 285")
    print(f"  is 1002 among them? {'yes' if 1002 in pk_missing else 'no'} -- "
          f"absence at any one position is therefore {len(pk_missing)/285:.0%} likely by chance, not evidence")


if __name__ == "__main__":
    main()
