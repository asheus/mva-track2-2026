#!/usr/bin/env python3
"""MVA Track 2 deck, Mohr-lab house style — figure-led, minimal text.

Geometry and type from mohr-lab-deck/SKILL.md (locked 20 Oct 2026). The skill's
preferred route is to copy the source .pptx; the uploaded bundles carry only
SKILL.md, so this builds to the measurements. Overriding priority from that
file, honoured here: simple, easy to see, minimal text.
"""
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUT = sys.argv[1]
IMG = sys.argv[2] if len(sys.argv) > 2 else "img"

BLUE  = RGBColor(0x4F, 0x81, 0xBD)
ORANGE= RGBColor(0xF7, 0x96, 0x46)
GREEN = RGBColor(0x00, 0xB0, 0x50)
NAVY  = RGBColor(0x1F, 0x49, 0x7D)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
GREY  = RGBColor(0x5C, 0x5C, 0x5C)
RED   = RGBColor(0xC0, 0x39, 0x2B)
TINTB = RGBColor(0xF2, 0xF6, 0xFB)
TINTO = RGBColor(0xFD, 0xF3, 0xE9)
TINTG = RGBColor(0xEC, 0xF7, 0xEE)

BANNER_H = 0.905
TAKE_Y, TAKE_H = 6.95, 0.50
CITE = dict(x=8.60, y=7.05, w=4.60, h=0.35)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def title_pt(t):
    n = len(t.split())
    return 28 if n <= 9 else (25 if n <= 12 else 22)


def box(s, x, y, w, h):
    tf = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)).text_frame
    tf.word_wrap = True
    return tf


def para(tf, text, size, bold=False, color=BLACK, align=PP_ALIGN.LEFT,
         italic=False, first=False, sa=6):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.alignment, p.space_after = align, Pt(sa)
    r = p.add_run(); r.text = text
    f = r.font
    f.name, f.size, f.bold, f.italic = "Arial", Pt(size), bold, italic
    f.color.rgb = color
    return p


def banner(s, text, italics=()):
    parts, rest = [], text
    for it in italics:
        i = rest.find(it)
        if i == -1: continue
        if i: parts.append((rest[:i], False))
        parts.append((it, True)); rest = rest[i + len(it):]
    if rest: parts.append((rest, False))
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0,
                            Inches(13.333), Inches(BANNER_H))
    sh.fill.solid(); sh.fill.fore_color.rgb = BLUE     # trap 2: hard-coded
    sh.line.fill.background(); sh.shadow.inherit = False
    tf = sh.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    size = title_pt(text)
    for seg, ital in parts:
        r = p.add_run(); r.text = seg
        f = r.font
        f.name, f.size, f.bold, f.italic = "Arial", Pt(size), False, ital
        f.color.rgb = WHITE                            # trap 3: explicit
    return sh


def takeaway(s, text, size=22, wide=False):
    """SKILL.md's TAKEAWAY and CITATION boxes overlap; narrow when both appear."""
    tf = box(s, 0.45, TAKE_Y, 12.45 if wide else 7.90, TAKE_H)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    para(tf, text, size, bold=True, color=ORANGE, align=PP_ALIGN.CENTER, first=True)


def citation(s, text):
    tf = box(s, **CITE); tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    para(tf, text, 11, color=GREY, align=PP_ALIGN.RIGHT, first=True)


def rubric(s, label, pct):
    tf = box(s, 9.95, 0.96, 2.95, 0.34)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT; p.space_after = Pt(0)
    for t, c, b in ((label + "  ", ORANGE, True), (pct, GREY, False)):
        r = p.add_run(); r.text = t
        f = r.font; f.name, f.size, f.bold, f.color.rgb = "Arial", Pt(14), b, c


def card(s, x, y, w, h, fill, line=None):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                            Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line is None: sh.line.fill.background()
    else: sh.line.color.rgb = line; sh.line.width = Pt(1.5)
    sh.shadow.inherit = False; sh.adjustments[0] = 0.07
    tf = sh.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.16)
    tf.margin_top = tf.margin_bottom = Inches(0.08)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return tf


def fig(s, name, x, y, w, h):
    s.shapes.add_picture(f"{IMG}/{name}", Inches(x), Inches(y),
                         Inches(w), Inches(h))      # native aspect, never stretched



