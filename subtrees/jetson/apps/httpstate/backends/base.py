from __future__ import unicode_literals

import base64
from datetime import datetime, timedelta
import string

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.utils.crypto import constant_time_compare
from django.utils.crypto import get_random_string
from django.utils.crypto import salted_hmac
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.module_loading import import_by_path

try:
    from django.utils.timezone import now as tz_now
except:
    tz_now = datetime.now

from jetson.apps.httpstate import settings as httpstate_settings

# httpstate_key should not be case sensitive because some backends can store it
# on case insensitive file systems.
VALID_KEY_CHARS = string.ascii_lowercase + string.digits


class CreateError(Exception):
    """
    Used internally as a consistent exception type to catch from save (see the
    docstring for HttpStateBase.save() for details).
    """
    pass


class HttpStateBase(object):
    """
    Base class for all HttpState classes.
    """
    TEST_COOKIE_NAME = 'testcookie'
    TEST_COOKIE_VALUE = 'worked'

    def __init__(self, httpstate_key=None):
        self._httpstate_key = httpstate_key
        self.accessed = False
        self.modified = False
        self.serializer = import_by_path(
            httpstate_settings.HTTPSTATE_SERIALIZER
        )

    def __contains__(self, key):
        return key in self._httpstate

    def __getitem__(self, key):
        return self._httpstate[key]

    def __setitem__(self, key, value):
        self._httpstate[key] = value
        self.modified = True

    def __delitem__(self, key):
        del self._httpstate[key]
        self.modified = True

    def get(self, key, default=None):
        return self._httpstate.get(key, default)

    def pop(self, key, *args):
        self.modified = self.modified or key in self._httpstate
        return self._httpstate.pop(key, *args)

    def setdefault(self, key, value):
        if key in self._httpstate:
            return self._httpstate[key]
        else:
            self.modified = True
            self._httpstate[key] = value
            return value

    def set_test_cookie(self):
        self[self.TEST_COOKIE_NAME] = self.TEST_COOKIE_VALUE

    def test_cookie_worked(self):
        return self.get(self.TEST_COOKIE_NAME) == self.TEST_COOKIE_VALUE

    def delete_test_cookie(self):
        del self[self.TEST_COOKIE_NAME]

    def _hash(self, value):
        key_salt = "jetson.apps.httpstate" + self.__class__.__name__
        return salted_hmac(key_salt, value).hexdigest()

    def encode(self, httpstate_dict):
        """Returns the given httpstate dictionary serialized and encoded as a string."""
        serialized = self.serializer().dumps(httpstate_dict)
        hash = self._hash(serialized)
        return base64.b64encode(hash.encode() + b":" +
                                serialized).decode('ascii')

    def decode(self, httpstate_data):
        encoded_data = base64.b64decode(force_bytes(httpstate_data))
        try:
            # could produce ValueError if there is no ':'
            hash, serialized = encoded_data.split(b':', 1)
            expected_hash = self._hash(serialized)
            if not constant_time_compare(hash.decode(), expected_hash):
                raise SuspiciousOperation("HttpState data corrupted")
            else:
                return self.serializer().loads(serialized)
        except Exception:
            # ValueError, SuspiciousOperation, deserialization exceptions. If
            # any of these happen, just return an empty dictionary (an empty
            # httpstate).
            return {}

    def update(self, dict_):
        self._httpstate.update(dict_)
        self.modified = True

    def has_key(self, key):
        return key in self._httpstate

    def keys(self):
        return self._httpstate.keys()

    def values(self):
        return self._httpstate.values()

    def items(self):
        return self._httpstate.items()

    def iterkeys(self):
        return self._httpstate.iterkeys()

    def itervalues(self):
        return self._httpstate.itervalues()

    def iteritems(self):
        return self._httpstate.iteritems()

    def clear(self):
        # To avoid unnecessary persistent storage accesses, we set up the
        # internals directly (loading data wastes time, since we are going to
        # set it to an empty dict anyway).
        self._httpstate_cache = {}
        self.accessed = True
        self.modified = True

    def _get_new_httpstate_key(self):
        """Returns httpstate key that isn't being used."""
        httpstate_key = None
        while True:
            httpstate_key = get_random_string(32, VALID_KEY_CHARS)
            if not self.exists(httpstate_key):
                break
        return httpstate_key

    def _get_or_create_httpstate_key(self):
        if self._httpstate_key is None:
            self._httpstate_key = self._get_new_httpstate_key()
        return self._httpstate_key

    def _get_httpstate_key(self):
        return self._httpstate_key

    httpstate_key = property(_get_httpstate_key)

    def _get_httpstate(self, no_load=False):
        """
        Lazily loads httpstate from storage (unless "no_load" is True, when only
        an empty dict is stored) and stores it in the current instance.
        """
        self.accessed = True
        try:
            return self._httpstate_cache
        except AttributeError:
            if self.httpstate_key is None or no_load:
                self._httpstate_cache = {}
            else:
                self._httpstate_cache = self.load()
        return self._httpstate_cache

    _httpstate = property(_get_httpstate)

    def get_expiry_age(self, **kwargs):
        """Get the number of seconds until the httpstate expires.

        Optionally, this function accepts `modification` and `expiry` keyword
        arguments specifying the modification and expiry of the httpstate.
        """
        try:
            modification = kwargs['modification']
        except KeyError:
            modification = timezone.now()
        # Make the difference between "expiry=None passed in kwargs" and
        # "expiry not passed in kwargs", in order to guarantee not to trigger
        # self.load() when expiry is provided.
        try:
            expiry = kwargs['expiry']
        except KeyError:
            expiry = self.get('_httpstate_expiry')

        if not expiry:  # Checks both None and 0 cases
            return httpstate_settings.HTTPSTATE_COOKIE_AGE
        if not isinstance(expiry, datetime):
            return expiry
        delta = expiry - modification
        return delta.days * 86400 + delta.seconds

    def get_expiry_date(self, **kwargs):
        """Get httpstate the expiry date (as a datetime object).

        Optionally, this function accepts `modification` and `expiry` keyword
        arguments specifying the modification and expiry of the httpstate.
        """
        try:
            modification = kwargs['modification']
        except KeyError:
            modification = timezone.now()
        # Same comment as in get_expiry_age
        try:
            expiry = kwargs['expiry']
        except KeyError:
            expiry = self.get('_httpstate_expiry')

        if isinstance(expiry, datetime):
            return expiry
        if not expiry:  # Checks both None and 0 cases
            expiry = httpstate_settings.HTTPSTATE_COOKIE_AGE
        return modification + timedelta(seconds=expiry)

    def set_expiry(self, value):
        """
        Sets a custom expiration for the httpstate. ``value`` can be an integer,
        a Python ``datetime`` or ``timedelta`` object or ``None``.

        If ``value`` is an integer, the httpstate will expire after that many
        seconds of inactivity. If set to ``0`` then the httpstate will expire on
        browser close.

        If ``value`` is a ``datetime`` or ``timedelta`` object, the httpstate
        will expire at that specific future time.

        If ``value`` is ``None``, the httpstate uses the global httpstate expiry
        policy.
        """
        if value is None:
            # Remove any custom expiration for this httpstate.
            try:
                del self['_httpstate_expiry']
            except KeyError:
                pass
            return
        if isinstance(value, timedelta):
            value = timezone.now() + value
        self['_httpstate_expiry'] = value

    def get_expire_at_browser_close(self):
        """
        Returns ``True`` if the httpstate is set to expire when the browser
        closes, and ``False`` if there's an expiry date. Use
        ``get_expiry_date()`` or ``get_expiry_age()`` to find the actual expiry
        date/age, if there is one.
        """
        if self.get('_httpstate_expiry') is None:
            return httpstate_settings.HTTPSTATE_EXPIRE_AT_BROWSER_CLOSE
        return self.get('_httpstate_expiry') == 0

    def flush(self):
        """
        Removes the current httpstate data from the database and regenerates the
        key.
        """
        self.clear()
        self.delete()
        self.create()

    def cycle_key(self):
        """
        Creates a new httpstate key, whilst retaining the current httpstate data.
        """
        data = self._httpstate_cache
        key = self.httpstate_key
        self.create()
        self._httpstate_cache = data
        self.delete(key)

    # Methods that child classes must implement.

    def exists(self, httpstate_key):
        """
        Returns True if the given httpstate_key already exists.
        """
        raise NotImplementedError

    def create(self):
        """
        Creates a new httpstate instance. Guaranteed to create a new object with
        a unique key and will have saved the result once (with empty data)
        before the method returns.
        """
        raise NotImplementedError

    def save(self, must_create=False):
        """
        Saves the httpstate data. If 'must_create' is True, a new httpstate object
        is created (otherwise a CreateError exception is raised). Otherwise,
        save() can update an existing object with the same key.
        """
        raise NotImplementedError

    def delete(self, httpstate_key=None):
        """
        Deletes the httpstate data under this key. If the key is None, the
        current httpstate key value is used.
        """
        raise NotImplementedError

    def load(self):
        """
        Loads the httpstate data and returns a dictionary.
        """
        raise NotImplementedError

    @classmethod
    def clear_expired(cls):
        """
        Remove expired httpstates from the httpstate store.

        If this operation isn't possible on a given backend, it should raise
        NotImplementedError. If it isn't necessary, because the backend has
        a built-in expiration mechanism, it should be a no-op.
        """
        raise NotImplementedError
