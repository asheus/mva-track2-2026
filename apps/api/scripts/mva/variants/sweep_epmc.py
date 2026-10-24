"""Europe PMC full-text sweep for BUB1B variant notations.

Paperclip missed PMC2887387 entirely, so a second literature index is not optional.
Europe PMC indexes full text for open-access papers and is a different corpus.

Strategy: query broadly, fetch every full text available, regex for HGVS protein and
cDNA notation, and keep only hits that sit in a BUB1B/BubR1 context -- papers routinely
discuss BUB1, CEP57 and TRIP13 variants in the same paragraph.
"""
import json, re, time, requests, sys
from collections import defaultdict

BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest"
QUERIES = [
 '(BUB1B OR BUBR1) AND "mosaic variegated aneuploidy"',
 '(BUB1B OR BUBR1) AND "premature chromatid separation"',
 'BUB1B AND (mutation OR variant) AND (patient OR proband OR family)',
 'BUB1B AND "compound heterozygous"',
 'BUB1B AND (c. OR p.) AND germline',
]
ids = {}
for q in QUERIES:
    cursor = "*"
    for _ in range(6):
        r = requests.get(f"{BASE}/search", params={"query": q, "format": "json",
                         "pageSize": 100, "cursorMark": cursor, "resultType": "lite"}, timeout=90)
        if r.status_code != 200: break
        j = r.json()
        for res in j.get("resultList", {}).get("result", []):
            if res.get("pmcid") and res.get("isOpenAccess") == "Y":
                ids[res["pmcid"]] = res.get("title", "")[:90]
        nxt = j.get("nextCursorMark")
        if not nxt or nxt == cursor: break
        cursor = nxt
        time.sleep(0.25)
print(f"open-access full texts to scan: {len(ids)}", flush=True)
json.dump(ids, open("epmc_ids.json", "w"))

PROT = re.compile(r"p\.\(?([A-Z][a-z]{2}|[A-Z])(\d{1,4})([A-Z][a-z]{2}|[A-Z*]|Ter|fs|del)")
CDNA = re.compile(r"c\.(\d{1,4}[+-]?\d*)([ACGT]>[ACGT]|del|dup|ins)")
hits = defaultdict(set)
scanned = 0
for pmcid in ids:
    try:
        r = requests.get(f"{BASE}/{pmcid}/fullTextXML", timeout=60)
        if r.status_code != 200 or len(r.content) < 500: continue
        txt = re.sub(r"<[^>]+>", " ", r.text)
        txt = re.sub(r"\s+", " ", txt)
        scanned += 1
        # only look in windows that mention BUB1B/BUBR1
        for m in re.finditer(r"BUB1B|BUBR1|BubR1", txt):
            w = txt[max(0, m.start()-350): m.end()+350]
            for p in PROT.finditer(w): hits[p.group(0)].add(pmcid)
            for c in CDNA.finditer(w): hits["c." + c.group(1) + c.group(2)].add(pmcid)
    except Exception:
        continue
    if scanned % 25 == 0: print(f"  scanned {scanned}", flush=True)
print(f"\nscanned {scanned} full texts, {len(hits)} distinct notations in BUB1B context")
json.dump({k: sorted(v) for k, v in hits.items()}, open("epmc_hits.json", "w"), indent=1)
