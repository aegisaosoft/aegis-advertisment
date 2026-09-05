# -*- coding: utf-8 -*-
"""Write the captions for a ToonBee cut from the real script.

    python make_captions.py en
    python make_captions.py es

The words are the film's own script — the fourteen Scene Texts for English, their
US/Latin-American Spanish for the dub. The timings come from Scribe's word stamps, so
a caption cannot drift away from what was recorded and cannot inherit what a
transcriber mishears: ToonBee's own caption option is transcription-based and has
already produced "cantry" for "gantry". Each line is checked to fall inside the scene
it belongs to before anything is written.

Both .srt and .vtt come out: players and editors read the first, a <video> element on
the site reads the second.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import align
import script

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = r'C:\aegis-aa\aegis-advertisment'

lang = sys.argv[1] if len(sys.argv) > 1 else 'en'
lines = {'en': script.EN, 'es': script.ES}[lang]
words = os.path.join(HERE, '%s.words.json' % lang)

timing, hit, want = align.spans(lines, words)
for n, ((a, b), (s0, s1)) in enumerate(zip(timing, script.grid()), 1):
    if not (s0 - 0.5 <= a <= s1):
        sys.exit('line %d starts at %.2fs, outside its scene (%.2f-%.2f)' % (n, a, s0, s1))
    if hit[n - 1] < 0.5 * want[n - 1]:
        sys.exit('line %d: only %d of %d words were heard' % (n, hit[n - 1], want[n - 1]))

cues = align.cues(lines, words)
for name, write in (('srt', align.write_srt), ('vtt', align.write_vtt)):
    path = os.path.join(OUT, 'myeztoll-toonbee-%s.%s' % (lang, name))
    if name == 'srt':
        write(path, [t for t, _, _ in cues], [(a, b) for _, a, b in cues])
    else:
        write(path, cues)
    print('wrote %s' % path)
print('%d lines in %d cues, %.2fs .. %.2fs, %d of %d words heard'
      % (len(timing), len(cues), cues[0][1], cues[-1][2], sum(hit), sum(want)))
