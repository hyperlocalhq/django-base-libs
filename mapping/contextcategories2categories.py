#! /usr/bin/env python
#  -*- coding: UTF-8 -*-

import csv
from pprint import pprint as pp
import categories
import contextcategories

cs = categories.main()
ccs = contextcategories.main()

ccs2cs = None

with open('csv/contextcategories2categories.csv') as f:
    r = csv.DictReader(f, delimiter=';')
    ls = [(
              row['context category'],
              (row['category'], row['category_sysname']),
          ) for row in r]
    ccs2cs = dict(ls)

del ccs2cs['']
pp(ccs2cs)

