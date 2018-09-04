# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import get_language, activate

from django_elasticsearch_dsl import DocType, Index, fields

from filebrowser.models import FileDescription
from ...apps.locations.models import Location
from .models import Production, Event, ProductionImage, EventImage

# Name of the Elasticsearch index
search_index = Index('events')
# See Elasticsearch Indices API reference for available settings
search_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

def _get_url_path(instance, language):
    current_language = get_language()
    activate(language)
    url_path = instance.get_url_path()
    activate(current_language)
    return url_path

@search_index.doc_type
class EventDocument(DocType):
    ensembles = fields.StringField()
    original_de = fields.StringField()
    original_en = fields.StringField()
    prefix_de = fields.StringField()
    prefix_en = fields.StringField()
    title_de = fields.StringField(fielddata=True)
    title_en = fields.StringField(fielddata=True)
    subtitle_de = fields.StringField()
    subtitle_en = fields.StringField()
    is_premiere = fields.BooleanField()
    is_canceled = fields.BooleanField()
    is_published = fields.BooleanField()
    teaser_de = fields.TextField()
    teaser_en = fields.TextField()

    url_path_de = fields.StringField()
    url_path_en = fields.StringField()

    start = fields.DateField()
    start_time = fields.StringField()

    categories = fields.NestedField(properties={
        'title_de': fields.StringField(),
        'title_en': fields.StringField(),
        'pk': fields.IntegerField(),
    }, include_in_root=True)

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

    play_stages = fields.NestedField(properties={
        'title_de': fields.StringField(),
        'title_en': fields.StringField(),
        'pk': fields.IntegerField(),
    }, include_in_root=True)

    festivals = fields.NestedField(properties={
        'title_de': fields.StringField(),
        'title_en': fields.StringField(),
        'url_path_de': fields.StringField(),
        'url_path_en': fields.StringField(),
        'pk': fields.IntegerField(),
    }, include_in_root=True)

    # There are no examples online how to use ObjectField in queries, so let's NestedField instead
    language_and_subtitles = fields.NestedField(properties={
        'title_de': fields.StringField(),
        'title_en': fields.StringField(),
        'pk': fields.IntegerField(),
    }, include_in_root=True)

    location_title = fields.StringField()

    tickets_website = fields.StringField()

    image_path = fields.StringField()
    image_author = fields.StringField()

    # _meta and pk added just for possibility to add to favorites

    _meta = Event._meta

    @property
    def pk(self):
        return self.id

    class Meta:
        model = Event # The model associated with this DocType

        # The fields of the model you want to be indexed in Elasticsearch
        fields = ['id']
        # For now we get rid of Location model, because the saving of locations takes too long and times out
        #related_models = [Production, Location]
        related_models = [Production, ProductionImage, EventImage]

    def get_queryset(self):
        return super(EventDocument, self).get_queryset().select_related('production')

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Production):
            production = related_instance
            if not getattr(production, "_skip_search_document_update", False):
                return production.event_set.all()
        elif isinstance(related_instance, ProductionImage):
            production = related_instance.production
            return production.event_set.all()
        elif isinstance(related_instance, EventImage):
            event = related_instance.event
            return [event]

        # For now we get rid of Location model, because the saving of locations takes too long and times out
        # If a location is renamed or deleted, all indexes have to be rebuilt with:
        # python manage.py search_index --rebuild
        #
        # elif isinstance(related_instance, Location):
        #     return Event.objects.filter(
        #         models.Q(production__in_program_of=related_instance) |
        #         models.Q(production__play_locations=related_instance) |
        #         models.Q(play_locations=related_instance)
        #     )

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

    # is_premiere

    def prepare_is_premiere(self, instance):
        return bool(instance.get_special_text(language='de'))

    # is_canceled

    def prepare_is_canceled(self, instance):
        return instance.is_canceled()

    # is_published

    def prepare_is_published(self, instance):
        return instance.event_status != "trashed" and instance.production.status == "published" and instance.production.part_set.count() == 0

    # teaser

    def prepare_teaser_de(self, instance):
        return instance.get_rendered_teaser_de() or instance.production.get_rendered_teaser_de()

    def prepare_teaser_en(self, instance):
        return (
            instance.get_rendered_teaser_en() or
            instance.production.get_rendered_teaser_en() or
            self.prepare_teaser_de(instance)
        )

    def get_teaser(self, language=settings.LANGUAGE_CODE):
        return getattr(self, 'teaser_{}'.format(language))

    # start

    def prepare_start(self, instance):
        from datetime import datetime
        return datetime.combine(instance.start_date, instance.start_time)

    def prepare_start_time(self, instance):
        if instance.start_time:
            return instance.start_time.strftime('%H:%M')
        return ''

    # categories

    def prepare_categories(self, instance):
        return [{
            'title_de': obj.title_de,
            'title_en': obj.title_en or obj.title_de,
            'pk': obj.pk,
        } for obj in instance.production.get_categories()]

    def get_first_category_title(self, language=settings.LANGUAGE_CODE):
        if not self.categories:
            return ''
        return getattr(self.categories[0], 'title_{}'.format(language))

    # in_program_of

    def prepare_in_program_of(self, instance):
        return [{
            'title_de': obj.title_de,
            'title_en': obj.title_en or obj.title_de,
            'pk': obj.pk,
        } for obj in instance.production.in_program_of.all()]

    def get_in_program_of(self, language=settings.LANGUAGE_CODE):
        return [{
            'title': item['title_{}'.format(language)],
            'pk': item['pk'],
        } for item in self.in_program_of]

    # play_locations

    def prepare_play_locations(self, instance):
        return [{
            'title_de': obj.title_de,
            'title_en': obj.title_en or obj.title_de,
            'pk': obj.pk,
        } for obj in instance.ev_or_prod_play_locations()]

    def get_play_locations(self, language=settings.LANGUAGE_CODE):
        return [{
            'title': item['title_{}'.format(language)],
            'pk': item['pk'],
        } for item in self.play_locations]

    # play_stages

    def prepare_play_stages(self, instance):
        return [{
            'title_de': obj.title_de,
            'title_en': obj.title_en or obj.title_de,
            'pk': obj.pk,
        } for obj in instance.ev_or_prod_play_stages()]

    def get_play_stages(self, language=settings.LANGUAGE_CODE):
        return [{
            'title': item['title_{}'.format(language)],
            'pk': item['pk'],
        } for item in self.play_stages]


    # play_stages

    def prepare_festivals(self, instance):
        return [{
            'title_de': obj.title_de,
            'title_en': obj.title_en or obj.title_de,
            'url_path_de': _get_url_path(obj, language='de'),
            'url_path_en': _get_url_path(obj, language='en'),
            'pk': obj.pk,
        } for obj in instance.get_festivals()]

    def get_festivals(self, language=settings.LANGUAGE_CODE):
        return [{
            'title': item['title_{}'.format(language)],
            'url_path': item['url_path_{}'.format(language)],
            'pk': item['pk'],
        } for item in self.festivals]


    # language_and_subtitles

    def prepare_language_and_subtitles(self, instance):
        obj = instance.language_and_subtitles or instance.production.language_and_subtitles
        if obj:
            return [{
                'title_de': obj.title_de,
                'title_en': obj.title_en or obj.title_de,
                'pk': obj.pk,
            }]
        return None

    def get_language_and_subtitles_title(self, language=settings.LANGUAGE_CODE):
        if not self.language_and_subtitles:
            return ''
        return getattr(self.language_and_subtitles[0], 'title_{}'.format(language))

    # tickets_website

    def prepare_tickets_website(self, instance):
        return instance.ev_or_prod_tickets_website()

    # image_path

    def prepare_image_path(self, instance):
        image_path = ''
        if instance.first_image and instance.first_image.path:
            image_path = instance.first_image.path.path
        elif instance.ev_or_prod_images():
            ev_or_prod_image = instance.ev_or_prod_images()[0]
            if ev_or_prod_image.path:
                image_path = ev_or_prod_image.path.path
        return image_path

    # image_author

    def prepare_image_author(self, instance):
        image_path = self.prepare_image_path(instance)
        if image_path:
            try:
                file_description = FileDescription.objects.get(file_path=image_path)
            except (FileDescription.DoesNotExist, FileDescription.MultipleObjectsReturned):
                return ''
            else:
                return file_description.author
        return ''

    # location_title

    def prepare_location_title(self, instance):
        return instance.location_title or instance.production.location_title

    # url_path

    def prepare_url_path_de(self, instance):
        return _get_url_path(instance, language='de')

    def prepare_url_path_en(self, instance):
        return _get_url_path(instance, language='en')

    def get_url_path(self, language=settings.LANGUAGE_CODE):
        return getattr(self, 'url_path_{}'.format(language))
