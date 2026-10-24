import numpy as np, math
T2O={"ALA":"A","ARG":"R","ASN":"N","ASP":"D","CYS":"C","GLU":"E","GLN":"Q","GLY":"G","HIS":"H",
"ILE":"I","LEU":"L","LYS":"K","MET":"M","PHE":"F","PRO":"P","SER":"S","THR":"T","TRP":"W","TYR":"Y","VAL":"V"}
MAXASA={"ALA":129,"ARG":274,"ASN":195,"ASP":193,"CYS":167,"GLU":223,"GLN":225,"GLY":104,"HIS":224,
"ILE":197,"LEU":201,"LYS":236,"MET":224,"PHE":240,"PRO":159,"SER":155,"THR":172,"TRP":285,"TYR":263,"VAL":174}
rn=[];nm=[];at=[];co=[];pl=[]
for l in open("/tmp/bubr1.pdb"):
    if l.startswith("ATOM"):
        rn.append(int(l[22:26])); nm.append(l[17:20].strip()); at.append(l[12:16].strip())
        co.append([float(l[30:38]),float(l[38:46]),float(l[46:54])]); pl.append(float(l[60:66]))
rn=np.array(rn); nm=np.array(nm); at=np.array(at); co=np.array(co); pl=np.array(pl)
def sc(r):
    i=np.where(rn==r)[0]; s=[j for j in i if at[j] not in ("N","CA","C","O")]
    return co[s] if s else co[i]
def ca(r): return co[np.where((rn==r)&(at=="CA"))[0][0]]

print("SPATIAL COUPLING\n")
for a,b,lab in [(1002,1008,"proband site -> Plk1 site"),(1002,1012,"proband -> L1012P"),
                (1012,1008,"L1012P -> Plk1 site"),(1002,978,"proband -> its H-bond partner W978"),
                (1002,998,"proband -> its H-bond partner V998")]:
    d1=np.linalg.norm(ca(a)-ca(b)); d2=np.linalg.norm(sc(a)[:,None,:]-sc(b)[None,:,:],axis=2).min()
    tag="DIRECT CONTACT" if d2<5 else ("second shell" if d2<8 else "no contact")
    print(f"  {a} <-> {b:<5} CA-CA {d1:5.1f}A  sidechain {d2:5.1f}A   {tag:<15} {lab}")

def shell(r,cut=8.0):
    d=np.linalg.norm(co[:,None,:]-sc(r)[None,:,:],axis=2).min(axis=1)
    return set(int(x) for x in rn[d<cut])
s2,s8,s12=shell(1002),shell(1008),shell(1012)
print(f"\nSHARED NEIGHBOURHOODS (8 A)")
print(f"  N1002 n={len(s2)}   T1008 n={len(s8)}   L1012 n={len(s12)}")
print(f"  N1002 & T1008 overlap: {sorted(s2&s8)}")
print(f"  N1002 & L1012 overlap: {sorted(s2&s12)}")

# SASA
VDW={"C":1.70,"N":1.55,"O":1.52,"S":1.80}
el=np.array([ (l) for l in at])
rad=np.array([VDW.get(a[0],1.7) for a in at])
def sphere(n=256):
    i=np.arange(n)+0.5; phi=np.arccos(1-2*i/n); th=math.pi*(1+5**0.5)*i
    return np.c_[np.cos(th)*np.sin(phi),np.sin(th)*np.sin(phi),np.cos(phi)]
SP=sphere(256); P=1.4
def rsa(r):
    idx=np.where(rn==r)[0]; c=co[idx].mean(0)
    near=np.where(np.linalg.norm(co-c,axis=1)<18)[0]
    tot=0
    for ai in idx:
        R=rad[ai]+P; pts=co[ai]+R*SP
        d=np.linalg.norm(pts[:,None,:]-co[near][None,:,:],axis=2)
        m=(near!=ai); occ=(d[:,m]<(rad[near][m]+P)[None,:]).any(axis=1)
        tot+=(4*math.pi*R*R)*(1-occ.mean())
    return 100*tot/MAXASA[nm[idx][0]]
print("\nACCESSIBILITY  (Plk1 must reach T1008 to phosphorylate it)")
for r in (1002,1008,1012):
    i=np.where(rn==r)[0]
    print(f"  {T2O[nm[i][0]]}{r}: RSA {rsa(r):5.1f}%   pLDDT {pl[i].mean():.1f}")

print("\n" + "="*78)
print("WHICH KNOWN DESTABILISER IS ACTUALLY THE CLOSEST STRUCTURAL ANALOGUE TO N1002?\n")
def ss(r):
    try:
        d=np.linalg.norm(ca(r)-ca(r+4))
    except Exception: return "?"
    return "helix" if 5.0<d<6.8 else ("turn" if d<=7.5 else "loop/extended")
print(f"{'site':>8}{'sec.struct':>16}{'RSA%':>8}{'contacts w/ T1008?':>20}{'shell size':>12}")
print("-"*66)
for r,lab in [(1002,"N1002 <-"),(1012,"L1012P"),(909,"I909T"),(844,"L844F"),(814,"R814H"),(727,"R727C")]:
    d2=np.linalg.norm(sc(r)[:,None,:]-sc(1008)[None,:,:],axis=2).min() if r!=1008 else 0
    print(f"{lab:>8}{ss(r):>16}{rsa(r):>8.1f}{('YES '+f'{d2:.1f}A') if d2<5 else ('no  '+f'{d2:.1f}A'):>20}{len(shell(r)):>12}")

print("\n\nDOES N1002 PACK AGAINST ANY SURFACE-EXPOSED RESIDUES?")
print("(if the loop it staples positions an exposed face, a defect could propagate outward)\n")
exposed=[(r,rsa(r)) for r in sorted(shell(1002)) if rsa(r)>40]
print(f"  residues within 8A of N1002 with RSA > 40%: {len(exposed)} of {len(shell(1002))}")
for r,v in exposed:
    i=np.where(rn==r)[0]
    print(f"    {T2O[nm[i][0]]}{r}  RSA {v:.0f}%")
print("\n  N1002 direct contacts (<5A, side chain):")
d=np.linalg.norm(co[:,None,:]-sc(1002)[None,:,:],axis=2).min(axis=1)
for r in sorted(set(int(x) for x in rn[d<5.0])-{1002}):
    i=np.where(rn==r)[0]
    print(f"    {T2O[nm[i][0]]}{r}  RSA {rsa(r):5.1f}%")
