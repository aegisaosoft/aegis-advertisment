# -*- coding: utf-8 -*-
"""Lay the channel's playlists out in learning order on the channel home page.

    python channel_order.py            # apply
    python channel_order.py --dry-run  # only say what would change

YouTube lets a channel order playlists in exactly one place: a home-page shelf of type
`multiplePlaylists` (channelSections). The Playlists TAB is always sorted by YouTube itself
(date), so it cannot be ordered — the shelf is what a visitor sees first.

Learning order (user 2026-09-30: "Get Started first, then by difficulty"), each English then Spanish:
Get Started -> the full owner series -> Payment Options (partners) -> Partner API -> the films.

The shelf is found by its title (SHELF_TITLE). If the channel still has an `allPlaylists`
shelf — the automatic one, which cannot be ordered — it is replaced in place by the ordered one
at the same position, so the page does not end up with two playlist shelves.
"""
import sys

import publish

SHELF_TITLE = 'Tutorials — start here'

FILMS = 'PLR2MwaFOApc0'      # MyEZToll — the films (English & Español): marketing, so last


def learning_order():
    """Playlist ids in the order a newcomer should meet them."""
    groups = publish.group_ids()
    order = []
    for lang in ('en', 'es'):
        order.append(groups['get-started'][lang])
    for lang in ('en', 'es'):
        order.append(publish.PLAYLIST[lang])
    for group in ('payment-options', 'partner-api'):
        for lang in ('en', 'es'):
            order.append(groups[group][lang])
    order.append(FILMS)
    return order


def plan(sections, order):
    """What to do with the channel's sections: ('update', id, pos) | ('replace', id, pos) | ('insert', None, 0) | None."""
    for s in sections:
        sn = s.get('snippet', {})
        if sn.get('type') == 'multiplePlaylists' and sn.get('title') == SHELF_TITLE:
            current = s.get('contentDetails', {}).get('playlists', [])
            return None if current == order else ('update', s['id'], sn.get('position', 0))
    for s in sections:
        sn = s.get('snippet', {})
        if sn.get('type') == 'allPlaylists':
            return ('replace', s['id'], sn.get('position', 0))
    return ('insert', None, 0)


def body(order, position, section_id=None):
    b = {'snippet': {'type': 'multiplePlaylists', 'title': SHELF_TITLE, 'position': position},
         'contentDetails': {'playlists': order}}
    if section_id:
        b['id'] = section_id
    return b


def main(dry):
    yt = publish.service()
    order = learning_order()
    sections = publish.call(yt.channelSections().list(part='snippet,contentDetails', mine=True)).get('items', [])
    step = plan(sections, order)
    if step is None:
        print('already in learning order: %s' % ', '.join(order))
        return
    action, section_id, pos = step
    print('%s shelf "%s" at position %d: %s' % (action, SHELF_TITLE, pos, ', '.join(order)))
    if dry:
        return
    if action == 'update':
        publish.call(yt.channelSections().update(part='snippet,contentDetails', body=body(order, pos, section_id)))
    elif action == 'replace':
        publish.call(yt.channelSections().delete(id=section_id))
        publish.call(yt.channelSections().insert(part='snippet,contentDetails', body=body(order, pos)))
    else:
        publish.call(yt.channelSections().insert(part='snippet,contentDetails', body=body(order, pos)))
    print('done')


if __name__ == '__main__':
    try:
        main('--dry-run' in sys.argv)
    except publish.QuotaOut as e:
        print('Daily quota reached — run again after it resets (midnight Pacific). %s' % str(e)[:160])
        sys.exit(2)
