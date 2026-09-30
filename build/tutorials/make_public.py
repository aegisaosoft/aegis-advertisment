# -*- coding: utf-8 -*-
"""Bring what is on YouTube in line with the privacy the series declares.

    python make_public.py            # apply
    python make_public.py --dry-run  # only say what would change

An episode's video privacy is `E.privacy` (see publish.video_privacy), a topic playlist's is
GROUPS[...]['privacy']. Changing either in code does not touch videos already uploaded — this does.
It reads each video's and playlist's current status first and only updates what differs, so a
second run changes nothing, and a run that dies on the daily quota is simply run again.

Written for 2026-09-30, when the partner guides (36-45) were made public after upload.
"""
import io
import json
import os
import sys

import episodes
import publish

HERE = os.path.dirname(os.path.abspath(__file__))


def wanted_videos(state):
    """{videoId: privacy} for every published recording, from its episode's declared privacy."""
    out = {}
    for key, st in state.items():
        vid = st.get('videoId')
        if not vid:
            continue
        try:
            num = int(key.split('-')[2])
        except (IndexError, ValueError):
            continue
        ep = episodes.BY_NUM.get(num)
        if ep is None:
            continue
        out[vid] = publish.video_privacy({'audience': ep.audience, 'privacy': ep.privacy})
    return out


def wanted_playlists():
    """{playlistId: (group, lang, privacy)} for the topic playlists on record."""
    out = {}
    for group, langs in publish.group_ids().items():
        spec = publish.GROUPS.get(group)
        if not spec:
            continue
        for lang, pl in langs.items():
            out[pl] = (group, lang, spec.get('privacy', 'public'))
    return out


def main(dry):
    state = json.loads(io.open(os.path.join(HERE, 'mp4', 'published.json'), encoding='utf-8').read())
    yt = publish.service()
    changed = 0

    for pl, (group, lang, privacy) in wanted_playlists().items():
        cur = publish.call(yt.playlists().list(part='status', id=pl)).get('items', [])
        if not cur or cur[0]['status']['privacyStatus'] == privacy:
            continue
        spec = publish.GROUPS[group]
        print('playlist %s [%s] %s -> %s' % (group, lang, cur[0]['status']['privacyStatus'], privacy))
        if not dry:
            publish.call(yt.playlists().update(part='snippet,status', body={
                'id': pl,
                'snippet': {'title': spec['title'][lang], 'description': spec['description'][lang],
                            'defaultLanguage': publish.LANG[lang]},
                'status': {'privacyStatus': privacy}}))
        changed += 1

    wanted = wanted_videos(state)
    ids = list(wanted)
    for i in range(0, len(ids), 50):                      # videos.list takes up to 50 ids, 1 unit
        for item in publish.call(yt.videos().list(part='status', id=','.join(ids[i:i + 50]))).get('items', []):
            vid, st = item['id'], item['status']
            if st['privacyStatus'] == wanted[vid]:
                continue
            print('video %s %s -> %s' % (vid, st['privacyStatus'], wanted[vid]))
            if not dry:
                publish.call(yt.videos().update(part='status', body={'id': vid, 'status': {
                    'privacyStatus': wanted[vid],
                    'selfDeclaredMadeForKids': st.get('selfDeclaredMadeForKids', False),
                    'embeddable': st.get('embeddable', True),
                    'license': st.get('license', 'youtube'),
                    'publicStatsViewable': st.get('publicStatsViewable', True)}}))
            changed += 1

    print('%s %d item(s)' % ('would change' if dry else 'changed', changed))


if __name__ == '__main__':
    try:
        main('--dry-run' in sys.argv)
    except publish.QuotaOut as e:
        print('Daily quota reached — run again after it resets (midnight Pacific). %s' % str(e)[:160])
        sys.exit(2)
