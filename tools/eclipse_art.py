#!/usr/bin/env python3
"""Write the artwork of eclipse: the corona, the ground and the continent.

    tools/eclipse_art.py demos/eclipse/assets

corona.png is the sun's outer atmosphere around a hole the size of the
moon: long streamers near the equator, short plumes at the poles and fine
rays everywhere, falling off with the distance from the limb. It is drawn
with `screen` over the dark sky. The skies and the glows are gradients in
the show itself.

ground.svg is the land at the foot of the sky window with a tree on the
left hill and two people on the right one, looking up, in silhouette.
continent.svg is the land on the edge of the Earth in the side view,
drawn past the Earth's edge, which the show clips away.

Needs numpy and Pillow.
"""

import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

# Sun radius in the sky window, as in tools/eclipse_show.py.
SUN_R = 100


def corona(size=560):
    rng = np.random.default_rng(7)
    c = (size - 1) / 2
    y, x = np.mgrid[0:size, 0:size]
    dx, dy = x - c, y - c
    r = np.hypot(dx, dy) / SUN_R
    a = np.arctan2(dy, dx)
    # Streamers: broad lobes near the equator (left and right), slightly
    # tilted, with a few narrower ones in between.
    lobes = np.zeros_like(a)
    for centre, width, strength in [
        (0.12, 0.28, 1.0), (math.pi + 0.1, 0.32, 0.9), (0.55, 0.14, 0.55),
        (-0.42, 0.16, 0.6), (math.pi - 0.5, 0.15, 0.5), (math.pi + 0.62, 0.12, 0.45),
        (2.1, 0.2, 0.25), (-2.2, 0.18, 0.3),
    ]:
        d = np.angle(np.exp(1j * (a - centre)))
        lobes += strength * np.exp(-((d / width) ** 2))
    # Fine rays: a sum of thin random spokes.
    rays = np.zeros_like(a)
    for _ in range(90):
        centre = rng.uniform(-math.pi, math.pi)
        d = np.angle(np.exp(1j * (a - centre)))
        rays += rng.uniform(0.05, 0.25) * np.exp(-((d / rng.uniform(0.01, 0.04)) ** 2))
    reach = 0.9 + 1.6 * lobes + 0.5 * rays
    over = np.clip(r - 1, 0, None)
    intensity = np.exp(-over / (0.22 * reach)) * (0.55 + 0.45 * np.clip(lobes + rays, 0, 1.4) / 1.4)
    # Brighter right at the limb, the inner corona.
    intensity += 0.6 * np.exp(-over / 0.05)
    intensity[r < 1] = 0
    # Fade out before the edge of the image so no square shows.
    edge = np.clip((c - np.hypot(dx, dy)) / 30, 0, 1)
    intensity = np.clip(intensity * edge, 0, 1)
    rgb = np.empty((size, size, 3))
    rgb[..., 0], rgb[..., 1], rgb[..., 2] = 236, 240, 255
    alpha = (intensity**0.9) * 255
    return Image.fromarray(np.dstack([rgb, alpha]).round().astype(np.uint8), "RGBA")


# The ground's picture: as wide as the sky window, its bottom on the
# window's (tools/eclipse_show.py places it there).
GROUND_W, GROUND_H = 600, 180


def svg(body, width, height):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}">\n{body}\n</svg>\n')


def ground():
    b = GROUND_H  # the window's bottom edge
    land = (f"M 0 {b - 70} C 60 {b - 84} 120 {b - 92} 190 {b - 80} "
            f"C 260 {b - 68} 300 {b - 62} 360 {b - 72} C 430 {b - 84} 520 {b - 96} {GROUND_W} {b - 78} "
            f"V {b} H 0 Z")
    tree = (f"M 96 {b - 84} V {b - 110} "
            f"C 70 {b - 112} 66 {b - 142} 84 {b - 150} C 84 {b - 172} 112 {b - 176} 118 {b - 158} "
            f"C 138 {b - 156} 140 {b - 124} 120 {b - 112} C 112 {b - 108} 104 {b - 108} 102 {b - 110} V {b - 84} Z")

    def person(x, base, height, lean):
        head = height * 0.16
        top = base - height
        body = (f"M {x - height * 0.13} {base} L {x - height * 0.11 + lean * 0.5} {top + head * 2.2} "
                f"Q {x + lean * 0.5} {top + head * 1.7} {x + height * 0.11 + lean * 0.5} {top + head * 2.2} "
                f"L {x + height * 0.13} {base} Z")
        return (f'<circle cx="{round(x + lean, 1)}" cy="{round(top + head, 1)}" r="{round(head, 1)}" fill="#151924"/>'
                f'<path d="{body}" fill="#151924"/>')

    return svg(f'<path d="{land}" fill="#1B2230"/><path d="{tree}" fill="#1B2230"/>'
               + person(452, b - 82, 34, -3) + person(476, b - 84, 28, -2), GROUND_W, GROUND_H)


# The continent's picture: its left edge on the Earth's, which the show
# places 128 px left of the Earth's centre and 52 px above it.
def continent():
    return svg('<path d="M 2 12 C 18 2 32 22 24 42 C 16 62 32 82 18 112 L 2 112 Z" fill="#9DB98A"/>', 34, 114)


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    corona().save(out / "corona.png")
    (out / "ground.svg").write_text(ground())
    (out / "continent.svg").write_text(continent())


if __name__ == "__main__":
    main()
