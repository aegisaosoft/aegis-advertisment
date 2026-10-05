# -*- coding: utf-8 -*-
"""Publish the tutorial series through the YouTube Data API — unattended and resumable.

    python publish.py --auth       # once: opens a browser, you click Allow
    python publish.py --status     # what is done, what is left, nothing changes
    python publish.py --adopt      # match videos already on the channel to the queue
    python publish.py              # publish everything still pending
    python publish.py --limit 5    # ... or just the next five
    python publish.py --replace <key> [<key> ...]   # re-upload a corrected episode in place
    python publish.py --refresh <tag>               # new episodes, then re-upload all the rest
    python publish.py --purge-replaced [--yes]      # delete superseded private versions (a person runs this)
    python publish.py --create-playlists            # the topic playlists (GROUPS) that do not exist yet, then fill them

Each episode takes three calls: the video, its caption track, and its playlist entry.
The state file records each step separately, so a run that dies halfway — or is stopped
by the daily quota — resumes exactly where it stopped and never uploads a video twice.

**Why this exists.** Driving YouTube Studio in a browser worked, but it cost about eight
interactions per video and could not attach captions at all, and a resized window twice
made it tick the wrong playlist. The API does the whole thing in three calls and cannot
misclick.

**The quota is the real limit, not the network.** A video insert costs 1600 units against
a default allowance of 10,000 a day, so about six videos a day until a higher quota is
granted. Captions and playlist entries cost 50 each. When the allowance runs out the API
answers `quotaExceeded`; this script stops cleanly, says how many are left, and the next
run picks them up. Nothing is lost by running it again tomorrow.
"""
import io
import json
import os
import sys
import time

# This machine sits behind a TLS-intercepting proxy whose root lives in the Windows store
# and nowhere else, so requests/httplib2 — which trust only certifi's bundle — cannot reach
# Google at all: the OAuth code comes back fine and then the token exchange dies with
# CERTIFICATE_VERIFY_FAILED. truststore hands verification to Windows itself, which accepts
# that root. Exporting the store into a PEM instead does not work: the proxy's certificate is
# malformed in a way OpenSSL refuses ("Basic Constraints not marked critical").
try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(HERE, 'mp4', 'upload-queue.json')
STATE = os.path.join(HERE, 'mp4', 'published.json')
CLIENT_SECRET = os.path.join(HERE, 'client_secret.json')
TOKEN = os.path.join(HERE, '.youtube-token.json')

# Both are needed: upload for the video, force-ssl for captions and playlist items.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube.force-ssl']

PLAYLIST = {
    'en': 'PLDv48XdAqNzM',   # MyEZToll Owner Portal — Full Tutorial Series
    'es': 'PLRAIxpc3U_40',   # Portal del Propietario MyEZToll — Serie completa
}

