# red_riding_hood

A picture book for children learning to read, on a 1280x720 canvas:
Little Red Riding Hood told in short lines of large type, an open book
on a wooden table, the story on the left page and a picture on the right.
The pictures never stand quite still: grass and flowers sway, the girl's
head bobs, smoke rises, a bird hops on the roof, the wolf blinks and wags
its tail.

One word on every page is printed red, and it makes the picture do
something: the girl twirls in her red hood, the basket swings, the wolf
hops, the flowers bob, Grandma peeks out of the cupboard, the wolf's eyes
grow and it shows its teeth, the candles on the cake flare up. Pressing
the word does it.

| Part | How it works |
| --- | --- |
| Pages | every spread is a scene (`cover`, `page_1` ... `page_8`), entered by its trigger. The table, the cover boards and the edges of the pages are the show's own layers and stay put; everything printed on the pages belongs to the scene |
| Turning the page | a dog-ear at the bottom outer corner of each page: the right one turns forward, the left one back (`press`). The corner is folded over its diagonal, showing the page beneath and the back of the flap, breathes a little so a young reader finds it and lifts further under the pointer (`input.pointer.under`, a binding that maps the corner's pressable pieces to a bigger `scale`), and an unseen square around it presses too, so a hand that misses the fold by a bit still turns the page; nowhere else on the page does, so a hand hunting for the red word cannot turn it by accident. ArrowRight, PageDown and Space turn forward, ArrowLeft and PageUp back, Home to the cover (`input.keys`). Each spread routes `next` and `prev` to its neighbours |
| Page turn | every spread is entered two ways, by its own trigger turning forward and by `<name>_back` from the spread after it turning back. Forward, a blank leaf over the right page turns on the spine (`scale_x` from 1 to -1), shading as it lifts, lands on the left page and fades into the new text, which only appears then. Back, the mirror image: the left page lifts, lands on the right and fades into the new picture. The sound of a page turning plays with either, one of two takes in turn (`pick`) |
| Paper | one PNG multiplied over both pages and the turning leaf: grain, darker edges, foxing and a deep crease where the pages bend into the binding, so the ink and the pictures look printed on it |
| Story | IM Fell English at 40 pixels, a line per layer; a page that starts with a letter gets a red initial in IM Fell French Canon, with the first two lines indented beside it |
| Red words | the lines are laid out by the script, word by word, with the font's advance widths, which is how the engine places glyphs, so each red word is a text layer of its own at a known place. It is anchored at its centre and jumps when its trigger fires; a press on it fires the same trigger (`press`). Under the pointer a red line draws in beneath it from the left, a shape whose `scale_x` is mapped from what is under the pointer |
| Pictures | a group clipped to the plate, drawn from SVGs in a few flat inks with a dark outline. Scenery that moves is its own file, drawn so that the point it turns around is on its box's edge: the big basket swings from its handle (`anchor: top`), a flower sways from its stem (`bottom`) |
| Idle motion | looping timelines, each with its own period and delay, so nothing moves in step with anything else |
| Characters | Red and the wolf are one SVG each, one image layer on the page, and their moving pieces are elements of it with an id that the layer moves as `parts`, around a `pivot` in the artwork's coordinates: her head bobs at her neck and her basket sways from her hand; the wolf's tail wags from its root, its head tilts at its neck and carries its jaw, which opens at its hinge, and its eye, which blinks and grows. Red with empty hands (`red_empty_handed.svg`) and the wolf in Grandma's bed, only its head, in her nightcap (`wolf_as_grandma.svg`), are pictures of their own with the same parts in the same places, so the same timelines move them; the wolf in bed is mirrored to face the room |

## Running

```sh
cd ../../../cuelight
cargo run -p cuelight-player -- ../cuelight-examples/demos/red_riding_hood
```

There is no driver: the book opens on its cover and waits for its
reader. Press the folded corner of the right-hand page to turn it, the
left one to turn back, and click a red word to make its picture move; or
from the player's prompt, `page_6` and `tap_eyes`.

The show and the artwork are written by
[`tools/red_riding_hood_show.py`](../../tools/red_riding_hood_show.py) and
[`tools/red_riding_hood_art.py`](../../tools/red_riding_hood_art.py); the
page turns by
[`tools/red_riding_hood_sounds.py`](../../tools/red_riding_hood_sounds.py);
the fonts are fetched by
[`tools/red_riding_hood_fetch.sh`](../../tools/red_riding_hood_fetch.sh).

## Assets

Everything under `assets/` is committed and free to redistribute. Licenses
were checked at the linked sources on 2026-09-24; the license texts that
have to travel with the files are in [`licenses/`](licenses/).

| Asset | Origin | License |
| --- | --- | --- |
| `*.svg`, `table.png`, `paper.png` | Made for this show, written by [`tools/red_riding_hood_art.py`](../../tools/red_riding_hood_art.py): the backdrops and scenery, the other characters, and Red and the wolf as one picture each (`red.svg`, `wolf.svg`) whose moving pieces are elements with an id, hidden where a page leaves them out | MIT, as this repository |
| `sounds/turn1.ogg`, `sounds/turn2.ogg` | Synthesized from noise by [`tools/red_riding_hood_sounds.py`](../../tools/red_riding_hood_sounds.py) | MIT, as this repository |
| `fonts/IMFellEnglish-Regular.ttf`, `fonts/IMFellEnglish-Italic.ttf`, `fonts/IMFellFrenchCanon-Regular.ttf` | [IM Fell Types](https://iginomarini.com/fell/) by Igino Marini, revivals of the Fell types of the 1680s, the unmodified files from [google/fonts](https://github.com/google/fonts/tree/8d618a0e96499047423510abb2c5ee9f475b987a/ofl/imfellenglish) and [IM Fell French Canon](https://github.com/google/fonts/tree/3b3145a92153418d09d62971e8238ad5bec48ca3/ofl/imfellfrenchcanon) | [OFL-1.1](licenses/IMFell-OFL.txt), no reserved font name |

The story is the folk tale, retold for young readers; in this telling
Grandma hides in the cupboard and nobody gets eaten.

## What would make it better

- Reading along: narration whose sound carries a marker per word that
  fires a trigger, so each word lights up as it is read aloud.
- Transitions between scenes: the page turn is played by the new scene
  over its own content, so the old page cannot be seen turning away.
- Laying out text in the engine: to know where a word lands, the script
  measures the font itself, and a line with a red word in it is several
  layers.
- Styles and repeated layers (cuelight#99): every page repeats the same
  paper, frame, leaf and rustle, and the characters are copied onto every
  page they appear on.
