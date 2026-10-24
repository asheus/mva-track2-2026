"""Box-restricted docking with AutoDock Vina, run locally.

Ligands come in as SMILES, are embedded and minimised with RDKit, converted to PDBQT
by Meeko, and docked into a box. Returns the best score and the pose centroid.
"""
import io, pathlib, sys
import numpy as np
from rdkit import Chem, RDLogger
from rdkit.Chem import AllChem
RDLogger.DisableLog("rdApp.*")
from meeko import MoleculePreparation, PDBQTWriterLegacy
from vina import Vina

ROOT = pathlib.Path(__file__).resolve().parents[5]
NS = ROOT / "docs/mva/data/neurosnap"


def ligand_pdbqt(smiles, seed=0xC0FFEE):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    mol = Chem.AddHs(mol)
    p = AllChem.ETKDGv3()
    p.randomSeed = seed
    if AllChem.EmbedMolecule(mol, p) != 0:
        return None
    try:
        AllChem.MMFFOptimizeMolecule(mol, maxIters=500)
    except Exception:
        pass
    # Fail soft. An exception here propagates out of a pool worker and kills the entire
    # screen -- which is exactly what one disconnected fragment did, 60 times, each
    # restart resuming to the same poisoned entry. A ligand we cannot prepare is a
    # dropped row, not a dead run.
    try:
        setups = MoleculePreparation().prepare(mol)
        if not setups:
            return None
        s, ok, _ = PDBQTWriterLegacy.write_string(setups[0])
        return s if ok else None
    except Exception:
        return None


class Site:
    """One docking box, with its Vina grid maps computed once.

    Building the maps is most of the cost of a Vina run, and they depend only on the
    receptor and the box -- not on the ligand. One Site per box, reused across the whole
    library, turns N_ligands x N_sites map builds into N_sites, which is the difference
    between a screen that finishes and one that does not. Maps cover the full AutoDock
    ligand atom-type set so a later fragment cannot introduce a type the maps lack.
    """

    def __init__(self, centre, size=18.0, receptor=None, seed=42):
        self.centre, self.size = tuple(centre), size
        self.v = Vina(sf_name="vina", seed=seed, verbosity=0)
        self.v.set_receptor(str(receptor or NS / "bubr1_pseudokinase.pdbqt"))
        # Built with no ligand set, which gives maps for the full AutoDock type set --
        # verified against fragments carrying F, Cl, S and P. Vina 1.2.7 has no
        # ligand_types argument, so this is the only way to get type-complete maps.
        self.v.compute_vina_maps(center=list(self.centre), box_size=[size] * 3)

    def dock(self, smiles=None, pdbqt=None, exhaustiveness=8, n_poses=5):
        pdbqt = pdbqt or (ligand_pdbqt(smiles) if smiles else None)
        if pdbqt is None:
            return None, None
        try:
            self.v.set_ligand_from_string(pdbqt)
            self.v.dock(exhaustiveness=exhaustiveness, n_poses=n_poses)
            score = float(self.v.energies(n_poses=1)[0][0])
            out = self.v.poses(n_poses=1)
        except Exception:
            return None, None
        xyz = [(float(l[30:38]), float(l[38:46]), float(l[46:54]))
               for l in out.splitlines()
               if l.startswith(("ATOM", "HETATM")) and l[77:79].strip() != "H"]
        return score, tuple(np.mean(xyz, axis=0)) if xyz else None


def dock(smiles, centre, size=18.0, exhaustiveness=8, n_poses=5,
         receptor=None, seed=42):
    """One-shot convenience wrapper. Use Site for anything repeated."""
    return Site(centre, size, receptor, seed).dock(
        smiles, exhaustiveness=exhaustiveness, n_poses=n_poses)


if __name__ == "__main__":
    # Positive control: the blind run could not put ATP in its own site (it finished
    # 38 A away). With a box on that site it must, or the pipeline is not trustworthy.
    ATP = ("Nc1ncnc2c1ncn2[C@@H]1O[C@H](COP(=O)(O)OP(=O)(O)OP(=O)(O)O)"
           "[C@@H](O)[C@H]1O")
    import math
    for label, centre in (("ATP site (positive control)", (-23.599, -18.248, 3.350)),
                          ("allosteric site (target)", (-41.850, -9.140, 4.710))):
        s, c = dock(ATP, centre)
        d = math.dist(c, centre) if c else float("nan")
        print(f"{label:30s} ATP scores {s:6.2f} kcal/mol, "
              f"pose centroid {d:.1f} A from box centre")
