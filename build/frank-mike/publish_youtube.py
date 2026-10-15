# -*- coding: utf-8 -*-
# Copyright (c) Aegis AO Soft LLC. All rights reserved.
"""Upload the Frank & Mike ad (EN + ES) to the @myeztoll channel, with its captions.

    python publish_youtube.py --dry   # print what would go up, check the channel for twins
    python publish_youtube.py         # upload whatever is not in frank-mike-youtube.json yet

Reuses the tutorial publisher's OAuth token, retry loop and playable() check, so there is
one credential for the channel. State is kept per step (video, captions) next to the
masters; a second run never uploads a video twice.
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'build', 'tutorials'))

STATE = os.path.join(ROOT, 'frank-mike-youtube.json')
CATEGORY_AUTOS = '2'

TAIL_EN = ('Free for fleet owners: no subscription, no set-up fee, nothing per vehicle. '
           'You are paid the toll in full plus a share of the fee we charge the renter.\n\n'
           'https://myeztoll.com\n\n'
           'Aegis AO Soft LLC. Sold and operated under licence by Aegis AG Soft LLC.')

TAIL_ES = ('Gratis para el dueño de la flota: sin suscripción, sin costo de instalación, sin '
           'cargo por vehículo. Recibes el peaje completo, más una parte de la comisión que le '
           'cobramos al cliente.\n\n'
           'https://myeztoll.com\n\n'
           'Aegis AO Soft LLC. Vendido y operado bajo licencia por Aegis AG Soft LLC.')

VIDEOS = {
    'en': {
        'file': os.path.join(ROOT, 'myeztoll-frank-mike-en.mp4'),
        'captions': os.path.join(ROOT, 'myeztoll-frank-mike-en.vtt'),
        'lang': 'en',
        'title': 'Frank and Mike: two rental fleets, same tolls, opposite results | MyEZToll',
        'description': (
            'Two rental fleets. Same street, same roads, same renters.\n\n'
            'Frank pays for every toll his cars run through and every camera notice that '
            'turns up after the car is back, usually past due, with a late fee on top.\n\n'
            "Mike's charges go to MyEZToll. Each one is matched to the booking that was open "
            'at that minute and billed to the card the renter left on file, plus our fee. '
            'Mike gets the toll back in full, and a share of that fee.\n\n' + TAIL_EN),
        'tags': ['myeztoll', 'toll recovery', 'rental fleet', 'car rental', 'tolls',
                 'E-ZPass', 'SunPass', 'camera violations', 'fleet management',
                 'Turo host', 'car rental software', 'toll billing'],
    },
    'es': {
        'file': os.path.join(ROOT, 'myeztoll-frank-mike-es.mp4'),
        'captions': os.path.join(ROOT, 'myeztoll-frank-mike-es.vtt'),
        'lang': 'es-419',
        'title': 'Frank y Mike: dos flotas de renta, los mismos peajes, resultados opuestos | MyEZToll',
        'description': (
            'Dos flotas de renta. La misma calle, las mismas carreteras, los mismos clientes.\n\n'
            'Frank paga cada peaje que cruzan sus autos y cada multa de cámara que llega '
            'cuando el auto ya regresó, casi siempre vencida y con recargo.\n\n'
            'Los cargos de Mike van a MyEZToll. Cada uno se cruza con la reserva que estaba '
            'abierta en ese minuto y se cobra a la tarjeta que el cliente dejó registrada, '
            'más nuestra comisión. Mike recupera el peaje completo, y parte de esa comisión.\n\n'
            + TAIL_ES),
        'tags': ['myeztoll', 'peajes', 'flota de renta', 'renta de autos', 'multas de cámara',
                 'gestión de flotas', 'anfitrión turo', 'recuperación de peajes',
                 'software de renta de autos', 'E-ZPass', 'SunPass'],
    },
}


def body(v):
    return {
        'snippet': {
            'title': v['title'],
            'description': v['description'],
            'tags': v['tags'],
            'categoryId': CATEGORY_AUTOS,
            'defaultLanguage': v['lang'],
            'defaultAudioLanguage': v['lang'],
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False,
            'embeddable': True,
        },
    }


def problems(v):
    """What YouTube would refuse only after the whole file has gone up."""
    out = []
    if len(v['title']) > 100:
        out.append('title over 100 chars')
    if len(v['description'].encode('utf-8')) > 5000:
        out.append('description over 5000 bytes')
    for field in ('title', 'description'):
        if '<' in v[field] or '>' in v[field]:
            out.append('angle bracket in ' + field)
    if len(','.join(v['tags'])) > 450:
        out.append('tags too long')
    return out


def load_state():
    if not os.path.exists(STATE):
        return {}
    return json.loads(io.open(STATE, encoding='utf-8').read())


def save_state(state):
    io.open(STATE, 'w', encoding='utf-8').write(json.dumps(state, indent=1, sort_keys=True))


def channel_titles(yt, call):
    """Titles already on the channel, read from the uploads playlist (search() lags)."""
    me = call(yt.channels().list(part='contentDetails', mine=True))
    uploads = me['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    titles = {}
    req = yt.playlistItems().list(part='snippet', playlistId=uploads, maxResults=50)
    while req is not None:
        res = call(req)
        for it in res.get('items', []):
            titles[it['snippet']['title'].strip()] = it['snippet']['resourceId']['videoId']
        req = yt.playlistItems().list_next(req, res)
    return titles


def main(argv):
    import publish
    from googleapiclient.http import MediaFileUpload

    for key, v in VIDEOS.items():
        bad = problems(v)
        if bad:
            sys.exit('%s: %s' % (key, ', '.join(bad)))
        if not publish.playable(v['file']):
            sys.exit('%s is not a playable mp4' % v['file'])

    yt = publish.service()
    state = load_state()
    on_channel = channel_titles(yt, publish.call)

    for key, v in VIDEOS.items():
        st = state.setdefault(key, {})
        if not st.get('video') and v['title'] in on_channel:
            st['video'] = on_channel[v['title']]
            print('%s: already on the channel as %s, adopted' % (key, st['video']))
        if '--dry' in argv:
            print('%s: %s -> %s' % (key, os.path.basename(v['file']),
                                    st.get('video') or 'would upload'))
            continue
        if not st.get('video'):
            print('%s: uploading %s' % (key, os.path.basename(v['file'])))
            media = MediaFileUpload(v['file'], chunksize=8 * 1024 * 1024, resumable=True,
                                    mimetype='video/mp4')
            req = yt.videos().insert(part='snippet,status', body=body(v), media_body=media)
            resp = None
            while resp is None:
                _, resp = req.next_chunk()
            st['video'] = resp['id']
            save_state(state)
            print('   https://youtu.be/%s' % st['video'])
        if not st.get('captions'):
            import time
            from googleapiclient.errors import HttpError
            cap = {'snippet': {'videoId': st['video'], 'language': v['lang'],
                               'name': '', 'isDraft': False}}
            for attempt in range(4):
                media = MediaFileUpload(v['captions'], mimetype='application/octet-stream',
                                        resumable=False)
                try:
                    publish.call(yt.captions().insert(part='snippet', body=cap,
                                                      media_body=media))
                    st['captions'] = True
                    break
                except HttpError as e:
                    if e.resp.status != 403 or attempt == 3:
                        print('   captions refused (%s), rerun later' % e.resp.status)
                        break
                    time.sleep(20 * (attempt + 1))
            save_state(state)
            print('   captions: %s' % ('ok' if st.get('captions') else 'pending'))
    if '--dry' not in argv:
        save_state(state)


if __name__ == '__main__':
    main(sys.argv[1:])
