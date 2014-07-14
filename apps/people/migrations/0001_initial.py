# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from ccb.apps.people.models import *
from base_libs.utils.misc import south_clean_multilingual_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Person'
        db.create_table('people_person', (
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('modified_date', models.DateTimeField(_("modified date"), null=True, editable=False)),
            ('user', models.OneToOneField(orm['auth.User'], unique=True)),
            ('individual_type', models.ForeignKey(orm['structure.Term'], limit_choices_to=models.Q(vocabulary__sysname='basics_object_types',path_search__contains=ObjectTypeFilter("person"))&~models.Q(models.Q(sysname="person")), null=True, blank=True)),
            ('prefix', models.ForeignKey(orm['optionset.Prefix'], null=True, blank=True)),
            ('salutation', models.ForeignKey(orm['optionset.Salutation'], null=True, blank=True)),
            ('nickname', models.CharField(_("Nickname"), max_length=200, blank=True)),
            ('birthname', models.CharField(_("Birth / Maiden name"), max_length=200, blank=True)),
            ('gender', models.CharField(_("Gender"), blank=True, max_length=1)),
            ('birthday_yyyy', models.IntegerField(_("Year of Birth"), null=True, blank=True)),
            ('birthday_mm', models.SmallIntegerField(_("Month of Birth"), null=True, blank=True)),
            ('birthday_dd', models.SmallIntegerField(_("Day of Birth"), null=True, blank=True)),
            ('nationality', models.ForeignKey(orm['i18n.Nationality'], limit_choices_to={'display':True}, null=True, max_length=200, blank=True)),
            ('degree', models.CharField(_("Academic Degree"), max_length=200, blank=True)),
            ('occupation', models.CharField(_("Current Occupation"), max_length=200, blank=True)),
            ('interests', models.CharField(_("Interests"), max_length=200, blank=True)),
            ('description', models.TextField(_("Description (English)"), blank=True)),
            ('description_de', models.TextField(_("Description (German)"), blank=True)),
            ('image', FileBrowseField(_('Image'), extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff'], max_length=255, directory="/%s/"%URL_ID_PEOPLE, blank=True)),
            ('status', models.ForeignKey(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_object_statuses'}, related_name="status_person_set", default=DefaultObjectStatus("draft"), blank=True, null=True)),
            ('preferred_language', models.ForeignKey(orm['i18n.Language'], limit_choices_to={'display':True}, null=True, blank=True)),
            ('timezone', models.ForeignKey(orm['i18n.TimeZone'], null=True, max_length=200, blank=True)),
            ('display_birthday', models.BooleanField(_("Display birthday to public"), default=True)),
            ('display_email', models.BooleanField(_("Display email address to public"), default=False)),
            ('display_address', models.BooleanField(_("Display address data to public"), default=True)),
            ('display_phone', models.BooleanField(_("Display phone numbers to public"), default=True)),
            ('display_fax', models.BooleanField(_("Display fax numbers to public"), default=True)),
            ('display_mobile', models.BooleanField(_("Display mobile phones to public"), default=True)),
            ('display_im', models.BooleanField(_("Display instant messengers to public"), default=True)),
            ('display_username', models.BooleanField(_("Display user name instead of full name"), default=False)),
            ('allow_search_engine_indexing', models.BooleanField(_("Allow indexing by search engines"), default=True)),
        ))
        db.send_create_signal('people', ['Person'])
        
        # Adding model 'IndividualContact'
        db.create_table('people_individualcontact', (
            ('id', models.AutoField(primary_key=True)),
            ('location_type', models.ForeignKey(orm['optionset.IndividualLocationType'], default=get_default_ind_loc_type)),
            ('location_title', models.CharField(_("Location title"), max_length=255, blank=True)),
            ('is_primary', models.BooleanField(_("Primary contact"), default=True)),
            ('is_seasonal', models.BooleanField(_("Seasonal"), default=False)),
            ('validity_start_yyyy', models.IntegerField(_("From Year"), null=True, blank=True)),
            ('validity_start_mm', models.SmallIntegerField(_("From Month"), null=True, blank=True)),
            ('validity_start_dd', models.SmallIntegerField(_("From Day"), null=True, blank=True)),
            ('validity_end_yyyy', models.IntegerField(_("Till Year"), null=True, blank=True)),
            ('validity_end_mm', models.SmallIntegerField(_("Till Month"), null=True, blank=True)),
            ('validity_end_dd', models.SmallIntegerField(_("Till Day"), null=True, blank=True)),
            ('institutional_title', models.CharField(_("Title in the institution"), max_length=255, blank=True)),
            ('postal_address', models.ForeignKey(orm['location.Address'], related_name="individual_address", null=True, blank=True)),
            ('is_billing_address', models.BooleanField(_("Use this address for billing"), default=True)),
            ('is_shipping_address', models.BooleanField(_("Use this address for shipping"), default=True)),
            ('phone0_type', models.ForeignKey(orm['optionset.PhoneType'], default=DefaultPhoneType("phone"), related_name='individual_contacts0', null=True, blank=True)),
            ('phone0_country', models.CharField(_("Country Code"), default='49', max_length=4, blank=True)),
            ('phone0_area', models.CharField(_("Area Code"), default='30', max_length=5, blank=True)),
            ('phone0_number', models.CharField(_("Subscriber Number and Extension"), max_length=15, blank=True)),
            ('is_phone0_default', models.BooleanField(_("Default?"), default=True)),
            ('is_phone0_on_hold', models.BooleanField(_("Default?"), default=False)),
            ('phone1_type', models.ForeignKey(orm['optionset.PhoneType'], default=DefaultPhoneType("fax"), related_name='individual_contacts1', null=True, blank=True)),
            ('phone1_country', models.CharField(_("Country Code"), default='49', max_length=4, blank=True)),
            ('phone1_area', models.CharField(_("Area Code"), default='30', max_length=5, blank=True)),
            ('phone1_number', models.CharField(_("Subscriber Number and Extension"), max_length=15, blank=True)),
            ('is_phone1_default', models.BooleanField(_("Default?"), default=False)),
            ('is_phone1_on_hold', models.BooleanField(_("Default?"), default=False)),
            ('phone2_type', models.ForeignKey(orm['optionset.PhoneType'], default=DefaultPhoneType("mobile"), related_name='individual_contacts2', null=True, blank=True)),
            ('phone2_country', models.CharField(_("Country Code"), default='49', max_length=4, blank=True)),
            ('phone2_area', models.CharField(_("Area Code"), max_length=5, blank=True)),
            ('phone2_number', models.CharField(_("Subscriber Number and Extension"), max_length=15, blank=True)),
            ('is_phone2_default', models.BooleanField(_("Default?"), default=False)),
            ('is_phone2_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('url0_type', models.ForeignKey(orm['optionset.URLType'], related_name='individual_contacts0', null=True, blank=True)),
            ('url0_link', URLField(_("URL"), blank=True)),
            ('is_url0_default', models.BooleanField(_("Default?"), default=True)),
            ('is_url0_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('url1_type', models.ForeignKey(orm['optionset.URLType'], related_name='individual_contacts1', null=True, blank=True)),
            ('url1_link', URLField(_("URL"), blank=True)),
            ('is_url1_default', models.BooleanField(_("Default?"), default=False)),
            ('is_url1_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('url2_type', models.ForeignKey(orm['optionset.URLType'], related_name='individual_contacts2', null=True, blank=True)),
            ('url2_link', URLField(_("URL"), blank=True)),
            ('is_url2_default', models.BooleanField(_("Default?"), default=False)),
            ('is_url2_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('im0_type', models.ForeignKey(orm['optionset.IMType'], related_name='individual_contacts0', null=True, blank=True)),
            ('im0_address', models.CharField(_("Instant Messenger"), max_length=255, blank=True)),
            ('is_im0_default', models.BooleanField(_("Default?"), default=True)),
            ('is_im0_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('im1_type', models.ForeignKey(orm['optionset.IMType'], related_name='individual_contacts1', null=True, blank=True)),
            ('im1_address', models.CharField(_("Instant Messenger"), max_length=255, blank=True)),
            ('is_im1_default', models.BooleanField(_("Default?"), default=False)),
            ('is_im1_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('im2_type', models.ForeignKey(orm['optionset.IMType'], related_name='individual_contacts2', null=True, blank=True)),
            ('im2_address', models.CharField(_("Instant Messenger"), max_length=255, blank=True)),
            ('is_im2_default', models.BooleanField(_("Default?"), default=False)),
            ('is_im2_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('email0_type', models.ForeignKey(orm['optionset.EmailType'], related_name='individual_contacts0', null=True, blank=True)),
            ('email0_address', models.CharField(_("Email Address"), max_length=255, blank=True)),
            ('is_email0_default', models.BooleanField(_("Default?"), default=True)),
            ('is_email0_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('email1_type', models.ForeignKey(orm['optionset.EmailType'], related_name='individual_contacts1', null=True, blank=True)),
            ('email1_address', models.CharField(_("Email Address"), max_length=255, blank=True)),
            ('is_email1_default', models.BooleanField(_("Default?"), default=False)),
            ('is_email1_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('email2_type', models.ForeignKey(orm['optionset.EmailType'], related_name='individual_contacts2', null=True, blank=True)),
            ('email2_address', models.CharField(_("Email Address"), max_length=255, blank=True)),
            ('is_email2_default', models.BooleanField(_("Default?"), default=False)),
            ('is_email2_on_hold', models.BooleanField(_("On Hold?"), default=False)),
            ('person', models.ForeignKey(orm['people.person'])),
            ('institution', models.ForeignKey(orm['institutions.institution'], null=True, blank=True)),
        ))
        db.send_create_signal('people', ['IndividualContact'])
        
        # Adding ManyToManyField 'Person.spoken_languages'
        db.create_table('people_person_spoken_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm.Person, null=False)),
            ('language', models.ForeignKey(orm['i18n.Language'], null=False))
        ))
        
        # Adding ManyToManyField 'Person.context_categories'
        db.create_table('people_person_context_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm.Person, null=False)),
            ('contextcategory', models.ForeignKey(orm['structure.ContextCategory'], null=False))
        ))
        
        # Adding ManyToManyField 'Person.creative_sectors'
        db.create_table('people_person_creative_sectors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm.Person, null=False)),
            ('term', models.ForeignKey(orm['structure.Term'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Person'
        db.delete_table('people_person')
        
        # Deleting model 'IndividualContact'
        db.delete_table('people_individualcontact')
        
        # Dropping ManyToManyField 'Person.spoken_languages'
        db.delete_table('people_person_spoken_languages')
        
        # Dropping ManyToManyField 'Person.context_categories'
        db.delete_table('people_person_context_categories')
        
        # Dropping ManyToManyField 'Person.creative_sectors'
        db.delete_table('people_person_creative_sectors')
        
    
    
    models = {
        'optionset.phonetype': {
            'Meta': {'ordering': "['sort_order','title']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'structure.contextcategory': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'people.person': {
            'allow_search_engine_indexing': ('models.BooleanField', ['_("Allow indexing by search engines")'], {'default': 'True'}),
            'birthday_dd': ('models.SmallIntegerField', ['_("Day of Birth")'], {'null': 'True', 'blank': 'True'}),
            'birthday_mm': ('models.SmallIntegerField', ['_("Month of Birth")'], {'null': 'True', 'blank': 'True'}),
            'birthday_yyyy': ('models.IntegerField', ['_("Year of Birth")'], {'null': 'True', 'blank': 'True'}),
            'birthname': ('models.CharField', ['_("Birth / Maiden name")'], {'max_length': '200', 'blank': 'True'}),
            'context_categories': ('models.ManyToManyField', ["orm['structure.ContextCategory']"], {'limit_choices_to': "{'is_applied4person':True}", 'blank': 'True'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'creative_sectors': ('models.ManyToManyField', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'categories_creativesectors'}", 'related_name': '"creative_industry_people"', 'blank': 'True'}),
            'degree': ('models.CharField', ['_("Academic Degree")'], {'max_length': '200', 'blank': 'True'}),
            'description': ('models.TextField', ['_("Description (English)")'], {'blank': 'True'}),
            'description_de': ('models.TextField', ['_("Description (German)")'], {'blank': 'True'}),
            'display_address': ('models.BooleanField', ['_("Display address data to public")'], {'default': 'True'}),
            'display_birthday': ('models.BooleanField', ['_("Display birthday to public")'], {'default': 'True'}),
            'display_email': ('models.BooleanField', ['_("Display email address to public")'], {'default': 'False'}),
            'display_fax': ('models.BooleanField', ['_("Display fax numbers to public")'], {'default': 'True'}),
            'display_im': ('models.BooleanField', ['_("Display instant messengers to public")'], {'default': 'True'}),
            'display_mobile': ('models.BooleanField', ['_("Display mobile phones to public")'], {'default': 'True'}),
            'display_phone': ('models.BooleanField', ['_("Display phone numbers to public")'], {'default': 'True'}),
            'display_username': ('models.BooleanField', ['_("Display user name instead of full name")'], {'default': 'False'}),
            'gender': ('models.CharField', ['_("Gender")'], {'blank': 'True', 'max_length': '1'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('FileBrowseField', ["_('Image')"], {'extensions': "['.jpg','.jpeg','.gif','.png','.tif','.tiff']", 'max_length': '255', 'directory': '"/%s/"%URL_ID_PEOPLE', 'blank': 'True'}),
            'individual_type': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': 'models.Q(vocabulary__sysname=\'basics_object_types\',path_search__contains=ObjectTypeFilter("person"))&~models.Q(models.Q(sysname="person"))', 'null': 'True', 'blank': 'True'}),
            'interests': ('models.CharField', ['_("Interests")'], {'max_length': '200', 'blank': 'True'}),
            'modified_date': ('models.DateTimeField', ['_("modified date")'], {'null': 'True', 'editable': 'False'}),
            'nationality': ('models.ForeignKey', ["orm['i18n.Nationality']"], {'limit_choices_to': "{'display':True}", 'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'nickname': ('models.CharField', ['_("Nickname")'], {'max_length': '200', 'blank': 'True'}),
            'occupation': ('models.CharField', ['_("Current Occupation")'], {'max_length': '200', 'blank': 'True'}),
            'preferred_language': ('models.ForeignKey', ["orm['i18n.Language']"], {'limit_choices_to': "{'display':True}", 'null': 'True', 'blank': 'True'}),
            'prefix': ('models.ForeignKey', ["orm['optionset.Prefix']"], {'null': 'True', 'blank': 'True'}),
            'salutation': ('models.ForeignKey', ["orm['optionset.Salutation']"], {'null': 'True', 'blank': 'True'}),
            'spoken_languages': ('models.ManyToManyField', ["orm['i18n.Language']"], {'related_name': '"speaking_people"', 'blank': 'True'}),
            'status': ('models.ForeignKey', ["orm['structure.Term']"], {'limit_choices_to': "{'vocabulary__sysname':'basics_object_statuses'}", 'related_name': '"status_person_set"', 'default': 'DefaultObjectStatus("draft")', 'blank': 'True', 'null': 'True'}),
            'timezone': ('models.ForeignKey', ["orm['i18n.TimeZone']"], {'null': 'True', 'max_length': '200', 'blank': 'True'}),
            'user': ('models.OneToOneField', ["orm['auth.User']"], {'unique': 'True'})
        },
        'optionset.individuallocationtype': {
            'Meta': {'ordering': "['sort_order','title']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'i18n.language': {
            'Meta': {'ordering': "XFieldList(['sort_order','name_'])"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'structure.term': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'people.individualcontact': {
            'email0_address': ('models.CharField', ['_("Email Address")'], {'max_length': '255', 'blank': 'True'}),
            'email0_type': ('models.ForeignKey', ["orm['optionset.EmailType']"], {'related_name': "'individual_contacts0'", 'null': 'True', 'blank': 'True'}),
            'email1_address': ('models.CharField', ['_("Email Address")'], {'max_length': '255', 'blank': 'True'}),
            'email1_type': ('models.ForeignKey', ["orm['optionset.EmailType']"], {'related_name': "'individual_contacts1'", 'null': 'True', 'blank': 'True'}),
            'email2_address': ('models.CharField', ['_("Email Address")'], {'max_length': '255', 'blank': 'True'}),
            'email2_type': ('models.ForeignKey', ["orm['optionset.EmailType']"], {'related_name': "'individual_contacts2'", 'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'im0_address': ('models.CharField', ['_("Instant Messenger")'], {'max_length': '255', 'blank': 'True'}),
            'im0_type': ('models.ForeignKey', ["orm['optionset.IMType']"], {'related_name': "'individual_contacts0'", 'null': 'True', 'blank': 'True'}),
            'im1_address': ('models.CharField', ['_("Instant Messenger")'], {'max_length': '255', 'blank': 'True'}),
            'im1_type': ('models.ForeignKey', ["orm['optionset.IMType']"], {'related_name': "'individual_contacts1'", 'null': 'True', 'blank': 'True'}),
            'im2_address': ('models.CharField', ['_("Instant Messenger")'], {'max_length': '255', 'blank': 'True'}),
            'im2_type': ('models.ForeignKey', ["orm['optionset.IMType']"], {'related_name': "'individual_contacts2'", 'null': 'True', 'blank': 'True'}),
            'institution': ('models.ForeignKey', ["orm['institutions.institution']"], {'null': 'True', 'blank': 'True'}),
            'institutional_title': ('models.CharField', ['_("Title in the institution")'], {'max_length': '255', 'blank': 'True'}),
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
            'is_phone0_on_hold': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_phone1_default': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_phone1_on_hold': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_phone2_default': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_phone2_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_primary': ('models.BooleanField', ['_("Primary contact")'], {'default': 'True'}),
            'is_seasonal': ('models.BooleanField', ['_("Seasonal")'], {'default': 'False'}),
            'is_shipping_address': ('models.BooleanField', ['_("Use this address for shipping")'], {'default': 'True'}),
            'is_url0_default': ('models.BooleanField', ['_("Default?")'], {'default': 'True'}),
            'is_url0_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_url1_default': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_url1_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'is_url2_default': ('models.BooleanField', ['_("Default?")'], {'default': 'False'}),
            'is_url2_on_hold': ('models.BooleanField', ['_("On Hold?")'], {'default': 'False'}),
            'location_title': ('models.CharField', ['_("Location title")'], {'max_length': '255', 'blank': 'True'}),
            'location_type': ('models.ForeignKey', ["orm['optionset.IndividualLocationType']"], {'default': 'get_default_ind_loc_type'}),
            'person': ('models.ForeignKey', ["orm['people.person']"], {}),
            'phone0_area': ('models.CharField', ['_("Area Code")'], {'default': "'30'", 'max_length': '5', 'blank': 'True'}),
            'phone0_country': ('models.CharField', ['_("Country Code")'], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone0_number': ('models.CharField', ['_("Subscriber Number and Extension")'], {'max_length': '15', 'blank': 'True'}),
            'phone0_type': ('models.ForeignKey', ["orm['optionset.PhoneType']"], {'default': 'DefaultPhoneType("phone")', 'related_name': "'individual_contacts0'", 'null': 'True', 'blank': 'True'}),
            'phone1_area': ('models.CharField', ['_("Area Code")'], {'default': "'30'", 'max_length': '5', 'blank': 'True'}),
            'phone1_country': ('models.CharField', ['_("Country Code")'], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone1_number': ('models.CharField', ['_("Subscriber Number and Extension")'], {'max_length': '15', 'blank': 'True'}),
            'phone1_type': ('models.ForeignKey', ["orm['optionset.PhoneType']"], {'default': 'DefaultPhoneType("fax")', 'related_name': "'individual_contacts1'", 'null': 'True', 'blank': 'True'}),
            'phone2_area': ('models.CharField', ['_("Area Code")'], {'max_length': '5', 'blank': 'True'}),
            'phone2_country': ('models.CharField', ['_("Country Code")'], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone2_number': ('models.CharField', ['_("Subscriber Number and Extension")'], {'max_length': '15', 'blank': 'True'}),
            'phone2_type': ('models.ForeignKey', ["orm['optionset.PhoneType']"], {'default': 'DefaultPhoneType("mobile")', 'related_name': "'individual_contacts2'", 'null': 'True', 'blank': 'True'}),
            'postal_address': ('models.ForeignKey', ["orm['location.Address']"], {'related_name': '"individual_address"', 'null': 'True', 'blank': 'True'}),
            'url0_link': ('URLField', ['_("URL")'], {'blank': 'True'}),
            'url0_type': ('models.ForeignKey', ["orm['optionset.URLType']"], {'related_name': "'individual_contacts0'", 'null': 'True', 'blank': 'True'}),
            'url1_link': ('URLField', ['_("URL")'], {'blank': 'True'}),
            'url1_type': ('models.ForeignKey', ["orm['optionset.URLType']"], {'related_name': "'individual_contacts1'", 'null': 'True', 'blank': 'True'}),
            'url2_link': ('URLField', ['_("URL")'], {'blank': 'True'}),
            'url2_type': ('models.ForeignKey', ["orm['optionset.URLType']"], {'related_name': "'individual_contacts2'", 'null': 'True', 'blank': 'True'}),
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
        'location.address': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'optionset.urltype': {
            'Meta': {'ordering': "['sort_order','title']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'institutions.institution': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'i18n.timezone': {
            'Meta': {'ordering': "['zone']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'optionset.imtype': {
            'Meta': {'ordering': "['sort_order','title']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'i18n.nationality': {
            'Meta': {'ordering': "XFieldList(['sort_order','name_'])"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'optionset.prefix': {
            'Meta': {'ordering': "['sort_order','title']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'optionset.salutation': {
            'Meta': {'ordering': "['sort_order','title']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['people']
