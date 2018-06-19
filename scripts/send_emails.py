# -*- coding: utf-8 -*-

import os
import sys


def configure_django_project():
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    EXTERNAL_LIBS_PATH = os.path.join(PROJECT_PATH, "jetson", "externals", "libs")
    EXTERNAL_APPS_PATH = os.path.join(PROJECT_PATH, "jetson", "externals", "apps")

    sys.path = ["", EXTERNAL_LIBS_PATH, EXTERNAL_APPS_PATH, PROJECT_PATH] + sys.path
    os.environ["DJANGO_SETTINGS_MODULE"] = "ccb.settings"
    os.environ["PYTHON_EGG_CACHE"] = "/srv/www/vhosts/creative-city-berlin.de/python_cache"


def send_emails():
    from jetson.apps.mailing.models import EmailMessage

    EmailMessage.objects.send_mails()


def main():
    configure_django_project()
    send_emails()


if __name__ == '__main__':
    main()
