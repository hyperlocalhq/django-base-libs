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
              (row['category'], row['category_slug']),
          ) for row in r]
    ccs2cs = dict(ls)

# pp(ccs2cs)
# pp(dict(reverse_cs))
# pp(dict(reverse_ccs))

ccs_slug2cs_slug = {}
for contexcategory in ccs2cs:
    category, slug = ccs2cs[contexcategory]
    try:
        contexcategory_slug = reverse_ccs[contexcategory.strip()][0]
    except IndexError:
        print 'no slug for contextcategory with title "{}"'.format(contexcategory.strip())
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
    ccs_slug2cs_slug[contexcategory_slug] = category_slug

# pp(ccs_slug2cs_slug)

items = ccs_slug2cs_slug.items()
items.sort()
mappings = []
for cc_slug, c_slug in items:
    cc_title = ccs[cc_slug]
    c_title = cs[c_slug]
    mappings += [{
        'context category title': cc_title,
        'context category slug': cc_slug,
        'category title': c_title,
        'category slug': c_slug,
    }]

# pp(mappings)

with open('full_contextcategories2categories.csv', 'w') as csvfile:
    fieldnames = [
        'context category title',
        'context category slug',
        'category title',
        'category slug',
    ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

    writer.writeheader()
    for d in mappings:
        writer.writerow(d)
