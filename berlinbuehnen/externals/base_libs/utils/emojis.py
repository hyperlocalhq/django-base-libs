# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import re

try:
    # UCS-4
    emoji_pattern = re.compile(u'[\U00010000-\U0010ffff]', flags=re.UNICODE | re.MULTILINE)
except re.error:
    # UCS-2
    emoji_pattern = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]', flags=re.UNICODE | re.MULTILINE)


def _replace_with_html_entity(match):
    # from something like "u'\U0001f60e'" get only "0001f60"
    symbols = match.group(0)
    return u'&#x{};'.format(repr(symbols)[4:-1])


def emojis_to_html_entities(html):
    # replace emojis and other 4-byte unicode characters with html entities
    result = re.sub(emoji_pattern, _replace_with_html_entity, html)
    return result


def strip_emojis(text):
    # strip emojis and other 4-byte unicode characters
    result = re.sub(emoji_pattern, u"", text)
    return result


if __name__ == "__main__":
    s = u"How 😎 is that, Mr. Müller?"
    r1 = emojis_to_html_entities(s)
    print(r1)
    assert(r1 == u"How &#x0001f60e; is that, Mr. Müller?")

    r2 = strip_emojis(s)
    print(r2)
    assert(r2 == u"How  is that, Mr. Müller?")
