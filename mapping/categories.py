#! /usr/bin/env python
#  -*- coding: UTF-8 -*-

import csv
from pprint import pprint as pp

d = None

with open('tsv/categories.tsv') as f:
    r = csv.DictReader(f, delimiter='\t')
    ls = [(
              row['sysname'],
              row['title'],
          ) for row in r]
    d = dict(ls)

pp(d)
