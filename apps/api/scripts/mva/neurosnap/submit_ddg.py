"""Two orthogonal stability predictors over the BubR1 pseudokinase domain.

ProteinMPNN-ddG runs saturation mutagenesis, so it returns ddG for every residue
and every substitution -- which gives both the corpus variants and a null
distribution at each site. EvoEF2 is a physics force field and is scored only on
the named corpus variants, as an independent check on the learned model.
"""
import pathlib, json
from neurosnap import submit

pdb = pathlib.Path("bubr1_pseudokinase_766_1050.pdb")
raw = pdb.read_bytes()
jobs = {}

# Corpus missense variants inside 766-1050 (chain A), from docs/mva/VARIANT-TABLE.md.
CORPUS = ["R770Q", "R814H", "L844F", "R893S", "I909T", "Q921H",
          "R999Q", "N1002K", "N1004S", "D1005E", "L1012P"]
# EvoEF2 wants <WT><chain><pos><MUT>, one per line.
muts = "\n".join(f"{v[0]}A{v[1:-1]}{v[-1]}" for v in CORPUS)
print("EvoEF2 mutant list:\n" + muts + "\n")

jobs["proteinmpnn_ddg"] = submit(
    "ProteinMPNN-ddG",
    {"Input Structure": (pdb.name, raw), "Number Repeats": "5", "Seed": "42"},
    note="BubR1 pseudokinase 766-1050 saturation ddG",
)
print("ProteinMPNN-ddG:", jobs["proteinmpnn_ddg"])

jobs["evoef2"] = submit(
    "EvoEF2 Mutant Stability Analysis",
    {"Input Structure": (pdb.name, raw), "Mutants": muts},
    note="BubR1 pseudokinase corpus variants, EvoEF2 ddG",
)
print("EvoEF2:", jobs["evoef2"])

pathlib.Path("jobs.json").write_text(json.dumps(jobs, indent=2))
