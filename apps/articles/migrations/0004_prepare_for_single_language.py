# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.conf import settings
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Article.language'
        db.add_column('articles_article', 'language', self.gf('django.db.models.fields.CharField')(default='', max_length=5, blank=True), keep_default=False)

        for lang_code, lang_name in settings.LANGUAGES:
            # Changing field 'Article.title_*'
            db.alter_column('articles_article', 'title_%s' % lang_code, self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))
            # Changing field 'Article.description_*'
            db.alter_column('articles_article', 'description_%s' % lang_code, self.gf('base_libs.models.fields.ExtendedTextField')(blank=True))
            # Changing field 'Article.content_*'
            db.alter_column('articles_article', 'content_%s' % lang_code, self.gf('base_libs.models.fields.ExtendedTextField')(blank=True))
            # Changing field 'Article.image_title_*'
            db.alter_column('articles_article', 'image_title_%s' % lang_code, self.gf('django.db.models.fields.CharField')(max_length=50, blank=True))
            # Changing field 'Article.subtitle_*'
            db.alter_column('articles_article', 'subtitle_%s' % lang_code, self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))
            # Changing field 'Article.image_description_*'
            db.alter_column('articles_article', 'image_description_%s' % lang_code, self.gf('base_libs.models.fields.ExtendedTextField')(blank=True))

        # Changing field 'Article.subtitle'
        db.alter_column('articles_article', 'subtitle', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))

        # Changing field 'Article.image_description'
        db.alter_column('articles_article', 'image_description', self.gf('base_libs.models.fields.ExtendedTextField')(blank=True))

        # Changing field 'Article.content'
        db.alter_column('articles_article', 'content', self.gf('base_libs.models.fields.ExtendedTextField')(blank=True))

        # Changing field 'Article.description'
        db.alter_column('articles_article', 'description', self.gf('base_libs.models.fields.ExtendedTextField')(blank=True))

        # Changing field 'Article.image_title'
        db.alter_column('articles_article', 'image_title', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True))

        # Changing field 'Article.title'
        db.alter_column('articles_article', 'title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))
    
    
    def backwards(self, orm):
        
        # Deleting field 'Article.language'
        db.delete_column('articles_article', 'language')

        for lang_code, lang_name in settings.LANGUAGES:
            # Changing field 'Article.title_*'
            db.alter_column('articles_article', 'title_%s' % lang_code, self.gf('django.db.models.fields.CharField')(u'title', unique=False, primary_key=False, db_column=None, editable=True, max_length=255, db_tablespace='', blank=False, null=False))
            # Changing field 'Article.description_*'
            db.alter_column('articles_article', 'description_%s' % lang_code, self.gf('base_libs.models.fields.ExtendedTextField')(u'summary', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique_for_date=None, db_tablespace=''))
            # Changing field 'Article.content_*'
            db.alter_column('articles_article', 'content_%s' % lang_code, self.gf('base_libs.models.fields.ExtendedTextField')(u'entry', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=False, unique_for_date=None, db_tablespace=''))
            # Changing field 'Article.image_title_*'
            db.alter_column('articles_article', 'image_title_%s' % lang_code, self.gf('django.db.models.fields.CharField')(u'image title', unique=False, primary_key=False, db_column=None, editable=True, max_length=50, db_tablespace='', blank=True, null=False))
            # Changing field 'Article.subtitle_*'
            db.alter_column('articles_article', 'subtitle_%s' % lang_code, self.gf('django.db.models.fields.CharField')(u'subtitle', unique=False, primary_key=False, db_column=None, editable=True, max_length=255, db_tablespace='', blank=True, null=False))
            # Changing field 'Article.image_description_*'
            db.alter_column('articles_article', 'image_description_%s' % lang_code, self.gf('base_libs.models.fields.ExtendedTextField')(u'image description', unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique_for_date=None, db_tablespace=''))

        # Changing field 'Article.subtitle'
        db.alter_column('articles_article', 'subtitle', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True))

        # Changing field 'Article.image_description'
        db.alter_column('articles_article', 'image_description', self.gf('base_libs.models.fields.MultilingualTextField')(null=True, blank=True))

        # Changing field 'Article.content'
        db.alter_column('articles_article', 'content', self.gf('base_libs.models.fields.MultilingualTextField')(null=True))

        # Changing field 'Article.description'
        db.alter_column('articles_article', 'description', self.gf('base_libs.models.fields.MultilingualTextField')(null=True, blank=True))

        # Changing field 'Article.image_title'
        db.alter_column('articles_article', 'image_title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=50, null=True, blank=True))

        # Changing field 'Article.title'
        db.alter_column('articles_article', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))
    
    
    models = {
        'articles.article': {
            'Meta': {'object_name': 'Article'},
            'article_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.ArticleType']", 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'article_author'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'content': ('base_libs.models.fields.ExtendedTextField', [], {'default': "''", 'blank': 'True'}),
            'content_de': ('base_libs.models.fields.ExtendedTextField', [], {'default': "''", 'blank': 'True'}),
            'content_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_en': ('base_libs.models.fields.ExtendedTextField', [], {'default': "''", 'blank': 'True'}),
            'content_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('base_libs.models.fields.ExtendedTextField', [], {'default': "''", 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', [], {'default': "''", 'blank': 'True'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', [], {'default': "''", 'blank': 'True'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'/articles/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'image_description': ('base_libs.models.fields.ExtendedTextField', [], {'default': "''", 'blank': 'True'}),
            'image_description_de': ('base_libs.models.fields.ExtendedTextField', [], {'default': "''", 'blank': 'True'}),
            'image_description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_description_en': ('base_libs.models.fields.ExtendedTextField', [], {'default': "''", 'blank': 'True'}),
            'image_description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'image_title_de': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'image_title_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'blank': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'published_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'published_till': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'subtitle_de': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'subtitle_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'articles.articletype': {
            'Meta': {'object_name': 'ArticleType'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_set'", 'blank': 'True', 'null': 'True', 'to': "orm['articles.ArticleType']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '8192', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '512', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
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
    
    complete_apps = ['articles']
