# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from django_elasticsearch_dsl import DocType, Index, fields

from ...apps.locations.models import Location
from .models import Production, Event

# Name of the Elasticsearch index
search_index = Index('library')
# See Elasticsearch Indices API reference for available settings
search_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

# TODO: collect all the fields and relations necessary for search and display of events

@search_index.doc_type
class EventDocument(DocType):
    ensembles = fields.StringField()
    original_de = fields.StringField()
    original_en = fields.StringField()
    prefix_de = fields.StringField()
    prefix_en = fields.StringField()
    title_de = fields.StringField()
    title_en = fields.StringField()
    subtitle_de = fields.StringField()
    subtitle_en = fields.StringField()
    start = fields.DateField()
    start_time = fields.DateField()
    in_program_of = fields.NestedField(properties={
        'title_de': fields.StringField(),
        'title_en': fields.StringField(),
        'pk': fields.IntegerField(),
    }, include_in_root=True)
    play_locations = fields.NestedField(properties={
        'title_de': fields.StringField(),
        'title_en': fields.StringField(),
        'pk': fields.IntegerField(),
    }, include_in_root=True)

    class Meta:
        model = Event # The model associated with this DocType

        # The fields of the model you want to be indexed in Elasticsearch
        fields = ['id']
        related_model = [Production, Location]

    def get_queryset(self):
        return super(EventDocument, self).get_queryset().select_related('production').filter(
            production__status="published",
            production__part=None,
        ).exclude(
            event_status="trashed",
        )

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Production):
            return related_instance.event_set.all()
        elif isinstance(related_instance, Location):
            return Event.objects.filter(
                models.Q(production__in_program_of=related_instance) |
                models.Q(production__play_locations=related_instance) |
                models.Q(play_locations=related_instance)
            )

    # ensembles

    def prepare_ensembles(self, instance):
        return instance.production.ensembles

    # original

    def prepare_original_de(self, instance):
        return instance.production.original_de

    def prepare_original_en(self, instance):
        return instance.production.original_en or instance.production.original_de

    def get_original(self, language=settings.LANGUAGE_CODE):
        return getattr(self, 'original_{}'.format(language))

    # prefix

    def prepare_prefix_de(self, instance):
        return instance.production.prefix_de

    def prepare_prefix_en(self, instance):
        return instance.production.prefix_en or instance.production.prefix_de

    def get_prefix(self, language=settings.LANGUAGE_CODE):
        return getattr(self, 'prefix_{}'.format(language))

    # title

    def prepare_title_de(self, instance):
        return instance.production.title_de

    def prepare_title_en(self, instance):
        return instance.production.title_en or instance.production.title_de

    def get_title(self, language=settings.LANGUAGE_CODE):
        return getattr(self, 'title_{}'.format(language))

    # subtitle

    def prepare_subtitle_de(self, instance):
        return instance.production.subtitle_de or instance.ev_or_prod_subtitles_text()

    def prepare_subtitle_en(self, instance):
        return instance.production.subtitle_en or instance.production.subtitle_de or instance.ev_or_prod_subtitles_text()

    def get_subtitle(self, language=settings.LANGUAGE_CODE):
        return getattr(self, 'subtitle_{}'.format(language))

    # start

    def prepare_start(self, instance):
        from datetime import datetime
        return datetime.combine(instance.start_date, instance.start_time)

    def prepare_start_time(self, instance):
        return instance.start_time

    # in_program_of

    def prepare_in_program_of(self, instance):
        return [{
            'title_de': obj.title_de,
            'title_en': obj.title_en or obj.title_de,
            'pk': obj.pk,
        } for obj in instance.production.in_program_of.all()]

    # play_locations

    def prepare_play_locations(self, instance):
        return [{
            'title_de': obj.title_de,
            'title_en': obj.title_en or obj.title_de,
            'pk': obj.pk,
        } for obj in instance.ev_or_prod_play_locations()]
