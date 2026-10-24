#!/usr/bin/env python3
"""Gate 2 of the MVA Track 2 funnel: which approved drugs reach a mechanism arm.

    python3 -m scripts.mva.gate2_mechanism
    python3 -m scripts.mva.gate2_mechanism --write

WHY THIS EXISTS. Gate 1 leaves ~1,500 approved molecules; nothing about that set
is specific to this child. This gate asks the only question that makes a molecule
a candidate at all: does it act on a target that a documented MVA mechanism runs
through? It works target-first, not molecule-first — the arms name the biology,
Open Targets names the drugs that reach it, and the funnel keeps the intersection
with what Gate 1 established is actually approved and obtainable.

Target identifiers are RESOLVED AT RUN TIME from the gene symbol via the Open
Targets search API rather than hard-coded, so a stale or mistyped Ensembl ID
cannot silently point the query at the wrong gene.

THE ARMS. Every target carries its own reason; a target without one does not
belong in a gate that has to survive a rigor review.

A  aneuploidy -> senescence -> SASP. The best-supported arm. Chronically
   aneuploid cells enter senescence and secrete an IL-6/TNF-dominated
   inflammatory programme.

B  cancer predisposition. Yost et al., Nat Genet 2017 (doi:10.1038/ng.3883)
   establish that embryonal tumour risk in MVA tracks the SEVERITY of
   spindle-assembly-checkpoint impairment and is genotype-specific: biallelic
   BUB1B or TRIP13 carry high risk, CEP57 and idiopathic MVA do not. This child
   has biallelic BUB1B, so this arm is evidenced for this genotype.

C  ciliopathy. Miyamoto & Matsuura, Oncotarget 2015 (doi:10.18632/oncotarget.5244)
   argue the mitotic kinases and kinesins disrupted in MVA also regulate the
   primary cilium. Hypothesis-generating, not established.

A STRUCTURAL WARNING THIS GATE IS DESIGNED TO SURFACE, not to hide. The obvious
pharmacology for arms B and C — AURKA, PLK1, TTK/MPS1, KIF11, WEE1 — is mitotic
machinery, and mitotic machinery is precisely what is already broken in this
child. A spindle-checkpoint-impaired patient is the worst possible recipient of a
drug that further perturbs mitosis. Those targets are therefore carried here
DELIBERATELY and flagged `mitotic_liability`, so that Gate 3 is seen to reject
them on the evidence rather than the funnel quietly never proposing them. A
safety gate that is never given anything dangerous to refuse proves nothing.
"""
import argparse, json, pathlib, time, urllib.request

API = "https://api.platform.opentargets.org/api/v4/graphql"
DATA = pathlib.Path(__file__).resolve().parents[2] / "data" / "mva"
IN, OUT = DATA / "gate1.json", DATA / "gate2.json"

ARMS = {
    "A_senescence_sasp": [
        ("IL6",     "core SASP cytokine; the secretome's dominant signal", False),
        ("IL6R",    "receptor arm of the same axis; tocilizumab/sarilumab reach it", False),
        ("TNF",     "second dominant SASP cytokine; large approved biosimilar class", False),
        ("IL1B",    "upstream SASP amplifier; CANTOS gives a hard clinical precedent", False),
        ("IL1R1",   "receptor arm of IL-1 signalling; anakinra reaches it", False),
        ("JAK1",    "transduces IL-6 family signalling into the SASP programme", False),
        ("JAK2",    "as JAK1; ruxolitinib reaches both", False),
        ("MTOR",    "geroprotection; rapamycin suppresses the SASP", False),
        ("FKBP1A",   "FKBP12. Rapalogs are annotated HERE, not on MTOR: sirolimus "
                     "and everolimus bind FKBP12 and the complex inhibits mTORC1. "
                     "Omitting it made the funnel miss both - see gate2b docstring", False),
        ("BCL2",    "senolytic axis - senescent cells depend on BCL2 family survival", False),
        ("BCL2L1",  "BCL-xL, the navitoclax senolytic target", False),
    ],
    "B_cancer_predisposition": [
        ("MDM2",    "p53 restraint; CIN cells are p53-pathway dependent", False),
        ("TP53",    "the damage response aneuploid cells must evade", False),
        ("PTGS2",   "COX-2 chemoprevention precedent in hereditary cancer syndromes", False),
        ("AURKA",   "mitotic kinase - carried to be REFUSED by Gate 3", True),
        ("PLK1",    "mitotic kinase - carried to be REFUSED by Gate 3", True),
        ("TTK",     "MPS1, the checkpoint kinase itself - carried to be REFUSED", True),
        ("KIF11",   "mitotic kinesin - carried to be REFUSED by Gate 3", True),
        ("WEE1",    "G2/M checkpoint - carried to be REFUSED by Gate 3", True),
    ],
    "C_ciliopathy": [
        ("HDAC6",   "tubulin deacetylase governing cilium disassembly", False),
        ("AURKA",   "the AURKA-HDAC6 cilium-disassembly axis; also mitotic", True),
    ],
}


