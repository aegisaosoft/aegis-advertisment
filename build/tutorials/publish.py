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
            'privacyStatus': 'public',
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


def add_to_playlist(yt, video_id, lang):
    call(yt.playlistItems().insert(part='snippet', body={
        'snippet': {'playlistId': PLAYLIST[lang],
                    'resourceId': {'kind': 'youtube#video', 'videoId': video_id}}}))


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
                add_to_playlist(yt, st['videoId'], entry['lang'])
                st['playlist'] = True
                save_state(state)
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
        call(yt.videos().delete(id=vid))
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
                    add_to_playlist(yt, st['videoId'], entry['lang'])
                    st['playlist'] = True
                    save_state(state)
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
    for k in ('videoId', 'caption', 'playlist', 'adopted', 'oldHidden'):
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
    """Put both playlists in episode order, 1 to the last."""
    for lang, pl in PLAYLIST.items():
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
