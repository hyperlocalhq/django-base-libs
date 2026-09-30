import re

from django.db import models


def strip_whitespaces_from_charfields(sender, instance, *args, **kwargs):
    """ Strips leading and trailing whitespace characters from all CharField values """
    regex = re.compile(r"^\s*(.+?)\s*$")
    for f in sender._meta.fields:
        if isinstance(f, models.CharField):
            val = getattr(instance, f.name, None)
            if isinstance(val, str):
                stripped = regex.sub(r"\1", val)
                # Only assign when something changes: some fields refuse
                # direct assignment (e.g. django-fsm's protected FSMField
                # used by djangocms-versioning's Version.state).
                if stripped != val:
                    setattr(instance, f.name, stripped)
