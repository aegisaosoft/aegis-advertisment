# Ad copy — the film on Facebook

The English film on the page `facebook.com/myeztoll`. Same argument as the LinkedIn post
in `linkedin-posts.md`, cut shorter: Facebook hides everything past the third line behind
"See more", so the mechanism has to land in the first two.

Video: `social/linkedin-en-720p.mp4` (7.5 MB, the size a browser will take from a script)
or the 1080p master `myeztoll-toonbee-en.mp4` (69 MB) when the file is picked by hand.
Facebook transcribes the audio itself; the correct wording, if the auto-captions need
fixing, is `social/linkedin-en.srt`.

---

## Post — English

A toll is billed to a plate, and the plate belongs to you.

That is why rental fleets absorb charges they never incurred. The agency knows which vehicle went through the gantry; it has no idea who was driving. By the time the invoice clears, the rental is closed, the deposit is back with the renter, and the only name left on the paperwork is yours.

MyEZToll closes that gap. We read from the toll networks themselves — thirty-one agency systems covering practically all of the United States — match every crossing against the booking that was open at that minute, and charge the card the renter already left on file. Camera violations go the same way.

It costs the fleet owner nothing: no subscription, no set-up fee, nothing per vehicle. You are paid the toll in full, plus a share of the fee we charge the renter, so a recovered charge is revenue and not a wash. The one thing we sell is our own telematics hardware, and it is optional.

A minute and a half, and you can see the whole loop.

myeztoll.com

---

## Where each claim is checked

Same table as `linkedin-posts.md`: thirty-one agency networks is the count of toll
providers configured in production, free-for-the-owner and the owner's share of the fee
are the commercial model, and the paid optional telematics module is named out loud in
both the film and the post.

## Notes

- Posted as the Page (My EZToll), not from a personal profile — Facebook asks to
  "switch into" the page first.
- **Published 2026-09-07 as a Reel:** https://www.facebook.com/reel/1761312061795456/
  Facebook now turns every video post into a reel; the landscape frame survives.
  `myeztoll-toonbee.en_US.srt` (a copy of `linkedin-en.srt`, renamed to the
  `filename.en_US.srt` pattern Facebook demands) is attached as the English caption
  track, and the **AI label is on** — the film is generated animation.
- Facebook, unlike LinkedIn, keeps real `input[type=file]` elements in the DOM, so the
  video, the caption file, the cover photo and the profile picture were all uploaded
  from disk by the browser tools; nothing had to be attached by hand.
- Page art set the same day: cover from `social/facebook-cover.png`
  (`build/social/fb-cover.html`, 1640x624 — the bottom-left corner is left empty because
  the profile picture sits over it), profile picture from
  `aegis-aa-web/images/ez_logo_linkedin_1000.jpg` — the EZ mark **without a frame**; the
  copy in the page's own Company album has a drawn border and is the wrong one.
