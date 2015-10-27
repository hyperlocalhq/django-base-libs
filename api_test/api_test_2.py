#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import requests

from tictoc import tic, toc

BASE_URL = 'http://www.berlin-buehnen.de'
# BASE_URL = 'http://127.0.0.1:8005'
endpoints = (
    '/de/api/v1/production/?username=BerlinOnline&api_key=3c42ccbfe87040951429e2d09c0e575747bac771&limit=25&offset=3675&format=json',
    '/de/api/v1/production/?username=BerlinOnline&api_key=3c42ccbfe87040951429e2d09c0e575747bac771&limit=25&offset=5625&format=json',
    '/de/api/v1/production/?username=BerlinOnline&api_key=3c42ccbfe87040951429e2d09c0e575747bac771&limit=25&offset=5600&format=json',
    '/de/api/v1/production/?username=BerlinOnline&api_key=3c42ccbfe87040951429e2d09c0e575747bac771&limit=25&offset=4200&format=json',
    '/de/api/v1/production/?username=BerlinOnline&api_key=3c42ccbfe87040951429e2d09c0e575747bac771&limit=25&offset=4950&format=json',
    '/de/api/v1/production/?username=BerlinOnline&api_key=3c42ccbfe87040951429e2d09c0e575747bac771&limit=25&offset=5750&format=json',
    '/de/api/v1/production/?username=BerlinOnline&api_key=3c42ccbfe87040951429e2d09c0e575747bac771&limit=25&offset=1375&format=json',
    '/de/api/v1/production/?username=BerlinOnline&api_key=3c42ccbfe87040951429e2d09c0e575747bac771&limit=25&offset=5725&format=json',
    '/de/api/v1/production/?username=BerlinOnline&api_key=3c42ccbfe87040951429e2d09c0e575747bac771&limit=25&offset=2150&format=json',
    '/de/api/v1/production/?username=BerlinOnline&api_key=3c42ccbfe87040951429e2d09c0e575747bac771&limit=25&offset=5700&format=json',
)

total_time = 0
for endpoint in endpoints:
    tic()
    r = requests.get(BASE_URL + endpoint)
    print r.url
    total_time += toc(save=True)

print 'Total time: {}'.format(total_time)