def fit(name, bx, by, bw, bh):
    """Place a figure at native aspect, centred in the box. Never stretch."""
    from PIL import Image
    w, h = Image.open(f"{IMG}/{name}").size
    sc = min(bw / w, bh / h)
    return (bx + (bw - w * sc) / 2, by + (bh - h * sc) / 2, w * sc, h * sc)


def figbox(s, name, bx, by, bw, bh):
    s.shapes.add_picture(f"{IMG}/{name}", *[Inches(v) for v in fit(name, bx, by, bw, bh)])


# ============================================================= 1 · title

# ============================================================= 1 · title
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid(); bg.fill.fore_color.rgb = NAVY
bg.line.fill.background(); bg.shadow.inherit = False
tf = box(s, 0.9, 1.70, 11.5, 1.5)
para(tf, "Rebalancing the kinetochore", 44, bold=True, color=WHITE, first=True)
tf = box(s, 0.9, 2.95, 11.5, 1.0)
para(tf, "A drug-repurposing case for one child with mosaic variegated aneuploidy",
     26, color=RGBColor(0xC9, 0xD6, 0xE6), first=True)
tf = box(s, 0.9, 4.25, 11.5, 1.9)
para(tf, "“Every cell-cycle drug in clinical use was built to break the cell cycle.",
     26, italic=True, color=ORANGE, first=True)
para(tf, "Not one was built to make it work better.”", 26, italic=True, color=ORANGE)
tf = box(s, 0.9, 6.35, 11.5, 0.5)
para(tf, "MVA Hackathon 2026  ·  Track 2  ·  proband WGS_EX2312012  ·  "
         "BUB1B p.Leu737Ter / p.Asn1002Lys", 15,
     color=RGBColor(0x9F, 0xB6, 0xCE), first=True)

# ============================================================= 2 · the problem
s = prs.slides.add_slide(BLANK)
banner(s, "THE PROBLEM: every cell division is a chance to get the chromosome count wrong")
figbox(s, "pap_cycle.png", 0.30, 1.08, 12.73, 2.10)
figbox(s, "pap_attach.png", 0.35, 3.35, 5.40, 3.35)
tf = card(s, 6.10, 3.35, 6.80, 1.56, TINTB, BLUE)
para(tf, "A checkpoint guards the hand-off", 20, bold=True, color=BLUE, first=True)
para(tf, "Each chromosome must grip both poles. Three of the four ways it can "
         "attach are wrong, so the cell holds mitosis until every one is right.", 19)
tf = card(s, 6.10, 5.14, 6.80, 1.56, TINTO, RED)
para(tf, "In this child the guard is weak", 20, bold=True, color=RED, first=True)
para(tf, "MVA: cells are born with the wrong chromosome count, giving growth "
         "failure, microcephaly and childhood cancer risk.", 19)
citation(s, "Bloom & North 2021 PMID 33892776 · McVey 2021 PMID 34445523, CC BY 4.0")

# ============================================================= 3 · the questions
s = prs.slides.add_slide(BLANK)
banner(s, "THE QUESTIONS we made this work answer, before we let ourselves pick anything")
qs = [("1", "What do these two alleles actually leave behind?",
       "Not “pathogenic”. How much protein, and with which domains.", BLUE),
      ("2", "Is the deficit reversible at all?",
       "If restoring BubR1 does nothing, no drug can work. Someone tested this.", BLUE),
      ("3", "Is there any drug that raises BubR1, or its phosphatase?",
       "Asked across the whole druggable universe, not a shortlist.", ORANGE),
      ("4", "If not, what else sits on the same node — and at what dose?",
       "Answered on measured human exposure, or not answered.", GREEN)]
y = 1.32
for n, q, sub, c in qs:
    tf = card(s, 0.45, y, 12.45, 1.26, TINTG if c == GREEN else
              (TINTO if c == ORANGE else TINTB), c)
    p = tf.paragraphs[0]; p.space_after = Pt(2)
    for t, sz, b, col in ((n + "   ", 26, True, c), (q, 23, True, BLACK)):
        r = p.add_run(); r.text = t
        f = r.font; f.name, f.size, f.bold, f.color.rgb = "Arial", Pt(sz), b, col
    para(tf, "      " + sub, 19, color=GREY)
    y += 1.37
