# -*- coding: utf-8 -*-
"""Write aa-web's `client/src/data/tutorials.ts` from what is actually on YouTube.

    python site_tutorials.py

Each language lists only a recording YouTube actually serves in public -- checked through
oEmbed, which costs no API quota and answers 404 for a private, deleted or failed video. An
episode whose other language is being re-uploaded still shows in the language that works.
Ids come from mp4/published.json and change on every re-upload, so this runs after each
publishing day, never by hand.
The runtime is the English cut's, read off the built timeline.
"""
import io
import json
import os

import urllib.error
import urllib.request

import episodes
import youtube

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = r'C:\aegis-aa\aegis-aa-web\client\src\data\tutorials.ts'
MARK = 'export const TUTORIALS: TutorialEpisode[] = ['


def ts(s):
    return "'" + s.replace('\\', '\\\\').replace("'", "\\'") + "'"


def live_id(st):
    """The id a viewer can watch right now, or None.

    A finished upload is the new video. Mid-replacement (new one uploaded but not yet in its
    playlist) the old one is still public and still in the playlist, so the site keeps it.
    """
    if st.get('videoId') and st.get('playlist'):
        return st['videoId']
    if st.get('replaces') and not st.get('oldHidden'):
        return st['replaces']
    return None


def is_public(video_id):
    """True when anyone can watch the video; oEmbed needs no key and no quota."""
    url = ('https://www.youtube.com/oembed?format=json&url='
           'https://www.youtube.com/watch?v=' + video_id)
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            return r.status == 200
    except urllib.error.HTTPError:
        return False


def recordings(state_for, public=is_public):
    """lang -> video id for the recordings of one episode that can be watched now."""
    out = {}
    for lang, st in state_for.items():
        vid = live_id(st)
        if vid and public(vid):
            out[lang] = vid
        elif vid:
            old = st.get('replaces')
            if old and old != vid and public(old):
                out[lang] = old
    return out


def main():
    state = json.loads(io.open(os.path.join(HERE, 'mp4', 'published.json'), encoding='utf-8').read())
    rows = []
    for ep in episodes.SERIES:
        recs = recordings({lang: state.get('myeztoll-tutorial-%02d-%s-%s' % (ep.num, ep.slug, lang), {})
                           for lang in ('en', 'es')})
        if not recs:
            continue
        film = youtube.timeline(ep, 'en')
        rows.append((ep, recs, youtube.clock(film['total']) if film else '0:00'))

    body = []
    for ep, recs, dur in rows:
        body.append('  {')
        body.append('    n: %d,' % ep.num)
        body.append("    slug: '%s'," % ep.slug)
        body.append("    duration: '%s'," % dur)
        for lang in [l for l in ('en', 'es') if l in recs]:
            title = '%s — %d. %s' % (youtube.SERIES_NAME[lang], ep.num, ep.title[lang])
            body.append('    %s: {' % lang)
            body.append('      title: %s,' % ts(title))
            body.append('      summary: %s,' % ts(ep.sub[lang]))
            body.append("      videoId: '%s'," % recs[lang])
            body.append('    },')
        body.append('  },')

    src = io.open(OUT, encoding='utf-8').read()
    head = src[:src.index(MARK) + len(MARK)]
    io.open(OUT, 'w', encoding='utf-8').write(head + '\n' + '\n'.join(body) + '\n];\n')
    print('tutorials.ts: %d episodes (%s)' % (len(rows), ', '.join(
        str(r[0].num) + ('' if len(r[1]) == 2 else ' ' + '/'.join(r[1]) + ' only') for r in rows)))


if __name__ == '__main__':
    main()
