"""Inline the recorded narration into the films and retime them to the voice.

Reads narration/audio/<film>/<lang>/<scene>-<cue>.mp3, measures each clip, moves
every cue to where the voice actually lands, stretches each scene to fit, and
embeds the clips as data: URIs. Visual beats follow because they are anchored to
cue indices rather than to hard-coded seconds.

    python embed_audio.py                 # one file per film if it fits
    python embed_audio.py --per-language  # always split by language

Artifacts must stay under 16 MB, so when the three languages together are too
big the script writes one file per language automatically.
"""
import argparse
import base64
import io
import json
import os
import re
import struct

FILMS = [('gantry-to-payout.html', 'A'), ('stop-losing-start-earning.html', 'B')]
LANGS = ['en', 'es', 'ru']

LEAD = 0.30      # beat before the first line of a scene
GAP = 0.55       # breath between lines
TAIL = 1.00      # beat after the last line before the scene cuts
MAX_BYTES = 14 * 1024 * 1024     # keep clear of the 16 MB artifact ceiling

BITRATES = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0]
RATES = {0: 44100, 1: 48000, 2: 32000}


def mp3_duration(path):
    """Duration in seconds, read from the MPEG frame headers (CBR-accurate)."""
    data = io.open(path, 'rb').read()
    i = 0
    if data[:3] == b'ID3':                       # skip the ID3v2 tag
        size = struct.unpack('>I', b'\0' + data[6:9])[0] if False else (
            (data[6] & 0x7F) << 21 | (data[7] & 0x7F) << 14 |
            (data[8] & 0x7F) << 7 | (data[9] & 0x7F))
        i = 10 + size

    while i < len(data) - 4:
        if data[i] == 0xFF and (data[i + 1] & 0xE0) == 0xE0:
            ver = (data[i + 1] >> 3) & 0x03      # 3 = MPEG1, 2 = MPEG2
            layer = (data[i + 1] >> 1) & 0x03    # 1 = Layer III
            br_i = (data[i + 2] >> 4) & 0x0F
            sr_i = (data[i + 2] >> 2) & 0x03
            if layer == 1 and br_i not in (0, 15) and sr_i != 3:
                kbps = BITRATES[br_i]
                rate = RATES[sr_i]
                if ver == 2:
                    rate //= 2
                elif ver == 0:
                    rate //= 4
                if kbps and rate:
                    return round((len(data) - i) * 8.0 / (kbps * 1000.0), 3)
        i += 1
    raise SystemExit('Not a readable MP3: ' + path)


def parse_scenes(html):
    body = html[html.index('  var SCENES = ['):html.index('  var TOTAL =')]
    scenes, cur = [], None
    for line in body.splitlines():
        m = re.match(r'\s*\{ chapter:"([^"]+)", dur:([0-9.]+),', line)
        if m:
            if cur:
                scenes.append(cur)
            cur = {'chapter': m.group(1), 'dur': float(m.group(2)), 'cues': []}
        c = re.match(r'\s*\{t:([0-9.]+),\s*en:"((?:[^"\\]|\\.)*)",', line)
        if c and cur is not None:
            cur['cues'].append({'t': float(c.group(1)), 'words': len(c.group(2).split())})
    if cur:
        scenes.append(cur)
    return scenes


def retime(scenes, durations):
    """New cue times and scene lengths, driven by the recorded clips."""
    out = []
    for si, sc in enumerate(scenes):
        t = LEAD
        times = []
        for ci, cue in enumerate(sc['cues']):
            times.append(round(t, 2))
            d = durations.get('%d-%d' % (si, ci))
            if d is None:                     # not recorded: estimate from words
                d = max(1.6, cue['words'] / 2.6)
            t += d + GAP
        out.append({'times': times, 'dur': round(t - GAP + TAIL, 2)})
    return out


def apply_timing(html, plan):
    """Rewrite every t: and dur: in the SCENES literal."""
    head = html.index('  var SCENES = [')
    tail = html.index('  var TOTAL =')
    body = html[head:tail]

    si = [-1]
    ci = [0]

    def scene_sub(m):
        si[0] += 1
        ci[0] = 0
        return '%s dur:%g,' % (m.group(1), plan[si[0]]['dur'])

    body = re.sub(r'(\{ chapter:"[^"]+",) dur:[0-9.]+,', scene_sub, body)

    si[0] = -1

    def cue_sub(m):
        if m.group(0).startswith('{ chapter'):
            return m.group(0)
        t = plan[si[0]]['times'][ci[0]]
        ci[0] += 1
        return '{t:%g,' % t

    def walk(m):
        if m.group(0).startswith('{ chapter'):
            si[0] += 1
            ci[0] = 0
            return m.group(0)
        t = plan[si[0]]['times'][ci[0]]
        ci[0] += 1
        return '{t:%g,' % t

    body = re.sub(r'\{ chapter:"[^"]+", dur:[0-9.]+,|\{t:[0-9.]+,', walk, body)
    return html[:head] + body + html[tail:]


def clip_bank(film, langs):
    bank, durations, total = {}, {}, 0
    for lg in langs:
        d = os.path.join('narration', 'audio', film, lg)
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if not name.endswith('.mp3'):
                continue
            lid = name[:-4]
            path = os.path.join(d, name)
            raw = io.open(path, 'rb').read()
            total += len(raw)
            bank.setdefault(lg, {})[lid] = 'data:audio/mpeg;base64,' + base64.b64encode(raw).decode('ascii')
            if lg == 'en' or lid not in durations:
                durations[lid] = mp3_duration(path)
    return bank, durations, total


def write(html, bank, out):
    payload = json.dumps(bank, ensure_ascii=False)
    html = re.sub(r'  var AUDIO = \{\};', '  var AUDIO = ' + payload.replace('\\', '\\\\') + ';', html, count=1)
    io.open(out, 'w', encoding='utf-8').write(html)
    return os.path.getsize(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--per-language', action='store_true')
    a = ap.parse_args()

    for fn, film in FILMS:
        html = io.open(fn, encoding='utf-8').read()
        if '  var AUDIO = {};' not in html:
            raise SystemExit('%s has no AUDIO slot - run patch_audio.py first' % fn)

        have = [lg for lg in LANGS if os.path.isdir(os.path.join('narration', 'audio', film, lg))]
        if not have:
            print('%s: no clips under narration/audio/%s - skipped' % (fn, film))
            continue

        scenes = parse_scenes(html)
        _, durations, total = clip_bank(film, have)
        plan = retime(scenes, durations)
        timed = apply_timing(html, plan)

        runtime = sum(p['dur'] for p in plan)
        print('%s: %d clips, %.1f MB raw, retimed to %d:%02d'
              % (fn, sum(len(os.listdir(os.path.join('narration', 'audio', film, lg))) for lg in have),
                 total / 1048576.0, int(runtime // 60), int(runtime % 60)))

        split = a.per_language or total * 1.37 > MAX_BYTES
        if not split:
            bank, _, _ = clip_bank(film, have)
            size = write(timed, bank, fn.replace('.html', '.voiced.html'))
            print('   -> %s  %.1f MB' % (fn.replace('.html', '.voiced.html'), size / 1048576.0))
        else:
            print('   three languages exceed the artifact ceiling; splitting per language')
            for lg in have:
                bank, _, _ = clip_bank(film, [lg])
                out = fn.replace('.html', '.voiced.%s.html' % lg)
                size = write(timed, bank, out)
                print('   -> %-42s %.1f MB' % (out, size / 1048576.0))


main()
