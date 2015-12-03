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

# pp(ccs2cs)
# pp(dict(reverse_cs))
# pp(dict(reverse_ccs))

ccs_sysname2cs_sysname = {}
for contexcategory in ccs2cs:
    category, sysname = ccs2cs[contexcategory]
    try:
        contexcategory_sysname = reverse_ccs[contexcategory.strip()][0]
    except IndexError:
        print 'no sysname for contextcategory with title "{}"'.format(contexcategory.strip())
        continue
    category_sysnames = reverse_cs[category.strip()]
    if not category:
        category_sysname = 'miscellaneous'
    else:
        if len(category_sysnames) == 0:
            print 'no sysnames for category with title "{}"'.format(category.strip())
            continue
        elif len(category_sysnames) == 1:
            category_sysname = category_sysnames[0]
        else:
            category_sysname = sysname
    ccs_sysname2cs_sysname[contexcategory_sysname] = category_sysname

# pp(ccs_sysname2cs_sysname)

mappings = []
for cc_sysname, c_sysname in ccs_sysname2cs_sysname.items():
    cc_title = ccs[cc_sysname]
    c_title = cs[c_sysname]
    mappings += [{
        'context category title': cc_title,
        'context category slug': cc_sysname,
        'category title': c_title,
        'category slug': c_sysname,
    }]

pp(mappings)
