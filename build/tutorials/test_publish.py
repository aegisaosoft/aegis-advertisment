# -*- coding: utf-8 -*-
import os
"""The replace bookkeeping in publish.py — run: python test_publish.py"""
import sys

import publish


def test_begin_replace_moves_old_id_and_clears_steps():
    state = {'k': {'videoId': 'OLD', 'caption': True, 'playlist': True, 'adopted': True}}
    st = publish.begin_replace(state, 'k')
    assert st == {'replaces': 'OLD'}, st


def test_begin_replace_is_idempotent_mid_replacement():
    state = {'k': {'replaces': 'OLD', 'videoId': 'NEW', 'caption': True}}
    st = publish.begin_replace(state, 'k')
    assert st == {'replaces': 'OLD', 'videoId': 'NEW', 'caption': True}, st


def test_begin_replace_after_finished_replacement_starts_a_new_one():
    state = {'k': {'replaces': 'OLD', 'videoId': 'NEW', 'caption': True,
                   'playlist': True, 'oldHidden': True}}
    st = publish.begin_replace(state, 'k')
    assert st == {'replaces': 'NEW', 'retired': ['OLD']}, st


def test_begin_replace_refuses_unpublished():
    try:
        publish.begin_replace({}, 'k')
    except ValueError:
        return
    raise AssertionError('expected ValueError')

def test_refresh_plan_puts_new_episodes_first_and_skips_done():
    import publish as p
    queue = {'a-01-x-en': {'num': 1, 'lang': 'en'}, 'a-02-x-en': {'num': 2, 'lang': 'en'},
             'a-22-x-en': {'num': 22, 'lang': 'en'}}
    state = {'a-01-x-en': {'videoId': 'V1', 'playlist': True},
             'a-02-x-en': {'videoId': 'V2', 'rev': 'yc'}}
    old_order = p.order
    p.order = lambda: sorted(queue, key=lambda k: queue[k]['num'])
    try:
        assert p.refresh_plan(queue, state, 'yc') == ['a-22-x-en', 'a-01-x-en']
    finally:
        p.order = old_order

def test_second_replacement_keeps_the_first_old_id_in_retired():
    import publish as p
    state = {'k': {'replaces': 'OLD1', 'videoId': 'NEW1', 'caption': True,
                   'playlist': True, 'oldHidden': True}}
    p.begin_replace(state, 'k')
    assert state['k']['retired'] == ['OLD1'] and state['k']['replaces'] == 'NEW1'


def test_retired_ids_lists_finished_replacements_never_the_live_video():
    import publish as p
    state = {'a': {'videoId': 'LIVE', 'replaces': 'OLD2', 'oldHidden': True, 'retired': ['OLD1']},
             'b': {'videoId': 'LIVE_B', 'replaces': 'MID', 'oldHidden': False},
             'c': {'videoId': 'LIVE_C', 'retired': ['GONE'], 'purged': ['GONE']}}
    assert p.retired_ids(state) == [('a', 'OLD1'), ('a', 'OLD2')]

def test_upload_cut_off_before_its_playlist_step_is_finished_not_replaced():
    import publish as p
    assert not p.was_published({'videoId': 'B9'})
    assert p.was_published({'videoId': 'V', 'playlist': True})
    assert p.was_published({'videoId': 'V', 'replaces': 'O'})


if __name__ == '__main__':
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    for t in tests:
        t()
    print('ok: %d tests' % len(tests))
    sys.exit(0)


def test_every_youtube_title_fits_the_100_character_limit():
    # YouTube rejects a longer title with invalidTitle, and only after the whole file is sent.
    import episodes
    import youtube
    for ep in episodes.SERIES:
        for lang in ('en', 'es'):
            title = '%s — %d. %s' % (youtube.SERIES_NAME[lang], ep.num, ep.title[lang])
            assert len(title) <= 100, (ep.num, lang, len(title))


def test_playlist_moves_sorts_by_episode_and_leaves_sorted_lists_alone():
    rank = {'a': 1, 'b': 2, 'c': 3, 'd': 26}
    cur = ['c', 'a', 'd', 'b']
    moves = publish.playlist_moves(cur, rank)
    now = list(cur)
    for vid, pos in moves:
        now.remove(vid)
        now.insert(pos, vid)
    assert now == ['a', 'b', 'c', 'd']
    assert publish.playlist_moves(['a', 'b', 'c', 'd'], rank) == []


def test_playlist_moves_puts_unknown_videos_after_the_series():
    moves = publish.playlist_moves(['x', 'b', 'a'], {'a': 1, 'b': 2})
    now = ['x', 'b', 'a']
    for vid, pos in moves:
        now.remove(vid)
        now.insert(pos, vid)
    assert now == ['a', 'b', 'x']


