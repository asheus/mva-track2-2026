# Recovered primary sources (not present in the paperclip corpus)

Both were flagged in `source_readiness.json` as a critical coverage gap and recovered
via the PubMed MCP server at the user's instruction (Question checkpoint, 2026-09-10).

| Source | PMID | PMC | DOI | Full text obtained |
|---|---|---|---|---|
| Hanks S, et al. "Constitutional aneuploidy and cancer predisposition caused by biallelic mutations in BUB1B." *Nat Genet* 36:1159-61 (2004) | 15475955 | none | 10.1038/ng1449 | **Abstract only** - not open access, no PMC deposit. Remains partially unverifiable. |
| Suijkerbuijk SJE, van Osch MHJ, Bos FL, Hanks S, Rahman N, Kops GJPL. "Molecular Causes for BUBR1 Dysfunction in the Human Cancer Predisposition Syndrome Mosaic Variegated Aneuploidy." *Cancer Res* 70:4891-900 (2010) | 20516114 | PMC2887387 | 10.1158/0008-5472.CAN-09-4319 | **FULL TEXT recovered.** Not indexed in paperclip (`cat /papers/PMC2887387/` returns empty). |

Retrieval attribution: article metadata and full text retrieved from PubMed/PMC.

## Why this mattered

`schema_discovery.json` recorded that zero of eight pilot papers reported a numerical
BubR1 percentage in readable text, and concluded the dosage axis was near-unpopulated.
That conclusion was an artefact of the corpus gap. The single paper that measures the
dosage axis quantitatively is the one paper the corpus does not index.

Had the review proceeded on the indexed corpus alone it would have reported a null
result on protein dosage. That would have been wrong.
