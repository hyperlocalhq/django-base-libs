# -*- coding: UTF-8 -*-
import datetime
from django.core.management.base import NoArgsCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(NoArgsCommand):
    help = """Runs daily tasks: removing expired http states and sessions, updating events, setting completeness for people and institutions"""

    def handle_noargs(self, **options):
        # self.remove_expired_sessions()
        # self.remove_expired_httpstates()
        self.update_expired_events()
        self.update_people_completeness()
        self.update_institutions_completeness()

    # def remove_expired_sessions(self):
    #     from django.contrib.sessions.models import Session
    #     Session.objects.filter(
    #         expire_date__lt=datetime.datetime.now()
    #     ).delete()
    #
    # def remove_expired_httpstates(self):
    #     from jetson.apps.httpstate.models import HttpState
    #     HttpState.objects.filter(
    #         expire_date__lt=datetime.datetime.now()
    #     ).delete()

    def update_expired_events(self):
        from django.apps import apps

        Event = apps.get_model("events", "Event")
        Event.objects.update_current()
        Event.objects.update_expired()

    def update_people_completeness(self):
        from django.apps import apps

        Person = apps.get_model("people", "Person")
        for p in Person.objects.all():
            p.calculate_completeness()
            p.save()

    def update_institutions_completeness(self):
        from django.apps import apps

        Institution = apps.get_model("institutions", "Institution")
        for inst in Institution.objects.all():
            inst.calculate_completeness()
            inst.save()
