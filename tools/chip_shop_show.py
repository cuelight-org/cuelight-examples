#!/usr/bin/env python3
"""Write the chip shop menu board: chip_shop/show.json.

    tools/chip_shop_show.py

One 5760x1080 canvas for three 1920x1080 screens side by side: the
boards are laid out per screen, and the news ticker along the bottom runs
across all three. Needs fontTools, for the ticker's width.
"""

import json
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent / "chip_shop"
SCREEN, SCREENS = (1920, 1080), 3
WIDTH, HEIGHT = SCREEN[0] * SCREENS, SCREEN[1]

YELLOW, WHITE, INK, STRIP, NEWS = "#FFC61A", "#F2F4F7", "#2B1F00", "#0A0B10", "#B8AA86"
HEADING, ITEM, PRICE, TICKER = 68, 37, 37, 42
BAR = 76                 # the ticker strip's height
LINE, GAP = 46, 24            # an item's row, and the room under a heading
M = 60                        # a screen's side margin

FONTS = {
    "heading": {"file": "BebasNeue-Regular", "size": HEADING, "color": YELLOW,
                "border": {"color": INK, "width": 3}},
    "column": {"file": "BebasNeue-Regular", "size": 30, "color": YELLOW},
    "item": {"file": "BarlowSemiCondensed-Bold", "size": ITEM, "color": WHITE,
             "shadow": {"color": "#00000099", "offset": [2, 2]}},
    "price": {"file": "BarlowSemiCondensed-Bold", "size": PRICE, "color": WHITE,
              "shadow": {"color": "#00000099", "offset": [2, 2]}},
    "ticker": {"file": "BarlowSemiCondensed-BoldItalic", "size": TICKER, "color": NEWS},
    "brand": {"file": "BebasNeue-Regular", "size": 96, "color": YELLOW,
              "border": {"color": INK, "width": 4}},
    "brand_line": {"file": "BarlowSemiCondensed-BoldItalic", "size": 30, "color": WHITE},
}

# Each item: name, price or (price, price), and an icon or None.
FRIES = [("SMALL CONE", "2.80"), ("SMALL", "3.20"), ("MEDIUM", "3.50"), ("LARGE", "3.80"),
         ("EXTRA LARGE", "6.00"), ("FAMILY BOX", "8.00")]
DRINKS = [("COLA / LIGHT / ZERO", "2.50", "3.00"), ("ORANGE / LEMON", "2.50", "3.00"), ("ICED TEA", "2.50", None),
          ("STILL WATER", None, "2.50"), ("LAGER", "2.50", None), ("ENERGY DRINK", "3.00", None)]
COLD = [("ON THE FRIES", "1.10"), ("SMALL TUB", "1.20"), ("LARGE TUB", "2.40")]
HOT = [("STEW GRAVY", "3.00"), ("GOULASH", "3.00"), ("CURRY", "2.50"), ("PEPPER SAUCE", "2.50"),
       ("BOLOGNESE", "3.00")]
SALADS = [("GARDEN SALAD", "7.00")]
SNACKS_A = [("SKEWER", "4.30"), ("NOODLE ROLL", "3.00", "leaf"), ("CRUNCHY BITE", "3.80"), ("BEAR PAW", "3.80"),
            ("MEATBALLS (5)", "3.00"), ("MEATBALL / SPECIAL", ("3.00", "4.00")), ("SAUSAGE / SPECIAL", ("4.20", "5.20")),
            ("CHEESE CRACK", "3.00"), ("CHICKEN CHILI", "3.90", "drumstick"), ("CHICKEN NUGGETS", "4.00", "drumstick"),
            ("GRIZZLY", "4.50", "flame"), ("CURRYWURST / SPECIAL", ("2.50", "3.50")), ("CURRYWURST XXL", "5.00"),
            ("DYNAMITE", "3.80", "flame"), ("PRAWN CROQUETTE", "3.80", "fish"), ("GOULASH CROQUETTE", "3.00"),
            ("CHEESE CROQUETTE", "3.20", "leaf"), ("COD STICK", "4.50", "fish")]
SNACKS_B = [("TURKEY SKEWER", "4.20"), ("CHEESY CHICKEN", "4.00", "drumstick"), ("CHICKEN CORN", "3.20", "drumstick"),
            ("CHICKEN WINGS", "5.30", "drumstick"), ("CHICKEN ROLL", "5.00", "drumstick"), ("MINI SPRING ROLLS", "4.00", "leaf"),
            ("SPRING ROLL", "3.70"), ("LUCIFER", "4.00", "flame"), ("MINI LUCIFER (4)", "4.00", "flame"), ("MAMMOTH", "3.50"),
            ("MEXICANO", "3.50", "flame"), ("MINI MEGA MIX", "5.00"), ("MUSSELS", "5.20", "fish"),
            ("MOZZARELLA FINGERS", "4.00", "leaf"), ("RAGOUT BALL", "3.50"), ("RIB BITES", "3.80"),
            ("BREADED SKEWER", "3.20"), ("SATAY", "4.00")]
