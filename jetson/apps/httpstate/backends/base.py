import base64
import os
import random
import sys
import time
from datetime import datetime, timedelta
try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from hashlib import md5

from jetson.apps.httpstate import settings as httpstate_settings

# Use the system (hardware-based) random number generator if it exists.
if hasattr(random, 'SystemRandom'):
    randrange = random.SystemRandom().randrange
else:
    randrange = random.randrange
MAX_HTTPSTATE_KEY = 18446744073709551616L     # 2 << 63

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

    def keys(self):
        return self._httpstate.keys()

    def items(self):
        return self._httpstate.items()

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

    def encode(self, httpstate_dict):
        "Returns the given httpstate dictionary pickled and encoded as a string."
        pickled = pickle.dumps(httpstate_dict, pickle.HIGHEST_PROTOCOL)
        pickled_md5 = md5(pickled + settings.SECRET_KEY).hexdigest()
        return base64.encodestring(pickled + pickled_md5)

    def decode(self, httpstate_data):
        encoded_data = base64.decodestring(httpstate_data)
        pickled, tamper_check = encoded_data[:-32], encoded_data[-32:]
        if md5(pickled + settings.SECRET_KEY).hexdigest() != tamper_check:
            raise SuspiciousOperation("User tampered with httpstate cookie.")
        try:
            return pickle.loads(pickled)
        # Unpickling can cause a variety of exceptions. If something happens,
        # just return an empty dictionary (an empty httpstate).
        except:
            return {}

    def update(self, dict_):
        self._httpstate.update(dict_)
        self.modified = True

    def has_key(self, key):
        return self._httpstate.has_key(key)

    def values(self):
        return self._httpstate.values()

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
        "Returns httpstate key that isn't being used."
        # The random module is seeded when this Apache child is created.
        # Use settings.SECRET_KEY as added salt.
        try:
            pid = os.getpid()
        except AttributeError:
            # No getpid() in Jython, for example
            pid = 1
        while 1:
            httpstate_key = md5("%s%s%s%s"
                    % (randrange(0, MAX_HTTPSTATE_KEY), pid, time.time(),
                       settings.SECRET_KEY)).hexdigest()
            if not self.exists(httpstate_key):
                break
        return httpstate_key

    def _get_httpstate_key(self):
        if self._httpstate_key:
            return self._httpstate_key
        else:
            self._httpstate_key = self._get_new_httpstate_key()
            return self._httpstate_key

    def _set_httpstate_key(self, httpstate_key):
        self._httpstate_key = httpstate_key

    httpstate_key = property(_get_httpstate_key, _set_httpstate_key)

    def _get_httpstate(self, no_load=False):
        """
        Lazily loads httpstate from storage (unless "no_load" is True, when only
        an empty dict is stored) and stores it in the current instance.
        """
        self.accessed = True
        try:
            return self._httpstate_cache
        except AttributeError:
            if self._httpstate_key is None or no_load:
                self._httpstate_cache = {}
            else:
                self._httpstate_cache = self.load()
        return self._httpstate_cache

    _httpstate = property(_get_httpstate)

    def get_expiry_age(self):
        """Get the number of seconds until the httpstate expires."""
        expiry = self.get('_httpstate_expiry')
        if not expiry:   # Checks both None and 0 cases
            return httpstate_settings.HTTPSTATE_COOKIE_AGE
        if not isinstance(expiry, datetime):
            return expiry
        delta = expiry - datetime.now()
        return delta.days * 86400 + delta.seconds

    def get_expiry_date(self):
        """Get httpstate the expiry date (as a datetime object)."""
        expiry = self.get('_httpstate_expiry')
        if isinstance(expiry, datetime):
            return expiry
        if not expiry:   # Checks both None and 0 cases
            expiry = httpstate_settings.HTTPSTATE_COOKIE_AGE
        return datetime.now() + timedelta(seconds=expiry)

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
            value = datetime.now() + value
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
