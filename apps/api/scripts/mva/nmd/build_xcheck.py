import csv, gzip, sys, collections
pred, gtf, out, n_want = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
rows=[r for r in csv.DictReader(open(pred)) if r["CHROM"]=="chr15"][:n_want*3]
genes={r["hgnc_symbol"] for r in rows}
# canonical = longest CDS protein_coding transcript per gene symbol
best={}
with gzip.open(gtf,"rt") as fh:
    for line in fh:
        if line.startswith("#"): continue
        f=line.split("\t")
        if f[0]!="chr15" or f[2]!="CDS": continue
        a=f[8]
        if 'transcript_type "protein_coding"' not in a: continue
        gn=a.split('gene_name "')[1].split('"')[0]
        if gn not in genes: continue
        tx=a.split('transcript_id "')[1].split('"')[0]
        best.setdefault(gn,collections.Counter())[tx]+=int(f[4])-int(f[3])+1
canon={g:c.most_common(1)[0][0] for g,c in best.items()}
w=csv.writer(open(out,"w"),delimiter="\t"); w.writerow(["variant_id","contig","position","refAllele","altAllele","gene","txnames"])
k=0
for r in rows:
    g=r["hgnc_symbol"]
    if g not in canon: continue
    w.writerow([r["variantID"],"chr15",r["POS"],r["REF_ALLELE"],r["ALT_ALLELE"],g,canon[g]]); k+=1
    if k>=n_want: break
print(f"wrote {k} cross-check variants")
