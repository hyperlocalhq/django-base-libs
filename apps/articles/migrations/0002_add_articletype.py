# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'ArticleType'
        db.create_table('articles_articletype', south_cleaned_fields((
            ('title_de', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=512, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=512, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, unique=True, db_index=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='child_set', blank=True, null=True, to=orm['articles.ArticleType'])),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=512, null=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=8192, null=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        )))
        db.send_create_signal('articles', ['ArticleType'])

        # Changing field 'Article.is_featured'
        db.alter_column('articles_article', 'is_featured', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Article.subtitle'
        db.alter_column('articles_article', 'subtitle', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True, blank=True))

        # Changing field 'Article.image'
        db.alter_column('articles_article', 'image', self.gf('filebrowser.fields.FileBrowseField')(directory='/articles/', max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'], blank=True))

        # Changing field 'Article.creation_date'
        db.alter_column('articles_article', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Article.article_type'
        db.alter_column('articles_article', 'article_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articles.ArticleType'], null=True, blank=True))

        # Changing field 'Article.description_de'
        db.alter_column('articles_article', 'description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'summary', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace=''))

        # Changing field 'Article.modified_date'
        db.alter_column('articles_article', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Article.author'
        db.alter_column('articles_article', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['auth.User']))

        # Changing field 'Article.image_description'
        db.alter_column('articles_article', 'image_description', self.gf('base_libs.models.fields.MultilingualTextField')(null=True, blank=True))

        # Changing field 'Article.published_till'
        db.alter_column('articles_article', 'published_till', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True))

        # Changing field 'Article.content'
        db.alter_column('articles_article', 'content', self.gf('base_libs.models.fields.MultilingualTextField')(null=True))

        # Changing field 'Article.content_de'
        db.alter_column('articles_article', 'content_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'entry', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=False, unique=False, db_tablespace=''))

        # Changing field 'Article.status'
        db.alter_column('articles_article', 'status', self.gf('django.db.models.fields.SmallIntegerField')())

        # Changing field 'Article.description'
        db.alter_column('articles_article', 'description', self.gf('base_libs.models.fields.MultilingualTextField')(null=True, blank=True))

        # Changing field 'Article.views'
        db.alter_column('articles_article', 'views', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Article.image_title'
        db.alter_column('articles_article', 'image_title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=50, null=True, blank=True))

        # Changing field 'Article.published_from'
        db.alter_column('articles_article', 'published_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True))

        # Changing field 'Article.title'
        db.alter_column('articles_article', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'Article.image_description_de'
        db.alter_column('articles_article', 'image_description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'image description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace=''))
    
    
    def backwards(self, orm):
        
        # Deleting model 'ArticleType'
        db.delete_table('articles_articletype')

        # Changing field 'Article.is_featured'
        db.alter_column('articles_article', 'is_featured', self.gf('models.BooleanField')(_("Featured")))

        # Changing field 'Article.subtitle'
        db.alter_column('articles_article', 'subtitle', self.gf('MultilingualCharField')(_('subtitle'), max_length=255, blank=True))

        # Changing field 'Article.image'
        db.alter_column('articles_article', 'image', self.gf('FileBrowseField')(_('overview image'), directory="/articles/", max_length=255, extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff'], blank=True))

        # Changing field 'Article.creation_date'
        db.alter_column('articles_article', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'Article.article_type'
        db.alter_column('articles_article', 'article_type_id', self.gf('models.ForeignKey')(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_article_types'}))

        # Changing field 'Article.description_de'
        db.alter_column('articles_article', 'description_de', self.gf('ExtendedTextField')(u'summary', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace=''))

        # Changing field 'Article.modified_date'
        db.alter_column('articles_article', 'modified_date', self.gf('models.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'Article.author'
        db.alter_column('articles_article', 'author_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, blank=True))

        # Changing field 'Article.image_description'
        db.alter_column('articles_article', 'image_description', self.gf('MultilingualTextField')(_('image description'), blank=True))

        # Changing field 'Article.published_till'
        db.alter_column('articles_article', 'published_till', self.gf('models.DateTimeField')(_("published until"), null=True, blank=True))

        # Changing field 'Article.content'
        db.alter_column('articles_article', 'content', self.gf('MultilingualTextField')(_('entry')))

        # Changing field 'Article.content_de'
        db.alter_column('articles_article', 'content_de', self.gf('ExtendedTextField')(u'entry', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=False, unique=False, unique_for_date=None, db_tablespace=''))

        # Changing field 'Article.status'
        db.alter_column('articles_article', 'status', self.gf('models.SmallIntegerField')(_("status")))

        # Changing field 'Article.description'
        db.alter_column('articles_article', 'description', self.gf('MultilingualTextField')(_('summary'), blank=True))

        # Changing field 'Article.views'
        db.alter_column('articles_article', 'views', self.gf('models.IntegerField')(_("views"), editable=False))

        # Changing field 'Article.image_title'
        db.alter_column('articles_article', 'image_title', self.gf('MultilingualCharField')(_('image title'), max_length=50, blank=True))

        # Changing field 'Article.published_from'
        db.alter_column('articles_article', 'published_from', self.gf('models.DateTimeField')(_("publishing date"), null=True, blank=True))

        # Changing field 'Article.title'
        db.alter_column('articles_article', 'title', self.gf('MultilingualCharField')(_('title'), max_length=255))

        # Changing field 'Article.image_description_de'
        db.alter_column('articles_article', 'image_description_de', self.gf('ExtendedTextField')(u'image description', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace=''))
    
    
    models = {
        'articles.article': {
            'Meta': {'object_name': 'Article'},
            'article_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articles.ArticleType']", 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'article_author'", 'blank': 'True', 'null': 'True', 'to': "orm['auth.User']"}),
            'content': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True'}),
            'content_de': ('base_libs.models.fields.ExtendedTextField', ["u'entry'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'False', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'content_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'content_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'summary'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'/articles/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'image_description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'image_description_de': ('base_libs.models.fields.ExtendedTextField', ["u'image description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'image_description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'image_title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'image_title_de': ('django.db.models.fields.CharField', ["u'image title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'published_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'published_till': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'unique': 'True', 'db_index': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'subtitle': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('django.db.models.fields.CharField', ["u'subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
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
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
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
