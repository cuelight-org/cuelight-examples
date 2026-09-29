#!/bin/sh
# Fetch the chip shop board's fonts, with their licenses.
#
#     tools/chip_shop_fetch.sh
#
# Bebas Neue for the headings and Barlow Semi Condensed for the items
# and the ticker, both OFL 1.1 with no reserved font name, from
# google/fonts, as they come.
set -eu

out=$(dirname "$0")/../chip_shop
mkdir -p "$out/assets/fonts" "$out/licenses"
fonts=https://raw.githubusercontent.com/google/fonts/main/ofl

fetch() {
  curl -sfL -o "$out/assets/fonts/$2" "$fonts/$1/$2"
}
fetch bebasneue BebasNeue-Regular.ttf
fetch barlowsemicondensed BarlowSemiCondensed-Bold.ttf
fetch barlowsemicondensed BarlowSemiCondensed-BoldItalic.ttf

curl -sfL -o "$out/licenses/BebasNeue-OFL.txt" "$fonts/bebasneue/OFL.txt"
curl -sfL -o "$out/licenses/BarlowSemiCondensed-OFL.txt" "$fonts/barlowsemicondensed/OFL.txt"
