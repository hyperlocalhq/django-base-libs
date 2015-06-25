# -*- coding: UTF-8 -*-

from django.db.models.loading import get_app
from django import template
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

register = template.Library()

### TAGS ###

def jetson_media_url():
    return getattr(settings, "JETSON_MEDIA_URL", "")
register.simple_tag(jetson_media_url)

### FILTERS ### 

def is_installed(appname):
    """
    Checks if an app is installed <=> listed in the INSTALLED_APPS
    """
    success = False
    try:
        get_app(appname)
        success = True
    except:
        pass
    return success

register.filter('is_installed', is_installed)

def app_verbose_name(appname):
    """
    Returns the verbose name of an app.
    If verbose_name is neither found in ADMIN_APP_INDEX nor in the models.py,
    the titled version of the app is returned.
    """
    appname = appname.lower()
    verbose_name = " ".join([word.title() for word in appname.split("_")])
    ADMIN_APP_INDEX = getattr(settings, "ADMIN_APP_INDEX", ())
    app_dict = {}
    for group in ADMIN_APP_INDEX:
        app_dict.update(dict(group['apps']))
    if appname in app_dict and 'verbose_name' in app_dict[appname]:
        verbose_name = _(app_dict[appname]['verbose_name'])
    else:
        app = get_app(appname)
        if hasattr(app, "verbose_name"):
            verbose_name = app.verbose_name
    return verbose_name
    
register.filter('app_verbose_name', app_verbose_name)


