# -*- coding: utf-8 -*-
import channel_order as co
import publish


def test_learning_order_starts_with_get_started_and_ends_with_the_films():
    order = co.learning_order()
    g = publish.group_ids()
    assert order[:2] == [g['get-started']['en'], g['get-started']['es']]
    assert order[2:4] == [publish.PLAYLIST['en'], publish.PLAYLIST['es']]
    assert order[4:8] == [g['payment-options']['en'], g['payment-options']['es'],
                          g['partner-api']['en'], g['partner-api']['es']]
    assert order[-1] == co.FILMS and len(order) == len(set(order)) == 9


def test_plan_updates_our_shelf_only_when_its_order_differs():
    order = ['A', 'B']
    ours = {'id': 'S1', 'snippet': {'type': 'multiplePlaylists', 'title': co.SHELF_TITLE, 'position': 2},
            'contentDetails': {'playlists': ['B', 'A']}}
    assert co.plan([ours], order) == ('update', 'S1', 2)
    ours['contentDetails']['playlists'] = ['A', 'B']
    assert co.plan([ours], order) is None


def test_plan_never_removes_the_playlists_shelf_and_inserts_after_the_films():
    auto = {'id': 'S9', 'snippet': {'type': 'allplaylists', 'position': 1}}
    assert co.plan([auto], ['A']) == ('insert', None, 1)
    assert co.plan([], ['A']) == ('insert', None, 1)


def _sec(sid, typ, pos, title='', playlists=None):
    s = {'id': sid, 'snippet': {'type': typ, 'position': pos, 'title': title}}
    if playlists:
        s['contentDetails'] = {'playlists': playlists}
    return s


def _apply(sections, moves):
    order = sorted(sections, key=lambda s: s['snippet']['position'])
    for s, pos in moves:
        order.remove(s)
        order.insert(pos, s)
    return [s['id'] for s in order]


def test_layout_puts_films_tutorials_foryou_videos_playlists():
    # The channel as it was on 2026-10-02 (types as the API returns them, lower-case).
    sections = [
        _sec('TUT', 'multipleplaylists', 0, co.SHELF_TITLE, ['x']),
        _sec('FILMS', 'singleplaylist', 1, '', [co.FILMS]),
        _sec('FORYOU', 'channelsectiontypeundefined', 2),
        _sec('VIDEOS', 'recentuploads', 3),
        _sec('U4', 'channelsectiontypeundefined', 4),
        _sec('EVENTS', 'completedevents', 5),
        _sec('PLAYLISTS', 'allplaylists', 6),
        _sec('U7', 'channelsectiontypeundefined', 7),
    ]
    moves = co.layout_moves(sections)
    assert _apply(sections, moves)[:5] == ['FILMS', 'TUT', 'FORYOU', 'VIDEOS', 'PLAYLISTS']
    # Only our own sections are ever moved.
    assert {s['id'] for s, _ in moves} <= {'FILMS', 'TUT', 'PLAYLISTS'}


def test_layout_is_a_no_op_when_already_in_order():
    sections = [
        _sec('FILMS', 'singleplaylist', 0, '', [co.FILMS]),
        _sec('TUT', 'multipleplaylists', 1, co.SHELF_TITLE, ['x']),
        _sec('FORYOU', 'channelsectiontypeundefined', 2),
        _sec('VIDEOS', 'recentuploads', 3),
        _sec('PLAYLISTS', 'allplaylists', 4),
    ]
    assert co.layout_moves(sections) == []
