#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import requests
import timeit

# code copied from this gist: https://gist.github.com/tylerhartley/5174230
# tic toc functions ala Matlab
import time

def tic(tag=None):
    '''Start timer function.
    tag = used to link a tic to a later toc. Can be any dictionary-able key.
    '''
    global TIC_TIME
    if tag is None:
        tag = 'default'

    try:
        TIC_TIME[tag] = time.time()
    except NameError:
        TIC_TIME = {tag: time.time()}


def toc(tag=None, save=False, fmt=False):
    '''Timer ending function.
    tag - used to link a toc to a previous tic. Allows multipler timers, nesting timers.
    save - if True, returns float time to out (in seconds)
    fmt - if True, formats time in H:M:S, if False just seconds.
    '''
    global TOC_TIME
    template = 'Elapsed time is:'
    if tag is None:
        tag = 'default'
    else:
        template = '%s - '%tag + template

    try:
        TOC_TIME[tag] = time.time()
    except NameError:
        TOC_TIME = {tag: time.time()}

    if TIC_TIME:
        d = (TOC_TIME[tag]-TIC_TIME[tag])

        if fmt:
            print template + ' %s'%time.strftime('%H:%M:%S', time.gmtime(d))
        else:
            print template + ' %f seconds'%(d)

        if save: return d

    else:
        print "no tic() start time available. Check global var settings"
# end of gist code

BASE_URL = 'http://www.berlin-buehnen.de'
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
toc()

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
        data = r.json()
        if data and 'meta' in data:
            meta = data['meta']
            if meta and 'next' in meta:
                next = meta['next']
                return_value = next
    return return_value

while next_path:
    tic()
    next_path = get_next(next_path)
    toc()

