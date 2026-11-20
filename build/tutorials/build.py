# -*- coding: utf-8 -*-
"""Lay each episode out around its own recording and write the page render.js renders.

    python build.py               # every episode, both languages
    python build.py 1 es          # one of them

Out come, per episode and language:

    ep<NN>.<lang>.html            the film — a pure function of t, self-timed
    audio/<lang>/ep<NN>/track.mp3 the clips at the exact seconds the timeline placed them
    mp4/<name>.srt / .vtt         the same words at the same seconds, for YouTube

Nothing here decides how long anything is. The recording does: a beat starts, the
camera and the cursor move during the lead-in, the line is spoken, and the next beat
begins a breath later. Writing a longer line therefore moves the picture rather than
desynchronising it, and re-recording one line reflows the episode around it.
"""
import io
import json
import os
import subprocess
import sys

from PIL import Image

import episodes
import model
import tts

HERE = os.path.dirname(os.path.abspath(__file__))
# Where a screen's picture comes from, best first. `shots/` is this build's own second
# redaction pass; `images-2x` is the high-density recapture the videos use, kept apart
# from `images` so the written guides keep the set they were laid out with.
SHOT_DIRS = (
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shots'),
    'C:\\aegis-aa\\docs\\images-2x',
    'C:\\aegis-aa\\docs\\images',
)
FFMPEG = next((p for p in ('D:\\ffmpeg\\bin\\ffmpeg.exe', 'C:\\ffmpeg\\bin\\ffmpeg.exe')
               if os.path.exists(p)), 'ffmpeg')
# Only the file name becomes ffprobe: a blanket replace turns D:\ffmpeg\bin\ffmpeg.exe
# into D:\ffprobe\bin\ffprobe.exe, which is not anywhere.
FFPROBE = os.path.join(os.path.dirname(FFMPEG), os.path.basename(FFMPEG).replace('ffmpeg', 'ffprobe'))

TITLE_HOLD = 3.2     # the opening card, before the first beat
LEAD = 0.55          # the camera and the cursor move before the line starts
GAP = 0.5            # breath between lines
END_HOLD = 3.4       # the closing card
CAPTION_TAIL = 0.3   # a subtitle stays this long after the last word


