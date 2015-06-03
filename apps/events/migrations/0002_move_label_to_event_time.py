# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models, models as django_models
from jetson.apps.events.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'EventTime.label'
        db.add_column('events_eventtime', 'label', models.ForeignKey(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':"event_time_labels",}, related_name="label_event_types", null=True, blank=True))
        
        # Changing field 'Event.description_de'
        db.alter_column('events_event', 'description_de', ExtendedTextField(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False))
        
        # Changing field 'Event.description_en'
        db.alter_column('events_event', 'description_en', ExtendedTextField(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False))
        
        # Changing field 'Event.exceptions_de'
        db.alter_column('events_event', 'exceptions_de', ExtendedTextField(u'Exceptions for working hours', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False))
        
        # Changing field 'Event.exceptions_en'
        db.alter_column('events_event', 'exceptions_en', ExtendedTextField(u'Exceptions for working hours', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False))
        
        # Changing field 'Event.additional_info_en'
        db.alter_column('events_event', 'additional_info_en', ExtendedTextField(u'Additional Info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False))
        
        # Changing field 'Event.additional_info_de'
        db.alter_column('events_event', 'additional_info_de', ExtendedTextField(u'Additional Info', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'EventTime.label'
        db.delete_column('events_eventtime', 'label_id')
        
        # Changing field 'Event.description_de'
        db.alter_column('events_event', 'description_de', ExtendedTextField(u'Description', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        
        # Changing field 'Event.description_en'
        db.alter_column('events_event', 'description_en', ExtendedTextField(u'Description', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        
        # Changing field 'Event.exceptions_de'
        db.alter_column('events_event', 'exceptions_de', ExtendedTextField(u'Exceptions for working hours', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        
        # Changing field 'Event.exceptions_en'
        db.alter_column('events_event', 'exceptions_en', ExtendedTextField(u'Exceptions for working hours', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        
        # Changing field 'Event.additional_info_en'
        db.alter_column('events_event', 'additional_info_en', ExtendedTextField(u'Additional Info', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        
        # Changing field 'Event.additional_info_de'
        db.alter_column('events_event', 'additional_info_de', ExtendedTextField(u'Additional Info', unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, unique_for_date=None, db_tablespace='', db_index=False))
        
    
    
    models = {
        'optionset.phonetype': {
            'Meta': {'ordering': "['sort_order','title']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'events.event': {
            'additional_info': ('MultilingualTextField', ['_("Additional Info")'], {'blank': 'True'}),
            'additional_info_de': ('ExtendedTextField', ["u'Additional Info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'additional_info_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'additional_info_en': ('ExtendedTextField', ["u'Additional Info'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'additional_info_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'additional_info_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_creator"', 'null': 'True'}),
            'description': ('MultilingualTextField', ['_("Description")'], {'blank': 'True'}),
            'description_de': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'email0_address': ('models.CharField', ['_("Email Address")'], {'max_length': '255', 'blank': 'True'}),
            'email0_type': ('models.ForeignKey', ["orm['optionset.EmailType']"], {'related_name': "'events0'", 'null': 'True', 'blank': 'True'}),
            'email1_address': ('models.CharField', ['_("Email Address")'], {'max_length': '255', 'blank': 'True'}),
            'email1_type': ('models.ForeignKey', ["orm['optionset.EmailType']"], {'related_name': "'events1'", 'null': 'True', 'blank': 'True'}),
            'email2_address': ('models.CharField', ['_("Email Address")'], {'max_length': '255', 'blank': 'True'}),
            'email2_type': ('models.ForeignKey', ["orm['optionset.EmailType']"], {'related_name': "'events2'", 'null': 'True', 'blank': 'True'}),
            'end': ('models.DateTimeField', ['_("End")'], {'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'event_type': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': 'models.Q(vocabulary__sysname=\'basics_object_types\',path_search__contains=ObjectTypeFilter("event"))&~models.Q(models.Q(sysname="event"))', 'related_name': '"type_events"'}),
            'exceptions': ('MultilingualTextField', ["_('Exceptions for working hours')"], {'blank': 'True'}),
            'exceptions_de': ('ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_de_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_en': ('ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_en_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_markup_type': ('models.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'fri_break_close': ('models.TimeField', ["_('Break Starts on Friday')"], {'null': 'True', 'blank': 'True'}),
            'fri_break_open': ('models.TimeField', ["_('Break Ends on Friday')"], {'null': 'True', 'blank': 'True'}),
            'fri_close': ('models.TimeField', ["_('Closes on Friday')"], {'null': 'True', 'blank': 'True'}),
            'fri_open': ('models.TimeField', ["_('Opens on Friday')"], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'im0_address': ('models.CharField', ['_("Instant Messenger")'], {'max_length': '255', 'blank': 'True'}),
            'im0_type': ('models.ForeignKey', ["orm['optionset.IMType']"], {'related_name': "'events0'", 'null': 'True', 'blank': 'True'}),
            'im1_address': ('models.CharField', ['_("Instant Messenger")'], {'max_length': '255', 'blank': 'True'}),
            'im1_type': ('models.ForeignKey', ["orm['optionset.IMType']"], {'related_name': "'events1'", 'null': 'True', 'blank': 'True'}),
            'im2_address': ('models.CharField', ['_("Instant Messenger")'], {'max_length': '255', 'blank': 'True'}),
            'im2_type': ('models.ForeignKey', ["orm['optionset.IMType']"], {'related_name': "'events2'", 'null': 'True', 'blank': 'True'}),
            'image': ('FileBrowseField', ["_('Image')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '200', 'directory': '"/%s/"%URL_ID_EVENTS', 'blank': 'True'}),
            'is_appointment_based': ('models.BooleanField', ['_("Visiting by Appointment")'], {'default': 'False'}),
            'is_email0_default': ('models.BooleanField', ['_("Default?")'], {'default': 'True'}),
            'is_email0_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_email1_default': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_email1_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_email2_default': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_email2_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_im0_default': ('models.BooleanField', ['_("Default?")'], {'default': 'True'}),
            'is_im0_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_im1_default': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_im1_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_im2_default': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_im2_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_phone0_default': ('models.BooleanField', ['_("Default?")'], {'default': 'True'}),
            'is_phone0_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_phone1_default': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_phone1_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_phone2_default': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_phone2_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_url0_default': ('models.BooleanField', ['_("Default?")'], {'default': 'True'}),
            'is_url0_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_url1_default': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_url1_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_url2_default': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_url2_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'modifier': ('models.ForeignKey', ["orm['auth.User']"], {'editable': 'False', 'related_name': '"%(class)s_modifier"', 'null': 'True'}),
            'mon_break_close': ('models.TimeField', ["_('Break Starts on Monday')"], {'null': 'True', 'blank': 'True'}),
            'mon_break_open': ('models.TimeField', ["_('Break Ends on Monday')"], {'null': 'True', 'blank': 'True'}),
            'mon_close': ('models.TimeField', ["_('Closes on Monday')"], {'null': 'True', 'blank': 'True'}),
            'mon_open': ('models.TimeField', ["_('Opens on Monday')"], {'null': 'True', 'blank': 'True'}),
            'organizer_title': ('models.TextField', ['_("Organizer")'], {'null': 'True', 'blank': 'True'}),
            'organizer_url_link': ('URLField', ['_("Organizer URL")'], {'null': 'True', 'blank': 'True'}),
            'phone0_area': ('models.CharField', ['_("Area Code")'], {'default': "'30'", 'max_length': '5', 'blank': 'True'}),
            'phone0_country': ('models.CharField', ['_("Country Code")'], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone0_number': ('models.CharField', ['_("Subscriber Number and Extension")'], {'max_length': '15', 'blank': 'True'}),
            'phone0_type': ('models.ForeignKey', ["orm['optionset.PhoneType']"], {'default': 'DefaultPhoneType("default")', 'related_name': "'events0'", 'null': 'True', 'blank': 'True'}),
            'phone1_area': ('models.CharField', ['_("Area Code")'], {'default': "'30'", 'max_length': '5', 'blank': 'True'}),
            'phone1_country': ('models.CharField', ['_("Country Code")'], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone1_number': ('models.CharField', ['_("Subscriber Number and Extension")'], {'max_length': '15', 'blank': 'True'}),
            'phone1_type': ('models.ForeignKey', ["orm['optionset.PhoneType']"], {'default': 'DefaultPhoneType("fax")', 'related_name': "'events1'", 'null': 'True', 'blank': 'True'}),
            'phone2_area': ('models.CharField', ['_("Area Code")'], {'max_length': '5', 'blank': 'True'}),
            'phone2_country': ('models.CharField', ['_("Country Code")'], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone2_number': ('models.CharField', ['_("Subscriber Number and Extension")'], {'max_length': '15', 'blank': 'True'}),
            'phone2_type': ('models.ForeignKey', ["orm['optionset.PhoneType']"], {'default': 'DefaultPhoneType("mobile")', 'related_name': "'events2'", 'null': 'True', 'blank': 'True'}),
            'postal_address': ('models.ForeignKey', ["orm['location.Address']"], {'related_name': '"address_events"', 'null': 'True', 'blank': 'True'}),
            'related_events': ('models.ManyToManyField', ["orm['events.Event']"], {'symmetrical': 'True', 'blank': 'True'}),
            'sat_break_close': ('models.TimeField', ["_('Break Starts on Saturday')"], {'null': 'True', 'blank': 'True'}),
            'sat_break_open': ('models.TimeField', ["_('Break Ends on Saturday')"], {'null': 'True', 'blank': 'True'}),
            'sat_close': ('models.TimeField', ["_('Closes on Saturday')"], {'null': 'True', 'blank': 'True'}),
            'sat_open': ('models.TimeField', ["_('Opens on Saturday')"], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.CharField', ['_("Slug for URIs")'], {'max_length': '255'}),
            'start': ('models.DateTimeField', ['_("Start")'], {'null': 'True', 'editable': 'False', 'blank': 'True'}),
            'status': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_object_statuses'}", 'related_name': '"status_events"', 'default': 'DefaultObjectStatus("draft")', 'blank': 'True', 'null': 'True'}),
            'sun_break_close': ('models.TimeField', ["_('Break Starts on Sunday')"], {'null': 'True', 'blank': 'True'}),
            'sun_break_open': ('models.TimeField', ["_('Break Ends on Sunday')"], {'null': 'True', 'blank': 'True'}),
            'sun_close': ('models.TimeField', ["_('Closes on Sunday')"], {'null': 'True', 'blank': 'True'}),
            'sun_open': ('models.TimeField', ["_('Opens on Sunday')"], {'null': 'True', 'blank': 'True'}),
            'thu_break_close': ('models.TimeField', ["_('Break Starts on Thursday')"], {'null': 'True', 'blank': 'True'}),
            'thu_break_open': ('models.TimeField', ["_('Break Ends on Thursday')"], {'null': 'True', 'blank': 'True'}),
            'thu_close': ('models.TimeField', ["_('Closes on Thursday')"], {'null': 'True', 'blank': 'True'}),
            'thu_open': ('models.TimeField', ["_('Opens on Thursday')"], {'null': 'True', 'blank': 'True'}),
            'title': ('MultilingualCharField', ['_("Title")'], {'max_length': '255'}),
            'title_de': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('models.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'tue_break_close': ('models.TimeField', ["_('Break Starts on Tuesday')"], {'null': 'True', 'blank': 'True'}),
            'tue_break_open': ('models.TimeField', ["_('Break Ends on Tuesday')"], {'null': 'True', 'blank': 'True'}),
            'tue_close': ('models.TimeField', ["_('Closes on Tuesday')"], {'null': 'True', 'blank': 'True'}),
            'tue_open': ('models.TimeField', ["_('Opens on Tuesday')"], {'null': 'True', 'blank': 'True'}),
            'url0_link': ('URLField', ['_("URL")'], {'blank': 'True'}),
            'url0_type': ('models.ForeignKey', ["orm['optionset.URLType']"], {'related_name': "'events0'", 'null': 'True', 'blank': 'True'}),
            'url1_link': ('URLField', ['_("URL")'], {'blank': 'True'}),
            'url1_type': ('models.ForeignKey', ["orm['optionset.URLType']"], {'related_name': "'events1'", 'null': 'True', 'blank': 'True'}),
            'url2_link': ('URLField', ['_("URL")'], {'blank': 'True'}),
            'url2_type': ('models.ForeignKey', ["orm['optionset.URLType']"], {'related_name': "'events2'", 'null': 'True', 'blank': 'True'}),
            'venue_title': ('models.CharField', ['_("Title")'], {'max_length': '255', 'blank': 'True'}),
            'wed_break_close': ('models.TimeField', ["_('Break Starts on Wednesday')"], {'null': 'True', 'blank': 'True'}),
            'wed_break_open': ('models.TimeField', ["_('Break Ends on Wednesday')"], {'null': 'True', 'blank': 'True'}),
            'wed_close': ('models.TimeField', ["_('Closes on Wednesday')"], {'null': 'True', 'blank': 'True'}),
            'wed_open': ('models.TimeField', ["_('Opens on Wednesday')"], {'null': 'True', 'blank': 'True'})
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
            'label': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': '{\'vocabulary__sysname\':"event_time_labels",}', 'related_name': '"label_event_types"', 'null': 'True', 'blank': 'True'}),
            'start': ('models.DateTimeField', ['_("Start")'], {'editable': 'False'}),
            'start_dd': ('models.SmallIntegerField', ['_("Start Day")'], {'null': 'True', 'blank': 'True'}),
            'start_hh': ('models.SmallIntegerField', ['_("Start Hour")'], {'null': 'True', 'blank': 'True'}),
            'start_ii': ('models.SmallIntegerField', ['_("Start Minute")'], {'null': 'True', 'blank': 'True'}),
            'start_mm': ('models.SmallIntegerField', ['_("Start Month")'], {'null': 'True', 'blank': 'True'}),
            'start_yyyy': ('models.IntegerField', ['_("Start Year")'], {'default': '2009'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'optionset.emailtype': {
            'Meta': {'ordering': "['sort_order','title']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'location.address': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'optionset.urltype': {
            'Meta': {'ordering': "['sort_order','title']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'structure.term': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'optionset.imtype': {
            'Meta': {'ordering': "['sort_order','title']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    # if institutions app is installed, add venue and organizing_institution
    if django_models.get_model("institutions", "Institution"):
        models['institutions.institution'] = {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
        models['events.event']['venue'] = ('models.ForeignKey', ["orm['institutions.Institution']"], {'related_name': '"events_happened"', 'null': 'True', 'blank': 'True'})
        models['events.event']['organizing_institution'] = ('models.ForeignKey', ["orm['institutions.Institution']"], {'null': 'True', 'blank': 'True'})
        
    # if people app is installed, add organizing_person
    if django_models.get_model("people", "Person"):
        models['people.person'] = {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
        models['events.event']['organizing_person'] = ('models.ForeignKey', ["orm['people.Person']"], {'related_name': '"events_organized"', 'null': 'True', 'blank': 'True'})
    south_clean_multilingual_fields(models)
    
    complete_apps = ['events']
