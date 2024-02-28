import unicodedata

from django.core.files.storage import FileSystemStorage
from django.utils.encoding import force_str


class ASCIIFileSystemStorage(FileSystemStorage):
    """
    Convert unicode characters in name to ASCII characters.
    """

    def get_valid_name(self, name):
        normalized_name = force_str(
            unicodedata.normalize("NFKD", name).encode("ascii", "ignore")
        )
        return super(ASCIIFileSystemStorage, self).get_valid_name(normalized_name)
