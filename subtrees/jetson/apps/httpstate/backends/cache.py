from django.core.cache import cache
from jetson.apps.httpstate.backends.base import HttpStateBase, CreateError

KEY_PREFIX = "jetson.apps.httpstate.cache"

class HttpStateStore(HttpStateBase):
    """
    A cache-based httpstate store.
    """

    @classmethod
    def clear_expired(cls):
        pass

    def __init__(self, httpstate_key=None):
        self._cache = cache
        super(HttpStateStore, self).__init__(httpstate_key)

    def load(self):
        httpstate_data = self._cache.get(KEY_PREFIX + self.httpstate_key)
        if httpstate_data is not None:
            return httpstate_data
        self.create()
        return {}

    def create(self):
        # Because a cache can fail silently (e.g. memcache), we don't know if
        # we are failing to create a new httpstate because of a key collision or
        # because the cache is missing. So we try for a (large) number of times
        # and then raise an exception. That's the risk you shoulder if using
        # cache backing.
        for i in xrange(10000):
            self.httpstate_key = self._get_new_httpstate_key()
            try:
                self.save(must_create=True)
            except CreateError:
                continue
            self.modified = True
            return
        raise RuntimeError("Unable to create a new httpstate key.")

    def save(self, must_create=False):
        if must_create:
            func = self._cache.add
        else:
            func = self._cache.set
        result = func(KEY_PREFIX + self.httpstate_key, self._get_httpstate(no_load=must_create),
                self.get_expiry_age())
        if must_create and not result:
            raise CreateError

    def exists(self, httpstate_key):
        if self._cache.get(KEY_PREFIX + httpstate_key):
            return True
        return False

    def delete(self, httpstate_key=None):
        if httpstate_key is None:
            if self._httpstate_key is None:
                return
            httpstate_key = self._httpstate_key
        self._cache.delete(KEY_PREFIX + httpstate_key)

