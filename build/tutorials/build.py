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

    # ---------------------------------------------------------------- timeline
    beats, cues, t = [], [], TITLE_HOLD
    for i, b in enumerate(ep.beats):
        my = mapper[b.shot]
        cam, cam_here = pick(b.cam, lang)
        point, point_here = pick(b.point, lang)
        ring, ring_here = pick(b.ring, lang)
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
            'eyebrow': '%s · %d' % (episodes.CARD[lang]['eyebrow'], ep.num),
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
    langs = [a for a in argv if a in ('en', 'es')] or ['en', 'es']
    nums = [int(a) for a in argv if a.isdigit()]
    series = [e for e in episodes.SERIES if not nums or e.num in nums]
    grand = 0.0
    for lang in langs:
        for ep in series:
            grand += build(ep, lang)
    print('\n%d files, %.1f minutes of finished video' % (len(series) * len(langs), grand / 60))


if __name__ == '__main__':
    main(sys.argv[1:])
