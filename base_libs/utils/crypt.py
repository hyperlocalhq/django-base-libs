# -*- coding: UTF-8 -*-
import base64

from Crypto.Cipher import DES
from django.utils.encoding import force_unicode, smart_str

def cryptString(plain, key=''):
    '''
    >>> decryptString(cryptString('the quick brown fox jumps over the lazy dog.', 'abcdefgh'), 'abcdefgh')
    u'the quick brown fox jumps over the lazy dog.'

    >>> decryptString(cryptString('', 'abcdefgh'), 'abcdefgh')
    u''

    >>> decryptString(cryptString(u'ãêç', 'abcdefgh'), 'abcdefgh')
    u'ãêç'
    '''
    plain = smart_str(plain)
    padded_length = len(plain)+8 - len(plain)%8
    plain = plain.ljust(padded_length,"\0")
    if not key:
        from django.conf import settings
        key = settings.SECRET_KEY[:8]
    k = DES.new(key, DES.MODE_CFB, "\0\0\0\0\0\0\0\0")
    cipher = k.encrypt(plain)
    base64_cipher = base64.b64encode(cipher, "_-").strip()
    return base64_cipher

def decryptString(cipher, key=''):
    if not key:
        from django.conf import settings
        key = settings.SECRET_KEY[:8]
    k = DES.new(key, DES.MODE_CFB, "\0\0\0\0\0\0\0\0")
    plain = k.decrypt(base64.b64decode(smart_str(cipher), "_-")).replace("\0", "")
    plain = force_unicode(plain)
    return plain

if __name__ == "__main__":
    import doctest
    doctest.testmod()
