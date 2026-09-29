#!/usr/bin/env python3
"""Draw the chip shop board's artwork into chip_shop/assets/.

    tools/chip_shop_art.py

chalk.png is a 480x270 blue-grey chalkboard with smudges and grain, drawn
at a quarter of a screen and stretched by the show (a texture, not a
picture, so the blur is the point). The icons beside the prices are
written as small SVGs: a leaf (vegetarian), a flame (spicy), a fish and a
drumstick. Needs numpy and Pillow.
"""

from pathlib import Path

import numpy as np
from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "chip_shop" / "assets"


def noise(rng, size, cells):
    """Smooth noise: a small random grid stretched up to `size`."""
    small = rng.random((cells[1], cells[0]), dtype=np.float32)
    return np.asarray(Image.fromarray(small * 255).resize(size, Image.BICUBIC), dtype=np.float32) / 255


def chalk(width=480, height=270, seed=7):
    rng = np.random.default_rng(seed)
    base = np.array([24, 34, 50], dtype=np.float32)
    smudge = np.array([120, 140, 170], dtype=np.float32)
    # Broad smudges, some finer ones, and grain.
    blot = 0.55 * noise(rng, (width, height), (6, 4)) + 0.3 * noise(rng, (width, height), (24, 14)) \
        + 0.15 * noise(rng, (width, height), (96, 54))
    blot = np.clip((blot - 0.42) * 1.6, 0, 1) ** 1.6
    grain = rng.normal(0, 0.035, (height, width)).astype(np.float32)
    mix = np.clip(blot * 0.55 + grain, 0, 1)[..., None]
    rgb = base * (1 - mix) + smudge * mix
    # Darker at the very edges, as a board in a frame is.
    y, x = np.mgrid[0:height, 0:width]
    edge = np.minimum(np.minimum(x, width - x), np.minimum(y, height - y)) / 40
    rgb *= np.clip(0.6 + 0.4 * edge, 0, 1)[..., None]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


ICONS = {
    "leaf": ("#4ADE80", "M15 2 C6 4 3 12 4 20 C6 28 13 29 16 28 C13 24 12 18 15 12 C13 18 15 24 18 26 C26 22 28 12 15 2 Z"),
    "flame": ("#FF6B3D", "M15 2 C17 8 22 10 22 17 C22 22 19 26 15 27 C11 26 8 22 8 17 C8 13 10 10 12 9 C11 13 13 15 15 15 C18 12 16 6 15 2 Z"),
    "fish": ("#5FB8FF", "M3 15 C8 8 15 7 20 11 L27 6 L25 15 L27 24 L20 19 C15 23 8 22 3 15 Z M18 14 A1.6 1.6 0 1 0 18 14.1 Z"),
    "drumstick": ("#F4A261", "M4 26 L9 21 C6 16 8 10 13 8 C18 6 24 8 26 13 C27 18 23 22 18 22 C15 22 13 21 11 23 L6 28 Z"),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    chalk().save(OUT / "chalk.png", optimize=True)
    for name, (fill, path) in ICONS.items():
        (OUT / f"{name}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 30 30">'
            f'<path d="{path}" fill="{fill}"/></svg>\n'
        )


if __name__ == "__main__":
    main()
