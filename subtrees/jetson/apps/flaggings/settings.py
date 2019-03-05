# -*- coding: UTF-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

FLAG_COLOR_CHOICES = getattr(
    settings,
    "FLAGGINGS_FLAG_COLOR_CHOICES",
    [
        (1, _("red")),
        (2, _("orange")),
        (3, _("yellow")),
        (4, _("green")),
        (5, _("blue")),
        (6, _("magenta")),
        (7, _("gray")),
    ],
)
