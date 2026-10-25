# Does *BUB1B* have an ASO-addressable splicing target, as *SCN1A* does?

**No. We tested our own best new idea and it failed.** This file records how, because the
test is more reusable than the idea was.

*All numbers from `scripts/mva/splice_architecture.py`. According to PubMed for the
literature. Annotation from Ensembl, retrieved 21 Oct 2026.*

## The idea, and why it was attractive

Zorevunersen (STK-001) raises Nav1.1 in Dravet syndrome by blocking inclusion of
**poison exon 20N** in *SCN1A* — a cassette exon whose inclusion frameshifts the message
and sends it to nonsense-mediated decay. Block it, that flux returns to productive mRNA,
and protein rises from the alleles the patient already has. It is in **Phase 3 in
children** (NCT06872125, 170 patients, 61 sites), and the mechanism is stated plainly in
the literature: the ASO was "generated using targeted augmentation of nuclear gene output
technology to prevent inclusion of the nonsense-mediated decay, or poison, exon 20N in
human *SCN1A*" (Yuan et al., Brain 2024,
[10.1093/brain/awad349](https://doi.org/10.1093/brain/awad349)).

Why it fit our case almost too well:

- Our dosage model says the gap to close is **~1.4×** — the size flux redirection gives.
- It is **gene-specific**, avoiding the systemic reach of raising NAD⁺.
- It acts on **allele 2**, the only allele we had identified as reachable.
- *BUB1B* appeared to have the substrate: **12 of its 31 annotated transcripts** carry the
  `nonsense_mediated_decay` biotype, against 6 of 30 for *SCN1A*.

That last point is what we reported a day earlier, and it is where the error was.

## Why counting decay transcripts proves nothing

A count cannot fail. *BUB1B* has 12 decay-biotype transcripts and would "pass" any
threshold built on counting them. Transcripts land in that biotype for many reasons, and
almost none of them is a thing an ASO can block.

The question is narrower: does a **specific, recurrent, frame-disrupting, blockable**
event exist? Three filters separate that from noise.

**1 · Terminal-exon filter.** Variation in where transcripts start and stop dominates the
raw signal and is annotation disagreement, not alternative splicing. Without this filter,
*BUB1B*'s top "skipped exon" is exon 1, apparently skipped in **9 of 10** decay isoforms —
which on inspection is four different 5′ boundaries for the same first exon. A pipeline
that missed this would have reported a spectacular and entirely false target.

**2 · Frame test.** A cassette exon only triggers decay if including it frameshifts the
downstream CDS or introduces an in-frame stop. An in-frame cassette with no stop inserts
residues and leaves the reading frame intact — it is not a poison exon, whatever biotype
its transcript carries.

**3 · Exclusivity.** The event must be absent from every protein-coding transcript. An
exon compatible with making protein is not poisoning anything.

## The control, and why it licenses the answer

A method that only ever confirms is worthless, so *SCN1A* was run as a positive control
with no hint of where to look. It had to rediscover a real, drugged target.

**It did.** The scan returned exactly one decay-exclusive intronic cassette in *SCN1A*:

```
  chr2:166,007,230-166,007,293    64 bp    FRAMESHIFTS -> poison-exon shaped
```

**64 bp** — the length at which exon 20N is described in the literature, frameshifting, and
exclusive to decay isoforms. The method recovers the target of a Phase 3 drug from
annotation alone.

## The result for *BUB1B*

```
                                     BUB1B     SCN1A
  decay-biotype transcripts             12         6
  as a share of all transcripts        39%       20%
  near-full-length decay isoforms       10         3
  decay-exclusive cassettes              1         1
  POISON-EXON-SHAPED (frameshifting)     0         1
```

*BUB1B*'s single decay-exclusive cassette is **chr15:40,176,383-40,176,436, 54 bp**. It
fails the frame test, and not marginally:

- 54 is divisible by 3.
- It enters the reading frame after **384** CDS nucleotides upstream — frame +0.
- In frame +0 it reads `GAA TTG CAT GTA GTA TCT CCA GTG ATT GTT TGG CAA CTA ATA GGC ATT
  CAA TAC` — **no stop codon.**

Including it would insert 18 residues and leave the protein full-length. It cannot be what
sends its transcript to decay. (The actual cause in that isoform is a separate event: the
197 bp canonical exon 5 is skipped, and 197 is not divisible by 3.)

So the honest summary of the comparison the question asked for:

> ***BUB1B* has more non-productive annotation than *SCN1A* and less targetable
> structure.** Twice the share of decay isoforms, and no frameshifting cassette to block.

Nor is the flux concentrated anywhere else. Across the 10 near-full-length decay isoforms,
the internal skipped exons scatter — exon 5 in 3, exon 12 in 2, four others in 1 each. There
is no dominant event an ASO could aim at.

## What this negative does and does not establish

**Does not:** prove no such event exists. Ensembl annotation is not RNA-seq, and exon 20N
was found *by sequencing*, not by reading annotation. A method that reads annotation can
miss a real event, and nothing here measures what fraction of *BUB1B*'s output takes any
path in any tissue. The definitive experiment is RNA-seq of a relevant tissue, which we do
not have.

**Does:** remove the basis on which we ranked this ahead of the other candidates. That
ranking rested on *BUB1B* having an SCN1A-like target. On the best test available to us, it
does not, and the test is one that recovers SCN1A's target when pointed at SCN1A.

## Consequence for the candidate ranking

The splice-modulating ASO route **drops below the NAD⁺ precursor route**, reversing what
`PATIENT-LED-PRECEDENTS.md` said a day earlier (corrected as **C45**). It is not removed —
an RNA-seq-based search could still find something annotation cannot see, and that is now
a named piece of future work rather than a live candidate.

**What survives is the instrument.** `splice_architecture.py` answers "does this gene have
a zorevunersen-shaped target?" for any gene, carries its own positive control, and fails
loudly when the control fails. The idea it was built to support did not survive; the tool
that killed it is the more useful artefact.
