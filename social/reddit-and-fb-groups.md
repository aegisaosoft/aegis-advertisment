# Ad copy: Reddit Ads and Facebook groups

Written 2026-09-21. Tone: the same as `linkedin-post-turo.md`, stating what the product does
without hype. Reddit readers and FB-group members punish marketing language faster than any
other audience: no "revolutionary", no exclamation marks, no emoji walls.

Every claim is checked in the table at the end. **Do not add** a share of violations
(there is none; only the fee is shared), a store listing for the phone app, or
Samsara/INVERS.

UTM for every link: `?utm_source=<reddit|facebook>&utm_medium=<paid|group>&utm_campaign=<turo|fleet|canada>`

---

## 1. Reddit Ads

**Format:** Promoted post, CTA button **Learn More**. Images: `social/reddit-card-<turo|fleet>-<wide|square>.png`
(1200x628 for desktop, 1080x1080 for the phone feed; upload the square one if only one is allowed).
Spanish copies end in `-es.png` (for Spanish-language targeting and the ES posts in the FB groups).
Source `build/social/reddit-card.html`, rendered by `node build/social/render-reddit-cards.js`.
The toll rows on the card are an illustration, not a screenshot: never caption it as "real screens".
Keep comments **ON** and answer them within a day; a promoted post with comments turned
off reads as spam. Use the answers from section 3.

### Launch plan (decided 2026-09-21)

First test = **ad group A only, $10/day, 7 days (~$70)**. Campaign `MyEZToll – Tolls – Test`,
objective **Traffic**, bidding automatic CPC, placement **Feed only**, comments ON, CTA Learn More,
location US. B (fleets) and C (Canada) are added after a week, once the real CPC and CTR are known.
The campaign is set up in ads.reddit.com by the owner (the browser tools cannot open that site).

**Published 2026-09-21** (as built, differs from the plan above): objective **Traffic**, goal Clicks, CBO on,
**$10/day** at campaign level, spend cap $100, 21–28 Sep 2026, US + Canada, one ad group `A · Turo hosts`
(r/turo, r/Turohosts, r/sidehustle + 32 keywords incl. tickets), one ad `A1 · reimbursement · image`
("Stop paying your Turo guests' tolls", `reddit-card-turo-square.png`, comments on). Conversions objective
was impossible on day one: Sign Up is greyed out until the pixel has event history.
**Known issue:** CTA was set to Learn More in the form but Review showed "REMIND ME" whatever was chosen;
check the live ad and fix if needed. Ad 2 (video, Frank & Mike) is added from Ads Manager after launch:
the creation wizard allows only one ad.

### A. Turo hosts
Targeting: communities r/turo, r/TuroHosts, r/sidehustle (r/carsharing not found by Reddit); US + Canada; automated targeting OFF.

**Keywords (Bulk entry, one per line):**
```
turo
turo host
tolls
toll charges
rental car tolls
toll bill
toll invoice
toll by plate
toll violation
unpaid tolls
E-ZPass
SunPass
FasTrak
TxTag
TollTag
Peach Pass
I-PASS
Good To Go
PikePass
407 ETR
Highway 407
A25
A30
Autoroute 30
parking ticket
red light camera
speed camera ticket
traffic citation
camera ticket
turo ticket
turo parking ticket
turo citation
```
Reddit's "Keywords related to your selection" (auto insurance, nba, parking fees, vehicle registration...)
are suggestions only: do not add them. There are no insurance products here.
Link: `https://myeztoll.com/tutorials?utm_source=reddit&utm_medium=paid&utm_campaign=turo`

