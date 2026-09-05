# -*- coding: utf-8 -*-
"""Give the already-built cuts an adult narrator.

The films speak with the voice pack on the viewer's own machine, and two settings
were making that read like a child: a default pitch of 1.14 (the slider's own label
says "higher reads younger"), and a voice ranking that put Microsoft's en-GB
"Maisie" and en-US "Ana" first — both of which are child voices. A film about what
a fleet loses to tolls cannot be narrated by a little girl.

`voice_defaults.py` holds the change and is applied by the two builders, so a rebuild
keeps it. This script applies the same edits to the six cuts already in the language
folders, which cannot be rebuilt here (the engine source and the screenshot crops
were withdrawn from this folder).

    python set_adult_narrator.py            # apply
    python set_adult_narrator.py --check    # report only, change nothing

Idempotent: a second run reports nothing to do. It does not touch a recorded
voice-over — that is `embed_audio.py`, and a recorded clip always wins over the
synthesised voice anyway.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voice_defaults import adult_narrator, pitch_markup  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ['en', 'es', 'fr', 'pt', 'de', 'ru']

check_only = '--check' in sys.argv[1:]
changed, failures = [], []

for lang in LANGS:
    path = os.path.join(ROOT, lang, 'two-minutes.html')
    if not os.path.exists(path):
        failures.append('%s: no film at %s' % (lang, path))
        continue

    before = io.open(path, encoding='utf-8').read()
    try:
        # The whole file goes through both: the player JS and the slider markup live
        # in the same document once the film is assembled.
        after = pitch_markup(adult_narrator(before, lang), lang)
    except SystemExit as exit_reason:
        failures.append(str(exit_reason))
        continue

    if after == before:
        continue
    changed.append(lang)
    if not check_only:
        io.open(path, 'w', encoding='utf-8').write(after)

for lang in changed:
    print(('would fix  ' if check_only else 'fixed      ') + '%s/two-minutes.html' % lang)
if not changed:
    print('nothing to do — every cut already narrates as an adult woman.')

if failures:
    print('\nfailures:')
    for failure in failures:
        print('  - ' + failure)
    sys.exit(1)
