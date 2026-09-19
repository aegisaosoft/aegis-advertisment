# The MyEZToll channel on YouTube — what goes in every field

Everything here is meant to be copied into YouTube Studio as it stands. The claims are
the ones the film and the LinkedIn copy already make, and they are checkable: thirty-one
agency networks is the count configured in production; free for the owner, the owner's
share of the fee, and the one paid optional module are the commercial model.

Artwork rendered next to this file: `banner.png` (2048x1152), `avatar-dark.png` /
`avatar-light.png` (800x800), `watermark-150.png`. Sources are `banner.html` and
`avatar.html`; re-render with chrome-headless-shell, `--window-size` at the target size.

---

## 1. Customization -> Profile

Studio no longer has Branding and Layout tabs. **Customization** has two: **Profile**,
which holds everything below — banner, picture, name, handle, description, links,
contact e-mail and the video watermark, in that order down one page — and **Home tab**,
which is the old Layout. Nothing is saved until **Publish**, top right.

| Field | File | Notes |
|---|---|---|
| Picture | `avatar-dark.png` | Masked to a circle and shown at 48px beside comments — the wordmark is unreadable at that size, so this is the EZ mark alone. `avatar-light.png` is the same on white. |
| Banner | `banner.png` | Only the middle 1235x338 is guaranteed to be seen; every word is inside it. |
| Video watermark | `watermark-150-ink.png` | Bottom of the same page. Display time: **Entire video**. Navy, not white: the film is a light-ground picture and a white mark disappears into it. `watermark-150.png` is the white version, for dark footage. |

### Same page, further down

**Name:** `MyEZToll`

**Handle:** `@myeztoll`

**Description** (946 characters against the 1000 limit):

```
A toll is billed to a plate, and the plate belongs to the fleet. That single fact is why rental fleets absorb charges they never incurred: the agency knows which vehicle went through the gantry, not who was behind the wheel, and by the time the invoice clears the rental is closed and the deposit is back with the renter.

MyEZToll closes that gap. We read from the toll networks themselves — thirty-one agency systems covering practically all of the United States — match every crossing against the booking that was open at that minute, and charge the card the renter already left on file. Camera violations go the same way.

For the fleet owner it costs nothing. No subscription, no set-up fee, nothing per vehicle, and connecting a GPS you already run is free. You are paid the toll in full, plus a share of the fee we charge the renter. The one thing we sell is our own telematics hardware, and it is optional.

myeztoll.com
Aegis AO Soft LLC
```

**Links** — "Add link", they show on the channel profile and the about page:

| Title | URL |
|---|---|
| MyEZToll | https://myeztoll.com |
| Watch the film | https://myeztoll.com/film |
| LinkedIn | https://www.linkedin.com/company/myeztoll/ |

**Contact email:** `support@myeztoll.com` — the address the site itself publishes.

## 3. Settings -> Channel -> Basic info

**Country of residence:** United States.

**Keywords** — comma-separated, quote the phrases, 500 characters is the cap:

```
"MyEZToll","toll recovery","rental fleet tolls","car rental software","toll management","toll billing","camera violations","traffic ticket recovery","fleet management","telematics","GPS tracking","E-ZPass","SunPass","rental car tolls","Turo host tools","fleet revenue recovery","car rental business"
```

## 4. Settings -> Channel -> Advanced settings

* **Audience: "No, set this channel as not made for kids."** Getting this wrong turns off comments, cards, end screens and the notification bell across the whole channel.
* Automatic captions: leave on; the uploaded `.srt` files override them where they exist.
* Google Ads account linking: only when a paid campaign actually starts.
* There is no Associated website field any more — Studio dropped it; the site link lives in Links on the Profile page instead.
* Show subscriber count: off while the number is small.

## 5. Settings -> Upload defaults

Set these once and every upload starts from them.