**Short headlines (≤ 50 chars, Reddit's recommendation: ~38% lower cost per action):**
> Stop paying your Turo guests' tolls.
> Turo tolls, billed to the guest. Free for hosts.
> Tolls & tickets from Turo trips? Bill the guest.
> E-ZPass to FasTrak: Turo tolls, billed to guests.

Ad 1 = image `reddit-card-turo-square.png` + "Stop paying your Turo guests' tolls."; Ad 2 = video
`myeztoll-frank-mike-en.mp4` (34 s, 720p) + "Tolls & tickets from Turo trips? Bill the guest."

**Long headlines (≤ 120 chars):**
> Turo host? Stop copying toll charges from the E-ZPass site into reimbursement requests.

**Alt headlines for A/B:**
> Your guests drive through tolls, and the bill lands on your plate. Here's the part you can automate.
> Free for hosts: every toll matched to the trip it belongs to and billed to the guest.
> E-ZPass, SunPass, FasTrak, 407 ETR, US and Canada, coast to coast: every toll matched to the Turo trip and billed to the guest. Free for hosts.
> Tolls and tickets from your guest's trip land on your plate. MyEZToll matches both to the Turo trip, so you pay on time and bill the guest. Free for hosts.

**Body:**
> Every toll your guest runs through is billed to your plate, weeks later, after the trip is closed. Most hosts end up matching dates by hand or just eating it.
>
> MyEZToll reads the charges straight from the toll agencies, matches each one to the Turo trip that was open at that minute, and gets it billed to the guest. Your Turo emails are forwarded into the portal, so trips show up on their own.
>
> For the host it costs nothing: no subscription, no setup fee, nothing per car. You get the toll back in full; the fee is charged to the renter.
>
> Not only Turo: the same portal works with HQ Rental Software, Fleetwire and your own booking site.
>
> Short walk-throughs (EN/ES) show every step on the real portal.

### B. Small rental fleets / independent car rental
Targeting: r/smallbusiness, r/Entrepreneur, r/fleetmanagement, r/CarRental; interests Autos, Business.
Link: `https://myeztoll.com/?utm_source=reddit&utm_medium=paid&utm_campaign=fleet`

**Headline:**
> Rental fleets pay for tolls they never drove through. It doesn't have to be your money.

**Alt:**
> A toll is billed to the plate, and the plate is yours. We bill it to the renter instead, free for the owner.
> Using HQ Rental Software? Every toll is matched to the reservation and charged to the renter's card, free for the fleet owner.
> E-ZPass, SunPass, FasTrak, 407 ETR, US and Canada, coast to coast: works with HQ Rental Software, Fleetwire, Turo or your own booking site.
> Tolls and camera tickets hit your plate. MyEZToll matches both to the reservation and bills the renter. Works with HQ Rental Software, Fleetwire, Turo or your own booking site.

**Keywords:** HQ Rental Software, car rental software, rental fleet, car rental business, fleet tolls, rental car tolls, Fleetwire, toll by plate, toll violation, parking ticket, red light camera, camera ticket, plus the agency names from group A.

**Body:**
> The agency knows which car went through the gantry, not who was driving. By the time the invoice arrives the rental is closed and the deposit is back.
>
> MyEZToll pulls charges from 31 toll agency systems covering practically the whole US, matches every crossing to the booking that was open at that minute, and charges the card the renter left on file.
>
> Bookings come in on their own: full integration with HQ Rental Software and Fleetwire, Turo, or your own booking site built into MyEZToll, where the renter's card is on file from the moment they book. Violation notices show up in the same place, so you pay on time and skip the late penalties, and the renter is billed for them.
>
> Free for the fleet owner: no subscription, no setup fee, nothing per vehicle. You get the toll back in full plus a share of the fee we charge the renter. The only paid part is our own GPS hardware, and it's optional. Your existing GPS connects for free.

### C. Canada (407 ETR / A30)
Targeting: r/turo, r/smallbusiness, geo Ontario + Quebec.
Link: `https://myeztoll.com/?utm_source=reddit&utm_medium=paid&utm_campaign=canada`

**Headline:**
> Renting cars in Ontario or Quebec? 407 ETR and A30 bills can go to the renter, not you.

**Body:**
> 407 ETR and A30 bill the plate, and the plate is yours. MyEZToll picks up those charges, matches each one to the rental that was open at the time and bills the renter. Free for the owner, nothing per car.

---

## 2. Facebook groups

Order: **first a DM to the admin, and post only after a "yes"**. Without permission the post
gets removed and the page may be banned from the group. Post from the **My EZToll** page (if the
group allows pages) or from a personal profile with the disclaimer "I work on this product".
Put the link **in the first comment**; in many groups a link in the post body sends it to moderation.

### 2.1 DM to the admin, EN
> Hi [Name], I work on MyEZToll, a tool that matches toll charges to rental trips (Turo, HQ Rental Software, Fleetwire or your own booking site) and bills them to the guest. It's free for hosts (the fee is paid by the renter). Would you be OK with one post in [Group] explaining how it works? Happy to follow any rules you have, and to answer questions in the comments rather than DMing members.

### 2.2 DM to the admin, ES
> Hola [Nombre], trabajo en MyEZToll, una herramienta que asigna cada peaje al viaje de alquiler correspondiente (Turo, HQ Rental Software, Fleetwire o tu propio sitio de reservas) y se lo cobra al huésped. Para el anfitrión es gratis (la comisión la paga el conductor). ¿Te parece bien que publique un post en [Grupo] explicando cómo funciona? Respeto las reglas del grupo y respondo las preguntas en los comentarios, no por mensaje privado.

### 2.3 Post, EN (Turo-host groups)
> Hosts, how are you handling tolls?
>
> The toll lands on your plate weeks after the trip. Then it's matching dates, screenshots, a reimbursement request, and half the time the guest never pays.
>
> Disclosure: I work on MyEZToll, which does that matching for you. It reads charges from the toll agencies, matches each one to the Turo trip that was open at that minute, and gets it billed to the guest. You forward your Turo emails into the portal and trips appear on their own. (If you also rent outside Turo, it works with HQ Rental Software, Fleetwire and your own booking site too.)
>
> For the host it costs nothing: no subscription, no setup fee, nothing per car. You get the toll back in full; the renter pays the fee.
>
> There are short step-by-step videos (English and Spanish) in the first comment. Happy to answer questions here.

**First comment:**
> Walk-throughs: https://myeztoll.com/tutorials?utm_source=facebook&utm_medium=group&utm_campaign=turo

### 2.4 Post, EN (rental-business / fleet groups)
> A toll is billed to a plate, and the plate belongs to you. That's why rental fleets absorb charges they never incurred.
>
> Disclosure: I work on MyEZToll. We pull charges from 31 toll agency systems (practically the whole US), match each crossing to the booking that was open at that minute, and charge the renter's card on file. Bookings sync from HQ Rental Software, Fleetwire or Turo, or come in through your own booking site. Violation notices show up too, so they get paid on time instead of doubling.
>
> Free for the fleet owner, nothing per vehicle. You get the toll back in full plus a share of the fee charged to the renter. The only paid thing is our own GPS hardware, which is optional.
>
> Link in the first comment. Questions welcome.

**First comment:**
> https://myeztoll.com/?utm_source=facebook&utm_medium=group&utm_campaign=fleet

### 2.5 Post, ES (Spanish-speaking host groups)
> Anfitriones, ¿cómo manejan los peajes?
>
> El peaje llega a nombre de tu placa semanas después del viaje. Luego toca cruzar fechas, sacar capturas, pedir el reembolso… y muchas veces el huésped nunca paga.
>
> Aclaro: trabajo en MyEZToll, que hace ese trabajo por ti. Toma los cargos directamente de las agencias de peaje, asigna cada uno al viaje de Turo que estaba activo en ese momento y se lo cobra al huésped. Reenvías tus correos de Turo al portal y los viajes aparecen solos. (Si también alquilas fuera de Turo, funciona con HQ Rental Software, Fleetwire y tu propio sitio de reservas.)
>
> Para el anfitrión no cuesta nada: sin suscripción, sin cuota de alta, nada por auto. Recuperas el peaje completo; la comisión la paga el conductor.
>
> En el primer comentario dejo videos cortos paso a paso (en español e inglés). Respondo preguntas aquí.

**First comment:**
> Tutoriales: https://myeztoll.com/tutorials?utm_source=facebook&utm_medium=group&utm_campaign=turo

---

## 3. Answers to typical comments (Reddit and FB)

**"What's the catch? Nothing is free."**
> The renter pays a service fee on top of the toll. You get the toll back in full and a share of that fee. The only thing we sell to owners is our own GPS hardware, and you don't need it: an existing GPS connects for free.

**"Turo guests don't leave a card with me."**
> If the guest has no card with us, Turo bills them through its own reimbursement invoice. We pick up Turo's email when the guest has paid and mark those tolls as settled, so nothing is charged twice.

**"Which states / agencies?"**
> 31 toll agency systems, which covers practically the whole US: every E-ZPass state, SunPass, FasTrak, TxTag, NTTA TollTag, Harris County, Peach Pass, I-PASS, Good To Go and the rest. In Canada, 407 ETR, A25 and A30.

**"I don't use Turo. What booking systems does it work with?"**
> Full integration with HQ Rental Software: bookings, vehicles and customers sync on their own, and tolls are charged to the card on the HQ reservation. Fleetwire bookings sync the same way; the toll is charged to the renter's card with us. No booking system at all? MyEZToll includes your own booking site on your subdomain or your own domain, so the renter's card is on file from the start. Turo works through email forwarding and the phone app.

**"Do I need to install anything?"**
> No. It's a web portal. For Turo there is an optional phone app that brings trips in, and email forwarding works without it.

**"Is it a scam / who are you?"**
> MyEZToll is run by Aegis AG Soft LLC. The walk-through videos are recorded on the real portal, so you can see every screen before signing up.

---

## Where each claim is checked

| claim | checked against |
|---|---|
| free for the owner, fee on the renter, toll back in full, share of the fee | `commercial_model_free_for_owner_revshare` memory |
| tickets (parking, cameras) shown matched to the trip, paid on time, fine + fee billed to the driver | `commercial_model_free_for_owner_revshare` memory (violations section) |
| **no** share of violations, only paying on time / no late penalties | same memory, "Доли от самих штрафов НЕТ" |
| telematics = only paid module, optional; third-party GPS free | same memory |
| 31 agency systems, practically the whole US | `facebook-post-film.md` / `linkedin-posts.md` (count of toll providers in prod) |
| Turo emails forwarded, trips appear, phone app | `linkedin-post-turo.md`, EP22–EP26 |
| no-card guest → Turo reimbursement, marked settled | `turo_toll_reimbursement_settlement` memory |
| HQ Rental Software: bookings/vehicles/customers sync, toll charged to the card on the HQ reservation | `hq_hourly_booking_sync`, `hq_webhooks_implemented`, `hq_toll_flow_payment_declined_bug` memories |
| Fleetwire: bookings sync; toll charged through our own Stripe (Fleetwire has no charge API) | `fleetwire_booking_plugin` memory |
| own booking site on a subdomain or own domain | `aegis_myezwheels_multitenant` memory (storefront, `OwnerSites`) |
| 407 ETR, A30 | `a30_and_407_canadian_plugins_2026_09` memory (deployed) |
| tutorials EN + ES | `myeztoll.com/tutorials` |
| operator Aegis AG Soft LLC | `aegis_entity_structure_ag_licenses_ao` memory |
