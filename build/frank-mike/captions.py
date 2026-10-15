# -*- coding: utf-8 -*-
"""Captions for the Frank vs Mike cut, from the script rather than a transcription.

    python captions.py <text lang> [voice lang] [--srt]      (WebVTT by default)

Line n of <text lang> is shown while <voice lang>'s clip n plays, on the same timeline
build.sh lays the narration on. The voice defaults to the text's own language; Uzbek is
read over the English narration and zh-Hant over the zh one.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lines
from timeline import layout, starts

VOICE_OF = {'uz': 'en', 'zh-Hant': 'zh'}


def ts(s, sep):
    ms = int(round(s * 1000))
    return '%02d:%02d:%02d%s%03d' % (ms // 3600000, ms // 60000 % 60, ms // 1000 % 60, sep, ms % 1000)


def cues(text_lang, voice_lang):
    T = starts(voice_lang)
    for n, line in enumerate(lines.LINES[text_lang], 1):
        a, e = T[n - 1]
        b = min(e + 0.6, T[n][0] - 0.05) if n < 9 else layout(voice_lang)['total'] - 0.1
        yield a, b, line.replace('{B}', '').replace('  ', ' ')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    text_lang = args[0]
    voice_lang = args[1] if len(args) > 1 else VOICE_OF.get(text_lang, text_lang)
    srt = '--srt' in sys.argv
    out = [] if srt else ['WEBVTT', '']
    for n, (a, b, text) in enumerate(cues(text_lang, voice_lang), 1):
        if srt:
            out += [str(n), '%s --> %s' % (ts(a, ','), ts(b, ',')), text, '']
        else:
            out += ['%s --> %s' % (ts(a, '.'), ts(b, '.')), text, '']
    sys.stdout.buffer.write('\n'.join(out).encode('utf-8'))
