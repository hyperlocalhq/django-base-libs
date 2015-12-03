#! /usr/bin/env python
#  -*- coding: UTF-8 -*-

import csv
from pprint import pprint as pp
import categories
import terms

cs = categories.main()
ts = terms.main()

ts2cs = None

with open('csv/terms2categories.csv') as f:
    r = csv.DictReader(f, delimiter=';')
    ls = [(
              row['term'],
              (row['category'], row['category_sysname']),
          ) for row in r]
    ts2cs = dict(ls)

del ts2cs['']
pp(ts2cs)
