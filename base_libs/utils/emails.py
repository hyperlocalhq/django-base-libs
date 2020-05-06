# -*- coding: UTF-8 -*-

import re

email_pat = re.compile(
    "^([a-zA-Z0-9_\.\-])+@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$", re.I
)


def is_valid_email(addr):
    return email_pat.match(addr) is not None


def get_email_and_name(recipient):
    regex = re.match("(.*?)([<(].*?[>)])", recipient)
    if not regex:
        name = None
        email = recipient
    else:
        name = regex.group(1)
        email = regex.group(2)
    email = re.sub("[<>()]", "", email)
    if name:
        name = name.strip()
    if email:
        email = email.strip()
    return email, name