# Topic playlists beside the series. A newcomer sent a link to "Get Started" sees two videos,
# not thirty-five; the same videos stay in the series playlist at their episode numbers.
# The ids are created once by --create-playlists and kept in mp4/playlists.json, so the
# code names a group and the file remembers what YouTube called it.
GROUPS = {
    'get-started': {
        'episodes': [34, 35],
        'title': {'en': 'Get Started — MyEZToll Owner Portal',
                  'es': 'Primeros pasos — Portal del Propietario MyEZToll'},
        'description': {
            'en': 'How to register with MyEZToll: as a fleet owner, and as a partner who refers '
                  'owners. The sign-up form, the agreement, and connecting the bank account '
                  'through Stripe. Then the two things to do next: toll agencies and cars.\n\n'
                  'Full series: MyEZToll Owner Portal — Full Tutorial Series.\n'
                  'Portal: owner.myeztoll.com',
            'es': 'Cómo registrarse en MyEZToll: como propietario de flota, y como socio que '
                  'recomienda propietarios. El formulario de registro, el contrato, y conectar '
                  'la cuenta bancaria a través de Stripe. Después, las dos cosas que siguen: '
                  'agencias de peaje y coches.\n\n'
                  'Serie completa: Portal del Propietario MyEZToll — Serie completa de tutoriales.\n'
                  'Portal: owner.myeztoll.com',
        },
    },
    # PARTNERS ONLY (E.audience): the three payment options (36-38) and how the
    # amounts themselves are set (39-40).
    'payment-options': {
        'episodes': [36, 37, 38, 39, 40],
        'privacy': 'public',            # user 2026-09-30: every video is visible, the partner guides too
        'title': {'en': 'Payment Options — MyEZToll Partner Guide',
                  'es': 'Formas de pago — Guía para socios MyEZToll'},
        'description': {
            'en': 'For MyEZToll partners. Every owner you bring to us pays the way that suits them. '
                  'Three options: the driver pays us and the owner pays nothing; the owner\'s own '
                  'booking system collects and we invoice only our share; or a flat fee per car '
                  'per day. Then how every amount is set — tolls, fines, rentals, GPS — and what '
                  'you earn.\n\n'
                  'Portal: owner.myeztoll.com',
            'es': 'Para socios de MyEZToll. Cada propietario que nos trae paga de la forma que le '
                  'conviene. Tres opciones: el conductor nos paga y el propietario no paga nada; '
                  'el propio sistema de reservas del propietario cobra y facturamos solo nuestra '
                  'parte; o una tarifa fija por coche y día. Después, cómo se fija cada importe '
                  '— peajes, multas, alquileres, GPS — y lo que usted gana.\n\n'
                  'Portal: owner.myeztoll.com',
        },
    },
    # PARTNERS ONLY (E.audience): the Partner API with examples (41-45).
    'partner-api': {
        'episodes': [41, 42, 43, 44, 45],
        # Public by the user's choice (2026-09-30): the API is not about what an owner pays, so the
        # playlist may be found on the channel. The videos in it stay unlisted (E.audience).
        'privacy': 'public',
        'title': {'en': 'Partner API — MyEZToll Partner Guide',
                  'es': 'API para socios — Guía para socios MyEZToll'},
        'description': {
            'en': 'For MyEZToll partners. The Partner API with examples: your key and the first call, '
                  'cars, drivers and bookings with your own ids, tolls and fines, GPS and webhooks, '
                  'and disputes on your own Stripe account.\n\n'
                  'Reference: owner.myeztoll.com/api/partner/v1/index',
            'es': 'Para socios de MyEZToll. La API para socios con ejemplos: su clave y la primera '
                  'llamada, coches, conductores y reservas con sus propios id, peajes y multas, GPS y '
                  'webhooks, y disputas en su propia cuenta de Stripe.\n\n'
                  'Referencia: owner.myeztoll.com/api/partner/v1/index',
        },
    },
    # Tesla (46-49): connecting a Tesla account, the MyEZToll key and the check, the QR sheet for a
    # lot, and Tesla for Business. 46-48 are owner episodes, 49 is for partners/admins (public).
    'tesla': {
        'episodes': [46, 47, 48, 49],
        'privacy': 'public',
        'title': {'en': 'Tesla — MyEZToll Owner Portal',
                  'es': 'Tesla — Portal del Propietario MyEZToll'},
        'description': {
            'en': 'Tolls for your Teslas with no tracker to install. Connect your Tesla account, add the '
                  'MyEZToll key to each car from a phone inside it, check which cars stream, print a QR '
                  'sheet to do a whole lot in one walk, and connect a Tesla for Business fleet with one '
                  'approval.\n\n'
                  'Portal: owner.myeztoll.com',
            'es': 'Peajes de sus Tesla sin instalar ningún rastreador. Conecte su cuenta de Tesla, agregue '
                  'la llave de MyEZToll a cada coche desde un teléfono dentro de él, revise qué coches '
                  'transmiten, imprima una hoja QR para toda la flota en un solo recorrido, y conecte una '
                  'flota de Tesla for Business con una sola aprobación.\n\n'
                  'Portal: owner.myeztoll.com',
        },
    },
}
GROUPS_FILE = os.path.join(HERE, 'mp4', 'playlists.json')

# YouTube's own language codes. The Spanish is US/Latin-American by design, never es-ES.
LANG = {'en': 'en', 'es': 'es-419'}

CATEGORY_EDUCATION = '27'

TAGS = {
    'en': ['myeztoll', 'fleet management', 'car rental software', 'toll management',
           'rental fleet', 'tolls', 'car sharing', 'turo host', 'fleet owner', 'tutorial'],
    'es': ['myeztoll', 'gestión de flotas', 'software de alquiler de coches',
           'gestión de peajes', 'flota de alquiler', 'peajes', 'carsharing',
           'anfitrión turo', 'dueño de flota', 'tutorial'],
}


