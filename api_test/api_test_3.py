#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import requests

from tictoc import tic, toc

BASE_URL = 'http://www.berlin-buehnen.de'
# BASE_URL = 'http://127.0.0.1:8005'
ENDPOINT = '/de/api/v1/production/'
URL = BASE_URL + ENDPOINT

OFFSET = 5700

params = dict(
    format='json',
    username='BerlinOnline',
    api_key='3c42ccbfe87040951429e2d09c0e575747bac771',
    limit='1',
)

total_time = 0
for i in range(25):
    tic()
    params['offset'] = str(OFFSET + i)
    r = requests.get(URL, params=params)
    print r.url
    total_time += toc(save=True)

print 'Total time: {}'.format(total_time)
