# -*- coding: utf-8 -*-
from site_tutorials import live_id


def test_finished_upload_is_the_new_video():
    assert live_id({'videoId': 'new', 'caption': True, 'playlist': True}) == 'new'


def test_mid_replacement_keeps_the_old_public_video():
    assert live_id({'replaces': 'old', 'videoId': 'new'}) == 'old'


def test_finished_replacement_uses_the_new_video_not_the_hidden_one():
    st = {'replaces': 'old', 'oldHidden': True, 'videoId': 'new', 'caption': True, 'playlist': True}
    assert live_id(st) == 'new'


def test_never_published_is_absent():
    assert live_id({}) is None
    assert live_id({'videoId': 'x'}) is None


def test_recordings_keeps_the_language_that_can_be_watched():
    from site_tutorials import recordings
    state = {'en': {'videoId': 'new', 'caption': True, 'playlist': True},
             'es': {'videoId': 'dead', 'caption': True, 'playlist': True}}
    assert recordings(state, public=lambda v: v == 'new') == {'en': 'new'}


def test_recordings_falls_back_to_the_old_public_video():
    from site_tutorials import recordings
    state = {'en': {'videoId': 'broken', 'playlist': True, 'replaces': 'old'}}
    assert recordings(state, public=lambda v: v == 'old') == {'en': 'old'}


def test_recordings_is_empty_when_nothing_is_public():
    from site_tutorials import recordings
    assert recordings({'en': {'videoId': 'x', 'playlist': True}}, public=lambda v: False) == {}