# ---------------------------------------------------------------- state


def load(path, default):
    if not os.path.exists(path):
        return default
    return json.loads(io.open(path, encoding='utf-8').read())


def save_state(state):
    io.open(STATE, 'w', encoding='utf-8').write(
        json.dumps(state, ensure_ascii=False, indent=1, sort_keys=True))


def order():
    """Queue keys in the order they should be published: episode 1 upward, en before es.

    Both playlists are sorted by publication date, so uploading in episode order is what
    puts the series in the right order without anyone dragging rows.
    """
    q = load(QUEUE, {})
    return sorted(q, key=lambda k: (q[k]['num'], q[k]['lang'] != 'en'))


# ---------------------------------------------------------------- auth


def service():
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build as build_service

    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        if not os.path.exists(CLIENT_SECRET):
            sys.exit('No client_secret.json next to this script. See the setup notes at '
                     'the bottom of this file.')
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
        creds = flow.run_local_server(port=0, prompt='consent')
    io.open(TOKEN, 'w', encoding='utf-8').write(creds.to_json())
    return build_service('youtube', 'v3', credentials=creds, cache_discovery=False)


class QuotaOut(Exception):
    """The daily allowance is gone. Not an error in the work — just a full day."""


def call(request):
    """Run a request, retrying the transient failures and naming the terminal ones."""
    from googleapiclient.errors import HttpError
    for attempt in range(5):
        try:
            return request.execute()
        except HttpError as e:
            body = (e.content or b'').decode('utf-8', 'replace')
            if 'quotaExceeded' in body or 'uploadLimitExceeded' in body:
                raise QuotaOut(body[:300])
            # 5xx and rate limits are worth waiting out; everything else is a real fault.
            if e.resp.status in (500, 502, 503, 504) or 'rateLimitExceeded' in body:
                time.sleep(2 ** attempt * 3)
                continue
            raise
    raise RuntimeError('gave up after five attempts')


# ---------------------------------------------------------------- steps


def playable(path):
    """True when ffprobe reads a duration: a render cut off mid-write has none.

    YouTube accepts such a file, fails to process it and then deletes the video on its own,
    leaving a dead entry in the playlist -- so it must never be sent.
    """
    import subprocess
    try:
        out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                              '-of', 'csv=p=0', path], capture_output=True, text=True,
                             timeout=60).stdout.strip()
        return float(out) > 1
    except (OSError, ValueError, subprocess.SubprocessError):
        return False


def partner_only(entry):
    """A partner episode (E.audience): never in the public owner series."""
    return entry.get('audience') == 'partner'


def video_privacy(entry):
    """An episode's own choice (E.privacy) wins; otherwise a partner episode is unlisted."""
    return entry.get('privacy') or ('unlisted' if partner_only(entry) else 'public')


def add_to_series(yt, st, entry):
    """Put a video in its language's series playlist — unless it is a partner episode, which
    lives only in its topic playlist. Either way the step is recorded as done."""
    if not partner_only(entry):
        add_to_playlist(yt, st['videoId'], entry['lang'])
    st['playlist'] = True


def upload_video(yt, entry, key):
    from googleapiclient.http import MediaFileUpload
    if not playable(entry['file']):
        raise SystemExit('%s is not a playable mp4 (render cut off?) -- re-render it first'
                         % entry['file'])
    lang = entry['lang']
    body = {
        'snippet': {
            'title': entry['title'],
            'description': entry['description'],
            'tags': TAGS[lang],
            'categoryId': CATEGORY_EDUCATION,
            'defaultLanguage': LANG[lang],
            'defaultAudioLanguage': LANG[lang],
        },
        'status': {
            'privacyStatus': video_privacy(entry),
            'selfDeclaredMadeForKids': False,
            'embeddable': True,
        },
    }
    media = MediaFileUpload(entry['file'], chunksize=8 * 1024 * 1024, resumable=True,
                            mimetype='video/mp4')
    request = yt.videos().insert(part='snippet,status', body=body, media_body=media)
    response, last = None, 0
    while response is None:
        try:
            status, response = request.next_chunk()
        except Exception as e:
            body_text = str(getattr(e, 'content', b'') or b'')
            if 'quotaExceeded' in body_text or 'uploadLimitExceeded' in body_text:
                raise QuotaOut(body_text[:300])
            raise
        if status and int(status.progress() * 100) >= last + 25:
            last = int(status.progress() * 100)
            print('      %d%%' % last)
    return response['id']