def duration(path):
    out = subprocess.run([FFPROBE, '-v', 'error', '-show_entries', 'format=duration',
                          '-of', 'csv=p=0', path], capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except ValueError:
        sys.exit('cannot measure %s' % path)


def stamp(seconds, comma=True):
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return '%02d:%02d:%02d%s%03d' % (h, m, s, ',' if comma else '.', ms)


def shot_file(lang, key):
    """The picture to use for a screen, from the first source that has it.

    A locally redacted copy wins over the recapture, and the recapture over the set the
    written guides use — so a screen this build had to blur again is never quietly
    replaced by the unblurred original just because a sharper one appeared.
    """
    for root in SHOT_DIRS:
        p = os.path.join(root, lang, key + '.png')
        if os.path.exists(p):
            return p
    return os.path.join(SHOT_DIRS[-1], lang, key + '.png')


def pick(value, lang):
    """A coordinate is either the same in every language, or given per language.

    Spanish labels are longer than English ones, so a right-aligned control — the
    language selector, Logout — sits at a different x. Anything anchored to the left
    or to the sidebar is identical in both and is written once.

    Returns (value, measured_here). A value written for this language was measured on
    this language's own capture, so it is used exactly as given; one inherited from
    English still has to be mapped onto the target capture.
    """
    if isinstance(value, dict) and lang in value:
        return value[lang], True
    if isinstance(value, dict):
        return value.get('en'), False
    return value, False


# Where a screen's Spanish capture puts a row that the English one puts somewhere else.
#
# Most screens differ only in total height, because a translated footer wraps to a
# different number of lines; everything above it is at the same pixel row, and scaling
# by the ratio of the two heights is exactly right. These three do not: a wrapped title,
# a button row that breaks onto two lines, a field description that runs to three lines
# — each pushes everything below it down, while the header above stays put.
#
# Pairs are (english y, spanish y) as fractions of each capture's own height, read off
# the two captures. Fractions rather than pixels so that recapturing at a higher pixel
# density does not invalidate the table. Between two landmarks the position is
# interpolated; outside them the nearest one's offset is held.
Y_LANDMARKS = {
    '10-all-vehicles': {'es': [(0.0443, 0.0426), (0.1261, 0.1213), (0.1415, 0.1269),
                               (0.2137, 0.2269), (0.3176, 0.3287), (0.8335, 0.8241)]},
    '30-settings-owner': {'es': [(0.0324, 0.0311), (0.3469, 0.3329), (0.4757, 0.4666),
                                 (0.6087, 0.5942), (0.6904, 0.6833), (0.7333, 0.7340),
                                 (0.7889, 0.7873), (0.9711, 0.9588)]},
    '37-settings-gps-alerts': {'es': [(0.0430, 0.0419), (0.2572, 0.2502), (0.2919, 0.2839),
                                      (0.4060, 0.4004), (0.5192, 0.5159), (0.6455, 0.6442),
                                      (0.7736, 0.7734), (0.8906, 0.8935)]},
}


def y_mapper(shot, lang, en_h, lang_h):
    """A function from an English vertical fraction to this language's own."""
    marks = Y_LANDMARKS.get(shot, {}).get(lang)
    if not marks:
        ratio = float(en_h) / lang_h
        return lambda y: min(1.0, y * ratio)

    xs = [m[0] for m in marks]
    ys = [m[1] for m in marks]

    def mapped(y):
        if y <= xs[0]:
            out = y + (ys[0] - xs[0])
        elif y >= xs[-1]:
            out = y + (ys[-1] - xs[-1])
        else:
            i = max(j for j in range(len(xs) - 1) if xs[j] <= y)
            span = xs[i + 1] - xs[i]
            u = (y - xs[i]) / span if span else 0.0
            out = ys[i] + u * (ys[i + 1] - ys[i])
        return min(1.0, max(0.0, out))

    return mapped


def load_boxes(lang):
    """The element boxes a capture recorded (capture-screenshots.js --boxes), {shot: {path: rect}}."""
    for root in SHOT_DIRS:
        p = os.path.join(root, lang, '_boxes.json')
        if os.path.exists(p):
            return json.load(io.open(p, encoding='utf-8'))
    return {}


class BoxMap(object):
    """Moves a rectangle or a point written against the English capture onto another language's capture.

    The coordinates in the series files were measured by hand on the English (and Spanish) screenshots.
    Another language moves every control: a longer label widens a button and pushes its neighbours, and
    Persian and Urdu lay the whole page out right to left. Both captures recorded where each element is,
    keyed by its DOM path, and the path names the same control in both languages. So a ring is matched
    to the element(s) it surrounds on the English capture and redrawn around the same element(s) on the
    target one, keeping its padding; a point keeps its place inside the smallest element that holds it.
    """

    def __init__(self, en, other, rtl):
        self.en, self.to, self.rtl = en, other, rtl
        self.common = [p for p in en if p in other]

    @staticmethod
    def _area(r):
        return max(0.0, r[2]) * max(0.0, r[3])

    @staticmethod
    def _inter(a, b):
        x0, y0 = max(a[0], b[0]), max(a[1], b[1])
        x1, y1 = min(a[0] + a[2], b[0] + b[2]), min(a[1] + a[3], b[1] + b[3])
        return max(0.0, x1 - x0) * max(0.0, y1 - y0)

    def _rel(self, outer, r, target):
        """r expressed inside `outer`, re-expressed inside `target`; mirrored for a right-to-left target."""
        rx = (r[0] - outer[0]) / outer[2] if outer[2] else 0.0
        ry = (r[1] - outer[1]) / outer[3] if outer[3] else 0.0
        rw = r[2] / outer[2] if outer[2] else 0.0
        rh = r[3] / outer[3] if outer[3] else 0.0
        if self.rtl:
            rx = 1.0 - rx - rw
        return (target[0] + rx * target[2], target[1] + ry * target[3], rw * target[2], rh * target[3])

    def rect(self, r):
        r = tuple(r)
        ra = self._area(r)
        if not ra or not self.common:
            return None
        # One element that is the ring's own target: the ring is it, padded.
        best, score = None, 0.0
        for p in self.common:
            e = self.en[p]
            i = self._inter(r, e)
            if i:
                iou = i / (ra + self._area(e) - i)
                if iou > score:
                    best, score = p, iou
        if best and score >= 0.6:
            return self._rel(self.en[best], r, self.to[best])
        # A ring over a group (a row of buttons, a block of fields): the elements it encloses.
        inside = [p for p in self.common
                  if self._area(self.en[p]) >= 0.02 * ra
                  and self._inter(r, self.en[p]) >= 0.8 * self._area(self.en[p])]
        if inside:
            def union(rs):
                x0 = min(q[0] for q in rs); y0 = min(q[1] for q in rs)
                x1 = max(q[0] + q[2] for q in rs); y1 = max(q[1] + q[3] for q in rs)
                return (x0, y0, x1 - x0, y1 - y0)
            ue, ut = union([self.en[p] for p in inside]), union([self.to[p] for p in inside])
            return self._rel(ue, r, ut)
        # Neither: hold its place inside the smallest element around it.
        holder = self._holder(r[0] + r[2] / 2, r[1] + r[3] / 2, 0.0)
        return self._rel(self.en[holder], r, self.to[holder]) if holder else None

    def _holder(self, x, y, min_area):
        found, size = None, None
        for p in self.common:
            e = self.en[p]
            a = self._area(e)
            if a >= min_area and e[0] <= x <= e[0] + e[2] and e[1] <= y <= e[1] + e[3]:
                if size is None or a < size:
                    found, size = p, a
        return found

    def point(self, x, y, min_area=0.0):
        holder = self._holder(x, y, min_area)
        if not holder:
            return None
        e, t = self.en[holder], self.to[holder]
        rx = (x - e[0]) / e[2] if e[2] else 0.5
        ry = (y - e[1]) / e[3] if e[3] else 0.5
        if self.rtl:
            rx = 1.0 - rx
        return (t[0] + rx * t[2], t[1] + ry * t[3])


# The English capture the boxes were recorded on. It is a fresh capture, not the one the series
# coordinates were measured on (that one has no boxes, and the account's data has moved since), so
# a coordinate first finds its own place on this capture by matching the picture (RefMatch).
REF_DIR = os.path.join(HERE, 'shots', '_ref', 'en')


class RefMatch(object):
    """Moves a point on the English capture the series was written against onto the reference capture.

    The two show the same screen, but a card added to the dashboard or a different number of rows moves
    everything below it. A patch of the old picture around the point is looked up in the new one.
    """

    def __init__(self, old_path, new_path):
        import cv2
        self.cv2 = cv2
        self.old = cv2.imread(old_path, cv2.IMREAD_GRAYSCALE)
        self.new = cv2.imread(new_path, cv2.IMREAD_GRAYSCALE)
        self.marks = self._anchors()

    def _anchors(self):
        """(old y, new y) pixel pairs from patches that match in exactly one place.

        Both captures are left-to-right and the same width, so a control moves up or down, never
        sideways: each patch is searched in a narrow band around its own x. A patch that also matches a
        second place (a table row looks like the next row) is dropped — matched one query at a time, such
        patches put rings on the wrong row. What is left is one vertical mapping for the whole screen.
        """
        cv2 = self.cv2
        oh, ow = self.old.shape
        nh, nw = self.new.shape
        pw, ph = 420, 150
        found = []
        for fy in [i / 60.0 for i in range(1, 60)]:
            for fx in (0.2, 0.4, 0.6, 0.8):
                px, py = int(fx * ow), int(fy * oh)
                x0, y0 = max(0, px - pw // 2), max(0, py - ph // 2)
                patch = self.old[y0:y0 + ph, x0:x0 + pw]
                if patch.shape != (ph, pw) or patch.std() < 8 or ph > nh:
                    continue
                slack = int(0.015 * nw)
                sx0 = max(0, x0 - slack)
                band = self.new[:, sx0:min(nw, x0 + pw + slack)]
                if band.shape[1] < pw:
                    continue
                res = cv2.matchTemplate(band, patch, cv2.TM_CCOEFF_NORMED)
                _, best, _, loc = cv2.minMaxLoc(res)
                if best < 0.85:
                    continue
                masked = res.copy()
                masked[max(0, loc[1] - ph // 2):loc[1] + ph // 2, :] = -1
                second = masked.max() if masked.size else -1
                if best - second < 0.1:
                    continue
                found.append((y0 + ph / 2.0, loc[1] + ph / 2.0))
        found.sort()
        # Keep the longest run that rises in both pictures; an anchor out of order is a false match.
        best_run = []
        for i in range(len(found)):
            run = [found[i]]
            for p in found[i + 1:]:
                if p[1] >= run[-1][1]:
                    run.append(p)
            if len(run) > len(best_run):
                best_run = run
        return best_run

    def _y(self, y):
        oh = self.old.shape[0]
        nh = self.new.shape[0]
        py = y * oh
        m = self.marks
        if not m:
            return None
        if py <= m[0][0]:
            out = py + (m[0][1] - m[0][0])
        elif py >= m[-1][0]:
            out = py + (m[-1][1] - m[-1][0])
        else:
            i = max(j for j in range(len(m) - 1) if m[j][0] <= py)
            span = m[i + 1][0] - m[i][0]
            u = (py - m[i][0]) / span if span else 0.0
            out = m[i][1] + u * (m[i + 1][1] - m[i][1])
        return out / float(nh)

    def _x(self, x):
        return x * self.old.shape[1] / float(self.new.shape[1])

    def _find(self, px, py, pw, ph, near_y):
        """Top-left pixel of the old patch (px, py, pw, ph) on the new capture, or None.

        The anchors only move things up or down; a column added to a table moves its neighbours
        sideways. So the patch under the ring itself is looked up across the whole width, in a band
        around the height the anchors predict, and kept only if it matches in one place.
        """
        cv2 = self.cv2
        oh, ow = self.old.shape
        nh, nw = self.new.shape
        px, py = max(0, int(px)), max(0, int(py))
        pw, ph = min(int(pw), ow - px), min(int(ph), oh - py)
        if pw < 60 or ph < 24:
            return None
        patch = self.old[py:py + ph, px:px + pw]
        if patch.std() < 8 or pw > nw:
            return None
        slack = int(0.08 * nh)
        by0 = max(0, int(near_y) - slack)
        by1 = min(nh, int(near_y) + ph + slack)
        band = self.new[by0:by1, :]
        if band.shape[0] < ph:
            return None
        res = cv2.matchTemplate(band, patch, cv2.TM_CCOEFF_NORMED)
        _, best, _, loc = cv2.minMaxLoc(res)
        if best < 0.8:
            return None
        masked = res.copy()
        masked[max(0, loc[1] - ph // 2):loc[1] + ph // 2 + 1,
               max(0, loc[0] - pw // 2):loc[0] + pw // 2 + 1] = -1
        if best - masked.max() < 0.05:
            return None
        return loc[0], by0 + loc[1]

    def point(self, x, y):
        ny = self._y(y)
        if ny is None:
            return None
        oh, ow = self.old.shape
        nh, nw = self.new.shape
        pw, ph = 360, 140
        hit = self._find(x * ow - pw / 2, y * oh - ph / 2, pw, ph, ny * nh - ph / 2)
        if hit:
            return ((hit[0] + pw / 2.0) / nw, (hit[1] + ph / 2.0) / nh)
        return (self._x(x), ny)

    def rect(self, r):
        oh, ow = self.old.shape
        nh, nw = self.new.shape
        # Controls keep their size between the two captures: move the ring's top, keep its pixel
        # height (mapping the bottom too squeezes a ring to a line where rows were added or dropped).
        y0 = self._y(r[1])
        if y0 is None:
            return None
        h = r[3] * oh / float(nh)
        # The ring's top part (a column's header, a whole button) is what identifies it.
        px, py, pw = r[0] * ow, r[1] * oh, r[2] * ow
        for ph in (min(r[3] * oh, 240), min(r[3] * oh, 110)):
            hit = self._find(px, py, pw, ph, y0 * nh)
            if hit:
                return (hit[0] / float(nw), hit[1] / float(nh), r[2] * ow / float(nw), h)
        return (self._x(r[0]), y0, r[2] * ow / float(nw), h)


class LangMap(object):
    """Old English coordinates → the reference capture (RefMatch) → this language (BoxMap)."""

    def __init__(self, ref, bm):
        self.ref, self.bm = ref, bm

    def rect(self, r):
        on_ref = self.ref.rect(r)
        return self.bm.rect(on_ref) if on_ref else None

    def point(self, x, y, min_area=0.0):
        on_ref = self.ref.point(x, y)
        return self.bm.point(on_ref[0], on_ref[1], min_area) if on_ref else None


def box_maps(ep, lang):
    """{shot: LangMap} for the shots both the English reference and this language recorded boxes for."""
    # English is what the coordinates were written on. Spanish shares them, and only a Spanish screen
    # captured again since (one with recorded boxes) has to be mapped.
    if lang == 'en':
        return {}
    ref_file = os.path.join(REF_DIR, '_boxes.json')
    if not os.path.exists(ref_file):
        return {}
    en, other = json.load(io.open(ref_file, encoding='utf-8')), load_boxes(lang)
    out = {}
    for b in ep.beats:
        if b.shot in en and b.shot in other and b.shot not in out:
            ref = RefMatch(shot_file('en', b.shot), os.path.join(REF_DIR, b.shot + '.png'))
            out[b.shot] = LangMap(ref, BoxMap(en[b.shot], other[b.shot], lang in model.RTL))
    return out


def _r4(v):
    return round(min(1.0, max(0.0, v)), 4)


def track(lang, ep, clips, starts, total):
    """One mp3 with every clip at its own second, rather than a concatenation.

    render.js muxes this file instead of capturing the browser's speakers, so picture
    and voice cannot disagree: both are placed by the same timeline.
    """
    out = os.path.join(HERE, 'audio', lang, 'ep%02d' % ep.num, 'track.mp3')
    args = [FFMPEG, '-y', '-v', 'error']
    for c in clips:
        args += ['-i', c]
    # `normalize=0` — amix otherwise divides every input by the number of inputs, and a
    # fourteen-line episode would come out fourteen times too quiet.
    chains = ['[%d:a]adelay=%d|%d[a%d]' % (i, int(t * 1000), int(t * 1000), i)
              for i, t in enumerate(starts)]
    mix = ''.join('[a%d]' % i for i in range(len(clips)))
    # `apad` before `-t`: amix ends with its last input, which is the final word of the
    # narration. render.js muxes with -shortest, so without the padding the video is cut
    # to the last syllable and the closing card never reaches the file.
    args += ['-filter_complex', ';'.join(chains) + ';' + mix +
             'amix=inputs=%d:normalize=0:dropout_transition=0[mixed];[mixed]apad[out]' % len(clips),
             '-map', '[out]', '-t', '%.3f' % total, '-c:a', 'libmp3lame', '-b:a', '192k', out]
    subprocess.run(args, check=True)
    return out


def build(ep, lang):
    # Every vertical fraction in episodes.py is written against the English capture,
    # unless it was written for this language, in which case it is already right.
    mapper = {}
    for b in ep.beats:
        if b.shot not in mapper:
            en_h = Image.open(shot_file('en', b.shot)).size[1]
            lang_h = Image.open(shot_file(lang, b.shot)).size[1]
            mapper[b.shot] = y_mapper(b.shot, lang, en_h, lang_h)

    clips, durs = [], []
    for i in range(len(ep.beats)):
        path = tts.clip_path(lang, ep, i)
        if not os.path.exists(path):
            sys.exit('no clip %s — run: python tts.py %d %s' % (path, ep.num, lang))
        clips.append(path)
        durs.append(duration(path))

    maps = box_maps(ep, lang)

    # ---------------------------------------------------------------- timeline
    beats, cues, t = [], [], TITLE_HOLD
    for i, b in enumerate(ep.beats):
        my = mapper[b.shot]
        cam, cam_here = pick(b.cam, lang)
        point, point_here = pick(b.point, lang)
        ring, ring_here = pick(b.ring, lang)
        bm = maps.get(b.shot)
        if bm:
            # Measured boxes beat the height ratio: they follow the target capture's own layout.
            if ring and not ring_here:
                moved = bm.rect(ring)
                if moved:
                    ring, ring_here = tuple(_r4(v) for v in moved), True
            if point and not point_here:
                moved = bm.point(point[0], point[1])
                if moved:
                    point, point_here = (_r4(moved[0]), _r4(moved[1])), True
            # A camera close enough to matter follows what it looks at; a wide one stays put.
            if not cam_here and cam[2] > 1.05:
                moved = bm.point(cam[0], cam[1], 0.01)
                if moved:
                    cam, cam_here = (_r4(moved[0]), _r4(moved[1]), cam[2]), True
        cam_y = cam[1] if cam_here else my(cam[1])
        cues.append({'t': t + LEAD, 'end': t + LEAD + durs[i] + CAPTION_TAIL,
                     'text': b.text[lang]})
        beats.append({
            't': round(t, 3),
            'shot': b.shot,
            'url': b.url or '',
            'cam': [cam[0], cam_y, cam[2]],
            'point': ([point[0], point[1] if point_here else my(point[1])]
                      if point else None),
            'click': (b.click + LEAD) if b.click is not None else None,
            'ring': ([ring[0], ring[1] if ring_here else my(ring[1]), ring[2],
                      (ring[3] if ring_here else my(ring[1] + ring[3]) - my(ring[1]))]
                     if ring else None),
            'ringOut': b.ring_out,
            'label': b.label[lang] if (b.label[lang] or '').strip() else None,
        })
        t += LEAD + durs[i] + GAP + b.hold
    total = t + END_HOLD

    # ---------------------------------------------------------------- shots
    used, shots = [], []
    for b in ep.beats:
        if b.shot not in used:
            used.append(b.shot)
    for shot_key in used:
        path = shot_file(lang, shot_key)
        if not os.path.exists(path):
            sys.exit('missing screenshot %s' % path)
        w, h = Image.open(path).size
        shots.append({'key': shot_key, 'w': w, 'h': h,
                      'src': 'file:///' + path.replace('\\', '/')})

    name = 'myeztoll-tutorial-%02d-%s-%s' % (ep.num, ep.slug, lang)
    film = {
        'total': round(total, 3),
        'titleOut': TITLE_HOLD,
        'endHold': END_HOLD,
        'shots': shots,
        'beats': beats,
        'card': {
            'eyebrow': '%s · %d' % ((model.PARTNER_EYEBROW[lang] if ep.audience == 'partner'
                                     else episodes.CARD[lang]['eyebrow']), ep.num),
            'title': ep.title[lang],
            'sub': ep.sub[lang],
            'endTitle': episodes.CARD[lang]['end_title'],
            'endSub': episodes.CARD[lang]['end_sub'],
        },
    }

    audio = track(lang, ep, clips, [c['t'] for c in cues], total)
    shell = io.open(os.path.join(HERE, 'shell.html'), encoding='utf-8').read()
    page = (shell
            .replace('__FILM_JSON__', json.dumps(film, ensure_ascii=False))
            .replace('__AUDIO__', 'audio/%s/ep%02d/track.mp3' % (lang, ep.num)))
    io.open(os.path.join(HERE, 'ep%02d.%s.html' % (ep.num, lang)), 'w',
            encoding='utf-8').write(page)

    # ---------------------------------------------------------------- captions
    os.makedirs(os.path.join(HERE, 'mp4'), exist_ok=True)
    srt, vtt = [], ['WEBVTT', '']
    for i, c in enumerate(cues, 1):
        srt += [str(i), '%s --> %s' % (stamp(c['t']), stamp(c['end'])), c['text'], '']
        vtt += ['%s --> %s' % (stamp(c['t'], False), stamp(c['end'], False)), c['text'], '']
    # UTF-8 with a BOM: several players mis-read accented characters in a plain .srt.
    io.open(os.path.join(HERE, 'mp4', name + '.srt'), 'w',
            encoding='utf-8-sig').write('\n'.join(srt))
    io.open(os.path.join(HERE, 'mp4', name + '.vtt'), 'w',
            encoding='utf-8').write('\n'.join(vtt))

    print('  ep%02d %-22s %s  %5.1fs  %2d beats  %2d shots' %
          (ep.num, ep.slug, lang, total, len(beats), len(shots)))
    return total


def main(argv):
    langs = [a for a in argv if a in model.LANGS] or list(model.LANGS)
    nums = [int(a) for a in argv if a.isdigit()]
    series = [e for e in episodes.SERIES if not nums or e.num in nums]
    grand, files = 0.0, 0
    for lang in langs:
        for ep in series:
            # Only the languages the episode was written or translated into.
            if lang not in ep.langs:
                continue
            grand += build(ep, lang)
            files += 1
    print('\n%d files, %.1f minutes of finished video' % (files, grand / 60))


if __name__ == '__main__':
    main(sys.argv[1:])
