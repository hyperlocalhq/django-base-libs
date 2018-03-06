#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
from __future__ import unicode_literals


def setup():
    import sys, os, django
    PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
    print(PROJECT_PATH)
    sys.path.append(PROJECT_PATH)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "berlinbuehnen.settings.local")
    django.setup()


def create_database_objects(data):
    import json
    print(json.dumps(data, indent=2))


def main():
    from collections import OrderedDict
    import os, json
    DUMP_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cms_pages.json")
    with open(DUMP_FILE) as fp:
        json_data = json.load(fp)
        processed_data = OrderedDict()
        '''
        The syntax of the processed data will be as follows:
        processed_data[<app>][<model>][<pk>] = {<fields>}
        '''
        for elem in json_data:
            app_label, model = elem['model'].split('.')
            fields = elem['fields']
            fields['pk'] = elem['pk']
            processed_data.setdefault(app_label, OrderedDict()).setdefault(model, OrderedDict())[elem['pk']] = fields
        create_database_objects(processed_data)


if __name__ == "__main__":
    setup()
    main()