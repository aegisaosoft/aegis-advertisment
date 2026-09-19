# Ad copy — the tutorial series on Facebook

Post announcing that the whole owner-portal series is up on `facebook.com/myeztoll`.
Written 2026-09-07, same voice as `linkedin-posts.md` and `linkedin-post-youtube.md`:
the post says what a viewer will actually see and does not sell over the top of it.

**It must not repeat the YouTube post** (published the same day). That one announced the
channel — the film plus a series that had just started. This one has a different fact to
report: the series is finished, all forty-two recordings are out, and Facebook is now the
second place they live. The angle is the series itself, not the channel.

Two links in the text, no image, so LinkedIn will build a preview card off the first URL.
If a card is not wanted, attach `social/linkedin-youtube-card.png` by hand — with an image
attached LinkedIn shows no preview (see `linkedin-post-youtube.md`; the composer sits in a
closed shadow root, so picking the file from disk is the only route).

---

## Post — English

We finished the tutorials, so there is now no part of MyEZToll you have to take on trust.

Twenty-one episodes on the owner portal, English and Spanish, forty-two recordings in all — about an hour and a half of screen time. They are on the MyEZToll page on Facebook, and on the YouTube channel in two playlists, one per language.

They run in the order you would actually meet the product: connecting your toll agencies, getting the fleet in, transponders, rates, the booking screen, where the tolls land and who ends up paying for them, violations, failed payments, payouts, GPS and its alerts, bookings arriving from a rental platform, your storefront, reports. Two minutes an episode, one job each.

Nothing in them is a mock-up. Every frame is a real screen from the portal an owner logs into, with the customers' data blurred out — the same captures that illustrate the written guides, so the video and the manual cannot drift apart. The Spanish set is not the English one with subtitles: it is the Spanish portal, recorded again with a Spanish narrator.

And the reason to watch before you talk to anyone: for the fleet owner it costs nothing — no subscription, no set-up fee, nothing per vehicle. You are paid the toll in full, plus a share of the fee we charge the renter. The one thing we sell is our own telematics hardware, and it is optional.

https://www.facebook.com/myeztoll
https://www.youtube.com/@myeztoll

#FleetManagement #CarRental #Tolls #Telematics #RevenueRecovery

---

## Where each claim is checked

| claim | checked against |
|---|---|
| 21 episodes, EN + ES, 42 recordings | `build/tutorials/mp4/` — 42 rendered `.mp4`, each with `.srt` and `.vtt` |
| about an hour and a half | 45 min EN + 53 min ES = 98 min, measured off the last caption cue of every `.srt` |
| two minutes an episode | 1:38–2:37 EN, 1:55–3:08 ES; two minutes is the honest round number, "two or three" also true |
| the topics, in that order | episode titles 3–20 in `series_a..h.py`, read in series order |
| real screens, data blurred | frames come from `docs/images-2x/<lang>/`, the same captures as the written guides; blurring is done at capture (`myeztoll-tutorial-video-series` memory) |
| Spanish is a separate recording | Spanish screenshots (`docs/images-2x/es/`) plus the Terry narration — not a subtitle track over the English cut |
| free for the owner, share of the fee, paid telematics is the exception | the commercial model, as in `linkedin-posts.md` |

## Notes

- **Do not name a video count for the Facebook page in the post** beyond "forty-two
  recordings" — Facebook turns every upload into a reel, so what the page shows is a reel
  grid, not a playlist, and it has no per-language grouping. The playlists are YouTube's.
- Published from the **Aegis AO Soft LLC** page (Start a post → arrow by the author →
  Posting as), same as the film and channel posts.
- LinkedIn English-only, as with the earlier posts; the Spanish audience is served by the
  ES episodes themselves.
- **Published 2026-09-07** from the Aegis AO Soft LLC page, no image, LinkedIn built its
  preview card off the second URL (the YouTube channel) and shortened both links to
  `lnkd.in`:
  https://www.linkedin.com/feed/update/urn:li:activity:7502792599662088192/
  The admin list and the public Posts tab both lagged by some minutes after publishing and
  kept showing the previous post — that is the listing, not the post.
- **The Facebook claim was ahead of the facts when this went out.** At publication the page
  `facebook.com/myeztoll` held only the film, and the channel was five episodes short. Both
  were finished afterwards — 2026-09-13 — so the post now reads true as written.

## Upload state on YouTube

