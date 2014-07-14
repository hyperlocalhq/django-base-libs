# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from ccb.apps.media_gallery.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields
from django.conf import settings

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'MediaFile.modifier'
        db.add_column('media_gallery_mediafile', 'modifier', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_modifier", null=True))
        
        # Adding field 'MediaSet.creator'
        db.add_column('media_gallery_mediaset', 'creator', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_creator", null=True))
        
        # Adding field 'MediaFile.creator'
        db.add_column('media_gallery_mediafile', 'creator', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_creator", null=True))
        
        # Adding field 'MediaSet.modifier'
        db.add_column('media_gallery_mediaset', 'modifier', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_modifier", null=True))
        
        for lang_code, lang_title in settings.LANGUAGES:
            # Changing fields 'MediaFile.description_*'
            db.alter_column('media_gallery_mediafile', 'description_%s' % lang_code, ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False))
        
            # Changing field 'MediaSet.description_*'
            db.alter_column('media_gallery_mediaset', 'description_%s' % lang_code, ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False))
        
            # Changing field 'MediaGallery.description_*'
            db.alter_column('media_gallery_mediagallery', 'description_%s' % lang_code, ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False))
        
        # Changing field 'MediaGallery.content_type'
        db.alter_column('media_gallery_mediagallery', 'content_type_id', models.ForeignKey(orm['contenttypes.ContentType'], null=False, blank=False))
    
    
    def backwards(self, orm):
        
        # Deleting field 'MediaFile.modifier'
        db.delete_column('media_gallery_mediafile', 'modifier_id')
        
        # Deleting field 'MediaSet.creator'
        db.delete_column('media_gallery_mediaset', 'creator_id')
        
        # Deleting field 'MediaFile.creator'
        db.delete_column('media_gallery_mediafile', 'creator_id')
        
        # Deleting field 'MediaSet.modifier'
        db.delete_column('media_gallery_mediaset', 'modifier_id')
        
        for lang_code, lang_title in settings.LANGUAGES:
            # Changing field 'MediaFile.description_*'
            db.alter_column('media_gallery_mediafile', 'description_%s' % lang_code, ExtendedTextField(u'Description', unique_for_month=None, null=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        
            # Changing field 'MediaSet.description_*'
            db.alter_column('media_gallery_mediaset', 'description_%s' % lang_code, ExtendedTextField(u'Description', unique_for_month=None, null=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        
            # Changing field 'MediaGallery.description_*'
            db.alter_column('media_gallery_mediagallery', 'description_%s' % lang_code, ExtendedTextField(u'Description', unique_for_month=None, null=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        
        # Changing field 'MediaGallery.content_type'
        db.alter_column('media_gallery_mediagallery', 'content_type_id', models.ForeignKey(orm['contenttypes.ContentType'], limit_choices_to={}, null=False, blank=False))
    
    models = {
        'media_gallery.mediafile': {
            'Meta': {'ordering': '["sort_order","creation_date"]'},
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_creator"', 'null': 'True'}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'external_url': ('URLField', ["_('External URL')"], {'blank': 'True'}),
            'file_type': ('models.CharField', [], {'default': "'-'", 'max_length': '1', 'editable': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'media_set': ('models.ForeignKey', ["orm['media_gallery.MediaSet']"], {}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_modifier"', 'null': 'True'}),
            'path': ('FileBrowseField', ["_('File path')"], {'max_length': '255', 'blank': 'True'}),
            'sort_order': ('models.IntegerField', ['_("Sort order")'], {'blank': 'True'}),
            'splash_image_path': ('FileBrowseField', ["_('Splash-image path')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '255', 'blank': 'True'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '255', 'blank': 'True'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'media_gallery.mediaset': {
            'Meta': {'ordering': '["creation_date"]'},
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_creator"', 'null': 'True'}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('models.BooleanField', ['_("Featured")'], {'default': 'False'}),
            'media_gallery': ('models.ForeignKey', ["orm['media_gallery.MediaGallery']"], {}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_modifier"', 'null': 'True'}),
            'slug': ('models.SlugField', [], {'default': "'default'", 'unique': 'False', 'max_length': '255'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '100', 'blank': 'True'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'views': ('models.IntegerField', ['_("views")'], {'default': '0', 'editable': 'False'})
        },
        'media_gallery.mediagallery': {
            'Meta': {'ordering': "['-creation_date']", 'get_latest_by': "'creation_date'"},
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '100', 'blank': 'True'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['media_gallery']
