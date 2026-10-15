# Ad copy — the in-app help assistant (post 2)

Written 2026-09-06. Companion image: `myeztoll-help-15-languages.png` (1200×1200).

**Published 2026-09-06** from the Aegis AO Soft LLC page, image attached, visible to anyone:
https://www.linkedin.com/feed/update/urn:li:activity:7502390929081806849/

Everything claimed here is checkable in `docs/pagehelp/*.json` (61 topics × 15 locales) and in
`Back/Aegis.Back/BusinessServices/PageHelp*.cs`:

| claim | where it lives |
|-------|----------------|
| 61 topics, 15 languages | `docs/pagehelp/en.json` (61 keys) + 14 locale files |
| English is the source, the rest translated from it | `PageHelpService.TranslateAsync` |
| English is the fallback so no page is help-less | `PageHelpService.GetAsync` |
| assistant reads the owner's own records | `PageHelpTools` |
| owner id comes from the caller, never from the model | `IPageHelpTools.RunAsync` contract |
| read-only, capped rows | `PageHelpTools` — `MaxRows = 20`, no write tool |
| learned answers plus paraphrases | `PageHelpQaStore.LearnAsync` |
| an admin can edit or block a learned answer | `PageHelpQaStore.UpdateAsync` |
| the answer navigates to the page, named in the caller's language | `PageHelpService` nav links |
| a send is prepared, shown, and only then confirmed by a person | `IPageHelpActions.PrepareAsync` / `ConfirmAsync` |
| the owner id is re-checked against the token at confirm time | `PageHelpPendingAction.OwnerId` |

**Not claimed on purpose:** the web-search pass (built, off by setting, not deployed).

---

## Post — English

Your night dispatcher does not necessarily think in English. Neither does the person who
takes the 6 a.m. call about a toll nobody recognises. Every fleet portal I have seen hands
them a manual in one language and wishes them luck.

MyEZToll's help is written once, in English, then carried into fourteen more — Spanish,
Portuguese, French, German, Turkish, Russian, Ukrainian, Uzbek, Armenian, Georgian, Persian,
Urdu, and both written forms of Chinese. Sixty-one topics, one for every page of the portal,
and English stays underneath as the safety net so no page is ever left without help.

A translated manual is still a manual. What matters is the assistant behind it.

Ask in your own language and the answer comes back in it — drawn from the product's own
documentation and from your own records: which booking was open at the minute of that
crossing, what is still unpaid, which trips came in from Turo. It only reads. And the
account it reads is the account you signed into — the server decides that, never the model
— so no clever phrasing gets anyone a look at another operator's fleet.

It learns as it goes. The first time somebody asks something new, the answer is composed
and then kept, together with the other ways people word the same question. The next person
to ask gets it at once. An administrator can edit or block anything it has learned, so the
help gets better with use instead of drifting.

And it does not just explain. It takes you there — the button carries the same page name
your menu shows, in your language.

It can act, too, and only with a hand on it. Ask it to send a driver the card link or the
rental agreement and it finds the booking and drafts the send, then stops. The panel shows
you the driver, the phone and the address it would reach, and on which channel, before
anything leaves the building. You press confirm. Nothing goes out on a model's say-so.

Free for the fleet, like the rest of it.

https://myeztoll.com

#FleetManagement #CarRental #CustomerExperience #Localization #Tolls

---

## Short version — caption / email subject / ad headline

**EN** — Help on every page of MyEZToll, in fifteen languages, that reads your own records to
answer and learns from every question asked. Free for the fleet. myeztoll.com
