# -*- coding: utf-8 -*-
"""Round-trip each clip through Scribe; report the share of script words heard back."""
import json, os, re, subprocess, sys, unicodedata
import lines
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(HERE, 'audio')
STT_OUT = os.path.join(HERE, 'takes', 'stt'); os.makedirs(STT_OUT, exist_ok=True)
STT = r'C:\aegis-aa\aegis-advertisment\build\toonbee\stt.py'
CODE = {'ru': 'ru', 'uk': 'uk', 'de': 'de', 'fr': 'fr', 'pt': 'pt', 'tr': 'tr', 'zh': 'zh',
        'hy': 'hy', 'ka': 'ka', 'fa': 'fa', 'ur': 'ur'}


def toks(s, lang):
    s = unicodedata.normalize('NFC', s.replace('{B}', '')).lower()
    s = ''.join(c if (c.isalnum() or c in '\u200c') else ' ' for c in s)
    if lang == 'zh':
        return [c for c in s if c.strip()]
    return s.replace('\u200c', '').split()


for lang in sys.argv[1:]:
    tot = hit = 0; bad = []
    for n, line in enumerate(lines.LINES[lang], 1):
        f = os.path.join(V, '%s_%02d.wav' % (lang, n)); o = os.path.join(STT_OUT, '%s_%02d.json' % (lang, n))
        subprocess.run([sys.executable, STT, f, o, CODE[lang]], capture_output=True)
        heard = json.load(open(o, encoding='utf-8'))['text']
        ref, got = toks(line, lang), toks(heard, lang)
        pool = list(got); h = 0
        for w in ref:
            if w in pool: pool.remove(w); h += 1
        tot += len(ref); hit += h
        if h < 0.6 * len(ref): bad.append('%02d: %s' % (n, heard))
    print('%s %3.0f%%  %s' % (lang, 100.0 * hit / tot, ' | '.join(bad)))
