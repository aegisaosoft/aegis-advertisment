# LinkedIn — the extended Partner API

**Published 2026-10-15:** https://www.linkedin.com/feed/update/urn:li:share:7516522701360922624/ (links in the body by user choice; hashtag dropped — the 29.09 Partner API posts kept Turo out).

Post from the **Aegis AO Soft LLC** page (`linkedin.com/company/aegis-ao-soft`), aimed at builders of
rental, P2P and fleet software. Integration partners are deliberately NOT named — only with their consent.

Image: `social/linkedin-partner-api-card.png` (1200×900, built from
`build/youtube/post-card-partner-api.html`; field names in the code panel are the real `Toll` schema,
the values are invented). **A human attaches it** — the composer's file input is out of reach once the
author is switched to the Page.

---

## Post — English

🔌 Tolls, tickets and telematics for your platform, one API call away

If you build software for rental companies, car-sharing hosts or fleets, toll charges and violations are probably still handled by hand: someone logs into agency portals, downloads statements and matches them to cars and renters.

Our MyEZToll Partner API does that work for you, and we've just expanded it.

What partners get:
🛣️ Tolls from 30+ US agencies (E-ZPass, SunPass, FasTrak, TxTag, NTTA, Peach Pass and more) and from Canada (407 ETR, A25, A30). Each toll is matched to the car and the rental, and comes with the raw agency amount and our service fee as separate fields.
🎫 Violations: parking and camera tickets, assigned to the right vehicle and booking.
🚗 Cars, transponders, drivers and bookings, all managed with your own IDs across the whole API. Driver's license capture, rental agreement links and card registration links are included.
📡 GPS and telematics: live positions, trip tracks, mileage, diagnostics and alerts.
💳 Charges and disputes: you charge on your own Stripe account. When a chargeback comes in, we prepare the evidence package for you.
🔔 HMAC-signed webhooks, so you don't have to poll.

New: owner provisioning for booking platforms
Your platform can now set up its rental companies on MyEZToll with a single POST /owners call. That call:
• applies your integration template, so every new company gets the same settings
• sends a payment setup link, or attaches a card token
• sends invitations in 15 languages
• supports auto-debit, and invoices are available at GET /billing/invoices

If you build rental, P2P or fleet software and want toll and violation handling built into your product, send us a message.

📚 Docs in 15 languages: https://myeztoll.com/api-docs
🧪 Try it live in Swagger: https://owner.myeztoll.com/api/partner/v1/index/index.html

#API #CarRental #FleetManagement #Tolls #Integration #SaaS #Mobility
