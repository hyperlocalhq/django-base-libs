# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.media_gallery.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        raise Warning, "skip old migrations by running:\npython manage.py migrate media_gallery 0010 --fake"
        # Adding model 'MediaFile'
        db.create_table('media_gallery_mediafile', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('media_set', models.ForeignKey(orm.MediaSet)),
            ('path', FileBrowseField(_('File path'), max_length=255, blank=True)),
            ('external_url', URLField(_('External URL'), blank=True)),
            ('splash_image_path', FileBrowseField(_('Splash-image path'), extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff'], max_length=255, blank=True)),
            ('file_type', models.CharField(default='-', max_length=1, editable=False)),
            ('title', MultilingualCharField(_("Title"), max_length=255, blank=True)),
            ('description', MultilingualTextField(_("Description"), blank=True)),
            ('sort_order', models.IntegerField(_("Sort order"), blank=True)),
            ('description_de', ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('description_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_en', ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('description_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('title_de', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal('media_gallery', ['MediaFile'])
        
        # Adding model 'MediaSet'
        db.create_table('media_gallery_mediaset', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('views', models.IntegerField(_("views"), default=0, editable=False)),
            ('slug', models.SlugField(default='default', unique=False, max_length=255)),
            ('media_gallery', models.ForeignKey(orm.MediaGallery)),
            ('title', MultilingualCharField(_("Title"), max_length=100, blank=True)),
            ('description', MultilingualTextField(_("Description"), blank=True)),
            ('is_featured', models.BooleanField(_("Featured"), default=False)),
            ('description_de', ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('description_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_en', ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('description_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('title_de', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal('media_gallery', ['MediaSet'])
        
        # Adding model 'MediaGallery'
        db.create_table('media_gallery_mediagallery', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], limit_choices_to={}, related_name=None, null=False, blank=False)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=False)),
            ('title', MultilingualCharField(_("Title"), max_length=100, blank=True)),
            ('description', MultilingualTextField(_("Description"), blank=True)),
            ('description_de', ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('description_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_en', ExtendedTextField(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=None, unique_for_year=None, rel=None, blank=True, null=False, unique_for_date=None, db_tablespace='', db_index=False)),
            ('description_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('title_de', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal('media_gallery', ['MediaGallery'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'MediaFile'
        db.delete_table('media_gallery_mediafile')
        
        # Deleting model 'MediaSet'
        db.delete_table('media_gallery_mediaset')
        
        # Deleting model 'MediaGallery'
        db.delete_table('media_gallery_mediagallery')
        
    
    
    models = {
        'media_gallery.mediafile': {
            'Meta': {'ordering': '["sort_order","creation_date"]'},
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'external_url': ('URLField', ["_('External URL')"], {'blank': 'True'}),
            'file_type': ('models.CharField', [], {'default': "'-'", 'max_length': '1', 'editable': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'media_set': ('models.ForeignKey', ["orm['media_gallery.MediaSet']"], {}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'path': ('FileBrowseField', ["_('File path')"], {'max_length': '255', 'blank': 'True'}),
            'sort_order': ('models.IntegerField', ['_("Sort order")'], {'blank': 'True'}),
            'splash_image_path': ('FileBrowseField', ["_('Splash-image path')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '255', 'blank': 'True'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '255', 'blank': 'True'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'media_gallery.mediaset': {
            'Meta': {'ordering': '["creation_date"]'},
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('models.BooleanField', ['_("Featured")'], {'default': 'False'}),
            'media_gallery': ('models.ForeignKey', ["orm['media_gallery.MediaGallery']"], {}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'slug': ('models.SlugField', [], {'default': "'default'", 'unique': 'False', 'max_length': '255'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '100', 'blank': 'True'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'views': ('models.IntegerField', ['_("views")'], {'default': '0', 'editable': 'False'})
        },
        'media_gallery.mediagallery': {
            'Meta': {'ordering': "['-creation_date']", 'get_latest_by': "'creation_date'"},
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'limit_choices_to': '{}', 'related_name': 'None', 'null': 'False', 'blank': 'False'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'null': 'False', 'unique_for_date': 'None', 'db_tablespace': "''", 'db_index': 'False'}),
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
