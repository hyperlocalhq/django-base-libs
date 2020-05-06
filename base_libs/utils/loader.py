# -*- coding: UTF-8 -*-
from django.template.loader import select_template as django_select_template


def get_template_name_list_for_object(
    template_name_prefix, obj, app_dir, use_embedded=False
):
    """
    Returns a list of template names to search for a specific template

    :param template_name_prefix: template file name with or without extension
    :param obj: object to which the template is related to
    :param app_dir: template (sub)directory to search for the template file
    :param use_embedded: suffix with "_embedded" or not?
    :return: list of template names

    For example,
    select_template_for_object("post_list.html", person, "blog", use_embedded=False)
    would return ["people/blog/post_list.html", "blog/post_list.html"]

    select_template_for_object("post_details", person, "blog", use_embedded=True)
    would return a ["people/blog/post_details_embedded.html", "blog/post_details_embedded.html"]

    select_template_for_object("post_details", None, "blog", use_embedded=False)
    would return a ["blog/post_details.html"]
    """
    template_list = []

    if template_name_prefix.endswith(".html"):
        template_name = template_name_prefix
        if use_embedded:
            template_name = "{}_embedded.html".format(template_name_prefix[:-5])
    else:
        template_name = "{}.html".format(template_name_prefix)
        if use_embedded:
            template_name = "{}_embedded.html".format(template_name_prefix)

    if obj:
        template_list.append(
            "{}/{}/{}".format(obj._meta.app_label, app_dir, template_name)
        )

    template_list.append("{}/{}".format(app_dir, template_name))

    return template_list


def select_template_for_object(template_name_prefix, obj, app_dir, use_embedded=False):
    """
    tries to get a template from some object-template dir.
    If this one does not exist, return a default template.

    :param template_name_prefix: template file name with or without extension
    :param obj: object to which the template is related to
    :param app_dir: template (sub)directory to search for the template file
    :param use_embedded: suffix with "_embedded" or not?
    :return: template object

    For example,
    select_template_for_object("post_list.html", person, "blog", use_embedded=False)
    would return a template loaded from "people/blog/post_list.html"

    select_template_for_object("post_details", person, "blog", use_embedded=True)
    would return a template loaded from "people/blog/post_details_embedded.html"
    """
    template_list = get_template_name_list_for_object(
        template_name_prefix, obj, app_dir, use_embedded
    )
    template = django_select_template(template_list)
    return template
