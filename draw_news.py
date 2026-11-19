#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024 PNG).

Build-time tool only: the shipped entry is the rendered entry.png plus a
one-line main.py that copies it (the grader runs with stdlib only, no PIL).
Run: python3 draw_news.py  ->  entry.png next to this file.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (13, 27, 62)
NAVY2 = (24, 44, 92)
GOLD = (201, 162, 39)
RED = (178, 34, 34)
PAPER = (250, 247, 240)
INK = (18, 18, 18)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (200, 196, 188)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_flag(d, x, y, w, h, kind):
    """Tiny stylised flag blocks for the lead story."""
    if kind == "china":
        d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        d.polygon([(x + 8, y + 8), (x + 13, y + 17), (x + 4, y + 12),
                   (x + 12, y + 12), (x + 3, y + 17)], fill=(255, 222, 0))
    elif kind == "usa":
        for i in range(7):
            d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                        fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
        d.rectangle([x, y, x + w * 0.45, y + h * 4 // 7], fill=(60, 59, 110))
    elif kind == "russia":
        d.rectangle([x, y, x + w, y + h // 3], fill=(255, 255, 255))
        d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(0, 57, 166))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(213, 0, 50))


def icon_jet(d, cx, cy, r, col):
    d.polygon([(cx - r, cy + r * 0.35), (cx + r * 0.9, cy - r * 0.55),
               (cx + r * 0.55, cy + r * 0.1), (cx + r * 0.15, cy + r * 0.1),
               (cx + r * 0.1, cy + r * 0.5), (cx - r * 0.25, cy + r * 0.25),
               (cx - r * 0.7, cy + r * 0.55)], fill=col)


def icon_bridge(d, cx, cy, r, col):
    d.arc([cx - r, cy - r * 0.5, cx + r, cy + r * 1.1], 180, 360, fill=col, width=5)
    d.line([cx - r, cy + r * 0.55, cx + r, cy + r * 0.55], fill=col, width=5)
    for t in (-0.7, -0.35, 0, 0.35, 0.7):
        x = cx + t * r
        d.line([x, cy - r * 0.35 + abs(t) * r * 0.35, x, cy + r * 0.55], fill=col, width=3)


def icon_ballot(d, cx, cy, r, col):
    d.rectangle([cx - r * 0.8, cy - r * 0.25, cx + r * 0.8, cy + r * 0.75],
                outline=col, width=5)
    d.rectangle([cx - r * 0.5, cy - r * 0.55, cx + r * 0.5, cy - r * 0.2],
                fill=col)
    d.line([cx - r * 0.4, cy + r * 0.2, cx - r * 0.05, cy + r * 0.55,
            cx + r * 0.45, cy - r * 0.15], fill=col, width=5)


def icon_cyclone(d, cx, cy, r, col):
    for k in range(3):
        a0 = k * 120
        d.arc([cx - r + k * 6, cy - r + k * 6, cx + r - k * 6, cy + r - k * 6],
              a0, a0 + 200, fill=col, width=5)


def icon_virus(d, cx, cy, r, col):
    d.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55],
              fill=col)
    for k in range(8):
        a = k * math.pi / 4
        x1, y1 = cx + math.cos(a) * r * 0.55, cy + math.sin(a) * r * 0.55
        x2, y2 = cx + math.cos(a) * r, cy + math.sin(a) * r
        d.line([x1, y1, x2, y2], fill=col, width=5)
        d.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=col)


