# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
                # Adding field 'MuseumCategory.title_fr'
        db.add_column(u'museums_museumcategory', 'title_fr',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'MuseumCategory.title_pl'
        db.add_column(u'museums_museumcategory', 'title_pl',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'MuseumCategory.title_tr'
        db.add_column(u'museums_museumcategory', 'title_tr',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'MuseumCategory.title_es'
        db.add_column(u'museums_museumcategory', 'title_es',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'MuseumCategory.title_it'
        db.add_column(u'museums_museumcategory', 'title_it',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Museum.reduced_price_info_fr'
        db.add_column(u'museums_museum', 'reduced_price_info_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Reduced admission price info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.reduced_price_info_fr_markup_type'
        db.add_column(u'museums_museum', 'reduced_price_info_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.reduced_price_info_pl'
        db.add_column(u'museums_museum', 'reduced_price_info_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Reduced admission price info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.reduced_price_info_pl_markup_type'
        db.add_column(u'museums_museum', 'reduced_price_info_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.reduced_price_info_tr'
        db.add_column(u'museums_museum', 'reduced_price_info_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Reduced admission price info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.reduced_price_info_tr_markup_type'
        db.add_column(u'museums_museum', 'reduced_price_info_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.reduced_price_info_es'
        db.add_column(u'museums_museum', 'reduced_price_info_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Reduced admission price info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.reduced_price_info_es_markup_type'
        db.add_column(u'museums_museum', 'reduced_price_info_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.reduced_price_info_it'
        db.add_column(u'museums_museum', 'reduced_price_info_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Reduced admission price info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.reduced_price_info_it_markup_type'
        db.add_column(u'museums_museum', 'reduced_price_info_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.group_ticket_fr'
        db.add_column(u'museums_museum', 'group_ticket_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Group ticket', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.group_ticket_fr_markup_type'
        db.add_column(u'museums_museum', 'group_ticket_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.group_ticket_pl'
        db.add_column(u'museums_museum', 'group_ticket_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Group ticket', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.group_ticket_pl_markup_type'
        db.add_column(u'museums_museum', 'group_ticket_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.group_ticket_tr'
        db.add_column(u'museums_museum', 'group_ticket_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Group ticket', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.group_ticket_tr_markup_type'
        db.add_column(u'museums_museum', 'group_ticket_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.group_ticket_es'
        db.add_column(u'museums_museum', 'group_ticket_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Group ticket', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.group_ticket_es_markup_type'
        db.add_column(u'museums_museum', 'group_ticket_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.group_ticket_it'
        db.add_column(u'museums_museum', 'group_ticket_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Group ticket', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.group_ticket_it_markup_type'
        db.add_column(u'museums_museum', 'group_ticket_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.title_fr'
        db.add_column(u'museums_museum', 'title_fr',
                      self.gf('django.db.models.fields.CharField')(u'Name', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Museum.title_pl'
        db.add_column(u'museums_museum', 'title_pl',
                      self.gf('django.db.models.fields.CharField')(u'Name', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Museum.title_tr'
        db.add_column(u'museums_museum', 'title_tr',
                      self.gf('django.db.models.fields.CharField')(u'Name', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Museum.title_es'
        db.add_column(u'museums_museum', 'title_es',
                      self.gf('django.db.models.fields.CharField')(u'Name', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Museum.title_it'
        db.add_column(u'museums_museum', 'title_it',
                      self.gf('django.db.models.fields.CharField')(u'Name', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Museum.admission_price_info_fr'
        db.add_column(u'museums_museum', 'admission_price_info_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Admission price info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.admission_price_info_fr_markup_type'
        db.add_column(u'museums_museum', 'admission_price_info_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.admission_price_info_pl'
        db.add_column(u'museums_museum', 'admission_price_info_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Admission price info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.admission_price_info_pl_markup_type'
        db.add_column(u'museums_museum', 'admission_price_info_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.admission_price_info_tr'
        db.add_column(u'museums_museum', 'admission_price_info_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Admission price info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.admission_price_info_tr_markup_type'
        db.add_column(u'museums_museum', 'admission_price_info_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.admission_price_info_es'
        db.add_column(u'museums_museum', 'admission_price_info_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Admission price info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.admission_price_info_es_markup_type'
        db.add_column(u'museums_museum', 'admission_price_info_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.admission_price_info_it'
        db.add_column(u'museums_museum', 'admission_price_info_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Admission price info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.admission_price_info_it_markup_type'
        db.add_column(u'museums_museum', 'admission_price_info_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.description_fr'
        db.add_column(u'museums_museum', 'description_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.description_fr_markup_type'
        db.add_column(u'museums_museum', 'description_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.description_pl'
        db.add_column(u'museums_museum', 'description_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.description_pl_markup_type'
        db.add_column(u'museums_museum', 'description_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.description_tr'
        db.add_column(u'museums_museum', 'description_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.description_tr_markup_type'
        db.add_column(u'museums_museum', 'description_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.description_es'
        db.add_column(u'museums_museum', 'description_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.description_es_markup_type'
        db.add_column(u'museums_museum', 'description_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.description_it'
        db.add_column(u'museums_museum', 'description_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.description_it_markup_type'
        db.add_column(u'museums_museum', 'description_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.subtitle_fr'
        db.add_column(u'museums_museum', 'subtitle_fr',
                      self.gf('django.db.models.fields.CharField')(u'Subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Museum.subtitle_pl'
        db.add_column(u'museums_museum', 'subtitle_pl',
                      self.gf('django.db.models.fields.CharField')(u'Subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Museum.subtitle_tr'
        db.add_column(u'museums_museum', 'subtitle_tr',
                      self.gf('django.db.models.fields.CharField')(u'Subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Museum.subtitle_es'
        db.add_column(u'museums_museum', 'subtitle_es',
                      self.gf('django.db.models.fields.CharField')(u'Subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Museum.subtitle_it'
        db.add_column(u'museums_museum', 'subtitle_it',
                      self.gf('django.db.models.fields.CharField')(u'Subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Museum.accessibility_fr'
        db.add_column(u'museums_museum', 'accessibility_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Accessibility', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.accessibility_fr_markup_type'
        db.add_column(u'museums_museum', 'accessibility_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.accessibility_pl'
        db.add_column(u'museums_museum', 'accessibility_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Accessibility', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.accessibility_pl_markup_type'
        db.add_column(u'museums_museum', 'accessibility_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.accessibility_tr'
        db.add_column(u'museums_museum', 'accessibility_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Accessibility', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.accessibility_tr_markup_type'
        db.add_column(u'museums_museum', 'accessibility_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.accessibility_es'
        db.add_column(u'museums_museum', 'accessibility_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Accessibility', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.accessibility_es_markup_type'
        db.add_column(u'museums_museum', 'accessibility_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.accessibility_it'
        db.add_column(u'museums_museum', 'accessibility_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Accessibility', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.accessibility_it_markup_type'
        db.add_column(u'museums_museum', 'accessibility_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.image_caption_fr'
        db.add_column(u'museums_museum', 'image_caption_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Image Caption', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=255, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.image_caption_fr_markup_type'
        db.add_column(u'museums_museum', 'image_caption_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.image_caption_pl'
        db.add_column(u'museums_museum', 'image_caption_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Image Caption', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=255, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.image_caption_pl_markup_type'
        db.add_column(u'museums_museum', 'image_caption_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.image_caption_tr'
        db.add_column(u'museums_museum', 'image_caption_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Image Caption', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=255, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.image_caption_tr_markup_type'
        db.add_column(u'museums_museum', 'image_caption_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.image_caption_es'
        db.add_column(u'museums_museum', 'image_caption_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Image Caption', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=255, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.image_caption_es_markup_type'
        db.add_column(u'museums_museum', 'image_caption_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.image_caption_it'
        db.add_column(u'museums_museum', 'image_caption_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Image Caption', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=255, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.image_caption_it_markup_type'
        db.add_column(u'museums_museum', 'image_caption_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.mobidat_fr'
        db.add_column(u'museums_museum', 'mobidat_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Mobidat', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.mobidat_fr_markup_type'
        db.add_column(u'museums_museum', 'mobidat_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.mobidat_pl'
        db.add_column(u'museums_museum', 'mobidat_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Mobidat', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.mobidat_pl_markup_type'
        db.add_column(u'museums_museum', 'mobidat_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.mobidat_tr'
        db.add_column(u'museums_museum', 'mobidat_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Mobidat', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.mobidat_tr_markup_type'
        db.add_column(u'museums_museum', 'mobidat_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.mobidat_es'
        db.add_column(u'museums_museum', 'mobidat_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Mobidat', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.mobidat_es_markup_type'
        db.add_column(u'museums_museum', 'mobidat_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Museum.mobidat_it'
        db.add_column(u'museums_museum', 'mobidat_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Mobidat', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Museum.mobidat_it_markup_type'
        db.add_column(u'museums_museum', 'mobidat_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.day_label_fr'
        db.add_column(u'museums_specialopeningtime', 'day_label_fr',
                      self.gf('django.db.models.fields.CharField')(u'Day label', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.day_label_pl'
        db.add_column(u'museums_specialopeningtime', 'day_label_pl',
                      self.gf('django.db.models.fields.CharField')(u'Day label', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.day_label_tr'
        db.add_column(u'museums_specialopeningtime', 'day_label_tr',
                      self.gf('django.db.models.fields.CharField')(u'Day label', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.day_label_es'
        db.add_column(u'museums_specialopeningtime', 'day_label_es',
                      self.gf('django.db.models.fields.CharField')(u'Day label', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.day_label_it'
        db.add_column(u'museums_specialopeningtime', 'day_label_it',
                      self.gf('django.db.models.fields.CharField')(u'Day label', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.exceptions_fr'
        db.add_column(u'museums_specialopeningtime', 'exceptions_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Exceptions for working hours', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.exceptions_fr_markup_type'
        db.add_column(u'museums_specialopeningtime', 'exceptions_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.exceptions_pl'
        db.add_column(u'museums_specialopeningtime', 'exceptions_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Exceptions for working hours', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.exceptions_pl_markup_type'
        db.add_column(u'museums_specialopeningtime', 'exceptions_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.exceptions_tr'
        db.add_column(u'museums_specialopeningtime', 'exceptions_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Exceptions for working hours', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.exceptions_tr_markup_type'
        db.add_column(u'museums_specialopeningtime', 'exceptions_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.exceptions_es'
        db.add_column(u'museums_specialopeningtime', 'exceptions_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Exceptions for working hours', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.exceptions_es_markup_type'
        db.add_column(u'museums_specialopeningtime', 'exceptions_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.exceptions_it'
        db.add_column(u'museums_specialopeningtime', 'exceptions_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Exceptions for working hours', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'SpecialOpeningTime.exceptions_it_markup_type'
        db.add_column(u'museums_specialopeningtime', 'exceptions_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'AccessibilityOption.title_fr'
        db.add_column(u'museums_accessibilityoption', 'title_fr',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'AccessibilityOption.title_pl'
        db.add_column(u'museums_accessibilityoption', 'title_pl',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'AccessibilityOption.title_tr'
        db.add_column(u'museums_accessibilityoption', 'title_tr',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'AccessibilityOption.title_es'
        db.add_column(u'museums_accessibilityoption', 'title_es',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'AccessibilityOption.title_it'
        db.add_column(u'museums_accessibilityoption', 'title_it',
                      self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Season.title_fr'
        db.add_column(u'museums_season', 'title_fr',
                      self.gf('django.db.models.fields.CharField')(u'Season title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Season.title_pl'
        db.add_column(u'museums_season', 'title_pl',
                      self.gf('django.db.models.fields.CharField')(u'Season title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Season.title_tr'
        db.add_column(u'museums_season', 'title_tr',
                      self.gf('django.db.models.fields.CharField')(u'Season title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Season.title_es'
        db.add_column(u'museums_season', 'title_es',
                      self.gf('django.db.models.fields.CharField')(u'Season title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Season.title_it'
        db.add_column(u'museums_season', 'title_it',
                      self.gf('django.db.models.fields.CharField')(u'Season title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Season.last_entry_fr'
        db.add_column(u'museums_season', 'last_entry_fr',
                      self.gf('django.db.models.fields.CharField')(u'Last entry', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Season.last_entry_pl'
        db.add_column(u'museums_season', 'last_entry_pl',
                      self.gf('django.db.models.fields.CharField')(u'Last entry', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Season.last_entry_tr'
        db.add_column(u'museums_season', 'last_entry_tr',
                      self.gf('django.db.models.fields.CharField')(u'Last entry', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Season.last_entry_es'
        db.add_column(u'museums_season', 'last_entry_es',
                      self.gf('django.db.models.fields.CharField')(u'Last entry', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Season.last_entry_it'
        db.add_column(u'museums_season', 'last_entry_it',
                      self.gf('django.db.models.fields.CharField')(u'Last entry', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Season.exceptions_fr'
        db.add_column(u'museums_season', 'exceptions_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Exceptions for working hours', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Season.exceptions_fr_markup_type'
        db.add_column(u'museums_season', 'exceptions_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Season.exceptions_pl'
        db.add_column(u'museums_season', 'exceptions_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Exceptions for working hours', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Season.exceptions_pl_markup_type'
        db.add_column(u'museums_season', 'exceptions_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Season.exceptions_tr'
        db.add_column(u'museums_season', 'exceptions_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Exceptions for working hours', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Season.exceptions_tr_markup_type'
        db.add_column(u'museums_season', 'exceptions_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Season.exceptions_es'
        db.add_column(u'museums_season', 'exceptions_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Exceptions for working hours', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Season.exceptions_es_markup_type'
        db.add_column(u'museums_season', 'exceptions_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Season.exceptions_it'
        db.add_column(u'museums_season', 'exceptions_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Exceptions for working hours', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Season.exceptions_it_markup_type'
        db.add_column(u'museums_season', 'exceptions_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

    
    
    def backwards(self, orm):
                # Deleting field 'MuseumCategory.title_fr'
        db.delete_column(u'museums_museumcategory', 'title_fr')

        # Deleting field 'MuseumCategory.title_pl'
        db.delete_column(u'museums_museumcategory', 'title_pl')

        # Deleting field 'MuseumCategory.title_tr'
        db.delete_column(u'museums_museumcategory', 'title_tr')

        # Deleting field 'MuseumCategory.title_es'
        db.delete_column(u'museums_museumcategory', 'title_es')

        # Deleting field 'MuseumCategory.title_it'
        db.delete_column(u'museums_museumcategory', 'title_it')

        # Deleting field 'Museum.reduced_price_info_fr'
        db.delete_column(u'museums_museum', 'reduced_price_info_fr')

        # Deleting field 'Museum.reduced_price_info_fr_markup_type'
        db.delete_column(u'museums_museum', 'reduced_price_info_fr_markup_type')

        # Deleting field 'Museum.reduced_price_info_pl'
        db.delete_column(u'museums_museum', 'reduced_price_info_pl')

        # Deleting field 'Museum.reduced_price_info_pl_markup_type'
        db.delete_column(u'museums_museum', 'reduced_price_info_pl_markup_type')

        # Deleting field 'Museum.reduced_price_info_tr'
        db.delete_column(u'museums_museum', 'reduced_price_info_tr')

        # Deleting field 'Museum.reduced_price_info_tr_markup_type'
        db.delete_column(u'museums_museum', 'reduced_price_info_tr_markup_type')

        # Deleting field 'Museum.reduced_price_info_es'
        db.delete_column(u'museums_museum', 'reduced_price_info_es')

        # Deleting field 'Museum.reduced_price_info_es_markup_type'
        db.delete_column(u'museums_museum', 'reduced_price_info_es_markup_type')

        # Deleting field 'Museum.reduced_price_info_it'
        db.delete_column(u'museums_museum', 'reduced_price_info_it')

        # Deleting field 'Museum.reduced_price_info_it_markup_type'
        db.delete_column(u'museums_museum', 'reduced_price_info_it_markup_type')

        # Deleting field 'Museum.group_ticket_fr'
        db.delete_column(u'museums_museum', 'group_ticket_fr')

        # Deleting field 'Museum.group_ticket_fr_markup_type'
        db.delete_column(u'museums_museum', 'group_ticket_fr_markup_type')

        # Deleting field 'Museum.group_ticket_pl'
        db.delete_column(u'museums_museum', 'group_ticket_pl')

        # Deleting field 'Museum.group_ticket_pl_markup_type'
        db.delete_column(u'museums_museum', 'group_ticket_pl_markup_type')

        # Deleting field 'Museum.group_ticket_tr'
        db.delete_column(u'museums_museum', 'group_ticket_tr')

        # Deleting field 'Museum.group_ticket_tr_markup_type'
        db.delete_column(u'museums_museum', 'group_ticket_tr_markup_type')

        # Deleting field 'Museum.group_ticket_es'
        db.delete_column(u'museums_museum', 'group_ticket_es')

        # Deleting field 'Museum.group_ticket_es_markup_type'
        db.delete_column(u'museums_museum', 'group_ticket_es_markup_type')

        # Deleting field 'Museum.group_ticket_it'
        db.delete_column(u'museums_museum', 'group_ticket_it')

        # Deleting field 'Museum.group_ticket_it_markup_type'
        db.delete_column(u'museums_museum', 'group_ticket_it_markup_type')

        # Deleting field 'Museum.title_fr'
        db.delete_column(u'museums_museum', 'title_fr')

        # Deleting field 'Museum.title_pl'
        db.delete_column(u'museums_museum', 'title_pl')

        # Deleting field 'Museum.title_tr'
        db.delete_column(u'museums_museum', 'title_tr')

        # Deleting field 'Museum.title_es'
        db.delete_column(u'museums_museum', 'title_es')

        # Deleting field 'Museum.title_it'
        db.delete_column(u'museums_museum', 'title_it')

        # Deleting field 'Museum.admission_price_info_fr'
        db.delete_column(u'museums_museum', 'admission_price_info_fr')

        # Deleting field 'Museum.admission_price_info_fr_markup_type'
        db.delete_column(u'museums_museum', 'admission_price_info_fr_markup_type')

        # Deleting field 'Museum.admission_price_info_pl'
        db.delete_column(u'museums_museum', 'admission_price_info_pl')

        # Deleting field 'Museum.admission_price_info_pl_markup_type'
        db.delete_column(u'museums_museum', 'admission_price_info_pl_markup_type')

        # Deleting field 'Museum.admission_price_info_tr'
        db.delete_column(u'museums_museum', 'admission_price_info_tr')

        # Deleting field 'Museum.admission_price_info_tr_markup_type'
        db.delete_column(u'museums_museum', 'admission_price_info_tr_markup_type')

        # Deleting field 'Museum.admission_price_info_es'
        db.delete_column(u'museums_museum', 'admission_price_info_es')

        # Deleting field 'Museum.admission_price_info_es_markup_type'
        db.delete_column(u'museums_museum', 'admission_price_info_es_markup_type')

        # Deleting field 'Museum.admission_price_info_it'
        db.delete_column(u'museums_museum', 'admission_price_info_it')

        # Deleting field 'Museum.admission_price_info_it_markup_type'
        db.delete_column(u'museums_museum', 'admission_price_info_it_markup_type')

        # Deleting field 'Museum.description_fr'
        db.delete_column(u'museums_museum', 'description_fr')

        # Deleting field 'Museum.description_fr_markup_type'
        db.delete_column(u'museums_museum', 'description_fr_markup_type')

        # Deleting field 'Museum.description_pl'
        db.delete_column(u'museums_museum', 'description_pl')

        # Deleting field 'Museum.description_pl_markup_type'
        db.delete_column(u'museums_museum', 'description_pl_markup_type')

        # Deleting field 'Museum.description_tr'
        db.delete_column(u'museums_museum', 'description_tr')

        # Deleting field 'Museum.description_tr_markup_type'
        db.delete_column(u'museums_museum', 'description_tr_markup_type')

        # Deleting field 'Museum.description_es'
        db.delete_column(u'museums_museum', 'description_es')

        # Deleting field 'Museum.description_es_markup_type'
        db.delete_column(u'museums_museum', 'description_es_markup_type')

        # Deleting field 'Museum.description_it'
        db.delete_column(u'museums_museum', 'description_it')

        # Deleting field 'Museum.description_it_markup_type'
        db.delete_column(u'museums_museum', 'description_it_markup_type')

        # Deleting field 'Museum.subtitle_fr'
        db.delete_column(u'museums_museum', 'subtitle_fr')

        # Deleting field 'Museum.subtitle_pl'
        db.delete_column(u'museums_museum', 'subtitle_pl')

        # Deleting field 'Museum.subtitle_tr'
        db.delete_column(u'museums_museum', 'subtitle_tr')

        # Deleting field 'Museum.subtitle_es'
        db.delete_column(u'museums_museum', 'subtitle_es')

        # Deleting field 'Museum.subtitle_it'
        db.delete_column(u'museums_museum', 'subtitle_it')

        # Deleting field 'Museum.accessibility_fr'
        db.delete_column(u'museums_museum', 'accessibility_fr')

        # Deleting field 'Museum.accessibility_fr_markup_type'
        db.delete_column(u'museums_museum', 'accessibility_fr_markup_type')

        # Deleting field 'Museum.accessibility_pl'
        db.delete_column(u'museums_museum', 'accessibility_pl')

        # Deleting field 'Museum.accessibility_pl_markup_type'
        db.delete_column(u'museums_museum', 'accessibility_pl_markup_type')

        # Deleting field 'Museum.accessibility_tr'
        db.delete_column(u'museums_museum', 'accessibility_tr')

        # Deleting field 'Museum.accessibility_tr_markup_type'
        db.delete_column(u'museums_museum', 'accessibility_tr_markup_type')

        # Deleting field 'Museum.accessibility_es'
        db.delete_column(u'museums_museum', 'accessibility_es')

        # Deleting field 'Museum.accessibility_es_markup_type'
        db.delete_column(u'museums_museum', 'accessibility_es_markup_type')

        # Deleting field 'Museum.accessibility_it'
        db.delete_column(u'museums_museum', 'accessibility_it')

        # Deleting field 'Museum.accessibility_it_markup_type'
        db.delete_column(u'museums_museum', 'accessibility_it_markup_type')

        # Deleting field 'Museum.image_caption_fr'
        db.delete_column(u'museums_museum', 'image_caption_fr')

        # Deleting field 'Museum.image_caption_fr_markup_type'
        db.delete_column(u'museums_museum', 'image_caption_fr_markup_type')

        # Deleting field 'Museum.image_caption_pl'
        db.delete_column(u'museums_museum', 'image_caption_pl')

        # Deleting field 'Museum.image_caption_pl_markup_type'
        db.delete_column(u'museums_museum', 'image_caption_pl_markup_type')

        # Deleting field 'Museum.image_caption_tr'
        db.delete_column(u'museums_museum', 'image_caption_tr')

        # Deleting field 'Museum.image_caption_tr_markup_type'
        db.delete_column(u'museums_museum', 'image_caption_tr_markup_type')

        # Deleting field 'Museum.image_caption_es'
        db.delete_column(u'museums_museum', 'image_caption_es')

        # Deleting field 'Museum.image_caption_es_markup_type'
        db.delete_column(u'museums_museum', 'image_caption_es_markup_type')

        # Deleting field 'Museum.image_caption_it'
        db.delete_column(u'museums_museum', 'image_caption_it')

        # Deleting field 'Museum.image_caption_it_markup_type'
        db.delete_column(u'museums_museum', 'image_caption_it_markup_type')

        # Deleting field 'Museum.mobidat_fr'
        db.delete_column(u'museums_museum', 'mobidat_fr')

        # Deleting field 'Museum.mobidat_fr_markup_type'
        db.delete_column(u'museums_museum', 'mobidat_fr_markup_type')

        # Deleting field 'Museum.mobidat_pl'
        db.delete_column(u'museums_museum', 'mobidat_pl')

        # Deleting field 'Museum.mobidat_pl_markup_type'
        db.delete_column(u'museums_museum', 'mobidat_pl_markup_type')

        # Deleting field 'Museum.mobidat_tr'
        db.delete_column(u'museums_museum', 'mobidat_tr')

        # Deleting field 'Museum.mobidat_tr_markup_type'
        db.delete_column(u'museums_museum', 'mobidat_tr_markup_type')

        # Deleting field 'Museum.mobidat_es'
        db.delete_column(u'museums_museum', 'mobidat_es')

        # Deleting field 'Museum.mobidat_es_markup_type'
        db.delete_column(u'museums_museum', 'mobidat_es_markup_type')

        # Deleting field 'Museum.mobidat_it'
        db.delete_column(u'museums_museum', 'mobidat_it')

        # Deleting field 'Museum.mobidat_it_markup_type'
        db.delete_column(u'museums_museum', 'mobidat_it_markup_type')

        # Deleting field 'SpecialOpeningTime.day_label_fr'
        db.delete_column(u'museums_specialopeningtime', 'day_label_fr')

        # Deleting field 'SpecialOpeningTime.day_label_pl'
        db.delete_column(u'museums_specialopeningtime', 'day_label_pl')

        # Deleting field 'SpecialOpeningTime.day_label_tr'
        db.delete_column(u'museums_specialopeningtime', 'day_label_tr')

        # Deleting field 'SpecialOpeningTime.day_label_es'
        db.delete_column(u'museums_specialopeningtime', 'day_label_es')

        # Deleting field 'SpecialOpeningTime.day_label_it'
        db.delete_column(u'museums_specialopeningtime', 'day_label_it')

        # Deleting field 'SpecialOpeningTime.exceptions_fr'
        db.delete_column(u'museums_specialopeningtime', 'exceptions_fr')

        # Deleting field 'SpecialOpeningTime.exceptions_fr_markup_type'
        db.delete_column(u'museums_specialopeningtime', 'exceptions_fr_markup_type')

        # Deleting field 'SpecialOpeningTime.exceptions_pl'
        db.delete_column(u'museums_specialopeningtime', 'exceptions_pl')

        # Deleting field 'SpecialOpeningTime.exceptions_pl_markup_type'
        db.delete_column(u'museums_specialopeningtime', 'exceptions_pl_markup_type')

        # Deleting field 'SpecialOpeningTime.exceptions_tr'
        db.delete_column(u'museums_specialopeningtime', 'exceptions_tr')

        # Deleting field 'SpecialOpeningTime.exceptions_tr_markup_type'
        db.delete_column(u'museums_specialopeningtime', 'exceptions_tr_markup_type')

        # Deleting field 'SpecialOpeningTime.exceptions_es'
        db.delete_column(u'museums_specialopeningtime', 'exceptions_es')

        # Deleting field 'SpecialOpeningTime.exceptions_es_markup_type'
        db.delete_column(u'museums_specialopeningtime', 'exceptions_es_markup_type')

        # Deleting field 'SpecialOpeningTime.exceptions_it'
        db.delete_column(u'museums_specialopeningtime', 'exceptions_it')

        # Deleting field 'SpecialOpeningTime.exceptions_it_markup_type'
        db.delete_column(u'museums_specialopeningtime', 'exceptions_it_markup_type')

        # Deleting field 'AccessibilityOption.title_fr'
        db.delete_column(u'museums_accessibilityoption', 'title_fr')

        # Deleting field 'AccessibilityOption.title_pl'
        db.delete_column(u'museums_accessibilityoption', 'title_pl')

        # Deleting field 'AccessibilityOption.title_tr'
        db.delete_column(u'museums_accessibilityoption', 'title_tr')

        # Deleting field 'AccessibilityOption.title_es'
        db.delete_column(u'museums_accessibilityoption', 'title_es')

        # Deleting field 'AccessibilityOption.title_it'
        db.delete_column(u'museums_accessibilityoption', 'title_it')

        # Deleting field 'Season.title_fr'
        db.delete_column(u'museums_season', 'title_fr')

        # Deleting field 'Season.title_pl'
        db.delete_column(u'museums_season', 'title_pl')

        # Deleting field 'Season.title_tr'
        db.delete_column(u'museums_season', 'title_tr')

        # Deleting field 'Season.title_es'
        db.delete_column(u'museums_season', 'title_es')

        # Deleting field 'Season.title_it'
        db.delete_column(u'museums_season', 'title_it')

        # Deleting field 'Season.last_entry_fr'
        db.delete_column(u'museums_season', 'last_entry_fr')

        # Deleting field 'Season.last_entry_pl'
        db.delete_column(u'museums_season', 'last_entry_pl')

        # Deleting field 'Season.last_entry_tr'
        db.delete_column(u'museums_season', 'last_entry_tr')

        # Deleting field 'Season.last_entry_es'
        db.delete_column(u'museums_season', 'last_entry_es')

        # Deleting field 'Season.last_entry_it'
        db.delete_column(u'museums_season', 'last_entry_it')

        # Deleting field 'Season.exceptions_fr'
        db.delete_column(u'museums_season', 'exceptions_fr')

        # Deleting field 'Season.exceptions_fr_markup_type'
        db.delete_column(u'museums_season', 'exceptions_fr_markup_type')

        # Deleting field 'Season.exceptions_pl'
        db.delete_column(u'museums_season', 'exceptions_pl')

        # Deleting field 'Season.exceptions_pl_markup_type'
        db.delete_column(u'museums_season', 'exceptions_pl_markup_type')

        # Deleting field 'Season.exceptions_tr'
        db.delete_column(u'museums_season', 'exceptions_tr')

        # Deleting field 'Season.exceptions_tr_markup_type'
        db.delete_column(u'museums_season', 'exceptions_tr_markup_type')

        # Deleting field 'Season.exceptions_es'
        db.delete_column(u'museums_season', 'exceptions_es')

        # Deleting field 'Season.exceptions_es_markup_type'
        db.delete_column(u'museums_season', 'exceptions_es_markup_type')

        # Deleting field 'Season.exceptions_it'
        db.delete_column(u'museums_season', 'exceptions_it')

        # Deleting field 'Season.exceptions_it_markup_type'
        db.delete_column(u'museums_season', 'exceptions_it_markup_type')

    
    
    models = {
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'museums.accessibilityoption': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'AccessibilityOption'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'accessibility/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_es': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_fr': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_it': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_pl': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_tr': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'museums.mediafile': {
            'Meta': {'ordering': "['sort_order', 'creation_date']", 'object_name': 'MediaFile'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'museum': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['museums.Museum']"}),
            'path': ('filebrowser.fields.FileBrowseField', [], {'directory': "'museums/'", 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'})
        },
        u'museums.museum': {
            'Meta': {'ordering': "['title']", 'object_name': 'Museum'},
            'accessibility': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'accessibility_de': ('base_libs.models.fields.ExtendedTextField', ["u'Accessibility'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'accessibility_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'accessibility_en': ('base_libs.models.fields.ExtendedTextField', ["u'Accessibility'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'accessibility_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'accessibility_es': ('base_libs.models.fields.ExtendedTextField', ["u'Accessibility'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'accessibility_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'accessibility_fr': ('base_libs.models.fields.ExtendedTextField', ["u'Accessibility'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'accessibility_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'accessibility_it': ('base_libs.models.fields.ExtendedTextField', ["u'Accessibility'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'accessibility_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'accessibility_options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['museums.AccessibilityOption']", 'symmetrical': 'False', 'blank': 'True'}),
            'accessibility_pl': ('base_libs.models.fields.ExtendedTextField', ["u'Accessibility'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'accessibility_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'accessibility_tr': ('base_libs.models.fields.ExtendedTextField', ["u'Accessibility'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'accessibility_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'admission_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'admission_price_info': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'admission_price_info_de': ('base_libs.models.fields.ExtendedTextField', ["u'Admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'admission_price_info_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'admission_price_info_en': ('base_libs.models.fields.ExtendedTextField', ["u'Admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'admission_price_info_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'admission_price_info_es': ('base_libs.models.fields.ExtendedTextField', ["u'Admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'admission_price_info_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'admission_price_info_fr': ('base_libs.models.fields.ExtendedTextField', ["u'Admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'admission_price_info_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'admission_price_info_it': ('base_libs.models.fields.ExtendedTextField', ["u'Admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'admission_price_info_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'admission_price_info_pl': ('base_libs.models.fields.ExtendedTextField', ["u'Admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'admission_price_info_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'admission_price_info_tr': ('base_libs.models.fields.ExtendedTextField', ["u'Admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'admission_price_info_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'audioguide_other_languages': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'categories': ('mptt.fields.TreeManyToManyField', [], {'to': u"orm['museums.MuseumCategory']", 'symmetrical': 'False'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'Berlin'", 'max_length': '255'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'de'", 'max_length': '255'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_es': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_fr': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_it': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_pl': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_tr': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'fax_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'fax_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'fax_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'free_entrance': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group_bookings_phone_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'group_bookings_phone_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'group_bookings_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'group_ticket': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'group_ticket_de': ('base_libs.models.fields.ExtendedTextField', ["u'Group ticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'group_ticket_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'group_ticket_en': ('base_libs.models.fields.ExtendedTextField', ["u'Group ticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'group_ticket_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'group_ticket_es': ('base_libs.models.fields.ExtendedTextField', ["u'Group ticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'group_ticket_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'group_ticket_fr': ('base_libs.models.fields.ExtendedTextField', ["u'Group ticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'group_ticket_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'group_ticket_it': ('base_libs.models.fields.ExtendedTextField', ["u'Group ticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'group_ticket_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'group_ticket_pl': ('base_libs.models.fields.ExtendedTextField', ["u'Group ticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'group_ticket_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'group_ticket_tr': ('base_libs.models.fields.ExtendedTextField', ["u'Group ticket'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'group_ticket_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'has_audioguide': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_de': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_en': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_for_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_for_learning_difficulties': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_fr': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_it': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_pl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_sp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_audioguide_tr': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'museums/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'image_caption': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_caption_de': ('base_libs.models.fields.ExtendedTextField', ["u'Image Caption'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '255', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_caption_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_caption_en': ('base_libs.models.fields.ExtendedTextField', ["u'Image Caption'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '255', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_caption_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_caption_es': ('base_libs.models.fields.ExtendedTextField', ["u'Image Caption'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '255', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_caption_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_caption_fr': ('base_libs.models.fields.ExtendedTextField', ["u'Image Caption'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '255', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_caption_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_caption_it': ('base_libs.models.fields.ExtendedTextField', ["u'Image Caption'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '255', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_caption_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_caption_pl': ('base_libs.models.fields.ExtendedTextField', ["u'Image Caption'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '255', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_caption_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_caption_tr': ('base_libs.models.fields.ExtendedTextField', ["u'Image Caption'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '255', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_caption_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'is_for_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'member_of_museumspass': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mobidat': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'mobidat_de': ('base_libs.models.fields.ExtendedTextField', ["u'Mobidat'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'mobidat_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'mobidat_en': ('base_libs.models.fields.ExtendedTextField', ["u'Mobidat'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'mobidat_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'mobidat_es': ('base_libs.models.fields.ExtendedTextField', ["u'Mobidat'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'mobidat_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'mobidat_fr': ('base_libs.models.fields.ExtendedTextField', ["u'Mobidat'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'mobidat_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'mobidat_it': ('base_libs.models.fields.ExtendedTextField', ["u'Mobidat'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'mobidat_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'mobidat_pl': ('base_libs.models.fields.ExtendedTextField', ["u'Mobidat'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'mobidat_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'mobidat_tr': ('base_libs.models.fields.ExtendedTextField', ["u'Mobidat'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'mobidat_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'open_on_mondays': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['museums.Museum']", 'null': 'True', 'blank': 'True'}),
            'phone_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'phone_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'reduced_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'reduced_price_info': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'reduced_price_info_de': ('base_libs.models.fields.ExtendedTextField', ["u'Reduced admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reduced_price_info_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reduced_price_info_en': ('base_libs.models.fields.ExtendedTextField', ["u'Reduced admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reduced_price_info_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reduced_price_info_es': ('base_libs.models.fields.ExtendedTextField', ["u'Reduced admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reduced_price_info_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reduced_price_info_fr': ('base_libs.models.fields.ExtendedTextField', ["u'Reduced admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reduced_price_info_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reduced_price_info_it': ('base_libs.models.fields.ExtendedTextField', ["u'Reduced admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reduced_price_info_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reduced_price_info_pl': ('base_libs.models.fields.ExtendedTextField', ["u'Reduced admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reduced_price_info_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'reduced_price_info_tr': ('base_libs.models.fields.ExtendedTextField', ["u'Reduced admission price info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'reduced_price_info_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'service_archive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_cafe': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_diaper_changing_table': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_library': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_phone_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'service_phone_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'service_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'service_restaurant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'service_shop': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_family_ticket': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_group_ticket': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_yearly_ticket': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '20', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'subtitle': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_en': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_es': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_fr': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_it': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_pl': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_tr': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tags': ('tagging_autocomplete.models.TagAutocompleteField', [], {'default': "''"}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_es': ('django.db.models.fields.CharField', ["u'Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_fr': ('django.db.models.fields.CharField', ["u'Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_it': ('django.db.models.fields.CharField', ["u'Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_pl': ('django.db.models.fields.CharField', ["u'Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_tr': ('django.db.models.fields.CharField', ["u'Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'website': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'museums.museumcategory': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'MuseumCategory'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['museums.MuseumCategory']", 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_es': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_fr': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_it': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_pl': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_tr': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'museums.season': {
            'Meta': {'ordering': "('start',)", 'object_name': 'Season'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'exceptions': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'exceptions_de': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_en': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_es': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_fr': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_it': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_pl': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_tr': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'fri_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_appointment_based': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_entry': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_entry_de': ('django.db.models.fields.CharField', ["u'Last entry'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'last_entry_en': ('django.db.models.fields.CharField', ["u'Last entry'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'last_entry_es': ('django.db.models.fields.CharField', ["u'Last entry'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'last_entry_fr': ('django.db.models.fields.CharField', ["u'Last entry'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'last_entry_it': ('django.db.models.fields.CharField', ["u'Last entry'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'last_entry_pl': ('django.db.models.fields.CharField', ["u'Last entry'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'last_entry_tr': ('django.db.models.fields.CharField', ["u'Last entry'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'mon_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'museum': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['museums.Museum']"}),
            'sat_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {}),
            'sun_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Season title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Season title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_es': ('django.db.models.fields.CharField', ["u'Season title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_fr': ('django.db.models.fields.CharField', ["u'Season title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_it': ('django.db.models.fields.CharField', ["u'Season title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_pl': ('django.db.models.fields.CharField', ["u'Season title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_tr': ('django.db.models.fields.CharField', ["u'Season title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tue_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'museums.socialmediachannel': {
            'Meta': {'ordering': "['channel_type']", 'object_name': 'SocialMediaChannel'},
            'channel_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'museum': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['museums.Museum']"}),
            'url': ('base_libs.models.fields.URLField', [], {'max_length': '255'})
        },
        u'museums.specialopeningtime': {
            'Meta': {'ordering': "('yyyy', 'mm', 'dd')", 'object_name': 'SpecialOpeningTime'},
            'break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'closing': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'day_label': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'day_label_de': ('django.db.models.fields.CharField', ["u'Day label'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'day_label_en': ('django.db.models.fields.CharField', ["u'Day label'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'day_label_es': ('django.db.models.fields.CharField', ["u'Day label'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'day_label_fr': ('django.db.models.fields.CharField', ["u'Day label'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'day_label_it': ('django.db.models.fields.CharField', ["u'Day label'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'day_label_pl': ('django.db.models.fields.CharField', ["u'Day label'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'day_label_tr': ('django.db.models.fields.CharField', ["u'Day label'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'dd': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'exceptions': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'exceptions_de': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_en': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_es': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_fr': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_it': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_pl': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_tr': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_regular': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mm': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'museum': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['museums.Museum']"}),
            'opening': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'yyyy': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'permissions.rowlevelpermission': {
            'Meta': {'object_name': 'RowLevelPermission', 'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': u"orm['contenttypes.ContentType']"}),
            'owner_object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Permission']"})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['museums']
