# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'DigestNotice'
        db.create_table('notification_digestnotice', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('digest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notification.Digest'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('notice_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notification.NoticeType'])),
        )))
        db.send_create_signal('notification', ['DigestNotice'])

        # Adding model 'Digest'
        db.create_table('notification_digest', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('is_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        )))
        db.send_create_signal('notification', ['Digest'])

        # Adding field 'NoticeSetting.frequency'
        db.add_column('notification_noticesetting', 'frequency', self.gf('django.db.models.fields.CharField')(default='never', max_length=15), keep_default=False)

        # Changing field 'NoticeSetting.notice_type'
        db.alter_column('notification_noticesetting', 'notice_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notification.NoticeType']))

        # Changing field 'NoticeSetting.medium'
        db.alter_column('notification_noticesetting', 'medium', self.gf('django.db.models.fields.CharField')(max_length=1))

        # Changing field 'NoticeSetting.user'
        db.alter_column('notification_noticesetting', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'NoticeSetting.send'
        db.alter_column('notification_noticesetting', 'send', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'NoticeTypeCategory.is_public'
        db.alter_column('notification_noticetypecategory', 'is_public', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'NoticeTypeCategory.title'
        db.alter_column('notification_noticetypecategory', 'title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=50, null=True))

        # Changing field 'NoticeEmailTemplate.emailtemplate_ptr'
        db.alter_column('notification_noticeemailtemplate', 'emailtemplate_ptr_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mailing.EmailTemplate'], unique=True, primary_key=True))

        # Changing field 'NoticeType.category'
        db.alter_column('notification_noticetype', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notification.NoticeTypeCategory'], null=True))

        # Changing field 'NoticeType.description'
        db.alter_column('notification_noticetype', 'description', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=100, null=True))

        # Changing field 'NoticeType.default'
        db.alter_column('notification_noticetype', 'default', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'NoticeType.message_template'
        db.alter_column('notification_noticetype', 'message_template', self.gf('base_libs.models.fields.MultilingualPlainTextField')(null=True))

        # Changing field 'NoticeType.is_public'
        db.alter_column('notification_noticetype', 'is_public', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'NoticeType.message_template_en'
        db.alter_column('notification_noticetype', 'message_template_en', self.gf('base_libs.models.fields.PlainTextModelField')(u'Nachrichten Vorlage', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'NoticeType.display'
        db.alter_column('notification_noticetype', 'display', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=50, null=True))

        # Changing field 'NoticeType.message_template_de'
        db.alter_column('notification_noticetype', 'message_template_de', self.gf('base_libs.models.fields.PlainTextModelField')(u'Nachrichten Vorlage', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, unique=False, db_tablespace=''))

        # Changing field 'Notice.archived'
        db.alter_column('notification_notice', 'archived', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Notice.added'
        db.alter_column('notification_notice', 'added', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Notice.notice_type'
        db.alter_column('notification_notice', 'notice_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notification.NoticeType']))

        # Changing field 'Notice.user'
        db.alter_column('notification_notice', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'Notice.unseen'
        db.alter_column('notification_notice', 'unseen', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'Notice.message'
        db.alter_column('notification_notice', 'message', self.gf('django.db.models.fields.TextField')())

        # Changing field 'ObservedItem.added'
        db.alter_column('notification_observeditem', 'added', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'ObservedItem.notice_type'
        db.alter_column('notification_observeditem', 'notice_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notification.NoticeType']))

        # Changing field 'ObservedItem.user'
        db.alter_column('notification_observeditem', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

        # Changing field 'ObservedItem.content_type'
        db.alter_column('notification_observeditem', 'content_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))
    
    
    def backwards(self, orm):
        
        # Deleting model 'DigestNotice'
        db.delete_table('notification_digestnotice')

        # Deleting model 'Digest'
        db.delete_table('notification_digest')

        # Deleting field 'NoticeSetting.frequency'
        db.delete_column('notification_noticesetting', 'frequency')

        # Changing field 'NoticeSetting.notice_type'
        db.alter_column('notification_noticesetting', 'notice_type_id', self.gf('models.ForeignKey')(orm['notification.NoticeType']))

        # Changing field 'NoticeSetting.medium'
        db.alter_column('notification_noticesetting', 'medium', self.gf('models.CharField')(_('medium'), max_length=1))

        # Changing field 'NoticeSetting.user'
        db.alter_column('notification_noticesetting', 'user_id', self.gf('models.ForeignKey')(orm['auth.User']))

        # Changing field 'NoticeSetting.send'
        db.alter_column('notification_noticesetting', 'send', self.gf('models.BooleanField')(_('send')))

        # Changing field 'NoticeTypeCategory.is_public'
        db.alter_column('notification_noticetypecategory', 'is_public', self.gf('models.BooleanField')(_('is this category displayed in the public notification settings?')))

        # Changing field 'NoticeTypeCategory.title'
        db.alter_column('notification_noticetypecategory', 'title', self.gf('MultilingualCharField')(_('display'), max_length=50))

        # Changing field 'NoticeEmailTemplate.emailtemplate_ptr'
        db.alter_column('notification_noticeemailtemplate', 'emailtemplate_ptr_id', self.gf('models.OneToOneField')(orm['mailing.EmailTemplate']))

        # Changing field 'NoticeType.category'
        db.alter_column('notification_noticetype', 'category_id', self.gf('models.ForeignKey')(orm['notification.NoticeTypeCategory'], null=True))

        # Changing field 'NoticeType.description'
        db.alter_column('notification_noticetype', 'description', self.gf('MultilingualCharField')(_('description'), max_length=100))

        # Changing field 'NoticeType.default'
        db.alter_column('notification_noticetype', 'default', self.gf('models.IntegerField')(_('default')))

        # Changing field 'NoticeType.message_template'
        db.alter_column('notification_noticetype', 'message_template', self.gf('MultilingualPlainTextField')(_("Message Template")))

        # Changing field 'NoticeType.is_public'
        db.alter_column('notification_noticetype', 'is_public', self.gf('models.BooleanField')(_('is this notice type displayed in the public notification settings?')))

        # Changing field 'NoticeType.message_template_en'
        db.alter_column('notification_noticetype', 'message_template_en', self.gf('PlainTextModelField')(u'Message Template', rel=None, unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, db_tablespace='', unique_for_date=None))

        # Changing field 'NoticeType.display'
        db.alter_column('notification_noticetype', 'display', self.gf('MultilingualCharField')(_('display'), max_length=50))

        # Changing field 'NoticeType.message_template_de'
        db.alter_column('notification_noticetype', 'message_template_de', self.gf('PlainTextModelField')(u'Message Template', rel=None, unique_for_year=None, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, db_tablespace='', unique_for_date=None))

        # Changing field 'Notice.archived'
        db.alter_column('notification_notice', 'archived', self.gf('models.BooleanField')(_('archived')))

        # Changing field 'Notice.added'
        db.alter_column('notification_notice', 'added', self.gf('models.DateTimeField')(_('added')))

        # Changing field 'Notice.notice_type'
        db.alter_column('notification_notice', 'notice_type_id', self.gf('models.ForeignKey')(orm['notification.NoticeType']))

        # Changing field 'Notice.user'
        db.alter_column('notification_notice', 'user_id', self.gf('models.ForeignKey')(orm['auth.User']))

        # Changing field 'Notice.unseen'
        db.alter_column('notification_notice', 'unseen', self.gf('models.BooleanField')(_('unseen')))

        # Changing field 'Notice.message'
        db.alter_column('notification_notice', 'message', self.gf('models.TextField')(_('message')))

        # Changing field 'ObservedItem.added'
        db.alter_column('notification_observeditem', 'added', self.gf('models.DateTimeField')(_('added')))

        # Changing field 'ObservedItem.notice_type'
        db.alter_column('notification_observeditem', 'notice_type_id', self.gf('models.ForeignKey')(orm['notification.NoticeType']))

        # Changing field 'ObservedItem.user'
        db.alter_column('notification_observeditem', 'user_id', self.gf('models.ForeignKey')(orm['auth.User']))

        # Changing field 'ObservedItem.content_type'
        db.alter_column('notification_observeditem', 'content_type_id', self.gf('models.ForeignKey')(orm['contenttypes.ContentType'], null=False))
    
    
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
        'mailing.emailtemplate': {
            'Meta': {'object_name': 'EmailTemplate'},
            'allowed_placeholders': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['mailing.EmailTemplatePlaceholder']", 'null': 'True', 'blank': 'True'}),
            'body': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'body_de': ('base_libs.models.fields.PlainTextModelField', [], {'blank': 'True'}),
            'body_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'body_html_de': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subject_de': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'mailing.emailtemplateplaceholder': {
            'Meta': {'object_name': 'EmailTemplatePlaceholder'},
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '64', 'unique': 'True', 'null': 'True'}),
            'name_de': ('django.db.models.fields.CharField', ["u'Placeholder Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '64', 'db_tablespace': "''", 'blank': 'True', 'unique': 'True', 'db_index': 'False'}),
            'name_en': ('django.db.models.fields.CharField', ["u'Placeholder Name'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '64', 'db_tablespace': "''", 'blank': 'True', 'unique': 'True', 'db_index': 'False'}),
            'relates_to': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'notification.digest': {
            'Meta': {'object_name': 'Digest'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'notification.digestnotice': {
            'Meta': {'ordering': "['creation_date']", 'object_name': 'DigestNotice'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'digest': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notification.Digest']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'notice_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notification.NoticeType']"})
        },
        'notification.notice': {
            'Meta': {'ordering': "['-added']", 'object_name': 'Notice'},
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'notice_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notification.NoticeType']"}),
            'unseen': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'notification.noticeemailtemplate': {
            'Meta': {'object_name': 'NoticeEmailTemplate', '_ormbases': ['mailing.EmailTemplate']},
            'emailtemplate_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['mailing.EmailTemplate']", 'unique': 'True', 'primary_key': 'True'})
        },
        'notification.noticesetting': {
            'Meta': {'object_name': 'NoticeSetting'},
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'notice_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notification.NoticeType']"}),
            'send': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'notification.noticetype': {
            'Meta': {'ordering': "('category__title', 'display')", 'object_name': 'NoticeType'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notification.NoticeTypeCategory']", 'null': 'True', 'blank': 'True'}),
            'default': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '100', 'null': 'True'}),
            'description_de': ('django.db.models.fields.CharField', ["u'description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'description_en': ('django.db.models.fields.CharField', ["u'description'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '100', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'display': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '50', 'null': 'True'}),
            'display_de': ('django.db.models.fields.CharField', ["u'display'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'display_en': ('django.db.models.fields.CharField', ["u'display'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'message_template': ('base_libs.models.fields.MultilingualPlainTextField', [], {'default': "''", 'null': 'True'}),
            'message_template_de': ('base_libs.models.fields.PlainTextModelField', ["u'Nachrichten Vorlage'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'message_template_en': ('base_libs.models.fields.PlainTextModelField', ["u'Nachrichten Vorlage'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'notification.noticetypecategory': {
            'Meta': {'ordering': "('title',)", 'object_name': 'NoticeTypeCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '50', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'display'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'display'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '50', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        'notification.observeditem': {
            'Meta': {'ordering': "['-added']", 'object_name': 'ObservedItem'},
            'added': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notice_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notification.NoticeType']"}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'signal': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
    
    complete_apps = ['notification']
