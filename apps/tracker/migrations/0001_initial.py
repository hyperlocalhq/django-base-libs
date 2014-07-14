# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from ccb.apps.tracker.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Ticket'
        db.create_table('tracker_ticket', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], limit_choices_to={}, related_name=None, null=True, blank=True)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=True)),
            ('submitted_date', models.DateTimeField(_("submitted Date"), auto_now_add=True)),
            ('modified_date', models.DateTimeField(_("modified Date"), null=True, editable=False, blank=True)),
            ('submitter', models.ForeignKey(orm['auth.User'], related_name="ticket_submitter", null=True, blank=True)),
            ('submitter_name', models.CharField('name', max_length=80)),
            ('submitter_email', models.EmailField('email')),
            ('modifier', models.ForeignKey(orm['auth.User'], related_name="ticket_modifier", null=True, blank=True)),
            ('description', models.TextField(_("description"))),
            ('status', models.IntegerField(_("status"), default=1)),
            ('priority', models.IntegerField(_("priority"), default=1)),
            ('url', URLField(_("related object's URL"), max_length=255, null=True, blank=True)),
            ('concern', models.ForeignKey(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'ticket_types'})),
        )))
        db.send_create_signal('tracker', ['Ticket'])
        
        # Adding model 'TicketModifications'
        db.create_table('tracker_ticketmodifications', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('ticket', models.ForeignKey(orm.Ticket, related_name="ticket_modification")),
            ('modified_date', models.DateTimeField(_("modified Date"), editable=False)),
            ('modifier', models.ForeignKey(orm['auth.User'], editable=False, related_name="ticket_modification_modifier")),
            ('modification', models.TextField(_("modification"))),
            ('status', models.IntegerField(_("status"), default=1)),
            ('priority', models.IntegerField(_("priority"), default=1)),
        )))
        db.send_create_signal('tracker', ['TicketModifications'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Ticket'
        db.delete_table('tracker_ticket')
        
        # Deleting model 'TicketModifications'
        db.delete_table('tracker_ticketmodifications')
        
    
    
    models = {
        'tracker.ticket': {
            'Meta': {'ordering': "('-submitted_date',)"},
            'concern': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'ticket_types'}"}),
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'limit_choices_to': '{}', 'related_name': 'None', 'null': 'True', 'blank': 'True'}),
            'description': ('models.TextField', ['_("description")'], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('models.DateTimeField', ['_("modified Date")'], {'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"ticket_modifier"', 'null': 'True', 'blank': 'True'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'True'}),
            'priority': ('models.IntegerField', ['_("priority")'], {'default': '1'}),
            'status': ('models.IntegerField', ['_("status")'], {'default': '1'}),
            'submitted_date': ('models.DateTimeField', ['_("submitted Date")'], {'auto_now_add': 'True'}),
            'submitter': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"ticket_submitter"', 'null': 'True', 'blank': 'True'}),
            'submitter_email': ('models.EmailField', ["'email'"], {}),
            'submitter_name': ('models.CharField', ["'name'"], {'max_length': '80'}),
            'url': ('URLField', ['_("related object\'s URL")'], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'tracker.ticketmodifications': {
            'Meta': {'ordering': "('modified_date',)"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'modification': ('models.TextField', ['_("modification")'], {}),
            'modified_date': ('models.DateTimeField', ['_("modified Date")'], {'editable': 'False'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"ticket_modification_modifier"'}),
            'priority': ('models.IntegerField', ['_("priority")'], {'default': '1'}),
            'status': ('models.IntegerField', ['_("status")'], {'default': '1'}),
            'ticket': ('models.ForeignKey', ["orm['tracker.Ticket']"], {'related_name': '"ticket_modification"'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'structure.term': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['tracker']
