# -*- coding: utf-8 -*-

import os, sys


def configure_django_project():
    PROJECT_PATH = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    EXTERNAL_LIBS_PATH = os.path.join(
        PROJECT_PATH, "jetson", "externals", "libs"
    )
    EXTERNAL_APPS_PATH = os.path.join(
        PROJECT_PATH, "jetson", "externals", "apps"
    )

    sys.path = [
        "", EXTERNAL_LIBS_PATH, EXTERNAL_APPS_PATH, PROJECT_PATH
    ] + sys.path
    os.environ["DJANGO_SETTINGS_MODULE"] = "jetson.settings"
    os.environ["PYTHON_EGG_CACHE"
              ] = "/srv/www/vhosts/jetsonproject.com/python_cache"


def main():
    configure_django_project()
    from jetson.mailing.models import EmailMessage
    EmailMessage.objects.send_mails()


if __name__ == '__main__':
    main()
