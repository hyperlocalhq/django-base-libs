# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields
from django.conf import settings

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'MediaFile.gallery'
        db.add_column('media_gallery_mediafile', 'gallery', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['media_gallery.MediaGallery']), keep_default=False)

        # Changing field 'MediaFile.description'
        db.alter_column('media_gallery_mediafile', 'description', self.gf('base_libs.models.fields.MultilingualTextField')(null=True, blank=True))

        # Changing field 'MediaFile.title'
        db.alter_column('media_gallery_mediafile', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True))

        for lang_code, lang_name in settings.LANGUAGES:
            # Changing field 'MediaFile.description_*'
            db.alter_column(
                'media_gallery_mediafile',
                'description_%s' % lang_code,
                self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace=''),
                )
            # Changing field 'MediaSet.description_*'
            db.alter_column(
                'media_gallery_mediaset',
                'description_%s' % lang_code,
                self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace=''),
                )
            # Changing field 'MediaGallery.description_*'
            db.alter_column(
                'media_gallery_mediagallery',
                'description_%s' % lang_code,
                self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace=''),
                )
            # Adding field 'MediaGallery.content_object_repr_*'
            db.add_column(
                'media_gallery_mediagallery',
                'content_object_repr_%s' % lang_code,
                self.gf('django.db.models.fields.CharField')(u'Content object representation', null=False, primary_key=False, db_column=None, default='', editable=False, max_length=100, db_tablespace='', blank=True, unique=False, db_index=False),
                keep_default=False,
                ) 


        # Changing field 'MediaFile.sort_order'
        db.alter_column('media_gallery_mediafile', 'sort_order', self.gf('base_libs.models.fields.PositionField')(blank=True, default=0))

        # Changing field 'MediaFile.media_set'
        db.alter_column('media_gallery_mediafile', 'media_set_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media_gallery.MediaSet'], null=True, blank=True))

        # Changing field 'MediaFile.path'
        db.alter_column('media_gallery_mediafile', 'path', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, blank=True))

        # Changing field 'MediaFile.splash_image_path'
        db.alter_column('media_gallery_mediafile', 'splash_image_path', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'], blank=True))

        # Changing field 'MediaFile.external_url'
        db.alter_column('media_gallery_mediafile', 'external_url', self.gf('base_libs.models.fields.URLField')(max_length=200, blank=True))

        # Changing field 'MediaSet.description'
        db.alter_column('media_gallery_mediaset', 'description', self.gf('base_libs.models.fields.MultilingualTextField')(null=True, blank=True))

        # Changing field 'MediaSet.title'
        db.alter_column('media_gallery_mediaset', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=100, null=True, blank=True))

        # Adding field 'MediaGallery.is_featured'
        db.add_column('media_gallery_mediagallery', 'is_featured', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Adding field 'MediaGallery.content_object_repr'
        db.add_column('media_gallery_mediagallery', 'content_object_repr', self.gf('base_libs.models.fields.MultilingualCharField')(default='', max_length=100, null=True, blank=True), keep_default=False)

        # Adding field 'MediaGallery.sort_order'
        db.add_column('media_gallery_mediagallery', 'sort_order', self.gf('base_libs.models.fields.PositionField')(default=0, blank=True), keep_default=False)

        # Adding field 'MediaGallery.content_object_id'
        db.add_column('media_gallery_mediagallery', 'content_object_id', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True), keep_default=False)

        # Adding field 'MediaGallery.views'
        db.add_column('media_gallery_mediagallery', 'views', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'MediaGallery.slug'
        db.add_column('media_gallery_mediagallery', 'slug', self.gf('django.db.models.fields.SlugField')(default='default', max_length=255, db_index=True), keep_default=False)

        # Adding field 'MediaGallery.cover_image'
        db.add_column('media_gallery_mediagallery', 'cover_image', self.gf('filebrowser.fields.FileBrowseField')(default='', max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'], blank=True), keep_default=False)

        # Changing field 'MediaGallery.description'
        db.alter_column('media_gallery_mediagallery', 'description', self.gf('base_libs.models.fields.MultilingualTextField')(null=True, blank=True))

        # Changing field 'MediaGallery.title'
        db.alter_column('media_gallery_mediagallery', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=100, null=True, blank=True))

        # Changing field 'MediaGallery.object_id'
        db.alter_column('media_gallery_mediagallery', 'object_id', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'MediaGallery.content_type'
        db.alter_column('media_gallery_mediagallery', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))
    
    
    def backwards(self, orm):
        
        # Deleting field 'MediaFile.gallery'
        db.delete_column('media_gallery_mediafile', 'gallery_id')

        # Changing field 'MediaFile.description'
        db.alter_column('media_gallery_mediafile', 'description', self.gf('base_libs.models.fields.MultilingualTextField')(_("Description"), blank=True))

        # Changing field 'MediaFile.title'
        db.alter_column('media_gallery_mediafile', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(_("Title"), max_length=255, blank=True))

        # Changing field 'MediaFile.sort_order'
        db.alter_column('media_gallery_mediafile', 'sort_order', self.gf('base_libs.models.fields.PositionField')(_("Sort order")))

        # Changing field 'MediaFile.media_set'
        db.alter_column('media_gallery_mediafile', 'media_set_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media_gallery.MediaSet']))

        # Changing field 'MediaFile.path'
        db.alter_column('media_gallery_mediafile', 'path', self.gf('filebrowser.fields.FileBrowseField')(_('File path'), max_length=255, blank=True))

        # Changing field 'MediaFile.splash_image_path'
        db.alter_column('media_gallery_mediafile', 'splash_image_path', self.gf('filebrowser.fields.FileBrowseField')(_('Splash-image path'), max_length=255, extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff'], blank=True))

        # Changing field 'MediaFile.external_url'
        db.alter_column('media_gallery_mediafile', 'external_url', self.gf('base_libs.models.fields.URLField')(_('External URL'), blank=True))

        # Changing field 'MediaSet.description'
        db.alter_column('media_gallery_mediaset', 'description', self.gf('base_libs.models.fields.MultilingualTextField')(_("Description"), blank=True))

        # Changing field 'MediaSet.title'
        db.alter_column('media_gallery_mediaset', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(_("Title"), max_length=100, blank=True))

        # Deleting field 'MediaGallery.is_featured'
        db.delete_column('media_gallery_mediagallery', 'is_featured')

        # Deleting field 'MediaGallery.content_object_repr'
        db.delete_column('media_gallery_mediagallery', 'content_object_repr')

        # Deleting field 'MediaGallery.sort_order'
        db.delete_column('media_gallery_mediagallery', 'sort_order')

        # Deleting field 'MediaGallery.content_object_id'
        db.delete_column('media_gallery_mediagallery', 'content_object_id')

        # Deleting field 'MediaGallery.views'
        db.delete_column('media_gallery_mediagallery', 'views')


        # Deleting field 'MediaGallery.slug'
        db.delete_column('media_gallery_mediagallery', 'slug')

        # Deleting field 'MediaGallery.cover_image'
        db.delete_column('media_gallery_mediagallery', 'cover_image')

        # Changing field 'MediaGallery.description'
        db.alter_column('media_gallery_mediagallery', 'description', self.gf('base_libs.models.fields.MultilingualTextField')(_("Description"), blank=True))

        # Changing field 'MediaGallery.title'
        db.alter_column('media_gallery_mediagallery', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(_("Title"), max_length=100, blank=True))

        # Changing field 'MediaGallery.object_id'
        db.alter_column('media_gallery_mediagallery', 'object_id', self.gf('django.db.models.fields.CharField')(u'Related object', max_length=255, null=False, blank=False))

        # Changing field 'MediaGallery.content_type'
        db.alter_column('media_gallery_mediagallery', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(orm['contenttypes.ContentType'], null=False, blank=False))

        for lang_code, lang_name in settings.LANGUAGES:
            # Changing field 'MediaGallery.description_*'
            db.alter_column('media_gallery_mediagallery', 'description_%s' % lang_code, self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique_for_date=None, db_tablespace=''))
            # Deleting field 'MediaGallery.content_object_repr_*'
            db.delete_column('media_gallery_mediagallery', 'content_object_repr_%s' % lang_code)
            # Changing field 'MediaSet.description_*'
            db.alter_column('media_gallery_mediaset', 'description_%s' % lang_code, self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique_for_date=None, db_tablespace=''))
            # Changing field 'MediaFile.description_*'
            db.alter_column('media_gallery_mediafile', 'description_%s' % lang_code, self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique_for_date=None, db_tablespace=''))
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'media_gallery.mediafile': {
            'Meta': {'object_name': 'MediaFile'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediafile_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'external_url': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'file_type': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '1'}),
            'gallery': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['media_gallery.MediaGallery']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['media_gallery.MediaSet']", 'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediafile_modifier'", 'null': 'True', 'to': "orm['auth.User']"}),
            'path': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'blank': 'True'}),
            'sort_order': ('base_libs.models.fields.PositionField', [], {'blank': 'True'}),
            'splash_image_path': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'media_gallery.mediagallery': {
            'Meta': {'object_name': 'MediaGallery'},
            'content_object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'content_object_repr': ('base_libs.models.fields.MultilingualCharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'content_object_repr_de': ('django.db.models.fields.CharField', ["u'Content object representation'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'False', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'content_object_repr_en': ('django.db.models.fields.CharField', ["u'Content object representation'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'False', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'cover_image': ('filebrowser.fields.FileBrowseField', [], {'default': "''", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "'default'", 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('base_libs.models.fields.PositionField', [], {'default': '0', 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'media_gallery.mediaset': {
            'Meta': {'object_name': 'MediaSet'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediaset_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'media_gallery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['media_gallery.MediaGallery']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mediaset_modifier'", 'null': 'True', 'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "'default'", 'max_length': '255', 'db_index': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'permissions.rowlevelpermission': {
            'Meta': {'object_name': 'RowLevelPermission', 'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': "orm['contenttypes.ContentType']"}),
            'owner_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Permission']"})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['media_gallery']
