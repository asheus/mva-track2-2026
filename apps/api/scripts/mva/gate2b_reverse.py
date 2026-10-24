#!/usr/bin/env python3
"""Gate 2b: the REVERSE mechanism pass, because Gate 2 alone is not complete.

    python3 -m scripts.mva.gate2b_reverse
    python3 -m scripts.mva.gate2b_reverse --write

WHY THIS EXISTS. Gate 2 walks target -> drug using Open Targets'
`drugAndClinicalCandidates`. That field is a curated clinical-candidate list, NOT
an exhaustive drug-target mapping, and the gap is not academic: querying MTOR
returns only PERHEXILINE and RIDAFOROLIMUS as approved, so **sirolimus and
everolimus never appear** — the two drugs most associated with mTOR-mediated
SASP suppression, both of them tier A in our own universe. A funnel that missed
sirolimus while claiming to screen for geroprotective mechanisms would be wrong
in the one place a reviewer would look first.

So this pass walks the other way: drug -> `mechanismsOfAction` -> targets, over
every molecule Gate 1 marked proposable, and unions the result with Gate 2's.
Two directions disagreeing is the point — the union is the answer and the
disagreement is recorded, because a single-direction query that looked clean
would have hidden the defect rather than surfaced it.

Names are resolved through Open Targets' own search rather than string-matched
against ChEMBL, and only exact case-folded name matches are accepted; a fuzzy
match here would quietly attach the wrong mechanism to the right drug.
"""
import argparse, json, pathlib, time, urllib.request

API = "https://api.platform.opentargets.org/api/v4/graphql"
DATA = pathlib.Path(__file__).resolve().parents[2] / "data" / "mva"
G1, G2, OUT = DATA / "gate1.json", DATA / "gate2.json", DATA / "gate2b.json"

from scripts.mva.gate2_mechanism import ARMS  # single definition of the arms

BATCH = 20


def gql(query, variables=None, tries=3):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(API, data=body,
                                 headers={"Content-Type": "application/json"})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                d = json.loads(r.read())
            if "errors" in d:
                raise RuntimeError(d["errors"][0]["message"][:200])
            return d["data"]
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 ** i)


def resolve_batch(names):
    """name -> chembl id, via aliased search calls (BATCH per request)."""
    decl = ",".join(f"$q{i}:String!" for i in range(len(names)))
    body = " ".join(
        f'd{i}:search(queryString:$q{i},entityNames:["drug"],page:{{index:0,size:3}})'
        f"{{hits{{id entity object{{... on Drug{{name}}}}}}}}"
        for i in range(len(names)))
    data = gql(f"query({decl}){{{body}}}", {f"q{i}": n for i, n in enumerate(names)})
    out = {}
    for i, n in enumerate(names):
        for h in (data.get(f"d{i}") or {}).get("hits", []):
            if h["entity"] == "drug" and (h["object"] or {}).get("name", "").lower() == n.lower():
                out[n] = h["id"]
                break
    return out


def mechanisms_batch(ids):
    decl = ",".join(f"$c{i}:String!" for i in range(len(ids)))
    body = " ".join(
        f"m{i}:drug(chemblId:$c{i}){{id name mechanismsOfAction"
        f"{{rows{{actionType mechanismOfAction targets{{approvedSymbol}}}}}}}}"
        for i in range(len(ids)))
    return gql(f"query({decl}){{{body}}}", {f"c{i}": c for i, c in enumerate(ids)})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()

    arm_of = {}
    for arm, targets in ARMS.items():
        for sym, why, mit in targets:
            arm_of.setdefault(sym, []).append((arm, why, mit))

    g1 = json.loads(G1.read_text())["molecules"]
    proposable = [m for m in g1 if m["approval_tier"] in ("A", "B")]
    if a.limit:
        proposable = proposable[:a.limit]
    names = [m["inn"] for m in proposable]
    by_inn = {m["inn"]: m for m in proposable}
    print(f"reverse pass over {len(names)} proposable molecules\n")

    resolved = {}
    for i in range(0, len(names), BATCH):
        chunk = names[i:i + BATCH]
        try:
            resolved.update(resolve_batch(chunk))
        except Exception as e:
            print(f"  resolve batch {i} failed: {e}")
        if (i // BATCH) % 10 == 0:
            print(f"  resolved {len(resolved)}/{min(i+BATCH,len(names))}")
    print(f"resolved to ChEMBL: {len(resolved)}/{len(names)}\n")

    ids = list(resolved.values())
    rev = {}
    id_to_inn = {v: k for k, v in resolved.items()}
    for i in range(0, len(ids), BATCH):
        chunk = ids[i:i + BATCH]
        try:
            data = mechanisms_batch(chunk)
        except Exception as e:
            print(f"  mechanism batch {i} failed: {e}")
            continue
        for j, cid in enumerate(chunk):
            d = data.get(f"m{j}")
            if not d:
                continue
            for row in (d.get("mechanismsOfAction") or {}).get("rows") or []:
                for t in row.get("targets") or []:
                    sym = t.get("approvedSymbol")
                    if sym not in arm_of:
                        continue
                    inn = id_to_inn[cid]
                    h = rev.setdefault(inn.lower(), {
                        "inn": inn, "chembl": cid,
                        "approval_tier": by_inn[inn]["approval_tier"],
                        "atc": by_inn[inn].get("atc") or [],
                        "biosimilar_flag": by_inn[inn].get("biosimilar_flag", False),
                        "arms": {}, "targets": {}, "mitotic_liability": False,
                        "actions": set()})
                    for arm, why, mit in arm_of[sym]:
                        h["arms"].setdefault(arm, [])
                        if sym not in h["arms"][arm]:
                            h["arms"][arm].append(sym)
                        h["targets"][sym] = why
                        h["mitotic_liability"] |= mit
                    h["actions"].add(row.get("actionType") or "?")
    for v in rev.values():
        v["actions"] = sorted(v["actions"])

    g2 = {c["inn"].lower(): c for c in json.loads(G2.read_text())["candidates"]}
    only_fwd = sorted(set(g2) - set(rev))
    only_rev = sorted(set(rev) - set(g2))
    print(f"forward (gate 2) : {len(g2)}")
    print(f"reverse (gate 2b): {len(rev)}")
    print(f"union            : {len(set(g2) | set(rev))}")
    print(f"\nfound ONLY by reverse ({len(only_rev)}): {', '.join(only_rev)}")
    print(f"\nfound ONLY by forward ({len(only_fwd)}): {', '.join(only_fwd)}")

    if a.write:
        OUT.write_text(json.dumps(
            {"gate": "2b", "api": API,
             "resolved": len(resolved), "attempted": len(names),
             "forward_only": only_fwd, "reverse_only": only_rev,
             "count": len(rev),
             "candidates": sorted(rev.values(), key=lambda r: r["inn"])}, indent=1) + "\n")
        print(f"\nwrote {OUT.name}")


if __name__ == "__main__":
    main()
