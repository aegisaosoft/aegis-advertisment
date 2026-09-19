# MyEZToll tutorial series

Twenty-one screen-recording tutorials for the owner portal, in English and Spanish,
1920×1080 at 30fps with a sidecar `.srt` and `.vtt` for YouTube.

```
python redact.py       # blur what the documentation capture missed (once)
python tts.py          # record the narration through ElevenLabs
python build.py        # lay each episode out around its own recording
node render.js         # render every built episode to mp4
```

Each step takes an episode number and a language to narrow it: `python tts.py 7 es`,
`node render.js 7 es`. Everything is incremental — `tts.py` skips a clip it already
has, `build.py` rewrites in seconds, and only `render.js` is slow.

---

## What it is

It looks like a screen recording of somebody using the portal, and it is not one. The
picture is a real screenshot from `docs/images/<lang>/` with a camera over it: the view
pans and zooms to whatever is being talked about, a cursor travels to the control and
clicks it, and the page cross-fades to the next screenshot the way a page load looks.

This was chosen over actually driving the live portal because a real recording would
need a live login, would risk showing another customer's data, would need re-shooting
for every UI change, and would need a second pass per language. The screenshots are
already captured for every language, already have personal data blurred, and are
already the pictures the written guide uses — so the video and the guide cannot drift
apart.

The page is a pure function of time. `window.__film.seek(t)` puts every element where
it belongs at second *t* and nothing animates itself, so `render.js` asks for frame *n*
at *n*/30s and screenshots it. A busy machine drops nothing and frame *n* is always the
same image.

## Files

| File | What it does |
|---|---|
| `model.py` | What a beat and an episode are. No content. |
| `series_a.py` … `series_h.py` | The content: every spoken line and what the screen does while it is spoken. |
| `episodes.py` | Puts the episodes in order. |
| `redact.py` | Blurs the two screens the documentation capture left personal data on. |
| `tts.py` | Records each line through ElevenLabs into `audio/<lang>/ep<NN>/`. |
| `build.py` | Measures the clips, lays out the timeline, writes `ep<NN>.<lang>.html`, the mixed `track.mp3`, and the subtitles. |
| `shell.html` | The film itself — the camera, the cursor, the spotlight, the cards. |
| `render.js` | Frame-by-frame to mp4, muxing the track. `--stills` for a handful of frames instead. |

## Writing an episode

A beat is one spoken line plus the state of the screen while it is spoken:

```python
B(en='Charges, Booking Info, View Tolls and View Violations are the read-only ones.',
  es='Cargos, Información de la reserva, Ver peajes y Ver multas son las de solo lectura.',
  shot='52-booking-row-menu', cam=(0.47, 0.660, 1.28),
  point=(0.42, 0.646), click=1.2,
  ring=(0.368, 0.592, 0.204, 0.176),
  label_en='The row menu', label_es='El menú de la fila'),
```

The **recording** decides how long a beat lasts. Writing a longer line moves the
picture rather than desynchronising it, and re-recording one line reflows the episode
around it — there are no hard-coded seconds anywhere.

`cam` is a focus point and a zoom, `point` is where the cursor goes, `click` is how many
seconds into the beat it lands, `ring` is a rectangle lit through a dimmed page.

### Coordinates

All of them are **fractions of the English capture**, never pixels.

`docs/images/en` and `docs/images/es` are the same width and laid out from the top; they
differ only in total height, because a translated footer wraps to a different number of
lines. `build.py` re-bases every vertical fraction onto the target language
automatically, so the sidebar and the header land correctly in both without being
written twice.

What does *not* transfer is a horizontal position that a longer label moves — the
language selector and Logout sit further left in Spanish. Those are written per
language:

```python
point={'en': (0.878, 0.042), 'es': (0.853, 0.042)},
```

Write a coordinate once; add the `es` form only when a still shows it landing wrong.

## Judging a change

A full render is minutes; judging is not.

```
node render.js --stills 7 20 34 60      # ep 7 at 20s, 34s and 60s, as PNGs
```

They land in `stills/`. Check Spanish separately — that is where a coordinate written
against English shows up wrong.

## Voices

Alice for English and Terry for Spanish, the same two that carry the advertising films,
so the product sounds like one company everywhere. Both are read steadier than the
advertising cut: this voice is explaining a procedure, not selling.

The API key comes from `ELEVENLABS_API_KEY`, then `HKCU\Environment`, then
`C:\aegis-aa\_elevenlabs.key.txt`.

## Redaction

`docs/tools/capture-screenshots.js --blur` hides personal data before each capture, and
as of 2026-09-06 it reaches every screen these episodes use. It did not always: it used
to leave real mobile numbers and customers' names in the Phone and Renter columns of
`94-sms-log`, and first names in the subject lines of `93-messages` ("<first name> has
sent you a message about your car"). `redact.py` blurred those again into
`shots/<lang>/`, which `build.py` prefers over `docs/images`.

That is over. The capture rules cover both screens, a DOM test holds them to it, and
all eight languages were recaptured — so `REGIONS` in `redact.py` is now empty and
`shots/` holds nothing. Every frame comes from `docs/images` directly.

Leave it that way unless a screen genuinely needs a second pass. Re-adding an entry now
would paste pixel blur over the real redaction and take the timestamps and the status
column with it — the guide reads those, and the harness deliberately leaves them sharp.

## Publishing

Upload the mp4 and attach the matching `.srt` as the caption track rather than burning
subtitles in — YouTube will then let a viewer turn them off, translate them, and search
them. The `.vtt` is the same cues for anywhere that wants WebVTT.

One playlist per language, episodes in number order. The numbering is the running order:
1 to 8 is a first week, 9 to 14 is the money, 15 to 21 is everything else.
