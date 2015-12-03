#! /usr/bin/env python
#  -*- coding: UTF-8 -*-

import csv
from pprint import pprint as pp
from collections import defaultdict

import categories
import contextcategories

cs = categories.main()
ccs = contextcategories.main()

reverse_cs = defaultdict(list)
for k, v in cs.items():
    reverse_cs[v] += [k]

reverse_ccs = defaultdict(list)
for k, v in ccs.items():
    reverse_ccs[v] += [k]

ccs2cs = None
with open('csv/contextcategories2categories.csv') as f:
    r = csv.DictReader(f, delimiter=';')
    ls = [(
              row['context category'],
              (row['category'], row['category_sysname']),
          ) for row in r]
    ccs2cs = dict(ls)
    del ccs2cs['']

# pp(ccs2cs)
# pp(dict(reverse_cs))
pp(dict(reverse_ccs))
