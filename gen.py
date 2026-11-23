#!/usr/bin/env python3
"""Generate the front page for news-image-20261123.

One-page newspaper front page summing up world news of Monday,
23 November 2026. Stories verified 2026-11-23 against Reuters, CNN
and Associated Press reporting:

  LEAD   COP31 climate summit in Antalya collapses with no deal
         (CNN / Reuters / WSJ).
  SECOND Ukraine sinks Russian corvette Merkury off Libya with
         seven sea drones (Reuters / CNN / AP).
  THIRD  24 dead, ~30 missing in candy factory fire, Cikande,
         Banten, Indonesia (Reuters).
  FOURTH Democrats win at least 258 US House seats, largest
         majority since 1992 (AP / Reuters).

Run:  python3 gen.py   -> writes entry.png (1024x1024) next to this file.
"""

import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 38
CONTENT = W - 2 * MARGIN

PAPER = (247, 243, 234)
INK = (18, 18, 18)
GREY = (90, 86, 78)
RED = (176, 32, 28)
NAVY = (16, 34, 64)
TEAL = (14, 74, 78)
GOLD = (214, 164, 60)

FONTS = "/usr/share/fonts/truetype"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


F_MAST = font("noto/NotoSerifDisplay-Black.ttf", 80)
F_HEAD = font("noto/NotoSerif-Bold.ttf", 46)
F_SUBHEAD = font("noto/NotoSerif-Bold.ttf", 28)
F_DECK = font("noto/NotoSerif-Italic.ttf", 24)
F_BODY = font("noto/NotoSerif-Regular.ttf", 20)
F_KICK = font("noto/NotoSans-Bold.ttf", 20)
F_SMALL = font("noto/NotoSans-Regular.ttf", 18)
F_TINY = font("noto/NotoSans-Regular.ttf", 15)
F_BANNER = font("noto/NotoSans-Bold.ttf", 25)
F_STAMP = font("noto/NotoSans-Black.ttf", 44)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, y, weight=2, color=INK, x0=None, x1=None):
    draw.line([(x0 or MARGIN, y), (x1 or W - MARGIN, y)], fill=color, width=weight)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top dateline bar ----
    d.text((MARGIN, 22), "MONDAY, 23 NOVEMBER 2026", font=F_SMALL, fill=INK)
    right = "WORLD EDITION"
    d.text((W - MARGIN - d.textlength(right, font=F_SMALL), 22),
           right, font=F_SMALL, fill=INK)
    rule(d, 52, weight=2)

    # ---- masthead ----
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, 54), title, font=F_MAST, fill=INK)
    rule(d, 150, weight=5)
    rule(d, 158, weight=1)

    # ---- lead kicker + headline ----
    y = 172
    d.text((MARGIN, y), "CLIMATE  |  ANTALYA, TURKEY", font=F_KICK, fill=RED)
    y += 26
    head = "COP31 COLLAPSES: NO DEAL AS NATIONS SPLIT OVER FOSSIL FUELS"
    y = draw_lines(d, wrap(d, head, F_HEAD, CONTENT), MARGIN, y,
                   F_HEAD, INK, 52) + 4

    deck = ("The longest climate summit in history ends without an agreement — "
            "the first major breakdown since Copenhagen in 2009.")
    y = draw_lines(d, wrap(d, deck, F_DECK, CONTENT), MARGIN, y,
                   F_DECK, GREY, 30) + 8

    # ---- lead illustration: cracked globe over a dark summit hall ----
    px0, py0, px1, py1 = MARGIN, y, W - MARGIN, y + 150
    d.rectangle([px0, py0, px1, py1], fill=NAVY)
    # hall floor line + flags row
    d.rectangle([px0, py1 - 34, px1, py1], fill=(10, 22, 44))
    for i, c in enumerate([(200, 60, 50), (60, 140, 200), (220, 180, 60),
                           (70, 170, 90), (200, 120, 40), (150, 90, 180)]):
        fx = px0 + 30 + i * 34
        d.line([(fx, py1 - 88), (fx, py1 - 34)], fill=(200, 200, 200), width=2)
        d.rectangle([fx, py1 - 88, fx + 22, py1 - 72], fill=c)
    # globe
    cx, cy, r = px0 + 640, py0 + 75, 56
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 130, 160),
              outline=(230, 230, 230), width=3)
    d.ellipse([cx - 30, cy - 34, cx + 6, cy + 2], fill=(96, 176, 110))
    d.ellipse([cx + 2, cy + 8, cx + 38, cy + 40], fill=(96, 176, 110))
    d.ellipse([cx - 44, cy + 16, cx - 12, cy + 44], fill=(96, 176, 110))
    # crack across the globe
    d.line([(cx - 40, cy - 52), (cx - 8, cy - 18), (cx - 22, cy + 6),
            (cx + 14, cy + 30), (cx + 6, cy + 56)],
           fill=(240, 240, 240), width=4)
    # "NO DEAL" stamp
    stamp = "NO DEAL"
    sw = d.textlength(stamp, font=F_STAMP)
    sx, sy = px0 + 300, py0 + 48
    d.rectangle([sx - 14, sy - 8, sx + sw + 14, sy + 52],
                outline=RED, width=4)
    d.text((sx, sy), stamp, font=F_STAMP, fill=(224, 80, 70))
    # caption inside panel
    d.text((px0 + 30, py1 - 28),
           "Nearly 200 nations walk away with no pact after two weeks of talks.",
           font=F_SMALL, fill=(220, 220, 220))
    y = py1 + 12

    # ---- lead body, two short columns ----
    lead_body = ("After more than two weeks of talks in Antalya, Turkey, the "
                 "COP31 climate conference collapsed on Sunday when the EU and "
                 "more than 100 nations refused a final text with no mention "
                 "of fossil fuels. Oil-producing states blocked the language; "
                 "the summit ran a record two days into overtime before its "
                 "president conceded there was no consensus.")
    col_w = (CONTENT - 24) // 2
    lines = wrap(d, lead_body, F_BODY, col_w)
    half = (len(lines) + 1) // 2
    draw_lines(d, lines[:half], MARGIN, y, F_BODY, INK, 26)
    draw_lines(d, lines[half:], MARGIN + col_w + 24, y, F_BODY, INK, 26)
    y += max(len(lines[:half]), len(lines[half:])) * 26 + 6
    rule(d, y, weight=1)
    y += 12

    # ---- secondary stories, two columns ----
    col_w = (CONTENT - 24) // 2
    x2 = MARGIN + col_w + 24

    d.text((MARGIN, y), "WAR IN UKRAINE  |  LIBYA", font=F_KICK, fill=RED)
    d.text((x2, y), "INDONESIA  |  BANTEN", font=F_KICK, fill=RED)
    y += 26

    h1 = "Ukrainian sea drones sink Russian warship off Libya"
    h2 = "24 dead in candy factory fire; dozens still missing"
    l1 = wrap(d, h1, F_SUBHEAD, col_w)
    l2 = wrap(d, h2, F_SUBHEAD, col_w)
    n = max(len(l1), len(l2))
    draw_lines(d, l1, MARGIN, y, F_SUBHEAD, INK, 33)
    draw_lines(d, l2, x2, y, F_SUBHEAD, INK, 33)
    y += n * 33 + 4

    b1 = ("Kyiv says seven Ukrainian-made naval drones sank the corvette "
          "Merkury, one of Russia's newest warships, at the Benghazi naval "
          "base on Sunday — 2,400 km from the front line. A Ka-27 helicopter "
          "aboard was destroyed; the cargo ship MV Angara was also hit.")
    b2 = ("A fire at the PT Fonusa Agung Mulia confectionery factory in "
          "Cikande, Serang Regency, killed at least 24 people on Saturday. "
          "About 30 workers are still missing as rescuers search the burned "
          "wreckage.")
    bl1 = wrap(d, b1, F_BODY, col_w)
    bl2 = wrap(d, b2, F_BODY, col_w)
    draw_lines(d, bl1, MARGIN, y, F_BODY, INK, 25)
    draw_lines(d, bl2, x2, y, F_BODY, INK, 25)
    y += max(len(bl1), len(bl2)) * 25 + 10

    # ---- bottom banner: US midterms ----
    by0, by1 = y, y + 56
    d.rectangle([MARGIN, by0, W - MARGIN, by1], fill=NAVY)
    banner = "U.S. MIDTERMS: Democrats win 258 House seats — largest majority since 1992"
    bsize = 25
    while True:
        bf = font("noto/NotoSans-Bold.ttf", bsize)
        bw = d.textlength(banner, font=bf)
        if bw <= CONTENT - 16 or bsize <= 14:
            break
        bsize -= 1
    d.text(((W - bw) / 2, by0 + 15), banner, font=bf, fill=(255, 255, 255))
    y = by1 + 8

    # ---- footer ----
    rule(d, y, weight=1)
    foot = ("Sources: Reuters · CNN · Associated Press  |  The World Today — "
            "one page, one day: Monday, 23 November 2026")
    fw = d.textlength(foot, font=F_TINY)
    d.text(((W - fw) / 2, y + 6), foot, font=F_TINY, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG")
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
