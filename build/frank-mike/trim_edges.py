# -*- coding: utf-8 -*-
"""Keep no more than 0.1 s of silence at either end of every clip.

Cutting a continuous reading by character timings leaves air at the edges — the v3
voices especially, whose alignment runs late — and in a cut where the voice is meant to
run on, that air is a gap. Edges below -45 dBFS go; 50 ms of room tone stays.

    python trim_edges.py [lang ...]        (all clips when no language is given)
"""
import os, struct, subprocess, sys, wave
V = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
TH = 32768 * 10 ** (-45 / 20.0)
PAD = 0.05


def edges(path):
    w = wave.open(path); n = w.getnframes(); sr = w.getframerate()
    a = struct.unpack('<%dh' % n, w.readframes(n)); w.close()
    i = next((k for k, x in enumerate(a) if abs(x) > TH), 0)
    j = next((k for k, x in enumerate(reversed(a)) if abs(x) > TH), 0)
    return i / sr, j / sr, n / sr


langs = sys.argv[1:]
for name in sorted(os.listdir(V)):
    if not name.endswith('.wav') or (langs and name.rsplit('_', 1)[0] not in langs):
        continue
    p = os.path.join(V, name)
    lead, tail, total = edges(p)
    if lead <= 0.1 and tail <= 0.1:
        continue
    a, b = max(0.0, lead - PAD), total - max(0.0, tail - PAD)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', p, '-ss', '%.3f' % a, '-to', '%.3f' % b,
                    '-c:a', 'pcm_s16le', p + '.tmp.wav'], check=True)
    os.replace(p + '.tmp.wav', p)
    l2, t2, n2 = edges(p)
    print('%-10s lead %.2f->%.2f  tail %.2f->%.2f  %.2fs->%.2fs' % (name, lead, l2, tail, t2, total, n2))
