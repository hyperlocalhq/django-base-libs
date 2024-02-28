import base64

from django.conf import settings
from django.utils.encoding import force_str, force_bytes

from pyDes import des, CBC as des_CBC


def cryptString(plain):
    plain = force_bytes(plain)
    padded_length = len(plain) + 8 - len(plain) % 8
    plain = plain.ljust(padded_length, force_bytes("\0"))
    k = des(
        force_bytes(settings.SECRET_KEY[:8]), des_CBC, force_bytes("\0\0\0\0\0\0\0\0")
    )
    return base64.b64encode(k.encrypt(plain), force_bytes("_-")).strip()


def decryptString(cipher):
    cipher = force_bytes(cipher)
    k = des(
        force_bytes(settings.SECRET_KEY[:8]), des_CBC, force_bytes("\0\0\0\0\0\0\0\0")
    )
    plain = k.decrypt(base64.b64decode(force_bytes(cipher), force_bytes("_-"))).replace(
        force_bytes("\0"), force_bytes("")
    )
    plain = force_str(plain)
    return plain
