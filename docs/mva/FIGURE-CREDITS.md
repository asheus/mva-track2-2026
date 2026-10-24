# Figure credits — MVA-Track2 deck

Our own text, data, analysis and figures in this repository are released under
**CC BY 4.0**, as Track 2 requires. That grant covers *our* content. Third-party
figures reproduced in the deck keep their own licence, listed below, and the
CC BY 4.0 grant does **not** extend to them.

| Slide | Figure | Source | Licence |
|---|---|---|---|
| 2 | Attachment geometries (A, B) | McVey SL, Cosby JK, Nannas NJ. *Int J Mol Sci* 2021;22:8818. PMID 34445523 | CC BY 4.0 — reproduced, attributed on slide |
| 2, 6 | Cell cycle of BubR1 functionality and abundance (Fig 2). **On slide 6 we added Aurora B, an arrow to the kinetochore-microtubule grip and a phosphate marker; Aurora B is not in the source panel. The addition is drawn in orange and declared on the slide.** | Bloom CR, North BJ. *Cell Biosci* 2021;11:76. PMID 33892776 | CC BY 4.0 — reproduced, attributed on slide |
| 12 | *trans*-RNA mechanism (Fig 1a) | Jia L, Nguyen T-T, et al. Programmable initiation of mRNA translation by *trans*-RNA. *Nat Biotechnol* 2025. doi:10.1038/s41587-025-02897-1 | **Not CC.** Reproduced as a single panel for non-commercial scholarly comment with full citation. Not relicensed. |
| 7 | LAP-BUBR1 rescue of MVA patient fibroblasts (Fig 4D) | Suijkerbuijk SJE, van Osch MHJ, Bos FL, Hanks S, Rahman N, Kops GJPL. *Cancer Res* 2010;70:4891. PMID 20516114 | **Not CC.** Author manuscript via Europe PMC. Reproduced as a single panel for non-commercial scholarly comment with full citation. Not relicensed. |

Figures we drew ourselves (`fig_*.png`, built by `apps/api/scripts/mva/deck/make_figs*.py`)
are CC BY 4.0. Two of them restate layouts from CC BY 4.0 reviews and say so in
their own docstrings:

- `fig_attach.png` — superseded on slide 3 by the McVey original; kept in the repo
  because earlier revisions cite it.
- `fig_domains2.png` — domain layout after Bloom & North 2021, variant set merged
  with our own atlas.

Protein structures are rendered from deposited coordinates (PDB **5JJA**, **4AF3**),
which carry no copyright. The barasertib-hQPA structure is drawn from PubChem.

**If the organisers require a repository free of all third-party figures**, slides
2, 6 and 7 can be rebuilt against `fig_attach.png`, `fig_kinase_map.png` and a
redrawn bar chart by reverting the three `figbox(... "pap_*.png" ...)` calls in
`build_deck.py`. The argument does not depend on reproducing the originals.
