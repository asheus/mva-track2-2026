import sys, pandas as pd
pd.set_option('display.width',220); pd.set_option('display.max_colwidth',45)
D=sys.argv[1]
gd=pd.read_parquet(f"{D}/aggregated/gene_drug_mapping.parquet")
mp=pd.read_parquet(f"{D}/aggregated/gene_indication_max_phase.parquet")
ch=pd.read_parquet(f"{D}/chembl_gene_drug.parquet")
dg=pd.read_parquet(f"{D}/dgidb_gene_drug.parquet")

def show(g,label):
    print("\n"+"="*74); print(label); print("="*74)
    s=gd[gd.gene==g]
    named=s[s.drug_name.notna()]
    print(f"total annotations={len(s)}  with names={len(named)}  sources={s.source.unique().tolist()}")
    if len(named):
        print(named[["drug_name","source","action_type","molecule_type","dgidb_evidence_score"]]
              .drop_duplicates().sort_values("dgidb_evidence_score",ascending=False).to_string(index=False))
    # chembl/dgidb direct
    for nm,t in [("ChEMBL",ch),("DGIdb",dg)]:
        x=t[t.gene==g]
        if len(x): print(f"\n  [{nm}] {x.drug_name.dropna().unique().tolist()[:25]}")
    ph=mp[mp.gene==g]
    if len(ph):
        top=ph.sort_values("max_phase",ascending=False).head(6)
        print(f"\n  top indications by max_phase:")
        print(top[["efo_term","max_phase","max_phase_concluded","is_ongoing","gene_drug_sources"]].to_string(index=False))

show("CIP2A","CIP2A — endogenous PP2A inhibitor; inhibiting it DE-REPRESSES PP2A")
show("BUB1B","BUB1B — the gene itself")
show("SET","SET / I2PP2A — the other endogenous PP2A inhibitor")
