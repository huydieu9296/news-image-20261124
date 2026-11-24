#!/usr/bin/env python3
"""Draw a one-page newspaper front page for Tuesday 24 November 2026.

Layout: a navy masthead naming the day, a red rule, then six story
cards in a two-by-three grid. Every card has a coloured spine, a
hand-drawn line glyph, a kicker, a headline that shrinks until it fits
two lines, a two-line deck and a one-line key-fact strip, with a
centred footer line underneath.

The six stories are the day's verified headlines, as reported on
24 November 2026: Nvidia reinstates Jensen Huang as CEO and its
shares jump 31% after Trump intervenes; Russian strikes kill at
least 14 in Ukraine's Kyiv region as Zelenskyy calls for four-way
talks and urges the US to release Patriot missiles; the death toll
from the Indonesian candy-factory fire rises to 24 with about 30
still missing; Oregon and Virginia sue Musk's firms over
nonconsensual sexualised images made with the Grok chatbot; Rep.
Jimmy Gomez resigns from Congress after the Ethics panel finds
evidence of sexual misconduct; and storms and airline glitches
threaten messy Thanksgiving travel across the US.

Everything is fixed: same fonts, same positions, no randomness, no
clock, no network. Running this file writes entry.png next to itself.
"""

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (246, 241, 227)
CARD = (255, 253, 246)
CARD_EDGE = (220, 213, 194)
NAVY = (22, 35, 63)
NAVY_SUB = (201, 210, 224)
RED = (180, 35, 24)
INK = (28, 28, 26)
DECK = (74, 70, 62)
GREY = (122, 114, 100)
HAIRLINE = (214, 207, 188)
TITLE_FILL = (250, 247, 238)

MASTHEAD = "THE WORLD IN ONE DAY"
DATELINE = "TUESDAY, 24 NOVEMBER 2026"
FOOTER = ("Six stories from a single day  ·  Compiled from verified reports  ·  "
          "24 November 2026")


@dataclass
class Story:
    kicker: str
    headline: str
    deck: str
    fact: str
    accent: tuple
    glyph: str


STORIES = [
    Story(
        "TECH  ·  USA",
        "Huang is back — Nvidia soars 31%",
        "Nvidia reinstates Jensen Huang as CEO after Trump "
        "intervenes; shares jump a third, Nasdaq rallies 6.5%.",
        "Nearly $1 trillion added in a single day",
        (21, 101, 192),
        "chip",
    ),
    Story(
        "WAR  ·  UKRAINE",
        "Kyiv strikes kill 14; Zelensky seeks talks",
        "Russian strikes hit a Kyiv-region flat block and a store; "
        "Zelenskyy calls for four-way talks as soon as possible.",
        "Urges US to release paid-for Patriot missiles",
        (166, 28, 28),
        "missile",
    ),
    Story(
        "DISASTER  ·  INDONESIA",
        "Factory fire toll rises to 24",
        "Candy-factory fire near Jakarta kills 24; about 30 still "
        "missing as rescuers search the unstable wreckage.",
        "Fire broke out on Saturday evening",
        (178, 106, 0),
        "flame",
    ),
    Story(
        "TECH  ·  AI",
        "States sue Musk firms over Grok images",
        "Oregon and Virginia sue over nonconsensual sexualised "
        "images of real people made with the Grok chatbot.",
        "Lawsuits target SpaceX's AI company",
        (106, 63, 181),
        "chat",
    ),
    Story(
        "POLITICS  ·  USA",
        "Congressman Gomez to quit over ethics probe",
        "Rep. Jimmy Gomez resigns effective 1 December after the "
        "Ethics panel finds evidence of sexual misconduct.",
        "Bipartisan panel found 'substantial evidence'",
        (27, 125, 61),
        "dome",
    ),
    Story(
        "WEATHER  ·  USA",
        "Storms threaten messy Thanksgiving travel",
        "Storms and airline glitches threaten holiday travel as "
        "millions head home for Thanksgiving.",
        "East Coast storm is the biggest worry",
        (14, 124, 123),
        "cloud",
    ),
]


def load_font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else PLAIN, size)


