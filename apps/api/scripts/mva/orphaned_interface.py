import numpy as np, math
exec(open("/tmp/sasa.py").read().split("# Calibration set")[0])   # reuse parser + residue_sasa

# Buried area of each residue that is buried *specifically by the kinase domain*:
# SASA of the residue in the full-length model vs SASA with the kinase domain (766-1050) deleted.
def sasa_subset(target_res, keep_mask):
    idx=np.where((resnum==target_res))[0]
    if len(idx)==0: return 0.0
    keep=np.where(keep_mask)[0]
    kxyz, krad = xyz[keep], rad[keep]+PROBE
    tot=0.0
    for ai in idx:
        r=rad[ai]+PROBE
        pts=xyz[ai]+r*SP
        d=np.linalg.norm(pts[:,None,:]-kxyz[None,:,:],axis=2)
        m=(keep!=ai)
        occ=(d[:,m] < krad[m][None,:]).any(axis=1)
        tot += (4*math.pi*r*r)*(1-occ.mean())
    return tot

full = np.ones(len(resnum),bool)
no_kd = ~((resnum>=766)&(resnum<=1050))

print("Interface each linker residue buries against the kinase domain")
print(f"{'res':>5}{'aa':>4}{'buried by KD (A^2)':>20}")
print("-"*32)
per={}
for r in range(720,766):
    a=sasa_subset(r, full); b=sasa_subset(r, no_kd)
    per[r]=max(0.0,b-a)
    if per[r]>5: print(f"{r:>5}{THREE2ONE.get(resname[np.where(resnum==r)[0][0]],'X'):>4}{per[r]:>20.1f}")

print("\nOrphaned interface for each truncation")
print("(surface that packs against the kinase domain but has nothing to pack against once the")
print(" kinase domain is gone -- an exposed greasy patch on the truncated fragment)\n")
print(f"{'truncation':<14}{'last residue':>13}{'orphaned interface (A^2)':>27}   relative")
base=None
for stop,lab in [(731,"731X  RESCUES"),(737,"737X  PROBAND"),(753,"753X  FAILS")]:
    tot=sum(v for k,v in per.items() if k<stop)
    if base is None: base=tot
    print(f"{lab:<14}{stop-1:>13}{tot:>27.0f}   {tot/base:>4.2f}x")
