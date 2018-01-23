# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
                # Deleting field 'Slide.title_markup_type'
        db.delete_column(u'slideshows_slide', 'title_markup_type')

        # Deleting field 'Slide.subtitle_markup_type'
        db.delete_column(u'slideshows_slide', 'subtitle_markup_type')

        # Adding field 'Slide.subtitle_fr'
        db.add_column(u'slideshows_slide', 'subtitle_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Subtitle', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Slide.subtitle_fr_markup_type'
        db.add_column(u'slideshows_slide', 'subtitle_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Slide.subtitle_pl'
        db.add_column(u'slideshows_slide', 'subtitle_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Subtitle', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Slide.subtitle_pl_markup_type'
        db.add_column(u'slideshows_slide', 'subtitle_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Slide.subtitle_tr'
        db.add_column(u'slideshows_slide', 'subtitle_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Subtitle', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Slide.subtitle_tr_markup_type'
        db.add_column(u'slideshows_slide', 'subtitle_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Slide.subtitle_es'
        db.add_column(u'slideshows_slide', 'subtitle_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Subtitle', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Slide.subtitle_es_markup_type'
        db.add_column(u'slideshows_slide', 'subtitle_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Slide.subtitle_it'
        db.add_column(u'slideshows_slide', 'subtitle_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Subtitle', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Slide.subtitle_it_markup_type'
        db.add_column(u'slideshows_slide', 'subtitle_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Slide.title_fr'
        db.add_column(u'slideshows_slide', 'title_fr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Title', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Slide.title_fr_markup_type'
        db.add_column(u'slideshows_slide', 'title_fr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Slide.title_pl'
        db.add_column(u'slideshows_slide', 'title_pl',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Title', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Slide.title_pl_markup_type'
        db.add_column(u'slideshows_slide', 'title_pl_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Slide.title_tr'
        db.add_column(u'slideshows_slide', 'title_tr',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Title', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Slide.title_tr_markup_type'
        db.add_column(u'slideshows_slide', 'title_tr_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Slide.title_es'
        db.add_column(u'slideshows_slide', 'title_es',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Title', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Slide.title_es_markup_type'
        db.add_column(u'slideshows_slide', 'title_es_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Slide.title_it'
        db.add_column(u'slideshows_slide', 'title_it',
                      self.gf('base_libs.models.fields.ExtendedTextField')(u'Title', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False),
                      keep_default=False)

        # Adding field 'Slide.title_it_markup_type'
        db.add_column(u'slideshows_slide', 'title_it_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Slide.credits_fr'
        db.add_column(u'slideshows_slide', 'credits_fr',
                      self.gf('django.db.models.fields.CharField')(u'Photo credits', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Slide.credits_pl'
        db.add_column(u'slideshows_slide', 'credits_pl',
                      self.gf('django.db.models.fields.CharField')(u'Photo credits', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Slide.credits_tr'
        db.add_column(u'slideshows_slide', 'credits_tr',
                      self.gf('django.db.models.fields.CharField')(u'Photo credits', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Slide.credits_es'
        db.add_column(u'slideshows_slide', 'credits_es',
                      self.gf('django.db.models.fields.CharField')(u'Photo credits', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Slide.credits_it'
        db.add_column(u'slideshows_slide', 'credits_it',
                      self.gf('django.db.models.fields.CharField')(u'Photo credits', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Slide.alt_fr'
        db.add_column(u'slideshows_slide', 'alt_fr',
                      self.gf('django.db.models.fields.CharField')(u'Alternative text', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Slide.alt_pl'
        db.add_column(u'slideshows_slide', 'alt_pl',
                      self.gf('django.db.models.fields.CharField')(u'Alternative text', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Slide.alt_tr'
        db.add_column(u'slideshows_slide', 'alt_tr',
                      self.gf('django.db.models.fields.CharField')(u'Alternative text', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Slide.alt_es'
        db.add_column(u'slideshows_slide', 'alt_es',
                      self.gf('django.db.models.fields.CharField')(u'Alternative text', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)

        # Adding field 'Slide.alt_it'
        db.add_column(u'slideshows_slide', 'alt_it',
                      self.gf('django.db.models.fields.CharField')(u'Alternative text', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False),
                      keep_default=False)


        # Changing field 'Slide.title_de'
        db.alter_column(u'slideshows_slide', 'title_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Title', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'Slide.subtitle_en'
        db.alter_column(u'slideshows_slide', 'subtitle_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Subtitle', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'Slide.title_en'
        db.alter_column(u'slideshows_slide', 'title_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Title', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'Slide.subtitle_de'
        db.alter_column(u'slideshows_slide', 'subtitle_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Subtitle', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))
    
    
    def backwards(self, orm):
                # Adding field 'Slide.title_markup_type'
        db.add_column(u'slideshows_slide', 'title_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Adding field 'Slide.subtitle_markup_type'
        db.add_column(u'slideshows_slide', 'subtitle_markup_type',
                      self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False),
                      keep_default=False)

        # Deleting field 'Slide.subtitle_fr'
        db.delete_column(u'slideshows_slide', 'subtitle_fr')

        # Deleting field 'Slide.subtitle_fr_markup_type'
        db.delete_column(u'slideshows_slide', 'subtitle_fr_markup_type')

        # Deleting field 'Slide.subtitle_pl'
        db.delete_column(u'slideshows_slide', 'subtitle_pl')

        # Deleting field 'Slide.subtitle_pl_markup_type'
        db.delete_column(u'slideshows_slide', 'subtitle_pl_markup_type')

        # Deleting field 'Slide.subtitle_tr'
        db.delete_column(u'slideshows_slide', 'subtitle_tr')

        # Deleting field 'Slide.subtitle_tr_markup_type'
        db.delete_column(u'slideshows_slide', 'subtitle_tr_markup_type')

        # Deleting field 'Slide.subtitle_es'
        db.delete_column(u'slideshows_slide', 'subtitle_es')

        # Deleting field 'Slide.subtitle_es_markup_type'
        db.delete_column(u'slideshows_slide', 'subtitle_es_markup_type')

        # Deleting field 'Slide.subtitle_it'
        db.delete_column(u'slideshows_slide', 'subtitle_it')

        # Deleting field 'Slide.subtitle_it_markup_type'
        db.delete_column(u'slideshows_slide', 'subtitle_it_markup_type')

        # Deleting field 'Slide.title_fr'
        db.delete_column(u'slideshows_slide', 'title_fr')

        # Deleting field 'Slide.title_fr_markup_type'
        db.delete_column(u'slideshows_slide', 'title_fr_markup_type')

        # Deleting field 'Slide.title_pl'
        db.delete_column(u'slideshows_slide', 'title_pl')

        # Deleting field 'Slide.title_pl_markup_type'
        db.delete_column(u'slideshows_slide', 'title_pl_markup_type')

        # Deleting field 'Slide.title_tr'
        db.delete_column(u'slideshows_slide', 'title_tr')

        # Deleting field 'Slide.title_tr_markup_type'
        db.delete_column(u'slideshows_slide', 'title_tr_markup_type')

        # Deleting field 'Slide.title_es'
        db.delete_column(u'slideshows_slide', 'title_es')

        # Deleting field 'Slide.title_es_markup_type'
        db.delete_column(u'slideshows_slide', 'title_es_markup_type')

        # Deleting field 'Slide.title_it'
        db.delete_column(u'slideshows_slide', 'title_it')

        # Deleting field 'Slide.title_it_markup_type'
        db.delete_column(u'slideshows_slide', 'title_it_markup_type')

        # Deleting field 'Slide.credits_fr'
        db.delete_column(u'slideshows_slide', 'credits_fr')

        # Deleting field 'Slide.credits_pl'
        db.delete_column(u'slideshows_slide', 'credits_pl')

        # Deleting field 'Slide.credits_tr'
        db.delete_column(u'slideshows_slide', 'credits_tr')

        # Deleting field 'Slide.credits_es'
        db.delete_column(u'slideshows_slide', 'credits_es')

        # Deleting field 'Slide.credits_it'
        db.delete_column(u'slideshows_slide', 'credits_it')

        # Deleting field 'Slide.alt_fr'
        db.delete_column(u'slideshows_slide', 'alt_fr')

        # Deleting field 'Slide.alt_pl'
        db.delete_column(u'slideshows_slide', 'alt_pl')

        # Deleting field 'Slide.alt_tr'
        db.delete_column(u'slideshows_slide', 'alt_tr')

        # Deleting field 'Slide.alt_es'
        db.delete_column(u'slideshows_slide', 'alt_es')

        # Deleting field 'Slide.alt_it'
        db.delete_column(u'slideshows_slide', 'alt_it')


        # Changing field 'Slide.title_de'
        db.alter_column(u'slideshows_slide', 'title_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Titel', rel=None, unique_for_year=None, unique_for_date=None, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace=''))

        # Changing field 'Slide.subtitle_en'
        db.alter_column(u'slideshows_slide', 'subtitle_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Untertitel', rel=None, unique_for_year=None, unique_for_date=None, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace=''))

        # Changing field 'Slide.title_en'
        db.alter_column(u'slideshows_slide', 'title_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Titel', rel=None, unique_for_year=None, unique_for_date=None, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace=''))

        # Changing field 'Slide.subtitle_de'
        db.alter_column(u'slideshows_slide', 'subtitle_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Untertitel', rel=None, unique_for_year=None, unique_for_date=None, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, db_tablespace=''))
    
    
    models = {
        u'slideshows.slide': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Slide'},
            'alt': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'alt_de': ('django.db.models.fields.CharField', ["u'Alternative text'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'alt_en': ('django.db.models.fields.CharField', ["u'Alternative text'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'alt_es': ('django.db.models.fields.CharField', ["u'Alternative text'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'alt_fr': ('django.db.models.fields.CharField', ["u'Alternative text'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'alt_it': ('django.db.models.fields.CharField', ["u'Alternative text'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'alt_pl': ('django.db.models.fields.CharField', ["u'Alternative text'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'alt_tr': ('django.db.models.fields.CharField', ["u'Alternative text'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'credits': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'credits_de': ('django.db.models.fields.CharField', ["u'Photo credits'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'credits_en': ('django.db.models.fields.CharField', ["u'Photo credits'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'credits_es': ('django.db.models.fields.CharField', ["u'Photo credits'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'credits_fr': ('django.db.models.fields.CharField', ["u'Photo credits'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'credits_it': ('django.db.models.fields.CharField', ["u'Photo credits'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'credits_pl': ('django.db.models.fields.CharField', ["u'Photo credits'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'credits_tr': ('django.db.models.fields.CharField', ["u'Photo credits'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'highlight': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'path': ('filebrowser.fields.FileBrowseField', [], {'directory': "'slideshows/'", 'max_length': '255', 'blank': 'True'}),
            'slideshow': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['slideshows.Slideshow']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'subtitle': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('base_libs.models.fields.ExtendedTextField', ["u'Subtitle'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'subtitle_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'subtitle_en': ('base_libs.models.fields.ExtendedTextField', ["u'Subtitle'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'subtitle_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'subtitle_es': ('base_libs.models.fields.ExtendedTextField', ["u'Subtitle'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'subtitle_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'subtitle_fr': ('base_libs.models.fields.ExtendedTextField', ["u'Subtitle'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'subtitle_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'subtitle_it': ('base_libs.models.fields.ExtendedTextField', ["u'Subtitle'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'subtitle_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'subtitle_pl': ('base_libs.models.fields.ExtendedTextField', ["u'Subtitle'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'subtitle_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'subtitle_tr': ('base_libs.models.fields.ExtendedTextField', ["u'Subtitle'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'subtitle_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'title_de': ('base_libs.models.fields.ExtendedTextField', ["u'Title'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'title_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title_en': ('base_libs.models.fields.ExtendedTextField', ["u'Title'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'title_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title_es': ('base_libs.models.fields.ExtendedTextField', ["u'Title'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'title_es_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title_fr': ('base_libs.models.fields.ExtendedTextField', ["u'Title'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'title_fr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title_it': ('base_libs.models.fields.ExtendedTextField', ["u'Title'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'title_it_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title_pl': ('base_libs.models.fields.ExtendedTextField', ["u'Title'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'title_pl_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'title_tr': ('base_libs.models.fields.ExtendedTextField', ["u'Title'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'title_tr_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'})
        },
        u'slideshows.slideshow': {
            'Meta': {'ordering': "['sysname']", 'object_name': 'Slideshow'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['slideshows']
