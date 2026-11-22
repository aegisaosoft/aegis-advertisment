# -*- coding: utf-8 -*-
"""Rebuild the eight source shots from the cuts already rendered.

The generator's original exports (SHOTS=D:\\Downloads) are gone. Every rendered cut holds
each shot trimmed to that language's line, so the longest copy of a shot across all cuts
is the closest thing to the original. This writes them as <clip>_recovered.mp4 into
./shots, named so build.sh finds them with SHOTS=./shots.

    python recover_shots.py
"""
import os, subprocess
import timeline as T

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, '..', '..')
DST = os.path.join(HERE, 'shots'); os.makedirs(DST, exist_ok=True)
CLIPS = "3682351749 3439427426 328671585 559783562 2827546893 2568051098 3979775174 920882951".split()
# Cuts whose narration has its own audio (uz and zh-Hant reuse en and zh).
LANGS = ['en', 'es', 'ru', 'de', 'fr', 'pt', 'uk', 'tr', 'zh', 'hy', 'ka', 'fa', 'ur']

best = {}
for lang in LANGS:
    mp4 = os.path.join(OUTDIR, 'myeztoll-frank-mike-%s.mp4' % lang)
    if not os.path.exists(mp4):
        continue
    shots = T.layout(lang)['shots']
    start = 0.0
    for k, d in enumerate(shots):
        if k not in best or d > best[k][2]:
            best[k] = (lang, start, d)
        start += d

for k, clip in enumerate(CLIPS):
    lang, start, d = best[k]
    src = os.path.join(OUTDIR, 'myeztoll-frank-mike-%s.mp4' % lang)
    out = os.path.join(DST, '%s_recovered.mp4' % clip)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', '%.3f' % start, '-i', src, '-t', '%.3f' % d,
                    '-an', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', out], check=True)
    print('shot %d (%s): %s %.3f..%.3f (%.2fs)' % (k + 1, clip, lang, start, start + d, d))