* Title: leave blank; Description: the two closing lines below, so no upload ships without them.
* Visibility: Private (so a half-finished upload cannot go out by accident).
* Category: **Autos & Vehicles**. Licence: Standard YouTube Licence.
* Language: English. Caption certification: none.
* Comments: Hold potentially inappropriate comments for review. Sort by: Top.
* Not made for kids.

Description tail for every video:

```
Free for fleet owners: no subscription, no set-up fee, nothing per vehicle. You are paid the toll in full plus a share of the fee we charge the renter.

myeztoll.com
```

## 6. Feature eligibility — do this before the first upload

Verify the phone number (Settings -> Channel -> Feature eligibility). Without it there
are no custom thumbnails, no videos over 15 minutes, and no external links in cards or
end screens. The verification takes a minute and gates the rest of the plan.

---

## 7. The film, in fourteen languages

The 1:37 cut is already up on the channel — check its language, subtitles and
description against this section rather than uploading it a second time.

There is one film — *Four-Twelve*, 1:37 — narrated in thirteen languages, with Uzbek
carried as subtitles over the English narration. Two ways to publish that, in order of
preference:

### Preferred: one video, many audio tracks

Upload the English cut, then Subtitles -> **Add audio track** for each of the other
twelve, and subtitles from the `.srt` files for all fourteen. YouTube serves the viewer
their own language automatically, all the watch time lands on one video, and the
translated title and description are set per language on that same video.

Uzbek is subtitles only — `myeztoll-toonbee-uz.srt` over the English audio — because the
uz cut is an English narration with burned-in captions; do not upload it as its own
audio track.

Check whether the channel has the feature: open a published video's Subtitles page and
look for the audio-track row. If it is absent, fall back to the plan below and revisit
it later — moving to multi-audio afterwards means re-uploading.

### Fallback: fourteen videos in one playlist

* Playlist: **Four-Twelve — MyEZToll in 14 languages**, ordered EN, ES, then the rest.
* Every video: its own language set as the video language, its own `.srt` as subtitles,
  and the English title kept as a translation so search finds it.
* Title pattern: `Four-Twelve — MyEZToll (Español)` and so on, the native name of the
  language in the parentheses.

### Title and description for the English cut

Title (under the 100-character limit, front-loaded so it survives truncation):

```
Four-Twelve: the toll your rental fleet pays and never billed
```

Description:

```
Tuesday, 4:12 in the afternoon. One of your cars goes through a toll, and nobody pays — not yet. Three weeks later the bill arrives with your name attached, the renter is gone, refunded, and the rental is closed. So you pay it and call it the cost of doing business.

The toll agencies knew all along. MyEZToll reads from thirty-one of their systems, covering practically all of the United States, matches every crossing against the booking that was open at that minute, and charges the card the renter already left on file. Camera violations go the same way.

It costs the fleet owner nothing: no subscription, no set-up fee, nothing per vehicle, and connecting a GPS you already run is free. You are paid the toll in full plus a share of the fee we charge the renter — a recovered charge is revenue, not a wash. The one thing we sell is our own telematics hardware, and it is optional.

myeztoll.com

Narrated in fourteen languages — pick yours from the audio track or the subtitles.

Aegis AO Soft LLC. Sold and operated under licence by Aegis AG Soft LLC.
```

Tags: `toll recovery, rental fleet, car rental, tolls, E-ZPass, SunPass, camera violations, fleet management, telematics, Turo host, car rental software, toll billing`

Thumbnail: 1280x720, and the words on it have to be readable at the size of a phone's
search result — three or four of them, not a sentence.

## 8. Customization -> Home tab

* Turn **Show Home Tab** on first — while it is off the trailer sections are not offered at all.
* **Add section -> Channel trailer:** the English film. It is what someone who has not subscribed sees at the top.
* **Add section -> Spotlight (for returning subscribers):** worth adding only once there is a second video; with one upload it just repeats the trailer.
* Sections, in order: the film's playlist, then Videos, then anything else. A channel
  with one video needs one section, not five empty ones.
