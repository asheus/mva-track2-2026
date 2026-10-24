import pyarrow.parquet as pq, pyarrow as pa, sys, json
sys.path.insert(0, __import__("pathlib").Path(__file__).resolve().parent.as_posix())
from hf_range_reader import CurlRangeFile  # was: /tmp/hfrange.py, never committed
M=sys.argv[1]; LO,HI=40160000,40223000     # BUB1B hg38 span, padded
url=f"https://huggingface.co/datasets/songlab/gpn-star-scores/resolve/main/data/gpn-star-hg38-{M}-200m/llr/llr_chr15.parquet"
f=CurlRangeFile(url); pf=pq.ParquetFile(f); md=pf.metadata
want=[]
for i in range(md.num_row_groups):
    st=md.row_group(i).column(1).statistics     # pos
    if st and not (st.max < LO or st.min > HI): want.append(i)
print(f"{M}: row groups {want}", file=sys.stderr)
t=pf.read_row_groups(want, columns=["pos","ref","alt","llr_calibrated"])
d=t.to_pydict()
rows=[(p,r,a,l) for p,r,a,l in zip(d["pos"],d["ref"],d["alt"],d["llr_calibrated"]) if LO<=p<=HI]
print(f"{M}: {len(rows):,} SNVs in span, {f.bytes_read/1e6:.1f} MB read in {f.n_requests} reqs", file=sys.stderr)
json.dump(rows, open(f"/tmp/gpn_{M}.json","w"))
