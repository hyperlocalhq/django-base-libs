# -*- coding: UTF-8 -*-
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

PRIORITY_CHOICES = getattr(
    settings,
    "PRIORITIES_PRIORITY_CHOICES",
    [
        (1, _("very high")),
        (2, _("high")),
        (3, _("normal")),
        (4, _("low")),
        (5, _("very low")),
    ],
)
