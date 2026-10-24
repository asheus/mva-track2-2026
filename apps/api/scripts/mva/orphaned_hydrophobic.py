import numpy as np, math
exec(open("/tmp/sasa.py").read().split("# Calibration set")[0])

# Refinement: only HYDROPHOBIC orphaned surface should destabilise. Polar/charged surface
# left exposed by a truncation simply gets solvated; exposed greasy surface drives
# aggregation and chaperone-mediated degradation.
HYDROPHOBIC = {"ALA","VAL","LEU","ILE","MET","PHE","TRP","PRO","CYS","TYR"}
def sasa_subset(res, keep_mask, carbon_only=False):
    idx=np.where(resnum==res)[0]
    if carbon_only: idx=np.array([i for i in idx if elem[i] in ("C","S")])
    if len(idx)==0: return 0.0
    keep=np.where(keep_mask)[0]; kxyz,krad=xyz[keep],rad[keep]+PROBE
    tot=0.0
    for ai in idx:
        r=rad[ai]+PROBE; pts=xyz[ai]+r*SP
        d=np.linalg.norm(pts[:,None,:]-kxyz[None,:,:],axis=2)
        m=(keep!=ai); occ=(d[:,m]<krad[m][None,:]).any(axis=1)
        tot+=(4*math.pi*r*r)*(1-occ.mean())
    return tot

full=np.ones(len(resnum),bool); no_kd=~((resnum>=766)&(resnum<=1050))
per_all={}; per_phobe={}
for r in range(720,766):
    idx=np.where(resnum==r)[0]
    if len(idx)==0: continue
    per_all[r]=max(0.,sasa_subset(r,no_kd)-sasa_subset(r,full))
    per_phobe[r]=max(0.,sasa_subset(r,no_kd,True)-sasa_subset(r,full,True))

print("Residues between 731 and 753 that orphan hydrophobic surface\n")
print(f"{'res':>5}{'aa':>4}{'total':>9}{'hydrophobic (C/S)':>20}")
for r in range(731,754):
    if r in per_all and per_phobe[r]>3:
        aa=THREE2ONE.get(resname[np.where(resnum==r)[0][0]],"X")
        print(f"{r:>5}{aa:>4}{per_all[r]:>9.0f}{per_phobe[r]:>20.0f}")

print("\n\nOrphaned HYDROPHOBIC interface by truncation")
print(f"{'truncation':<16}{'total A^2':>11}{'hydrophobic A^2':>18}{'rel. to 731X':>14}   outcome")
print("-"*78)
base=None
for stop,out in [(731,"stable, RESCUES"),(737,"UNKNOWN - proband"),(753,"unstable, FAILS")]:
    t=sum(v for k,v in per_all.items() if k<stop)
    p=sum(v for k,v in per_phobe.items() if k<stop)
    if base is None: base=p
    print(f"{str(stop)+'X':<16}{t:>11.0f}{p:>18.0f}{p/base:>13.2f}x   {out}")
print("\n737X adds, relative to 731X, essentially ONE buried hydrophobic residue (L734).")
print("753X adds five more (L737, L743, C744, I745, M750) plus P749/P751.")
