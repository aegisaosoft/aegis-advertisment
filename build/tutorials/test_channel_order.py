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


def test_plan_replaces_the_automatic_shelf_in_place_or_inserts_first():
    auto = {'id': 'S9', 'snippet': {'type': 'allPlaylists', 'position': 1}}
    assert co.plan([auto], ['A']) == ('replace', 'S9', 1)
    assert co.plan([], ['A']) == ('insert', None, 0)
