#!/usr/bin/env python3
"""Grounding screen for scientific claims.

The scientific counterpart of roast-room's check_quotes.py (MIT,
github.com/nateherkai/roast-room). That script enforces that a persona's quotes
appear verbatim in a cited source. This one enforces the project's own standing
rule: a quantitative claim ships with the thing that produced it -- a committed
query, a PMID, or a DOI -- or it ships explicitly labelled as untraced.

WHAT THIS IS: a cheap screen that narrows where a reviewer looks.
WHAT THIS IS NOT: a proof of grounding. It matches tokens near a claim; it does
not read the source or check that the source says what the claim says. Its
measured behaviour on a labelled panel is printed by --selftest and must be
quoted wherever its output is. This disclaimer exists because this project
already shipped a 56%-sensitive detector described as a general instrument
(CORRECTIONS-2026-10-06.md, C46); the lesson is applied here rather than
re-learned.
"""
import argparse
import pathlib
import re
import sys

# A quantitative assertion carries a unit or a magnitude marker. Bare integers
# (dates, residue numbers, section refs, HPO ids) are deliberately NOT claims:
# matching them produced unusable noise in development.
CLAIM = re.compile(r"""
    (?<![\w.])
    (?:
        \d[\d,]*\.?\d*\s?%                                  # 35%, 4.28 %
      | \d[\d,]*\.?\d*\s?(?:×|x)\b                     # 2.2x, 1.43 times
      | \d[\d,]*\.?\d*[-–]fold                         # 5-fold
      | \d[\d,]*\.?\d*\s?kcal/mol                           # +1.51 kcal/mol
      | \d[\d,]*\.?\d*\s?(?:nt|bp|aa|Å)\b              # 748 nt, 10,911 bp
      | [pqn]\s?=\s?[\d.][\d.eE+-]*                         # p=0.0384, n=31
      | (?:ρ|rho|r)\s?=\s?[-+]?[\d.][\d.eE+-]*         # rho=-0.665
    )
""", re.VERBOSE)

# Tokens that count as grounding.
GROUND = re.compile(r"""
    (?:
        PMID[:\s]*\d{6,9}
      | PMC\d{6,9}
      | \b10\.\d{4,9}/\S+
      | \b[a-z_][a-z0-9_]*\.py\b
      | \b[A-Za-z0-9_-]+\.(?:json|jsonl|tsv|csv|sqlite|xlsx)\b
      | \b[A-Z][A-Z0-9-]{3,}\.md\b
    )
""", re.VERBOSE)

# Explicit honesty labels. A labelled claim PASSES: saying "untraced" is the
# behaviour the rule wants, not a violation of it.
LABEL = re.compile(
    r"FIGURE_ONLY|untraced|not traced|untraceable|unverified|cannot be traced"
    r"|TO BE FILLED|QUARANTINED|not citable|trajectory-only|no primary source",
    re.IGNORECASE,
)

def scan(text, window):
    """Yield (lineno, claim, status) for every quantitative claim."""
    lines = text.splitlines()
    out = []
    for i, line in enumerate(lines):
        if line.lstrip().startswith(("|---", "```")):
            continue
        for m in CLAIM.finditer(line):
            lo = max(0, i - window)
            hi = min(len(lines), i + window + 1)
            ctx = "\n".join(lines[lo:hi])
            if GROUND.search(ctx):
                status = "grounded"
            elif LABEL.search(ctx):
                status = "labelled"
            else:
                status = "UNGROUNDED"
            out.append((i + 1, m.group(0).strip(), status))
    return out

# Labelled panel: crafted positives (should flag) and negatives (should pass).
PANEL = [
    ("Protein fell 71.1% in T-47D cells.", "UNGROUNDED"),
    ("BubR1 rose 2.2x after knockout.", "UNGROUNDED"),
    ("The stop sits 748 nt upstream.", "UNGROUNDED"),
    ("Median lifespan rose 58% (p=0.0384).", "UNGROUNDED"),
    ("Residual was 13% in that titration.", "UNGROUNDED"),
    ("Lifespan rose 58% (North 2014, PMID 24825348).", "grounded"),
    ("The stop sits 748 nt upstream, per ptc_context.py.", "grounded"),
    ("Mutants fell 5-fold (doi 10.1158/0008-5472.CAN-09-4319).", "grounded"),
    ("Residual 35% is FIGURE_ONLY and QUARANTINED.", "labelled"),
    ("It reported 89.4% but this is untraced to a primary source.", "labelled"),
]

def selftest(window):
    tp = fp = tn = fn = 0
    for text, want in PANEL:
        got = scan(text, window)
        flagged = any(s == "UNGROUNDED" for _, _, s in got)
        if not got:
            print("  PANEL GAP: no claim detected in: " + text)
            continue
        should_flag = want == "UNGROUNDED"
        if should_flag and flagged:
            tp += 1
        elif should_flag and not flagged:
            fn += 1
        elif not should_flag and flagged:
            fp += 1
        else:
            tn += 1
    sens = tp / (tp + fn) if (tp + fn) else 0.0
    spec = tn / (tn + fp) if (tn + fp) else 0.0
    print("  positives: %d/%d flagged   sensitivity %.0f%%" % (tp, tp + fn, 100 * sens))
    print("  negatives: %d/%d passed    specificity %.0f%%" % (tn, tn + fp, 100 * spec))
    return sens, spec

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", type=pathlib.Path)
    ap.add_argument("--window", type=int, default=3,
                    help="lines either side searched for a grounding token")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--quiet", action="store_true", help="counts only")
    a = ap.parse_args()

    print("GROUNDING SCREEN -- a screen, not a proof. Measured behaviour:")
    sens, spec = selftest(a.window)
    if a.selftest and not a.files:
        return 0 if (sens >= 0.99 and spec >= 0.99) else 1

    total = ungrounded = 0
    for f in a.files:
        if not f.exists():
            print("\nMISSING: %s" % f)
            continue
        rows = scan(f.read_text(encoding="utf-8"), a.window)
        bad = [r for r in rows if r[2] == "UNGROUNDED"]
        total += len(rows)
        ungrounded += len(bad)
        pct = (100.0 * len(bad) / len(rows)) if rows else 0.0
        print("\n%s" % f)
        print("  claims %d   ungrounded %d (%.0f%%)" % (len(rows), len(bad), pct))
        if not a.quiet:
            for ln, claim, _ in bad[:25]:
                print("    L%-6d %s" % (ln, claim))
            if len(bad) > 25:
                print("    ... %d more" % (len(bad) - 25))
    if total:
        print("\nTOTAL claims %d   ungrounded %d (%.0f%%)"
              % (total, ungrounded, 100.0 * ungrounded / total))
    return 0

if __name__ == "__main__":
    sys.exit(main())