takeaway(s, "Each question had to close before the next one opened", wide=True)

# ============================================================= 4 · the alleles
s = prs.slides.add_slide(BLANK)
banner(s, "Q1 — Two alleles, and the domain that sits between them")
figbox(s, "fig_domains2.png", 0.25, 1.12, 12.83, 3.95)
tf = card(s, 0.45, 5.22, 3.95, 1.46, TINTB, BLUE)
para(tf, "Allele 1 truncates at 737", 19, bold=True, color=BLUE, first=True)
para(tf, "73 nt upstream of the last junction, so the transcript is destroyed.", 18)
tf = card(s, 4.69, 5.22, 3.95, 1.46, TINTB, BLUE)
para(tf, "Allele 2 is buried, not surface", 19, bold=True, color=BLUE, first=True)
para(tf, "87% buried. Made, then degraded: a dosage mutant, not an interface one.", 18)
tf = card(s, 8.93, 5.22, 3.95, 1.46, TINTO, ORANGE)
para(tf, "Both land on the KARD", 19, bold=True, color=ORANGE, first=True)
para(tf, "667–681: the motif that recruits the phosphatase PP2A-B56.", 18)
citation(s, "Domain layout adapted from Bloom & North 2021, PMID 33892776")

# ============================================================= 5 · scalability
s = prs.slides.add_slide(BLANK)
banner(s, "SCALABILITY (15%) — we scored every BUB1B allele, not this child's two")
rubric(s, "Scalability", "15%")
figbox(s, "fig_scoring.png", 0.30, 1.40, 12.73, 4.35)
tf = box(s, 0.45, 5.88, 12.45, 0.95)
para(tf, "Suijkerbuijk reached the same two classes experimentally: truncating alleles "
         "lose the transcript, missense alleles are made and turned over.", 20,
     align=PP_ALIGN.CENTER, first=True)
citation(s, "Suijkerbuijk et al., Cancer Res 2010, PMID 20516114")

# ============================================================= 6 · mechanism
s = prs.slides.add_slide(BLANK)
banner(s, "Q1 \u2014 Aurora B LOOSENS grips on purpose. PP2A-B56 SETS them. This child cannot set.")
figbox(s, "pap_kcmt_annot.png", 0.40, 1.20, 4.85, 5.50)
tf = card(s, 5.55, 1.26, 7.35, 1.66, TINTO, ORANGE)
para(tf, "AURORA B \u2014 the loosener", 20, bold=True, color=ORANGE, first=True)
para(tf, "It phosphorylates the GRIP (Hec1) holding a chromosome to a microtubule. "
         "A phosphorylated grip lets go. That is how wrong attachments get broken.", 18)
tf = card(s, 5.55, 3.02, 7.35, 1.66, TINTG, GREEN)
para(tf, "PP2A-B56 \u2014 the setter", 20, bold=True, color=GREEN, first=True)
para(tf, "It removes those phosphates so a correct grip can set. Error correction is "
         "these two in a tug-of-war, and both are needed.", 18)
tf = card(s, 5.55, 4.78, 7.35, 1.04, TINTB, BLUE)
para(tf, "BubR1 is the TAXI, not an enzyme. Plk1 puts 3 phosphates in its KARD (shown "
         "left, on BubR1): that is the TICKET PP2A-B56 binds. Different phosphates, "
         "opposite job to Aurora B's.", 18, first=True)
tf = card(s, 5.55, 5.92, 7.35, 0.78, TINTO, RED)
para(tf, "No KARD delivered \u2192 no setter arrives \u2192 Aurora B is not stronger, "
         "it is UNOPPOSED. So we lower it to match.", 18, bold=True, color=RED, first=True)
citation(s, "Bloom & North 2021, Fig 2 detail; Aurora B added by us")

# ============================================================= 7 · reversible
s = prs.slides.add_slide(BLANK)
banner(s, "Q2 — The deficit is reversible: put BubR1 back and the checkpoint recovers")
figbox(s, "pap_rescue.png", 0.30, 1.15, 7.95, 5.55)
tf = card(s, 8.55, 1.30, 4.35, 1.72, TINTB, BLUE)
para(tf, "This child's genotype shape", 19, bold=True, color=BLUE, first=True)
para(tf, "753X/R814H and 731X/Y155C: one truncating allele, one missense — "
         "the MVA pattern.", 18)
