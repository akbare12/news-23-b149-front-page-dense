#!/usr/bin/env python3
"""news-23 b149 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026 (31 stories)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (163, 18, 18)
DARKRED = (120, 10, 10)
NAVY = (16, 42, 90)
GOLD = (176, 141, 42)
GREY = (90, 90, 90)
LIGHT = (232, 226, 210)
GREEN = (28, 84, 48)
TEAL = (18, 90, 96)
PURPLE = (88, 52, 110)
MAPGREEN = (196, 222, 178)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(d, text, fnt, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(d, text, maxw, start, fname, minsize=8):
    s = start
    while s > minsize:
        f = fname(s)
        if d.textlength(text, font=f) <= maxw:
            return f
        s -= 1
    return fname(minsize)


def chip(d, x, y, label, color):
    f = SANS_B(8)
    w = int(d.textlength(label, font=f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=2, fill=color)
    d.text((x + 5, y + 2), label, font=f, fill=(255, 255, 255))
    return w


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 10
CW = 1004  # usable width 10..1014

# ---------- masthead ----------
d.text((MX, 2), "THE WORLD TODAY", font=SERIF_B(50), fill=INK)
df = SANS_B(15)
d.text((1014 - d.textlength("MONDAY 23 NOVEMBER 2026", font=df), 20),
       "MONDAY 23 NOVEMBER 2026", font=df, fill=GOLD)
d.rectangle([MX, 56, 1014, 58], fill=GOLD)

# ---------- kicker ----------
d.rectangle([MX, 60, 1014, 82], fill=RED)
kf = SANS_B(13)
kick = "AI rout hits Asia   \u00b7   UN chief urges AI rules   \u00b7   US lead over China at record low   \u00b7   Anthropic IPO $107.3B"
d.text((MX + 6, 65), kick, font=kf, fill=(255, 255, 255))

# ---------- number strip (2 rows x 5) ----------
nums = [
    ("-3.3%", "KOSPI"),
    ("5.3", "US-CHINA POWER GAP"),
    ("11,762", "EBOLA CASES, DRC"),
    ("10T won", "SEOUL STABILISATION FUND"),
    ("2%", "BILLIONAIRE TAX IN PARIS"),
    ("$450M", "SKUBAL DEAL"),
    ("165", "RUSSIAN MISSILES/WEEK"),
    ("12,000", "CLEARED IN MANCHESTER"),
    ("264 kg", "EXPLOSIVES SEIZED"),
    ("$107.3B", "ANTHROPIC IPO"),
]
cellw = CW // 5
for i, (val, lab) in enumerate(nums):
    row, col = divmod(i, 5)
    x = MX + col * cellw
    y = 86 + row * 32
    d.text((x + 4, y), val, font=SANS_B(19), fill=INK)
    d.text((x + 4, y + 20), lab, font=SANS_B(8), fill=GREY)
d.line([MX, 150, 1014, 150], fill=(200, 190, 170), width=1)

# ---------- region bar ----------
regions = [
    ("ASIA-PACIFIC 7", 227, NAVY),
    ("AMERICAS 8", 259, RED),
    ("MIDDLE EAST 6", 194, TEAL),
    ("EUROPE 5", 162, PURPLE),
    ("AFRICA 3", 97, (150, 110, 30)),
    ("WORLD 2", 65, GOLD),
]
x = MX
rf = SANS_B(10)
for label, w, col in regions:
    d.rectangle([x, 152, x + w, 168], fill=col)
    tw = d.textlength(label, font=rf)
    d.text((x + (w - tw) / 2, 155), label, font=rf, fill=(255, 255, 255))
    x += w

# ---------- UTC strip ----------
d.text((MX, 172), "THE DAY IN UTC", font=SANS_B(9), fill=INK)
utc = "~00:00 Kospi dives  \u00b7  ~05:30 Guterres opens  \u00b7  ~09:00 Power Index  \u00b7  ~12:00 Paris 2% tax  \u00b7  ~15:00 Kyiv missiles"
d.text((MX + 92, 172), utc, font=SANS(9), fill=GREY)
d.text((1014 - d.textlength("~ APPROX", font=SANS(9)), 172), "~ APPROX", font=SANS(9), fill=GREY)

# ---------- heroes ----------
HX = [MX, 347, 684]
HW = 330
HY = 184
SCENE_H = 112


def scene_kospi(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 26, 60))
    # buildings along the bottom, max height 44 so the big -3.3% stays clear
    import random
    rnd = random.Random(23)
    bx = x + 6
    while bx < x + w - 14:
        bw = rnd.randint(16, 26)
        bh = rnd.randint(22, 44)
        d.rectangle([bx, y + h - 16 - bh, bx + bw, y + h - 16], fill=(24, 48, 96))
        for wy in range(y + h - 14 - bh, y + h - 18, 7):
            for wx in range(bx + 3, bx + bw - 3, 6):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 4
    # falling chart line, kept clear of the big number (starts right of it)
    pts = [(x + 185, y + 26), (x + 205, y + 38), (x + 228, y + 34),
           (x + 252, y + 54), (x + 278, y + 50), (x + 302, y + 72),
           (x + 322, y + 88)]
    d.line(pts, fill=(255, 140, 40), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 255, 255))
    d.text((x + 8, y + 6), "-3.3%", font=SANS_B(42), fill=(255, 255, 255))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(0, 0, 0))
    d.text((x + 6, y + h - 14),
           "KOSPI 4,708.54  \u00b7  -161 PTS  \u00b7  SAMSUNG -3.1%  \u00b7  HYNIX -2.5%",
           font=SANS_B(9), fill=(255, 255, 255))


def scene_guterres(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 66, 38))
    d.text((x + 10, y + 8), "150", font=SANS_B(46), fill=(232, 196, 80))
    d.text((x + 10, y + 56), "DELEGATES BACK A", font=SANS_B(15), fill=(232, 196, 80))
    d.text((x + 10, y + 74), "RISK FRAMEWORK", font=SANS_B(15), fill=(232, 196, 80))
    # globe, masked to its circle
    cx, cy, r = x + w - 52, y + 52, 42
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([cx - r - x, cy - r - y, cx + r - x, cy + r - y], fill=255)
    globe = Image.new("RGB", (w, h), (16, 66, 38))
    gd = ImageDraw.Draw(globe)
    gd.ellipse([cx - r - x, cy - r - y, cx + r - x, cy + r - y],
               outline=(190, 220, 180), width=2)
    gd.ellipse([cx - r // 2 - x, cy - r - y, cx + r // 2 - x, cy + r - y],
               outline=(190, 220, 180), width=1)
    gd.line([cx - r - x, cy - y, cx + r - x, cy - y], fill=(190, 220, 180), width=1)
    gd.arc([cx - r - x, cy - r // 2 - y, cx + r - x, cy + r // 2 - y], 0, 360,
           fill=(190, 220, 180), width=1)
    img.paste(globe, (x, y), mask)
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(0, 0, 0))
    d.text((x + 6, y + h - 14), "BRIDGETOWN SUMMIT, BARBADOS",
           font=SANS_B(9), fill=(255, 255, 255))


def scene_power(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 214))
    d.text((x + 8, y + 6), "NARROWEST SINCE 2018", font=SANS_B(11), fill=INK)
    d.text((x + w - 66, y + 6), "GAP 5.3", font=SANS_B(11), fill=RED)
    bars = [("78.9", "US", NAVY, 250), ("73.6", "CHINA", RED, 236),
            ("40.5", "INDIA", GOLD, 130)]
    by = y + 26
    for val, lab, col, bw in bars:
        d.text((x + 8, by + 2), val, font=SANS_B(13), fill=INK)
        d.rectangle([x + 62, by, x + 62 + bw, by + 18], fill=col)
        tcol = (255, 255, 255) if col != GOLD else (30, 30, 30)
        lf = SANS_B(11)
        d.text((x + 62 + bw - 4 - d.textlength(lab, font=lf), by + 3), lab,
               font=lf, fill=tcol)
        by += 24
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(0, 0, 0))
    d.text((x + 6, y + h - 14), "ASIA POWER INDEX 2026  \u00b7  LOWY INSTITUTE",
           font=SANS_B(9), fill=(255, 255, 255))


heroes = [
    (scene_kospi, "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE", "REPORTED"),
    (scene_guterres, "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS", "REPORTED"),
    (scene_power, "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE", "REPORTED"),
]
for (scene_fn, head, body, src, chip_lab), hx in zip(heroes, HX):
    scene_fn(hx, HY, HW, SCENE_H)
    ty = HY + SCENE_H + 6
    hf = fit_font(d, head, HW, 16, SANS_B)
    hlines = wrap(d, head, hf, HW)
    for ln in hlines[:2]:
        d.text((hx, ty), ln, font=hf, fill=INK)
        ty += 19
    bf = SANS(10)
    for ln in wrap(d, body, bf, HW)[:2]:
        d.text((hx, ty), ln, font=bf, fill=(40, 40, 40))
        ty += 13
    # source + chip on their own row, clear of the body
    sy = HY + SCENE_H + 82
    d.text((hx, sy), src, font=SANS(8), fill=GREY)
    chip(d, hx + HW - 62, sy - 1, chip_lab, NAVY)

# ---------- more of the day ----------
d.rectangle([MX, 398, 1014, 416], fill=(0, 0, 0))
d.text((MX + 6, 402), "MORE OF THE DAY  \u2014  10 STORIES", font=SANS_B(11),
       fill=(255, 255, 255))

cards = [
    ("1", "AMERICAS", "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "WSJ", "REPORTED"),
    ("2", "AMERICAS", "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("3", "WHITE HOUSE", "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("4", "MARKETS", "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("5", "SPORT", "SKUBAL'S $450M METS DEAL", "Nine-year, largest ever.", "AP", "REPORTED"),
    ("6", "SPORT", "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("7", "LEGAL", "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("8", "TECH", "ANTHROPIC IPO: $107.3B", "Raised $83, closes $97.17.", "WSJ", "REPORTED"),
    ("9", "EUROPE", "POLAND: 3 MISSILES CROSSED", "3 Kh-101s crossed airspace.", "AP", "CLAIM"),
    ("10", "SPACE", "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
cardw, cardh = 196, 68
for i, (num, cat, head, body, src, chip_lab) in enumerate(cards):
    row, col = divmod(i, 5)
    cx = MX + col * (cardw + 6)
    cy = 420 + row * (cardh + 4)
    d.rectangle([cx, cy, cx + cardw, cy + cardh], outline=(200, 190, 170), width=1)
    d.text((cx + 5, cy + 3), num, font=SANS_B(11), fill=RED)
    d.text((cx + 22, cy + 4), cat, font=SANS_B(8), fill=RED)
    hf = fit_font(d, head, cardw - 10, 10, SANS_B)
    hlines = wrap(d, head, hf, cardw - 10)
    hy = cy + 16
    for ln in hlines[:2]:
        d.text((cx + 5, hy), ln, font=hf, fill=INK)
        hy += 12
    d.text((cx + 5, cy + 42), body, font=SANS(9), fill=(40, 40, 40))
    d.text((cx + 5, cy + 54), src, font=SANS(8), fill=GREY)
    chip(d, cx + cardw - 62, cy + 53, chip_lab,
         NAVY if chip_lab == "REPORTED" else RED)

# ---------- where it happened ----------
d.rectangle([MX, 560, 1014, 578], fill=(0, 0, 0))
d.text((MX + 6, 564), "WHERE IT HAPPENED", font=SANS_B(11), fill=(255, 255, 255))

# map blobs (stylised)
MAPX, MAPY, MAPW, MAPH = MX, 582, 340, 190
d.rectangle([MAPX, MAPY, MAPX + MAPW, MAPY + MAPH], fill=(238, 236, 222))
# Americas blob
d.polygon([(MAPX + 18, MAPY + 12), (MAPX + 78, MAPY + 8), (MAPX + 92, MAPY + 40),
           (MAPX + 70, MAPY + 96), (MAPX + 52, MAPY + 150), (MAPX + 34, MAPY + 176),
           (MAPX + 16, MAPY + 120), (MAPX + 8, MAPY + 60)], fill=MAPGREEN)
# Eurasia blob
d.polygon([(MAPX + 118, MAPY + 22), (MAPX + 330, MAPY + 14), (MAPX + 336, MAPY + 60),
           (MAPX + 300, MAPY + 108), (MAPX + 220, MAPY + 120), (MAPX + 150, MAPY + 96),
           (MAPX + 116, MAPY + 60)], fill=MAPGREEN)
# Africa blob
d.polygon([(MAPX + 158, MAPY + 118), (MAPX + 210, MAPY + 112), (MAPX + 224, MAPY + 150),
           (MAPX + 196, MAPY + 184), (MAPX + 168, MAPY + 172)], fill=MAPGREEN)
pins = [
    (1, 300, 60), (2, 62, 148), (3, 318, 44), (4, 52, 66), (5, 76, 92),
    (6, 238, 52), (7, 196, 66), (8, 172, 48), (9, 222, 70), (10, 152, 36),
    (11, 262, 92), (12, 238, 112), (13, 188, 152),
]
pf = SANS_B(9)
for n, px, py in pins:
    d.ellipse([MAPX + px - 9, MAPY + py - 9, MAPX + px + 9, MAPY + py + 9],
              fill=RED, outline=(255, 255, 255), width=1)
    t = str(n)
    d.text((MAPX + px - d.textlength(t, font=pf) / 2, MAPY + py - 6), t,
           font=pf, fill=(255, 255, 255))
leg = ["Pins 1\u201313:  1 Seoul  \u00b7  2 Bridgetown  \u00b7  3 Beijing  \u00b7  4 Washington",
       "5 New York  \u00b7  6 Kyiv  \u00b7  7 Paris  \u00b7  8 London  \u00b7  9 Warsaw  \u00b7  10 Manchester",
       "11 Beirut  \u00b7  12 Gaza  \u00b7  13 Khartoum"]
ly = MAPY + MAPH + 4
for ln in leg:
    d.text((MAPX, ly), ln, font=SANS(9), fill=GREY)
    ly += 12

# ---------- ALSO ----------
AX = 372
d.text((AX, 582), "ALSO ON MONDAY", font=SANS_B(11), fill=INK)
also = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: Antalya pact rejected",
    "18. Israel unity talks resume",
    "19. Gaza: two killed in Israeli strike",
    "20. West Bank settler attacks",
    "21. Iran war: no deal in sight",
    "22. Lebanon seizes 264 kg explosives",
    "23. Bahrain: strike hits plant, 2 hurt",
    "24. Benghazi: UN demands probe [CLAIM]",
    "25. Sudan: defences down drones [CLAIM]",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits over AI exam row",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
af = SANS(10)
ay = 600
for item in also:
    d.text((AX, ay), item, font=af, fill=INK)
    ay += 14

# ---------- DATE CHECK ----------
d.rectangle([MX, 862, 1014, 944], outline=RED, width=2)
d.text((MX + 8, 868), "DATE CHECK  \u2014  READ 23 NOV 2026, 23:59 UTC  \u00b7  STORIES DATED 23 NOV ONLY",
       font=SANS_B(10), fill=RED)
d.text((MX + 8, 886),
       "LEFT OUT \u2014 NOT 23 NOV:  Dems reach 258 (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo Isidro captured (22 Nov)",
       font=SANS(10), fill=INK)
d.text((MX + 8, 902),
       "EU\u2013Indonesia pact (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar ruling (19 Nov)",
       font=SANS(10), fill=INK)
d.text((MX + 8, 922),
       "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
       font=SANS(10), fill=INK)

# ---------- footer ----------
d.text((MX, 952), "Sources: Reuters  \u00b7  AP  \u00b7  Bloomberg  \u00b7  AFP  \u00b7  Yonhap  \u00b7  BBC  \u00b7  WSJ  \u00b7  ESPN  \u00b7  Lowy Institute (Asia Power Index 2026).",
       font=SANS(9), fill=GREY)
d.text((MX, 966), "CHIPS: REPORTED = confirmed by wires  \u00b7  CLAIM = one side's claim, independently unconfirmed  \u00b7  ONGOING = still developing.",
       font=SANS(9), fill=GREY)
d.text((MX, 980), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
       font=SANS(9), fill=GREY)
d.line([MX, 998, 1014, 998], fill=GOLD, width=1)
ff = SANS_B(10)
ft = "THE WORLD TODAY  \u00b7  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions"
d.text(((1024 - d.textlength(ft, font=ff)) / 2, 1004), ft, font=ff, fill=GOLD)

img.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"))
print("saved entry.png", img.size)