def test_episode_of_maps_live_and_replaced_ids_per_language():
    state = {'myeztoll-tutorial-09-tolls-en': {'videoId': 'new', 'replaces': 'old'},
             'myeztoll-tutorial-09-tolls-es': {'videoId': 'es'}}
    assert publish.episode_of(state, 'en') == {'new': 9, 'old': 9}


def test_keep_order_survives_running_out_of_quota(monkeypatch):
    def out(yt, state):
        raise publish.QuotaOut('quotaExceeded')
    monkeypatch.setattr(publish, 'sort_playlists', out)
    publish.keep_order(None, {})        # must not raise: the next run sorts instead


def test_keep_order_sorts_after_a_run(monkeypatch):
    seen = []
    monkeypatch.setattr(publish, 'sort_playlists', lambda yt, state: seen.append(state))
    publish.keep_order(None, {'k': 1})
    assert seen == [{'k': 1}]


class _Resp(dict):
    def __init__(self, status):
        super().__init__()
        self.status = status
        self.reason = ''


class _Videos:
    def __init__(self, status):
        self.status = status

    def update(self, **kw):
        from googleapiclient.errors import HttpError
        status = self.status

        class R:
            def execute(self):
                reason = b'videoNotFound' if status == 404 else b'forbidden'
                raise HttpError(_Resp(status), b'{"error": {"errors": [{"reason": "' + reason + b'"}]}}')
        return R()


class _YT:
    def __init__(self, status):
        self._v = _Videos(status)

    def videos(self):
        return self._v


def test_hide_video_treats_a_deleted_video_as_hidden():
    publish.hide_video(_YT(404), 'gone')     # must not raise


def test_hide_video_still_raises_other_errors():
    import pytest
    from googleapiclient.errors import HttpError
    with pytest.raises(HttpError):
        publish.hide_video(_YT(403), 'x')


def test_playable_rejects_a_truncated_or_missing_file(tmp_path):
    bad = tmp_path / 'cut.mp4'
    bad.write_bytes(b'\x00\x00\x00\x18ftypmp42' + b'\x00' * 4096)   # header, no moov atom
    assert not publish.playable(str(bad))
    assert not publish.playable(str(tmp_path / 'missing.mp4'))


def test_playable_accepts_a_finished_render():
    import glob
    good = sorted(glob.glob(os.path.join(publish.HERE, 'mp4', '*-03-*-en.mp4')))
    if good:
        assert publish.playable(good[0])


def test_purge_stops_cleanly_when_the_quota_runs_out(monkeypatch, capsys):
    state = {'k': {'videoId': 'new', 'replaces': 'old', 'oldHidden': True}}

    class _Del:
        def list(self, **kw):
            class R:
                def execute(self_inner):
                    return {'items': [{'id': 'old', 'status': {'privacyStatus': 'private'},
                                       'snippet': {'title': 'old one'}}]}
            return R()

        def delete(self, **kw):
            raise publish.QuotaOut('quotaExceeded')

    class _YT2:
        def videos(self):
            return _Del()

    monkeypatch.setattr(publish, 'call', lambda req: req.execute())
    monkeypatch.setattr(publish, 'save_state', lambda st: None)
    publish.purge_replaced(_YT2(), state, True)          # must not raise
    assert 'quota' in capsys.readouterr().out.lower()
    assert 'purged' not in state['k']                    # nothing recorded as deleted


# ---------------------------------------------------------------- topic playlists


def test_groups_of_names_the_get_started_episodes_only():
    assert publish.groups_of(34) == ['get-started']
    assert publish.groups_of(35) == ['get-started']
    assert publish.groups_of(36) == ['payment-options']
    assert publish.groups_of(40) == ['payment-options']
    assert publish.groups_of(33) == []
    assert publish.groups_of(33) == []


def test_begin_replace_clears_group_entries_too():
    state = {'k': {'videoId': 'OLD', 'caption': True, 'playlist': True, 'groups': {'get-started': True}}}
    st = publish.begin_replace(state, 'k')
    assert st == {'replaces': 'OLD'}, st


def test_add_to_groups_inserts_once_per_group_and_records_it(monkeypatch):
    inserted = []
    monkeypatch.setattr(publish, 'group_ids', lambda: {'get-started': {'en': 'PL_GS_EN'}})
    monkeypatch.setattr(publish, 'add_to_playlist',
                        lambda yt, vid, lang, pl=None: inserted.append((vid, lang, pl)))
    monkeypatch.setattr(publish, 'save_state', lambda st: None)
    state = {'k': {'videoId': 'V34'}}
    entry = {'num': 34, 'lang': 'en'}
    publish.add_to_groups(None, 'k', entry, state['k'], state)
    publish.add_to_groups(None, 'k', entry, state['k'], state)     # a second call adds nothing
    assert inserted == [('V34', 'en', 'PL_GS_EN')]
    assert state['k']['groups'] == {'get-started': True}


