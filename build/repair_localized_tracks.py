# -*- coding: utf-8 -*-
"""One-off repair of the localised cuts that were built before localize.py was fixed.

Two defects, both in the tracks that ride along rather than in the film's own
language, and both now fixed at the source in `localize.py`:

1. **The money cue quoted the English cut's figures.** Every localised film carries
   the English subtitle track (and the Russian one, unless it is the Russian cut),
   lifted verbatim from the English film — which was captured on another day, off
   other screens. So the Spanish film showed $100.89 over fifteen crossings while
   its English subtitle said "four hundred and twelve dollars, across thirty-nine
   crossings". The film's own track was always right.

2. **The subtitle picker offered languages the file does not have.** The picker was
   built as `<locale>, en, ru` regardless of the cut, so the Russian film listed
   "RU" twice and no Spanish, while `?lang=` still advertised `es` — a link with
   `?lang=es` on that film showed blank captions. Its fineprint claimed an ES track
   too.

Run once, from this folder:

    python repair_localized_tracks.py            # repair in place
    python repair_localized_tracks.py --check     # report only, change nothing

It rewrites the six `<lang>/two-minutes.html` and the recording scripts under
`<lang>/narration/`, and is idempotent — a second run reports nothing to do.
localize.py is the source of truth for all of this; the tables below are copied
here only because this script has to run without re-running a build whose inputs
(the English engine and the per-locale screenshot crops) are not in this folder.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ['en', 'es', 'fr', 'pt', 'de', 'ru']

# The money cue as the English cut says it, in both tracks that ride along.
EN_MONEY_CUE = 'Four hundred and twelve dollars, across thirty-nine crossings.'
RU_MONEY_CUE = 'Четыреста двенадцать долларов за тридцать девять проездов.'

# Per film: the same figures said aloud, read off that locale's own screenshots.
# `en` is the English cut and quotes the English screens, so it needs no repair.
SPOKEN = {
    'es': {'en': 'One hundred dollars and eighty-nine cents, across fifteen crossings.',
           'ru': 'Сто долларов восемьдесят девять центов за пятнадцать проездов.'},
    'fr': {'en': 'One hundred dollars and eighty-nine cents, across fifteen crossings.',
           'ru': 'Сто долларов восемьдесят девять центов за пятнадцать проездов.'},
    'pt': {'en': 'One hundred dollars and eighty-nine cents, across fifteen crossings.',
           'ru': 'Сто долларов восемьдесят девять центов за пятнадцать проездов.'},
    'de': {'en': 'One hundred and eighty-two dollars and forty-one cents, across twenty-five crossings.',
           'ru': 'Сто восемьдесят два доллара сорок один цент за двадцать пять проездов.'},
    'ru': {'en': 'One hundred and eighty-two dollars and forty-one cents, across twenty-five crossings.',
           'ru': 'Сто восемьдесят два доллара сорок один цент за двадцать пять проездов.'},
}

ANCHOR = {'en': EN_MONEY_CUE, 'ru': RU_MONEY_CUE}

SUB_LABELS = {'en': 'Subtitles · EN', 'es': 'Subtítulos · ES', 'fr': 'Sous-titres · FR',
              'pt': 'Legendas · PT', 'de': 'Untertitel · DE', 'ru': 'Субтитры · RU'}

# The one cut whose fineprint named a track it does not carry.
FINEPRINT = {'ru': ('Озвучка и субтитры · RU · EN · ES', 'Озвучка и субтитры · RU · EN')}

check_only = '--check' in sys.argv[1:]
changes = []
failures = []


def repair_film(lang):
    path = os.path.join(ROOT, lang, 'two-minutes.html')
    if not os.path.exists(path):
        failures.append('%s: no film at %s' % (lang, path))
        return
    html = original = io.open(path, encoding='utf-8').read()
    done = []

    # 1. the money cue, in every track this cut carries but its own
    for track, spoken in SPOKEN.get(lang, {}).items():
        if track == lang:
            continue
        anchor = ANCHOR[track]
        hits = html.count('%s:"%s"' % (track, anchor))
        if hits > 1:
            failures.append('%s: %s money cue appears %d times' % (lang, track, hits))
        elif hits == 1:
            html = html.replace('%s:"%s"' % (track, anchor), '%s:"%s"' % (track, spoken), 1)
            done.append('%s cue' % track)

    # 2. the subtitle picker: this cut's own language, then the tracks it carries
    select = re.search(r'(<select[^>]*id="langSel"[^>]*>)([\s\S]*?)(</select>)', html)
    if not select:
        failures.append('%s: no #langSel picker' % lang)
        return
    # A track is only offered if its cues are really in the file. The localised cuts
    # carry en and ru; the English cut carries es as well, and keeps it.
    subs = [lang] + [code for code in ('en', 'es', 'ru') if code != lang]
    subs = [code for code in subs if re.search(r'[{,]\s*%s\s*:\s*"' % code, html)]
    options = '\n'.join('      <option value="%s">%s</option>' % (code, SUB_LABELS[code]) for code in subs)
    wanted = '%s\n%s\n    %s' % (select.group(1), options, select.group(3))
    if select.group(0) != wanted:
        html = html.replace(select.group(0), wanted, 1)
        done.append('picker → %s' % '/'.join(subs))

    # 3. ...and the ?lang= switch, held to the same list
    switch = re.search(r'/\[\?&\]lang=\(([a-z|]+)\)/i', html)
    if not switch:
        failures.append('%s: no ?lang= switch' % lang)
    elif switch.group(1) != '|'.join(subs):
        html = html.replace(switch.group(0), '/[?&]lang=(%s)/i' % '|'.join(subs), 1)
        done.append('?lang= → %s' % '|'.join(subs))

    # 4. the fineprint under the poster, where it named a track that is not there
    if lang in FINEPRINT:
        old, new = FINEPRINT[lang]
        if old in html:
            html = html.replace(old, new, 1)
            done.append('fineprint')

    if html != original:
        changes.append('%s/two-minutes.html: %s' % (lang, ', '.join(done)))
        if not check_only:
            io.open(path, 'w', encoding='utf-8').write(html)


def repair_scripts(lang):
    """The recording scripts are the film's cues in prose; they carried the same figures."""
    folder = os.path.join(ROOT, lang, 'narration')
    if not os.path.isdir(folder):
        return
    for name in sorted(os.listdir(folder)):
        # two-minutes.<track>.md is this film's track; two-minutes.from-<src>.<track>.md
        # is a copy of the <src> film's track, so it follows <src>'s figures.
        m = re.match(r'two-minutes(?:\.from-([a-z]{2}))?\.([a-z]{2})\.md$', name)
        if not m:
            continue
        film, track = (m.group(1) or lang), m.group(2)
        spoken = SPOKEN.get(film, {}).get(track)
        if not spoken or track == film:
            continue
        path = os.path.join(folder, name)
        text = io.open(path, encoding='utf-8').read()
        if ANCHOR[track] not in text:
            continue
        changes.append('%s/narration/%s: %s cue' % (lang, name, track))
        if not check_only:
            io.open(path, 'w', encoding='utf-8').write(text.replace(ANCHOR[track], spoken, 1))


for lg in LANGS:
    repair_film(lg)
    repair_scripts(lg)

for line in changes:
    print(('would fix  ' if check_only else 'fixed      ') + line)
if not changes:
    print('nothing to do — every cut already quotes its own figures and offers only the tracks it has.')

if failures:
    print('\nfailures:')
    for line in failures:
        print('  - ' + line)
    sys.exit(1)
