"""Resolve Gate-1 approved-medicine INNs to structures via PubChem.

Produces docs/mva/data/approved_smiles.json, which build_fragments.py fragments into
the screening library and to_approved_drugs.py searches for lookalikes. Both of those
are committed scripts, so their input has to be committed too -- it lived in scratch
for one working session and survived a container restart only by luck.

Resolution is ~44% (646 of 1,485). The misses are not failures: they are biologics,
vaccines, immunoglobulins and combination products, which have no single small-molecule
structure to resolve. Cached and rate-limited to PubChem's 5 requests/second.
"""
import json, pathlib, sys, time, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[5]
GATE1 = ROOT / "apps/api/data/mva/gate1.json"
OUT = ROOT / "docs/mva/data/approved_smiles.json"
URL = ("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{}"
       "/property/SMILES,MolecularWeight/JSON")


def main():
    names = [m["inn"] for m in json.loads(GATE1.read_text())["molecules"]
             if m.get("approval_tier") in ("A", "B")]
    got = json.loads(OUT.read_text()) if OUT.exists() else {}
    print(f"{len(names)} approved medicines; {len(got)} already cached", flush=True)

    for i, n in enumerate(names):
        if n in got:
            continue
        try:
            with urllib.request.urlopen(URL.format(urllib.parse.quote(n, safe="")),
                                        timeout=30) as r:
                p = json.load(r)["PropertyTable"]["Properties"][0]
            got[n] = {"smiles": p.get("SMILES"), "mw": p.get("MolecularWeight"),
                      "cid": p.get("CID")}
        except Exception:
            got[n] = None                      # unresolvable: biologic, vaccine, mixture
        if i % 100 == 0:
            OUT.write_text(json.dumps(got, indent=0))
            print(f"  {i}/{len(names)} resolved={sum(1 for v in got.values() if v)}",
                  flush=True)
        time.sleep(0.21)
    OUT.write_text(json.dumps(got, indent=0))
    print(f"DONE {sum(1 for v in got.values() if v)} of {len(names)} -> {OUT}")


if __name__ == "__main__":
    main()
