# -*- coding: utf-8 -*-

import os
import sys
import datetime


def configure_django_project():
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    EXTERNAL_LIBS_PATH = os.path.join(PROJECT_PATH, "jetson", "externals", "libs")
    EXTERNAL_APPS_PATH = os.path.join(PROJECT_PATH, "jetson", "externals", "apps")

    sys.path = ["", EXTERNAL_LIBS_PATH, EXTERNAL_APPS_PATH, PROJECT_PATH] + sys.path
    os.environ["DJANGO_SETTINGS_MODULE"] = "ccb.settings"
    os.environ["PYTHON_EGG_CACHE"] = "/home/ccb/project/jetson-project/ccb/tmp/python_cache"


def remove_expired_sessions():
    from django.contrib.sessions.models import Session

    Session.objects.filter(expire_date__lt=datetime.datetime.now()).delete()


def remove_expired_httpstates():
    from jetson.apps.httpstate.models import HttpState

    HttpState.objects.filter(expire_date__lt=datetime.datetime.now()).delete()


def update_expired_events():
    from django.db import models

    Event = models.get_model("events", "Event")
    Event.objects.update_current()
    Event.objects.update_expired()


def update_people_completeness():
    from django.apps import apps

    Person = apps.get_model("people", "Person")
    for p in Person.objects.all():
        p.calculate_completeness()
        p.save()


def update_institutions_completeness():
    from django.apps import apps

    Institution = apps.get_model("institutions", "Institution")
    for inst in Institution.objects.all():
        inst.calculate_completeness()
        inst.save()


def main():
    configure_django_project()
    remove_expired_sessions()
    remove_expired_httpstates()
    update_expired_events()
    update_people_completeness()
    update_institutions_completeness()


if __name__ == '__main__':
    main()
