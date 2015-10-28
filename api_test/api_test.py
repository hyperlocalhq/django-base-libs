#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import requests
import simplejson.scanner

from tictoc import tic, toc

BASE_URL = 'http://www.berlin-buehnen.de'
# BASE_URL = 'http://127.0.0.1:8005'
URL_PATH = '/de/api/v1/production/'
ENDPOINT = '{0}{1}'.format(BASE_URL, URL_PATH)

params = dict(
    format='json',
    username='BerlinOnline',
    api_key='3c42ccbfe87040951429e2d09c0e575747bac771',
    limit='25',
    offset='0',
)

tic()
r = requests.get(ENDPOINT, params=params)
print r.url
total_time = toc(save=True)

data = r.json()
next_path = None
if data and 'meta' in data:
    meta = data['meta']
    if meta and 'next' in meta:
        next_path = meta['next']

def get_next(next_path):
    return_value = None
    if next_path:
        url = '{0}{1}'.format(BASE_URL, next_path)
        r = requests.get(url)
        print r.url
        try:
            data = r.json()
            if data and 'meta' in data:
                meta = data['meta']
                if meta and 'next' in meta:
                    next = meta['next']
                    return_value = next
        except simplejson.scanner.JSONDecodeError:
            return_value = next_path
    return return_value

while next_path:
    tic()
    next_path = get_next(next_path)
    total_time += toc(save=True)

print 'Total time: {}'.format(total_time)
