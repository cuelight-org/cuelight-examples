#!/usr/bin/env python3
"""Write car_dashboard's artwork: the turn signal arrow.

    tools/car_dashboard_art.py demos/car_dashboard/assets

arrow.svg points left, 72x56, in the signal green; the show mirrors it
with `scale_x` for the right-hand signal and dims it when it is off.
"""

import sys
from pathlib import Path

GREEN = "#3DDC84"


def svg(body, width, height):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}">\n{body}\n</svg>\n')


def arrow():
    return svg(f'<path d="M 0 28 L 36 0 L 36 15 L 72 15 L 72 41 L 36 41 L 36 56 Z" fill="{GREEN}"/>', 72, 56)


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    (out / "arrow.svg").write_text(arrow())


if __name__ == "__main__":
    main()
