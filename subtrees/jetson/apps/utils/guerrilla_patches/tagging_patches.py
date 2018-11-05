# -*- coding: UTF-8 -*-
from __future__ import unicode_literals


def patch_tagging():
    ### Allow multi-word tags, always separate by comma ###
    from django.conf import settings

    if "tagging" in settings.INSTALLED_APPS:

        from tagging.utils import edit_string_for_tags

        def _edit_string_for_tags(tags):
            """
            Given list of ``Tag`` instances, creates a string representation of
            the list suitable for editing by the user, such that submitting the
            given string representation back without changing it will give the
            same list of tags.

            Tag names which contain commas will be double quoted.

            The resulting string of tag names will be comma-delimited.
            """
            names = []
            for tag in tags:
                name = getattr(tag, 'name', tag)
                if u',' in name:
                    names.append('"%s"' % name)
                    continue
                names.append(name)
            glue = u', '
            output = glue.join(names)
            if output:
                output += ", "
            return output

        edit_string_for_tags.func_code = _edit_string_for_tags.func_code

    if "tagging_autocomplete" in settings.INSTALLED_APPS:

        ### don't include jquery again ###

        from tagging_autocomplete.widgets import TagAutocomplete

        _js_base_url = getattr(settings, 'TAGGING_AUTOCOMPLETE_JS_BASE_URL','%s/jquery-autocomplete' % settings.MEDIA_URL)
        TagAutocomplete.Media.js = (
            '%s/jquery.bgiframe.min.js' % _js_base_url,
            '%s/jquery.autocomplete.js' % _js_base_url,
            )


patch_tagging()