def test_add_to_groups_waits_for_a_playlist_that_does_not_exist_yet(monkeypatch):
    monkeypatch.setattr(publish, 'group_ids', lambda: {})
    monkeypatch.setattr(publish, 'add_to_playlist',
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError('must not insert')))
    state = {'k': {'videoId': 'V34'}}
    publish.add_to_groups(None, 'k', {'num': 34, 'lang': 'es'}, state['k'], state)
    assert 'groups' not in state['k'] or not state['k']['groups']


def test_add_to_groups_ignores_episodes_outside_every_group(monkeypatch):
    monkeypatch.setattr(publish, 'group_ids', lambda: {'get-started': {'en': 'PL'}})
    monkeypatch.setattr(publish, 'add_to_playlist',
                        lambda *a, **k: (_ for _ in ()).throw(AssertionError('must not insert')))
    state = {'k': {'videoId': 'V1'}}
    publish.add_to_groups(None, 'k', {'num': 1, 'lang': 'en'}, state['k'], state)


def test_create_playlists_creates_only_the_missing_ones_and_fills_them(monkeypatch, tmp_path):
    created, inserted = [], []

    class _PL:
        def insert(self, part, body):
            class R:
                def execute(self_inner):
                    created.append(body['snippet']['title'])
                    return {'id': 'NEW_%d' % len(created)}
            return R()

    class _YT:
        def playlists(self):
            return _PL()

    # One group is enough to prove the rule; the real GROUPS grows with the series.
    monkeypatch.setattr(publish, 'GROUPS', {'get-started': publish.GROUPS['get-started']})
    monkeypatch.setattr(publish, 'GROUPS_FILE', str(tmp_path / 'playlists.json'))
    monkeypatch.setattr(publish, 'call', lambda req: req.execute())
    monkeypatch.setattr(publish, 'save_state', lambda st: None)
    monkeypatch.setattr(publish, 'order', lambda: ['a-34-x-en', 'a-34-x-es', 'a-01-x-en'])
    monkeypatch.setattr(publish, 'add_to_playlist',
                        lambda yt, vid, lang, pl=None: inserted.append((vid, lang, pl)))
    import json as _json
    (tmp_path / 'playlists.json').write_text(_json.dumps({'get-started': {'en': 'HAVE_EN'}}))
    queue = {'a-34-x-en': {'num': 34, 'lang': 'en'}, 'a-34-x-es': {'num': 34, 'lang': 'es'},
             'a-01-x-en': {'num': 1, 'lang': 'en'}}
    state = {'a-34-x-en': {'videoId': 'V_EN', 'playlist': True},
             'a-34-x-es': {'videoId': 'V_ES', 'playlist': True},
             'a-01-x-en': {'videoId': 'V1', 'playlist': True}}
    publish.create_playlists(_YT(), queue, state)
    assert created == [publish.GROUPS['get-started']['title']['es']]        # en already existed
    assert publish.group_ids() == {'get-started': {'en': 'HAVE_EN', 'es': 'NEW_1'}}
    assert sorted(inserted) == [('V_EN', 'en', 'HAVE_EN'), ('V_ES', 'es', 'NEW_1')]
    assert state['a-34-x-en']['groups'] == {'get-started': True}
    assert 'groups' not in state['a-01-x-en']


def test_partner_episode_is_unlisted_and_skips_the_series_playlist(monkeypatch):
    added = []
    monkeypatch.setattr(publish, 'add_to_playlist', lambda yt, vid, lang, pl=None: added.append((vid, lang)))
    st = {'videoId': 'V'}
    publish.add_to_series(None, st, {'lang': 'en', 'audience': 'partner'})
    assert added == [] and st['playlist'] is True
    st = {'videoId': 'W'}
    publish.add_to_series(None, st, {'lang': 'en', 'audience': 'owner'})
    assert added == [('W', 'en')] and st['playlist'] is True
    assert publish.GROUPS['payment-options']['privacy'] == 'unlisted'
    assert publish.GROUPS['partner-api']['privacy'] == 'unlisted'
    assert publish.groups_of(41) == ['partner-api'] and publish.groups_of(45) == ['partner-api']


def test_partner_episode_upload_body_is_unlisted(monkeypatch):
    bodies = []

    class _Req:
        def next_chunk(self):
            return None, {'id': 'NEWID'}

    class _Videos:
        def insert(self, part, body, media_body):
            bodies.append(body)
            return _Req()

    class _YT:
        def videos(self):
            return _Videos()

    import types
    fake_http = types.ModuleType('googleapiclient.http')
    fake_http.MediaFileUpload = lambda *a, **k: None
    monkeypatch.setitem(sys.modules, 'googleapiclient.http', fake_http)
    monkeypatch.setattr(publish, 'playable', lambda f: True)
    entry = {'file': 'x.mp4', 'lang': 'en', 'title': 't', 'description': 'd', 'audience': 'partner'}
    publish.upload_video(_YT(), entry, 'k')
    assert bodies[0]['status']['privacyStatus'] == 'unlisted'
