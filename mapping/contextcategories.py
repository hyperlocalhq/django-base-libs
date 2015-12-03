#! /usr/bin/env python
#  -*- coding: UTF-8 -*-

import csv
from pprint import pprint as pp

def main():
    d = None

    with open('tsv/contextcategories.tsv') as f:
        r = csv.DictReader(f, delimiter='\t')
        ls = [(
                  row['sysname'],
                  row['title'],
              ) for row in r]
        d = dict(ls)

    return d

if __name__ == '__main__':
    d = main()
    pp(d)
