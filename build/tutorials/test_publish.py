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
