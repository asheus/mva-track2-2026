"""Step 4 of the Millet protocol: fragment hits -> approved medicines.

Millet took his best fragments and searched a library of approved drugs for similar
compounds, which is how an antifungal (ciclopirox) turned up as a stabiliser of
uroporphyrinogen III synthase. Two routes here, answering different questions:

  PARENTAGE   which approved drugs this fragment is literally a piece of. Exact, and
              free, because the library was built by fragmenting those drugs.
  SIMILARITY  which approved drugs resemble it but did not contain it. Morgan
              fingerprints, Tanimoto. This is Millet's own step, and the only one
              that can reach a molecule parentage cannot.

Reads millet_ranked.json (written by analyse.py, which owns the statistics) and writes
millet_hits.json. It reports ONLY fragments that cleared the empirical false-positive
gate; if none did, it says so and writes an empty list rather than ranking noise.

NOTHING HERE IS A CANDIDATE. A fragment that docks well is a starting point for a
binding assay, not a molecule to give a child.
"""
import json, pathlib, sys
from rdkit import Chem, DataStructs, RDLogger
from rdkit.Chem import rdFingerprintGenerator
RDLogger.DisableLog("rdApp.*")

ROOT = pathlib.Path(__file__).resolve().parents[5]
DATA = ROOT / "docs/mva/data"
FPR_MAX = 0.01
SIM_MIN = 0.35
GEN = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)


def fp(smiles):
    m = Chem.MolFromSmiles(smiles)
    return GEN.GetFingerprint(m) if m else None


def main():
    ranked = json.loads((DATA / "millet_ranked.json").read_text())
    hits = [h for h in ranked if h.get("fpr") is not None and h["fpr"] <= FPR_MAX]
    print(f"{len(ranked)} ranked fragments; {len(hits)} clear FPR <= {FPR_MAX:.0%}\n")

    if not hits:
        (DATA / "millet_hits.json").write_text(json.dumps([], indent=1))
        print("No fragment survives the decoy-derived null. There is nothing to map to")
        print("approved drugs, and mapping the best non-significant fragment anyway")
        print("would manufacture a lead out of a negative result.")
        return

    drugs = {k: v["smiles"] for k, v in
             json.loads((DATA / "approved_smiles.json").read_text()).items()
             if v and v.get("smiles")}
    drug_fps = {n: f for n, f in ((n, fp(s)) for n, s in drugs.items()) if f is not None}

    out = []
    print(f"{'rank':>4s} {'allo':>6s} {'delta':>6s} {'FPR':>7s} {'par':>4s}  fragment")
    for i, h in enumerate(hits, 1):
        f = fp(h["smiles"])
        sims = sorted(((DataStructs.TanimotoSimilarity(f, g), n)
                       for n, g in drug_fps.items()), reverse=True)
        near = [(n, round(s, 3)) for s, n in sims[:6] if s >= SIM_MIN]
        print(f"{i:4d} {h['allosteric']:6.2f} {h['delta']:+6.2f} {h['fpr']:7.4f} "
              f"{h['n_parents']:4d}  {h['smiles']}")
        print(f"       parents: {', '.join(h['parents'][:5])}"
              f"{' ...' if len(h['parents']) > 5 else ''}")
        if near:
            print(f"       similar approved: {', '.join(f'{n} ({s})' for n, s in near[:4])}")
        out.append({**h, "similar_approved": near})

    (DATA / "millet_hits.json").write_text(json.dumps(out, indent=1))
    print(f"\nwrote {DATA / 'millet_hits.json'}")


if __name__ == "__main__":
    main()
