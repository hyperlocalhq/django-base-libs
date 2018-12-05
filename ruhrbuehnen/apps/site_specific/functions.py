# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import re


def remove_copyright_label(text):
    # remove copyright symbol (©, (c), or c) and surrounding whitespace characters
    text = re.sub(r'^c\s+', '', text, flags=re.I)
    text = re.sub(r'\s*(\(c\)|\xa9)\s*', '', text, flags=re.I)
    # remove "copyright" word and surrounding punctuation characters
    text = re.sub(r'\W*copyright\W*', '', text, flags=re.I)
    return text
