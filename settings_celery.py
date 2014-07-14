from settings import *

INSTALLED_APPS = filter(
    lambda app: app != "haystack",
    INSTALLED_APPS
    )
