# -*- coding: utf-8 -*-
"""Lay the recorded clips onto the ToonBee cut's scene grid.

    python assemble.py es out.wav

The picture is fixed — it was generated once and cannot be re-exported without
spending another export — so the voice is placed against it rather than the other
way round: every clip starts a beat after its scene cuts, exactly where the English
narrator starts (Scribe measured that lead at 0.08-0.26s across all fourteen scenes).

Each clip is trimmed to its first sound first, because an encoder's leading padding
would otherwise push the line late by a frame or two, and the finished track is
brought to the same loudness as the English mix so the two cuts play at one level.
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import script

HERE = os.path.dirname(os.path.abspath(__file__))
FF = r'D:\ffmpeg\bin\ffmpeg.exe'
LEAD = 0.16
LOUDNESS = '-16'   # what the English export measures at, and what web players expect


def head_silence(path):
    """Seconds of quiet before the first word, so the line lands on the beat."""
    out = subprocess.run([FF, '-hide_banner', '-i', path, '-af',
                          'silencedetect=noise=-40dB:d=0.05', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    first = re.search(r'silence_start: (0(?:\.\d+)?)\s', out)
    if not first:
        return 0.0
    end = re.search(r'silence_end: ([0-9.]+)', out)
    return float(end.group(1)) if end and float(end.group(1)) < 1.0 else 0.0


lang = sys.argv[1] if len(sys.argv) > 1 else 'es'
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, '%s.wav' % lang)
folder = os.path.join(HERE, 'audio', lang)
clips = [os.path.join(folder, '%02d.mp3' % n) for n in range(1, len(script.SCENES) + 1)]
missing = [c for c in clips if not os.path.exists(c)]
if missing:
    sys.exit('not recorded yet: %s' % ', '.join(os.path.basename(m) for m in missing))

total = sum(script.SCENES)
args, chains, labels = [], [], []
for i, ((start, _), path) in enumerate(zip(script.grid(), clips)):
    args += ['-i', path]
    trim = head_silence(path)
    at = int(round((start + LEAD) * 1000))
    chains.append('[%d:a]atrim=start=%.3f,asetpts=PTS-STARTPTS,aresample=48000,'
                  'adelay=%d|%d[a%d]' % (i, trim, at, at, i))
    labels.append('[a%d]' % i)

mix = ('%samix=inputs=%d:duration=longest:normalize=0,'
       'loudnorm=I=%s:TP=-1.5:LRA=11,'
       'apad,atrim=0:%.3f,aformat=sample_fmts=s16:sample_rates=48000:channel_layouts=stereo[out]'
       % (''.join(labels), len(labels), LOUDNESS, total))

subprocess.run([FF, '-y', '-hide_banner', '-loglevel', 'error'] + args +
               ['-filter_complex', ';'.join(chains) + ';' + mix,
                '-map', '[out]', out], check=True)
print('wrote %s (%.2fs)' % (out, total))
