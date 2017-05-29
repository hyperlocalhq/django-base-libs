# -*- coding: UTF-8 -*-
from django.template.loader import select_template


def get_template_dir_from_object(obj):
    """
    gets the relative template dir from an object.
    """
    if obj:
        return "%s/" % obj._meta.app_label
    return ""


def select_template_for_object(template_name, obj, app_dir):
    """
    tries to get a template from some object-template dir.
    If this one does not exist, return a default template.
    """
    obj_template_name = ""
    if obj:
        obj_template_name = "%s%s/%s" % \
            (get_template_dir_from_object(obj), app_dir, template_name)
    return select_template([obj_template_name, "%s/%s" % (app_dir, template_name)])


def select_template_name(template_name_prefix, obj, app_dir, use_embedded=False):
    """
    tries to get a atemplate with a given prefix and an optional 
    "use_embedded" parameter:
    """
    template_name = template_name_prefix
    if use_embedded:    
        template_name = "%s_embedded" % template_name_prefix
    t = select_template_for_object("%s.html" % template_name, obj, app_dir)
    if t:
        return t.origin.loadname
    return ""