SNACKS_C = [("CHICKEN SKEWER", "4.00", "drumstick"), ("SHASHLIK", "5.80"), ("TACO", "4.50"), ("THE DOUBTER", "5.50"),
            ("VIANDEL / SPECIAL", ("3.20", "4.20")), ("MEAT CROQUETTE", "3.00"), ("FIRE EATER", "3.50", "flame"),
            ("GYPSY STICK", "3.80"), ("VEGGIE CURRYWURST", "3.00"), ("VEGGIE CHICKEN CORN", "3.50", "leaf"),
            ("VEGGIE MEATBALLS", "3.50", "leaf")]
HOMEMADE = [("BEEF STEW", "6.00"), ("GOULASH", "5.50"), ("VOL-AU-VENT", "5.50", "drumstick"),
            ("SPAGHETTI SMALL / LARGE", ("8.50", "9.50"))]
BURGERS = [("HAMBURGER", "4.20"), ("BICKY BURGER", "4.50"), ("BICKY CHEESE", "4.80"), ("BICKY CHICKEN", "4.80", "drumstick"),
           ("BICKY FISH", "4.80", "fish"), ("BICKY BASTARD", "4.80", "leaf"), ("BICKY CHICKLESS", "4.80", "leaf"),
           ("VEGGIE BURGER", "4.80", "leaf"), ("MEXICAN SANDWICH", "5.50", "flame"), ("BICKY ROYAL", "6.80"),
           ("BICKY ROYAL CHEESE", "7.20"), ("BICKY WRAP", "5.50"), ("BICKY MEXICANO", "5.50", "flame")]

HEADLINES = [
    "Local man wins a lifetime supply of mayonnaise, asks whether it comes with fries",
    "Town council approves a second fryer after a forty-year debate",
    "Study finds the last fry in the cone is the best one, and always was",
    "Weather: a chance of drizzle this afternoon, a certainty of gravy tonight",
    "Seagull elected chairman of the harbour committee on a platform of chips",
    "Scientists confirm fries taste better when somebody else is paying",
    "Record turnout as the village votes on the correct amount of salt",
    "Lost cat found asleep in the mayonnaise aisle, in excellent spirits",
]

FONT_FILES = {}


def advance(font, size, text):
    """Width of `text` in the font at `size`, from its advances."""
    file = FONTS[font]["file"]
    if file not in FONT_FILES:
        FONT_FILES[file] = TTFont(ROOT / "assets/fonts" / f"{file}.ttf")
    tt = FONT_FILES[file]
    cmap, hmtx, upm = tt.getBestCmap(), tt["hmtx"], tt["head"].unitsPerEm
    units = sum(hmtx[cmap.get(ord(c), ".notdef")][0] for c in text)
    return units * size / upm


def text(name, words, x, y, font, **extra):
    return {"name": name, "type": "text", "text": words, "font": font, "x": x, "y": y, **extra}


def euro(price):
    return f"€{price}"


def rows(prefix, items, x, right, y, icons=True):
    """Menu rows from `y` down: the name at `x`, the price ending at
    `right`, an icon just left of the price where one is given."""
    out = []
    for i, item in enumerate(items):
        name, price, icon = (item + (None,))[:3]
        top = y + i * LINE
        out.append(text(f"{prefix}_{i}", name, x, top, "item"))
        if isinstance(price, tuple):
            shown = f"{euro(price[0])} / {euro(price[1])}"
        else:
            shown = euro(price)
        out.append(text(f"{prefix}_{i}_price", shown, right, top, "price", anchor="top_right"))
        if icon and icons:
            out.append({"name": f"{prefix}_{i}_icon", "type": "image", "image": icon,
                        "x": right - advance("price", PRICE, shown) - 40, "y": top + 8})
    return out


def heading(name, words, x, y):
    return text(name, words, x, y, "heading")


def block(prefix, title, items, x, right, y):
    """A heading and its rows; returns the layers and the y below them."""
    layers = [heading(f"{prefix}_heading", title, x, y)]
    layers += rows(prefix, items, x, right, y + HEADING + GAP)
    return layers, y + HEADING + GAP + len(items) * LINE + 34


