"""Does this docking pipeline actually work? Re-dock crystal complexes and measure RMSD.

Everything downstream rests on a receptor PDBQT written by hand in prep_receptor.py --
atom typing and charges I wrote myself rather than taking from a prepared tool. If that
typing is wrong, every score in the screen is noise wearing a decimal point, and no
amount of decoy control would reveal it: a systematically mistyped receptor is wrong at
every box equally.

THE TEST. Take protein-ligand crystal structures, strip the ligand, rebuild the receptor
through OUR prep, dock the ligand back in from SMILES (fresh conformer, no memory of the
crystal pose), and measure symmetry-corrected RMSD to where it actually sits. The field's
convention is that <2.0 A counts as a recovered pose.

This validates the PIPELINE, not the BubR1 model -- a predicted structure can still be
wrong about its own pockets. It answers only: does the machinery reproduce a known answer.
"""
import json, os, pathlib, sys, tempfile, urllib.request
import numpy as np
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem, rdMolAlign
RDLogger.DisableLog("rdApp.*")

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import prep_receptor
from dock import Site, ligand_pdbqt

# Re-downloadable scratch: PDBe entries and chem-comp definitions. Not committed, and
# not tied to a session path -- a missing cache just costs one fetch.
CACHE = pathlib.Path(os.environ.get("MVA_PDB_CACHE",
                                    pathlib.Path(tempfile.gettempdir()) / "mva_pdb"))
CACHE.mkdir(parents=True, exist_ok=True)

# (PDB id, ligand chem-comp id, what it tests)
CASES = [
    ("3PTB", "BEN", "trypsin + benzamidine -- the classic easy benchmark"),
    ("1M17", "AQ4", "EGFR kinase + erlotinib -- an ATP-site inhibitor"),
    ("1STP", "BTN", "streptavidin + biotin -- deep buried pocket"),
    ("2HYY", "STI", "ABL kinase + imatinib -- large and very flexible"),
]


def fetch(url, dest):
    if not dest.exists():
        dest.write_bytes(urllib.request.urlopen(url, timeout=120).read())
    return dest


def ligand_smiles(ccd):
    """SMILES for a chem-comp id, from PDBe.

    RCSB is refused by this environment's network policy (the proxy answers 403 to
    CONNECT for data.rcsb.org and files.rcsb.org). PDBe serves the same wwPDB content
    and is permitted, so both the structures and the ligand definitions come from EBI.
    """
    d = json.loads(fetch(f"https://www.ebi.ac.uk/pdbe/api/pdb/compound/summary/{ccd}",
                         CACHE / f"{ccd}.json").read_text())
    rec = list(d.values())[0][0]
    smis = {s["program"]: s["name"] for s in rec.get("smiles", [])}
    return smis.get("CACTVS") or smis.get("OpenEye OEToolkits") or next(iter(smis.values()), None)


def split(pdb_id, ccd):
    """Receptor PDB (protein only, first altloc/chain) and the crystal ligand block."""
    txt = fetch(f"https://www.ebi.ac.uk/pdbe/entry-files/download/pdb{pdb_id.lower()}.ent",
                CACHE / f"{pdb_id}.pdb").read_text()
    prot, lig, chain = [], [], None
    for line in txt.splitlines():
        if line.startswith("ATOM") and line[16] in " A":
            prot.append(line + "\n")
        elif line.startswith("HETATM") and line[17:20].strip() == ccd and line[16] in " A":
            if chain is None:
                chain = line[21]
            if line[21] == chain:
                lig.append(line + "\n")
    rp = CACHE / f"{pdb_id}_rec.pdb"
    rp.write_text("".join(prot))
    return rp, "".join(lig)


def crystal_mol(block, smiles):
    raw = Chem.MolFromPDBBlock(block, sanitize=False, removeHs=True)
    if raw is None:
        return None
    tpl = Chem.MolFromSmiles(smiles)
    if tpl is None:
        return None
    try:
        return AllChem.AssignBondOrdersFromTemplate(tpl, raw)
    except Exception:
        return None


def docked_mol(pdbqt):
    from meeko import PDBQTMolecule, RDKitMolCreate
    pm = PDBQTMolecule(pdbqt, is_dlg=False, skip_typing=True)
    mols = RDKitMolCreate.from_pdbqt_mol(pm)
    return Chem.RemoveHs(mols[0]) if mols else None


def main():
    print(f"{'case':6s} {'atoms':>5s} {'score':>6s} {'RMSD':>6s}  verdict   description")
    results = []
    for pdb_id, ccd, desc in CASES:
        try:
            smi = ligand_smiles(ccd)
            rec_pdb, lig_block = split(pdb_id, ccd)
            xtal = crystal_mol(lig_block, smi)
            if xtal is None or xtal.GetNumConformers() == 0:
                print(f"{pdb_id:6s} {'-':>5s} {'-':>6s} {'-':>6s}  SKIP      could not rebuild crystal ligand")
                continue
            rec_pdbqt = CACHE / f"{pdb_id}_rec.pdbqt"
            prep_receptor.main(str(rec_pdb), str(rec_pdbqt))   # OUR typing, under test
            centre = xtal.GetConformer().GetPositions().mean(axis=0)

            site = Site(tuple(centre), size=20.0, receptor=rec_pdbqt)
            pdbqt = ligand_pdbqt(smi)
            if pdbqt is None:
                print(f"{pdb_id:6s}  ligand embed failed"); continue
            site.v.set_ligand_from_string(pdbqt)
            site.v.dock(exhaustiveness=16, n_poses=10)
            score = float(site.v.energies(n_poses=1)[0][0])
            pose = docked_mol(site.v.poses(n_poses=1))
            rms = rdMolAlign.GetBestRMS(pose, xtal)
            ok = "PASS" if rms < 2.0 else ("marginal" if rms < 3.0 else "FAIL")
            print(f"{pdb_id:6s} {xtal.GetNumHeavyAtoms():5d} {score:6.2f} {rms:6.2f}  {ok:9s} {desc}")
            results.append((pdb_id, rms, ok))
        except Exception as e:
            print(f"{pdb_id:6s}  ERROR {type(e).__name__}: {str(e)[:60]}")

    passed = sum(1 for _, r, _ in results if r < 2.0)
    print(f"\n{passed}/{len(results)} recovered the crystal pose within 2.0 A")
    if results and passed == 0:
        print("PIPELINE IS NOT VALIDATED. Do not interpret the fragment screen.")


if __name__ == "__main__":
    main()
