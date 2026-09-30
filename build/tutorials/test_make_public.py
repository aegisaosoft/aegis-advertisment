# -*- coding: utf-8 -*-
import make_public


def test_wanted_videos_follow_each_episode_privacy():
    state = {
        'myeztoll-tutorial-01-tour-en': {'videoId': 'A'},
        'myeztoll-tutorial-36-pay-driver-pays-en': {'videoId': 'B'},
        'myeztoll-tutorial-41-api-first-call-es': {'videoId': 'C'},
        'myeztoll-tutorial-99-nothing-en': {'videoId': 'D'},        # no such episode: left alone
        'myeztoll-tutorial-02-rules-en': {},                         # never uploaded: left alone
    }
    assert make_public.wanted_videos(state) == {'A': 'public', 'B': 'public', 'C': 'public'}


def test_both_partner_playlists_are_wanted_public():
    wanted = make_public.wanted_playlists()
    groups = {(g, lang): p for g, lang, p in wanted.values()}
    for lang in ('en', 'es'):
        assert groups[('payment-options', lang)] == 'public'
        assert groups[('partner-api', lang)] == 'public'
