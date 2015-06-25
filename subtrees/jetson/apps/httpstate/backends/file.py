import errno
import os
import tempfile

from django.conf import settings
from django.core.exceptions import SuspiciousOperation, ImproperlyConfigured

from jetson.apps.httpstate.backends.base import HttpStateBase, CreateError
from jetson.apps.httpstate import settings as httpstate_settings

class HttpStateStore(HttpStateBase):
    """
    Implements a file based httpstate store.
    """

    @classmethod
    def clear_expired(cls):
        pass

    def __init__(self, httpstate_key=None):
        self.storage_path = httpstate_settings.HTTPSTATE_FILE_PATH
        if not self.storage_path:
            self.storage_path = tempfile.gettempdir()

        # Make sure the storage path is valid.
        if not os.path.isdir(self.storage_path):
            raise ImproperlyConfigured(
                "The httpstate storage path %r doesn't exist. Please set your"
                " HTTPSTATE_FILE_PATH setting to an existing directory in which"
                " Django can store httpstate data." % self.storage_path)

        self.file_prefix = httpstate_settings.HTTPSTATE_COOKIE_NAME
        super(HttpStateStore, self).__init__(httpstate_key)

    VALID_KEY_CHARS = set("abcdef0123456789")

    def _key_to_file(self, httpstate_key=None):
        """
        Get the file associated with this httpstate key.
        """
        if httpstate_key is None:
            httpstate_key = self.httpstate_key

        # Make sure we're not vulnerable to directory traversal. HttpState keys
        # should always be md5s, so they should never contain directory
        # components.
        if not set(httpstate_key).issubset(self.VALID_KEY_CHARS):
            raise SuspiciousOperation(
                "Invalid characters in session key")        

        return os.path.join(self.storage_path, self.file_prefix + httpstate_key)

    def load(self):
        httpstate_data = {}
        try:
            httpstate_file = open(self._key_to_file(), "rb")
            try:
                file_data = httpstate_file.read()
                # Don't fail if there is no data in the httpstate file.
                # We may have opened the empty placeholder file.
                if file_data:
                    try:
                        httpstate_data = self.decode(file_data)
                    except (EOFError, SuspiciousOperation):
                        self.create()
            finally:
                httpstate_file.close()
        except IOError:
            self.create()
        return httpstate_data

    def create(self):
        while True:
            self._httpstate_key = self._get_new_httpstate_key()
            try:
                self.save(must_create=True)
            except CreateError:
                continue
            self.modified = True
            self._httpstate_cache = {}
            return

    def save(self, must_create=False):
        # Get the httpstate data now, before we start messing
        # with the file it is stored within.
        httpstate_data = self._get_httpstate(no_load=must_create)

        httpstate_file_name = self._key_to_file()

        try:
            # Make sure the file exists.  If it does not already exist, an
            # empty placeholder file is created.
            flags = os.O_WRONLY | os.O_CREAT | getattr(os, 'O_BINARY', 0)
            if must_create:
                flags |= os.O_EXCL
            fd = os.open(httpstate_file_name, flags)
            os.close(fd)

        except OSError, e:
            if must_create and e.errno == errno.EEXIST:
                raise CreateError
            raise

        # Write the httpstate file without interfering with other threads
        # or processes.  By writing to an atomically generated temporary
        # file and then using the atomic os.rename() to make the complete
        # file visible, we avoid having to lock the httpstate file, while
        # still maintaining its integrity.
        #
        # Note: Locking the httpstate file was explored, but rejected in part
        # because in order to be atomic and cross-platform, it required a
        # long-lived lock file for each httpstate, doubling the number of
        # files in the httpstate storage directory at any given time.  This
        # rename solution is cleaner and avoids any additional overhead
        # when reading the httpstate data, which is the more common case
        # unless HTTPSTATE_SAVE_EVERY_REQUEST = True.
        #
        # See ticket #8616.
        dir, prefix = os.path.split(httpstate_file_name)

        try:
            output_file_fd, output_file_name = tempfile.mkstemp(dir=dir,
                prefix=prefix + '_out_')
            renamed = False
            try:
                try:
                    os.write(output_file_fd, self.encode(httpstate_data))
                finally:
                    os.close(output_file_fd)
                os.rename(output_file_name, httpstate_file_name)
                renamed = True
            finally:
                if not renamed:
                    os.unlink(output_file_name)

        except (OSError, IOError, EOFError):
            pass

    def exists(self, httpstate_key):
        if os.path.exists(self._key_to_file(httpstate_key)):
            return True
        return False

    def delete(self, httpstate_key=None):
        if httpstate_key is None:
            if self._httpstate_key is None:
                return
            httpstate_key = self._httpstate_key
        try:
            os.unlink(self._key_to_file(httpstate_key))
        except OSError:
            pass

    def clean(self):
        pass
