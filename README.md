# MyEZToll — advertising films

The advertising for [MyEZToll](https://myeztoll.com), a platform that recovers tolls and
camera violations for rental fleets: the films themselves, the scripts they were read
from, and the build that assembles them.

Copyright © 2026 Alexander Orlov / Aegis AO Soft LLC. All rights reserved. Published so
the work can be looked at, linked to and quoted; it is not licensed for reuse. Sold and
operated under licence by Aegis AG Soft LLC.

## What is here

### The current film — *Four-Twelve* (1:37)

An animated short, narrated in English and in Mexican Spanish over the same picture. It
is the film on [myeztoll.com/film](https://myeztoll.com/film), and it is what the
subtitle files and the social copy in this repository belong to.

| | |
|---|---|
| `build/toonbee/script.py` | The fourteen spoken lines, both languages, and the scene grid they are cut against |
| `build/toonbee/tts.py` | Records the narration, one clip per scene, and refuses a take that overruns its scene |
| `build/toonbee/assemble.py` | Lays the clips onto the scene grid and matches the loudness |
| `build/toonbee/stt.py`, `align.py`, `make_captions.py` | Word-level timings, and the captions built from the script rather than from a transcription |
| `build/toonbee/pricecard.{html,js}` | The price list of scene 10, drawn |
| `build/toonbee/splice_scene10.sh` | Composites it over the generated shot |
| `build/short45/endcard{,.es}.html` | The closing card |
| `build/toonbee/append_endcard.sh` | Puts that card on the end |
| `myeztoll-toonbee-{en,es}.{srt,vtt}` | Subtitles, in both formats |
| `social/linkedin-posts.md` | The advertising copy written for it |

The picture is generated; the lettering is not. Every frame in this film that has to be
read — the closing card, the price list — is drawn as HTML and composited in, because
the generator cannot letter. See *What the generator gets wrong* below.

### The earlier films — *Two Minutes on Your Fleet* (2:04, six languages)

One folder per language, each a self-contained HTML document that plays itself: scenes,
subtitles and narration all run off a single clock. Open any `two-minutes.html` straight
in a browser — no server, no build step, nothing fetched but a font stylesheet.

```
en/  two-minutes.html   Two Minutes on Your Fleet
es/  two-minutes.html   Dos Minutos con Su Flota
fr/  two-minutes.html   Deux Minutes sur Votre Flotte
pt/  two-minutes.html   Dois Minutos com Sua Frota
de/  two-minutes.html   Zwei Minuten mit Ihrer Flotte
ru/  two-minutes.html   Две Минуты о Вашем Парке
```

`narration/` holds one script per voice track, with line IDs and time budgets — the same
brief a human voice artist would be handed. `screens/` holds the cropped, redacted
product screenshots that version uses, the interface in that language.

These were replaced on the site by the animated film and are kept here as the work they
are. Narration is spoken by the voice pack installed on the viewer's own machine, so
nothing about a viewing leaves it; on a device without that language installed the film
plays with subtitles only.

### Releases

The finished mp4s are attached to the releases rather than committed. They run 60–90 MB
each and are rebuilt from what is here, and a clone should not cost that to read a build
script.

## What the generator gets wrong

The animated film is machine-generated, and generated lettering drifts. Three passes
were needed, and the notes are worth keeping for anyone doing the same:

* **It cannot spell.** The price discs in scene 10 first came out reading "5tv" and
  "3s"; regenerated, the discs were clean but nonsense text orbited them. That scene is
  now drawn (`pricecard.html`) and composited over the generated one.
* **It animates numbers that should hold still.** The week's total counted itself down
  inside its own shot — $412.68 → 412.53 → 412.43 — and the crossing count with it. The
  fix was to stop that shot moving at all.
* **Cuts are dissolves.** Scene 10 dissolves in until 64.25s and out between 70.10s and
  70.30s, and the lettering being covered is on screen to the end of the outgoing
  dissolve. A patch that fades out any earlier shows what it is covering.

## Captions are built from the script, never from the audio

Transcription mishears exactly the words that matter. Fed this film, it produced "My
easy toll" for MyEZToll, "Easy Pass" for E-ZPass, "that cantry" for "that gantry", and
$412.00 for $412.68.

So `make_captions.py` takes the words from the script and only the *timings* from
speech-to-text, matching the two with an edit-distance alignment. A misheard word costs
that word's timing and never reaches the caption. Lines are then cut into cards at the
sentence breaks the script already has and balanced so no card is left an orphan.

The one platform where this cannot be used is LinkedIn: it transcribes the audio itself
and offers only a row editor over the result. Anything published there needs those rows
corrected by hand against the `.srt` in this repository.

## Three traps in the six-language films

**Plates.** `build/build_shots_lang.py` blurs the plate and transponder columns of every
screenshot unconditionally, and must keep doing so — several source captures ship them
fully readable. The capture tool is the real place to fix this: the same unredacted
images go into the user guides for all eight languages, not only here.

**Figures.** Each locale was captured on a different day, so the numbers on screen
genuinely differ: $100.89 over 15 crossings in es/fr/pt, $182.41 over 25 in de/ru.
The narration quotes whatever that locale's screen shows, and `FIGURES` at the top of
`build/localize.py` records them.

This bites hardest in the tracks that ride along. Each localised cut carries English —
and Russian — subtitles lifted from the English film, and for a long time they narrated
*its* figures: every non-English cut said "four hundred and twelve dollars, across
thirty-nine crossings" over a screen showing something else. `localize.py` now re-says
that one cue per locale, and stops the build if the English cut is re-worded and the
anchor stops matching.

**A blank map.** One capture caught the fleet map before its tiles loaded — a grey pane.
The builder detects it (the file comes out under 20 KB) and borrows the English capture,
which is safe because a map carries no interface text.

## The claim these films make

Free for the fleet owner: no subscription, no set-up fee, nothing per vehicle, and
connecting a GPS the owner already runs costs nothing either. Tolls and violations are
collected from the renter who incurred them, and the owner is paid the toll in full plus
a share of the fee charged to that renter.

The one exception — stated on screen and in the narration both — is our own telematics
hardware, an optional paid module. Keep that exception in any edit: a "free" claim with
the exception quietly removed is the only thing here that would be a lie.
