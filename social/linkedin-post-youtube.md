# Ad copy — the YouTube channel

Post announcing the `@myeztoll` channel: the film plus the owner-portal tutorial series.
Written 2026-09-07, in the same voice as `linkedin-posts.md` — the post explains what a
viewer will actually see, it does not sell over the top of it.

Link in the post: `https://www.youtube.com/@myeztoll`, plus the image
`social/linkedin-youtube-card.png` (1200x900, rendered from `build/youtube/post-card.html`
the same way as the channel art). With an image attached LinkedIn shows no preview card
for the link, so the URL stays in the text as its own line.

**Attaching the image is a manual click.** The composer is now rendered inside a closed
shadow root: no `contenteditable` and no `input[type=file]` are reachable from the page,
a synthetic `paste`/`drop` with a `DataTransfer` never reaches their handler, and the
browser tools' Ctrl+V only carries clipboard *text* — the clipboard trick in
`linkedin-image-paste-via-clipboard` no longer attaches a picture. Photo -> pick the PNG
from disk is the only route.

---

## Post — English

We put the whole product on YouTube, screen by screen.

Fleet software is normally sold by demo: someone else drives, you see the parts they chose to show you, and you meet the rest after signing. We would rather you saw it first.

There are two things on the channel.

A ninety-seven-second film — *Four-Twelve* — about a toll a rental fleet pays and never billed. The crossing is charged to the plate, the plate belongs to the owner, and by the time the invoice clears the rental is closed and the deposit is back with the renter.

And the owner portal itself, one screen at a time: connecting your toll agencies, the vehicle list, transponders, bookings, tolls, charges. Two or three minutes an episode, English and Spanish, twenty-one episodes in the series, and the first of them are up now.

None of it is a mock-up. It is the portal an owner logs into, captured from the real screens with the customers' data blurred out.

For the fleet owner it costs nothing: no subscription, no set-up fee, nothing per vehicle. You are paid the toll in full, plus a share of the fee we charge the renter. The one thing we sell is our own telematics hardware, and it is optional.

https://www.youtube.com/@myeztoll

#FleetManagement #CarRental #Tolls #Telematics #RevenueRecovery

---

## Where each claim is checked

| claim | checked against |
|---|---|
| film 1:37, *Four-Twelve* | `aegis-advertisment/myeztoll-toonbee-en.mp4`, on the channel since 2026-09-06 |
| 21 episodes, EN + ES | `build/tutorials/` — `series_a..h.py`, 21 episodes x 2 languages |
| 2–3 minutes an episode | published durations 1:59–3:12 |
| screens are real, data blurred | frames come from `docs/images-2x/`, the same captures as the written guides; blurring is done at capture (`myeztoll-tutorial-video-series` memory) |
| free for the owner, share of the fee, paid telematics is the exception | the commercial model, as in `linkedin-posts.md` and `channel-copy.md` |

## Notes

- No date is promised for the remaining episodes — an earlier draft said "the rest
  follow this week" and it was cut deliberately. Keep it that way.
- Published from the **Aegis AO Soft LLC** page, same as the film post.
- A Spanish version was not written; the earlier campaign kept LinkedIn English-only.
- Published 2026-09-07 from the Aegis AO Soft LLC page, image attached by hand:
  https://www.linkedin.com/feed/update/urn:li:activity:7502716255720837120/