tf = card(s, 8.55, 3.18, 4.35, 1.72, TINTG, GREEN)
para(tf, "2.06x and 2.01x", 19, bold=True, color=GREEN, first=True)
para(tf, "Nocodazole arrest doubles when BubR1 is restored. Healthy controls and "
         "the carrier parent do not move.", 18)
tf = card(s, 8.55, 5.06, 4.35, 1.64, TINTO, ORANGE)
para(tf, "But it does not normalise", 19, bold=True, color=ORANGE, first=True)
para(tf, "15%→31% and 26%→50% of healthy. And no drug raises BubR1.", 18)
citation(s, "Suijkerbuijk et al., Cancer Res 2010, PMID 20516114, Fig 1D")

# ============================================================= 8 · rigor
s = prs.slides.add_slide(BLANK)
banner(s, "SCIENTIFIC RIGOR (35%) — Q3: ten arms, four themes, every one closed on a number")
rubric(s, "Scientific rigor", "35%")
figbox(s, "fig_themes.png", 0.35, 1.30, 5.55, 5.12)
figbox(s, "fig_exposure.png", 6.15, 1.80, 6.85, 2.90)
tf = box(s, 6.15, 4.95, 6.85, 1.55)
para(tf, "Two gates closed these arms. EXPOSURE: most needed more drug than a person "
         "can be given. SAFETY IN THIS CHILD: proteasome and HSP90 inhibitors are "
         "myelosuppressive and carcinogenic, disqualifying where tumour risk already "
         "comes from missegregation. Barasertib alone sits 1,200x ABOVE the effect.",
     17, align=PP_ALIGN.CENTER, first=True)
takeaway(s, "Three themes die upstream. One node survives.", size=20, wide=True)

# ============================================================= 9 · innovation
s = prs.slides.add_slide(BLANK)
banner(s, "INNOVATION (25%) — many engines generate, one human decides, nothing rests on one paper")
rubric(s, "Innovation", "25%")
figbox(s, "fig_funnel.png", 0.60, 1.22, 12.10, 4.42)
figbox(s, "fig_evidence.png", 0.40, 5.78, 12.53, 1.22)

# ============================================================= 10 · the drug
s = prs.slides.add_slide(BLANK)
banner(s, "POTENTIAL IMPACT (25%) — Q4: lower the kinase, because the phosphatase cannot be raised")
rubric(s, "Potential impact", "25%")
figbox(s, "barasertib_hqpa.png", 0.45, 1.70, 3.90, 2.70)
tf = box(s, 0.45, 4.45, 3.90, 0.45)
para(tf, "barasertib-hQPA", 17, color=GREY, align=PP_ALIGN.CENTER, first=True)
figbox(s, "pap_kard_surface.png", 0.45, 4.95, 3.90, 1.75)
tf = box(s, 0.45, 6.72, 3.90, 0.40)
para(tf, "the groove neither allele reaches", 13, color=GREY,
     align=PP_ALIGN.CENTER, first=True)
rows = [("0.37 nM", "Aurora B IC50", BLUE),
        ("~3,700x", "selective over Aurora A", BLUE),
        ("447 nM", "human steady-state Css", BLUE),
        ("~1,200x", "Css over IC50 — the only candidate that needs LESS drug", GREEN)]
y = 1.50
for big, lab, c in rows:
    tf = card(s, 4.65, y, 8.25, 1.14, TINTG if c == GREEN else TINTB, c)
    p = tf.paragraphs[0]; p.space_after = Pt(0)
    for t, sz, b, col in ((big + "   ", 28, True, c), (lab, 20, False, BLACK)):
        r = p.add_run(); r.text = t
        f = r.font; f.name, f.size, f.bold, f.color.rgb = "Arial", Pt(sz), b, col
    y += 1.26
tf = box(s, 4.65, 6.60, 8.25, 0.55)
para(tf, "Structure: PP2A-B56 surface with the BubR1 KARD peptide bound "
         "(Bloom & North 2021, CC BY 4.0)", 13, color=GREY, first=True)

