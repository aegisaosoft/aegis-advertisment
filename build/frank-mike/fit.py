# -*- coding: utf-8 -*-
"""Tempo-fit lines that overrun their scene (atempo, pitch kept, capped at 1.2x)."""
import os, subprocess, sys
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
LIMIT = [5.6] * 8 + [4.6]


def dur(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                                 '-of', 'csv=p=0', p], capture_output=True, text=True).stdout)


for lang in sys.argv[1:]:
    for n in range(1, 10):
        p = os.path.join(V, '%s_%02d.wav' % (lang, n))
        d = dur(p)
        if d > LIMIT[n - 1]:
            k = min(d / LIMIT[n - 1], 1.2)
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', p, '-af', 'atempo=%.4f' % k,
                            '-c:a', 'pcm_s16le', p + '.tmp.wav'], check=True)
            os.replace(p + '.tmp.wav', p)
            print('%s_%02d %.2f -> %.2f (x%.3f)' % (lang, n, d, dur(p), k))
