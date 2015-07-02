# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'FaqContainer.title_en'
        db.add_column(u'faqs_faqcontainer', 'title_en', self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False), keep_default=False)

        # Deleting field 'FaqCategory.description_markup_type'
        db.delete_column(u'faqs_faqcategory', 'description_markup_type')

        # Adding field 'FaqCategory.title_en'
        db.add_column(u'faqs_faqcategory', 'title_en', self.gf('django.db.models.fields.CharField')(u'title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=512, db_tablespace='', blank=True, unique=False, db_index=False), keep_default=False)

        # Adding field 'FaqCategory.description_en'
        db.add_column(u'faqs_faqcategory', 'description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=8192, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'FaqCategory.description_en_markup_type'
        db.add_column(u'faqs_faqcategory', 'description_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Adding field 'FaqCategory.short_title_en'
        db.add_column(u'faqs_faqcategory', 'short_title_en', self.gf('django.db.models.fields.CharField')(u'short title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=80, db_tablespace='', blank=True, unique=False, db_index=False), keep_default=False)

        # Changing field 'FaqCategory.description_de'
        db.alter_column(u'faqs_faqcategory', 'description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=8192, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Deleting field 'QuestionAnswer.answer_markup_type'
        db.delete_column(u'faqs_questionanswer', 'answer_markup_type')

        # Adding field 'QuestionAnswer.question_en'
        db.add_column(u'faqs_questionanswer', 'question_en', self.gf('django.db.models.fields.CharField')(u'question', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False), keep_default=False)

        # Adding field 'QuestionAnswer.answer_en'
        db.add_column(u'faqs_questionanswer', 'answer_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'answer', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=16384, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False), keep_default=False)

        # Adding field 'QuestionAnswer.answer_en_markup_type'
        db.add_column(u'faqs_questionanswer', 'answer_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Changing field 'QuestionAnswer.answer_de'
        db.alter_column(u'faqs_questionanswer', 'answer_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'answer', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=16384, unique_for_year=None, rel=None, unique=False, db_tablespace=''))
    
    
    def backwards(self, orm):
        
        # Deleting field 'FaqContainer.title_en'
        db.delete_column(u'faqs_faqcontainer', 'title_en')

        # Adding field 'FaqCategory.description_markup_type'
        db.add_column(u'faqs_faqcategory', 'description_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Deleting field 'FaqCategory.title_en'
        db.delete_column(u'faqs_faqcategory', 'title_en')

        # Deleting field 'FaqCategory.description_en'
        db.delete_column(u'faqs_faqcategory', 'description_en')

        # Deleting field 'FaqCategory.description_en_markup_type'
        db.delete_column(u'faqs_faqcategory', 'description_en_markup_type')

        # Deleting field 'FaqCategory.short_title_en'
        db.delete_column(u'faqs_faqcategory', 'short_title_en')

        # Changing field 'FaqCategory.description_de'
        db.alter_column(u'faqs_faqcategory', 'description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Beschreibung', rel=None, unique_for_year=None, unique_for_date=None, unique_for_month=None, unique=False, primary_key=False, db_column=None, default='', max_length=8192, db_tablespace=''))

        # Adding field 'QuestionAnswer.answer_markup_type'
        db.add_column(u'faqs_questionanswer', 'answer_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False), keep_default=False)

        # Deleting field 'QuestionAnswer.question_en'
        db.delete_column(u'faqs_questionanswer', 'question_en')

        # Deleting field 'QuestionAnswer.answer_en'
        db.delete_column(u'faqs_questionanswer', 'answer_en')

        # Deleting field 'QuestionAnswer.answer_en_markup_type'
        db.delete_column(u'faqs_questionanswer', 'answer_en_markup_type')

        # Changing field 'QuestionAnswer.answer_de'
        db.alter_column(u'faqs_questionanswer', 'answer_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Antwort', rel=None, unique_for_year=None, unique_for_date=None, unique_for_month=None, unique=False, primary_key=False, db_column=None, default=None, max_length=16384, db_tablespace=''))
    
    
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 2, 16, 13, 58, 957093)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 2, 16, 13, 58, 956301)'}),
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
        u'faqs.faqcategory': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'FaqCategory'},
            'children_sort_order_format': ('django.db.models.fields.CharField', [], {'default': "'%02d'", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['faqs.FaqContainer']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'faqcategory_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'max_length': '8192', 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '8192', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '8192', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'faqs_on_separate_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'faqcategory_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': u"orm['faqs.FaqCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'short_title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '80', 'null': 'True'}),
            'short_title_de': ('django.db.models.fields.CharField', ["u'short title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'short_title_en': ('django.db.models.fields.CharField', ["u'short title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '512', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'faqs.faqcontainer': {
            'Meta': {'ordering': "('title',)", 'object_name': 'FaqContainer'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'sysname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'faqs.questionanswer': {
            'Meta': {'ordering': "['category']", 'object_name': 'QuestionAnswer'},
            'answer': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'max_length': '16384', 'null': 'True'}),
            'answer_de': ('base_libs.models.fields.ExtendedTextField', ["u'answer'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '16384', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'answer_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'answer_en': ('base_libs.models.fields.ExtendedTextField', ["u'answer'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '16384', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'answer_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'category': ('mptt.fields.TreeForeignKey', [], {'to': u"orm['faqs.FaqCategory']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionanswer_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionanswer_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'question': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'question_de': ('django.db.models.fields.CharField', ["u'question'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'question_en': ('django.db.models.fields.CharField', ["u'question'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['faqs']
