from django.conf import settings

HTTPSTATE_COOKIE_NAME = getattr(settings, 'HTTPSTATE_COOKIE_NAME', 'httpstateid')                   # Cookie name. This can be whatever you want.
HTTPSTATE_COOKIE_AGE = getattr(settings, 'HTTPSTATE_COOKIE_AGE', 60 * 60 * 24 * 7 * 2)              # Age of cookie, in seconds (default: 2 weeks).
HTTPSTATE_COOKIE_DOMAIN = getattr(settings, 'HTTPSTATE_COOKIE_DOMAIN', None)                        # A string like ".lawrence.com", or None for standard domain cookie.
HTTPSTATE_COOKIE_SECURE = getattr(settings, 'HTTPSTATE_COOKIE_SECURE', False)                       # Whether the httpstate cookie should be secure (https:// only).
HTTPSTATE_COOKIE_PATH = getattr(settings, 'HTTPSTATE_COOKIE_PATH', '/')                             # The path of the httpstate cookie.
HTTPSTATE_SAVE_EVERY_REQUEST = getattr(settings, 'HTTPSTATE_SAVE_EVERY_REQUEST', False)             # Whether to save the httpstate data on every request.
HTTPSTATE_EXPIRE_AT_BROWSER_CLOSE = getattr(settings, 'HTTPSTATE_EXPIRE_AT_BROWSER_CLOSE', False)   # Whether a user's httpstate cookie expires when the Web browser is closed.
HTTPSTATE_ENGINE = getattr(settings, 'HTTPSTATE_ENGINE', 'jetson.apps.httpstate.backends.db')       # The module to store httpstate data
HTTPSTATE_FILE_PATH = getattr(settings, 'HTTPSTATE_FILE_PATH', None)                                # Directory to store httpstate files if using the file httpstate module. If None, the backend will use a sensible default.