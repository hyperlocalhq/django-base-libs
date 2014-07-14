# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Person.completeness'
        db.add_column('people_person', 'completeness', self.gf('django.db.models.fields.SmallIntegerField')(default=0), keep_default=False)

        # Changing field 'Person.interests'
        db.alter_column('people_person', 'interests', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True))

        # Changing field 'Person.birthday_dd'
        db.alter_column('people_person', 'birthday_dd', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True))

        # Changing field 'Person.display_email'
        db.alter_column('people_person', 'display_email', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Person.image'
        db.alter_column('people_person', 'image', self.gf('filebrowser.fields.FileBrowseField')(directory='/people/', max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'], blank=True))

        # Changing field 'Person.creation_date'
        db.alter_column('people_person', 'creation_date', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Person.prefix'
        db.alter_column('people_person', 'prefix_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['optionset.Prefix'], null=True, blank=True))

        # Changing field 'Person.individual_type'
        db.alter_column('people_person', 'individual_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['structure.Term'], null=True, blank=True))

        # Changing field 'Person.display_phone'
        db.alter_column('people_person', 'display_phone', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Person.salutation'
        db.alter_column('people_person', 'salutation_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['optionset.Salutation'], null=True, blank=True))

        # Changing field 'Person.timezone'
        db.alter_column('people_person', 'timezone_id', self.gf('django.db.models.fields.related.ForeignKey')(max_length=200, to=orm['i18n.TimeZone'], null=True, blank=True))

        # Changing field 'Person.description_de'
        db.alter_column('people_person', 'description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace=''))

        # Changing field 'Person.occupation'
        db.alter_column('people_person', 'occupation', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True))

        # Changing field 'Person.modified_date'
        db.alter_column('people_person', 'modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Person.birthname'
        db.alter_column('people_person', 'birthname', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True))

        # Changing field 'Person.display_im'
        db.alter_column('people_person', 'display_im', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Person.allow_search_engine_indexing'
        db.alter_column('people_person', 'allow_search_engine_indexing', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Person.birthday_yyyy'
        db.alter_column('people_person', 'birthday_yyyy', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True))

        # Changing field 'Person.display_address'
        db.alter_column('people_person', 'display_address', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Person.description'
        db.alter_column('people_person', 'description', self.gf('base_libs.models.fields.MultilingualTextField')(null=True, blank=True))

        # Changing field 'Person.degree'
        db.alter_column('people_person', 'degree', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True))

        # Changing field 'Person.display_fax'
        db.alter_column('people_person', 'display_fax', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Person.description_en'
        db.alter_column('people_person', 'description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace=''))

        # Changing field 'Person.user'
        db.alter_column('people_person', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True))

        # Changing field 'Person.display_birthday'
        db.alter_column('people_person', 'display_birthday', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Person.nationality'
        db.alter_column('people_person', 'nationality_id', self.gf('django.db.models.fields.related.ForeignKey')(max_length=200, to=orm['i18n.Nationality'], null=True, blank=True))

        # Changing field 'Person.nickname'
        db.alter_column('people_person', 'nickname', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True))

        # Changing field 'Person.preferred_language'
        db.alter_column('people_person', 'preferred_language_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['i18n.Language'], null=True, blank=True))

        # Changing field 'Person.gender'
        db.alter_column('people_person', 'gender', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True))

        # Changing field 'Person.display_username'
        db.alter_column('people_person', 'display_username', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'Person.birthday_mm'
        db.alter_column('people_person', 'birthday_mm', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True))

        # Changing field 'Person.status'
        db.alter_column('people_person', 'status_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['structure.Term']))

        # Changing field 'Person.display_mobile'
        db.alter_column('people_person', 'display_mobile', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.is_phone2_on_hold'
        db.alter_column('people_individualcontact', 'is_phone2_on_hold', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.institutional_title'
        db.alter_column('people_individualcontact', 'institutional_title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))

        # Changing field 'IndividualContact.location_type'
        db.alter_column('people_individualcontact', 'location_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['optionset.IndividualLocationType']))

        # Changing field 'IndividualContact.is_im0_default'
        db.alter_column('people_individualcontact', 'is_im0_default', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.email0_type'
        db.alter_column('people_individualcontact', 'email0_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['optionset.EmailType']))

        # Changing field 'IndividualContact.is_im2_default'
        db.alter_column('people_individualcontact', 'is_im2_default', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.is_phone2_default'
        db.alter_column('people_individualcontact', 'is_phone2_default', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.is_url0_default'
        db.alter_column('people_individualcontact', 'is_url0_default', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.is_primary'
        db.alter_column('people_individualcontact', 'is_primary', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.is_url2_default'
        db.alter_column('people_individualcontact', 'is_url2_default', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.validity_start_mm'
        db.alter_column('people_individualcontact', 'validity_start_mm', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True))

        # Changing field 'IndividualContact.phone1_type'
        db.alter_column('people_individualcontact', 'phone1_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['optionset.PhoneType']))

        # Changing field 'IndividualContact.is_url1_on_hold'
        db.alter_column('people_individualcontact', 'is_url1_on_hold', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.is_phone0_default'
        db.alter_column('people_individualcontact', 'is_phone0_default', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.url1_link'
        db.alter_column('people_individualcontact', 'url1_link', self.gf('base_libs.models.fields.URLField')(max_length=200, blank=True))

        # Changing field 'IndividualContact.url0_link'
        db.alter_column('people_individualcontact', 'url0_link', self.gf('base_libs.models.fields.URLField')(max_length=200, blank=True))

        # Changing field 'IndividualContact.email1_type'
        db.alter_column('people_individualcontact', 'email1_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['optionset.EmailType']))

        # Changing field 'IndividualContact.phone0_type'
        db.alter_column('people_individualcontact', 'phone0_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['optionset.PhoneType']))

        # Changing field 'IndividualContact.phone2_country'
        db.alter_column('people_individualcontact', 'phone2_country', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True))

        # Changing field 'IndividualContact.is_im0_on_hold'
        db.alter_column('people_individualcontact', 'is_im0_on_hold', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.im1_type'
        db.alter_column('people_individualcontact', 'im1_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['optionset.IMType']))

        # Changing field 'IndividualContact.im2_type'
        db.alter_column('people_individualcontact', 'im2_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['optionset.IMType']))

        # Changing field 'IndividualContact.is_im1_default'
        db.alter_column('people_individualcontact', 'is_im1_default', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.is_url2_on_hold'
        db.alter_column('people_individualcontact', 'is_url2_on_hold', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.validity_end_mm'
        db.alter_column('people_individualcontact', 'validity_end_mm', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True))

        # Changing field 'IndividualContact.person'
        db.alter_column('people_individualcontact', 'person_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['people.Person']))

        # Changing field 'IndividualContact.phone1_country'
        db.alter_column('people_individualcontact', 'phone1_country', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True))

        # Changing field 'IndividualContact.im0_type'
        db.alter_column('people_individualcontact', 'im0_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['optionset.IMType']))

        # Changing field 'IndividualContact.url0_type'
        db.alter_column('people_individualcontact', 'url0_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['optionset.URLType']))

        # Changing field 'IndividualContact.is_phone0_on_hold'
        db.alter_column('people_individualcontact', 'is_phone0_on_hold', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.is_email1_default'
        db.alter_column('people_individualcontact', 'is_email1_default', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.email2_type'
        db.alter_column('people_individualcontact', 'email2_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['optionset.EmailType']))

        # Changing field 'IndividualContact.validity_start_dd'
        db.alter_column('people_individualcontact', 'validity_start_dd', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True))

        # Changing field 'IndividualContact.email2_address'
        db.alter_column('people_individualcontact', 'email2_address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))

        # Changing field 'IndividualContact.is_email0_on_hold'
        db.alter_column('people_individualcontact', 'is_email0_on_hold', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.is_im2_on_hold'
        db.alter_column('people_individualcontact', 'is_im2_on_hold', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.is_email2_default'
        db.alter_column('people_individualcontact', 'is_email2_default', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.email0_address'
        db.alter_column('people_individualcontact', 'email0_address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))

        # Changing field 'IndividualContact.phone0_area'
        db.alter_column('people_individualcontact', 'phone0_area', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True))

        # Changing field 'IndividualContact.im1_address'
        db.alter_column('people_individualcontact', 'im1_address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))

        # Changing field 'IndividualContact.postal_address'
        db.alter_column('people_individualcontact', 'postal_address_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['location.Address']))

        # Changing field 'IndividualContact.is_email2_on_hold'
        db.alter_column('people_individualcontact', 'is_email2_on_hold', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.phone0_country'
        db.alter_column('people_individualcontact', 'phone0_country', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True))

        # Changing field 'IndividualContact.is_billing_address'
        db.alter_column('people_individualcontact', 'is_billing_address', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.im2_address'
        db.alter_column('people_individualcontact', 'im2_address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))

        # Changing field 'IndividualContact.location_title'
        db.alter_column('people_individualcontact', 'location_title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))

        # Changing field 'IndividualContact.validity_end_yyyy'
        db.alter_column('people_individualcontact', 'validity_end_yyyy', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True))

        # Changing field 'IndividualContact.im0_address'
        db.alter_column('people_individualcontact', 'im0_address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))

        # Changing field 'IndividualContact.email1_address'
        db.alter_column('people_individualcontact', 'email1_address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True))

        # Changing field 'IndividualContact.is_url0_on_hold'
        db.alter_column('people_individualcontact', 'is_url0_on_hold', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.url1_type'
        db.alter_column('people_individualcontact', 'url1_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['optionset.URLType']))

        # Changing field 'IndividualContact.url2_type'
        db.alter_column('people_individualcontact', 'url2_type_id', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['optionset.URLType']))

        # Changing field 'IndividualContact.is_email0_default'
        db.alter_column('people_individualcontact', 'is_email0_default', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.is_phone1_on_hold'
        db.alter_column('people_individualcontact', 'is_phone1_on_hold', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.validity_end_dd'
        db.alter_column('people_individualcontact', 'validity_end_dd', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True))

        # Changing field 'IndividualContact.phone2_type'
        db.alter_column('people_individualcontact', 'phone2_type_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, blank=True, to=orm['optionset.PhoneType']))

        # Changing field 'IndividualContact.is_url1_default'
        db.alter_column('people_individualcontact', 'is_url1_default', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.url2_link'
        db.alter_column('people_individualcontact', 'url2_link', self.gf('base_libs.models.fields.URLField')(max_length=200, blank=True))

        # Changing field 'IndividualContact.phone0_number'
        db.alter_column('people_individualcontact', 'phone0_number', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True))

        # Changing field 'IndividualContact.is_email1_on_hold'
        db.alter_column('people_individualcontact', 'is_email1_on_hold', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.phone1_number'
        db.alter_column('people_individualcontact', 'phone1_number', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True))

        # Changing field 'IndividualContact.is_shipping_address'
        db.alter_column('people_individualcontact', 'is_shipping_address', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.phone1_area'
        db.alter_column('people_individualcontact', 'phone1_area', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True))

        # Changing field 'IndividualContact.is_im1_on_hold'
        db.alter_column('people_individualcontact', 'is_im1_on_hold', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.phone2_area'
        db.alter_column('people_individualcontact', 'phone2_area', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True))

        # Changing field 'IndividualContact.phone2_number'
        db.alter_column('people_individualcontact', 'phone2_number', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True))

        # Changing field 'IndividualContact.is_phone1_default'
        db.alter_column('people_individualcontact', 'is_phone1_default', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.is_seasonal'
        db.alter_column('people_individualcontact', 'is_seasonal', self.gf('django.db.models.fields.BooleanField')(blank=True))

        # Changing field 'IndividualContact.validity_start_yyyy'
        db.alter_column('people_individualcontact', 'validity_start_yyyy', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True))
    
    
    def backwards(self, orm):
        
        # Deleting field 'Person.completeness'
        db.delete_column('people_person', 'completeness')

        # Changing field 'Person.interests'
        db.alter_column('people_person', 'interests', self.gf('models.CharField')(_("Interests"), max_length=200, blank=True))

        # Changing field 'Person.birthday_dd'
        db.alter_column('people_person', 'birthday_dd', self.gf('models.SmallIntegerField')(_("Day of Birth"), null=True, blank=True))

        # Changing field 'Person.display_email'
        db.alter_column('people_person', 'display_email', self.gf('models.BooleanField')(_("Display email address to public")))

        # Changing field 'Person.image'
        db.alter_column('people_person', 'image', self.gf('FileBrowseField')(_('Image'), directory="/%s/"%URL_ID_PEOPLE, max_length=255, extensions=['.jpg','.jpeg','.gif','.png','.tif','.tiff'], blank=True))

        # Changing field 'Person.creation_date'
        db.alter_column('people_person', 'creation_date', self.gf('models.DateTimeField')(_("creation date"), editable=False))

        # Changing field 'Person.prefix'
        db.alter_column('people_person', 'prefix_id', self.gf('models.ForeignKey')(orm['optionset.Prefix'], null=True, blank=True))

        # Changing field 'Person.individual_type'
        db.alter_column('people_person', 'individual_type_id', self.gf('models.ForeignKey')(orm['structure.Term'], limit_choices_to=models.Q(vocabulary__sysname='basics_object_types',path_search__contains=ObjectTypeFilter("person"))&~models.Q(models.Q(sysname="person")), null=True, blank=True))

        # Changing field 'Person.display_phone'
        db.alter_column('people_person', 'display_phone', self.gf('models.BooleanField')(_("Display phone numbers to public")))

        # Changing field 'Person.salutation'
        db.alter_column('people_person', 'salutation_id', self.gf('models.ForeignKey')(orm['optionset.Salutation'], null=True, blank=True))

        # Changing field 'Person.timezone'
        db.alter_column('people_person', 'timezone_id', self.gf('models.ForeignKey')(orm['i18n.TimeZone'], max_length=200, null=True, blank=True))

        # Changing field 'Person.description_de'
        db.alter_column('people_person', 'description_de', self.gf('ExtendedTextField')(u'Description', rel=None, unique_for_year=None, blank=True, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, db_tablespace='', unique_for_date=None))

        # Changing field 'Person.occupation'
        db.alter_column('people_person', 'occupation', self.gf('models.CharField')(_("Current Occupation"), max_length=200, blank=True))

        # Changing field 'Person.modified_date'
        db.alter_column('people_person', 'modified_date', self.gf('models.DateTimeField')(_("modified date"), null=True, editable=False))

        # Changing field 'Person.birthname'
        db.alter_column('people_person', 'birthname', self.gf('models.CharField')(_("Birth / Maiden name"), max_length=200, blank=True))

        # Changing field 'Person.display_im'
        db.alter_column('people_person', 'display_im', self.gf('models.BooleanField')(_("Display instant messengers to public")))

        # Changing field 'Person.allow_search_engine_indexing'
        db.alter_column('people_person', 'allow_search_engine_indexing', self.gf('models.BooleanField')(_("Allow indexing by search engines")))

        # Changing field 'Person.birthday_yyyy'
        db.alter_column('people_person', 'birthday_yyyy', self.gf('models.IntegerField')(_("Year of Birth"), null=True, blank=True))

        # Changing field 'Person.display_address'
        db.alter_column('people_person', 'display_address', self.gf('models.BooleanField')(_("Display address data to public")))

        # Changing field 'Person.description'
        db.alter_column('people_person', 'description', self.gf('MultilingualTextField')(_("Description"), blank=True))

        # Changing field 'Person.degree'
        db.alter_column('people_person', 'degree', self.gf('models.CharField')(_("Academic Degree"), max_length=200, blank=True))

        # Changing field 'Person.display_fax'
        db.alter_column('people_person', 'display_fax', self.gf('models.BooleanField')(_("Display fax numbers to public")))

        # Changing field 'Person.description_en'
        db.alter_column('people_person', 'description_en', self.gf('ExtendedTextField')(u'Description', rel=None, unique_for_year=None, blank=True, unique=False, unique_for_month=None, null=False, primary_key=False, db_column=None, max_length=None, db_tablespace='', unique_for_date=None))

        # Changing field 'Person.user'
        db.alter_column('people_person', 'user_id', self.gf('models.OneToOneField')(orm['auth.User'], unique=True))

        # Changing field 'Person.display_birthday'
        db.alter_column('people_person', 'display_birthday', self.gf('models.BooleanField')(_("Display birthday to public")))

        # Changing field 'Person.nationality'
        db.alter_column('people_person', 'nationality_id', self.gf('models.ForeignKey')(orm['i18n.Nationality'], limit_choices_to={'display':True}, max_length=200, null=True, blank=True))

        # Changing field 'Person.nickname'
        db.alter_column('people_person', 'nickname', self.gf('models.CharField')(_("Nickname"), max_length=200, blank=True))

        # Changing field 'Person.preferred_language'
        db.alter_column('people_person', 'preferred_language_id', self.gf('models.ForeignKey')(orm['i18n.Language'], limit_choices_to={'display':True}, null=True, blank=True))

        # Changing field 'Person.gender'
        db.alter_column('people_person', 'gender', self.gf('models.CharField')(_("Gender"), max_length=1, blank=True))

        # Changing field 'Person.display_username'
        db.alter_column('people_person', 'display_username', self.gf('models.BooleanField')(_("Display user name instead of full name")))

        # Changing field 'Person.birthday_mm'
        db.alter_column('people_person', 'birthday_mm', self.gf('models.SmallIntegerField')(_("Month of Birth"), null=True, blank=True))

        # Changing field 'Person.status'
        db.alter_column('people_person', 'status_id', self.gf('models.ForeignKey')(orm['structure.Term'], limit_choices_to={'vocabulary__sysname':'basics_object_statuses'}, null=True, blank=True))

        # Changing field 'Person.display_mobile'
        db.alter_column('people_person', 'display_mobile', self.gf('models.BooleanField')(_("Display mobile phones to public")))

        # Changing field 'IndividualContact.is_phone2_on_hold'
        db.alter_column('people_individualcontact', 'is_phone2_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'IndividualContact.institutional_title'
        db.alter_column('people_individualcontact', 'institutional_title', self.gf('models.CharField')(_("Title in the institution"), max_length=255, blank=True))

        # Changing field 'IndividualContact.location_type'
        db.alter_column('people_individualcontact', 'location_type_id', self.gf('models.ForeignKey')(orm['optionset.IndividualLocationType']))

        # Changing field 'IndividualContact.is_im0_default'
        db.alter_column('people_individualcontact', 'is_im0_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'IndividualContact.email0_type'
        db.alter_column('people_individualcontact', 'email0_type_id', self.gf('models.ForeignKey')(orm['optionset.EmailType'], null=True, blank=True))

        # Changing field 'IndividualContact.is_im2_default'
        db.alter_column('people_individualcontact', 'is_im2_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'IndividualContact.is_phone2_default'
        db.alter_column('people_individualcontact', 'is_phone2_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'IndividualContact.is_url0_default'
        db.alter_column('people_individualcontact', 'is_url0_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'IndividualContact.is_primary'
        db.alter_column('people_individualcontact', 'is_primary', self.gf('models.BooleanField')(_("Primary contact")))

        # Changing field 'IndividualContact.is_url2_default'
        db.alter_column('people_individualcontact', 'is_url2_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'IndividualContact.validity_start_mm'
        db.alter_column('people_individualcontact', 'validity_start_mm', self.gf('models.SmallIntegerField')(_("From Month"), null=True, blank=True))

        # Changing field 'IndividualContact.phone1_type'
        db.alter_column('people_individualcontact', 'phone1_type_id', self.gf('models.ForeignKey')(orm['optionset.PhoneType'], null=True, blank=True))

        # Changing field 'IndividualContact.is_url1_on_hold'
        db.alter_column('people_individualcontact', 'is_url1_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'IndividualContact.is_phone0_default'
        db.alter_column('people_individualcontact', 'is_phone0_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'IndividualContact.url1_link'
        db.alter_column('people_individualcontact', 'url1_link', self.gf('URLField')(_("URL"), blank=True))

        # Changing field 'IndividualContact.url0_link'
        db.alter_column('people_individualcontact', 'url0_link', self.gf('URLField')(_("URL"), blank=True))

        # Changing field 'IndividualContact.email1_type'
        db.alter_column('people_individualcontact', 'email1_type_id', self.gf('models.ForeignKey')(orm['optionset.EmailType'], null=True, blank=True))

        # Changing field 'IndividualContact.phone0_type'
        db.alter_column('people_individualcontact', 'phone0_type_id', self.gf('models.ForeignKey')(orm['optionset.PhoneType'], null=True, blank=True))

        # Changing field 'IndividualContact.phone2_country'
        db.alter_column('people_individualcontact', 'phone2_country', self.gf('models.CharField')(_("Country Code"), max_length=4, blank=True))

        # Changing field 'IndividualContact.is_im0_on_hold'
        db.alter_column('people_individualcontact', 'is_im0_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'IndividualContact.im1_type'
        db.alter_column('people_individualcontact', 'im1_type_id', self.gf('models.ForeignKey')(orm['optionset.IMType'], null=True, blank=True))

        # Changing field 'IndividualContact.im2_type'
        db.alter_column('people_individualcontact', 'im2_type_id', self.gf('models.ForeignKey')(orm['optionset.IMType'], null=True, blank=True))

        # Changing field 'IndividualContact.is_im1_default'
        db.alter_column('people_individualcontact', 'is_im1_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'IndividualContact.is_url2_on_hold'
        db.alter_column('people_individualcontact', 'is_url2_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'IndividualContact.validity_end_mm'
        db.alter_column('people_individualcontact', 'validity_end_mm', self.gf('models.SmallIntegerField')(_("Till Month"), null=True, blank=True))

        # Changing field 'IndividualContact.person'
        db.alter_column('people_individualcontact', 'person_id', self.gf('models.ForeignKey')(orm['people.person']))

        # Changing field 'IndividualContact.phone1_country'
        db.alter_column('people_individualcontact', 'phone1_country', self.gf('models.CharField')(_("Country Code"), max_length=4, blank=True))

        # Changing field 'IndividualContact.im0_type'
        db.alter_column('people_individualcontact', 'im0_type_id', self.gf('models.ForeignKey')(orm['optionset.IMType'], null=True, blank=True))

        # Changing field 'IndividualContact.url0_type'
        db.alter_column('people_individualcontact', 'url0_type_id', self.gf('models.ForeignKey')(orm['optionset.URLType'], null=True, blank=True))

        # Changing field 'IndividualContact.is_phone0_on_hold'
        db.alter_column('people_individualcontact', 'is_phone0_on_hold', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'IndividualContact.is_email1_default'
        db.alter_column('people_individualcontact', 'is_email1_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'IndividualContact.email2_type'
        db.alter_column('people_individualcontact', 'email2_type_id', self.gf('models.ForeignKey')(orm['optionset.EmailType'], null=True, blank=True))

        # Changing field 'IndividualContact.validity_start_dd'
        db.alter_column('people_individualcontact', 'validity_start_dd', self.gf('models.SmallIntegerField')(_("From Day"), null=True, blank=True))

        # Changing field 'IndividualContact.email2_address'
        db.alter_column('people_individualcontact', 'email2_address', self.gf('models.CharField')(_("Email Address"), max_length=255, blank=True))

        # Changing field 'IndividualContact.is_email0_on_hold'
        db.alter_column('people_individualcontact', 'is_email0_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'IndividualContact.is_im2_on_hold'
        db.alter_column('people_individualcontact', 'is_im2_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'IndividualContact.is_email2_default'
        db.alter_column('people_individualcontact', 'is_email2_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'IndividualContact.email0_address'
        db.alter_column('people_individualcontact', 'email0_address', self.gf('models.CharField')(_("Email Address"), max_length=255, blank=True))

        # Changing field 'IndividualContact.phone0_area'
        db.alter_column('people_individualcontact', 'phone0_area', self.gf('models.CharField')(_("Area Code"), max_length=5, blank=True))

        # Changing field 'IndividualContact.im1_address'
        db.alter_column('people_individualcontact', 'im1_address', self.gf('models.CharField')(_("Instant Messenger"), max_length=255, blank=True))

        # Changing field 'IndividualContact.postal_address'
        db.alter_column('people_individualcontact', 'postal_address_id', self.gf('models.ForeignKey')(orm['location.Address'], null=True, blank=True))

        # Changing field 'IndividualContact.is_email2_on_hold'
        db.alter_column('people_individualcontact', 'is_email2_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'IndividualContact.phone0_country'
        db.alter_column('people_individualcontact', 'phone0_country', self.gf('models.CharField')(_("Country Code"), max_length=4, blank=True))

        # Changing field 'IndividualContact.is_billing_address'
        db.alter_column('people_individualcontact', 'is_billing_address', self.gf('models.BooleanField')(_("Use this address for billing")))

        # Changing field 'IndividualContact.im2_address'
        db.alter_column('people_individualcontact', 'im2_address', self.gf('models.CharField')(_("Instant Messenger"), max_length=255, blank=True))

        # Changing field 'IndividualContact.location_title'
        db.alter_column('people_individualcontact', 'location_title', self.gf('models.CharField')(_("Location title"), max_length=255, blank=True))

        # Changing field 'IndividualContact.validity_end_yyyy'
        db.alter_column('people_individualcontact', 'validity_end_yyyy', self.gf('models.IntegerField')(_("Till Year"), null=True, blank=True))

        # Changing field 'IndividualContact.im0_address'
        db.alter_column('people_individualcontact', 'im0_address', self.gf('models.CharField')(_("Instant Messenger"), max_length=255, blank=True))

        # Changing field 'IndividualContact.email1_address'
        db.alter_column('people_individualcontact', 'email1_address', self.gf('models.CharField')(_("Email Address"), max_length=255, blank=True))

        # Changing field 'IndividualContact.is_url0_on_hold'
        db.alter_column('people_individualcontact', 'is_url0_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'IndividualContact.url1_type'
        db.alter_column('people_individualcontact', 'url1_type_id', self.gf('models.ForeignKey')(orm['optionset.URLType'], null=True, blank=True))

        # Changing field 'IndividualContact.url2_type'
        db.alter_column('people_individualcontact', 'url2_type_id', self.gf('models.ForeignKey')(orm['optionset.URLType'], null=True, blank=True))

        # Changing field 'IndividualContact.is_email0_default'
        db.alter_column('people_individualcontact', 'is_email0_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'IndividualContact.is_phone1_on_hold'
        db.alter_column('people_individualcontact', 'is_phone1_on_hold', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'IndividualContact.validity_end_dd'
        db.alter_column('people_individualcontact', 'validity_end_dd', self.gf('models.SmallIntegerField')(_("Till Day"), null=True, blank=True))

        # Changing field 'IndividualContact.phone2_type'
        db.alter_column('people_individualcontact', 'phone2_type_id', self.gf('models.ForeignKey')(orm['optionset.PhoneType'], null=True, blank=True))

        # Changing field 'IndividualContact.is_url1_default'
        db.alter_column('people_individualcontact', 'is_url1_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'IndividualContact.url2_link'
        db.alter_column('people_individualcontact', 'url2_link', self.gf('URLField')(_("URL"), blank=True))

        # Changing field 'IndividualContact.phone0_number'
        db.alter_column('people_individualcontact', 'phone0_number', self.gf('models.CharField')(_("Subscriber Number and Extension"), max_length=15, blank=True))

        # Changing field 'IndividualContact.is_email1_on_hold'
        db.alter_column('people_individualcontact', 'is_email1_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'IndividualContact.phone1_number'
        db.alter_column('people_individualcontact', 'phone1_number', self.gf('models.CharField')(_("Subscriber Number and Extension"), max_length=15, blank=True))

        # Changing field 'IndividualContact.is_shipping_address'
        db.alter_column('people_individualcontact', 'is_shipping_address', self.gf('models.BooleanField')(_("Use this address for shipping")))

        # Changing field 'IndividualContact.phone1_area'
        db.alter_column('people_individualcontact', 'phone1_area', self.gf('models.CharField')(_("Area Code"), max_length=5, blank=True))

        # Changing field 'IndividualContact.is_im1_on_hold'
        db.alter_column('people_individualcontact', 'is_im1_on_hold', self.gf('models.BooleanField')(_("On Hold?")))

        # Changing field 'IndividualContact.phone2_area'
        db.alter_column('people_individualcontact', 'phone2_area', self.gf('models.CharField')(_("Area Code"), max_length=5, blank=True))

        # Changing field 'IndividualContact.phone2_number'
        db.alter_column('people_individualcontact', 'phone2_number', self.gf('models.CharField')(_("Subscriber Number and Extension"), max_length=15, blank=True))

        # Changing field 'IndividualContact.is_phone1_default'
        db.alter_column('people_individualcontact', 'is_phone1_default', self.gf('models.BooleanField')(_("Default?")))

        # Changing field 'IndividualContact.is_seasonal'
        db.alter_column('people_individualcontact', 'is_seasonal', self.gf('models.BooleanField')(_("Seasonal")))

        # Changing field 'IndividualContact.validity_start_yyyy'
        db.alter_column('people_individualcontact', 'validity_start_yyyy', self.gf('models.IntegerField')(_("From Year"), null=True, blank=True))
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'i18n.country': {
            'Meta': {'object_name': 'Country'},
            'adm_area': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'iso2_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2', 'primary_key': 'True'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '56'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '56', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'territory_of': ('django.db.models.fields.CharField', [], {'max_length': '3', 'blank': 'True'})
        },
        'i18n.language': {
            'Meta': {'object_name': 'Language'},
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso2_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'synonym': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        'i18n.nationality': {
            'Meta': {'object_name': 'Nationality'},
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'name_de': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'})
        },
        'i18n.timezone': {
            'Meta': {'object_name': 'TimeZone'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'zone': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'})
        },
        'institutions.institution': {
            'Meta': {'object_name': 'Institution'},
            'access': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'context_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.ContextCategory']", 'symmetrical': 'False', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creative_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'creative_sector_institutions'", 'blank': 'True', 'to': "orm['structure.Term']"}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'establishment_mm': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'establishment_yyyy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exceptions': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'exceptions_de': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_en': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'fri_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'/institutions/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'institution_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.Term']", 'symmetrical': 'False'}),
            'is_appointment_based': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_card_americanexpress_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_card_mastercard_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_card_visa_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_cash_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_ec_maestro_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_giropay_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_invoice_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_non_profit': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_on_delivery_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_parking_avail': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_paypal_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_prepayment_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_transaction_ok': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_wlan_avail': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'legal_form': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'legal_form_institution'", 'null': 'True', 'to': "orm['structure.Term']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'mon_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'nof_employees': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['institutions.Institution']", 'null': 'True', 'blank': 'True'}),
            'sat_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '87L', 'related_name': "'status_institution_set'", 'null': 'True', 'blank': 'True', 'to': "orm['structure.Term']"}),
            'sun_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tax_id_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'thu_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'title2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tue_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'vat_id_number': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'wed_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'location.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'default': "'Berlin'", 'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'default': "'DE'", 'to': "orm['i18n.Country']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'street_address3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'optionset.emailtype': {
            'Meta': {'object_name': 'EmailType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.imtype': {
            'Meta': {'object_name': 'IMType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.individuallocationtype': {
            'Meta': {'object_name': 'IndividualLocationType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.phonetype': {
            'Meta': {'object_name': 'PhoneType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'vcard_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        'optionset.prefix': {
            'Meta': {'object_name': 'Prefix'},
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.salutation': {
            'Meta': {'object_name': 'Salutation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'template': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'template_de': ('django.db.models.fields.CharField', ["u'template'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'template_en': ('django.db.models.fields.CharField', ["u'template'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'optionset.urltype': {
            'Meta': {'object_name': 'URLType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'people.individualcontact': {
            'Meta': {'object_name': 'IndividualContact'},
            'email0_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email0_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'individual_contacts0'", 'null': 'True', 'to': "orm['optionset.EmailType']"}),
            'email1_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email1_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'individual_contacts1'", 'null': 'True', 'to': "orm['optionset.EmailType']"}),
            'email2_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email2_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'individual_contacts2'", 'null': 'True', 'to': "orm['optionset.EmailType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'im0_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'im0_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'individual_contacts0'", 'null': 'True', 'to': "orm['optionset.IMType']"}),
            'im1_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'im1_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'individual_contacts1'", 'null': 'True', 'to': "orm['optionset.IMType']"}),
            'im2_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'im2_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'individual_contacts2'", 'null': 'True', 'to': "orm['optionset.IMType']"}),
            'institution': ('django.db.models.fields.related.ForeignKey', ["orm['institutions.institution']"], {'null': 'True', 'blank': 'True'}),
            'institutional_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'is_billing_address': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_email0_default': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_email0_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_email1_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_email1_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_email2_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_email2_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_im0_default': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_im0_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_im1_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_im1_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_im2_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_im2_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_phone0_default': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_phone0_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_phone1_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_phone1_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_phone2_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_phone2_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_seasonal': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_shipping_address': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_url0_default': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_url0_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_url1_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_url1_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_url2_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_url2_on_hold': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'location_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'location_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1L', 'to': "orm['optionset.IndividualLocationType']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['people.Person']"}),
            'phone0_area': ('django.db.models.fields.CharField', [], {'default': "'30'", 'max_length': '5', 'blank': 'True'}),
            'phone0_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone0_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'phone0_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1L', 'related_name': "'individual_contacts0'", 'null': 'True', 'blank': 'True', 'to': "orm['optionset.PhoneType']"}),
            'phone1_area': ('django.db.models.fields.CharField', [], {'default': "'30'", 'max_length': '5', 'blank': 'True'}),
            'phone1_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone1_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'phone1_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '2L', 'related_name': "'individual_contacts1'", 'null': 'True', 'blank': 'True', 'to': "orm['optionset.PhoneType']"}),
            'phone2_area': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'phone2_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone2_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'phone2_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '3L', 'related_name': "'individual_contacts2'", 'null': 'True', 'blank': 'True', 'to': "orm['optionset.PhoneType']"}),
            'postal_address': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'individual_address'", 'null': 'True', 'to': "orm['location.Address']"}),
            'url0_link': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'url0_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'individual_contacts0'", 'null': 'True', 'to': "orm['optionset.URLType']"}),
            'url1_link': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'url1_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'individual_contacts1'", 'null': 'True', 'to': "orm['optionset.URLType']"}),
            'url2_link': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'url2_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'individual_contacts2'", 'null': 'True', 'to': "orm['optionset.URLType']"}),
            'validity_end_dd': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'validity_end_mm': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'validity_end_yyyy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'validity_start_dd': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'validity_start_mm': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'validity_start_yyyy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'people.person': {
            'Meta': {'object_name': 'Person'},
            'allow_search_engine_indexing': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'birthday_dd': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'birthday_mm': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'birthday_yyyy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'birthname': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'completeness': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'context_categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['structure.ContextCategory']", 'symmetrical': 'False', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creative_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'creative_industry_people'", 'blank': 'True', 'to': "orm['structure.Term']"}),
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'display_address': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'display_birthday': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'display_email': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'display_fax': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'display_im': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'display_mobile': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'display_phone': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'display_username': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'/people/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'individual_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Term']", 'null': 'True', 'blank': 'True'}),
            'interests': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'nationality': ('django.db.models.fields.related.ForeignKey', [], {'max_length': '200', 'to': "orm['i18n.Nationality']", 'null': 'True', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'preferred_language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['i18n.Language']", 'null': 'True', 'blank': 'True'}),
            'prefix': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['optionset.Prefix']", 'null': 'True', 'blank': 'True'}),
            'salutation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['optionset.Salutation']", 'null': 'True', 'blank': 'True'}),
            'spoken_languages': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'speaking_people'", 'blank': 'True', 'to': "orm['i18n.Language']"}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'default': '87L', 'related_name': "'status_person_set'", 'null': 'True', 'blank': 'True', 'to': "orm['structure.Term']"}),
            'timezone': ('django.db.models.fields.related.ForeignKey', [], {'max_length': '200', 'to': "orm['i18n.TimeZone']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'permissions.rowlevelpermission': {
            'Meta': {'object_name': 'RowLevelPermission', 'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': "orm['contenttypes.ContentType']"}),
            'owner_object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.Permission']"})
        },
        'structure.contextcategory': {
            'Meta': {'object_name': 'ContextCategory'},
            'body': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'body_de': ('base_libs.models.fields.ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_en': ('base_libs.models.fields.ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'creative_sectors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['structure.Term']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'is_applied4document': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_applied4event': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_applied4institution': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_applied4person': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_applied4persongroup': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['structure.ContextCategory']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '8192', 'null': 'True'}),
            'path_search': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        },
        'structure.term': {
            'Meta': {'object_name': 'Term'},
            'body': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'body_de': ('base_libs.models.fields.ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_en': ('base_libs.models.fields.ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'child_set'", 'null': 'True', 'to': "orm['structure.Term']"}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '8192', 'null': 'True'}),
            'path_search': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'vocabulary': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['structure.Vocabulary']"})
        },
        'structure.vocabulary': {
            'Meta': {'object_name': 'Vocabulary'},
            'body': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'body_de': ('base_libs.models.fields.ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_en': ('base_libs.models.fields.ExtendedTextField', ["u'body'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'body_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'body_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'hierarchy': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff']", 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'False', 'unique': 'False', 'db_index': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['people']