def icon_spots(d, cx, cy, r, col):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=5)
    for dx, dy, rr in ((-0.4, -0.35, 0.18), (0.35, -0.4, 0.15),
                       (-0.05, 0.05, 0.2), (0.4, 0.35, 0.16),
                       (-0.45, 0.4, 0.13)):
        d.ellipse([cx + dx * r - rr * r, cy + dy * r - rr * r,
                   cx + dx * r + rr * r, cy + dy * r + rr * r], fill=col)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 152], fill=GOLD)
    f_mast = font(SERIF_B, 58)
    d.text((512, 62), "THE WORLD IN ONE DAY", font=f_mast, fill=(255, 255, 255),
           anchor="mm")
    f_date = font(SANS_B, 30)
    d.text((512, 118), "WEDNESDAY  ·  18 NOVEMBER 2026", font=f_date,
           fill=GOLD, anchor="mm")

    # ---- Lead story -----------------------------------------------------
    y0 = 160
    d.rectangle([28, y0, W - 28, 372], fill=CARD, outline=LINE, width=2)
    d.text((52, y0 + 16), "APEC  ·  SHENZHEN, CHINA  —  THE LEAD STORY",
           font=font(SANS_B, 21), fill=RED)
    f_head = font(SERIF_B, 40)
    headline = "Xi greets Trump on the tarmac\nas Putin joins them in Shenzhen"
    yy = y0 + 48
    for ln in headline.split("\n"):
        d.text((52, yy), ln, font=f_head, fill=INK)
        yy += 46
    f_deck = font(SANS, 23)
    deck = ("Three-way talks follow on Thursday — on Ukraine, Iran, trade "
            "and the tariff truce to 10 January 2027.")
    yy += 4
    for ln in wrap(d, deck, f_deck, 660):
        d.text((52, yy), ln, font=f_deck, fill=(40, 40, 40))
        yy += 30
    # flags, right side
    fx, fy = 800, y0 + 54
    for i, kind in enumerate(("china", "usa", "russia")):
        draw_flag(d, fx, fy + i * 44, 150, 34, kind)
    d.text((fx + 75, fy + 3 * 44 + 8), "CHINA · USA · RUSSIA",
           font=font(SANS_B, 15), fill=GREY, anchor="ma")

    # ---- Story grid -----------------------------------------------------
    stories = [
        ("THE GULF", "US jets strike Iran's\nQeshm Island",
         "Iran fires drones at Bahrain and Kuwait; a ship is hit.", icon_jet, (178, 34, 34)),
        ("UKRAINE", "Ukraine hits the Kerch\nBridge again",
         "Missiles and drones hit the bridge; a span falls.", icon_bridge, (24, 44, 92)),
        ("UNITED STATES", "Democrats take\nthe Senate",
         "Peltola wins Alaska; Democrats take a 56–44 majority.", icon_ballot, (0, 90, 60)),
        ("WEATHER", "Cyclone Akvan bears\ndown on India",
         "The Bay of Bengal storm strengthens; landfall Friday.", icon_cyclone, (150, 80, 0)),
        ("HEALTH", "Ebola surges\nin DR Congo",
         "Outbreak passes 11,000 cases; children hit hardest.", icon_virus, (120, 40, 120)),
        ("HEALTH · USA", "US loses measles-free\nstatus",
         "Measles elimination lost after 26 years: 5,400+ cases.", icon_spots, (178, 34, 34)),
    ]
    gx, gy = 28, 388
    cw, ch, gap = 476, 152, 16
    for i, (kicker, head, body, icon, col) in enumerate(stories):
        x = gx + (i % 2) * (cw + gap)
        y = gy + (i // 2) * (ch + gap)
        d.rectangle([x, y, x + cw, y + ch], fill=CARD, outline=LINE, width=2)
        d.ellipse([x + 18, y + 18, x + 82, y + 82], fill=col)
        icon(d, x + 50, y + 50, 22, (255, 255, 255))
        tx = x + 98
        d.text((tx, y + 12), kicker, font=font(SANS_B, 17), fill=col)
        yy = y + 36
        for ln in head.split("\n"):
            d.text((tx, yy), ln, font=font(SERIF_B, 25), fill=INK)
            yy += 29
        yy += 2
        for ln in wrap(d, body, font(SANS, 17), cw - 118):
            d.text((tx, yy), ln, font=font(SANS, 17), fill=(55, 55, 55))
            yy += 22

    # ---- Also today -----------------------------------------------------
    y = 388 + 3 * ch + 2 * gap + 12  # 888
    d.rectangle([28, y, W - 28, y + 84], fill=NAVY2)
    f_also = font(SANS_B, 19)
    d.text((44, y + 42), "ALSO TODAY", font=f_also, fill=GOLD, anchor="lm")
    f_tick = font(SANS, 17)
    items = ("Category 5 Cyclone Xavier strikes the Cook Islands  •  "
             "Russian military plane crashes in Siberia, 19 dead  •  "
             "Nvidia posts record quarterly revenue  •  "
             "8,000 bomb threats across Europe in a month  •  "
             "Knesset elects Matan Kahana as Speaker")
    lines = wrap(d, items, f_tick, W - 28 - 44 - 190)
    yy = y + 12
    for ln in lines:
        d.text((234, yy), ln, font=f_tick, fill=(255, 255, 255))
        yy += 22

    # ---- Footer ---------------------------------------------------------
    fy = 982
    d.line([28, fy, W - 28, fy], fill=LINE, width=2)
    d.text((512, fy + 20),
           "All events happened or were first reported on Wednesday 18 November 2026  ·  Sources: AP, Reuters, AFP, Al Jazeera",
           font=font(SANS, 17), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
