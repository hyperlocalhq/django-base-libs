r"""

>>> from django.conf import settings
>>> from jetson.apps.httpstate.backends.db import HttpStateStore as DatabaseHttpState
>>> from jetson.apps.httpstate.backends.cache import HttpStateStore as CacheHttpState
>>> from jetson.apps.httpstate.backends.cached_db import HttpStateStore as CacheDBHttpState
>>> from jetson.apps.httpstate.backends.file import HttpStateStore as FileHttpState
>>> from jetson.apps.httpstate.backends.base import HttpStateBase
>>> from jetson.apps.httpstate.models import HttpState
>>> from jetson.apps.httpstate import settings as httpstate_settings
>>> db_httpstate = DatabaseHttpState()
>>> db_httpstate.modified
False
>>> db_httpstate.get('cat')
>>> db_httpstate['cat'] = "dog"
>>> db_httpstate.modified
True
>>> db_httpstate.pop('cat')
'dog'
>>> db_httpstate.pop('some key', 'does not exist')
'does not exist'
>>> db_httpstate.save()
>>> db_httpstate.exists(db_httpstate.httpstate_key)
True
>>> db_httpstate.delete(db_httpstate.httpstate_key)
>>> db_httpstate.exists(db_httpstate.httpstate_key)
False

>>> db_httpstate['foo'] = 'bar'
>>> db_httpstate.save()
>>> db_httpstate.exists(db_httpstate.httpstate_key)
True
>>> prev_key = db_httpstate.httpstate_key
>>> db_httpstate.flush()
>>> db_httpstate.exists(prev_key)
False
>>> db_httpstate.httpstate_key == prev_key
False
>>> db_httpstate.modified, db_httpstate.accessed
(True, True)
>>> db_httpstate['a'], db_httpstate['b'] = 'c', 'd'
>>> db_httpstate.save()
>>> prev_key = db_httpstate.httpstate_key
>>> prev_data = db_httpstate.items()
>>> db_httpstate.cycle_key()
>>> db_httpstate.httpstate_key == prev_key
False
>>> db_httpstate.items() == prev_data
True

# Submitting an invalid httpstate key (either by guessing, or if the db has
# removed the key) results in a new key being generated.
>>> HttpState.objects.filter(pk=db_httpstate.httpstate_key).delete()
>>> db_httpstate = DatabaseHttpState(db_httpstate.httpstate_key)
>>> db_httpstate.save()
>>> DatabaseHttpState('1').get('cat')

#
# Cached DB httpstate tests
#

>>> cdb_httpstate = CacheDBHttpState()
>>> cdb_httpstate.modified
False
>>> cdb_httpstate['cat'] = "dog"
>>> cdb_httpstate.modified
True
>>> cdb_httpstate.pop('cat')
'dog'
>>> cdb_httpstate.pop('some key', 'does not exist')
'does not exist'
>>> cdb_httpstate.save()
>>> cdb_httpstate.exists(cdb_httpstate.httpstate_key)
True
>>> cdb_httpstate.delete(cdb_httpstate.httpstate_key)
>>> cdb_httpstate.exists(cdb_httpstate.httpstate_key)
False

#
# File httpstate tests.
#

# Do file httpstate tests in an isolated directory, and kill it after we're done.
>>> original_httpstate_file_path = httpstate_settings.HTTPSTATE_FILE_PATH
>>> import tempfile
>>> temp_httpstate_store = httpstate_settings.HTTPSTATE_FILE_PATH = tempfile.mkdtemp()

>>> file_httpstate = FileHttpState()
>>> file_httpstate.modified
False
>>> file_httpstate['cat'] = "dog"
>>> file_httpstate.modified
True
>>> file_httpstate.pop('cat')
'dog'
>>> file_httpstate.pop('some key', 'does not exist')
'does not exist'
>>> file_httpstate.save()
>>> file_httpstate.exists(file_httpstate.httpstate_key)
True
>>> file_httpstate.delete(file_httpstate.httpstate_key)
>>> file_httpstate.exists(file_httpstate.httpstate_key)
False
>>> FileHttpState('1').get('cat')

>>> file_httpstate['foo'] = 'bar'
>>> file_httpstate.save()
>>> file_httpstate.exists(file_httpstate.httpstate_key)
True
>>> prev_key = file_httpstate.httpstate_key
>>> file_httpstate.flush()
>>> file_httpstate.exists(prev_key)
False
>>> file_httpstate.httpstate_key == prev_key
False
>>> file_httpstate.modified, file_httpstate.accessed
(True, True)
>>> file_httpstate['a'], file_httpstate['b'] = 'c', 'd'
>>> file_httpstate.save()
>>> prev_key = file_httpstate.httpstate_key
>>> prev_data = file_httpstate.items()
>>> file_httpstate.cycle_key()
>>> file_httpstate.httpstate_key == prev_key
False
>>> file_httpstate.items() == prev_data
True

>>> HttpState.objects.filter(pk=file_httpstate.httpstate_key).delete()
>>> file_httpstate = FileHttpState(file_httpstate.httpstate_key)
>>> file_httpstate.save()

# Make sure the file backend checks for a good storage dir
>>> httpstate_settings.HTTPSTATE_FILE_PATH = "/if/this/directory/exists/you/have/a/weird/computer"
>>> FileHttpState()
Traceback (innermost last):
    ...
ImproperlyConfigured: The httpstate storage path '/if/this/directory/exists/you/have/a/weird/computer' doesn't exist. Please set your HTTPSTATE_FILE_PATH setting to an existing directory in which Django can store httpstate data.

# Clean up after the file tests
>>> httpstate_settings.HTTPSTATE_FILE_PATH = original_httpstate_file_path
>>> import shutil
>>> shutil.rmtree(temp_httpstate_store)

#
# Cache-based tests
# NB: be careful to delete any httpstates created; stale httpstates fill up the
# /tmp and eventually overwhelm it after lots of runs (think buildbots)
#

>>> cache_httpstate = CacheHttpState()
>>> cache_httpstate.modified
False
>>> cache_httpstate['cat'] = "dog"
>>> cache_httpstate.modified
True
>>> cache_httpstate.pop('cat')
'dog'
>>> cache_httpstate.pop('some key', 'does not exist')
'does not exist'
>>> cache_httpstate.save()
>>> cache_httpstate.delete(cache_httpstate.httpstate_key)
>>> cache_httpstate.exists(cache_httpstate.httpstate_key)
False
>>> cache_httpstate['foo'] = 'bar'
>>> cache_httpstate.save()
>>> cache_httpstate.exists(cache_httpstate.httpstate_key)
True
>>> prev_key = cache_httpstate.httpstate_key
>>> cache_httpstate.flush()
>>> cache_httpstate.exists(prev_key)
False
>>> cache_httpstate.httpstate_key == prev_key
False
>>> cache_httpstate.modified, cache_httpstate.accessed
(True, True)
>>> cache_httpstate['a'], cache_httpstate['b'] = 'c', 'd'
>>> cache_httpstate.save()
>>> prev_key = cache_httpstate.httpstate_key
>>> prev_data = cache_httpstate.items()
>>> cache_httpstate.cycle_key()
>>> cache_httpstate.httpstate_key == prev_key
False
>>> cache_httpstate.items() == prev_data
True

>>> HttpState.objects.filter(pk=cache_httpstate.httpstate_key).delete()
>>> cache_httpstate = CacheHttpState(cache_httpstate.httpstate_key)
>>> cache_httpstate.save()
>>> cache_httpstate.delete(cache_httpstate.httpstate_key)

>>> s = HttpStateBase()
>>> s._httpstate['some key'] = 'exists' # Pre-populate the httpstate with some data
>>> s.accessed = False   # Reset to pretend this wasn't accessed previously

>>> s.accessed, s.modified
(False, False)

>>> s.pop('non existant key', 'does not exist')
'does not exist'
>>> s.accessed, s.modified
(True, False)

>>> s.setdefault('foo', 'bar')
'bar'
>>> s.setdefault('foo', 'baz')
'bar'

>>> s.accessed = False  # Reset the accessed flag

>>> s.pop('some key')
'exists'
>>> s.accessed, s.modified
(True, True)

>>> s.pop('some key', 'does not exist')
'does not exist'


>>> s.get('update key', None)

# test .update()
>>> s.modified = s.accessed = False   # Reset to pretend this wasn't accessed previously
>>> s.update({'update key':1})
>>> s.accessed, s.modified
(True, True)
>>> s.get('update key', None)
1

# test .has_key()
>>> s.modified = s.accessed = False   # Reset to pretend this wasn't accessed previously
>>> s.has_key('update key')
True
>>> s.accessed, s.modified
(True, False)

# test .values()
>>> s = HttpStateBase()
>>> s.values()
[]
>>> s.accessed
True
>>> s['x'] = 1
>>> s.values()
[1]

# test .iterkeys()
>>> s.accessed = False
>>> i = s.iterkeys()
>>> hasattr(i,'__iter__')
True
>>> s.accessed
True
>>> list(i)
['x']

# test .itervalues()
>>> s.accessed = False
>>> i = s.itervalues()
>>> hasattr(i,'__iter__')
True
>>> s.accessed
True
>>> list(i)
[1]

# test .iteritems()
>>> s.accessed = False
>>> i = s.iteritems()
>>> hasattr(i,'__iter__')
True
>>> s.accessed
True
>>> list(i)
[('x', 1)]

# test .clear()
>>> s.modified = s.accessed = False
>>> s.items()
[('x', 1)]
>>> s.clear()
>>> s.items()
[]
>>> s.accessed, s.modified
(True, True)

#########################
# Custom httpstate expiry #
#########################

>>> from django.conf import settings
>>> from datetime import datetime, timedelta
>>> from django.utils.timezone import now as tz_now

>>> td10 = timedelta(seconds=10)

# A normal httpstate has a max age equal to settings
>>> s.get_expiry_age() == httpstate_settings.HTTPSTATE_COOKIE_AGE
True

# So does a custom httpstate with an idle expiration time of 0 (but it'll expire
# at browser close)
>>> s.set_expiry(0)
>>> s.get_expiry_age() == httpstate_settings.HTTPSTATE_COOKIE_AGE
True

# Custom httpstate idle expiration time
>>> s.set_expiry(10)
>>> delta = s.get_expiry_date() - tz_now()
>>> delta.seconds in (9, 10)
True
>>> age = s.get_expiry_age()
>>> age in (9, 10)
True

# Custom httpstate fixed expiry date (timedelta)
>>> s.set_expiry(td10)
>>> delta = s.get_expiry_date() - tz_now()
>>> delta.seconds in (9, 10)
True
>>> age = s.get_expiry_age()
>>> age in (9, 10)
True

# Custom httpstate fixed expiry date (fixed datetime)
>>> s.set_expiry(tz_now() + td10)
>>> delta = s.get_expiry_date() - tz_now()
>>> delta.seconds in (9, 10)
True
>>> age = s.get_expiry_age()
>>> age in (9, 10)
True

# Set back to default httpstate age
>>> s.set_expiry(None)
>>> s.get_expiry_age() == httpstate_settings.HTTPSTATE_COOKIE_AGE
True

# Allow to set back to default httpstate age even if no alternate has been set
>>> s.set_expiry(None)


# We're changing the setting then reverting back to the original setting at the
# end of these tests.
>>> original_expire_at_browser_close = httpstate_settings.HTTPSTATE_EXPIRE_AT_BROWSER_CLOSE
>>> httpstate_settings.HTTPSTATE_EXPIRE_AT_BROWSER_CLOSE = False

# Custom httpstate age
>>> s.set_expiry(10)
>>> s.get_expire_at_browser_close()
False

# Custom expire-at-browser-close
>>> s.set_expiry(0)
>>> s.get_expire_at_browser_close()
True

# Default httpstate age
>>> s.set_expiry(None)
>>> s.get_expire_at_browser_close()
False

>>> httpstate_settings.HTTPSTATE_EXPIRE_AT_BROWSER_CLOSE = True

# Custom httpstate age
>>> s.set_expiry(10)
>>> s.get_expire_at_browser_close()
False

# Custom expire-at-browser-close
>>> s.set_expiry(0)
>>> s.get_expire_at_browser_close()
True

# Default httpstate age
>>> s.set_expiry(None)
>>> s.get_expire_at_browser_close()
True

>>> httpstate_settings.HTTPSTATE_EXPIRE_AT_BROWSER_CLOSE = original_expire_at_browser_close
"""

if __name__ == '__main__':
    import doctest
    doctest.testmod()
