# -*- coding: utf-8 -*-
"""Lay the channel's playlists out in learning order on the channel home page.

    python channel_order.py            # apply
    python channel_order.py --dry-run  # only say what would change
    python channel_order.py --arrange [--dry-run]   # home page: films, tutorials, For you, Videos, Playlists

YouTube lets a channel order playlists in exactly one place: a home-page shelf of type
`multiplePlaylists` (channelSections). The Playlists TAB is always sorted by YouTube itself
(date), so it cannot be ordered — the shelf is what a visitor sees first.

Learning order (user 2026-09-30: "Get Started first, then by difficulty"), each English then Spanish:
Get Started -> the full owner series -> Payment Options (partners) -> Partner API -> the films.

The shelf is found by its title (SHELF_TITLE); a missing one is inserted. The automatic
`allPlaylists` shelf ("Playlists") is never removed: the user wants it at the end of the page.

The home page itself (user 2026-10-02): the films first, then this shelf, then YouTube's own
"For you", then Videos (recent uploads), then Playlists. `layout_moves` computes the position
changes for the sections we may move; the ones YouTube manages ("For you", Shorts and the like)
come back from the API as type `channelsectiontypeundefined` and cannot be moved, so the films
and the tutorials are put in front of them and Playlists right behind Videos.
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


def _type(snippet):
    """Section type, case-folded: insert takes 'multiplePlaylists' but list returns 'multipleplaylists'."""
    return (snippet.get('type') or '').lower()


def plan(sections, order):
    """What to do with the channel's sections: ('update', id, pos) | ('replace', id, pos) | ('insert', None, 0) | None."""
    for s in sections:
        sn = s.get('snippet', {})
        if _type(sn) == 'multipleplaylists' and sn.get('title') == SHELF_TITLE:
            current = s.get('contentDetails', {}).get('playlists', [])
            return None if current == order else ('update', s['id'], sn.get('position', 0))
    return ('insert', None, 1)


def layout_moves(sections):
    """[(section, new_position)] that give: films, tutorials, <YouTube's own>, Videos, Playlists.

    Moves go front to back; each update shifts the sections behind it, so every move is computed
    against the list as it will be after the moves before it.
    """
    by_pos = sorted(sections, key=lambda s: s.get('snippet', {}).get('position', 0))
    films = next((s for s in by_pos if _type(s['snippet']) == 'singleplaylist'
                  and FILMS in s.get('contentDetails', {}).get('playlists', [])), None)
    shelf = next((s for s in by_pos if _type(s['snippet']) == 'multipleplaylists'
                  and s['snippet'].get('title') == SHELF_TITLE), None)
    videos = next((s for s in by_pos if _type(s['snippet']) == 'recentuploads'), None)
    playlists = next((s for s in by_pos if _type(s['snippet']) == 'allplaylists'), None)

    head = [x for x in (films, shelf) if x]
    rest = [s for s in by_pos if s not in head and s is not playlists]
    if playlists is not None and videos is not None and videos in rest:
        rest.insert(rest.index(videos) + 1, playlists)
    elif playlists is not None:
        rest.append(playlists)
    wanted = head + rest

    moves, current = [], list(by_pos)
    for target, s in enumerate(wanted):
        if current.index(s) != target:
            if s not in (films, shelf, playlists):
                continue                    # never ours to move; the moves of ours put it in place
            moves.append((s, target))
            current.remove(s)
            current.insert(target, s)
    return moves


def move_body(section, position):
    """An update body that only changes a section's position (type and content kept as they are)."""
    sn = section['snippet']
    b = {'id': section['id'], 'snippet': {'type': sn['type'], 'position': position}}
    if sn.get('title'):
        b['snippet']['title'] = sn['title']
    if section.get('contentDetails'):
        b['contentDetails'] = section['contentDetails']
    return b


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
    else:
        publish.call(yt.channelSections().insert(part='snippet,contentDetails', body=body(order, pos)))
    print('done')


def arrange(dry):
    """Put the home page in the user's order: films, tutorials, For you, Videos, Playlists."""
    yt = publish.service()
    sections = publish.call(yt.channelSections().list(part='snippet,contentDetails', mine=True)).get('items', [])
    moves = layout_moves(sections)
    if not moves:
        print('home page already in order')
        return
    for s, pos in moves:
        print('move %s "%s" -> position %d' % (s['snippet']['type'], s['snippet'].get('title', ''), pos))
        if not dry:
            publish.call(yt.channelSections().update(part='snippet,contentDetails', body=move_body(s, pos)))
    print('dry run' if dry else 'done')


if __name__ == '__main__':
    try:
        if '--arrange' in sys.argv:
            arrange('--dry-run' in sys.argv)
        else:
            main('--dry-run' in sys.argv)
    except publish.QuotaOut as e:
        print('Daily quota reached — run again after it resets (midnight Pacific). %s' % str(e)[:160])
        sys.exit(2)
