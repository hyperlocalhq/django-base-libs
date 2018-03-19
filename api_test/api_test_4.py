#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import requests

total_count_from_api = 0
total_count = 0

def check_page_data(data):
    global total_count
    total_count += len(data['objects'])


BASE_URL = 'http://www.berlin-buehnen.de'
# BASE_URL = 'http://127.0.0.1:8005'
URL_PATH = '/de/api/v1/production/'
ENDPOINT = '{0}{1}'.format(BASE_URL, URL_PATH)

params = dict(
    format='json',
    username='Cinemarketing',
    api_key='3769231756cd12a55e5fc8467c15f8ad50dbef2a',
    limit='25',
    offset='0',
)

r = requests.get(ENDPOINT, params=params)
print r.url

data = r.json()
next_path = None
if data and 'meta' in data:
    meta = data['meta']
    if meta and 'next' in meta:
        next_path = meta['next']
    total_count_from_api = meta['total_count']
    check_page_data(data)

def get_next(next_path):
    return_value = None
    if next_path:
        url = '{0}{1}'.format(BASE_URL, next_path)
        r = requests.get(url)
        print r.url
        data = r.json()
        if data and 'meta' in data:
            meta = data['meta']
            if meta and 'next' in meta:
                next = meta['next']
                return_value = next
        check_page_data(data)
    return return_value

while next_path:
    next_path = get_next(next_path)

print("total_count_from_api: {0}".format(total_count_from_api))
print("total_count: {0}".format(total_count))