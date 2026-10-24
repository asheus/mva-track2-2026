"""Wait for the openmm run to release its credit reservation, then submit the
matched N1002K Lacuna run."""
import time, json, pathlib, traceback
from neurosnap import status, submit
OPENMM="6aa8c0c4bd4dd3655071b3f5"
p=pathlib.Path("bubr1_pseudokinase_N1002K.pdb")
t0=time.time()
while time.time()-t0 < 5400:
    s=str(status(OPENMM)).lower()
    print(f"[{int(time.time()-t0):5d}s] openmm={s}",flush=True)
    if s in ("completed","failed"):
        for attempt in range(12):
            try:
                j=submit("Lacuna Cryptic Pocket Discovery",
                    {"Input Structure":(p.name,p.read_bytes()),"Sampling Backend":"nma",
                     "Number of Conformers":"20","Ranking Strategy":"learned","Maximum Pockets":"10",
                     "Minimum Crypticity":"0","Minimum Druggability":"0","Minimum Persistence":"0",
                     "Export Boltz Pocket Constraints":"true","Export Vina Docking Boxes":"true",
                     "Export Individual Pocket PDB Files":"true"},
                    note="BubR1 pseudokinase N1002K, nma 20 conformers - matched to WT")
                print("SUBMITTED mutant:",j,flush=True)
                jobs=json.load(open("jobs.json")); jobs["lacuna_nma_n1002k"]=j
                json.dump(jobs,open("jobs.json","w"),indent=1)
                raise SystemExit(0)
            except SystemExit: raise
            except Exception as e:
                print("  retry",attempt,type(e).__name__,str(e)[:120],flush=True); time.sleep(120)
        raise SystemExit("could not submit mutant run")
    time.sleep(60)
print("TIMED OUT waiting on openmm")
