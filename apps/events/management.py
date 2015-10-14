# -*- coding: UTF-8 -*-

from django.db.models import signals
# -*- coding: UTF-8 -*-
from django.db import models
from django.conf import settings

from base_libs.utils.misc import get_translation

try:
    from jetson.apps.structure import models as structure_models

    def create_structure(app, created_models, verbosity, **kwargs):
        from jetson.apps.events.base import ComplexEventBase

        Vocabulary = models.get_model("structure", "Vocabulary")
        Term = models.get_model("structure", "Term")
        Event = models.get_model("events", "Event")

        if not issubclass(Event, ComplexEventBase):
            return

        _ = lambda s: s
        try:
            v = Vocabulary.objects.get(sysname='basics_object_types')
        except Vocabulary.DoesNotExist:
            v = Vocabulary(
                sysname='basics_object_types',
                slug='basics_object_types',
            )
            for lang_code, lang_title in settings.LANGUAGES:
                setattr(
                    v,
                    "title_%s" % lang_code,
                    get_translation(
                        _("Object Types"),
                        language=lang_code,
                    ),
                )
            v.save()
            if verbosity > 1:
                print 'Vocabulary "basics_object_types" created.'

        t, created = Term.objects.get_or_create(
            vocabulary=v,
            sysname="event",
        )
        if created:
            for lang_code, lang_title in settings.LANGUAGES:
                t.slug = "event"
                setattr(
                    t,
                    "title_%s" % lang_code,
                    get_translation(
                        _("Event"),
                        language=lang_code,
                    ),
                )
            t.save()
            if verbosity > 1:
                print 'Term "event" created.'

        if not t.child_set.count():
            defaults = (
                {'sysname': u'biennial', 'title': _(u'Biennial')},
                {'sysname': u'competition', 'title': _(u'Competition')},
                {'sysname': u'concert', 'title': _(u'Concert')},
                {'sysname': u'conference', 'title': _(u'Conference')},
                {'sysname': u'convention', 'title': _(u'Convention')},
                {'sysname': u'exhibition', 'title': _(u'Exhibition')},
                {'sysname': u'lecture', 'title': _(u'Lecture')},
                {'sysname': u'meeting', 'title': _(u'Meeting')},
                {'sysname': u'opening', 'title': _(u'Opening')},
                {'sysname': u'performance', 'title': _(u'Performance')},
                {'sysname': u'reading', 'title': _(u'Reading')},
                {'sysname': u'reception', 'title': _(u'Reception')},
                {'sysname': u'symposium', 'title': _(u'Symposium')},
                {'sysname': u'trade_show', 'title': _(u'Trade Show')},
                {'sysname': u'workshop', 'title': _(u'Workshop')},
                {'sysname': u'festival', 'title': _(u'Festival')},
            )
            for t_child_data in defaults:
                t_child = Term(
                    vocabulary=v,
                    parent=t,
                    sysname=t_child_data['sysname'],
                    slug=t_child_data['sysname'].replace("_", "-"),
                )
                for lang_code, lang_title in settings.LANGUAGES:
                    setattr(
                        t_child,
                        "title_%s" % lang_code,
                        get_translation(
                            t_child_data['title'],
                            language=lang_code,
                        ),
                    )
                t_child.save()
            if verbosity > 1:
                print 'Default event types created.'

        try:
            v = Vocabulary.objects.get(sysname='event_time_labels')
        except Vocabulary.DoesNotExist:
            v = Vocabulary(
                sysname='event_time_labels',
                slug='event_time_labels',
            )
            for lang_code, lang_title in settings.LANGUAGES:
                setattr(
                    v,
                    "title_%s" % lang_code,
                    get_translation(
                        _("Event-time Labels"),
                        language=lang_code,
                    ),
                )
            v.save()
            if verbosity > 1:
                print 'Vocabulary "event_time_labels" created.'
        if not v.term_set.count():
            defaults = (
                {'sysname': u'app_submission', 'title': _(u'Application Submission')},
                {'sysname': u'app_deadline', 'title': _(u'Application Deadline')},
                {'sysname': u'vernissage', 'title': _(u'Vernissage')},
                {'sysname': u'finissage', 'title': _(u'Finissage')},
            )
            for t_data in defaults:
                t = Term(
                    vocabulary=v,
                    sysname=t_data['sysname'],
                    slug=t_data['sysname'].replace("_", "-"),
                )
                for lang_code, lang_title in settings.LANGUAGES:
                    setattr(
                        t,
                        "title_%s" % lang_code,
                        get_translation(
                            t_data['title'],
                            language=lang_code,
                        ),
                    )
                t.save()
            if verbosity > 1:
                print 'Default event time labels created.'


                # models.signals.post_syncdb.connect(create_structure, sender=structure_models)
except ImportError:
    print "Skipping creation of Vocabularies and Terms as structure app not found"

try:
    from jetson.apps.notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type(
            "event_by_favorite_institution",
            "New event by your favorite institution",
            "one of your favorite institutions published a new event",
            default=0,
        )
        notification.create_notice_type(
            "event_by_contact",
            "New event by your contact",
            "one of your contacts published a new event",
            default=0,
        )

    signals.post_syncdb.connect(create_notice_types, sender=notification)
except ImportError:
    print "Skipping creation of NoticeTypes as notification app not found"
