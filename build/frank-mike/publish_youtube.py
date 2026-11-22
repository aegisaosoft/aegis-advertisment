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
# The channel's OAuth files (client_secret.json, .youtube-token.json) are not in git and live
# next to the tutorial publisher of the main checkout; YT_PUBLISHER points a worktree at it.
sys.path.insert(0, os.environ.get('YT_PUBLISHER') or os.path.join(ROOT, 'build', 'tutorials'))

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

TAIL_NB = ('Gratis for flåteeiere: ingen abonnement, ingen oppstart, ingenting per bil. '
           'Du får hele bompengebeløpet tilbake, pluss en andel av tillegget leietakeren betaler.\n\n'
           'https://myeztoll.com\n\n'
           'Aegis AO Soft LLC. Solgt og drevet på lisens av Aegis AG Soft LLC.')

TAIL_IT = ('Gratis per chi gestisce una flotta: nessun abbonamento, nessuna attivazione, niente per '
           'veicolo. Ti torna tutto il pedaggio, più una quota della commissione che paga il cliente.\n\n'
           'https://myeztoll.com\n\n'
           'Aegis AO Soft LLC. Venduto e gestito su licenza da Aegis AG Soft LLC.')

TAIL_JA = ('車両オーナーは無料です。月額料金なし、初期費用なし、台数課金なし。通行料は全額戻り、'
           '借り手が支払う手数料の一部も受け取れます。\n\n'
           'https://myeztoll.com\n\n'
           'Aegis AO Soft LLC。Aegis AG Soft LLC がライセンスに基づき販売・運営しています。')

TAIL_UZ = ('Avtopark egalari uchun bepul: obuna yoʻq, ulanish toʻlovi yoʻq, mashina uchun toʻlov yoʻq. '
           'Yoʻl toʻlovi sizga toʻliq qaytadi, ustiga ijarachidan olinadigan komissiyadan ulush ham.\n\n'
           'https://myeztoll.com\n\n'
           'Aegis AO Soft LLC. Aegis AG Soft LLC tomonidan litsenziya asosida sotiladi va boshqariladi.')