def caption_file(key):
    """The .srt beside the mp4 — same stem, whether or not the mp4 was shrunk."""
    p = os.path.join(HERE, 'mp4', key + '.srt')
    return p if os.path.exists(p) else None


def upload_caption(yt, video_id, key, lang):
    from googleapiclient.http import MediaFileUpload
    srt = caption_file(key)
    if not srt:
        return False
    body = {'snippet': {'videoId': video_id, 'language': LANG[lang],
                        'name': '', 'isDraft': False}}
    from googleapiclient.errors import HttpError
    # A caption track attached seconds after the video went up is sometimes refused with a
    # 403 about insufficient permissions — the video is not registered yet and YouTube
    # reports it as an authorisation problem rather than a missing one. Waiting fixes it.
    # If it still refuses, leave the track unattached rather than stopping the whole run:
    # the state file keeps it pending and --status counts it, so a later run picks it up.
    for attempt in range(4):
        media = MediaFileUpload(srt, mimetype='application/octet-stream', resumable=False)
        try:
            call(yt.captions().insert(part='snippet', body=body, media_body=media))
            return True
        except HttpError as e:
            if e.resp.status != 403 or attempt == 3:
                if e.resp.status == 403:
                    print('      captions refused, leaving them for a later run')
                    return False
                raise
            time.sleep(20 * (attempt + 1))
    return False


def add_to_playlist(yt, video_id, lang, playlist_id=None):
    call(yt.playlistItems().insert(part='snippet', body={
        'snippet': {'playlistId': playlist_id or PLAYLIST[lang],
                    'resourceId': {'kind': 'youtube#video', 'videoId': video_id}}}))


def group_ids():
    """{group: {lang: playlistId}} for the topic playlists that exist on the channel."""
    return load(GROUPS_FILE, {})


def groups_of(num):
    """The topic playlists an episode belongs to."""
    return [g for g, spec in GROUPS.items() if num in spec['episodes']]


def add_to_groups(yt, key, entry, st, state):
    """Put a published video into every topic playlist its episode belongs to.

    Runs after the series playlist step, for new uploads and replacements alike; a group
    whose playlist has not been created yet is simply left for --create-playlists, which
    fills it from the state afterwards. Each group costs one playlistItems.insert.
    """
    ids = group_ids()
    for g in groups_of(entry['num']):
        pl = ids.get(g, {}).get(entry['lang'])
        if not pl or st.setdefault('groups', {}).get(g):
            continue
        add_to_playlist(yt, st['videoId'], entry['lang'], pl)
        st['groups'][g] = True
        save_state(state)


def create_playlists(yt, queue, state):
    """Create the topic playlists that do not exist yet, then fill them from the state.

    playlists.insert is 50 units; a playlist already recorded in mp4/playlists.json is
    never created twice. Videos already on the channel that belong to a group are added
    right away, so the command is also the way to fill a group after the fact.
    """
    ids = group_ids()
    for g, spec in GROUPS.items():
        for lang in ('en', 'es'):
            if ids.get(g, {}).get(lang):
                continue
            res = call(yt.playlists().insert(part='snippet,status', body={
                'snippet': {'title': spec['title'][lang],
                            'description': spec['description'][lang],
                            'defaultLanguage': LANG[lang]},
                'status': {'privacyStatus': spec.get('privacy', 'public')}}))
            ids.setdefault(g, {})[lang] = res['id']
            io.open(GROUPS_FILE, 'w', encoding='utf-8').write(
                json.dumps(ids, ensure_ascii=False, indent=1, sort_keys=True))
            print('  created %s [%s]: %s' % (g, lang, res['id']))
    for key in order():
        st = state.get(key, {})
        if st.get('videoId') and (st.get('playlist') or st.get('adopted')):
            add_to_groups(yt, key, queue[key], st, state)
    for g, spec in GROUPS.items():
        for lang in ('en', 'es'):
            n = sum(1 for k, st in state.items()
                    if k.endswith('-' + lang) and st.get('groups', {}).get(g))
            print('  %s [%s]: %d of %d videos in place' % (g, lang, n, len(spec['episodes'])))


# ---------------------------------------------------------------- commands


