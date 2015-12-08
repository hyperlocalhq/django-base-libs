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
              (row['category'], row['category_slug']),
          ) for row in r]
    ts2cs = dict(ls)

# pp(ts2cs)
# pp(dict(reverse_cs))
# pp(dict(reverse_ts))

ts_slug2cs_slug = {}
for term in ts2cs:
    category, slug = ts2cs[term]
    try:
        term_slug = reverse_ts[term.strip()][0]
    except IndexError:
        print 'no slug for term with title "{}"'.format(term.strip())
        continue
    category_slugs = reverse_cs[category.strip()]
    if not category:
        category_slug = 'sonstiges'
    else:
        if len(category_slugs) == 0:
            print 'no slugs for category with title "{}"'.format(category.strip())
            continue
        elif len(category_slugs) == 1:
            category_slug = category_slugs[0]
        else:
            category_slug = slug
    ts_slug2cs_slug[term_slug] = category_slug

# pp(ts_slug2cs_slug)

items = ts_slug2cs_slug.items()
items.sort()
mappings = []
for t_slug, c_slug in items:
    t_title = ts[t_slug]
    c_title = cs[c_slug]
    mappings += [{
        'term title': t_title,
        'term slug': t_slug,
        'category title': c_title,
        'category slug': c_slug,
    }]

# pp(mappings)

with open('full_terms2categories.csv', 'w') as csvfile:
    fieldnames = [
        'term title',
        'term slug',
        'category title',
        'category slug',
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

    writer.writeheader()
    for d in mappings:
        writer.writerow(d)