VIDEOS = {
    # Italian and Japanese cuts of both films (2026-11-22, with the it/ja site and portal).
    'it': {
        'file': os.path.join(ROOT, 'myeztoll-frank-mike-it.mp4'),
        'captions': os.path.join(ROOT, 'myeztoll-frank-mike-it.vtt'),
        'lang': 'it',
        'title': 'Frank e Mike: due flotte a noleggio, stessi pedaggi, risultati opposti | MyEZToll',
        'description': (
            'Due flotte a noleggio. Stessa strada, stesse autostrade, stessi clienti.\n\n'
            'Frank paga ogni pedaggio che le sue auto attraversano e ogni multa che arriva quando '
            "l'auto è già tornata, spesso scaduta e con la mora.\n\n"
            "Gli addebiti di Mike vanno a MyEZToll. Ognuno viene collegato al noleggio aperto in "
            'quel minuto e addebitato sulla carta del cliente, più la nostra commissione. Mike '
            'recupera tutto il pedaggio, e una quota della commissione.\n\n' + TAIL_IT),
        'tags': ['myeztoll', 'pedaggi', 'noleggio auto', 'flotta a noleggio', 'gestione flotta',
                 'multe', 'E-ZPass', 'SunPass', 'Turo', 'software noleggio auto'],
    },
    'toonbee-it': {
        'file': os.path.join(ROOT, 'myeztoll-toonbee-it.mp4'),
        'captions': os.path.join(ROOT, 'myeztoll-toonbee-it.vtt'),
        'lang': 'it',
        'title': 'Le quattro e dodici: il conto del pedaggio che arriva a te | MyEZToll',
        'description': (
            'Martedì, le quattro e dodici del pomeriggio. Una delle tue auto passa a un casello. '
            'Tre settimane dopo arriva il conto, intestato a te, e il cliente è sparito da tempo.\n\n'
            "Il gestore del pedaggio sa quando l'auto è passata. La prenotazione sa chi guidava. "
            'MyEZToll unisce le due cose e addebita sulla carta del cliente, invece di farti '
            'pagare.\n\n' + TAIL_IT),
        'tags': ['myeztoll', 'pedaggi', 'noleggio auto', 'flotta a noleggio', 'gestione flotta',
                 'multe', 'E-ZPass', 'SunPass', 'cliente', 'software noleggio auto'],
    },
    'ja': {
        'file': os.path.join(ROOT, 'myeztoll-frank-mike-ja.mp4'),
        'captions': os.path.join(ROOT, 'myeztoll-frank-mike-ja.vtt'),
        'lang': 'ja',
        'title': 'フランクとマイク：同じ通行料、正反対の結果 | MyEZToll',
        'description': (
            '二つのレンタカー会社。同じ通り、同じ道路、同じ借り手。\n\n'
            'フランクは自社の車が通った通行料も、車が戻ってから届く違反通知も、すべて自腹で払います。'
            '多くは期限切れで、延滞金までついています。\n\n'
            'マイクの請求は MyEZToll に届きます。一件ずつ、その時刻に開いていた予約に結びつけられ、'
            '借り手が登録したカードに手数料込みで請求されます。マイクには通行料が全額戻り、'
            '手数料の一部も入ります。\n\n' + TAIL_JA),
        'tags': ['myeztoll', '通行料', 'レンタカー', 'フリート管理', '違反金', 'E-ZPass',
                 'SunPass', 'Turo', 'カーシェア', 'レンタカーソフト'],
    },
    'toonbee-ja': {
        'file': os.path.join(ROOT, 'myeztoll-toonbee-ja.mp4'),
        'captions': os.path.join(ROOT, 'myeztoll-toonbee-ja.vtt'),
        'lang': 'ja',
        'title': '四時十二分：あなたに届く通行料の請求書 | MyEZToll',
        'description': (
            '火曜日、午後四時十二分。あなたの車の一台が料金所を通過します。'
            '三週間後、あなた宛てに請求書が届く頃には、借り手はもういません。\n\n'
            '料金所側は車が通った時刻を知っています。予約は誰が運転していたかを知っています。'
            'MyEZToll が両者を結びつけ、あなたの代わりに借り手のカードに請求します。\n\n' + TAIL_JA),
        'tags': ['myeztoll', '通行料', 'レンタカー', 'フリート管理', '違反金', 'E-ZPass',
                 'SunPass', '借り手', 'カーシェア', 'レンタカーソフト'],
    },
    # Norwegian cuts of both films (2026-11-21, Norway pilot outreach). The Four-Twelve film
    # is built in ../toonbee; it is published from here so the channel has one uploader.
    'nb': {
        'file': os.path.join(ROOT, 'myeztoll-frank-mike-nb.mp4'),
        'captions': os.path.join(ROOT, 'myeztoll-frank-mike-nb.vtt'),
        'lang': 'no',
        'title': 'Frank og Mike: to utleieflåter, samme bompenger, motsatt resultat | MyEZToll',
        'description': (
            'To utleieflåter. Samme gate, samme veier, samme leietakere.\n\n'
            'Frank betaler for hver bompassering bilene hans kjører gjennom, og for hver bot som '
            'kommer etter at bilen er levert tilbake, ofte forfalt og med gebyr på toppen.\n\n'
            'Mikes passeringer går til MyEZToll. Hver av dem kobles til leieforholdet som var åpent '
            'i det minuttet, og faktureres leietakeren, med vårt tillegg. Mike får hele beløpet '
            'tilbake, og en andel av tillegget.\n\n' + TAIL_NB),
        'tags': ['myeztoll', 'bompenger', 'AutoPASS', 'bilutleie', 'leiebil', 'utleieflåte',
                 'flåtestyring', 'bompassering', 'bøter', 'bildeling'],
    },
    # Uzbek cuts of both films (2026-11-22): narrated in Uzbek since eleven_v4 speaks it.
    'uz': {
        'file': os.path.join(ROOT, 'myeztoll-frank-mike-uz.mp4'),
        'captions': os.path.join(ROOT, 'myeztoll-frank-mike-uz.vtt'),
        'lang': 'uz',
        'title': 'Frank va Mayk: ikki ijara avtoparki, bir xil yoʻl toʻlovlari, teskari natija | MyEZToll',
        'description': (
            'Ikki ijara avtoparki. Bitta koʻcha, bir xil yoʻllar, bir xil ijarachilar.\n\n'
            'Frank mashinalari oʻtgan har bir pullik yoʻl uchun va mashina qaytarilgandan keyin '
            'keladigan har bir jarima uchun oʻzi toʻlaydi, koʻpincha muddati oʻtgan va penyasi bilan.\n\n'
            'Maykning oʻtishlari MyEZTollga boradi. Har biri oʻsha daqiqada ochiq boʻlgan ijaraga '
            'bogʻlanadi va bizning komissiyamiz bilan birga haydovchiga hisoblanadi. Mayk butun '
            'summani qaytarib oladi, ustiga komissiyadan ulush ham.\n\n' + TAIL_UZ),
        'tags': ['myeztoll', 'yoʻl toʻlovi', 'E-ZPass', 'avtomobil ijarasi', 'ijara avtoparki',
                 'avtopark boshqaruvi', 'jarimalar', 'Turo', 'rental fleet', 'tolls'],
    },
    'toonbee-uz': {
        'file': os.path.join(ROOT, 'myeztoll-toonbee-uz.mp4'),
        'captions': os.path.join(ROOT, 'myeztoll-toonbee-uz.vtt'),
        'lang': 'uz',
        'title': 'Toʻrt oʻn ikki: sizga kelib tushadigan yoʻl toʻlovi hisobi | MyEZToll',
        'description': (
            'Seshanba, soat toʻrtdan oʻn ikki daqiqa oʻtganda. Mashinalaringizdan biri pullik yoʻl '
            'punktidan oʻtadi. Uch haftadan keyin hisob sizning nomingizga keladi, ijarachi esa '
            'allaqachon ketib boʻlgan.\n\n'
            'Yoʻl operatori mashina qachon oʻtganini biladi. Bron kim haydaganini biladi. MyEZToll '
            'ikkalasini bogʻlaydi va summani siz toʻlash oʻrniga ijarachining kartasidan yechadi.\n\n'
            + TAIL_UZ),
        'tags': ['myeztoll', 'yoʻl toʻlovi', 'E-ZPass', 'SunPass', 'avtomobil ijarasi',
                 'ijara avtoparki', 'avtopark boshqaruvi', 'jarimalar', 'rental fleet', 'tolls'],
    },
    'toonbee-nb': {
        'file': os.path.join(ROOT, 'myeztoll-toonbee-nb.mp4'),
        'captions': os.path.join(ROOT, 'myeztoll-toonbee-nb.vtt'),
        'lang': 'no',
        'title': 'Tolv over fire: bompengeregningen som havner hos deg | MyEZToll',
        'description': (
            'Tirsdag, tolv over fire. En av bilene dine kjører gjennom en bomstasjon. '
            'Tre uker senere kommer regningen, i ditt navn, og da er leietakeren for lengst borte.\n\n'
            'Bomselskapet vet når bilen passerte. Bookingen vet hvem som kjørte. MyEZToll kobler de '
            'to sammen og trekker beløpet fra leietakerens kort, i stedet for at du betaler det selv.\n\n'
            + TAIL_NB),
        'tags': ['myeztoll', 'bompenger', 'AutoPASS', 'bilutleie', 'leiebil', 'utleieflåte',
                 'flåtestyring', 'bompassering', 'bøter', 'leietaker'],
    },
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

    # Only what still has to go up is checked: the masters are gitignored, so a fresh
    # checkout holds just the cuts built in it, not the ones already on the channel.
    done = load_state()
    for key, v in VIDEOS.items():
        if done.get(key, {}).get('video') and done[key].get('captions'):
            continue
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
