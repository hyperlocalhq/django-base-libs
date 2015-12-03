#! /usr/bin/env python
#  -*- coding: UTF-8 -*-

import csv
from pprint import pprint as pp
from collections import defaultdict

import categories
import terms

cs = categories.main()
ts = terms.main()

reverse_cs = defaultdict(list)
for k, v in cs.items():
    reverse_cs[v] += [k]

reverse_ts = defaultdict(list)
for k, v in ts.items():
    reverse_ts[v] += [k]

ts2cs = None
with open('csv/terms2categories.csv') as f:
    r = csv.DictReader(f, delimiter=';')
    ls = [(
              row['term'],
              (row['category'], row['category_sysname']),
          ) for row in r]
    ts2cs = dict(ls)
    del ts2cs['']

# pp(ts2cs)
# pp(dict(reverse_cs))
pp(dict(reverse_ts))
