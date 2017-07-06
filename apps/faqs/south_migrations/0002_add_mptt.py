# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'FaqContainer.sysname'
        db.alter_column('faqs_faqcontainer', 'sysname', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'FaqContainer.title'
        db.alter_column('faqs_faqcontainer', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'FaqContainer.creation_date'
        db.alter_column('faqs_faqcontainer', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'FaqContainer.modified_date'
        db.alter_column('faqs_faqcontainer', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'FaqContainer.content_type'
        db.alter_column('faqs_faqcontainer', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True))

        # Deleting field 'faqcategory.path'
        db.delete_column('faqs_faqcategory', 'path')

        # Adding field 'FaqCategory.lft'
        db.add_column('faqs_faqcategory', 'lft', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'FaqCategory.rght'
        db.add_column('faqs_faqcategory', 'rght', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'FaqCategory.tree_id'
        db.add_column('faqs_faqcategory', 'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Adding field 'FaqCategory.level'
        db.add_column('faqs_faqcategory', 'level', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True), keep_default=False)

        # Changing field 'FaqCategory.creator'
        db.alter_column('faqs_faqcategory', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'FaqCategory.creation_date'
        db.alter_column('faqs_faqcategory', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'FaqCategory.sort_order'
        db.alter_column('faqs_faqcategory', 'sort_order', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'FaqCategory.description_de'
        db.alter_column('faqs_faqcategory', 'description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Beschreibung', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=8192, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'FaqCategory.modified_date'
        db.alter_column('faqs_faqcategory', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'FaqCategory.container'
        db.alter_column('faqs_faqcategory', 'container_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['faqs.FaqContainer']))

        # Changing field 'FaqCategory.parent'
        db.alter_column('faqs_faqcategory', 'parent_id', self.gf('mptt.fields.TreeForeignKey')(null=True, to=orm['faqs.FaqCategory']))

        # Changing field 'FaqCategory.title'
        db.alter_column('faqs_faqcategory', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=512, null=True))

        # Changing field 'FaqCategory.children_sort_order_format'
        db.alter_column('faqs_faqcategory', 'children_sort_order_format', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'FaqCategory.description'
        db.alter_column('faqs_faqcategory', 'description', self.gf('base_libs.models.fields.MultilingualTextField')(max_length=8192, null=True))

        # Changing field 'FaqCategory.faqs_on_separate_page'
        db.alter_column('faqs_faqcategory', 'faqs_on_separate_page', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'FaqCategory.description_en'
        db.alter_column('faqs_faqcategory', 'description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Beschreibung', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=8192, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'FaqCategory.short_title'
        db.alter_column('faqs_faqcategory', 'short_title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=80, null=True))

        # Changing field 'FaqCategory.modifier'
        db.alter_column('faqs_faqcategory', 'modifier_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'QuestionAnswer.category'
        db.alter_column('faqs_questionanswer', 'category_id', self.gf('mptt.fields.TreeForeignKey')(to=orm['faqs.FaqCategory']))

        # Changing field 'QuestionAnswer.modified_date'
        db.alter_column('faqs_questionanswer', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'QuestionAnswer.modifier'
        db.alter_column('faqs_questionanswer', 'modifier_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'QuestionAnswer.views'
        db.alter_column('faqs_questionanswer', 'views', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'QuestionAnswer.creator'
        db.alter_column('faqs_questionanswer', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'QuestionAnswer.question'
        db.alter_column('faqs_questionanswer', 'question', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True))

        # Changing field 'QuestionAnswer.answer_de'
        db.alter_column('faqs_questionanswer', 'answer_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Antwort', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=16384, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'QuestionAnswer.creation_date'
        db.alter_column('faqs_questionanswer', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'QuestionAnswer.sort_order'
        db.alter_column('faqs_questionanswer', 'sort_order', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'QuestionAnswer.answer'
        db.alter_column('faqs_questionanswer', 'answer', self.gf('base_libs.models.fields.MultilingualTextField')(max_length=16384, null=True))

        # Changing field 'QuestionAnswer.answer_en'
        db.alter_column('faqs_questionanswer', 'answer_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Antwort', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=16384, unique_for_year=None, rel=None, unique=False, db_tablespace=''))
    
    
    def backwards(self, orm):
        
        # Changing field 'FaqContainer.sysname'
        db.alter_column('faqs_faqcontainer', 'sysname', self.gf('models.CharField')(_("URL Identifier"), max_length=255))

        # Changing field 'FaqContainer.title'
        db.alter_column('faqs_faqcontainer', 'title', self.gf('MultilingualCharField')(_('title'), max_length=255))

        # Changing field 'FaqContainer.creation_date'
        db.alter_column('faqs_faqcontainer', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'FaqContainer.modified_date'
        db.alter_column('faqs_faqcontainer', 'modified_date', self.gf('models.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'FaqContainer.content_type'
        db.alter_column('faqs_faqcontainer', 'content_type_id', self.gf('models.ForeignKey')(orm['contenttypes.ContentType'], limit_choices_to={}, null=True))

        # Adding field 'faqcategory.path'
        db.add_column('faqs_faqcategory', 'path', self.gf('models.CharField')(_('path'), null=True, max_length=8192, editable=False), keep_default=False)

        # Deleting field 'FaqCategory.lft'
        db.delete_column('faqs_faqcategory', 'lft')

        # Deleting field 'FaqCategory.rght'
        db.delete_column('faqs_faqcategory', 'rght')

        # Deleting field 'FaqCategory.tree_id'
        db.delete_column('faqs_faqcategory', 'tree_id')

        # Deleting field 'FaqCategory.level'
        db.delete_column('faqs_faqcategory', 'level')

        # Changing field 'FaqCategory.creator'
        db.alter_column('faqs_faqcategory', 'creator_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'FaqCategory.creation_date'
        db.alter_column('faqs_faqcategory', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'FaqCategory.sort_order'
        db.alter_column('faqs_faqcategory', 'sort_order', self.gf('models.IntegerField')(_("sort order"), editable=False))

        # Changing field 'FaqCategory.description_de'
        db.alter_column('faqs_faqcategory', 'description_de', self.gf('ExtendedTextField')(u'description', db_tablespace='', unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=8192, rel=None, unique_for_date=None))

        # Changing field 'FaqCategory.modified_date'
        db.alter_column('faqs_faqcategory', 'modified_date', self.gf('models.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'FaqCategory.container'
        db.alter_column('faqs_faqcategory', 'container_id', self.gf('models.ForeignKey')(orm['faqs.FaqContainer']))

        # Changing field 'FaqCategory.parent'
        db.alter_column('faqs_faqcategory', 'parent_id', self.gf('models.ForeignKey')(orm['faqs.FaqCategory'], null=True))

        # Changing field 'FaqCategory.title'
        db.alter_column('faqs_faqcategory', 'title', self.gf('MultilingualCharField')(_('title'), max_length=512))

        # Changing field 'FaqCategory.children_sort_order_format'
        db.alter_column('faqs_faqcategory', 'children_sort_order_format', self.gf('models.CharField')(_('format for child categories'), max_length=20, null=True))

        # Changing field 'FaqCategory.description'
        db.alter_column('faqs_faqcategory', 'description', self.gf('MultilingualTextField')(_('description'), max_length=8192))

        # Changing field 'FaqCategory.faqs_on_separate_page'
        db.alter_column('faqs_faqcategory', 'faqs_on_separate_page', self.gf('models.BooleanField')(_('separate page')))

        # Changing field 'FaqCategory.description_en'
        db.alter_column('faqs_faqcategory', 'description_en', self.gf('ExtendedTextField')(u'description', db_tablespace='', unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=8192, rel=None, unique_for_date=None))

        # Changing field 'FaqCategory.short_title'
        db.alter_column('faqs_faqcategory', 'short_title', self.gf('MultilingualCharField')(_('short title'), max_length=80))

        # Changing field 'FaqCategory.modifier'
        db.alter_column('faqs_faqcategory', 'modifier_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'QuestionAnswer.category'
        db.alter_column('faqs_questionanswer', 'category_id', self.gf('models.ForeignKey')(orm['faqs.FaqCategory']))

        # Changing field 'QuestionAnswer.modified_date'
        db.alter_column('faqs_questionanswer', 'modified_date', self.gf('models.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'QuestionAnswer.modifier'
        db.alter_column('faqs_questionanswer', 'modifier_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'QuestionAnswer.views'
        db.alter_column('faqs_questionanswer', 'views', self.gf('models.IntegerField')(_("views"), editable=False))

        # Changing field 'QuestionAnswer.creator'
        db.alter_column('faqs_questionanswer', 'creator_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'QuestionAnswer.question'
        db.alter_column('faqs_questionanswer', 'question', self.gf('MultilingualCharField')(_('question'), max_length=255))

        # Changing field 'QuestionAnswer.answer_de'
        db.alter_column('faqs_questionanswer', 'answer_de', self.gf('ExtendedTextField')(u'answer', db_tablespace='', unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=16384, rel=None, unique_for_date=None))

        # Changing field 'QuestionAnswer.creation_date'
        db.alter_column('faqs_questionanswer', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'QuestionAnswer.sort_order'
        db.alter_column('faqs_questionanswer', 'sort_order', self.gf('models.IntegerField')(_('sort order')))

        # Changing field 'QuestionAnswer.answer'
        db.alter_column('faqs_questionanswer', 'answer', self.gf('MultilingualTextField')(_('answer'), max_length=16384))

        # Changing field 'QuestionAnswer.answer_en'
        db.alter_column('faqs_questionanswer', 'answer_en', self.gf('ExtendedTextField')(u'answer', db_tablespace='', unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=16384, rel=None, unique_for_date=None))
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'ordering': "('username',)", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'faqs.faqcategory': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'FaqCategory'},
            'children_sort_order_format': ('django.db.models.fields.CharField', [], {'default': "'%02d'", 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'container': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['faqs.FaqContainer']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'faqcategory_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'max_length': '8192', 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Beschreibung'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '8192', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Beschreibung'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '8192', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'faqs_on_separate_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'faqcategory_modifier'", 'null': 'True', 'to': "orm['auth.User']"}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['faqs.FaqCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'short_title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '80', 'null': 'True'}),
            'short_title_de': ('django.db.models.fields.CharField', ["u'short title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'short_title_en': ('django.db.models.fields.CharField', ["u'short title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '80', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '512', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '512', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'faqs.faqcontainer': {
            'Meta': {'ordering': "('title',)", 'object_name': 'FaqContainer'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'sysname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'faqs.questionanswer': {
            'Meta': {'ordering': "['category']", 'object_name': 'QuestionAnswer'},
            'answer': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'max_length': '16384', 'null': 'True'}),
            'answer_de': ('base_libs.models.fields.ExtendedTextField', ["u'Antwort'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '16384', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'answer_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'answer_en': ('base_libs.models.fields.ExtendedTextField', ["u'Antwort'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': '16384', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'answer_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'answer_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'category': ('mptt.fields.TreeForeignKey', [], {'to': "orm['faqs.FaqCategory']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionanswer_creator'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questionanswer_modifier'", 'null': 'True', 'to': "orm['auth.User']"}),
            'question': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'question_de': ('django.db.models.fields.CharField', ["u'question'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'question_en': ('django.db.models.fields.CharField', ["u'question'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'permissions.rowlevelpermission': {
            'Meta': {'object_name': 'RowLevelPermission', 'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': "orm['contenttypes.ContentType']"}),
            'owner_object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Permission']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['faqs']
