# encoding: utf-8
import datetime
import copy
from guess_language import guessLanguageTag
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.conf import settings
from django.template.defaultfilters import striptags
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields
from base_libs.utils.misc import html_to_plain_text

def guess_language_code(*args):
    """
    Takes a bunch of values and checks what language is probably used there
    from all settings.LANGUAGES
    """
    lang_dict = dict(((t[0], 0) for t in settings.LANGUAGES))
    # check how often each language is guessed
    for v in args:
        v = html_to_plain_text(v)
        guessed_code = guessLanguageTag(v)
        if guessed_code in lang_dict:
            lang_dict[guessed_code] += 1
    # consider the most often guess as the most probable language
    most_likely = sorted(lang_dict.items(), key=lambda x: x[1], reverse=True)
    return most_likely[0][0]

class Migration(DataMigration):
    
    def forwards(self, orm):
        for a in orm.Article.objects.all():
            lang_code = settings.LANGUAGE_CODE
            a.title = getattr(a, "title_%s" % lang_code) 
            a.subtitle = getattr(a, "subtitle_%s" % lang_code) 
            a.description = getattr(a, "description_%s" % lang_code) 
            a.description_markup_type = getattr(a, "description_%s_markup_type" % lang_code) 
            a.content = getattr(a, "content_%s" % lang_code)
            a.content_markup_type = getattr(a, "content_%s_markup_type" % lang_code)
            a.image_title = getattr(a, "image_title_%s" % lang_code) 
            a.image_description = getattr(a, "image_description_%s" % lang_code)
            a.image_description_markup_type = getattr(a, "image_description_%s_markup_type" % lang_code)
            a.language = guess_language_code(
                a.title,
                a.subtitle,
                a.description,
                a.content,
                )
            #a.language = lang_code
            a.save()
            for lang_code, lang_name in settings.LANGUAGES:
                if lang_code != settings.LANGUAGE_CODE and lang_code != a.language:
                    content = striptags(getattr(a, "content_%s" % lang_code)).strip()
                    if content and content != striptags(a.content).strip():
                        a2 = copy.copy(a)
                        a2.id = None
                        a2.title = getattr(a, "title_%s" % lang_code) 
                        a2.subtitle = getattr(a, "subtitle_%s" % lang_code) 
                        a2.description = getattr(a, "description_%s" % lang_code) 
                        a2.description_markup_type = getattr(a, "description_%s_markup_type" % lang_code) 
                        a2.content = getattr(a, "content_%s" % lang_code)
                        a2.content_markup_type = getattr(a, "content_%s_markup_type" % lang_code)
                        a2.image_title = getattr(a, "image_title_%s" % lang_code) 
                        a2.image_description = getattr(a, "image_description_%s" % lang_code)
                        a2.image_description_markup_type = getattr(a, "image_description_%s_markup_type" % lang_code)
                        a2.language = guess_language_code(
                            a2.title,
                            a2.subtitle,
                            a2.description,
                            a2.content,
                            )
                        #a2.language = lang_code
                        a2.save()
                        for field in a._meta.many_to_many:
                            source = getattr(a, field.attname)
                            destination = getattr(a2, field.attname)
                            for item in source.all():
                                destination.add(item)
    
    
    def backwards(self, orm):
        pass

    
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
