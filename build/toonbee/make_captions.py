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
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import align
import script

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = r'C:\aegis-aa\aegis-advertisment'

lang = sys.argv[1] if len(sys.argv) > 1 else 'en'
lines = script.LANGS[lang]

# A language nobody records is captioned off the reading the film actually carries.
# The words differ, so there is nothing to align; what carries over is when each line
# is spoken, measured on the language whose voice is in the file.
heard_in = script.SUBTITLED.get(lang, lang)
words = os.path.join(HERE, '%s.words.json' % heard_in)

timing, hit, want = align.spans(script.LANGS[heard_in], words)
for n, ((a, b), (s0, s1)) in enumerate(zip(timing, script.grid()), 1):
    if not (s0 - 0.5 <= a <= s1):
        sys.exit('line %d starts at %.2fs, outside its scene (%.2f-%.2f)' % (n, a, s0, s1))
    if hit[n - 1] < 0.5 * want[n - 1]:
        sys.exit('line %d: only %d of %d words were heard' % (n, hit[n - 1], want[n - 1]))

# Where each line really is: the scene it was placed in, plus the length of the clip
# recorded for it. Passing this in stops an interpolated word time from walking a
# caption into the shot before it — which is what the Chinese cut did.
def clip_seconds(n):
    """Length of the clip recorded for scene n, or None if we did not record it.

    English is the one language we never recorded: its narration is ToonBee's own,
    inside the export. There the scene itself is the bound, which is looser but still
    keeps a caption out of the neighbouring shot.
    """
    path = os.path.join(HERE, 'audio', heard_in, '%02d.mp3' % n)
    if not os.path.exists(path):
        return None
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                          '-of', 'csv=p=0', path], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        return None


bounds = []
for n, (start, end) in enumerate(script.grid()):
    spoken = clip_seconds(n + 1)
    bounds.append((start + script.LEAD,
                   start + script.LEAD + spoken if spoken else end))

cues = (align.borrowed_cues(lines, timing) if lang in script.SUBTITLED
        else align.cues(lines, words, bounds=bounds))
for name, write in (('srt', align.write_srt), ('vtt', align.write_vtt)):
    path = os.path.join(OUT, 'myeztoll-toonbee-%s.%s' % (lang, name))
    if name == 'srt':
        write(path, [t for t, _, _ in cues], [(a, b) for _, a, b in cues])
    else:
        write(path, cues)
    print('wrote %s' % path)
print('%d lines in %d cues, %.2fs .. %.2fs, %d of %d words heard'
      % (len(timing), len(cues), cues[0][1], cues[-1][2], sum(hit), sum(want)))