def screen_1():
    left, lright = M, 930
    right, rright = 1010, SCREEN[0] - M
    layers, y = block("fries", "FRIES", FRIES, left, lright, 40)
    # Drinks: two price columns, can and bottle.
    y += 20
    layers.append(heading("drinks_heading", "DRINKS", left, y))
    layers.append(text("drinks_can", "CAN", lright - 260, y + 30, "column", anchor="top_right"))
    layers.append(text("drinks_bottle", "BOTTLE", lright, y + 30, "column", anchor="top_right"))
    top = y + HEADING + GAP
    for i, (name, can, bottle) in enumerate(DRINKS):
        layers.append(text(f"drink_{i}", name, left, top + i * LINE, "item"))
        if can:
            layers.append(text(f"drink_{i}_can", euro(can), lright - 260, top + i * LINE, "price", anchor="top_right"))
        if bottle:
            layers.append(text(f"drink_{i}_bottle", euro(bottle), lright, top + i * LINE, "price", anchor="top_right"))
    more, y = block("cold", "COLD SAUCES", COLD, right, rright, 40)
    layers += more
    more, y = block("hot", "HOT SAUCES", HOT, right, rright, y)
    layers += more
    more, y = block("salads", "SALADS", SALADS, right, rright, y)
    layers += more
    return layers


def screen_2():
    layers = [heading("snacks_heading", "SNACKS", M, 40)]
    top = 40 + HEADING + GAP
    layers += rows("snack_a", SNACKS_A, M, 930, top)
    layers += rows("snack_b", SNACKS_B, 1010, SCREEN[0] - M, top)
    return layers


def screen_3():
    left, lright = M, 900
    right, rright = 980, SCREEN[0] - M
    layers, y = block("snack_c", "SNACKS", SNACKS_C, left, lright, 40)
    more, y = block("homemade", "HOMEMADE", HOMEMADE, left, lright, y)
    layers += more
    more, y = block("burgers", "BURGERS", BURGERS, right, rright, 40)
    layers += more
    # The shop's mark, where the supplier's logo goes on the real board.
    layers.append(text("brand", "THE CHIP SHOP", rright, y + 10, "brand", anchor="top_right"))
    layers.append(text("brand_line", "fried fresh since 1962", rright, y + 118, "brand_line", anchor="top_right"))
    return layers


def ticker():
    """One line of headlines crossing all three screens, right to left,
    over and over."""
    line = "   ·   ".join(HEADLINES) + "   ·   "
    width = advance("ticker", TICKER, line)
    speed = 240.0            # canvas pixels per second
    total = (WIDTH + width) / speed
    return [
        {"name": "strip", "type": "shape", "shape": {"rect": [0, 0, WIDTH, BAR]}, "y": HEIGHT - BAR, "fill": STRIP},
        {"name": "rule", "type": "shape", "shape": {"rect": [0, 0, WIDTH, 2]}, "y": HEIGHT - BAR, "fill": YELLOW, "opacity": 0.35},
        {
            "name": "news", "type": "text", "text": line, "font": "ticker", "x": WIDTH, "y": HEIGHT - BAR + (BAR - TICKER) // 2,
            "timelines": [{"name": "crawl", "autoplay": True, "loop": True, "tracks": [
                {"property": "x", "keys": [{"t": 0, "v": WIDTH}, {"t": round(total, 2), "v": round(-width, 1)}]}]}],
        },
    ]


def main():
    screens = []
    for i, build in enumerate((screen_1, screen_2, screen_3)):
        screens.append({"name": f"screen_{i + 1}", "type": "group", "x": i * SCREEN[0], "y": 0, "children": build()})
    show = {
        "$schema": "https://raw.githubusercontent.com/francisdb/cuelight/main/crates/cuelight/schemas/show.schema.json",
        "format": 1,
        "name": "chip_shop",
        "size": [WIDTH, HEIGHT],
        "background": "#131A26",
        "fonts": FONTS,
        "layers": [
            {"name": "board", "type": "image", "image": "chalk", "size": [WIDTH, HEIGHT],
             "repeat": {"size": list(SCREEN)}},
            *screens,
            *ticker(),
        ],
    }
    (ROOT / "show.json").write_text(json.dumps(show, indent=2, ensure_ascii=False) + "\n")
    print(f"chip_shop/show.json: {sum(1 for _ in open(ROOT / 'show.json'))} lines, ticker {advance('ticker', TICKER, '   ·   '.join(HEADLINES)):.0f} px")


if __name__ == "__main__":
    main()
