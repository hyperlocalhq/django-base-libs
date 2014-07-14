# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from ccb.apps.institutions.models import *
from base_libs.utils.misc import south_clean_multilingual_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Institution'
        db.create_table('institutions_institution', (
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('title', models.CharField(_("Title"), max_length=255)),
            ('title2', models.CharField(_("Title (second line)"), max_length=255, blank=True)),
            ('slug', models.CharField(_("Slug"), max_length=255)),
            ('parent', models.ForeignKey(orm.Institution, null=True, blank=True)),
            ('description', models.TextField(_("Description (English)"), blank=True)),
            ('description_de', models.TextField(_("Description (German)"), blank=True)),
            ('image', FileBrowseField(_('Image'), extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff'], max_length=255, directory="/%s/"%URL_ID_INSTITUTIONS, blank=True)),
            ('status', models.ForeignKey(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_object_statuses'}, related_name="status_institution_set", default=DefaultObjectStatus("draft"), blank=True, null=True)),
            ('legal_form', models.ForeignKey(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_legal_form'}, related_name="legal_form_institution", null=True, blank=True)),
            ('access', models.CharField(_("Access"), max_length=255, blank=True)),
            ('is_parking_avail', models.BooleanField(_("Is parking available?"), default=False)),
            ('is_wlan_avail', models.BooleanField(_("Is WLAN Internet available?"), default=False)),
            ('is_non_profit', models.BooleanField(_("Non profit (business elsewhere)?"), default=False)),
            ('tax_id_number', models.CharField(_("Tax ID"), max_length=100, blank=True)),
            ('vat_id_number', models.CharField(_("VAT ID"), max_length=100, blank=True)),
            ('is_card_visa_ok', models.BooleanField(_("Visa"), default=False)),
            ('is_card_mastercard_ok', models.BooleanField(_("MasterCard"), default=False)),
            ('is_card_americanexpress_ok', models.BooleanField(_("American Express"), default=False)),
            ('is_paypal_ok', models.BooleanField(_("PayPal"), default=False)),
            ('is_cash_ok', models.BooleanField(_("Cash"), default=False)),
            ('is_transaction_ok', models.BooleanField(_("Bank transfer"), default=False)),
            ('is_prepayment_ok', models.BooleanField(_("Prepayment"), default=False)),
            ('is_on_delivery_ok', models.BooleanField(_("Payment on delivery"), default=False)),
            ('is_invoice_ok', models.BooleanField(_("Invoice"), default=False)),
            ('is_ec_maestro_ok', models.BooleanField(_("EC Maestro"), default=False)),
            ('is_giropay_ok', models.BooleanField(_("Giropay"), default=False)),
            ('is_appointment_based', models.BooleanField(_("Visiting by Appointment"), default=False)),
            ('mon_open', models.TimeField(_('Opens on Monday'), null=True, blank=True)),
            ('mon_break_close', models.TimeField(_('Break Starts on Monday'), null=True, blank=True)),
            ('mon_break_open', models.TimeField(_('Break Ends on Monday'), null=True, blank=True)),
            ('mon_close', models.TimeField(_('Closes on Monday'), null=True, blank=True)),
            ('tue_open', models.TimeField(_('Opens on Tuesday'), null=True, blank=True)),
            ('tue_break_close', models.TimeField(_('Break Starts on Tuesday'), null=True, blank=True)),
            ('tue_break_open', models.TimeField(_('Break Ends on Tuesday'), null=True, blank=True)),
            ('tue_close', models.TimeField(_('Closes on Tuesday'), null=True, blank=True)),
            ('wed_open', models.TimeField(_('Opens on Wednesday'), null=True, blank=True)),
            ('wed_break_close', models.TimeField(_('Break Starts on Wednesday'), null=True, blank=True)),
            ('wed_break_open', models.TimeField(_('Break Ends on Wednesday'), null=True, blank=True)),
            ('wed_close', models.TimeField(_('Closes on Wednesday'), null=True, blank=True)),
            ('thu_open', models.TimeField(_('Opens on Thursday'), null=True, blank=True)),
            ('thu_break_close', models.TimeField(_('Break Starts on Thursday'), null=True, blank=True)),
            ('thu_break_open', models.TimeField(_('Break Ends on Thursday'), null=True, blank=True)),
            ('thu_close', models.TimeField(_('Closes on Thursday'), null=True, blank=True)),
            ('fri_open', models.TimeField(_('Opens on Friday'), null=True, blank=True)),
            ('fri_break_close', models.TimeField(_('Break Starts on Friday'), null=True, blank=True)),
            ('fri_break_open', models.TimeField(_('Break Ends on Friday'), null=True, blank=True)),
            ('fri_close', models.TimeField(_('Closes on Friday'), null=True, blank=True)),
            ('sat_open', models.TimeField(_('Opens on Saturday'), null=True, blank=True)),
            ('sat_break_close', models.TimeField(_('Break Starts on Saturday'), null=True, blank=True)),
            ('sat_break_open', models.TimeField(_('Break Ends on Saturday'), null=True, blank=True)),
            ('sat_close', models.TimeField(_('Closes on Saturday'), null=True, blank=True)),
            ('sun_open', models.TimeField(_('Opens on Sunday'), null=True, blank=True)),
            ('sun_break_close', models.TimeField(_('Break Starts on Sunday'), null=True, blank=True)),
            ('sun_break_open', models.TimeField(_('Break Ends on Sunday'), null=True, blank=True)),
            ('sun_close', models.TimeField(_('Closes on Sunday'), null=True, blank=True)),
            ('exceptions', models.TextField(_('Exceptions for working hours (English)'), blank=True)),
            ('exceptions_de', models.TextField(_('Exceptions for working hours (German)'), blank=True)),
            ('establishment_yyyy', models.IntegerField(_("Year of Establishment"), null=True, blank=True)),
            ('establishment_mm', models.SmallIntegerField(_("Month of Establishment"), null=True, blank=True)),
            ('nof_employees', models.IntegerField(_("Number of Employees"), null=True, blank=True)),
        ))
        db.send_create_signal('institutions', ['Institution'])
        
        # Adding model 'InstitutionalContact'
        db.create_table('institutions_institutionalcontact', (
            ('id', models.AutoField(primary_key=True)),
            ('location_type', models.ForeignKey(orm['optionset.InstitutionalLocationType'], default=get_default_ins_loc_type)),
            ('location_title', models.CharField(_("Location title"), max_length=255, blank=True)),
            ('is_primary', models.BooleanField(_("Primary contact"), default=True)),
            ('is_temporary', models.BooleanField(_("Temporary"), default=False)),
            ('validity_start_yyyy', models.IntegerField(_("From Year"), null=True, blank=True)),
            ('validity_start_mm', models.SmallIntegerField(_("From Month"), null=True, blank=True)),
            ('validity_start_dd', models.SmallIntegerField(_("From Day"), null=True, blank=True)),
            ('validity_end_yyyy', models.IntegerField(_("Till Year"), null=True, blank=True)),
            ('validity_end_mm', models.SmallIntegerField(_("Till Month"), null=True, blank=True)),
            ('validity_end_dd', models.SmallIntegerField(_("Till Day"), null=True, blank=True)),
            ('postal_address', models.ForeignKey(orm['location.Address'], related_name="institutional_address", null=True, blank=True)),
            ('is_billing_address', models.BooleanField(_("Use this address for billing"), default=True)),
            ('is_shipping_address', models.BooleanField(_("Use this address for shipping"), default=True)),
            ('phone0_type', models.ForeignKey(orm['optionset.PhoneType'], default=DefaultPhoneType("phone"), related_name='institutional_contacts0', null=True, blank=True)),
            ('phone0_country', models.CharField(_("Country Code"), default='49', max_length=4, blank=True)),
            ('phone0_area', models.CharField(_("Area Code"), default='30', max_length=5, blank=True)),
            ('phone0_number', models.CharField(_("Subscriber Number and Extension"), max_length=15, blank=True)),
            ('is_phone0_default', models.BooleanField(_("Default?"), default=True)),
            ('is_phone0_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('phone1_type', models.ForeignKey(orm['optionset.PhoneType'], default=DefaultPhoneType("fax"), related_name='institutional_contacts1', null=True, blank=True)),
            ('phone1_country', models.CharField(_("Country Code"), default='49', max_length=4, blank=True)),
            ('phone1_area', models.CharField(_("Area Code"), default='30', max_length=5, blank=True)),
            ('phone1_number', models.CharField(_("Subscriber Number and Extension"), max_length=15, blank=True)),
            ('is_phone1_default', models.BooleanField(_("Default?"), default=False)),
            ('is_phone1_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('phone2_type', models.ForeignKey(orm['optionset.PhoneType'], default=DefaultPhoneType("mobile"), related_name='institutional_contacts2', null=True, blank=True)),
            ('phone2_country', models.CharField(_("Country Code"), default='49', max_length=4, blank=True)),
            ('phone2_area', models.CharField(_("Area Code"), max_length=5, blank=True)),
            ('phone2_number', models.CharField(_("Subscriber Number and Extension"), max_length=15, blank=True)),
            ('is_phone2_default', models.BooleanField(_("Default?"), default=False)),
            ('is_phone2_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('url0_type', models.ForeignKey(orm['optionset.URLType'], related_name='institutional_contacts0', null=True, blank=True)),
            ('url0_link', URLField(_("URL"), blank=True)),
            ('is_url0_default', models.BooleanField(_("Default?"), default=True)),
            ('is_url0_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('url1_type', models.ForeignKey(orm['optionset.URLType'], related_name='institutional_contacts1', null=True, blank=True)),
            ('url1_link', URLField(_("URL"), blank=True)),
            ('is_url1_default', models.BooleanField(_("Default?"), default=False)),
            ('is_url1_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('url2_type', models.ForeignKey(orm['optionset.URLType'], related_name='institutional_contacts2', null=True, blank=True)),
            ('url2_link', URLField(_("URL"), blank=True)),
            ('is_url2_default', models.BooleanField(_("Default?"), default=False)),
            ('is_url2_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('im0_type', models.ForeignKey(orm['optionset.IMType'], related_name='institutional_contacts0', null=True, blank=True)),
            ('im0_address', models.CharField(_("Instant Messenger"), max_length=255, blank=True)),
            ('is_im0_default', models.BooleanField(_("Default?"), default=True)),
            ('is_im0_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('im1_type', models.ForeignKey(orm['optionset.IMType'], related_name='institutional_contacts1', null=True, blank=True)),
            ('im1_address', models.CharField(_("Instant Messenger"), max_length=255, blank=True)),
            ('is_im1_default', models.BooleanField(_("Default?"), default=False)),
            ('is_im1_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('im2_type', models.ForeignKey(orm['optionset.IMType'], related_name='institutional_contacts2', null=True, blank=True)),
            ('im2_address', models.CharField(_("Instant Messenger"), max_length=255, blank=True)),
            ('is_im2_default', models.BooleanField(_("Default?"), default=False)),
            ('is_im2_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('email0_type', models.ForeignKey(orm['optionset.EmailType'], related_name='institutional_contacts0', null=True, blank=True)),
            ('email0_address', models.CharField(_("Email Address"), max_length=255, blank=True)),
            ('is_email0_default', models.BooleanField(_("Default?"), default=True)),
            ('is_email0_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('email1_type', models.ForeignKey(orm['optionset.EmailType'], related_name='institutional_contacts1', null=True, blank=True)),
            ('email1_address', models.CharField(_("Email Address"), max_length=255, blank=True)),
            ('is_email1_default', models.BooleanField(_("Default?"), default=False)),
            ('is_email1_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('email2_type', models.ForeignKey(orm['optionset.EmailType'], related_name='institutional_contacts2', null=True, blank=True)),
            ('email2_address', models.CharField(_("Email Address"), max_length=255, blank=True)),
            ('is_email2_default', models.BooleanField(_("Default?"), default=False)),
            ('is_email2_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('institution', models.ForeignKey(orm['institutions.institution'])),
        ))
        db.send_create_signal('institutions', ['InstitutionalContact'])
        
        # Adding ManyToManyField 'Institution.context_categories'
        db.create_table('institutions_institution_context_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('institution', models.ForeignKey(orm.Institution, null=False)),
            ('contextcategory', models.ForeignKey(orm['structure.ContextCategory'], null=False))
        ))
        
        # Adding ManyToManyField 'Institution.institution_types'
        db.create_table('institutions_institution_institution_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('institution', models.ForeignKey(orm.Institution, null=False)),
            ('term', models.ForeignKey(orm['structure.Term'], null=False))
        ))
        
        # Adding ManyToManyField 'Institution.creative_sectors'
        db.create_table('institutions_institution_creative_sectors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('institution', models.ForeignKey(orm.Institution, null=False)),
            ('term', models.ForeignKey(orm['structure.Term'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Institution'
        db.delete_table('institutions_institution')
        
        # Deleting model 'InstitutionalContact'
        db.delete_table('institutions_institutionalcontact')
        
        # Dropping ManyToManyField 'Institution.context_categories'
        db.delete_table('institutions_institution_context_categories')
        
        # Dropping ManyToManyField 'Institution.institution_types'
        db.delete_table('institutions_institution_institution_types')
        
        # Dropping ManyToManyField 'Institution.creative_sectors'
        db.delete_table('institutions_institution_creative_sectors')
        
    
    
    models = {
        'optionset.phonetype': {
            'Meta': {'ordering': "['sort_order','title']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'optionset.institutionallocationtype': {
            'Meta': {'ordering': "['sort_order','title']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'institutions.institution': {
            'access': ('models.CharField', ['_("Access")'], {'max_length': '255', 'blank': 'True'}),
            'context_categories': ('models.ManyToManyField', ["orm['structure.ContextCategory']"], {'limit_choices_to': "{'is_applied4institution':True}", 'blank': 'True'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creative_sectors': ('models.ManyToManyField', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'categories_creativesectors'}", 'related_name': '"creative_sector_institutions"', 'blank': 'True'}),
            'description': ('models.TextField', ['_("Description (English)")'], {'blank': 'True'}),
            'description_de': ('models.TextField', ['_("Description (German)")'], {'blank': 'True'}),
            'establishment_mm': ('models.SmallIntegerField', ['_("Month of Establishment")'], {'null': 'True', 'blank': 'True'}),
            'establishment_yyyy': ('models.IntegerField', ['_("Year of Establishment")'], {'null': 'True', 'blank': 'True'}),
            'exceptions': ('models.TextField', ["_('Exceptions for working hours (English)')"], {'blank': 'True'}),
            'exceptions_de': ('models.TextField', ["_('Exceptions for working hours (German)')"], {'blank': 'True'}),
            'fri_break_close': ('models.TimeField', ["_('Break Starts on Friday')"], {'null': 'True', 'blank': 'True'}),
            'fri_break_open': ('models.TimeField', ["_('Break Ends on Friday')"], {'null': 'True', 'blank': 'True'}),
            'fri_close': ('models.TimeField', ["_('Closes on Friday')"], {'null': 'True', 'blank': 'True'}),
            'fri_open': ('models.TimeField', ["_('Opens on Friday')"], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ["_('Image')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '255', 'directory': '"/%s/"%URL_ID_INSTITUTIONS', 'blank': 'True'}),
            'institution_types': ('models.ManyToManyField', ["orm['structure.Term']"], {'limit_choices_to': 'models.Q(vocabulary__sysname=\'basics_object_types\',path_search__contains=ObjectTypeFilter("institution"))&~models.Q(models.Q(sysname="institution"))'}),
            'is_appointment_based': ('models.BooleanField', ['_("Visiting by Appointment")'], {'default': 'False'}),
            'is_card_americanexpress_ok': ('models.BooleanField', ['_("American Express")'], {'default': 'False'}),
            'is_card_mastercard_ok': ('models.BooleanField', ['_("MasterCard")'], {'default': 'False'}),
            'is_card_visa_ok': ('models.BooleanField', ['_("Visa")'], {'default': 'False'}),
            'is_cash_ok': ('models.BooleanField', ['_("Cash")'], {'default': 'False'}),
            'is_ec_maestro_ok': ('models.BooleanField', ['_("EC Maestro")'], {'default': 'False'}),
            'is_giropay_ok': ('models.BooleanField', ['_("Giropay")'], {'default': 'False'}),
            'is_invoice_ok': ('models.BooleanField', ['_("Invoice")'], {'default': 'False'}),
            'is_non_profit': ('models.BooleanField', ['_("Non profit (business elsewhere)?")'], {'default': 'False'}),
            'is_on_delivery_ok': ('models.BooleanField', ['_("Payment on delivery")'], {'default': 'False'}),
            'is_parking_avail': ('models.BooleanField', ['_("Is parking available?")'], {'default': 'False'}),
            'is_paypal_ok': ('models.BooleanField', ['_("PayPal")'], {'default': 'False'}),
            'is_prepayment_ok': ('models.BooleanField', ['_("Prepayment")'], {'default': 'False'}),
            'is_transaction_ok': ('models.BooleanField', ['_("Bank transfer")'], {'default': 'False'}),
            'is_wlan_avail': ('models.BooleanField', ['_("Is WLAN Internet available?")'], {'default': 'False'}),
            'legal_form': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_legal_form'}", 'related_name': '"legal_form_institution"', 'null': 'True', 'blank': 'True'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'mon_break_close': ('models.TimeField', ["_('Break Starts on Monday')"], {'null': 'True', 'blank': 'True'}),
            'mon_break_open': ('models.TimeField', ["_('Break Ends on Monday')"], {'null': 'True', 'blank': 'True'}),
            'mon_close': ('models.TimeField', ["_('Closes on Monday')"], {'null': 'True', 'blank': 'True'}),
            'mon_open': ('models.TimeField', ["_('Opens on Monday')"], {'null': 'True', 'blank': 'True'}),
            'nof_employees': ('models.IntegerField', ['_("Number of Employees")'], {'null': 'True', 'blank': 'True'}),
            'parent': ('models.ForeignKey', ["orm['institutions.Institution']"], {'null': 'True', 'blank': 'True'}),
            'sat_break_close': ('models.TimeField', ["_('Break Starts on Saturday')"], {'null': 'True', 'blank': 'True'}),
            'sat_break_open': ('models.TimeField', ["_('Break Ends on Saturday')"], {'null': 'True', 'blank': 'True'}),
            'sat_close': ('models.TimeField', ["_('Closes on Saturday')"], {'null': 'True', 'blank': 'True'}),
            'sat_open': ('models.TimeField', ["_('Opens on Saturday')"], {'null': 'True', 'blank': 'True'}),
            'slug': ('models.CharField', ['_("Slug")'], {'max_length': '255'}),
            'status': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_object_statuses'}", 'related_name': '"status_institution_set"', 'default': 'DefaultObjectStatus("draft")', 'blank': 'True', 'null': 'True'}),
            'sun_break_close': ('models.TimeField', ["_('Break Starts on Sunday')"], {'null': 'True', 'blank': 'True'}),
            'sun_break_open': ('models.TimeField', ["_('Break Ends on Sunday')"], {'null': 'True', 'blank': 'True'}),
            'sun_close': ('models.TimeField', ["_('Closes on Sunday')"], {'null': 'True', 'blank': 'True'}),
            'sun_open': ('models.TimeField', ["_('Opens on Sunday')"], {'null': 'True', 'blank': 'True'}),
            'tax_id_number': ('models.CharField', ['_("Tax ID")'], {'max_length': '100', 'blank': 'True'}),
            'thu_break_close': ('models.TimeField', ["_('Break Starts on Thursday')"], {'null': 'True', 'blank': 'True'}),
            'thu_break_open': ('models.TimeField', ["_('Break Ends on Thursday')"], {'null': 'True', 'blank': 'True'}),
            'thu_close': ('models.TimeField', ["_('Closes on Thursday')"], {'null': 'True', 'blank': 'True'}),
            'thu_open': ('models.TimeField', ["_('Opens on Thursday')"], {'null': 'True', 'blank': 'True'}),
            'title': ('models.CharField', ['_("Title")'], {'max_length': '255'}),
            'title2': ('models.CharField', ['_("Title (second line)")'], {'max_length': '255', 'blank': 'True'}),
            'tue_break_close': ('models.TimeField', ["_('Break Starts on Tuesday')"], {'null': 'True', 'blank': 'True'}),
            'tue_break_open': ('models.TimeField', ["_('Break Ends on Tuesday')"], {'null': 'True', 'blank': 'True'}),
            'tue_close': ('models.TimeField', ["_('Closes on Tuesday')"], {'null': 'True', 'blank': 'True'}),
            'tue_open': ('models.TimeField', ["_('Opens on Tuesday')"], {'null': 'True', 'blank': 'True'}),
            'vat_id_number': ('models.CharField', ['_("VAT ID")'], {'max_length': '100', 'blank': 'True'}),
            'wed_break_close': ('models.TimeField', ["_('Break Starts on Wednesday')"], {'null': 'True', 'blank': 'True'}),
            'wed_break_open': ('models.TimeField', ["_('Break Ends on Wednesday')"], {'null': 'True', 'blank': 'True'}),
            'wed_close': ('models.TimeField', ["_('Closes on Wednesday')"], {'null': 'True', 'blank': 'True'}),
            'wed_open': ('models.TimeField', ["_('Opens on Wednesday')"], {'null': 'True', 'blank': 'True'})
        },
        'institutions.institutionalcontact': {
            'email0_address': ('models.CharField', ['_("Email Address")'], {'max_length': '255', 'blank': 'True'}),
            'email0_type': ('models.ForeignKey', ["orm['optionset.EmailType']"], {'related_name': "'institutional_contacts0'", 'null': 'True', 'blank': 'True'}),
            'email1_address': ('models.CharField', ['_("Email Address")'], {'max_length': '255', 'blank': 'True'}),
            'email1_type': ('models.ForeignKey', ["orm['optionset.EmailType']"], {'related_name': "'institutional_contacts1'", 'null': 'True', 'blank': 'True'}),
            'email2_address': ('models.CharField', ['_("Email Address")'], {'max_length': '255', 'blank': 'True'}),
            'email2_type': ('models.ForeignKey', ["orm['optionset.EmailType']"], {'related_name': "'institutional_contacts2'", 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'im0_address': ('models.CharField', ['_("Instant Messenger")'], {'max_length': '255', 'blank': 'True'}),
            'im0_type': ('models.ForeignKey', ["orm['optionset.IMType']"], {'related_name': "'institutional_contacts0'", 'null': 'True', 'blank': 'True'}),
            'im1_address': ('models.CharField', ['_("Instant Messenger")'], {'max_length': '255', 'blank': 'True'}),
            'im1_type': ('models.ForeignKey', ["orm['optionset.IMType']"], {'related_name': "'institutional_contacts1'", 'null': 'True', 'blank': 'True'}),
            'im2_address': ('models.CharField', ['_("Instant Messenger")'], {'max_length': '255', 'blank': 'True'}),
            'im2_type': ('models.ForeignKey', ["orm['optionset.IMType']"], {'related_name': "'institutional_contacts2'", 'null': 'True', 'blank': 'True'}),
            'institution': ('models.ForeignKey', ["orm['institutions.institution']"], {}),
            'is_billing_address': ('models.BooleanField', ['_("Use this address for billing")'], {'default': 'True'}),
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
            'is_primary': ('models.BooleanField', ['_("Primary contact")'], {'default': 'True'}),
            'is_shipping_address': ('models.BooleanField', ['_("Use this address for shipping")'], {'default': 'True'}),
            'is_temporary': ('models.BooleanField', ['_("Temporary")'], {'default': 'False'}),
            'is_url0_default': ('models.BooleanField', ['_("Default?")'], {'default': 'True'}),
            'is_url0_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_url1_default': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_url1_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_url2_default': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_url2_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'location_title': ('models.CharField', ['_("Location title")'], {'max_length': '255', 'blank': 'True'}),
            'location_type': ('models.ForeignKey', ["orm['optionset.InstitutionalLocationType']"], {'default': 'get_default_ins_loc_type'}),
            'phone0_area': ('models.CharField', ['_("Area Code")'], {'default': "'30'", 'max_length': '5', 'blank': 'True'}),
            'phone0_country': ('models.CharField', ['_("Country Code")'], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone0_number': ('models.CharField', ['_("Subscriber Number and Extension")'], {'max_length': '15', 'blank': 'True'}),
            'phone0_type': ('models.ForeignKey', ["orm['optionset.PhoneType']"], {'default': 'DefaultPhoneType("phone")', 'related_name': "'institutional_contacts0'", 'null': 'True', 'blank': 'True'}),
            'phone1_area': ('models.CharField', ['_("Area Code")'], {'default': "'30'", 'max_length': '5', 'blank': 'True'}),
            'phone1_country': ('models.CharField', ['_("Country Code")'], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone1_number': ('models.CharField', ['_("Subscriber Number and Extension")'], {'max_length': '15', 'blank': 'True'}),
            'phone1_type': ('models.ForeignKey', ["orm['optionset.PhoneType']"], {'default': 'DefaultPhoneType("fax")', 'related_name': "'institutional_contacts1'", 'null': 'True', 'blank': 'True'}),
            'phone2_area': ('models.CharField', ['_("Area Code")'], {'max_length': '5', 'blank': 'True'}),
            'phone2_country': ('models.CharField', ['_("Country Code")'], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone2_number': ('models.CharField', ['_("Subscriber Number and Extension")'], {'max_length': '15', 'blank': 'True'}),
            'phone2_type': ('models.ForeignKey', ["orm['optionset.PhoneType']"], {'default': 'DefaultPhoneType("mobile")', 'related_name': "'institutional_contacts2'", 'null': 'True', 'blank': 'True'}),
            'postal_address': ('models.ForeignKey', ["orm['location.Address']"], {'related_name': '"institutional_address"', 'null': 'True', 'blank': 'True'}),
            'url0_link': ('URLField', ['_("URL")'], {'blank': 'True'}),
            'url0_type': ('models.ForeignKey', ["orm['optionset.URLType']"], {'related_name': "'institutional_contacts0'", 'null': 'True', 'blank': 'True'}),
            'url1_link': ('URLField', ['_("URL")'], {'blank': 'True'}),
            'url1_type': ('models.ForeignKey', ["orm['optionset.URLType']"], {'related_name': "'institutional_contacts1'", 'null': 'True', 'blank': 'True'}),
            'url2_link': ('URLField', ['_("URL")'], {'blank': 'True'}),
            'url2_type': ('models.ForeignKey', ["orm['optionset.URLType']"], {'related_name': "'institutional_contacts2'", 'null': 'True', 'blank': 'True'}),
            'validity_end_dd': ('models.SmallIntegerField', ['_("Till Day")'], {'null': 'True', 'blank': 'True'}),
            'validity_end_mm': ('models.SmallIntegerField', ['_("Till Month")'], {'null': 'True', 'blank': 'True'}),
            'validity_end_yyyy': ('models.IntegerField', ['_("Till Year")'], {'null': 'True', 'blank': 'True'}),
            'validity_start_dd': ('models.SmallIntegerField', ['_("From Day")'], {'null': 'True', 'blank': 'True'}),
            'validity_start_mm': ('models.SmallIntegerField', ['_("From Month")'], {'null': 'True', 'blank': 'True'}),
            'validity_start_yyyy': ('models.IntegerField', ['_("From Year")'], {'null': 'True', 'blank': 'True'})
        },
        'optionset.emailtype': {
            'Meta': {'ordering': "['sort_order','title']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'structure.term': {
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
        'structure.contextcategory': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'optionset.imtype': {
            'Meta': {'ordering': "['sort_order','title']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['institutions']