def wrap_text(draw, text, fnt, max_width):
    """Greedy word wrap; returns the lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_lines(draw, text, max_width, max_lines, start, floor, bold):
    """Shrink the font until the text wraps into at most max_lines.

    If it still overflows at the smallest size, clip the last line
    with an ellipsis so nothing ever draws outside its box.
    """
    size = start
    while size > floor:
        fnt = load_font(size, bold=bold)
        if len(wrap_text(draw, text, fnt, max_width)) <= max_lines:
            return wrap_text(draw, text, fnt, max_width), fnt
        size -= 1
    fnt = load_font(floor, bold=bold)
    lines = wrap_text(draw, text, fnt, max_width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        tail = lines[-1]
        while tail and draw.textlength(tail + "…", font=fnt) > max_width:
            tail = tail.rsplit(" ", 1)[0] if " " in tail else tail[:-1]
        lines[-1] = tail + "…"
    return lines, fnt


def draw_glyph(draw, kind, x0, y0, size, colour):
    """A small line-drawn glyph inside the square (x0, y0, size)."""
    x1, y1 = x0 + size, y0 + size
    cx, cy = x0 + size // 2, y0 + size // 2
    w = 3
    if kind == "missile":
        # A rocket climbing diagonally, with a flame trail.
        draw.polygon([(x0 + 26, y0 + 4), (x0 + 36, y0 + 14),
                      (x0 + 30, y0 + 24), (x0 + 22, y0 + 14)],
                     outline=colour, width=w)
        draw.line([x0 + 22, y0 + 22, x0 + 12, y0 + 34], fill=colour, width=w)
        draw.line([x0 + 30, y0 + 26, x0 + 20, y0 + 38], fill=colour, width=2)
        draw.line([x0 + 10, y0 + 40, x0 + 18, y0 + 32], fill=colour, width=2)
        draw.ellipse([x0 + 30, y0 + 30, x0 + 40, y0 + 40], fill=colour)
    elif kind == "chip":
        # A computer chip: square body, inner die and pins.
        draw.rectangle([x0 + 10, y0 + 10, x1 - 10, y1 - 10],
                       outline=colour, width=w)
        draw.rectangle([x0 + 17, y0 + 17, x1 - 17, y1 - 17],
                       outline=colour, width=2)
        for px in (x0 + 16, x0 + 23, x0 + 30):
            draw.line([px, y0 + 4, px, y0 + 10], fill=colour, width=2)
            draw.line([px, y1 - 10, px, y1 - 4], fill=colour, width=2)
        for py in (y0 + 16, y0 + 23, y0 + 30):
            draw.line([x0 + 4, py, x0 + 10, py], fill=colour, width=2)
            draw.line([x1 - 10, py, x1 - 4, py], fill=colour, width=2)
    elif kind == "flame":
        # A flame: outer tongue and inner core.
        draw.arc([x0 + 8, y0 + 10, x1 - 8, y0 + 34], 0, 180,
                 fill=colour, width=w)
        draw.line([x0 + 8, y0 + 22, cx, y0 + 4], fill=colour, width=w)
        draw.line([cx, y0 + 4, x1 - 8, y0 + 22], fill=colour, width=w)
        draw.arc([x0 + 16, y0 + 22, x1 - 16, y0 + 40], 0, 180,
                 fill=colour, width=2)
        draw.line([x0 + 16, y0 + 31, cx, y0 + 20], fill=colour, width=2)
        draw.line([cx, y0 + 20, x1 - 16, y0 + 31], fill=colour, width=2)
    elif kind == "chat":
        # A chat bubble with three dots.
        draw.rounded_rectangle([x0 + 4, y0 + 8, x1 - 4, y1 - 14],
                               radius=7, outline=colour, width=w)
        draw.polygon([(x0 + 14, y1 - 14), (x0 + 10, y1 - 2),
                      (x0 + 22, y1 - 14)], fill=colour)
        for dx in (-10, 0, 10):
            draw.ellipse([cx + dx - 3, cy - 4, cx + dx + 3, cy + 2],
                         fill=colour)
    elif kind == "dome":
        # A capitol dome: base, columns and dome.
        draw.arc([x0 + 10, y0 + 4, x1 - 10, y0 + 26], 180, 360,
                 fill=colour, width=w)
        draw.line([cx, y0 + 2, cx, y0 + 8], fill=colour, width=2)
        draw.line([x0 + 8, y0 + 24, x1 - 8, y0 + 24], fill=colour, width=w)
        for dx in (-12, -4, 4, 12):
            draw.line([cx + dx, y0 + 24, cx + dx, y0 + 34],
                      fill=colour, width=2)
        draw.line([x0 + 6, y0 + 36, x1 - 6, y0 + 36], fill=colour, width=w)
    elif kind == "cloud":
        # A rain cloud with three drops.
        draw.arc([x0 + 6, y0 + 8, x0 + 24, y0 + 24], 90, 360,
                 fill=colour, width=w)
        draw.arc([x0 + 16, y0 + 4, x0 + 34, y0 + 22], 180, 360,
                 fill=colour, width=w)
        draw.arc([x0 + 28, y0 + 10, x1 - 4, y0 + 26], 270, 90,
                 fill=colour, width=w)
        draw.line([x0 + 8, y0 + 24, x1 - 6, y0 + 24], fill=colour, width=w)
        for dx in (-10, 0, 10):
            draw.line([cx + dx, y0 + 32, cx + dx - 2, y0 + 38],
                      fill=colour, width=2)


def draw_card(draw, story, bx, by, bw, bh):
    """One story card: spine, kicker and glyph, headline, deck, fact."""
    draw.rectangle([bx, by, bx + bw, by + bh], fill=CARD,
                   outline=CARD_EDGE, width=1)
    draw.rectangle([bx + 1, by + 1, bx + 10, by + bh - 1], fill=story.accent)

    tx = bx + 26
    tw = bw - 26 - 20
    draw.text((tx, by + 18), story.kicker, font=load_font(16, bold=True),
              fill=story.accent)
    draw_glyph(draw, story.glyph, bx + bw - 20 - 46, by + 14, 46,
               story.accent)

    lines, fnt = fit_lines(draw, story.headline, tw, 2, 30, 18, bold=True)
    y = by + 64
    for line in lines:
        draw.text((tx, y), line, font=fnt, fill=INK)
        y += fnt.size + 8

    lines, fnt = fit_lines(draw, story.deck, tw, 2, 18, 14, bold=False)
    y = by + 150
    for line in lines:
        draw.text((tx, y), line, font=fnt, fill=DECK)
        y += fnt.size + 8

    draw.line([tx, by + bh - 42, bx + bw - 20, by + bh - 42],
              fill=HAIRLINE, width=1)
    draw.text((tx, by + bh - 32), story.fact, font=load_font(16, bold=True),
              fill=story.accent)


def render():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)

    # Masthead: title, dateline, red rule.
    draw.rectangle([0, 0, PAGE_W, 140], fill=NAVY)
    title_fnt = load_font(56, bold=True)
    tw = draw.textlength(MASTHEAD, font=title_fnt)
    draw.text(((PAGE_W - tw) / 2, 24), MASTHEAD, font=title_fnt,
              fill=TITLE_FILL)
    date_fnt = load_font(23)
    dw = draw.textlength(DATELINE, font=date_fnt)
    draw.text(((PAGE_W - dw) / 2, 98), DATELINE, font=date_fnt, fill=NAVY_SUB)
    draw.rectangle([0, 140, PAGE_W, 145], fill=RED)

    # Six cards, two columns by three rows.
    margin, gutter = 28, 20
    grid_top, grid_bottom = 162, 962
    card_w = (PAGE_W - 2 * margin - gutter) // 2
    card_h = (grid_bottom - grid_top - 2 * 16) // 3
    for i, story in enumerate(STORIES):
        row, col = divmod(i, 2)
        bx = margin + col * (card_w + gutter)
        by = grid_top + row * (card_h + 16)
        draw_card(draw, story, bx, by, card_w, card_h)

    footer_fnt = load_font(15)
    fw = draw.textlength(FOOTER, font=footer_fnt)
    draw.text(((PAGE_W - fw) / 2, 980), FOOTER, font=footer_fnt, fill=GREY)

    out = Path(__file__).resolve().parent / "entry.png"
    page.save(out, format="PNG")
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    render()
