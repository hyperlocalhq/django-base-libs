# -*- coding: UTF-8 -*-
import base64

from django.conf import settings
try:
    from django.utils.encoding import force_text, force_bytes
except ImportError:
    from django.utils.encoding import force_unicode as force_text, smart_str as force_bytes

from pyDes import des, CBC as des_CBC


def cryptString(plain):
    plain = force_bytes(plain)
    padded_length = len(plain) + 8 - len(plain) % 8
    plain = plain.ljust(padded_length, "\0")
    k = des(force_bytes(settings.SECRET_KEY[:8]), des_CBC, "\0\0\0\0\0\0\0\0")
    return base64.b64encode(k.encrypt(plain), "_-").strip()


def decryptString(cipher):
    k = des(force_bytes(settings.SECRET_KEY[:8]), des_CBC, "\0\0\0\0\0\0\0\0")
    plain = k.decrypt(base64.b64decode(force_bytes(cipher), "_-")).replace("\0", "")
    plain = force_text(plain)
    return plain
