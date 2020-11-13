# -*- coding: UTF-8 -*-
import unicodedata

from django.core.files.storage import FileSystemStorage

try:
    from django.utils.encoding import force_text
except ImportError:
    force_text = str


class ASCIIFileSystemStorage(FileSystemStorage):
    """
    Convert unicode characters in name to ASCII characters.
    """

    def get_valid_name(self, name):
        normalized_name = force_text(
            unicodedata.normalize("NFKD", name).encode("ascii", "ignore")
        )
        return super(ASCIIFileSystemStorage, self).get_valid_name(normalized_name)
