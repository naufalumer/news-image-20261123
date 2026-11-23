#!/usr/bin/env python3
"""Render the news-image-20261123 entry: a Monday-edition broadsheet.

Layout (1024x1024, PIL only, DejaVu fonts):
  burgundy masthead -> Nepal-India lead panel with schematic map ->
  TODAY (Mon 23 Nov) briefs -> SUNDAY'S AFTERMATH (22 Nov, dated) ->
  numbers strip -> sources footer.
Every story in NEWS_FACTS.md; Sunday stories are never shown as today's.
Run: python3 render.py [out.png]
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 26  # page margin

PAPER = (246, 239, 224)
CARD = (255, 252, 244)
INK = (30, 26, 23)
BURG = (94, 26, 36)
BURG_LT = (122, 42, 54)
GOLD = (185, 138, 47)
GREEN = (31, 77, 58)
SLATE = (59, 74, 90)
MUTED = (110, 100, 88)
RULE = (200, 185, 160)
SAFFRON = (255, 153, 51)
LEAF = (19, 136, 8)
NAVY = (6, 60, 140)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, color, width, leading):
    lines = wrap(draw, text, fnt, width)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def chip(draw, x, y, text, fnt, bg, fg):
    w = int(draw.textlength(text, font=fnt)) + 14
    h = fnt.size + 10
    draw.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=bg)
    draw.text((x + 7, y + 5), text, font=fnt, fill=fg)
    return w


# ---- small drawn glyphs (30x30 box, drawn with primitives only) ----

def glyph_flame(d, x, y, c):
    d.polygon([(x + 15, y + 2), (x + 24, y + 14), (x + 20, y + 24),
               (x + 10, y + 24), (x + 6, y + 14)], fill=c)
    d.ellipse([x + 11, y + 15, x + 19, y + 26], fill=(255, 200, 60))


def glyph_ship(d, x, y, c):
    d.polygon([(x + 2, y + 18), (x + 28, y + 18), (x + 24, y + 26),
               (x + 6, y + 26)], fill=c)
    d.rectangle([x + 14, y + 4, x + 16, y + 18], fill=c)
    d.polygon([(x + 16, y + 5), (x + 26, y + 16), (x + 16, y + 16)], fill=(200, 60, 50))


def glyph_globe(d, x, y, c):
    d.ellipse([x + 2, y + 2, x + 28, y + 28], outline=c, width=2)
    d.ellipse([x + 8, y + 6, x + 16, y + 13], fill=c)
    d.ellipse([x + 16, y + 15, x + 24, y + 22], fill=c)
    d.arc([x + 2, y + 2, x + 28, y + 28], 200, 340, fill=c, width=2)


def glyph_bat(d, x, y, c):
    d.line([x + 8, y + 26, x + 20, y + 6], fill=c, width=5)
    d.ellipse([x + 19, y + 2, x + 27, y + 10], fill=(180, 40, 40))


def glyph_film(d, x, y, c):
    d.rectangle([x + 3, y + 6, x + 27, y + 24], outline=c, width=2)
    for xx in (7, 13, 19, 25):
        d.rectangle([x + xx, y + 9, x + xx + 2, y + 12], fill=c)
        d.rectangle([x + xx, y + 18, x + xx + 2, y + 21], fill=c)


def glyph_chip(d, x, y, c):
    d.rectangle([x + 8, y + 8, x + 22, y + 22], outline=c, width=2)
    d.rectangle([x + 12, y + 12, x + 18, y + 18], fill=c)
    for xx in (11, 15, 19):
        d.line([x + xx, y + 3, x + xx, y + 8], fill=c, width=2)
        d.line([x + xx, y + 22, x + xx, y + 27], fill=c, width=2)


def glyph_dome(d, x, y, c):
    d.pieslice([x + 6, y + 8, x + 24, y + 26], 180, 360, fill=c)
    d.rectangle([x + 4, y + 22, x + 26, y + 27], fill=c)
    d.line([x + 15, y + 2, x + 15, y + 9], fill=c, width=2)


def glyph_building(d, x, y, c):
    d.rectangle([x + 5, y + 8, x + 25, y + 27], outline=c, width=2)
    d.line([x + 5, y + 8, x + 15, y + 2, x + 25, y + 8], fill=c, width=2)
    for xx in (9, 14, 19):
        d.line([x + xx, y + 12, x + xx, y + 24], fill=c, width=2)


def glyph_doc(d, x, y, c):
    d.rectangle([x + 7, y + 3, x + 23, y + 27], outline=c, width=2)
    d.line([x + 10, y + 9, x + 20, y + 9], fill=c, width=2)
    d.line([x + 10, y + 14, x + 20, y + 14], fill=c, width=2)
    d.line([x + 10, y + 19, x + 16, y + 19], fill=c, width=2)


def glyph_cap(d, x, y, c):
    d.polygon([(x + 15, y + 5), (x + 28, y + 12), (x + 15, y + 19),
               (x + 2, y + 12)], fill=c)
    d.rectangle([x + 10, y + 16, x + 20, y + 24], fill=c)
    d.line([x + 26, y + 13, x + 26, y + 22], fill=c, width=2)


def glyph_warn(d, x, y, c):
    d.polygon([(x + 15, y + 3), (x + 28, y + 26), (x + 2, y + 26)],
              outline=c, width=2)
    d.line([x + 15, y + 11, x + 15, y + 19], fill=c, width=3)
    d.ellipse([x + 13, y + 21, x + 17, y + 25], fill=c)


def glyph_ribbon(d, x, y, c):
    d.rectangle([x + 4, y + 4, x + 26, y + 26], fill=(20, 20, 20))
    d.line([x + 4, y + 4, x + 26, y + 26], fill=(240, 240, 240), width=2)


def glyph_crack(d, x, y, c):
    d.rectangle([x + 5, y + 5, x + 25, y + 25], outline=c, width=2)
    d.line([x + 8, y + 5, x + 13, y + 12, x + 10, y + 18, x + 16, y + 25],
           fill=c, width=2)


def glyph_star_flag(d, x, y, c):
    d.rectangle([x + 3, y + 6, x + 27, y + 24], outline=c, width=2)
    d.polygon([(x + 15, y + 8), (x + 17, y + 14), (x + 23, y + 14),
               (x + 18, y + 18), (x + 20, y + 23), (x + 15, y + 20),
               (x + 10, y + 23), (x + 12, y + 18), (x + 7, y + 14),
               (x + 13, y + 14)], fill=c)


GLYPHS = {
    "flame": glyph_flame, "ship": glyph_ship, "globe": glyph_globe,
    "bat": glyph_bat, "film": glyph_film, "chip": glyph_chip,
    "dome": glyph_dome, "building": glyph_building, "doc": glyph_doc,
    "cap": glyph_cap, "warn": glyph_warn, "ribbon": glyph_ribbon,
    "crack": glyph_crack, "star": glyph_star_flag,
}


def card(d, x, y, w, h, glyph, accent, head, deck, head_size=16, deck_size=12):
    d.rounded_rectangle([x, y, x + w, y + h], radius=6, fill=CARD,
                        outline=RULE, width=1)
    d.rectangle([x, y, x + 5, y + h], fill=accent)
    gx, gy = x + 12, y + (h - 30) // 2
    GLYPHS[glyph](d, gx, gy, accent)
    tx = x + 48
    tw = w - 48 - 10
    hf = SANS_B(head_size)
    df = SANS(deck_size)
    hy = y + 7
    lines = wrap(d, head, hf, tw)
    for ln in lines[:2]:
        d.text((tx, hy), ln, font=hf, fill=INK)
        hy += head_size + 4
    para(d, tx, hy, deck, df, (74, 66, 58), tw, deck_size + 4)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 124], fill=BURG)
    d.text((M, 14), "THE WORLD IN ONE DAY", font=SERIF_B(56), fill=(250, 244, 230))
    d.text((M, 88), "MONDAY, 23 NOVEMBER 2026",
           font=SANS_B(21), fill=(232, 196, 120))
    right = "16 STORIES  ·  6 REGIONS  ·  MONDAY EDITION"
    rw = d.textlength(right, font=SANS_B(15))
    d.text((W - M - rw, 92), right, font=SANS_B(15), fill=(232, 196, 120))
    d.rectangle([0, 124, W, 130], fill=GOLD)

    # ---------- lead: Nepal-India talks ----------
    ly, lh = 138, 152
    d.rounded_rectangle([M, ly, W - M, ly + lh], radius=8, fill=CARD,
                        outline=BURG, width=2)
    d.rectangle([M, ly, M + 6, ly + lh], fill=BURG)
    chip(d, M + 18, ly + 12, "LEAD  —  DELHI, TODAY", SANS_B(13), BURG, (250, 244, 230))
    d.text((M + 18, ly + 44), "NEPAL AND INDIA TALK TRADE,",
           font=SERIF_B(27), fill=INK)
    d.text((M + 18, ly + 76), "POWER AND FLOOD RELIEF",
           font=SERIF_B(27), fill=INK)
    para(d, M + 18, ly + 110,
         "PM Balendra Shah meets PM Modi in Delhi on his first bilateral "
         "visit since March: a 34-member delegation, MoUs on energy and "
         "health, and a joint vision.",
         SANS(13), (74, 66, 58), 600, 17)

    # schematic map, right of the lead
    mx0, my0 = 690, ly + 12
    d.rectangle([mx0, my0, mx0 + 282, my0 + 96], outline=RULE, width=1)
    d.text((mx0 + 8, my0 + 4), "SCHEMATIC MAP — NOT TO SCALE",
           font=SANS(9), fill=MUTED)
    # India: rough peninsula polygon
    india = [(mx0 + 60, my0 + 30), (mx0 + 130, my0 + 26), (mx0 + 175, my0 + 38),
             (mx0 + 210, my0 + 46), (mx0 + 190, my0 + 66), (mx0 + 165, my0 + 86),
             (mx0 + 140, my0 + 92), (mx0 + 120, my0 + 72), (mx0 + 82, my0 + 66),
             (mx0 + 55, my0 + 50)]
    d.polygon(india, fill=(255, 232, 200), outline=(150, 110, 60))
    # Nepal: strip above India's north edge
    nepal = [(mx0 + 105, my0 + 18), (mx0 + 195, my0 + 20), (mx0 + 190, my0 + 26),
             (mx0 + 108, my0 + 25)]
    d.polygon(nepal, fill=(200, 40, 60), outline=(40, 60, 140))
    # Delhi star
    sx, sy = mx0 + 118, my0 + 46
    d.polygon([(sx, sy - 8), (sx + 2, sy - 2), (sx + 8, sy), (sx + 2, sy + 2),
               (sx, sy + 8), (sx - 2, sy + 2), (sx - 8, sy), (sx - 2, sy - 2)],
              fill=BURG)
    d.text((sx + 12, sy - 7), "DELHI", font=SANS_B(11), fill=INK)
    d.text((mx0 + 198, my0 + 14), "NEPAL", font=SANS_B(10), fill=(40, 60, 140))
    d.text((mx0 + 150, my0 + 76), "INDIA", font=SANS_B(11), fill=(150, 110, 60))
    # flag chips under the map frame, inside the lead panel
    fx, fy = mx0, my0 + 102
    # India tricolour
    d.rectangle([fx, fy + 4, fx + 34, fy + 10], fill=SAFFRON)
    d.rectangle([fx, fy + 10, fx + 34, fy + 16], fill=(255, 255, 255), outline=(180, 180, 180))
    d.rectangle([fx, fy + 16, fx + 34, fy + 22], fill=LEAF)
    d.ellipse([fx + 14, fy + 11, fx + 20, fy + 15], outline=NAVY)
    d.text((fx + 40, fy + 6), "INDIA", font=SANS_B(11), fill=INK)
    # Nepal pennon
    d.polygon([(fx + 130, fy + 22), (fx + 130, fy + 4), (fx + 152, fy + 12),
               (fx + 130, fy + 12), (fx + 146, fy + 18)], fill=(200, 40, 60),
              outline=(40, 60, 140))
    d.text((fx + 158, fy + 6), "NEPAL", font=SANS_B(11), fill=INK)

    # ---------- section header helper ----------
    def section(y, text, bg):
        d.rectangle([M, y, W - M, y + 28], fill=bg)
        d.text((M + 12, y + 5), text, font=SANS_B(15), fill=(250, 244, 230))
        return y + 28

    # ---------- TODAY cards ----------
    y = section(298, "TODAY  —  MONDAY 23 NOVEMBER 2026", GREEN)
    y += 8
    cw, ch, gap = 472, 66, 8
    today = [
        ("bat", GREEN, "WELLINGTON, FINAL DAY",
         "NZ resume 119/2, trailing by 233. India declared a record 720/9 "
         "on Sunday; the hosts must bat out the day to save the Test."),
        ("flame", (178, 60, 40), "INDONESIA: FACTORY SEARCH RESUMES",
         "Rescue crews return at 7am to the Serang candy factory. 24 body "
         "bags found; about 50 still missing after Saturday's fire."),
        ("building", GREEN, "SHAH'S Rs 4,000 CRORE PUSH",
         "Home Minister Amit Shah launches an infrastructure package in "
         "Arunachal Pradesh, stressing self-reliance and cooperation."),
        ("ribbon", (60, 60, 60), "RAJYA SABHA MP DIES IN DELHI",
         "BJP Rajya Sabha MP Ramrao Wadkute dies of a cardiac arrest in "
         "the capital."),
        ("film", (120, 70, 130), "IFFI HOSTS BRICS FILM TABLE",
         "Goa's film festival gathers BRICS partners for a roundtable on "
         "stronger film-industry ties."),
        ("chip", (40, 90, 140), "NVIDIA ROW: NEW CHIP DETAILS",
         "Fresh details tie Alice Huang to a secret network said to divert "
         "AI chips to China."),
        ("warn", (178, 60, 40), "NINE PILGRIMS KILLED IN KOTA",
         "A vehicle carrying pilgrims rams a truck in Rajasthan's Kota; "
         "several more are injured."),
        ("cap", GREEN, "HYDERABAD STUDENTS PROTEST ON",
         "University of Hyderabad students keep up their protest, seeking "
         "a faculty member's removal over alleged casteist remarks."),
    ]
    for i, (gl, ac, hd, dk) in enumerate(today):
        cx = M + (i % 2) * (cw + gap)
        cy = y + (i // 2) * (ch + gap)
        card(d, cx, cy, cw, ch, gl, ac, hd, dk)

    # ---------- AFTERMATH cards ----------
    y = 298 + 28 + 8 + 4 * ch + 3 * gap  # 618
    y = section(y + 8, "SUNDAY'S AFTERMATH  —  22 NOVEMBER 2026", SLATE)
    y += 8
    # COP31 full-width card
    d.rounded_rectangle([M, y, W - M, y + 70], radius=6, fill=CARD,
                        outline=RULE, width=1)
    d.rectangle([M, y, M + 5, y + 70], fill=SLATE)
    glyph_globe(d, M + 14, y + 20, SLATE)
    para(d, M + 52, y + 7,
         "COP31 COLLAPSES IN ANTALYA — NO DEAL",
         SANS_B(17), INK, W - 2 * M - 62, 21)
    para(d, M + 52, y + 30,
         "The first COP to fail since Copenhagen 2009, after 44+ hours of "
         "overtime. The final draft never named fossil fuels; the EU, backed "
         "by about 130 countries, refused it. Guterres: 'deeply "
         "disappointed'. COP32 goes to Addis Ababa in Nov 2027.",
         SANS(12), (74, 66, 58), W - 2 * M - 62, 16)
    y += 70 + gap
    after = [
        ("ship", SLATE, "RUSSIAN WARSHIP SUNK OFF LIBYA",
         "Corvette Merkury capsizes at Benghazi after a suspected "
         "Ukrainian sea-drone strike; 10 lightly hurt."),
        ("ship", SLATE, "SPARTA II TOWED OUT OF FINLAND",
         "The Russian cargo ship, hit by drones in the Baltic on "
         "Saturday, is towed out of Finnish waters on Sunday night."),
        ("crack", SLATE, "KYIV FLAT HIT, 14 MISSING",
         "A Russian drone strikes a five-storey block in the Kyiv region; "
         "part collapses. Nine are evacuated, two hurt."),
        ("dome", SLATE, "GULF: MISSILE DOWN, BAHRAIN HIT",
         "Saudi defences stop a Houthi missile aimed west early Sunday; "
         "an Iranian attack sets a Bahrain site ablaze."),
        ("doc", SLATE, "SEOUL MINISTER QUITS OVER AI EXAMS",
         "Education chief Choi Kyo-jin resigns after anti-cheating chaos "
         "at the CSAT; 111 device cases were caught."),
        ("star", SLATE, "MYANMAR CALLS ASEAN MOVE UNFAIR",
         "The army-backed government denounces its continued exclusion "
         "from ASEAN summits (statement, Sat 21 Nov)."),
    ]
    ah = 56
    for i, (gl, ac, hd, dk) in enumerate(after):
        cx = M + (i % 2) * (cw + gap)
        cy = y + (i // 2) * (ah + gap)
        card(d, cx, cy, cw, ah, gl, ac, hd, dk, head_size=15, deck_size=12)
    y = y + 3 * ah + 2 * gap  # 922

    # ---------- numbers strip ----------
    ny = y + 8
    d.rectangle([M, ny, W - M, ny + 46], fill=BURG)
    nums = [("34", "NEPAL DELEGATES"), ("720/9", "INDIA'S RECORD"),
            ("233", "NZ TRAIL BY"), ("24", "BODY BAGS, SERANG"),
            ("130", "BACK EU AT COP31"), ("44h", "COP31 OVERTIME")]
    seg = (W - 2 * M) // 6
    for i, (n, lab) in enumerate(nums):
        cx = M + i * seg
        d.text((cx + 12, ny + 5), n, font=SANS_B(17), fill=(250, 244, 230))
        d.text((cx + 12, ny + 26), lab, font=SANS_B(9), fill=(232, 196, 120))
        if i:
            d.line([cx, ny + 6, cx, ny + 40], fill=(150, 100, 100), width=1)

    # ---------- footer ----------
    fy = ny + 46 + 8
    d.line([M, fy, W - M, fy], fill=RULE, width=1)
    para(d, M, fy + 6,
         "Sources: MEA / News On AIR, ESPNcricinfo, Reuters, UN News, AP, "
         "Korea JoongAng Daily. Counts as reported by 00:30 UTC, 23 Nov 2026. "
         "Map schematic; flags drawn. Stories are dated in the image.",
         SANS(10), MUTED, W - 2 * M, 14)

    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img.save(out, optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    render()