def adopt(yt, queue, state):
    """Match what is already on the channel to the queue, by exact title.

    Seven episodes went up through the browser before this script existed. Without this
    they would be uploaded a second time.
    """
    mine = {}
    req = yt.search().list(part='snippet', forMine=True, type='video', maxResults=50)
    while req is not None:
        res = call(req)
        for item in res.get('items', []):
            mine[item['snippet']['title'].strip()] = item['id']['videoId']
        req = yt.search().list_next(req, res)
    found = 0
    for key, entry in queue.items():
        vid = mine.get(entry['title'].strip())
        if vid:
            st = state.setdefault(key, {})
            if not st.get('videoId'):
                st['videoId'] = vid
                st['adopted'] = True
                found += 1
    save_state(state)
    print('adopted %d already-published videos' % found)


def status(queue, state):
    todo = [k for k in order() if not state.get(k, {}).get('videoId')]
    caps = [k for k in order() if state.get(k, {}).get('videoId')
            and not state.get(k, {}).get('caption')]
    pls = [k for k in order() if state.get(k, {}).get('videoId')
           and not state.get(k, {}).get('playlist')]
    print('queue %d · uploaded %d · to upload %d' % (len(queue), len(queue) - len(todo), len(todo)))
    print('captions still to attach: %d' % len(caps))
    print('playlist entries still to add: %d' % len(pls))
    ids = group_ids()
    grp = [k for k in order() if state.get(k, {}).get('videoId')
           and any(not state[k].get('groups', {}).get(g) for g in groups_of(queue[k]['num']))]
    missing = [g for g in GROUPS if not ids.get(g)]
    if grp or missing:
        print('topic playlist entries still to add: %d%s' %
              (len(grp), ' (create first: %s)' % ', '.join(missing) if missing else ''))
    if todo:
        print('next up: ' + ', '.join(todo[:6]) + (' …' if len(todo) > 6 else ''))


def run(yt, queue, state, limit):
    done = 0
    for key in order():
        if limit is not None and done >= limit:
            break
        entry = queue[key]
        st = state.setdefault(key, {})
        try:
            if not st.get('videoId'):
                print('  %s  (%.1f MB)' % (key, os.path.getsize(entry['file']) / 1048576))
                st['videoId'] = upload_video(yt, entry, key)
                save_state(state)
                print('      video %s' % st['videoId'])
                done += 1
            if not st.get('caption'):
                st['caption'] = upload_caption(yt, st['videoId'], key, entry['lang'])
                save_state(state)
            if not st.get('playlist'):
                add_to_series(yt, st, entry)
                save_state(state)
            add_to_groups(yt, key, entry, st, state)
        except QuotaOut as e:
            save_state(state)
            print('\nDaily quota reached — stopping cleanly. %s' % str(e)[:160])
            print('Run this again tomorrow; everything finished so far is recorded.')
            return
    print('\nnothing left to do' if not done else '\n%d video(s) published this run' % done)


def retired_ids(state):
    """Every superseded video id on record: finished replacements plus their history."""
    out = []
    for key in sorted(state):
        st = state[key]
        ids = list(st.get('retired', []))
        if st.get('replaces') and st.get('oldHidden'):
            ids.append(st['replaces'])
        for vid in ids:
            if vid and vid != st.get('videoId') and vid not in st.get('purged', []):
                out.append((key, vid))
    return out


def purge_replaced(yt, state, really):
    """Delete superseded versions for good -- run by a person, never on a schedule.

    Only ids this script itself retired are candidates, and only those YouTube reports as
    private are deleted: a public video is never touched, whatever the state file says.
    Without --yes it lists what it would delete and stops.
    """
    todo = retired_ids(state)
    if not todo:
        print('nothing to purge')
        return
    ids = [vid for _, vid in todo]
    status = {}
    for i in range(0, len(ids), 50):
        res = call(yt.videos().list(part='status,snippet', id=','.join(ids[i:i + 50])))
        for it in res.get('items', []):
            status[it['id']] = (it['status']['privacyStatus'], it['snippet']['title'])
    for key, vid in todo:
        priv, title = status.get(vid, ('gone', ''))
        if priv == 'gone':
            state[key].setdefault('purged', []).append(vid)       # already deleted by hand
            print('  %s  already gone' % vid)
            continue
        if priv != 'private':
            print('  %s  SKIPPED: it is %s, not private — %s' % (vid, priv, title))
            continue
        if not really:
            print('  %s  would delete — %s' % (vid, title))
            continue
        try:
            call(yt.videos().delete(id=vid))
        except QuotaOut as e:
            save_state(state)
            print('\nDaily quota reached — run the same command tomorrow, the rest is still '
                  'on record. %s' % str(e)[:160])
            return
        state[key].setdefault('purged', []).append(vid)
        save_state(state)
        print('  %s  deleted — %s' % (vid, title))
    save_state(state)
    if not really:
        print('\nNothing deleted. Run again with --yes to delete the ones marked "would delete".')


