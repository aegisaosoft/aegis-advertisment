# -*- coding: utf-8 -*-
"""Write the subtitle file for each cut.

    python srt.py

LinkedIn plays video muted in the feed, so for most of the audience the subtitles
are the film. These carry the same words at the same seconds as the burnt-in caption
— both come from the timeline the recording produced — so uploading the .srt adds a
selectable, searchable track without contradicting the picture.

End times follow the clip, not the next cue: a line stays up for as long as it is
being spoken and then goes, rather than hanging on through the silence.
"""
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def stamp(seconds):
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return '%02d:%02d:%02d,%03d' % (h, m, s, ms)


def duration(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                          '-of', 'csv=p=0', path], capture_output=True, text=True)
    return float(out.stdout.strip())


for lang in (sys.argv[1:] or ['en', 'es']):
    film = os.path.join(HERE, 'film.%s.html' % lang)
    if not os.path.exists(film):
        sys.exit('no film.%s.html — run build.py first' % lang)
    html = io.open(film, encoding='utf-8').read()
    timeline = json.loads(re.search(r'var FILM = (\{.*?\});\n', html, re.S).group(1))

    lines = []
    for i, cue in enumerate(timeline['cues'], 1):
        clip = os.path.join(HERE, 'audio', lang, '%s.mp3' % cue['id'])
        end = cue['t'] + duration(clip) + 0.25
        lines += [str(i), '%s --> %s' % (stamp(cue['t']), stamp(end)), cue['text'], '']

    out = os.path.join(HERE, 'mp4', 'myeztoll-four-twelve-%s.srt' % lang)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    # UTF-8 with a BOM: several players, LinkedIn's included, mis-read accented
    # characters in a plain UTF-8 .srt.
    io.open(out, 'w', encoding='utf-8-sig').write('\n'.join(lines))
    print('%s  %d lines  %s' % (lang, len(timeline['cues']), os.path.basename(out)))