# ============================================================= 11 · the window
s = prs.slides.add_slide(BLANK)
banner(s, "The window is narrow, we name it ourselves, and it is the experiment we propose")
figbox(s, "fig_window.png", 0.45, 1.25, 7.55, 4.45)
tf = card(s, 8.25, 1.55, 4.63, 1.58, TINTG, GREEN)
para(tf, "Calibrate on PD, not dose", 22, bold=True, color=GREEN, first=True)
para(tf, "1-10x IC50 free. Titrate phospho-Hec1, never to ablation.", 20)
tf = card(s, 8.25, 3.33, 4.63, 1.58, TINTO, ORANGE)
para(tf, "Measure both curves", 22, bold=True, color=ORANGE, first=True)
para(tf, "Congression rescue and checkpoint competence, same cells.", 20)
tf = card(s, 8.25, 5.11, 4.63, 1.58, TINTB, RED)
para(tf, "The risk we are not hiding", 22, bold=True, color=RED, first=True)
para(tf, "Slide 7 showed this checkpoint at 15-26% of normal. Our drug must not cost it.", 20)
citation(s, "Santaguida 2011, PMID 21399614")

# ============================================================= 12 · moonshot
s = prs.slides.add_slide(BLANK)
banner(s, "The moonshot: programmable translation, on the message the patient already has")
figbox(s, "pap_trna.png", 0.35, 1.15, 12.63, 3.05)
tf = card(s, 0.45, 4.40, 4.05, 2.30, TINTB, BLUE)
para(tf, "What it does", 20, bold=True, color=BLUE, first=True)
para(tf, "A separate capped RNA (orange) base-pairs with the target mRNA (blue). The "
         "ribosome loads from the trans-cap and is handed to a start codon of our "
         "choosing.", 18)
tf = card(s, 4.74, 4.40, 4.05, 2.30, TINTG, GREEN)
para(tf, "Why it reaches this child", 20, bold=True, color=GREEN, first=True)
para(tf, "Allele 1's transcript is gone, so nothing can rescue it. But allele 2's "
         "message IS present \u2014 raising its output is a genome-free way to restore "
         "the dose.", 18)
tf = card(s, 9.03, 4.40, 3.85, 2.30, TINTO, ORANGE)
para(tf, "Why it deserves funding", 20, bold=True, color=ORANGE, first=True)
para(tf, "One mechanism, no edit, and dosage disease is a whole class. Delivery is the "
         "unsolved half: liver and muscle today, brain and marrow not yet.", 18)
citation(s, "Jia et al., Nat Biotechnol 2025, Fig 1a")

# ============================================================= 13 · close
s = prs.slides.add_slide(BLANK)
banner(s, "What we answered, and the one prediction we commit to")
y = 1.30
for q, a, c in [("Q1  What do the alleles leave?",
                 "No transcript, and an unstable protein. Both lose the KARD's function.", BLUE),
                ("Q2  Is it reversible?",
                 "Yes — restoring BubR1 doubles checkpoint arrest in patient cells.", BLUE),
                ("Q3  Can a drug raise BubR1?",
                 "No. Zero compounds across 107,407 curated pairs, and no PP2A activator.", ORANGE),
                ("Q4  What else sits on the node?",
                 "Aurora B — the one target where human exposure runs in our favour.", GREEN)]:
    tf = card(s, 0.45, y, 12.45, 1.06, TINTG if c == GREEN else
              (TINTO if c == ORANGE else TINTB), c)
    p = tf.paragraphs[0]; p.space_after = Pt(0)
    for t, sz, b, col in ((q + "    ", 20, True, c), (a, 20, False, BLACK)):
        r = p.add_run(); r.text = t
        f = r.font; f.name, f.size, f.bold, f.color.rgb = "Arial", Pt(sz), b, col
    y += 1.17
tf = card(s, 0.45, 6.02, 12.45, 1.14, TINTG, GREEN)
para(tf, "The prediction: partial Aurora B inhibition rescues congression in this "
         "child's cells BEFORE it costs checkpoint competence. If it does not, we are wrong.",
     21, bold=True, color=GREEN, align=PP_ALIGN.CENTER, first=True)

prs.save(OUT)
print(f"saved {OUT}")
