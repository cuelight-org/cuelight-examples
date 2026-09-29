# The chip shop

A menu board over the counter of a chip shop: three landscape screens side
by side, driven as one wide picture. The boards are laid out per screen,
fries and drinks on the first, snacks across the second and third, burgers
and the house dishes on the third, and a ticker of the day's news runs
along the bottom of all three, through the bezels.

The show is one 5760 x 1080 canvas. Each screen is a group at `x` 0, 1920
and 3840 holding its own boards, so a screen's layout is written in its
own coordinates; the chalkboard behind them is one small texture tiled
per screen, and the ticker is one text layer whose `x` runs from the
right edge of the third screen to past the left edge of the first, over
and over.

## How signage does this

A player computer with three outputs shows one wide surface, either
because the compositor or the graphics driver joins the outputs into one
and the player draws one window on it, or because the player opens one
window per output and draws each its part of the canvas.

On Linux the first is a kiosk compositor's job. [cage](https://github.com/cage-kiosk/cage)
in extend mode arranges the outputs side by side and gives its one
application a window across all of them:

```sh
cage -m extend -- cuelight-player chip_shop
```

The player gets a 5760 x 1080 window and fits the show into it as it
fits any window. For a wall that runs all day, `--fps` caps the frames
drawn a second: `cuelight-player chip_shop --fps 30`. Other wlroots compositors do the same with a rule that
places and sizes the window. A desktop compositor that will not let a
window span outputs needs the second way, one window per screen, which
the player does not have yet (cuelight#257, on the presented view of
cuelight#245). Until then the website shows the whole canvas scaled to
fit, and `cuelight-render` renders it whole.

## Regenerating

```sh
tools/chip_shop_fetch.sh   # the fonts, from Google Fonts
tools/chip_shop_art.py     # the chalkboard texture and the icons
tools/chip_shop_show.py    # show.json
```

The menu, the prices and the headlines are in `tools/chip_shop_show.py`;
the headlines are made up.

## Assets

| Asset | Origin | License |
| --- | --- | --- |
| `fonts/BebasNeue-Regular.ttf` | [Bebas Neue](https://github.com/dharmatype/Bebas-Neue) by Dharma Type, from [Google Fonts](https://github.com/google/fonts/tree/main/ofl/bebasneue) | [OFL-1.1](licenses/BebasNeue-OFL.txt), no reserved font name |
| `fonts/BarlowSemiCondensed-*.ttf` | [Barlow](https://github.com/jpt/barlow) by Jeremy Tribby, from [Google Fonts](https://github.com/google/fonts/tree/main/ofl/barlowsemicondensed) | [OFL-1.1](licenses/BarlowSemiCondensed-OFL.txt), no reserved font name |
| `chalk.png`, `leaf.svg`, `flame.svg`, `fish.svg`, `drumstick.svg` | Made for this show by [`tools/chip_shop_art.py`](../tools/chip_shop_art.py) | MIT, as this repository |
