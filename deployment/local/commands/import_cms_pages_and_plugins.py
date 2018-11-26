#!/usr/bin/env python
#  -*- coding: UTF-8 -*-
from __future__ import unicode_literals


def setup():
    import sys, os, django
    PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
    sys.path.append(PROJECT_PATH)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ruhrbuehnen.settings.local")
    django.setup()


class DataImporter(object):
    refined_data = {}
    page_tree = []
    old_page_id_to_new_page = {}

    def __init__(self):
        # create self.refined_data
        self.load_data()

        # create self.page_tree
        self.prepare_page_tree(self.refined_data)

        # for reference, save to a file
        self.save_page_tree(self.page_tree)

        # create pages, populate self.old_page_id_to_new_page
        print("=== Creating pages ===")
        self.create_pages(self.page_tree)
        self.update_page_mapper()
        print("=== Saving plugins ===")
        self.save_plugins(self.page_tree)
        print("=== Publishing pages ===")
        self.publish_pages(self.page_tree)

        print("Finished")

    def load_data(self):
        from collections import OrderedDict
        import os, json
        DUMP_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cms_pages.json")
        self.refined_data = OrderedDict()
        with open(DUMP_FILE) as fp:
            dump_data = json.load(fp)
            '''
            The syntax of the processed data will be as follows:
            refined_data[<app>][<model>][<pk>] = {<fields>}
            '''
            for elem in dump_data:
                app_label, model = elem['model'].split('.')
                fields = elem['fields']
                fields['pk'] = elem['pk']
                self.refined_data.setdefault(app_label, OrderedDict()).setdefault(model, OrderedDict())[elem['pk']] = fields

    def prepare_page_tree(self, data):
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
        # collect links (very specific to Ruhr Bühnen)
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

        self.page_tree = page_tree

    def save_page_tree(self, page_tree):
        import os, json
        import json
        REFERENCE_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "cms_pages_reorganized.json")
        with open(REFERENCE_FILE, 'w') as outfile:
            json.dump(page_tree, outfile, indent=4)

    def get_plugin_model_form(self, app_label, model_name):
        from django.apps import apps
        from django import forms
        _model = apps.get_model(app_label, model_name)
        class ModelForm(forms.ModelForm):
            class Meta:
                model = _model
                exclude = [
                    "placeholder", "parent", "position", "language", "plugin_type", "creation_date", "changed_date"
                ]
                fields = "__all__"
        return ModelForm

    def create_pages(self, page_tree, parent_page=None):
        from dateutil.parser import parse
        from django.contrib.sites.models import Site
        from cms.api import create_page, create_title

        for page_dict in page_tree:
            if page_dict.get('publisher_is_draft'):  # skip unpublished pages
               continue
            page = None
            for lang_code, title_dict in page_dict.get('titles').items():
                if not page:
                    print("    " * page_dict['level'] + title_dict['title'])
                    page = create_page(
                        title=title_dict['title'],
                        template=page_dict['template'],
                        language=lang_code,
                        menu_title=title_dict['menu_title'],
                        slug=title_dict['slug'],
                        apphook=title_dict['application_urls'] if not "BlogApphook" == title_dict['application_urls'] else "",
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
                    if page_dict['lft'] == 1:
                        page.is_home = True
                        page.save()
                    self.old_page_id_to_new_page[page_dict['pk']] = page
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
            # save the children pages recursively
            children = page_dict.get('children', [])
            if children:
                self.create_pages(children, parent_page=page)

    def update_page_mapper(self):
        for pk, fields in self.refined_data['cms']['page'].items():
            if fields['publisher_is_draft']:
                self.old_page_id_to_new_page[pk] = self.old_page_id_to_new_page[fields['publisher_public']]

    def save_plugins(self, page_tree, parent_page=None):
        from copy import deepcopy
        from cms.api import add_plugin
        from django.conf import settings

        for page_dict in page_tree:
            if page_dict.get('publisher_is_draft'):  # skip unpublished pages
               continue
            page = self.old_page_id_to_new_page.get(page_dict['pk'])
            if not page:
                continue

            placeholder_slots = page.rescan_placeholders()
            for placeholder_dict in page_dict.get('placeholders', []):
                placeholder = placeholder_slots.get(placeholder_dict['slot'])
                if not placeholder:
                    # there seemed to be some trash data in the database,
                    # where placeholder was commented out or removed from the template
                    print("Deprecated placholder found: " + placeholder_dict['slot'])
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
                        plugin_data.pop('links', None)  # very Berlin Buehnen specific
                        app_label, model_name = plugin_data.pop('plugin_model', (None, None))

                        if "internal_link" in plugin_data:
                            old_linked_page_id = plugin_data.pop('internal_link')
                            if old_linked_page_id:
                                linked_page = self.old_page_id_to_new_page.get(old_linked_page_id)
                                if linked_page:
                                    # reverse-enginered undocumented way to assign the page to a PageSelectFormField
                                    plugin_data["internal_link_0"] = settings.SITE_ID
                                    plugin_data["internal_link_1"] = linked_page.pk
                                    plugin_data["internal_link_2"] = linked_page.pk
                                else:
                                    print("Invalid internal link for plugin {}".format(plugin_dict['pk']))

                        if app_label and model_name:
                            # let's validate the data and change all ids to instances for the ModelChoiceField fields
                            PluginForm = self.get_plugin_model_form(app_label, model_name)
                            form = PluginForm(data=plugin_data)
                            if form.is_valid():
                                plugin_data = form.cleaned_data
                            else:
                                print("Error while validating {}.{} with id {}".format(app_label, model_name, plugin_dict['pk']))
                                print(form.errors)

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
                        else:
                            print("Incomplete plugin with id {}".format(plugin_dict['pk']))

            # save the children pages recursively
            children = page_dict.get('children', [])
            if children:
                self.save_plugins(children, parent_page=page)

    def publish_pages(self, page_tree, parent_page=None):
        from django.contrib.auth.models import User
        from cms.api import publish_page

        for page_dict in page_tree:
            if page_dict.get('publisher_is_draft'):  # skip unpublished pages
               continue
            page = self.old_page_id_to_new_page.get(page_dict['pk'])
            if not page:
                continue

            if page_dict['published']:
                user = User.objects.get(username=page_dict['created_by'])
                for lang_code, title_dict in page_dict.get('titles').items():
                    publish_page(page, user, lang_code)

            # save the children pages recursively
            children = page_dict.get('children', [])
            if children:
                self.publish_pages(children, parent_page=page)


if __name__ == "__main__":
    setup()
    DataImporter()
