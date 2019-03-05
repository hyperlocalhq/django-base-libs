"""
Cached, database-backed httpstates.
"""

from django.conf import settings
from django.core.cache import cache
from jetson.apps.httpstate.backends.db import HttpStateStore as DBStore
from jetson.apps.httpstate import settings as httpstate_settings

KEY_PREFIX = "jetson.apps.httpstate.cached_db"


class HttpStateStore(DBStore):
    """
    Implements cached, database backed httpstates.
    """

    def __init__(self, httpstate_key=None):
        super(HttpStateStore, self).__init__(httpstate_key)

    def load(self):
        data = cache.get(KEY_PREFIX + self.httpstate_key, None)
        if data is None:
            data = super(HttpStateStore, self).load()
            cache.set(
                KEY_PREFIX + self.httpstate_key, data,
                httpstate_settings.HTTPSTATE_COOKIE_AGE
            )
        return data

    def exists(self, httpstate_key):
        return super(HttpStateStore, self).exists(httpstate_key)

    def save(self, must_create=False):
        super(HttpStateStore, self).save(must_create)
        cache.set(
            KEY_PREFIX + self.httpstate_key, self._httpstate,
            httpstate_settings.HTTPSTATE_COOKIE_AGE
        )

    def delete(self, httpstate_key=None):
        super(HttpStateStore, self).delete(httpstate_key)
        cache.delete(KEY_PREFIX + (httpstate_key or self.httpstate_key))

    def flush(self):
        """
        Removes the current httpstate data from the database and regenerates the
        key.
        """
        self.clear()
        self.delete(self.httpstate_key)
        self.create()
