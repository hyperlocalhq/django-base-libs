# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from basic_project.apps.events.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Event'
        db.create_table('events_event', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('creator', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_creator", null=True)),
            ('modifier', models.ForeignKey(orm['auth.User'], editable=False, related_name="%(class)s_modifier", null=True)),
            ('title', MultilingualCharField(_("Title"), max_length=255)),
            ('slug', models.CharField(_("Slug for URIs"), max_length=255)),
            ('description', MultilingualTextField(_("Description"), blank=True)),
            ('image', FileBrowseField(_('Image'), extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff'], max_length=200, directory="/%s/"%URL_ID_EVENTS, blank=True)),
            ('start', models.DateTimeField(_("Start"), null=True, editable=False, blank=True)),
            ('end', models.DateTimeField(_("End"), null=True, editable=False, blank=True)),
            ('status', models.ForeignKey(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_object_statuses'}, related_name="status_events", default=DefaultObjectStatus("draft"), blank=True, null=True)),
            ('title_de', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('title_en', models.CharField(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=False, unique=False, db_index=False)),
            ('description_de', ExtendedTextField(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('description_de_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_en', ExtendedTextField(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('description_en_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
            ('description_markup_type', models.CharField('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal('events', ['Event'])
        
        # Adding model 'EventTime'
        db.create_table('events_eventtime', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('start_yyyy', models.IntegerField(_("Start Year"), default=2009)),
            ('start_mm', models.SmallIntegerField(_("Start Month"), null=True, blank=True)),
            ('start_dd', models.SmallIntegerField(_("Start Day"), null=True, blank=True)),
            ('start_hh', models.SmallIntegerField(_("Start Hour"), null=True, blank=True)),
            ('start_ii', models.SmallIntegerField(_("Start Minute"), null=True, blank=True)),
            ('start', models.DateTimeField(_("Start"), editable=False)),
            ('end_yyyy', models.IntegerField(_("End Year"), blank=True, null=True)),
            ('end_mm', models.SmallIntegerField(_("End Month"), null=True, blank=True)),
            ('end_dd', models.SmallIntegerField(_("End Day"), null=True, blank=True)),
            ('end_hh', models.SmallIntegerField(_("End Hour"), null=True, blank=True)),
            ('end_ii', models.SmallIntegerField(_("End Minute"), null=True, blank=True)),
            ('end', models.DateTimeField(_("Start"), editable=False)),
            ('is_all_day', models.BooleanField(_("All Day Event"), default=False)),
            ('event', models.ForeignKey(orm['events.event'])),
        )))
        db.send_create_signal('events', ['EventTime'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Event'
        db.delete_table('events_event')
        
        # Deleting model 'EventTime'
        db.delete_table('events_eventtime')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'events.event': {
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_creator"', 'null': 'True'}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'end': ('models.DateTimeField', ['_("End")'], {'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ["_('Image')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '200', 'directory': '"/%s/"%URL_ID_EVENTS', 'blank': 'True'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_modifier"', 'null': 'True'}),
            'slug': ('models.CharField', ['_("Slug for URIs")'], {'max_length': '255'}),
            'start': ('models.DateTimeField', ['_("Start")'], {'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'status': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_object_statuses'}", 'related_name': '"status_events"', 'default': 'DefaultObjectStatus("draft")', 'blank': 'True', 'null': 'True'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'events.eventtime': {
            'end': ('models.DateTimeField', ['_("Start")'], {'editable': 'False'}),
            'end_dd': ('models.SmallIntegerField', ['_("End Day")'], {'null': 'True', 'blank': 'True'}),
            'end_hh': ('models.SmallIntegerField', ['_("End Hour")'], {'null': 'True', 'blank': 'True'}),
            'end_ii': ('models.SmallIntegerField', ['_("End Minute")'], {'null': 'True', 'blank': 'True'}),
            'end_mm': ('models.SmallIntegerField', ['_("End Month")'], {'null': 'True', 'blank': 'True'}),
            'end_yyyy': ('models.IntegerField', ['_("End Year")'], {'blank': 'True', 'null': 'True'}),
            'event': ('models.ForeignKey', ["orm['events.event']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_all_day': ('models.BooleanField', ['_("All Day Event")'], {'default': 'False'}),
            'start': ('models.DateTimeField', ['_("Start")'], {'editable': 'False'}),
            'start_dd': ('models.SmallIntegerField', ['_("Start Day")'], {'null': 'True', 'blank': 'True'}),
            'start_hh': ('models.SmallIntegerField', ['_("Start Hour")'], {'null': 'True', 'blank': 'True'}),
            'start_ii': ('models.SmallIntegerField', ['_("Start Minute")'], {'null': 'True', 'blank': 'True'}),
            'start_mm': ('models.SmallIntegerField', ['_("Start Month")'], {'null': 'True', 'blank': 'True'}),
            'start_yyyy': ('models.IntegerField', ['_("Start Year")'], {'default': '2009'})
        },
        'structure.term': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['events']
