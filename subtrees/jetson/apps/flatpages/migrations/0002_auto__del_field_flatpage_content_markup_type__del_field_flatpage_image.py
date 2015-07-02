# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'flatpage.content_markup_type'
        db.delete_column(u'flatpages_flatpage', 'content_markup_type')

        # Deleting field 'flatpage.image_description_markup_type'
        db.delete_column(u'flatpages_flatpage', 'image_description_markup_type')

        # Changing field 'FlatPage.status'
        db.alter_column(u'flatpages_flatpage', 'status', self.gf('django.db.models.fields.SmallIntegerField')())

        # Changing field 'FlatPage.subtitle'
        db.alter_column(u'flatpages_flatpage', 'subtitle', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'FlatPage.creator'
        db.alter_column(u'flatpages_flatpage', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'FlatPage.template_name'
        db.alter_column(u'flatpages_flatpage', 'template_name', self.gf('django.db.models.fields.CharField')(max_length=70))

        # Changing field 'FlatPage.image'
        db.alter_column(u'flatpages_flatpage', 'image', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']))

        # Changing field 'FlatPage.creation_date'
        db.alter_column(u'flatpages_flatpage', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'FlatPage.modified_date'
        db.alter_column(u'flatpages_flatpage', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'FlatPage.registration_required'
        db.alter_column(u'flatpages_flatpage', 'registration_required', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'FlatPage.author'
        db.alter_column(u'flatpages_flatpage', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'FlatPage.image_description'
        db.alter_column(u'flatpages_flatpage', 'image_description', self.gf('base_libs.models.fields.MultilingualTextField')(null=True))

        # Changing field 'FlatPage.published_till'
        db.alter_column(u'flatpages_flatpage', 'published_till', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'FlatPage.content'
        db.alter_column(u'flatpages_flatpage', 'content', self.gf('base_libs.models.fields.MultilingualTextField')(null=True))

        # Changing field 'FlatPage.content_de'
        db.alter_column(u'flatpages_flatpage', 'content_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'content', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'FlatPage.enable_comments'
        db.alter_column(u'flatpages_flatpage', 'enable_comments', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'FlatPage.image_description_en'
        db.alter_column(u'flatpages_flatpage', 'image_description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'image description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'FlatPage.content_en'
        db.alter_column(u'flatpages_flatpage', 'content_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'content', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'FlatPage.image_title'
        db.alter_column(u'flatpages_flatpage', 'image_title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=50, null=True))

        # Changing field 'FlatPage.published_from'
        db.alter_column(u'flatpages_flatpage', 'published_from', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'FlatPage.url'
        db.alter_column(u'flatpages_flatpage', 'url', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'FlatPage.title'
        db.alter_column(u'flatpages_flatpage', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'FlatPage.short_title'
        db.alter_column(u'flatpages_flatpage', 'short_title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=32, null=True))

        # Changing field 'FlatPage.image_description_de'
        db.alter_column(u'flatpages_flatpage', 'image_description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'image description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'FlatPage.modifier'
        db.alter_column(u'flatpages_flatpage', 'modifier_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))
    
    
    def backwards(self, orm):
        
        # Adding field 'flatpage.content_markup_type'
        db.add_column(u'flatpages_flatpage', 'content_markup_type', self.gf('models.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'flatpage.image_description_markup_type'
        db.add_column(u'flatpages_flatpage', 'image_description_markup_type', self.gf('models.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Changing field 'FlatPage.status'
        db.alter_column(u'flatpages_flatpage', 'status', self.gf('models.SmallIntegerField')(_("status")))

        # Changing field 'FlatPage.subtitle'
        db.alter_column(u'flatpages_flatpage', 'subtitle', self.gf('MultilingualCharField')(_('subtitle'), max_length=255))

        # Changing field 'FlatPage.creator'
        db.alter_column(u'flatpages_flatpage', 'creator_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'FlatPage.template_name'
        db.alter_column(u'flatpages_flatpage', 'template_name', self.gf('models.CharField')(_('template name'), max_length=70))

        # Changing field 'FlatPage.image'
        db.alter_column(u'flatpages_flatpage', 'image', self.gf('FileBrowseField')(_('image'), max_length=255, extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff']))

        # Changing field 'FlatPage.creation_date'
        db.alter_column(u'flatpages_flatpage', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'FlatPage.modified_date'
        db.alter_column(u'flatpages_flatpage', 'modified_date', self.gf('models.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'FlatPage.registration_required'
        db.alter_column(u'flatpages_flatpage', 'registration_required', self.gf('models.BooleanField')(_('registration required')))

        # Changing field 'FlatPage.author'
        db.alter_column(u'flatpages_flatpage', 'author_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True))

        # Changing field 'FlatPage.image_description'
        db.alter_column(u'flatpages_flatpage', 'image_description', self.gf('MultilingualTextField')(_('image description')))

        # Changing field 'FlatPage.published_till'
        db.alter_column(u'flatpages_flatpage', 'published_till', self.gf('models.DateTimeField')(_("published until"), null=True))

        # Changing field 'FlatPage.content'
        db.alter_column(u'flatpages_flatpage', 'content', self.gf('MultilingualTextField')(_('content')))

        # Changing field 'FlatPage.content_de'
        db.alter_column(u'flatpages_flatpage', 'content_de', self.gf('ExtendedTextField')(u'content', db_tablespace='', unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, rel=None, unique_for_date=None))

        # Changing field 'FlatPage.enable_comments'
        db.alter_column(u'flatpages_flatpage', 'enable_comments', self.gf('models.BooleanField')(_('enable comments')))

        # Changing field 'FlatPage.image_description_en'
        db.alter_column(u'flatpages_flatpage', 'image_description_en', self.gf('ExtendedTextField')(u'image description', db_tablespace='', unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, rel=None, unique_for_date=None))

        # Changing field 'FlatPage.content_en'
        db.alter_column(u'flatpages_flatpage', 'content_en', self.gf('ExtendedTextField')(u'content', db_tablespace='', unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, rel=None, unique_for_date=None))

        # Changing field 'FlatPage.image_title'
        db.alter_column(u'flatpages_flatpage', 'image_title', self.gf('MultilingualCharField')(_('image title'), max_length=50))

        # Changing field 'FlatPage.published_from'
        db.alter_column(u'flatpages_flatpage', 'published_from', self.gf('models.DateTimeField')(_("publishing date"), null=True))

        # Changing field 'FlatPage.url'
        db.alter_column(u'flatpages_flatpage', 'url', self.gf('models.CharField')(_('URL'), max_length=100))

        # Changing field 'FlatPage.title'
        db.alter_column(u'flatpages_flatpage', 'title', self.gf('MultilingualCharField')(_('title'), max_length=255))

        # Changing field 'FlatPage.short_title'
        db.alter_column(u'flatpages_flatpage', 'short_title', self.gf('MultilingualCharField')(_('short title'), max_length=32))

        # Changing field 'FlatPage.image_description_de'
        db.alter_column(u'flatpages_flatpage', 'image_description_de', self.gf('ExtendedTextField')(u'image description', db_tablespace='', unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, rel=None, unique_for_date=None))

        # Changing field 'FlatPage.modifier'
        db.alter_column(u'flatpages_flatpage', 'modifier_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))
    
    
    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'ordering': "('username',)", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 2, 16, 16, 18, 252608)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 2, 16, 16, 18, 251904)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'flatpages.flatpage': {
            'Meta': {'ordering': "('url',)", 'object_name': 'FlatPage'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'flatpage_author'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'content': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'content_de': ('base_libs.models.fields.ExtendedTextField', ["u'content'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_en': ('base_libs.models.fields.ExtendedTextField', ["u'content'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flatpage_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'image_description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'image_description_de': ('base_libs.models.fields.ExtendedTextField', ["u'image description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_description_en': ('base_libs.models.fields.ExtendedTextField', ["u'image description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'image_title_de': ('django.db.models.fields.CharField', ["u'image title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'image_title_en': ('django.db.models.fields.CharField', ["u'image title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'flatpage_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'published_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'published_till': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'short_title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'short_title_de': ('django.db.models.fields.CharField', ["u'short title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '32', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'short_title_en': ('django.db.models.fields.CharField', ["u'short title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '32', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sites.Site']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'subtitle': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('django.db.models.fields.CharField', ["u'subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_en': ('django.db.models.fields.CharField', ["u'subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['flatpages']
