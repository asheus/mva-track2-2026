"""Lacuna Cryptic Pocket Discovery on the BubR1 pseudokinase domain (766-1050).

Asks: does this pseudokinase carry a ligandable pocket that only opens on
motion -- the structural precondition for a pharmacological chaperone.
"""
import pathlib, json, sys
from neurosnap import submit, wait

pdb = pathlib.Path("bubr1_pseudokinase_766_1050.pdb")
job = submit(
    "Lacuna Cryptic Pocket Discovery",
    {
        "Input Structure": (pdb.name, pdb.read_bytes()),
        "Sampling Backend": "nma",
        "Number of Conformers": "20",
        "Ranking Strategy": "learned",
        "Maximum Pockets": "10",
        "Minimum Crypticity": "0",
        "Minimum Druggability": "0",
        "Minimum Persistence": "0",
        "Export Boltz Pocket Constraints": "true",
        "Export Vina Docking Boxes": "true",
        "Export Individual Pocket PDB Files": "true",
    },
    note="BubR1 pseudokinase domain 766-1050, AlphaFold O60566",
)
print("job:", job)
pathlib.Path("lacuna_job.json").write_text(json.dumps(job, indent=2) if not isinstance(job, str) else job)