def gql(query, variables=None, tries=3):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=body,
                                 headers={"Content-Type": "application/json"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                d = json.loads(r.read())
            if "errors" in d:
                raise RuntimeError(d["errors"][0]["message"][:200])
            return d["data"]
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 ** i)


RESOLVE = """query($q:String!){search(queryString:$q,entityNames:["target"],page:{index:0,size:5})
{hits{id entity object{... on Target{approvedSymbol}}}}}"""

DRUGS = """query($id:String!){target(ensemblId:$id){approvedSymbol
drugAndClinicalCandidates{count rows{maxClinicalStage drug{id name drugType}}}}}"""


def resolve(symbol):
    for h in gql(RESOLVE, {"q": symbol})["search"]["hits"]:
        if h["entity"] == "target" and (h["object"] or {}).get("approvedSymbol") == symbol:
            return h["id"]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    if not IN.exists():
        raise SystemExit(f"missing {IN} — run gate1_approved.py --write first")
    g1 = json.loads(IN.read_text())["molecules"]
    proposable = {m["inn"].lower(): m for m in g1 if m["approval_tier"] in ("A", "B")}

    hits, unresolved = {}, []
    for arm, targets in ARMS.items():
        print(f"\n=== {arm} ===")
        for symbol, why, mitotic in targets:
            eid = resolve(symbol)
            if not eid:
                unresolved.append(symbol)
                print(f"  {symbol:<8} UNRESOLVED")
                continue
            rows = gql(DRUGS, {"id": eid})["target"]["drugAndClinicalCandidates"]["rows"]
            approved = [r for r in rows if r["maxClinicalStage"] == "APPROVAL"]
            matched = []
            for r in approved:
                inn = r["drug"]["name"].lower()
                if inn in proposable:
                    matched.append(inn)
                    h = hits.setdefault(inn, {
                        "inn": proposable[inn]["inn"],
                        "approval_tier": proposable[inn]["approval_tier"],
                        "atc": proposable[inn].get("atc") or [],
                        "biosimilar_flag": proposable[inn].get("biosimilar_flag", False),
                        "arms": {}, "targets": {}, "mitotic_liability": False})
                    h["arms"].setdefault(arm, []).append(symbol)
                    h["targets"][symbol] = why
                    h["mitotic_liability"] |= mitotic
            flag = "  [mitotic]" if mitotic else ""
            print(f"  {symbol:<8} {eid:<16} approved={len(approved):<3} "
                  f"in-universe={len(matched)}{flag}")
            if matched:
                print(f"           -> {', '.join(sorted(matched))}")

    print(f"\nGate 2 candidates: {len(hits)}")
    clean = {k: v for k, v in hits.items() if not v["mitotic_liability"]}
    print(f"  carrying a mitotic liability (for Gate 3 to refuse): "
          f"{len(hits) - len(clean)}")
    print(f"  without one: {len(clean)}")
    print(f"  biosimilar available: {sum(1 for v in hits.values() if v['biosimilar_flag'])}")
    if unresolved:
        print(f"  UNRESOLVED SYMBOLS: {unresolved}")

    if a.write:
        OUT.write_text(json.dumps(
            {"gate": 2, "api": API, "arms": {k: [t[0] for t in v] for k, v in ARMS.items()},
             "count": len(hits), "unresolved": unresolved,
             "candidates": sorted(hits.values(), key=lambda r: r["inn"])}, indent=1) + "\n")
        print(f"\nwrote {OUT.name}")


if __name__ == "__main__":
    main()
