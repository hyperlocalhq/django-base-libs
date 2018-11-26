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

# execute guerrilla patches
patches_dir = os.path.join(os.path.dirname(__file__), "guerrilla_patches")
for filename in os.listdir(patches_dir):
    if os.path.splitext(filename)[1] == ".py":
        execfile(os.path.join(patches_dir, filename))
