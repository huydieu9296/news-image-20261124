#!/usr/bin/env python3
"""The World in One Day -- Tuesday, 24 November 2026.

Draws a 1024x1024 newspaper front page summing up the day's world news
and writes it to /output/entry.png.

Reads nothing from disk except fonts, uses no network, no clock and no
randomness, so every run writes exactly the same bytes.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "/output/entry.png"

PAPER = (247, 243, 234)   # warm newsprint
INK = (26, 26, 26)        # near-black ink
MUTED = (96, 89, 76)      # grey-brown for datelines and footers
RED = (185, 28, 28)       # masthead accent
NAVY = (30, 58, 95)       # deep blue for rules

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
BOLD = "DejaVuSans-Bold.ttf"
REG = "DejaVuSans.ttf"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(draw, text, fname, start, max_w, max_lines):
    """Largest font size (shrinking from start) whose wrap fits max_lines."""
    size = start
    while size > 12:
        fnt = font(fname, size)
        if len(wrap(draw, text, fnt, max_w)) <= max_lines:
            return fnt, wrap(draw, text, fnt, max_w)
        size -= 1
    fnt = font(fname, 12)
    return fnt, wrap(draw, text, fnt, max_w)


# ---------------------------------------------------------------- pictograms
# Small geometric marks drawn with plain shapes; they decorate the cards
# while the headlines and summaries carry the news.

def chip(d, x, y, s, color):
    """A microchip: dark square, inner die, pins on all four sides."""
    d.rounded_rectangle([x, y, x + s, y + s], radius=s // 8, fill=color)
    d.rounded_rectangle([x + s // 4, y + s // 4, x + 3 * s // 4, y + 3 * s // 4],
                        radius=s // 16, outline=(255, 255, 255), width=3)
    for i in range(3):
        off = s // 4 + i * s // 4
        d.line([x + off, y - 8, x + off, y], fill=color, width=4)
        d.line([x + off, y + s, x + off, y + s + 8], fill=color, width=4)
        d.line([x - 8, y + off, x, y + off], fill=color, width=4)
        d.line([x + s, y + off, x + s + 8, y + off], fill=color, width=4)


def burst(d, x, y, s, color):
    """A starburst: 12 spikes around a dark centre."""
    cx, cy = x + s // 2, y + s // 2
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        r = s // 2 if i % 2 == 0 else s // 4
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=color)
    d.ellipse([cx - s // 6, cy - s // 6, cx + s // 6, cy + s // 6], fill=INK)


def phone(d, x, y, s, color):
    """A phone with a chat bubble on its screen."""
    d.rounded_rectangle([x + s // 5, y, x + 4 * s // 5, y + s], radius=s // 8,
                        fill=color)
    d.rounded_rectangle([x + s // 5 + 8, y + 12, x + 4 * s // 5 - 8, y + s - 12],
                        radius=6, fill=(255, 255, 255))
    bx, by, bw, bh = x + s // 5 + 18, y + 22, s // 2, s // 4
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=8, fill=color)
    d.polygon([(bx + 8, by + bh), (bx + 8, by + bh + 12), (bx + 24, by + bh)],
              fill=color)
    d.line([bx + 10, by + bh // 2 - 4, bx + bw - 10, by + bh // 2 - 4],
           fill=(255, 255, 255), width=3)
    d.line([bx + 10, by + bh // 2 + 4, bx + bw - 22, by + bh // 2 + 4],
           fill=(255, 255, 255), width=3)


def jet(d, x, y, s, color):
    """A jet seen from above: pointed nose, delta wings, tail."""
    cx = x + s // 2
    d.polygon([(cx, y + 4), (x + s - 4, y + 3 * s // 4),
               (cx + s // 8, y + 5 * s // 8), (cx + s // 8, y + s - 4),
               (cx - s // 8, y + s - 4), (cx - s // 8, y + 5 * s // 8),
               (x + 4, y + 3 * s // 4)], fill=color)
    d.line([cx, y + s // 4, cx, y + s // 2], fill=(255, 255, 255), width=4)


def shield(d, x, y, s, color):
    """A shield with a check mark."""
    top = y + 8
    pts = [(x + s // 2, top), (x + s - 6, top + s // 4),
           (x + s - 6, top + s // 2),
           (x + s // 2, y + s - 6), (x + 6, top + s // 2),
           (x + 6, top + s // 4)]
    d.polygon(pts, outline=color, width=4)
    d.line([x + s // 4, y + s // 2, x + s // 2 - 4, y + 2 * s // 3],
           fill=color, width=5)
    d.line([x + s // 2 - 4, y + 2 * s // 3, x + 3 * s // 4, y + s // 3],
           fill=color, width=5)


def globe(d, x, y, s, color):
    """A globe: circle, meridians and parallels."""
    d.ellipse([x, y, x + s, y + s], outline=color, width=4)
    d.ellipse([x + s // 4, y, x + 3 * s // 4, y + s], outline=color, width=3)
    d.line([x, y + s // 2, x + s, y + s // 2], fill=color, width=3)
    d.arc([x, y + s // 6, x + s, y + 5 * s // 6], 0, 360, fill=color, width=3)


ICONS = {"chip": chip, "burst": burst, "phone": phone,
         "jet": jet, "shield": shield, "globe": globe}


# ------------------------------------------------------------------- stories
# Six stories first reported on Tuesday, 24 November 2026 (Reuters, AP,
# AFP, SCMP). Headlines are short on purpose so they survive wrapping.

STORIES = [
    {
        "kicker": "TECHNOLOGY  •  UNITED STATES",
        "color": (21, 128, 61),
        "icon": "chip",
        "headline": "Huang back as Nvidia chief after Trump steps in",
        "summary": "The board reinstated Jensen Huang as CEO, 11 days after he "
                   "stepped down; shares jumped 33%.",
    },
    {
        "kicker": "WAR  •  UKRAINE",
        "color": (185, 28, 28),
        "icon": "burst",
        "headline": "Russian strikes kill at least 14 in Kyiv region",
        "summary": "Missile and drone attacks hit homes around the capital as "
                   "the war's toll on civilians grew again.",
    },
    {
        "kicker": "AI  •  UNITED STATES",
        "color": (124, 58, 237),
        "icon": "phone",
        "headline": "States sue Musk firms over Grok's sexualised images",
        "summary": "State attorneys say the chatbot generated sexualised images "
                   "of real people without their consent.",
    },
    {
        "kicker": "SECURITY  •  ASIA",
        "color": (30, 58, 95),
        "icon": "jet",
        "headline": "Seoul warns island after Russian jet enters airspace",
        "summary": "South Korea briefly told Ulleung islanders to shelter as a "
                   "Russian aircraft crossed into its air defence zone.",
    },
    {
        "kicker": "DIPLOMACY  •  ASIA-PACIFIC",
        "color": (15, 118, 110),
        "icon": "shield",
        "headline": "Trump offers Manila $2.4bn for self-defence",
        "summary": "Washington's defence aid offer to the Philippines comes "
                   "with conditions attached, and Manila is weighing it.",
    },
    {
        "kicker": "GLOBAL  •  UNITED NATIONS",
        "color": (29, 78, 216),
        "icon": "globe",
        "headline": "UN chief: agree AI risk rules within a year",
        "summary": "The Secretary-General urged governments to agree global AI "
                   "risk rules within a year.",
    },
]


# -------------------------------------------------------------------- cards

def draw_card(d, box, story, lead=False, compact=False):
    """One news card: kicker, headline, summary, pictogram at right.

    The summary is fitted to the vertical space left in the card, so no
    line ever spills past the card's bottom edge. Compact cards are
    single-line strips with no pictogram.
    """
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=10, fill=(255, 255, 255),
                        outline=(210, 202, 184), width=2)
    pad = 16 if compact else 24
    if compact:
        text_w = (x1 - x0) - 2 * pad
    else:
        icon_s = 150 if lead else 104
        ix = x1 - pad - icon_s
        iy = y0 + (y1 - y0 - icon_s) // 2
        text_w = ix - 14 - (x0 + pad)

    ky = y0 + pad
    kf = font(BOLD, 17 if compact else (20 if lead else 18))
    d.text((x0 + pad, ky), story["kicker"], font=kf, fill=story["color"])
    ky += 26 if compact else (30 if lead else 28)

    hf, hlines = fit(d, story["headline"], BOLD,
                     26 if compact else (40 if lead else 30),
                     text_w, 2)
    for line in hlines:
        d.text((x0 + pad, ky), line, font=hf, fill=INK)
        ky += int(hf.size * 1.18)

    ky += 6
    avail = (y1 - 8) - ky
    max_lines = 1 if compact else 2
    size = 19 if compact else 21
    while size > 12:
        sf = font(REG, size)
        slines = wrap(d, story["summary"], sf, text_w)
        if len(slines) <= max_lines and \
                len(slines) * int(size * 1.28) <= avail:
            break
        size -= 1
    sf = font(REG, size)
    slines = wrap(d, story["summary"], sf, text_w)[:max_lines]
    for line in slines:
        d.text((x0 + pad, ky), line, font=sf, fill=MUTED)
        ky += int(sf.size * 1.28)

    if not compact:
        ICONS[story["icon"]](d, ix, iy, icon_s, story["color"])


def draw_masthead(d):
    """Title, rules and dateline across the top of the page."""
    d.line([40, 30, W - 40, 30], fill=INK, width=4)
    title = "THE WORLD IN ONE DAY"
    tf = font(BOLD, 62)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 44), title, font=tf, fill=INK)
    d.line([40, 128, W - 40, 128], fill=RED, width=3)
    date = "TUESDAY, 24 NOVEMBER 2026  •  SIX STORIES THAT DEFINED THE DAY"
    df = font(BOLD, 23)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 140), date, font=df, fill=MUTED)
    d.line([40, 176, W - 40, 176], fill=INK, width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)

    mx = 40
    cw = W - 2 * mx
    # Lead story, full width.
    draw_card(d, (mx, 192, W - mx, 424), STORIES[0], lead=True)
    # Four stories in a 2x2 grid.
    gy0, gh, gap = 440, 192, 16
    gw = (cw - gap) // 2
    for i, story in enumerate(STORIES[1:5]):
        col, row = i % 2, i // 2
        x0 = mx + col * (gw + gap)
        y0 = gy0 + row * (gh + gap)
        draw_card(d, (x0, y0, x0 + gw, y0 + gh), story)
    # Last story, full width, compact single-line strip.
    draw_card(d, (mx, 848, W - mx, 960), STORIES[5], compact=True)
    # Footer.
    foot = "Sources: Reuters  •  Associated Press  •  Agence France-Presse  •  " \
           "South China Morning Post  —  24 November 2026"
    ff = font(REG, 17)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 972), foot, font=ff, fill=MUTED)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    img.save(OUT, format="PNG")


if __name__ == "__main__":
    main()
