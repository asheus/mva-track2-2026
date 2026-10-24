import sys, pandas as pd
D = sys.argv[1]
gd = pd.read_parquet(f"{D}/aggregated/gene_drug_mapping.parquet")
mp = pd.read_parquet(f"{D}/aggregated/gene_indication_max_phase.parquet")

GROUPS = {
 "BubR1 itself":      ["BUB1B"],
 "PP2A-B56 regulatory":["PPP2R5A","PPP2R5B","PPP2R5C","PPP2R5D","PPP2R5E"],
 "PP2A core":         ["PPP2R1A","PPP2R1B","PPP2CA","PPP2CB","PTPA"],
 "PP2A endog. inhib": ["SET","CIP2A","KIAA1524","ANP32A","PPME1"],
 "APC/C":             ["CDC20","FZR1","CDC27","ANAPC1","ANAPC2","ANAPC4","ANAPC5","ANAPC7","ANAPC10","ANAPC11"],
 "Aurora":            ["AURKA","AURKB","AURKC"],
 "SAC kinases":       ["TTK","BUB1","MAD1L1","MAD2L1","BUB3","PLK1","CENPE"],
 "NMD":               ["UPF1","UPF2","UPF3A","UPF3B","SMG1","SMG5","SMG6","SMG7"],
 "Chaperone/degrade": ["HSP90AA1","HSP90AB1","HSPA1A","HSF1","STUB1","SIRT2"],
}
ALL = [g for v in GROUPS.values() for g in v]
sub = gd[gd.gene.isin(ALL)]
ph  = mp[mp.gene.isin(ALL)]

print("="*78); print("DRUG-TARGET ANNOTATIONS PER NODE"); print("="*78)
for grp, genes in GROUPS.items():
    print(f"\n--- {grp} ---")
    for g in genes:
        s = sub[sub.gene==g]
        if len(s)==0: continue
        mx = ph[ph.gene==g].max_phase.max() if len(ph[ph.gene==g]) else None
        acts = s.action_type.dropna().value_counts().to_dict()
        print(f"  {g:<10} drugs={s.our_drug_id.nunique():<5} maxphase={mx}  actions={acts}")

print("\n"+"="*78); print("ACTIVATORS / AGONISTS ON THE PP2A AXIS  (what the mechanism needs)"); print("="*78)
pp2a = [g for g in GROUPS["PP2A-B56 regulatory"]+GROUPS["PP2A core"]+GROUPS["PP2A endog. inhib"]]
act = sub[sub.gene.isin(pp2a)]
if len(act):
    print(act[["gene","drug_name","source","action_type","molecule_type","pchembl"]]
          .sort_values(["gene","action_type"]).to_string(index=False))
else:
    print("  NONE")

print("\n"+"="*78); print("APC/C + AURORA B: every annotated drug, with max phase reached"); print("="*78)
for g in ["CDC20","FZR1","CDC27","AURKB"]:
    s = sub[sub.gene==g]
    if len(s)==0: print(f"  {g}: no annotated drug"); continue
    print(f"\n  {g}  ({s.our_drug_id.nunique()} drugs)")
    print(s[["drug_name","source","action_type","molecule_type"]].drop_duplicates()
          .head(25).to_string(index=False))
