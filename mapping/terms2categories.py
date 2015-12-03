#! /usr/bin/env python
#  -*- coding: UTF-8 -*-

import csv
from pprint import pprint as pp

d = None

with open('csv/terms2categories.csv') as f:
    r = csv.DictReader(f, delimiter=';')
    ls = [(
              row['term'],
              (row['category'], row['category_sysname']),
          ) for row in r]
    d = dict(ls)

del d['']
pp(d)
