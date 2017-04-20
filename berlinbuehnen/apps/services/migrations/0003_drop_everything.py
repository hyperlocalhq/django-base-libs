# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
                # Deleting model 'ImageAndText'
        db.delete_table(u'cmsplugin_imageandtext')

        # Deleting model 'Service'
        db.delete_table(u'services_service')

        # Deleting model 'ArticlesPage'
        db.delete_table(u'services_articlespage')

        # Deleting model 'Link'
        db.delete_table(u'services_link')

        # Deleting model 'ServicesOverviewPage'
        db.delete_table(u'services_servicesoverviewpage')

        # Deleting model 'ServicePage'
        db.delete_table(u'services_servicepage')

        # Deleting model 'ServicesCategory'
        db.delete_table(u'services_servicescategory')

        # Deleting model 'TitleAndText'
        db.delete_table(u'cmsplugin_titleandtext')

        # Deleting model 'LinksPage'
        db.delete_table(u'services_linkspage')

        # Deleting model 'LinkCategory'
        db.delete_table(u'cmsplugin_linkcategory')

        # Deleting model 'IndexItem'
        db.delete_table(u'cmsplugin_indexitem')

    
    
    def backwards(self, orm):
        
        # Adding model 'ImageAndText'
        db.create_table(u'cmsplugin_imageandtext', south_cleaned_fields((
            ('body', self.gf('base_libs.models.fields.ExtendedTextField')()),
            ('layout', self.gf('django.db.models.fields.CharField')(default=u'image-left', max_length=20)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, extensions=[u'.jpg', u'.jpeg', u'.gif', u'.png'])),
            ('body_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal(u'services', ['ImageAndText'])

        # Adding model 'Service'
        db.create_table(u'services_service', south_cleaned_fields((
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title', unique=False, max_length=200, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False)),
            ('subtitle', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=200, null=True, blank=True)),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(directory=u'services/', max_length=255, extensions=[u'.jpg', u'.jpeg', u'.gif', u'.png'])),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('short_description_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('subtitle_en', self.gf('django.db.models.fields.CharField')(u'Subtitle', unique=False, max_length=200, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.ServicesCategory'])),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=200, null=True)),
            ('short_description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Short Description', rel=None, unique_for_year=None, blank=True, unique_for_date=None, db_index=False, unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, db_tablespace='')),
            ('short_description_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('external_link', self.gf('base_libs.models.fields.MultilingualURLField')(max_length=255, null=True)),
            ('short_description', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('external_link_en', self.gf('django.db.models.fields.CharField')(u'External Link', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Location'], null=True, blank=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title', unique=False, max_length=200, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False)),
            ('subtitle_de', self.gf('django.db.models.fields.CharField')(u'Subtitle', unique=False, max_length=200, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('short_description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Short Description', rel=None, unique_for_year=None, blank=True, unique_for_date=None, db_index=False, unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, db_tablespace='')),
            ('external_link_de', self.gf('django.db.models.fields.CharField')(u'External Link', unique=False, max_length=255, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False)),
        )))
        db.send_create_signal(u'services', ['Service'])

        # Adding model 'ArticlesPage'
        db.create_table(u'services_articlespage', south_cleaned_fields((
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Placeholder'], null=True)),
            (u'servicepage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['services.ServicePage'], unique=True, primary_key=True)),
        )))
        db.send_create_signal(u'services', ['ArticlesPage'])

        # Adding model 'Link'
        db.create_table(u'services_link', south_cleaned_fields((
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.LinkCategory'])),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('short_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
        )))
        db.send_create_signal(u'services', ['Link'])

        # Adding model 'ServicesOverviewPage'
        db.create_table(u'services_servicesoverviewpage', south_cleaned_fields((
            (u'servicepage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['services.ServicePage'], unique=True, primary_key=True)),
        )))
        db.send_create_signal(u'services', ['ServicesOverviewPage'])

        # Adding model 'ServicePage'
        db.create_table(u'services_servicepage', south_cleaned_fields((
            ('status', self.gf('django.db.models.fields.CharField')(default=u'draft', max_length=20, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('header_icon', self.gf('filebrowser.fields.FileBrowseField')(directory=u'services/', max_length=255, extensions=[u'.jpg', u'.jpeg', u'.gif', u'.png'])),
            ('short_description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Short Description', rel=None, unique_for_year=None, blank=True, unique_for_date=None, db_index=False, unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, db_tablespace='')),
            ('short_description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Short Description', rel=None, unique_for_year=None, blank=True, unique_for_date=None, db_index=False, unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, db_tablespace='')),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, unique=True)),
            ('short_description_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title', unique=False, max_length=200, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('short_description', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('short_description_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('header_bg_color', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=200, null=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title', unique=False, max_length=200, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        )))
        db.send_create_signal(u'services', ['ServicePage'])

        # Adding model 'ServicesCategory'
        db.create_table(u'services_servicescategory', south_cleaned_fields((
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title', unique=False, max_length=200, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255, unique=True)),
            ('subtitle', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=200, null=True, blank=True)),
            ('short_description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Short Description', rel=None, unique_for_year=None, blank=True, unique_for_date=None, db_index=False, unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, db_tablespace='')),
            ('short_description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Short Description', rel=None, unique_for_year=None, blank=True, unique_for_date=None, db_index=False, unique_for_month=None, unique=False, primary_key=False, db_column=None, max_length=None, db_tablespace='')),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(directory=u'services/', max_length=255, extensions=[u'.jpg', u'.jpeg', u'.gif', u'.png'])),
            ('short_description_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title', unique=False, max_length=200, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('subtitle_de', self.gf('django.db.models.fields.CharField')(u'Subtitle', unique=False, max_length=200, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False)),
            ('short_description_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=200, null=True)),
            ('short_description', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('subtitle_en', self.gf('django.db.models.fields.CharField')(u'Subtitle', unique=False, max_length=200, primary_key=False, db_column=None, blank=True, default='', null=False, editable=True, db_tablespace='', db_index=False)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.ServicesOverviewPage'])),
        )))
        db.send_create_signal(u'services', ['ServicesCategory'])

        # Adding model 'TitleAndText'
        db.create_table(u'cmsplugin_titleandtext', south_cleaned_fields((
            ('body', self.gf('base_libs.models.fields.ExtendedTextField')()),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('width', self.gf('django.db.models.fields.CharField')(default=u'full', max_length=20)),
            ('body_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal(u'services', ['TitleAndText'])

        # Adding model 'LinksPage'
        db.create_table(u'services_linkspage', south_cleaned_fields((
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Placeholder'], null=True)),
            (u'servicepage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['services.ServicePage'], unique=True, primary_key=True)),
        )))
        db.send_create_signal(u'services', ['LinksPage'])

        # Adding model 'LinkCategory'
        db.create_table(u'cmsplugin_linkcategory', south_cleaned_fields((
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        )))
        db.send_create_signal(u'services', ['LinkCategory'])

        # Adding model 'IndexItem'
        db.create_table(u'cmsplugin_indexitem', south_cleaned_fields((
            ('service_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.ServicePage'])),
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('width', self.gf('django.db.models.fields.CharField')(default=u'sigle', max_length=20)),
        )))
        db.send_create_signal(u'services', ['IndexItem'])
    
    
    models = {
        
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['services']