**Complete as of 2026-09-13** — `build/tutorials/mp4/published.json` lists all 42
recordings with a video id, a caption track and a playlist entry. The 7 September run had
stopped five short on YouTube's daily upload limit (`uploadLimitExceeded`, not an API
quota) and left EN 19 outside its playlist; a later run finished both.

## Upload state on the Facebook page

Uploaded from `social/fb-tutorials/` (every file re-encoded under the 10 MB the browser
upload accepts), one reel per episode, caption = episode title + subtitle + the channel
link, **AI label on** (the narration is synthesised).

**Complete as of 2026-09-13** — all 42 episodes are reels on the page.

| date | episodes |
|---|---|
| 2026-09-07 | EN 1–21, ES 1, 2, 4, 5, 6, 7, 8 — 28 reels |
| 2026-09-13 | ES 3, 9, 10, 11, 12, 13, 14, 15, 16 (the drafts), then ES 17–21 — 14 reels |

Facebook's anti-spam limit had stopped the first run after 28 posts ("We limit how often you
can post…"). **Post stops working silently** — the dialogs stack one on top of another and
nothing reaches the page — so the nine in flight were saved as drafts and published five
days later. A draft is finished through Content Library → Drafts → ⋯ → **Edit post** →
Next → **Publish** (the ⋯ menu itself has no publish entry), and it keeps the caption and
the AI label it was saved with.

Two things that cost time on the second run and are worth knowing: typing into the composer
before the upload finishes drops most of the text (clear the field with ctrl+A, Delete and
retype), and the "Edit reel" step renders slowly — clicking its Next too early lands behind
the dialog and closes it, leaving the draft in the page composer.

## Episode 18 replaced — 2026-09-18

The Platform cars lines in ep18 were wrong (the pencil only opens the car page; the tab
lists your own fleet cars from the platform, not the platform's listings). Two lines were
rewritten and re-voiced, and both languages re-published:

| where | old | new |
|---|---|---|
| YouTube EN | `zZltB7x0Tmo` (private) | `Wb0F_aO5I1k` |
| YouTube ES | `JXAteFkWGfw` (private) | `RK_3lN3NQ2Q` |
| Facebook EN reel | still up, delete by hand | `facebook.com/reel/1375435848004570` |
| Facebook ES reel | `facebook.com/reel/931236443384593`, delete by hand | `facebook.com/reel/2062187657835186` |

The ES playlist was switched to "Manually sorted" in Studio so `publish.py --replace` can
put a replacement in the old slot. Facebook's link allowance for the page is nearly spent
until 1 October ("You can still add links to 1 post this month") — a reel caption with the
channel URL counts. A composer upload that sits at 0% never recovers: reload the page and
start again; a stuck file stays in the composer as a draft and gets re-attached.

## Episode 2 (ES) replaced — 2026-09-18

The Spanish `30-settings-owner` capture had been taken while the page was still loading
("Cargando configuración…" spinners where the settings belong), so the published ES ep2 showed
no settings. The capture harness now waits for spinners (`waitForSpinners`), the screen was
recaptured, ES ep2 rebuilt on it.

| where | old | new |
|---|---|---|
| YouTube ES | `Jv3A6GLrK6s` (private) | `KuPcgNjX150` |
| Facebook ES reel | old ES ep2 reel still up — delete by hand | `facebook.com/reel/1052048907825962` |

Caption has no URL (the page's link allowance for September is spent); a bare `@myeztoll`
turns into a mention of the page itself, so the channel is written without the `@`.

## Episodes 18 and 21 replaced again — 2026-09-18 (privacy)

Turo reservation numbers (ep18, History tab) and a Turo host page URL (ep21, Turo Agents)
were legible. The capture rules now blur Turo host/listing URLs, bare platform ids and a
date range followed by a renter's name; screens recaptured, both episodes rebuilt.

| where | old (private / to delete) | new |
|---|---|---|
| YouTube 18 EN | `Wb0F_aO5I1k`, `zZltB7x0Tmo` | `Z6TG1p0KP1E` |
| YouTube 18 ES | `RK_3lN3NQ2Q`, `JXAteFkWGfw` | `-0yJujvb-q0` |
| YouTube 21 EN | `SnTa-_7JJRg` | `PUx0Ixj53CU` |
| YouTube 21 ES | `sO5eK-kiRgQ` | `diRMMel7bhQ` |
| Facebook | 18 EN `1375435848004570`, 18 ES `2062187657835186`, 18 ES `931236443384593`, the original 18 EN and 21 EN/ES reels of 2026-09-07/13 | new reels `1886931868938605`, `3467910653378811`, `966696869801678` + 21 ES (processing when noted) |
