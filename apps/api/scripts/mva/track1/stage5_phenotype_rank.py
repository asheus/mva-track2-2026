"""Stage 5: rank the surviving candidate genes by phenotype similarity to the proband.

    python3 stage5_phenotype_rank.py --in stage3.json --obo hp.obo --g2p genes_to_phenotype.txt \
        --terms HP:0002859,HP:0000121,... [--top 25]

The proband's HPO terms are supplied on the COMMAND LINE and are not stored in this
file. The challenge data is gated and must not be redistributed, so no patient
observation is committed; the operator provides the terms, which is also what makes the
run auditable -- you can see exactly what the ranking was given.

METHOD. Resnik-style information-content similarity, the standard for this task.

  * Each HPO term's information content is -log(fraction of annotated genes carrying it,
    with ancestor closure). Rare, specific observations therefore weigh far more than
    generic ones -- matching "Rhabdomyosarcoma" is strong evidence, matching "Short
    stature" is nearly free, and a method that treated them equally would rank the
    wrong genes.
  * A gene's score is the sum, over the proband's terms, of the best information
    content shared between that term and any term annotated to the gene, using the
    closure of both. This is the standard asymmetric best-match sum.
  * Ancestor closure matters because gene annotations and clinical records rarely use
    the same level of the ontology; without it, exact-string matching throws away most
    of the signal.

NO GENE IS NAMED HERE EITHER. Scores come from the public HPO gene-to-phenotype file.
"""
import argparse, collections, json, math, pathlib


def load_obo(path):
    parents, names = collections.defaultdict(set), {}
    cur = None
    for line in pathlib.Path(path).read_text().splitlines():
        if line == "[Term]":
            cur = None
        elif line.startswith("id: HP:"):
            cur = line[4:].strip()
        elif cur and line.startswith("name: "):
            names[cur] = line[6:].strip()
        elif cur and line.startswith("is_a: "):
            parents[cur].add(line[6:].split("!")[0].strip())
    return parents, names


def closure(term, parents, memo):
    if term in memo:
        return memo[term]
    out, stack = {term}, [term]
    while stack:
        for p in parents.get(stack.pop(), ()):
            if p not in out:
                out.add(p); stack.append(p)
    memo[term] = out
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--obo", required=True)
    ap.add_argument("--g2p", required=True)
    ap.add_argument("--terms", required=True, help="comma-separated proband HPO ids")
    ap.add_argument("--top", type=int, default=25)
    a = ap.parse_args()

    parents, names = load_obo(a.obo)
    memo = {}

    gene_terms = collections.defaultdict(set)
    for line in pathlib.Path(a.g2p).read_text().splitlines()[1:]:
        p = line.split("\t")
        if len(p) > 2 and p[2].startswith("HP:"):
            gene_terms[p[1]].add(p[2])
    # Expand each gene's annotations to their ancestors once.
    gene_closed = {g: set().union(*(closure(t, parents, memo) for t in ts)) if ts else set()
                   for g, ts in gene_terms.items()}

    # Information content from the annotation corpus itself.
    freq = collections.Counter()
    for ts in gene_closed.values():
        freq.update(ts)
    N = max(1, len(gene_closed))
    ic = {t: -math.log(c / N) for t, c in freq.items() if c}

    probands = [t.strip() for t in a.terms.split(",") if t.strip()]
    print(f"{len(gene_closed):,} annotated genes | {len(ic):,} terms with IC")
    print(f"\nproband terms and their information content (higher = more specific):")
    for t in probands:
        print(f"   {t}  IC {ic.get(t, 0):5.2f}  {names.get(t, '?')}")

    cands = json.loads(pathlib.Path(a.inp).read_text())
    print(f"\nscoring {len(cands):,} candidate genes")

    scored = []
    for g, vs in cands.items():
        gt = gene_closed.get(g)
        if not gt:
            scored.append((0.0, g, vs, 0)); continue
        total, matched = 0.0, 0
        for t in probands:
            tc = closure(t, parents, memo)
            shared = tc & gt
            best = max((ic.get(s, 0.0) for s in shared), default=0.0)
            total += best
            if best > 0:
                matched += 1
        scored.append((total, g, vs, matched))
    scored.sort(key=lambda r: (-r[0], r[1]))

    print(f"\n{'rank':>4s} {'score':>7s} {'terms':>5s} {'gene':<14s} variants")
    for i, (sc, g, vs, m) in enumerate(scored[:a.top], 1):
        desc = "; ".join(f"{x['pos']}{x['ref']}>{x['alt']}({x['zyg']},{x['csq']})" for x in vs[:3])
        print(f"{i:4d} {sc:7.2f} {m:5d} {g:<14s} {desc}")

    out = [{"rank": i, "gene": g, "score": round(sc, 3), "terms_matched": m,
            "variants": vs} for i, (sc, g, vs, m) in enumerate(scored, 1)]
    dest = pathlib.Path(a.inp).with_name("stage5_ranked.json")
    dest.write_text(json.dumps(out))
    print(f"\n-> {dest}")


if __name__ == "__main__":
    main()