def refresh_plan(queue, state, tag):
    """Which keys a `--refresh TAG` run still has to do, new episodes first.

    A key is done for this refresh once its state carries `rev == TAG`. Never-published keys
    go first -- they are new content and simply append to the playlist in episode order --
    then the published ones, each re-uploaded in place, in episode order.
    """
    todo = [k for k in order() if k in queue and state.get(k, {}).get('rev') != tag]
    new = [k for k in todo if not was_published(state.get(k, {}))]
    return new + [k for k in todo if k not in new]


def was_published(st):
    """Published before this refresh: finished (in its playlist) or mid-replacement. A video
    uploaded by this refresh whose caption or playlist step the day's limit cut off is NOT --
    it is finished, never re-uploaded."""
    return bool(st.get('replaces') or (st.get('videoId') and st.get('playlist')))


def refresh(yt, queue, state, tag, limit=None):
    """Upload everything that is new and re-upload everything already published, stopping
    cleanly at the day's upload limit. Run it again the next day with the same tag."""
    done = 0
    for key in refresh_plan(queue, state, tag):
        if limit is not None and done >= limit:
            break
        st = state.setdefault(key, {})
        entry = queue[key]
        try:
            if was_published(st):                            # published: re-upload in place
                replace(yt, queue, state, [key])
                if not state[key].get('oldHidden'):
                    return      # the quota ran out inside the replacement
            else:
                print('  %s  (%.1f MB) new' % (key, os.path.getsize(entry['file']) / 1048576))
                if not st.get('videoId'):
                    st['videoId'] = upload_video(yt, entry, key)
                    save_state(state)
                if not st.get('caption'):
                    st['caption'] = upload_caption(yt, st['videoId'], key, entry['lang'])
                    save_state(state)
                if not st.get('playlist'):
                    add_to_series(yt, st, entry)
                    save_state(state)
                add_to_groups(yt, key, entry, st, state)
            state[key]['rev'] = tag
            save_state(state)
            done += 1
        except QuotaOut as e:
            save_state(state)
            print('\nDaily limit reached — run the same command tomorrow. %s' % str(e)[:160])
            return
    left = len(refresh_plan(queue, state, tag))
    print('\n%d done this run, %d left for refresh %s' % (done, left, tag))


def begin_replace(state, key):
    """Mark a published episode for re-upload, keeping the id it replaces.

    YouTube cannot swap the file under an existing video, so a corrected episode is a new
    video. The old id moves to `replaces` and the upload steps are cleared; `replaces`
    survives a crash, so the new video still lands in the old one's playlist slot and the
    old one is still hidden on the next run. Calling it again mid-replacement is a no-op;
    once a replacement has finished, calling it again starts the next one.
    """
    st = state.setdefault(key, {})
    if st.get('replaces') and not st.get('oldHidden'):
        return st                       # a replacement already under way
    if not st.get('videoId'):
        raise ValueError('%s was never published, nothing to replace' % key)
    # Every version this one supersedes stays on record until --purge-replaced removes it.
    if st.get('replaces'):
        st.setdefault('retired', [])
        if st['replaces'] not in st['retired']:
            st['retired'].append(st['replaces'])
    st['replaces'] = st['videoId']
    for k in ('videoId', 'caption', 'playlist', 'adopted', 'oldHidden', 'groups'):
        st.pop(k, None)
    return st


def playlist_item_of(yt, playlist_id, video_id):
    req = yt.playlistItems().list(part='snippet', playlistId=playlist_id, maxResults=50)
    while req is not None:
        res = call(req)
        for item in res.get('items', []):
            if item['snippet']['resourceId']['videoId'] == video_id:
                return item
        req = yt.playlistItems().list_next(req, res)
    return None


