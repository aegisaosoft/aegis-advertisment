# LinkedIn — the Turo part of the tutorial series

Post announcing episodes 22–26 (Turo) of the owner-portal series. Written 2026-09-18, same
voice as `linkedin-post-tutorials.md`: say what the viewer will see, do not sell over it.

**It must not repeat the 2026-09-07 post.** That one announced the finished series of 21.
The new fact is narrower: Turo hosts now have a walk-through of their own, and it is written
for people who do not think of themselves as technical.

**Publish only when all three are true** — otherwise the post points at something missing:
1. episode 26 is up in both languages (`python publish.py --refresh yc-2026-09`, then
   `published.json` shows a playlist for `26-…-en` and `26-…-es`);
2. `python site_tutorials.py` re-run after that, so the site lists all 26;
3. aa-web deployed (by the owner of the repo), so `myeztoll.com/tutorials` shows the Turo part.

One link, no image, so LinkedIn builds the preview card off episode 22 on YouTube.
**Published version (2026-09-18) is the "fifth tomorrow" one** — the site did not have the Turo part yet, so the link goes to EP22 EN rather than `myeztoll.com/tutorials`.
Published from the **Aegis AO Soft LLC** page (Start a post → Posting as).

---

## Post — English

If you host on Turo, the tolls your guests run up are yours to chase — and most of that work is copying numbers from one screen to another. We recorded five short episodes on how MyEZToll takes it off your hands — the first four are out now, the fifth tomorrow.

They go in the order you would set it up:
1. Your own mailbox inside the portal, made in a minute.
2. Forwarding your Turo emails to it from Gmail — every click shown, including the confirmation step Gmail asks for.
3. The phone app that brings in your Turo trips, and where it shows up once it is running.
4. Telling the portal which Turo listing is which of your cars.
5. Pending bookings: confirming them, and what to do when the car is already booked for those days.

No step assumes you know what a "forwarding filter" is. Each episode is a few minutes, in English and in Spanish, recorded on the real portal with every guest name and listing number blurred.

And the part that matters before you try it: for the fleet owner it costs nothing — no subscription, no set-up fee, nothing per car. You get the toll back in full; the fee is charged to the renter.

Start with part one: https://www.youtube.com/watch?v=AK_Rv9OF2Ow

#Turo #TuroHost #CarSharing #CarRental #FleetManagement #Tolls

---

## Where each claim is checked

| claim | checked against |
|---|---|
| five episodes, in that order | `build/tutorials/series_i.py` — EP22 mailbox, EP23 Gmail, EP24 phone agent, EP25 listings→cars, EP26 pending / car taken |
| Gmail confirmation step shown | EP23 frames of the "Confirm forwarding" page and the verification email |
| a few minutes each, EN + ES | rendered mp4 in `build/tutorials/mp4/`, Terry narration for ES |
| guest names and listing ids blurred | `docs/tools/redaction-rules.js` (`looksPlatformId`, `looksRangeWithName`, Turo URLs) + `data-pii` on the renter name in `ConfirmPendingBookingModal` |
| free for the owner, fee on the renter | `commercial_model_free_for_owner_revshare` memory |
| 26 episodes on the page | `client/src/data/tutorials.ts` after `site_tutorials.py` — **25 today**, 26 after the ES upload |

## Notes

- The phone app in EP24 is the APK from `owner.myeztoll.com/download`, not the Play build —
  the post says "the phone app" and does not promise a store listing.
- No `@myeztoll` in the text (turns into a mention); one link only, so the card is EP22.

## Published 2026-09-18

- **With the image** `social/linkedin-turo-card.png` (1200x900, from
  `build/youtube/post-card-turo.html`; tile 3 is cropped above the "Driver (name)" line of
  `58-confirm-pending`): https://www.linkedin.com/feed/update/urn:li:activity:7506804572741378048/
  The image was attached by hand — this time the feed's Photo button *did* expose a file input
  (`file_upload` worked), but switching the author to the Page afterwards drops the attachment,
  and the composer's own Add media opens an input inside a shadow root the tools cannot reach.
- **Link-card version** (published first, same text):
  https://www.linkedin.com/feed/update/urn:li:activity:7506802946714603520/ — duplicate, deleted by the
  user the same day.
