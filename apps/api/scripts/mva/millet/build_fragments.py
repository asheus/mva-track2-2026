"""Step 2 of the Millet protocol: the fragment library.

Millet screened 2,500 diverse commercial fragments, then searched approved drugs for
compounds resembling the hits. We inverted the order: the library is built BY
FRAGMENTING THE APPROVED MEDICINES THEMSELVES (BRICS bond decomposition), so every
fragment carries the parent drugs it came from.

That inversion matters here. Millet's step 4 -- fragment hit to approved drug -- is a
similarity search that can fail to land on anything approved. Fragmenting approved
drugs makes the mapping exact and guarantees that a hit has at least one parent that
already cleared Gate 1 of this project's own safety funnel. For a child, the approved
set is the only set worth searching.

Fragments are filtered on Astex's rule of three (Congreve et al., Drug Discov Today
2003): MW <= 300, cLogP <= 3, donors <= 3, acceptors <= 3, rotatable bonds <= 3.
"""
import collections, json, pathlib, sys
from rdkit import Chem, RDLogger
from rdkit.Chem import BRICS, Crippen, Descriptors, Lipinski
RDLogger.DisableLog("rdApp.*")

ROOT = pathlib.Path(__file__).resolve().parents[5]
OUT = ROOT / "docs/mva/data/millet_fragments.json"

MW_MAX, LOGP_MAX, HBD_MAX, HBA_MAX, ROT_MAX = 300.0, 3.0, 3, 3, 3
MIN_HEAVY = 8           # below this a fragment is a functional group, not a probe


def rule_of_three(mol):
    return (Descriptors.MolWt(mol) <= MW_MAX
            and Crippen.MolLogP(mol) <= LOGP_MAX
            and Lipinski.NumHDonors(mol) <= HBD_MAX
            and Lipinski.NumHAcceptors(mol) <= HBA_MAX
            and Lipinski.NumRotatableBonds(mol) <= ROT_MAX
            and mol.GetNumHeavyAtoms() >= MIN_HEAVY)


def clean(frag):
    """BRICS leaves [n*] dummy attachment atoms; cap them with hydrogen.

    The isotope label MUST be cleared too. BRICS encodes the bond environment as the
    dummy's isotope ([8*], [16*]); setting only the atomic number turns those into
    [8H] and [16H] -- isotope-labelled hydrogens, which survive sanitisation, change
    the canonical SMILES, and so break both deduplication and fingerprint similarity.
    """
    m = Chem.MolFromSmiles(frag)
    if m is None:
        return None
    # Keep only the largest connected component. BRICS does not break ionic bonds, so
    # salt forms among the approved drugs (hydrochlorides, sodium salts) survive intact
    # as multi-component "fragments". A counterion is not part of the binding entity,
    # and Meeko refuses a disconnected molecule outright -- which killed a whole screen.
    if len(Chem.GetMolFrags(m)) > 1:
        m = max(Chem.GetMolFrags(m, asMols=True, sanitizeFrags=False),
                key=lambda f: f.GetNumHeavyAtoms())
    ed = Chem.RWMol(m)
    for a in list(ed.GetAtoms()):
        if a.GetAtomicNum() == 0:
            a.SetAtomicNum(1)
            a.SetIsotope(0)
    try:
        out = Chem.RemoveHs(ed.GetMol())
        Chem.SanitizeMol(out)
        return out
    except Exception:
        return None


def main():
    src = json.loads((ROOT / "docs/mva/data/approved_smiles.json").read_text())
    drugs = {k: v["smiles"] for k, v in src.items() if v and v.get("smiles")}
    print(f"{len(drugs)} approved medicines with a structure")

    parents = collections.defaultdict(set)
    bad = 0
    for name, smi in drugs.items():
        mol = Chem.MolFromSmiles(smi)
        if mol is None or mol.GetNumHeavyAtoms() > 100:      # skip peptides/polymers
            bad += 1
            continue
        try:
            pieces = BRICS.BRICSDecompose(mol, minFragmentSize=MIN_HEAVY, returnMols=False)
        except Exception:
            bad += 1
            continue
        for p in pieces:
            m = clean(p)
            if m is not None and rule_of_three(m):
                parents[Chem.MolToSmiles(m)].add(name)
    print(f"{bad} unparseable or oversized; {len(parents)} unique rule-of-three fragments")

    lib = [{"smiles": s, "parents": sorted(p), "n_parents": len(p)}
           for s, p in parents.items()]
    lib.sort(key=lambda f: (-f["n_parents"], f["smiles"]))
    OUT.write_text(json.dumps(lib, indent=1))
    print(f"wrote {OUT}")
    print(f"\nmost widely-used fragments (a proxy for medicinal-chemistry tolerance):")
    for f in lib[:8]:
        print(f"  {f['n_parents']:3d} parents  {f['smiles']}")


if __name__ == "__main__":
    main()
