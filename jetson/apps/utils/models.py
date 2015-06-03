# -*- coding: UTF-8 -*-
import os

from django.db import models
from django.db.models import signals
from django.utils.encoding import force_unicode, smart_unicode, smart_str
from django.conf import settings
from django.dispatch import Signal
from django.utils.translation import ugettext, get_language, activate
from django.utils.translation import ugettext_lazy as _
from django.utils.text import get_text_list
from django.contrib.auth.models import User

from base_libs.middleware import get_current_language
from base_libs.utils.misc import get_translation

'''
ACTION_CHOICES = (
    (settings.A_UNDEFINED, _("Undefined")),
    (settings.A_ADDITION, _("Add")),
    (settings.A_READ, _("Read")),
    (settings.A_CHANGE, _("Change")),
    (settings.A_DELETION, _("Delete")),
    (settings.A_CUSTOM1, _("Custom #1")),
    (settings.A_CUSTOM2, _("Custom #2")),
    (settings.A_CUSTOM3, _("Custom #3")),
)

SCOPE_CHOICES = (
    (settings.AS_SYSTEM, _("System")),
    (settings.AS_PRIVATE, _("Private")),
    (settings.AS_PUBLIC, _("Public")),
)
'''
MONTH_CHOICES = (
    (1, _("January")),
    (2, _("February")),
    (3, _("March")),
    (4, _("April")),
    (5, _("May")),
    (6, _("June")),
    (7, _("July")),
    (8, _("August")),
    (9, _("September")),
    (10, _("October")),
    (11, _("November")),
    (12, _("December")),
)

class XFieldList(list):
    """ List for field names.
    Changes "*_" to translations of the current language,
    i.e.
    "sort_order" => "sort_order"
    "title_" => "title", "title_de", or "title_es"
    "__str__" => "__str__"
    """
    def __init__(self, sequence=[]):
        self.sequence = sequence
    def __iter__(self):
        return iter(self._get_list())
    def __getitem__(self, k):
        return self._get_list()[k]
    def __nonzero__(self):
        return bool(self.sequence)
    def __len__(self):
        return len(self.sequence)
    def __str__(self):
        return str(self._get_list())
    def __unicode__(self):
        return unicode(self._get_list())
    def __repr__(self):
        return repr(self._get_list())
    def _get_list(self):
        language = get_current_language()
        result = []
        for item in self.sequence:
            if item[:1]=="-":
                order = "-"
                item = item[1:]
            else:
                order = ""
            if item[:2] == "__" or item[-1:] != "_":
                result.append(order + item)
            else:
                if language == "en":
                    result.append(order + item[:-1])
                else:
                    result.append(order + item + language)
        return result

# execute guerrilla patches
patches_dir = os.path.join(os.path.dirname(__file__), "guerrilla_patches")
for filename in os.listdir(patches_dir):
    if os.path.splitext(filename)[1] == ".py":
        execfile(os.path.join(patches_dir, filename))

