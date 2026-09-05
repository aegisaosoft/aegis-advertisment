"""Re-anchor scene animations from hard-coded seconds to cue indices.

Every inline `animation-delay:Ns` inside a scene is rewritten as
`data-cue="<index>" data-cue-offset="<seconds after that cue>"`. When narration
is later recorded and the cue timings shift, the visuals follow automatically
instead of drifting away from the voice.
"""
import io
import json
import re

FILES = ['gantry-to-payout.html', 'stop-losing-start-earning.html']

SCENE_RE = re.compile(r'<section class="scene" data-scene="(\d+)">(.*?)\n    </section>', re.S)
DELAY_RE = re.compile(r'style="([^"]*?)animation-delay:\s*([0-9.]+)s([^"]*)"')


def cue_times(html):
    """Pull the cue start times out of the SCENES literal, per scene."""
    body = html[html.index('  var SCENES = ['):html.index('  var TOTAL =')]
    scenes, cur = [], None
    for line in body.splitlines():
        if re.match(r'\s*\{ chapter:', line):
            if cur is not None:
                scenes.append(cur)
            cur = []
        m = re.match(r'\s*\{t:([0-9.]+),', line)
        if m and cur is not None:
            cur.append(float(m.group(1)))
    if cur is not None:
        scenes.append(cur)
    return scenes


def patch(fn):
    s = io.open(fn, encoding='utf-8').read()
    times = cue_times(s)
    stats = []

    def do_scene(m):
        idx, inner = int(m.group(1)), m.group(2)
        ts = times[idx]
        n = [0]

        def do_delay(dm):
            before, secs, after = dm.group(1), float(dm.group(2)), dm.group(3)
            # the cue that is speaking when this element appears
            cue = 0
            for i, t in enumerate(ts):
                if secs >= t - 0.001:
                    cue = i
            off = round(secs - ts[cue], 2)
            rest = (before + after).strip().rstrip(';').strip()
            n[0] += 1
            keep = ('style="%s" ' % rest) if rest else ''
            return '%sdata-cue="%d" data-cue-offset="%s"' % (keep, cue, off)

        inner2 = DELAY_RE.sub(do_delay, inner)
        stats.append((idx, n[0]))
        return '<section class="scene" data-scene="%d">%s\n    </section>' % (idx, inner2)

    s2, n = SCENE_RE.subn(do_scene, s)
    if n == 0:
        raise SystemExit('no scenes matched in ' + fn)

    io.open(fn, 'w', encoding='utf-8').write(s2)
    print('%s: %d scenes, delays rewired %s'
          % (fn, n, json.dumps({str(a): b for a, b in stats})))


for f in FILES:
    patch(f)
