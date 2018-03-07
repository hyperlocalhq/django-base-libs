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


def prepare_page_tree(data):
    from copy import deepcopy
    data = deepcopy(data)
    '''
    The syntax of the page_tree will be as follows:
    [
        {
            'placeholders': [
                '<placeholder name 1>': {
                    'plugins': {
                        'en': [
                            {...plugin 1 fields...},
                            {...plugin 2 fields...},
                            ...
                        ],
                        'de': [
                            {...plugin 1 fields...},
                            {...plugin 2 fields...},
                            ...
                        ],
                    },
                    ...
                },
                '<placeholder name 2>': {
                    'plugins': {
                        'en': [],
                        'de': [],
                    },
                    ...
                },
                ...
            ],
            'titles': {
                'en': {...en title fields...},
                'de': {...de title fields...},
            }
            ...other page fields...
            'children': [...]
        }
    ]
    '''
    # collect links (very specific to Berlin Bühnen)
    for pk, fields in data['services']['link'].items():
        data['services']['linkcategory'][fields['category']].setdefault('links', []).append(fields)

    # combine all plugins into cms.cmsplugin fields
    plugin_models = [
        ("richtext", "richtext"),
        ("page_teaser", "pageteaser"),
        ("services", "indexitem"),
        ("services", "servicepagebanner"),
        ("services", "servicegriditem"),
        ("services", "servicelistitem"),
        ("services", "linkcategory"),
        ("services", "titleandtext"),
        ("services", "imageandtext"),
    ]
    for app_label, model in plugin_models:
        for pk, fields in data[app_label][model].items():
            data['cms']['cmsplugin'][pk]['plugin_model'] = (app_label, model)
            data['cms']['cmsplugin'][pk].update(fields)

    # collect plugins to placeholders
    for pk, fields in data['cms']['cmsplugin'].items():
        data['cms']['placeholder'][fields['placeholder']].setdefault('plugins', {}).setdefault(fields['language'], []).append(fields)

    # collect placeholders to pages
    for pk, fields in data['cms']['page'].items():
        fields['placeholders'] = [
            data['cms']['placeholder'][pk] for pk in fields['placeholders']
        ]

    # collect pagetitles to pages
    for pk, fields in data['cms']['title'].items():
        data['cms']['page'][fields['page']].setdefault('titles', {})[fields['language']] = fields

    # collect pages to a tree
    page_tree = []
    page_ids_sorted_reversed = [
        page['pk'] for page in sorted(

            data['cms']['page'].values(),
            key=lambda elem: (elem['tree_id'], elem['lft']),
            reverse=True,
        )
    ]
    for pk in page_ids_sorted_reversed:
        page_fields = data['cms']['page'].pop(pk)
        parent_pk = page_fields['parent']
        if parent_pk:
            data['cms']['page'][parent_pk].setdefault('children', []).insert(0, page_fields)
        else:
            page_tree.insert(0, page_fields)

    return page_tree


def save_page_tree(page_tree):
    import os, json
    import json
    REFERENCE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cms_pages_reorganized.json")
    with open(REFERENCE_FILE, 'w') as outfile:
        json.dump(page_tree, outfile, indent=4)


def create_database_objects(page_tree):
    print("Finished")


def main():
    from collections import OrderedDict
    import os, json
    DUMP_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cms_pages.json")
    with open(DUMP_FILE) as fp:
        dump_data = json.load(fp)
        refined_data = OrderedDict()
        '''
        The syntax of the processed data will be as follows:
        processed_data[<app>][<model>][<pk>] = {<fields>}
        '''
        for elem in dump_data:
            app_label, model = elem['model'].split('.')
            fields = elem['fields']
            fields['pk'] = elem['pk']
            refined_data.setdefault(app_label, OrderedDict()).setdefault(model, OrderedDict())[elem['pk']] = fields

        page_tree = prepare_page_tree(refined_data)
        save_page_tree(page_tree)
        create_database_objects(page_tree)


if __name__ == "__main__":
    setup()
    main()