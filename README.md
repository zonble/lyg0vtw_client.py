lyg0vtw_client.py
=================

> **⚠️ This project is archived and no longer maintained.**
> The upstream API (`api-beta.ly.g0v.tw`) is no longer available. This repository is kept for historical reference only.

[![Build Status](https://travis-ci.org/zonble/lyg0vtw_client.py.png?branch=master)](https://travis-ci.org/zonble/lyg0vtw_client.py)

A Python module to access [api-beta.ly.g0v.tw](http://api-beta.ly.g0v.tw), which was the open data API for the [Legislative Yuan of Taiwan](https://www.ly.gov.tw/) (立法院) provided by the [g0v.tw](https://g0v.tw/) civic technology community.

## Background

[g0v.tw](https://g0v.tw/) is a Taiwanese civic tech community that forks government websites and services to make public data more accessible. The `ly.g0v.tw` project specifically focused on the Legislative Yuan (Taiwan's parliament), parsing and republishing legislative data — including bills, motions, and committee sittings — through an open REST API at `http://api-beta.ly.g0v.tw/v0/`.

This client library was written around 2013, during the early days of the g0v movement.

## What the API Provided

The API exposed three main collections from the Legislative Yuan:

- **Bills** (`/collections/bills`) — legislative bills including sponsors, co-sponsors, abstracts, summaries, and related document links (PDF/DOC).
- **Motions** (`/collections/motions`) — individual motions tied to bills and committee sittings, with voting results and resolutions.
- **Sittings** (`/collections/sittings`) — committee and plenary sitting records, including dates, session numbers, and video links.

## Usage

```python
from lyg0vtw_client import lyg0vtw_client

client = lyg0vtw_client.LY_G0V_Client()

# Fetch all bills
bills = client.fetch_all_bills()

# Fetch all motions
motions = client.fetch_all_motions()

# Fetch all sittings
sittings = client.fetch_all_sittings()

# Fetch a specific bill by its ID
bill = client.fetch_bill('1021021071000400')

# Fetch the full text/data of a specific bill
bill_data = client.fetch_bill_data('1021021071000400')

# Fetch motions related to a specific bill
related_motions = client.fetch_motions_related_with_bill('1021021071000400')
```

## Python Compatibility

The module was written to support both Python 2 (2.6, 2.7) and Python 3 (3.3+), using conditional imports for `urllib`.
