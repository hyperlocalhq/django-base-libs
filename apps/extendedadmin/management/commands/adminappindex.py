# -*- coding: UTF-8 -*-
from django.core.management.base import NoArgsCommand
from django.contrib.admin.sites import site
from django.utils.text import capfirst
from django.utils.safestring import mark_safe
from django.contrib import admin


class Command(NoArgsCommand):
    help = """
    Prints a sample ADMIN_APP_INDEX to put in the settings
    
    In addition, you can add 'verbose_name' and 'classes' settings to the options for apps
    
        Structure:
        
        ADMIN_APP_INDEX = (
            {
                'title': _('<group_title>'),
                'apps': (
                    ('<app_label>', app_options),
                    ...
                ),
            },{
                ...
            }
        )
        
        app_options == {
            'verbose_name': _("<App Verbose Name>"),
            'models': (model, ...)
            'classes': ('<css_class>', ...),
            }
        
        model == '<ModelName>'
    
    """

    def handle_noargs(self, **options):
        admin.autodiscover()
        app_dict = {}

        for model, model_admin in site._registry.items():
            app_label = model._meta.app_label
            model_dict = {
                'name':
                    capfirst(model._meta.verbose_name_plural),
                'admin_url':
                    mark_safe('%s/%s/' % (app_label, model.__name__.lower())),
            }
            if app_label in app_dict:
                app_dict[app_label]['model_dict'][model.__name__] = model_dict
            else:
                app_dict[app_label] = {
                    'app_label': app_label,
                    'name': app_label.title(),
                    'app_url': app_label + '/',
                    'model_dict': {
                        model.__name__: model_dict
                    },
                }

        # Sort the apps alphabetically.
        app_list = app_dict.values()
        app_list.sort(lambda x, y: cmp(x['name'], y['name']))

        print """
ADMIN_APP_INDEX = (
    {
        'title': "Enter a group name here...",
        'apps': ("""
        for app in app_list:
            models = app['model_dict'].keys()
            if models:
                # Sort the models alphabetically within each app.
                models.sort()
                print """
            ("%s", {
                'models': ("%s",),
            }),""" % (app['app_label'], '", "'.join(models))

        print """
        ),
    },
)
"""