def episode_of(state, lang):
    """video id -> episode number, for the live video and the one it is replacing."""
    out = {}
    for key, st in state.items():
        if not key.endswith('-' + lang):
            continue
        num = int(key.split('-')[2])
        for vid in [st.get('videoId'), st.get('replaces')] + st.get('retired', []):
            if vid:
                out.setdefault(vid, num)
    return out


def playlist_moves(current, rank):
    """Moves that put `current` (video ids in playlist order) into episode order.

    Returns [(video_id, position)] to apply one after another, each a YouTube position
    update. Videos the state does not know keep their relative order after the series.
    Only videos out of place are moved, so an already sorted playlist costs nothing.
    """
    want = sorted(current, key=lambda v: (rank.get(v, 10 ** 6), current.index(v)))
    now, moves = list(current), []
    for pos, vid in enumerate(want):
        if now[pos] != vid:
            now.remove(vid)
            now.insert(pos, vid)
            moves.append((vid, pos))
    return moves


def sort_playlists(yt, state):
    """Put every playlist — the two series ones and the topic ones — in episode order."""
    lists = list(PLAYLIST.items())
    for g, per_lang in group_ids().items():
        lists += [(lang, pl) for lang, pl in per_lang.items()]
    for lang, pl in lists:
        items = []
        req = yt.playlistItems().list(part='snippet', playlistId=pl, maxResults=50)
        while req is not None:
            res = call(req)
            items += res.get('items', [])
            req = yt.playlistItems().list_next(req, res)
        items.sort(key=lambda it: it['snippet']['position'])
        by_vid = {it['snippet']['resourceId']['videoId']: it for it in items}
        moves = playlist_moves(list(by_vid), episode_of(state, lang))
        print('  %s: %d videos, %d to move' % (lang, len(items), len(moves)))
        for vid, pos in moves:
            it = by_vid[vid]
            call(yt.playlistItems().update(part='snippet', body={
                'id': it['id'],
                'snippet': {'playlistId': pl, 'position': pos,
                            'resourceId': it['snippet']['resourceId']}}))


def keep_order(yt, state):
    """After any upload run: put the playlists back in episode order.

    A replacement lands in its old slot when YouTube allows it, but a fallback insert or a
    new episode goes to the end; this repairs both. Out of quota, the next run does it.
    """
    try:
        sort_playlists(yt, state)
    except QuotaOut:
        print('  playlist order: out of quota, the next run will sort them')


def hide_video(yt, video_id):
    """Make a superseded video private; one already deleted counts as hidden."""
    from googleapiclient.errors import HttpError
    try:
        call(yt.videos().update(part='status', body={
            'id': video_id, 'status': {'privacyStatus': 'private',
                                       'selfDeclaredMadeForKids': False}}))
    except HttpError as e:
        if e.resp.status != 404 and 'videoNotFound' not in str(e.content):
            raise
        print('      %s is already gone, nothing to hide' % video_id)


def replace(yt, queue, state, keys):
    """Re-upload corrected episodes in place of the published ones.

    The new video takes the old one's position in the playlist (the playlists are
    manually sorted, so a plain insert would land it at the end), the old entry leaves the
    playlist, and the old video goes private. Private, not deleted: deleting is final and
    loses its view count, so that is left to a person in Studio.
    """
    for key in keys:
        if key not in queue:
            sys.exit('%s is not in the upload queue' % key)
        entry = queue[key]
        if partner_only(entry):
            # The slot swap below works on the series playlist, where a partner episode never is.
            sys.exit('%s is a partner episode: replace it by hand in Studio (unlisted, topic '
                     'playlist only) -- --replace does not handle those yet' % key)
        st = begin_replace(state, key)
        save_state(state)
        old = st['replaces']
        pl = PLAYLIST[entry['lang']]
        try:
            if not st.get('videoId'):
                print('  %s  (%.1f MB) replacing %s' % (
                    key, os.path.getsize(entry['file']) / 1048576, old))
                st['videoId'] = upload_video(yt, entry, key)
                save_state(state)
                print('      video %s' % st['videoId'])
            if not st.get('caption'):
                st['caption'] = upload_caption(yt, st['videoId'], key, entry['lang'])
                save_state(state)
            if not st.get('playlist'):
                old_item = playlist_item_of(yt, pl, old)
                snippet = {'playlistId': pl,
                           'resourceId': {'kind': 'youtube#video', 'videoId': st['videoId']}}
                if old_item is not None:
                    snippet['position'] = old_item['snippet']['position']
                if playlist_item_of(yt, pl, st['videoId']) is None:
                    from googleapiclient.errors import HttpError
                    try:
                        call(yt.playlistItems().insert(part='snippet', body={'snippet': snippet}))
                    except HttpError as e:
                        # A playlist sorted by date refuses a position, and the sort type
                        # can only be switched in Studio. Insert anyway and say so.
                        if 'manualSortRequired' not in str(e.content) or 'position' not in snippet:
                            raise
                        del snippet['position']
                        call(yt.playlistItems().insert(part='snippet', body={'snippet': snippet}))
                        print('      playlist is not manually sorted: added at the default '
                              'place — set Manual order in Studio and move it to #%d'
                              % (old_item['snippet']['position'] + 1))
                if old_item is not None:
                    call(yt.playlistItems().delete(id=old_item['id']))
                st['playlist'] = True
                save_state(state)
            if not st.get('oldHidden'):
                hide_video(yt, old)
                st['oldHidden'] = True
                save_state(state)
            print('      done: %s -> %s (old one is private)' % (old, st['videoId']))
        except QuotaOut as e:
            save_state(state)
            print('\nDaily quota reached — run the same command tomorrow. %s' % str(e)[:160])
            return


