# Trans-splicing molecules for *BUB1B*: there is no drug, and here is the specification

**There is no trans-splicing drug.** None approved, and none in trials: ClinicalTrials.gov
returns **exactly one** study mentioning trans-splicing, and it is a Huntington's disease
**skin biopsy** for preclinical development — not a molecule given to anyone. No RTM for
any gene has ever been administered to a patient.

So this is not a list of drugs. It is the specification for the molecule that would have
to be built, computed from the transcript structure we verified ourselves.

*Producer: `scripts/mva/rtm_design.py`. Trials queried 21 Oct 2026. According to PubMed
for the design literature.*

## What the molecule is

A 3′ pre-mRNA trans-splicing molecule (RTM) has three parts:

1. **Binding domain** — antisense to a chosen intron of the target pre-mRNA, tethering the
   molecule to the nascent transcript
2. **Splice domain** — branch point, polypyrimidine tract, 3′ AG — competing with that
   intron's own 3′ splice site
3. **Coding cassette** — the corrected sequence from that point to the stop

The spliceosome joins the target's upstream exons to the cassette, replacing **everything
downstream of the binding site**, including whatever mutation it carried.

## Why the geometry suits this genotype

```
  allele 1  c.2210  p.Leu737Ter    coding exon 17  (c.2144-2284)
  allele 2  c.3006  p.Asn1002Lys   coding exon 23  (c.2958-3153)
```

**One RTM binding any intron upstream of coding exon 17 replaces both.** It does not need
to know which allele it landed on — which is what "mutation-agnostic" means in practice,
and why the same molecule would serve most of the 2,536 catalogued alleles rather than
this child alone.

## The candidate target introns

| intron after coding exon | genomic span | intron length | cassette | codons | room |
|---|---|---|---|---|---|
| 8 | chr15:40,185,643–40,196,544 | **10,902 nt** | 2,095 nt | 698 | ample |
| 5 | chr15:40,176,674–40,183,713 | 7,040 nt | 2,572 nt | 857 | ample |
| 4 | chr15:40,170,682–40,176,476 | 5,795 nt | 2,769 nt | 923 | ample |
| 15 | chr15:40,206,459–40,208,636 | 2,178 nt | **1,144 nt** | 381 | workable |
| 16 | chr15:40,208,771–40,209,634 | 864 nt | **1,010 nt** | 336 | workable |
| 3, 7, 13 | — | 123–415 nt | — | — | **too short to bind** |

**My own shortlist ordering was wrong, and the table shows it.** Ranking by binding-domain
room alone puts intron 8 first — 10.9 kb of intron, but a 2,095 nt cassette. The better
engineering trade is **intron 15 or 16**: a cassette of 1,010–1,144 nt, roughly half the
payload, with an intron still long enough for a binding domain that clears the natural
branch point. Payload size matters for every delivery route, and the first ordering
optimised the wrong variable.

If only allele 2 mattered, the last intron (chr15:40,218,563–40,220,563, 2,001 nt) needs a
cassette of just **196 nt / 65 codons** — but it leaves allele 1 untouched, which is the
entire reason to prefer trans-splicing over the mRNA-level options.

## What the field has actually achieved

The groups who have built these are candid about the constraint:

- **RTMs are selected empirically, not designed.** Hüttner et al. screened pools of
  randomly generated variants with a fluorescence reporter to find efficient ones, and
  demonstrated the first internal-exon replacement in an endogenous transcript
  ([10.3390/ijms17101609](https://doi.org/10.3390/ijms17101609)). Nothing in the table
  above substitutes for that screen.
- **Co-delivered antisense RNAs raise efficiency** by masking competing splicing elements
  (Koller et al., [10.3390/ijms16011179](https://doi.org/10.3390/ijms16011179)) — the same
  trick the *CTNNB1* group used in 2025, alongside a 5′ ribozyme for nuclear retention.
- **Efficiency is the whole problem.** It is why a modality demonstrated in the 1990s has
  produced no clinical candidate in thirty years.

## The honest position

Our dosage model puts the bar at **23–38% trans-splicing efficiency** to reach carrier
level. Published RTMs have generally fallen well short of that, which is the real reason
this ranks first on merit and is not something anyone can act on next year.

What the specification above is good for is narrow and real: it says **where** to bind,
**how big** the cassette is, and **which introns are disqualified** — so that if anyone
does screen RTMs for this gene, they start from five candidates rather than twenty-two,
with the payload trade-off already quantified.

**And what it is not: a drug that would work.** Nothing in this class has worked in a
patient yet.
