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


def create_pages_and_plugins(page_tree, parent_page=None):
    from copy import deepcopy
    from dateutil.parser import parse
    from django.contrib.sites.models import Site
    from cms.api import create_page, create_title, add_plugin

    for page_dict in page_tree:
        page = None
        for lang_code, title_dict in page_dict.get('titles').items():
            if not page:
                page = create_page(
                    title=title_dict['title'],
                    template=page_dict['template'],
                    language=lang_code,
                    menu_title=title_dict['menu_title'],
                    slug=title_dict['slug'],
                    apphook=title_dict['application_urls'],
                    apphook_namespace=None,
                    redirect=title_dict['redirect'],
                    meta_description=title_dict['meta_description'],
                    created_by=page_dict['created_by'],
                    parent=parent_page,
                    publication_date=parse(page_dict['publication_date']) if page_dict['publication_date'] else None,
                    publication_end_date=parse(page_dict['publication_end_date']) if page_dict['publication_end_date'] else None,
                    in_navigation=page_dict['in_navigation'],
                    soft_root=page_dict['soft_root'],
                    reverse_id=page_dict['reverse_id'],
                    navigation_extenders=page_dict['navigation_extenders'],
                    published=page_dict['published'],
                    site=Site.objects.get(pk=page_dict['site']),
                    login_required=page_dict['login_required'],
                    limit_visibility_in_menu=page_dict['limit_visibility_in_menu'],
                    position="last-child",
                    overwrite_url=title_dict['path'] if title_dict['has_url_overwrite'] else "",
                    #xframe_options=Page.X_FRAME_OPTIONS_INHERIT,
                )
            else:
                create_title(
                    language=lang_code,
                    title=title_dict['title'],
                    page=page,
                    menu_title=title_dict['menu_title'],
                    slug=title_dict['slug'],
                    redirect=title_dict['redirect'],
                    meta_description=title_dict['meta_description'],
                    parent=parent_page,
                    overwrite_url=title_dict['path'] if title_dict['has_url_overwrite'] else "",
                )
        placeholder_slots = page.rescan_placeholders()
        for placeholder_dict in page_dict.get('placeholders', []):
            placeholder = placeholder_slots.get(placeholder_dict['slot'])
            if not placeholder:
                # there seemed to be some trash data in the database,
                # where placeholder was commented out or removed from the template
                continue
            for lang_code, plugin_dict_list in placeholder_dict.get("plugins", {}).items():
                for plugin_dict in sorted(plugin_dict_list, key=lambda d: d['position']):
                    plugin_data = deepcopy(plugin_dict)
                    plugin_data.pop('parent')
                    plugin_data.pop('tree_id')
                    plugin_data.pop('lft')
                    plugin_data.pop('rght')
                    plugin_data.pop('position')
                    plugin_data.pop('level')
                    plugin_data.pop('placeholder')
                    plugin_data.pop('pk')
                    plugin_data.pop('language')
                    plugin_data.pop('plugin_type')
                    plugin_data.pop('plugin_model', None)  # TODO: isn't this redundant?
                    plugin_data.pop('links', None)  # very Berlin Buehnen specific
                    plugin = add_plugin(
                        placeholder=placeholder,
                        plugin_type=plugin_dict['plugin_type'],
                        language=lang_code,
                        position="last-child",
                        target=plugin_dict['parent'],
                        **plugin_data
                    )
                    # very Berlin Buehnen specific situation:
                    if plugin_dict['plugin_type'] == "LinkCategoryPlugin":
                        for link_dict in plugin_dict['links']:
                            plugin.link_set.create(
                                title=link_dict['title'],
                                url=link_dict['url'],
                                short_description=link_dict['short_description'],
                                sort_order=link_dict['sort_order'],
                            )

        # save the children pages recursively
        if page_dict.get('children', []):
            create_pages_and_plugins(page_tree, parent_page=page)

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
        create_pages_and_plugins(page_tree)


if __name__ == "__main__":
    setup()
    main()