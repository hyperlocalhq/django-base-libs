# -*- coding: UTF-8 -*-


def force_bytes(s, encoding="utf-8", strings_only=False, errors="strict"):
    """
    Similar to smart_bytes, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if isinstance(s, str):
        if encoding == "utf-8":
            return s
        else:
            return s.decode("utf-8", errors).encode(encoding, errors)
    if strings_only and (s is None or isinstance(s, int)):
        return s
    if not isinstance(s, unicode):
        try:
            return bytes(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return " ".join(
                    [force_bytes(arg, encoding, strings_only, errors) for arg in s]
                )
            return s.encode(encoding, errors)
    else:
        return s.encode(encoding, errors)


force_str = force_bytes
# backwards compatibility for Python 2

force_str.__doc__ = """\
Apply force_text in Python 3 and force_bytes in Python 2.
"""
