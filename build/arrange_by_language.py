"""Lay the advertising films out one folder per language.

Each language folder holds the films that lead in that language, the recording
script for every voice track they contain, and the screenshots they use.
"""
import io
import os
import re
import shutil

SCRATCH = os.path.dirname(os.path.abspath(__file__))
DEST = r'C:\aegis-aa\aegis-advertisment'

LANG_NAME = {'en': 'English', 'es': 'Spanish', 'fr': 'French', 'pt': 'Portuguese',
             'de': 'German', 'ru': 'Russian'}

# film file -> (language folder, name inside it, human title)
FILMS = [
    ('two-minutes-on-your-fleet.html', 'en', 'two-minutes.html', 'Two Minutes on Your Fleet'),
    ('two-minutes.es.html',            'es', 'two-minutes.html', 'Dos Minutos con Su Flota'),
    ('two-minutes.fr.html',            'fr', 'two-minutes.html', 'Deux Minutes sur Votre Flotte'),
    ('two-minutes.pt.html',            'pt', 'two-minutes.html', 'Dois Minutos com Sua Frota'),
    ('two-minutes.de.html',            'de', 'two-minutes.html', 'Zwei Minuten mit Ihrer Flotte'),
    ('two-minutes.ru.html',            'ru', 'two-minutes.html', 'Две Минуты о Вашем Парке'),
]

CUE_LANGS = re.compile(r'\b(en|es|fr|pt|de|ru):"((?:[^"\\]|\\.)*)"')


def parse_scenes(html):
    """chapters, durations and every cue with all its language variants."""
    body = html[html.index('  var SCENES = ['):html.index('  var TOTAL =')]
    scenes, cur, cue = [], None, None
    for line in body.splitlines():
        m = re.match(r'\s*\{ chapter:"([^"]+)", dur:([0-9.]+),', line)
        if m:
            if cur:
                scenes.append(cur)
            cur = {'chapter': m.group(1), 'dur': float(m.group(2)), 'cues': []}
        t = re.match(r'\s*\{t:([0-9.]+),', line)
        if t and cur is not None:
            cue = {'t': float(t.group(1))}
            cur['cues'].append(cue)
        if cue is not None:
            for lg, txt in CUE_LANGS.findall(line):
                cue[lg] = txt
    if cur:
        scenes.append(cur)
    return scenes


def write_script(scenes, lang, title, path):
    total = sum(s['dur'] for s in scenes)
    out = ['# %s — %s narration' % (title, LANG_NAME[lang]), '',
           'Runtime %d:%02d. One audio file per line, named exactly by its ID '
           '(`0-0.mp3`, `0-1.mp3`, …).' % (int(total // 60), int(total % 60)),
           'Stay inside the time budget — the visuals are cut to it.', '']
    n = 0
    for si, sc in enumerate(scenes):
        out.append('## Scene %d — %s (%.0fs)' % (si + 1, sc['chapter'], sc['dur']))
        out.append('')
        for ci, cue in enumerate(sc['cues']):
            nxt = sc['cues'][ci + 1]['t'] if ci + 1 < len(sc['cues']) else sc['dur']
            text = cue.get(lang)
            if not text:
                continue
            out.append('**%d-%d** _(max %.1fs)_' % (si, ci, nxt - cue['t']))
            out.append('')
            out.append('> ' + text)
            out.append('')
            n += 1
    io.open(path, 'w', encoding='utf-8').write('\n'.join(out))
    return n


def main():
    # start clean so a re-run cannot leave withdrawn films or stale scripts behind
    for name in ('films', 'narration', 'en', 'es', 'fr', 'pt', 'de', 'ru'):
        p = os.path.join(DEST, name)
        if os.path.isdir(p):
            shutil.rmtree(p)

    index = {}
    for src, lang, name, title in FILMS:
        folder = os.path.join(DEST, lang)
        os.makedirs(os.path.join(folder, 'narration'), exist_ok=True)
        html = io.open(os.path.join(SCRATCH, src), encoding='utf-8').read()
        shutil.copy(os.path.join(SCRATCH, src), os.path.join(folder, name))

        scenes = parse_scenes(html)
        langs = sorted({k for s in scenes for c in s['cues'] for k in c if k != 't'})
        stem = name[:-5]
        made = []
        for lg in langs:
            path = os.path.join(folder, 'narration', '%s.%s.md' % (stem, lg))
            cnt = write_script(scenes, lg, title, path)
            made.append('%s(%d)' % (lg, cnt))
            # a film's own foreign-language track belongs with that language too
            if lg != lang and lg in LANG_NAME:
                other = os.path.join(DEST, lg, 'narration')
                os.makedirs(other, exist_ok=True)
                shutil.copy(path, os.path.join(other, '%s.from-%s.%s.md' % (stem, lang, lg)))
        index.setdefault(lang, []).append((name, title, made))
        print('%-4s %-38s tracks: %s' % (lang, name, ' '.join(made)))

    # screenshots next to the film that uses them
    for lang, srcdir in [('en', 'shots'), ('es', 'shots_es'), ('fr', 'shots_fr'),
                         ('pt', 'shots_pt'), ('de', 'shots_de'), ('ru', 'shots_ru')]:
        s = os.path.join(SCRATCH, srcdir)
        if os.path.isdir(s):
            d = os.path.join(DEST, lang, 'screens')
            if os.path.isdir(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)

    # shared tooling
    build = os.path.join(DEST, 'build')
    os.makedirs(build, exist_ok=True)
    for f in ['localize.py', 'build_shots_lang.py', 'build_shots.py', 'build_shots_es.py',
              'assemble_2min.py', 'make_es.py', 'two_min_shell.html', 'patch_audio.py',
              'wire_cues.py', 'tts_generate.py', 'embed_audio.py', 'make_test_clips.py',
              'arrange_by_language.py']:
        p = os.path.join(SCRATCH, f)
        if os.path.exists(p):
            shutil.copy(p, os.path.join(build, f))
    src_readme = os.path.join(SCRATCH, 'README_narration.md')
    if os.path.exists(src_readme):
        shutil.copy(src_readme, os.path.join(build, 'README_narration.md'))

    print('\nlayout:')
    for lang in ['en', 'es', 'fr', 'pt', 'de', 'ru']:
        p = os.path.join(DEST, lang)
        if os.path.isdir(p):
            films = [f for f in os.listdir(p) if f.endswith('.html')]
            scripts = os.listdir(os.path.join(p, 'narration')) if os.path.isdir(os.path.join(p, 'narration')) else []
            print('  %-3s %d film(s), %d recording script(s)' % (lang, len(films), len(scripts)))


main()
