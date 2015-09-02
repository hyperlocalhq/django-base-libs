# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'InternalMessage.body'
        db.alter_column(u'messaging_internalmessage', 'body', self.gf('base_libs.models.fields.ExtendedTextField')())

        # Changing field 'InternalMessage.modified_date'
        db.alter_column(u'messaging_internalmessage', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'InternalMessage.is_deleted'
        db.alter_column(u'messaging_internalmessage', 'is_deleted', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InternalMessage.sender'
        db.alter_column(u'messaging_internalmessage', 'sender_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'InternalMessage.creator'
        db.alter_column(u'messaging_internalmessage', 'creator_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'InternalMessage.is_replied'
        db.alter_column(u'messaging_internalmessage', 'is_replied', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InternalMessage.recipient'
        db.alter_column(u'messaging_internalmessage', 'recipient_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'InternalMessage.subject'
        db.alter_column(u'messaging_internalmessage', 'subject', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'InternalMessage.creation_date'
        db.alter_column(u'messaging_internalmessage', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'InternalMessage.is_read'
        db.alter_column(u'messaging_internalmessage', 'is_read', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InternalMessage.modifier'
        db.alter_column(u'messaging_internalmessage', 'modifier_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'InternalMessage.is_draft'
        db.alter_column(u'messaging_internalmessage', 'is_draft', self.gf('django.db.models.fields.BooleanField')())

        # Changing field 'InternalMessage.is_spam'
        db.alter_column(u'messaging_internalmessage', 'is_spam', self.gf('django.db.models.fields.BooleanField')())
    
    
    def backwards(self, orm):
        
        # Changing field 'InternalMessage.body'
        db.alter_column(u'messaging_internalmessage', 'body', self.gf('ExtendedTextField')(_("Message")))

        # Changing field 'InternalMessage.modified_date'
        db.alter_column(u'messaging_internalmessage', 'modified_date', self.gf('models.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'InternalMessage.is_deleted'
        db.alter_column(u'messaging_internalmessage', 'is_deleted', self.gf('models.BooleanField')(_("Deleted")))

        # Changing field 'InternalMessage.sender'
        db.alter_column(u'messaging_internalmessage', 'sender_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True))

        # Changing field 'InternalMessage.creator'
        db.alter_column(u'messaging_internalmessage', 'creator_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'InternalMessage.is_replied'
        db.alter_column(u'messaging_internalmessage', 'is_replied', self.gf('models.BooleanField')(_("Replied")))

        # Changing field 'InternalMessage.recipient'
        db.alter_column(u'messaging_internalmessage', 'recipient_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True))

        # Changing field 'InternalMessage.subject'
        db.alter_column(u'messaging_internalmessage', 'subject', self.gf('models.CharField')(_("Subject"), max_length=255))

        # Changing field 'InternalMessage.creation_date'
        db.alter_column(u'messaging_internalmessage', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'InternalMessage.is_read'
        db.alter_column(u'messaging_internalmessage', 'is_read', self.gf('models.BooleanField')(_("Read")))

        # Changing field 'InternalMessage.modifier'
        db.alter_column(u'messaging_internalmessage', 'modifier_id', self.gf('models.ForeignKey')(orm['auth.User'], null=True, editable=False))

        # Changing field 'InternalMessage.is_draft'
        db.alter_column(u'messaging_internalmessage', 'is_draft', self.gf('models.BooleanField')(_("Draft")))

        # Changing field 'InternalMessage.is_spam'
        db.alter_column(u'messaging_internalmessage', 'is_spam', self.gf('models.BooleanField')(_("Spam")))
    
    
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 2, 16, 16, 30, 791906)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 7, 2, 16, 16, 30, 791298)'}),
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
        u'messaging.internalmessage': {
            'Meta': {'ordering': "('-creation_date', 'subject')", 'object_name': 'InternalMessage'},
            'body': ('base_libs.models.fields.ExtendedTextField', [], {'blank': 'True'}),
            'body_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'internalmessage_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_draft': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_replied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_spam': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'internalmessage_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'recipient': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'received_message_set'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sent_message_set'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['messaging']
