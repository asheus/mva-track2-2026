"""LitVar2: every BUB1B variant that has literature attached to it."""
import json, requests, time, string
seen={}
queries=["BUB1B","BUBR1"]+[f"BUB1B {c}" for c in string.ascii_uppercase]
for q in queries:
    try:
        r=requests.get("https://www.ncbi.nlm.nih.gov/research/litvar2-api/variant/autocomplete/",
                       params={"query":q}, timeout=45)
        if r.status_code!=200: continue
        for v in r.json():
            if "BUB1B" not in (v.get("gene") or []): continue
            seen[v["_id"]]=v
    except Exception as e: pass
    time.sleep(0.34)
json.dump(list(seen.values()),open("litvar_bub1b.json","w"),indent=1)
print("unique BUB1B variants with literature:",len(seen))
withlit=sorted(seen.values(),key=lambda v:-(v.get("pmids_count") or 0))
print(f"\n{'variant':16s} {'rsid':14s} {'papers':>6s}  clinical significance")
for v in withlit[:30]:
    print(f"{(v.get('name') or '?'):16s} {(v.get('rsid') or '-'):14s} {v.get('pmids_count') or 0:6d}  "
          f"{','.join(v.get('data_clinical_significance') or []) or '-'}")
