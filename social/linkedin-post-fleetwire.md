# LinkedIn — Fleetwire integration

**Published 2026-11-04:** https://www.linkedin.com/feed/update/urn:li:share:7523586854592372736/

Post from the **Aegis AO Soft LLC** page (company id 143078465), aimed at rental companies on Fleetwire.
Image: `social/linkedin-fleetwire-card.png` (1200×900, built from `build/youtube/post-card-fleetwire.html`).
Fleetwire appears as text only: their logo has not been supplied yet.

---

## Post — English

MyEZToll now works with Fleetwire.

Rental companies on Fleetwire can get tolls and tickets onto the right rental without logging into agency portals or matching statements by hand.

How it works:

1️⃣ Turn on MyEZToll in Fleetwire, under Connections → Toll and violation partners.

2️⃣ Add your toll accounts to MyEZToll. We cover 30+ US agencies, plus Canada.

3️⃣ Agency tolls and violations reach Fleetwire as charges on the matching rental, with the agency amount and our service fee shown separately. A charge with no matching rental waits for the host to review.

Your renters are billed from Fleetwire, the system you already use.

Thanks to the Fleetwire team for building their Partner API with us.

MyEZToll is operated under licence by Aegis AG Soft LLC.

#CarRental #FleetManagement #TollManagement #Integration

**First comment:** MyEZToll: https://myeztoll.com · Fleetwire: https://fleetwire.io

| Claim | Where it is checked |
|---|---|
| charges on the rental, tolls and violations | `FleetwirePlatformProvider.Partner.cs` (kind toll / violation, `AttributesChargesToRentals`) |
| agency amount and service fee separate | `amount_cents` + `provider_fee_cents` in `FleetwirePartnerModels.cs` |
| agency tolls only | Chad 14.10; GPS-sourced rows are filtered on the host |
| unmatched goes to host review | Fleetwire Partner API docs (`match: unmatched`) |
| Connections → Toll and violation partners | Chad's email 14.10, not checked in Fleetwire's UI |

Not claimed: host names, host or car counts, prices, free trial.
