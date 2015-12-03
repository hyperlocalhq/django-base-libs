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

# pp(ts2cs)
# pp(dict(reverse_cs))
# pp(dict(reverse_ts))

ts_sysname2cs_sysname = {}
for term in ts2cs:
    category, sysname = ts2cs[term]
    try:
        term_sysname = reverse_ts[term.strip()][0]
    except IndexError:
        print 'no sysname for term with title "{}"'.format(term.strip())
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
    ts_sysname2cs_sysname[term_sysname] = category_sysname

# pp(ts_sysname2cs_sysname)

mappings = []
for t_sysname, c_sysname in ts_sysname2cs_sysname.items():
    t_title = ts[t_sysname]
    c_title = cs[c_sysname]
    mappings += [{
        'context category title': t_title,
        'context category slug': t_sysname,
        'category title': c_title,
        'category slug': c_sysname,
    }]

pp(mappings)
