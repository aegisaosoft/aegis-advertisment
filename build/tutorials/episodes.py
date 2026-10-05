# -*- coding: utf-8 -*-
"""The tutorial series, assembled.

The shape of an episode is in `model.py`; the content is in the `series_*.py` files,
grouped in roughly the order somebody would work through them in their first week.
This file only puts them in order, so `tts.py`, `build.py` and `render.js` have one
list to iterate and none of them has to know how many files the content is spread over.
"""
from model import B, E, CARD           # noqa: F401 - re-exported for the content files

import series_a
import series_b
import series_c
import series_d
import series_e
import series_f
import series_g
import series_h
import series_i
import series_j
import series_k
import series_l
import series_m
import series_n
import series_o

SERIES = [
    series_a.EP01, series_a.EP02,                   # find your way around, set the rules
    series_b.EP03, series_b.EP04, series_b.EP05,    # agencies, the fleet list, adding cars
    series_c.EP06, series_c.EP07, series_c.EP08,    # transponders, prices, bookings
    series_d.EP09, series_d.EP10, series_d.EP11,    # tolls, charges, violations
    series_e.EP12, series_e.EP13, series_e.EP14,    # payments, Stripe, payouts
    series_f.EP15, series_f.EP16, series_f.EP17,    # GPS, alerts, drivers
    series_g.EP18, series_g.EP19,                   # platform bookings, storefront
    series_h.EP20, series_h.EP21,                   # reports, the last settings tabs
    series_i.EP22, series_i.EP23, series_i.EP24, series_i.EP25, series_i.EP26,  # Turo
    series_j.EP27, series_j.EP28, series_j.EP29, series_j.EP30,  # HQ Rental Software
    series_k.EP31, series_k.EP32, series_k.EP33,  # collections agencies
    series_l.EP34, series_l.EP35,  # registration: owner, partner
    series_m.EP36, series_m.EP37, series_m.EP38,  # partners: payment options
    series_m.EP39, series_m.EP40,                 # partners: the amounts
    series_n.EP41, series_n.EP42, series_n.EP43, series_n.EP44, series_n.EP45,  # partners: the API
    series_o.EP46, series_o.EP47, series_o.EP48, series_o.EP49,  # Tesla
]

BY_NUM = dict((e.num, e) for e in SERIES)
