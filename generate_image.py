#!/usr/bin/env python3
"""Draw the 25 November 2026 world-news front page (1024x1024, build time only).

Layout: masthead + date check, three hero stories with drawn scenes,
a pin map and a UTC timeline strip, then a 3 x 8 grid of short stories,
and a sources footer. Every story below was published or first reported
on Wednesday 25 November 2026 (any time zone); sources are listed in the
footer and in the README.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (246, 241, 229)
INK = (20, 20, 20)
GREY = (90, 86, 76)
NAVY = (22, 50, 79)
RED = (158, 27, 27)
TEAL = (15, 95, 92)
GOLD = (138, 109, 0)
CARD = (255, 253, 247)
LINE = (180, 172, 150)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
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


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text, truncating with an ellipsis so it never overflows."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + " ...", font=fnt) > max_w:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + " ..."
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- heroes
HEROES = [
    {
        "tag": "CYBERATTACK",
        "color": (123, 31, 162),
        "scene": "cyber",
        "head": "CIA and spy chief's office hit by cyberattack",
        "body": ("CNN reports the CIA and the spy chief's office were hit by "
                 "a cyberattack on classified systems."),
    },
    {
        "tag": "HEALTH",
        "color": (0, 105, 92),
        "scene": "health",
        "head": "WHO evacuates Ebola hospital as fighting closes in",
        "body": ("WHO staff sheltered three days in a hospital in Akwe, Ituri, "
                 "then left under fire."),
    },
    {
        "tag": "ENERGY",
        "color": (141, 110, 0),
        "scene": "energy",
        "head": "Three oil tankers hit by mines in Strait of Hormuz",
        "body": ("Iran's Revolutionary Guard Navy says mines struck three "
                 "tankers in the strait, raising fears for shipping."),
    },
]


def draw_scene(draw, kind, x, y, w, h):
    if kind == "cyber":
        draw.rectangle([x, y, x + w, y + h], fill=(24, 32, 58))
        # laptop
        draw.rectangle([x + 18, y + 14, x + 78, y + 48], fill=(200, 205, 215),
                       outline=(120, 125, 140))
        draw.rectangle([x + 22, y + 18, x + 74, y + 44], fill=(16, 60, 40))
        for i, ln in enumerate(["10110 011", "01101 110", "11010 001"]):
            draw.text((x + 25, y + 21 + i * 8), ln, font=font(SANS, 7),
                      fill=(80, 220, 140))
        draw.rectangle([x + 10, y + 48, x + 86, y + 53], fill=(150, 155, 168))
        # warning shield
        cx, cy = x + w - 52, y + 32
        draw.polygon([(cx, cy - 20), (cx + 18, cy - 12), (cx + 18, cy + 6),
                      (cx, cy + 20), (cx - 18, cy + 6), (cx - 18, cy - 12)],
                     fill=(198, 40, 40), outline=(255, 255, 255))
        draw.text((cx - 3, cy - 12), "!", font=font(SANS_B, 20), fill=(255, 255, 255))
        draw.text((x + 100, y + 12), "CLASSIFIED", font=font(SANS_B, 11),
                  fill=(255, 120, 120))
        draw.text((x + 100, y + 28), "SYSTEMS", font=font(SANS_B, 11),
                  fill=(255, 120, 120))
        draw.text((x + 100, y + 44), "BREACHED", font=font(SANS_B, 11),
                  fill=(255, 120, 120))
    elif kind == "health":
        draw.rectangle([x, y, x + w, y + h], fill=(214, 232, 228))
        # hospital building
        draw.rectangle([x + 16, y + 16, x + 96, y + h - 6], fill=(255, 255, 255),
                       outline=(120, 140, 135))
        draw.rectangle([x + 46, y + 22, x + 66, y + 42], fill=(198, 40, 40))
        draw.rectangle([x + 52, y + 16, x + 60, y + 48], fill=(198, 40, 40))
        for i in range(3):
            draw.rectangle([x + 24 + i * 24, y + 52, x + 38 + i * 24, y + 62],
                           fill=(150, 180, 175))
        # ambulance van
        draw.rectangle([x + 120, y + 34, x + 190, y + 58], fill=(255, 255, 255),
                       outline=(120, 140, 135))
        draw.rectangle([x + 126, y + 38, x + 140, y + 46], fill=(198, 40, 40))
        draw.rectangle([x + 132, y + 34, x + 136, y + 50], fill=(198, 40, 40))
        draw.ellipse([x + 128, y + 54, x + 140, y + 64], fill=(40, 40, 40))
        draw.ellipse([x + 168, y + 54, x + 180, y + 64], fill=(40, 40, 40))
        draw.text((x + 200, y + 20), "AKWE, ITURI", font=font(SANS_B, 11),
                  fill=(0, 105, 92))
        draw.text((x + 200, y + 36), "EVACUATED", font=font(SANS_B, 11),
                  fill=(0, 105, 92))
    else:  # energy
        draw.rectangle([x, y, x + w, y + h], fill=(158, 196, 222))
        # tanker
        draw.polygon([(x + 14, y + 30), (x + 150, y + 30), (x + 168, y + 46),
                      (x + 168, y + 56), (x + 14, y + 56)], fill=(60, 60, 70))
        for i in range(4):
            draw.rectangle([x + 24 + i * 32, y + 12, x + 50 + i * 32, y + 30],
                           fill=(178, 60, 40) if i % 2 else (40, 90, 140))
        draw.rectangle([x + 152, y + 8, x + 164, y + 30], fill=(220, 220, 220))
        # waves
        for i in range(5):
            wx = x + 10 + i * 34
            draw.arc([wx, y + h - 18, wx + 30, y + h + 2], 180, 360,
                     fill=(255, 255, 255), width=3)
        # sea mines
        for mx, my in [(x + 205, y + 18), (x + 235, y + 40), (x + 200, y + 48)]:
            draw.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=(30, 30, 30))
            for dx, dy in [(0, -11), (0, 11), (-11, 0), (11, 0)]:
                draw.line([mx, my, mx + dx, my + dy], fill=(30, 30, 30), width=2)
        draw.text((x + 250, y + 12), "3 TANKERS", font=font(SANS_B, 11),
                  fill=(120, 60, 0))
        draw.text((x + 250, y + 28), "MINED", font=font(SANS_B, 11),
                  fill=(120, 60, 0))


# ---------------------------------------------------------------- timeline
TIMELINE = [
    ("00-06 UTC", "UN warns aid lines choking for 7.3m"),
    ("00-06 UTC", "Nepal quake 5.3; tremors in N. Bengal"),
    ("06-12 UTC", "NATO early-warning planes for Poland"),
    ("06-12 UTC", "Huawei guilty on 10 of 12 counts"),
    ("12-18 UTC", "Zelenskiy: Ukraine hit Russian ship"),
    ("12-18 UTC", "Trump pardons turkeys Freedom, Feathers"),
    ("18-24 UTC", "Wall St cools: Nasdaq -2.0%, Nvidia -5.9%"),
    ("18-24 UTC", "S. Korea warns evacuation; Russian jet"),
]

# ---------------------------------------------------------------- pin map
# Rough continent outlines as (lon, lat) polygons, equirectangular.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 71), (-95, 71), (-80, 70), (-58, 62),
     (-65, 50), (-70, 42), (-76, 35), (-81, 26), (-90, 21), (-97, 16),
     (-92, 14), (-105, 20), (-114, 28), (-125, 40), (-150, 60)],
    [(-80, 10), (-62, 9), (-50, 0), (-35, -6), (-40, -22), (-48, -28),
     (-58, -35), (-66, -40), (-70, -50), (-74, -30), (-77, -12), (-81, -4)],
    [(-10, 36), (-2, 43), (-4, 48), (2, 51), (8, 57), (12, 55), (18, 56),
     (21, 60), (28, 70), (32, 68), (40, 60), (44, 42), (36, 36), (28, 40),
     (22, 40), (18, 40), (12, 38), (3, 38)],
    [(-17, 15), (-16, 21), (-10, 31), (0, 36), (10, 37), (20, 32), (30, 31),
     (33, 27), (38, 20), (43, 11), (48, 10), (51, -2), (40, -12), (38, -26),
     (32, -29), (26, -34), (19, -35), (16, -28), (12, -18), (9, -2), (8, 4),
     (-8, 5)],
    [(40, 68), (55, 70), (68, 73), (90, 76), (110, 77), (130, 72), (150, 70),
     (170, 66), (162, 60), (158, 52), (142, 50), (140, 40), (130, 33),
     (127, 35), (122, 30), (120, 22), (110, 20), (105, 9), (100, 7), (97, 16),
     (92, 22), (88, 22), (85, 19), (80, 13), (77, 8), (73, 16), (70, 22),
     (66, 25), (61, 25), (57, 26), (52, 27), (50, 30), (48, 30), (44, 39),
     (41, 41), (38, 46), (40, 55)],
    [(113, -22), (122, -14), (130, -12), (136, -12), (142, -11), (146, -19),
     (150, -22), (153, -27), (150, -37), (140, -38), (132, -32), (124, -33),
     (115, -35), (113, -26)],
]
PINS = [  # (lon, lat, label)
    (-77, 39, "1"), (24, 60, "2"), (56, 26, "3"), (30, 2, "4"),
    (121, 31, "5"), (0, 51, "6"), (149, -35, "7"), (45, 13, "8"),
]
PIN_LEGEND = [
    "1 Washington  2 Gulf of Finland  3 Hormuz  4 Ituri, DR Congo",
    "5 Shanghai  6 London  7 Canberra  8 Aden",
]

# ---------------------------------------------------------------- grid
TAG_COLORS = {
    "EUROPE": (31, 78, 121), "MIDDLE EAST": (122, 59, 0), "ASIA": (138, 26, 26),
    "AMERICAS": (20, 90, 50), "AFRICA": (107, 63, 160), "OCEANIA": (0, 105, 92),
    "SPORT": (178, 106, 0), "TECH": (55, 71, 79),
}
GRID = [
    ("EUROPE", "Sarkozy case sent to trial",
     "Ex-president's case to trial; hearing 1 Apr 2027."),
    ("EUROPE", "EU adds Russia sanctions",
     "Brussels announces more measures over Ukraine war."),
    ("EUROPE", "Russia, Ukraine clash at UN",
     "Both sides trade accusations over shipping, energy."),
    ("EUROPE", "Sweden votes on its PM",
     "Parliament votes on Kristersson staying prime minister."),
    ("MIDDLE EAST", "Houthis close on Aden",
     "Push to 60 km from Yemen's capital; army says it holds."),
    ("MIDDLE EAST", "UN warns over Gaza",
     "UN highlights hardship for civilians seeking aid in Gaza."),
    ("MIDDLE EAST", "US, Qatar in talks",
     "Officials discuss regional issues, strategic cooperation."),
    ("MIDDLE EAST", "Doubt over Israel aid cut",
     "US envoy 'not certain' Israel aid ends this year."),
    ("ASIA", "China probes Shanghai chief",
     "Beijing opens probe into Party chief Chen Jining."),
    ("ASIA", "Death sentence for leaks",
     "Official sentenced to death for revealing 100+ secrets."),
    ("ASIA", "US blacklists chip firm",
     "US blacklists Singapore chip firm Megaspeed."),
    ("ASIA", "Punjab alliance struck",
     "BJP, Akali Dal ally for 2027 Punjab elections."),
    ("ASIA", "India buys helicopters",
     "Navy, Coast Guard to buy 76 helicopters for \u20b915,000 cr."),
    ("ASIA", "Varanasi lights up",
     "Dev Deepawali glows; Murmu attends Bali Jatra."),
    ("AMERICAS", "Giuliani gets top honour",
     "Trump awards Rudy Giuliani the Medal of Freedom."),
    ("AMERICAS", "Abrego Garcia to leave US",
     "Salvadoran migrant to leave voluntarily, media report."),
    ("AMERICAS", "Fort Hood gunman seeks stay",
     "Nidal Hasan seeks stay of execution set for next week."),
    ("AMERICAS", "Radar outage hits O'Hare",
     "Radar outage delays flights into Chicago O'Hare."),
    ("AMERICAS", "WHO: lift Cuba fuel blockade",
     "Tedros urges US to lift blockade on Cuba."),
    ("AFRICA", "RSF commander defects",
     "Commander defects, joins Sudanese army with troops."),
    ("AFRICA", "Libya conflict warning",
     "Russian vessel sunk in Libyan port; conflict may flare."),
    ("OCEANIA", "Australia says sorry",
     "Australia apologises to LGBTQ veterans for past wrongs."),
    ("SPORT", "Real Madrid hit PSV for five",
     "Madrid stay perfect; Man City held 2-2 by Napoli."),
    ("TECH", "Asia cheers Huang's return",
     "Nvidia suppliers, Asian startups cheer Huang's return."),
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(210, 226, 236))
    lon0, lon1, lat0, lat1 = -170, 190, 78, -58

    def px(lon, lat):
        return (x + (lon - lon0) / (lon1 - lon0) * w,
                y + (lat0 - lat) / (lat0 - lat1) * h)

    for poly in CONTINENTS:
        draw.polygon([px(lon, lat) for lon, lat in poly],
                     fill=(120, 140, 120), outline=(70, 95, 70))
    for lon, lat, label in PINS:
        cx, cy = px(lon, lat)
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                     outline=(255, 255, 255), width=1)
        draw.text((cx - 3, cy - 6), label, font=font(SANS_B, 9),
                  fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 84], fill=NAVY)
    d.text((W // 2, 16), "THE WORLD IN ONE PAGE", font=font(SERIF_B, 46),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 96), "WEDNESDAY 25 NOVEMBER 2026",
           font=font(SERIF_B, 34), fill=RED, anchor="ma")
    d.text((W // 2, 136),
           "35 stories from every region \u2014 as reported on 25 November 2026 \u00b7 All times UTC",
           font=font(SANS, 15), fill=GREY, anchor="ma")
    d.line([20, 160, W - 20, 160], fill=INK, width=2)
    d.line([20, 164, W - 20, 164], fill=INK, width=1)

    # ---- heroes
    hy, hh, hw, gap = 174, 172, 320, 12
    for i, hero in enumerate(HEROES):
        x = 20 + i * (hw + gap)
        d.rectangle([x, hy, x + hw, hy + hh], fill=CARD, outline=LINE, width=1)
        d.rectangle([x, hy, x + hw, hy + 6], fill=hero["color"])
        d.text((x + 10, hy + 12), hero["tag"], font=font(SANS_B, 12),
               fill=hero["color"])
        draw_scene(d, hero["scene"], x + 10, hy + 32, hw - 20, 56)
        head_lines = fit_lines(d, hero["head"], font(SERIF_B, 17), hw - 20, 2)
        y = text_block(d, x + 10, hy + 94, head_lines, font(SERIF_B, 17),
                       INK, 20)
        body_lines = fit_lines(d, hero["body"], font(SANS, 12), hw - 20, 2)
        text_block(d, x + 10, y + 2, body_lines, font(SANS, 12), (60, 56, 48), 14)

    # ---- middle row: map + timeline
    my, mh = 356, 128
    d.rectangle([20, my, 498, my + mh], fill=CARD, outline=LINE, width=1)
    d.text((30, my + 6), "WHERE IT HAPPENED", font=font(SANS_B, 12), fill=NAVY)
    draw_map(d, 30, my + 24, 458, 66)
    ly = my + 94
    for line in PIN_LEGEND:
        d.text((30, ly), line, font=font(SANS, 10), fill=GREY)
        ly += 13

    d.rectangle([526, my, 1004, my + mh], fill=CARD, outline=LINE, width=1)
    d.text((536, my + 6), "THE DAY IN UTC", font=font(SANS_B, 12), fill=NAVY)
    ty = my + 26
    for j in range(0, 8, 2):
        for k, idx in enumerate((j, j + 1)):
            cx = 536 + k * 238
            when, what = TIMELINE[idx]
            d.text((cx, ty), when, font=font(SANS_B, 10), fill=RED)
            lines = fit_lines(d, what, font(SANS, 11), 232, 1)
            yy = ty + 12
            for line in lines:
                d.text((cx, yy), line, font=font(SANS, 11), fill=INK)
                yy += 13
        ty += 26

    # ---- story grid
    gy, row_h, col_w = 494, 59, 318
    for i, (tag, head, detail) in enumerate(GRID):
        r, c = divmod(i, 3)
        x = 20 + c * (col_w + 14)
        y = gy + r * row_h
        d.rectangle([x, y, x + col_w, y + row_h - 4], fill=CARD,
                    outline=LINE, width=1)
        d.text((x + 8, y + 4), tag, font=font(SANS_B, 10),
               fill=TAG_COLORS[tag])
        head_lines = fit_lines(d, head, font(SERIF_B, 14), col_w - 16, 1)
        d.text((x + 8, y + 18), head_lines[0], font=font(SERIF_B, 14), fill=INK)
        det_lines = fit_lines(d, detail, font(SANS, 11), col_w - 16, 1)
        d.text((x + 8, y + 37), det_lines[0], font=font(SANS, 11),
               fill=(70, 66, 58))

    # ---- footer
    fy = 972
    d.line([20, fy, W - 20, fy], fill=INK, width=1)
    d.text((W // 2, fy + 6),
           "Sources: Reuters \u00b7 CNN \u00b7 WHO \u00b7 UEFA \u00b7 AP \u00b7 Le Monde \u00b7 Jagran Josh",
           font=font(SANS, 12), fill=GREY, anchor="ma")
    d.text((W // 2, fy + 24),
           "Drawn entirely in code \u2014 no photographs. Every story happened or was first reported on 25 November 2026.",
           font=font(SANS, 11), fill=GREY, anchor="ma")

    img.save(OUT, optimize=True)
    print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
