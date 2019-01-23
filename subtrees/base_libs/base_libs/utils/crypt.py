# -*- coding: UTF-8 -*-
from pyDes import des, CBC as des_CBC
from django.utils.encoding import force_unicode, smart_str
from django.conf import settings
import base64

def cryptString(plain):
    plain = smart_str(plain)
    padded_length = len(plain)+8 - len(plain)%8
    plain = plain.ljust(padded_length,"\0")
    k = des(smart_str(settings.SECRET_KEY[:8]), des_CBC, "\0\0\0\0\0\0\0\0")
    return base64.b64encode(k.encrypt(plain), "_-").strip()    

def decryptString(cipher):
    k = des(smart_str(settings.SECRET_KEY[:8]), des_CBC, "\0\0\0\0\0\0\0\0")
    plain = k.decrypt(base64.b64decode(smart_str(cipher), "_-")).replace("\0", "")
    plain = force_unicode(plain)
    return plain