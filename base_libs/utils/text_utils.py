try:
    from django.utils.translation import string_concat  # up to django 2.0
except ImportError:
    from django.utils.encoding import force_text
    from django.utils.functional import lazy

    @lazy
    def string_concat(*strings):  # backport for django 2.1 and greater
        """
        Lazy variant of string concatenation, needed for translations that are
        constructed from multiple parts.
        """
        return "".join(force_text(s) for s in strings)
