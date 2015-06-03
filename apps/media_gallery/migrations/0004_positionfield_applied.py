# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.media_gallery.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        '''
        # Changing field 'MediaFile.modified_date'
        # (to signature: django.db.models.fields.DateTimeField(null=True))
        db.alter_column('media_gallery_mediafile', 'modified_date', orm['media_gallery.mediafile:modified_date'])
        
        # Changing field 'MediaFile.creator'
        # (to signature: django.db.models.fields.related.ForeignKey(null=True, to=orm['auth.User']))
        db.alter_column('media_gallery_mediafile', 'creator_id', orm['media_gallery.mediafile:creator'])
        
        # Changing field 'MediaFile.file_type'
        # (to signature: django.db.models.fields.CharField(default='-', max_length=1))
        db.alter_column('media_gallery_mediafile', 'file_type', orm['media_gallery.mediafile:file_type'])
        
        # Changing field 'MediaFile.description_en'
        # (to signature: ExtendedTextField(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False))
        db.alter_column('media_gallery_mediafile', 'description_en', orm['media_gallery.mediafile:description_en'])
        
        # Changing field 'MediaFile.creation_date'
        # (to signature: django.db.models.fields.DateTimeField())
        db.alter_column('media_gallery_mediafile', 'creation_date', orm['media_gallery.mediafile:creation_date'])
        
        # Changing field 'MediaFile.media_set'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['media_gallery.MediaSet']))
        db.alter_column('media_gallery_mediafile', 'media_set_id', orm['media_gallery.mediafile:media_set'])
        
        # Changing field 'MediaFile.description_de'
        # (to signature: ExtendedTextField(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False))
        db.alter_column('media_gallery_mediafile', 'description_de', orm['media_gallery.mediafile:description_de'])
        
        # Changing field 'MediaFile.modifier'
        # (to signature: django.db.models.fields.related.ForeignKey(null=True, to=orm['auth.User']))
        db.alter_column('media_gallery_mediafile', 'modifier_id', orm['media_gallery.mediafile:modifier'])
        
        # Changing field 'MediaSet.modified_date'
        # (to signature: django.db.models.fields.DateTimeField(null=True))
        db.alter_column('media_gallery_mediaset', 'modified_date', orm['media_gallery.mediaset:modified_date'])
        
        # Changing field 'MediaSet.is_featured'
        # (to signature: django.db.models.fields.BooleanField(default=False, blank=True))
        db.alter_column('media_gallery_mediaset', 'is_featured', orm['media_gallery.mediaset:is_featured'])
        
        # Changing field 'MediaSet.creator'
        # (to signature: django.db.models.fields.related.ForeignKey(null=True, to=orm['auth.User']))
        db.alter_column('media_gallery_mediaset', 'creator_id', orm['media_gallery.mediaset:creator'])
        
        # Changing field 'MediaSet.views'
        # (to signature: django.db.models.fields.IntegerField(default=0))
        db.alter_column('media_gallery_mediaset', 'views', orm['media_gallery.mediaset:views'])
        
        # Changing field 'MediaSet.description_en'
        # (to signature: ExtendedTextField(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False))
        db.alter_column('media_gallery_mediaset', 'description_en', orm['media_gallery.mediaset:description_en'])
        
        # Changing field 'MediaSet.creation_date'
        # (to signature: django.db.models.fields.DateTimeField())
        db.alter_column('media_gallery_mediaset', 'creation_date', orm['media_gallery.mediaset:creation_date'])
        
        # Changing field 'MediaSet.media_gallery'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['media_gallery.MediaGallery']))
        db.alter_column('media_gallery_mediaset', 'media_gallery_id', orm['media_gallery.mediaset:media_gallery'])
        
        # Changing field 'MediaSet.description_de'
        # (to signature: ExtendedTextField(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False))
        db.alter_column('media_gallery_mediaset', 'description_de', orm['media_gallery.mediaset:description_de'])
        
        # Changing field 'MediaSet.modifier'
        # (to signature: django.db.models.fields.related.ForeignKey(null=True, to=orm['auth.User']))
        db.alter_column('media_gallery_mediaset', 'modifier_id', orm['media_gallery.mediaset:modifier'])
        
        # Changing field 'MediaGallery.modified_date'
        # (to signature: django.db.models.fields.DateTimeField(null=True))
        db.alter_column('media_gallery_mediagallery', 'modified_date', orm['media_gallery.mediagallery:modified_date'])
        
        # Changing field 'MediaGallery.description_en'
        # (to signature: ExtendedTextField(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False))
        db.alter_column('media_gallery_mediagallery', 'description_en', orm['media_gallery.mediagallery:description_en'])
        
        # Changing field 'MediaGallery.creation_date'
        # (to signature: django.db.models.fields.DateTimeField())
        db.alter_column('media_gallery_mediagallery', 'creation_date', orm['media_gallery.mediagallery:creation_date'])
        
        # Changing field 'MediaGallery.description_de'
        # (to signature: ExtendedTextField(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False))
        db.alter_column('media_gallery_mediagallery', 'description_de', orm['media_gallery.mediagallery:description_de'])
        '''
        # Changing field 'MediaFile.sort_order'
        # (to signature: PositionField(_("Sort order")))
        db.alter_column('media_gallery_mediafile', 'sort_order', orm['media_gallery.mediafile:sort_order'])
    
    
    def backwards(self, orm):
        '''
        # Changing field 'MediaFile.modified_date'
        # (to signature: models.DateTimeField(_("modified date"), null=True, editable=False))
        db.alter_column('media_gallery_mediafile', 'modified_date', orm['media_gallery.mediafile:modified_date'])
        
        # Changing field 'MediaFile.creator'
        # (to signature: models.ForeignKey(orm['auth.User'], null=True, editable=False))
        db.alter_column('media_gallery_mediafile', 'creator_id', orm['media_gallery.mediafile:creator'])
        
        # Changing field 'MediaFile.file_type'
        # (to signature: models.CharField(default='-', max_length=1, editable=False))
        db.alter_column('media_gallery_mediafile', 'file_type', orm['media_gallery.mediafile:file_type'])
        
        # Changing field 'MediaFile.description_en'
        # (to signature: ExtendedTextField(u'Description', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        db.alter_column('media_gallery_mediafile', 'description_en', orm['media_gallery.mediafile:description_en'])
        
        # Changing field 'MediaFile.creation_date'
        # (to signature: models.DateTimeField(_("creation date"), editable=False))
        db.alter_column('media_gallery_mediafile', 'creation_date', orm['media_gallery.mediafile:creation_date'])
        
        # Changing field 'MediaFile.media_set'
        # (to signature: models.ForeignKey(orm['media_gallery.MediaSet']))
        db.alter_column('media_gallery_mediafile', 'media_set_id', orm['media_gallery.mediafile:media_set'])
        
        # Changing field 'MediaFile.description_de'
        # (to signature: ExtendedTextField(u'Description', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        db.alter_column('media_gallery_mediafile', 'description_de', orm['media_gallery.mediafile:description_de'])
        
        # Changing field 'MediaFile.modifier'
        # (to signature: models.ForeignKey(orm['auth.User'], null=True, editable=False))
        db.alter_column('media_gallery_mediafile', 'modifier_id', orm['media_gallery.mediafile:modifier'])
        
        # Changing field 'MediaSet.modified_date'
        # (to signature: models.DateTimeField(_("modified date"), null=True, editable=False))
        db.alter_column('media_gallery_mediaset', 'modified_date', orm['media_gallery.mediaset:modified_date'])
        
        # Changing field 'MediaSet.is_featured'
        # (to signature: models.BooleanField(_("Featured"), default=False))
        db.alter_column('media_gallery_mediaset', 'is_featured', orm['media_gallery.mediaset:is_featured'])
        
        # Changing field 'MediaSet.creator'
        # (to signature: models.ForeignKey(orm['auth.User'], null=True, editable=False))
        db.alter_column('media_gallery_mediaset', 'creator_id', orm['media_gallery.mediaset:creator'])
        
        # Changing field 'MediaSet.views'
        # (to signature: models.IntegerField(_("views"), default=0, editable=False))
        db.alter_column('media_gallery_mediaset', 'views', orm['media_gallery.mediaset:views'])
        
        # Changing field 'MediaSet.description_en'
        # (to signature: ExtendedTextField(u'Description', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        db.alter_column('media_gallery_mediaset', 'description_en', orm['media_gallery.mediaset:description_en'])
        
        # Changing field 'MediaSet.creation_date'
        # (to signature: models.DateTimeField(_("creation date"), editable=False))
        db.alter_column('media_gallery_mediaset', 'creation_date', orm['media_gallery.mediaset:creation_date'])
        
        # Changing field 'MediaSet.media_gallery'
        # (to signature: models.ForeignKey(orm['media_gallery.MediaGallery']))
        db.alter_column('media_gallery_mediaset', 'media_gallery_id', orm['media_gallery.mediaset:media_gallery'])
        
        # Changing field 'MediaSet.description_de'
        # (to signature: ExtendedTextField(u'Description', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        db.alter_column('media_gallery_mediaset', 'description_de', orm['media_gallery.mediaset:description_de'])
        
        # Changing field 'MediaSet.modifier'
        # (to signature: models.ForeignKey(orm['auth.User'], null=True, editable=False))
        db.alter_column('media_gallery_mediaset', 'modifier_id', orm['media_gallery.mediaset:modifier'])
        
        # Changing field 'MediaGallery.modified_date'
        # (to signature: models.DateTimeField(_("modified date"), null=True, editable=False))
        db.alter_column('media_gallery_mediagallery', 'modified_date', orm['media_gallery.mediagallery:modified_date'])
        
        # Changing field 'MediaGallery.description_en'
        # (to signature: ExtendedTextField(u'Description', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        db.alter_column('media_gallery_mediagallery', 'description_en', orm['media_gallery.mediagallery:description_en'])
        
        # Changing field 'MediaGallery.creation_date'
        # (to signature: models.DateTimeField(_("creation date"), editable=False))
        db.alter_column('media_gallery_mediagallery', 'creation_date', orm['media_gallery.mediagallery:creation_date'])
        
        # Changing field 'MediaGallery.description_de'
        # (to signature: ExtendedTextField(u'Description', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        db.alter_column('media_gallery_mediagallery', 'description_de', orm['media_gallery.mediagallery:description_de'])
        '''
        # Changing field 'MediaFile.sort_order'
        # (to signature: models.IntegerField(_("Sort order"), blank=True))
        db.alter_column('media_gallery_mediafile', 'sort_order', orm['media_gallery.mediafile:sort_order'])
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'row_level_permissions_owned': ('django.contrib.contenttypes.generic.GenericRelation', [], {'object_id_field': "'owner_object_id'", 'content_type_field': "'owner_content_type'", 'to': "orm['permissions.RowLevelPermission']"}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'media_gallery.mediafile': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediafile_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'external_url': ('URLField', ["_('External URL')"], {'blank': 'True'}),
            'file_type': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['media_gallery.MediaSet']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediafile_modifier'", 'null': 'True', 'to': "orm['auth.User']"}),
            'path': ('FileBrowseField', ["_('File path')"], {'max_length': '255', 'blank': 'True'}),
            'sort_order': ('PositionField', ['_("Sort order")'], {}),
            'splash_image_path': ('FileBrowseField', ["_('Splash-image path')"], {'max_length': '255', 'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'blank': 'True'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '255', 'blank': 'True'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'media_gallery.mediagallery': {
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '100', 'blank': 'True'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'media_gallery.mediaset': {
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediaset_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'media_gallery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['media_gallery.MediaGallery']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediaset_modifier'", 'null': 'True', 'to': "orm['auth.User']"}),
            'slug': ('models.SlugField', [], {'default': "'default'", 'unique': 'False', 'max_length': '255'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '100', 'blank': 'True'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'permissions.rowlevelpermission': {
            'Meta': {'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'owner_content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': "'owner'", 'null': 'False', 'blank': 'False'}),
            'owner_object_id': ('models.CharField', ["u'Owner'"], {'max_length': '255', 'null': 'False', 'blank': 'False'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Permission']"})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['media_gallery']
