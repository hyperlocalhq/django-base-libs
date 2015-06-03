# -*- coding: UTF-8 -*-

import re

from django.db import models

def strip_whitespaces_from_charfields(sender, instance, *args, **kwargs):
    """ Strips leading and trailing whitespace characters from all CharField values """
    regex = re.compile(r'^\s*(.+?)\s*$')
    for f in sender._meta.fields:
        if isinstance(f, models.CharField):
            val = getattr(instance, f.name, None)
            if isinstance(val, basestring):
                setattr(instance, f.name, regex.sub(r"\1", val))