def main(argv):
    queue = load(QUEUE, {})
    state = load(STATE, {})
    if not queue:
        sys.exit('No mp4/upload-queue.json — run youtube.py first.')

    if '--status' in argv and '--auth' not in argv and '--adopt' not in argv:
        return status(queue, state)

    yt = service()
    if '--auth' in argv:
        me = call(yt.channels().list(part='snippet', mine=True))
        items = me.get('items') or []
        if not items:
            # A Brand Account channel does not belong to the Google account itself. Consent
            # given by the plain account authorises nothing to upload to, and the failure
            # would otherwise only surface at the first upload.
            sys.exit('That account has no YouTube channel of its own, so nothing here could '
                     'be uploaded. On the account chooser pick the row named after the '
                     'channel, not the row with a personal name. Delete .youtube-token.json '
                     'and run --auth again.')
        print('authorised as: %s (%s)' % (items[0]['snippet']['title'], items[0]['id']))
        return
    if '--adopt' in argv:
        return adopt(yt, queue, state)
    if '--replace' in argv:
        replace(yt, queue, state, argv[argv.index('--replace') + 1:])
        return keep_order(yt, state)
    if '--sort-playlists' in argv:
        return sort_playlists(yt, state)
    if '--create-playlists' in argv:
        create_playlists(yt, queue, state)
        return keep_order(yt, state)
    if '--purge-replaced' in argv:
        return purge_replaced(yt, state, '--yes' in argv)
    if '--refresh' in argv:
        lim = int(argv[argv.index('--limit') + 1]) if '--limit' in argv else None
        refresh(yt, queue, state, argv[argv.index('--refresh') + 1], lim)
        return keep_order(yt, state)

    limit = None
    if '--limit' in argv:
        limit = int(argv[argv.index('--limit') + 1])
    run(yt, queue, state, limit)
    keep_order(yt, state)


if __name__ == '__main__':
    main(sys.argv[1:])


# ---------------------------------------------------------------- setup notes
#
# One-time, and only you can do it — it is your Google account:
#
#   1. console.cloud.google.com → create a project (any name).
#   2. APIs & Services → Library → enable "YouTube Data API v3".
#   3. APIs & Services → OAuth consent screen → External → fill in the app name and your
#      email → add yourself under "Test users". It does not need verifying by Google:
#      a test user can authorise it, which is all this needs.
#   4. Credentials → Create credentials → OAuth client ID → Desktop app → Download JSON.
#   5. Save that file next to this script as `client_secret.json`.
#   6. `python publish.py --auth` → a browser opens → Allow. The token is written to
#      `.youtube-token.json` and refreshes itself after that.
#
# Neither file belongs in git. `client_secret.json` identifies the app and
# `.youtube-token.json` is a live credential for the channel.
#
# If six videos a day is too slow: in the Cloud console, IAM & Admin → Quotas, filter to
# YouTube Data API, and request more. It is free and takes a few days to be reviewed.
