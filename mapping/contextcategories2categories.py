#! /usr/bin/env python
#  -*- coding: UTF-8 -*-

import csv
from pprint import pprint as pp

d = None

with open('csv/contextcategories2categories.csv') as f:
    r = csv.DictReader(f, delimiter=';')
    ls = [(
              row['context category'],
              (row['category'], row['category_sysname']),
          ) for row in r]
    d = dict(ls)

del d['']
pp(d)
