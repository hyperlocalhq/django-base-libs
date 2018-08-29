# -*- coding: utf-8 -*-

import os
import sys
import time
import datetime

def configure_django_project():
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    EXTERNAL_LIBS_PATH = os.path.join(PROJECT_PATH, "jetson", "externals", "libs")
    EXTERNAL_APPS_PATH = os.path.join(PROJECT_PATH, "jetson", "externals", "apps")
    
    sys.path = ["", EXTERNAL_LIBS_PATH, EXTERNAL_APPS_PATH, PROJECT_PATH] + sys.path
    os.environ["DJANGO_SETTINGS_MODULE"] = "jetson.settings"
    os.environ["PYTHON_EGG_CACHE"] = "/srv/www/vhosts/jetsonproject.com/python_cache"

def remove_expired_sessions():
    from django.contrib.sessions.models import Session
    Session.objects.filter(expire_date__lt=datetime.datetime.now()).delete()

def update_expired_events():
    from jetson.events.models import Event
    Event.objects.update_expired()

def main():
    configure_django_project()
    remove_expired_sessions()
    update_expired_events()

if __name__ == '__main__':
    main()
