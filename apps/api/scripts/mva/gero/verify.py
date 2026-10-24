import sys, pandas as pd
D=sys.argv[1]
srcs={n:pd.read_parquet(f"{D}/{n}_gene_drug.parquet") for n in
      ["chembl","dgidb","stitch","opentargets","trialpanorama"]}
gd=pd.read_parquet(f"{D}/aggregated/gene_drug_mapping.parquet")

print("UNIVERSE")
print(f"  aggregated gene-drug pairs : {len(gd):,}")
print(f"  distinct genes             : {gd.gene.nunique():,}")
for n,t in srcs.items(): print(f"  {n:<14} rows={len(t):>8,}  genes={t.gene.nunique():>6,}")

APC=["CDC20","FZR1","CDC27","ANAPC1","ANAPC2","ANAPC4","ANAPC5","ANAPC7",
     "ANAPC10","ANAPC11","ANAPC13","ANAPC15","ANAPC16","CDC16","CDC23","CDC26"]
print("\nAPC/C SUBUNITS + COACTIVATORS — per source")
for g in APC:
    hits={n:int((t.gene==g).sum()) for n,t in srcs.items()}
    tot=sum(hits.values())
    if tot: print(f"  {g:<9} {hits}")
present=[g for g in APC if any((t.gene==g).any() for t in srcs.values())]
ingene =[g for g in APC if (gd.gene==g).any()]
print(f"  APC/C genes with ANY drug annotation in ANY of 5 sources: {present if present else 'NONE'}")
print(f"  APC/C genes present in aggregated table                 : {ingene if ingene else 'NONE'}")

print("\nSTITCH NAMELESS-ROW RATE (the interpretation trap)")
st=gd[gd.source=="STITCH"]
print(f"  STITCH rows in aggregated: {len(st):,}; with a drug_name: {st.drug_name.notna().sum():,}"
      f" ({100*st.drug_name.notna().mean():.1f}%)")
print(f"  ALL rows with a drug_name: {gd.drug_name.notna().sum():,} / {len(gd):,}"
      f" ({100*gd.drug_name.notna().mean():.1f}%)")

print("\nPP2A AXIS — NAMED drugs only, any source")
pp=["PPP2CA","PPP2CB","PPP2R1A","PPP2R1B","PTPA","PPP2R5A","PPP2R5B","PPP2R5C","PPP2R5D","PPP2R5E","SET","CIP2A"]
n=gd[(gd.gene.isin(pp))&(gd.drug_name.notna())][["gene","drug_name","source","action_type"]].drop_duplicates()
print(n.to_string(index=False) if len(n) else "  NONE")
