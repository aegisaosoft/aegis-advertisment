# LinkedIn — Frank & Mike (33-second ad)

Post for the **Aegis AO Soft LLC** page (Start a post → Posting as). Written 2026-09-19.

Video: `myeztoll-frank-mike-en.mp4` (1280×720, 33.8 s, 8.7 MB — small enough for a browser
upload, no 720p re-encode needed). Captions `myeztoll-frank-mike-en.vtt` — LinkedIn will not
take them; it transcribes itself, check the rows for "My easy toll" / "Easy Pass" after posting.

**It must not repeat the 2026-09-05 post** (the ToonBee film, "a toll is billed to a plate").
That one explained the mechanism; this one is the side-by-side: same cars, same roads, two
outcomes. The film tells it, the post only frames it.

Link goes into the **first comment**, not the body — a bare link in the body cuts reach.

---

## Post — English

Two rental fleets. Same street, same roads, same renters.

Frank pays for every toll his cars run through and every camera notice that turns up after the car is back — usually past due, with a late fee on top.

Mike's charges go to MyEZToll. Each one is matched to the booking that was open at that minute and billed to the card the renter left on file, plus our fee. Mike gets the toll back in full, and a share of that fee.

What Mike pays for it: nothing. No subscription, no set-up fee, nothing per car.

33 seconds, side by side.

MyEZToll is operated under licence by Aegis AG Soft LLC.

#CarRental #FleetManagement #Tolls #TuroHost #RevenueRecovery

**First comment:** See how it works: https://myeztoll.com

---

## Where each claim is checked

| claim | checked against |
|---|---|
| matched to the booking open at that minute | toll → booking attach by `[from, to)` window (`violations_follow_the_booking_window` memory) |
| billed to the card on file, plus a fee | `commercial_model_free_for_owner_revshare` memory |
| toll back in full + share of fee | same; partner share — `partner_share_earning_term` memory |
| nothing for the owner | same; only optional own telematics is paid, not mentioned here |

## Published

2026-09-19 — published from the Aegis AO Soft LLC page with `myeztoll-frank-mike-en.mp4` (video attached by the owner by hand). LinkedIn added auto-captions — check them for "My easy toll". First comment with the link — not added yet.
