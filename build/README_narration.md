# Voice-over for the two MyEZToll films

Both films narrate themselves today using the viewer's own browser voice. This
folder turns that into a real recorded voice-over — the same young British woman
on every machine — and keeps the picture in sync with her.

Runtime today: **A — Gantry to Payout 4:46**, **B — Stop Losing, Start Earning 3:58**.
Volume: 91 lines per language, 2 821 words / 16 835 characters across EN + ES + RU.

---

## The short version

```
setx ELEVENLABS_API_KEY "sk_..."     # new terminal after this
python tts_generate.py                # records all 273 clips
python embed_audio.py                 # embeds them and retimes both films
```

Out come `*.voiced.html` files. Hand those to Claude to publish, and the films
play the recorded voice instead of the browser's.

---

## Files

| File | What it does |
|---|---|
| `narration/script-<film>-<lang>.md` | The reading script: every line with its ID and time budget. Give this to a human voice artist. |
| `narration/script.json` | The same thing as data; both scripts below read it. |
| `tts_generate.py` | Records every line through ElevenLabs into `narration/audio/`. |
| `embed_audio.py` | Measures the clips, retimes the films to the real voice, inlines the audio. |
| `make_test_clips.py` | Silent placeholder clips, to rehearse the pipeline without paying. |

## Step 1 — record

### Option A: ElevenLabs (~$22, one month of the Creator plan)

Sign up, create an API key, then:

```
python tts_generate.py --list-voices     # see what your account offers
python tts_generate.py                   # record everything
```

The voice is set at the top of `tts_generate.py`. Default is **Lily** — young
British female. **Matilda** is the other young British option; **Alice** and
**Charlotte** read older and more formal. One multilingual voice reads all three
languages, so the brand sounds like the same person in every market.

Costs one credit per character: 16 835 credits for everything, against the
121 000 the Creator plan includes. That leaves room for six full re-records.

Re-recording one line: delete its mp3 and run the script again — everything else
is skipped.

### Option B: a human voice artist ($450–550 per film per language)

Send them `narration/script-<film>-<lang>.md`. Ask for **one file per line**,
named exactly by the ID in the script (`0-0.mp3`, `0-1.mp3`, …), and drop them
into `narration/audio/<film>/<lang>/`. Everything downstream is identical.

Budget note: a UK studio fee (£200–400/session) does **not** include usage
rights. Agree the usage separately if the film goes into paid advertising.

## Step 2 — embed and retime

```
python embed_audio.py
```

This is the part that matters. Recorded speech never lands exactly on a planned
timing, so the script:

1. measures every clip,
2. moves each subtitle cue to where the voice actually starts,
3. stretches each scene to fit its lines,
4. moves the on-screen animation with it — every visual beat is anchored to a
   cue index, not to a hard-coded second,
5. inlines the audio as `data:` URIs so the page stays self-contained.

Lines you have not recorded fall back to a word-count estimate, so a partial
recording still produces a coherent film.

**Size:** published pages must stay under 16 MB. If the three languages together
are too large, the script writes one file per language automatically
(`…voiced.en.html`, `…voiced.es.html`, `…voiced.ru.html`) — which is also what
you want if you are sending a Spanish link to Spanish buyers. Force that split
with `--per-language`.

## Step 3 — publish

Ask Claude to publish the `.voiced.html` files. Variant A and variant B keep
their existing URLs if published to the same artifact.

---

## Rehearsing without spending anything

```
python make_test_clips.py     # silent clips of plausible length
python embed_audio.py         # watch the retiming happen
```

Delete `narration/audio/` afterwards, before recording for real.

## If you skip the voice-over entirely

Nothing breaks. Without `narration/audio/`, both films keep narrating through
the browser's speech engine, and the language picker still switches subtitles
and voice between EN, ES and RU.
