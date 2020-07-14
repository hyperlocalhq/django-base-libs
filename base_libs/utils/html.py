# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import re

try:
    from html.entities import name2codepoint  # Python 3
except ImportError:
    from htmlentitydefs import name2codepoint  # Python 2

try:
    from django.utils.encoding import force_text
except:
    from django.utils.encoding import force_unicode as force_text

entity_re = re.compile("&(#?)([Xx]?)(\d+|[A-Fa-f0-9]+|%s);" % "|".join(name2codepoint))

entity_no_escape_chars_re = re.compile(
    r"&(#?)([Xx]?)((?!39;)(\d+|[A-Fa-f0-9]+)|%s);"
    % "|".join([k for k in name2codepoint if k not in ("amp", "lt", "gt", "quot")])
)


def decode_entities(html, decode_all=False):
    """
    Replaces HTML entities with unicode equivalents.
    Ampersands, quotes and carets are not replaced by default.
    """

    def _replace_entity(m):
        entity = m.group(3)
        if m.group(1) == "#":
            val = int(entity, m.group(2) == "" and 10 or 16)
        else:
            val = name2codepoint[entity]
        return unichr(val)

    regexp = decode_all and entity_re or entity_no_escape_chars_re
    return regexp.sub(_replace_entity, force_text(html))
