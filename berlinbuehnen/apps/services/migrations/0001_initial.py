# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'ServicePage'
        db.create_table(u'services_servicepage', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=200, null=True)),
            ('short_description', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('header_bg_color', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('header_icon', self.gf('filebrowser.fields.FileBrowseField')(directory=u'services/', max_length=255, extensions=[u'.jpg', u'.jpeg', u'.gif', u'.png'])),
            ('status', self.gf('django.db.models.fields.CharField')(default=u'draft', max_length=20, blank=True)),
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('short_description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Short Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('short_description_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('short_description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Short Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('short_description_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal(u'services', ['ServicePage'])

        # Adding model 'IndexItem'
        db.create_table(u'cmsplugin_indexitem', south_cleaned_fields((
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('service_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.ServicePage'])),
            ('width', self.gf('django.db.models.fields.CharField')(default=u'sigle', max_length=20)),
        )))
        db.send_create_signal(u'services', ['IndexItem'])

        # Adding model 'ServicesOverviewPage'
        db.create_table(u'services_servicesoverviewpage', south_cleaned_fields((
            (u'servicepage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['services.ServicePage'], unique=True, primary_key=True)),
        )))
        db.send_create_signal(u'services', ['ServicesOverviewPage'])

        # Adding model 'ServicesCategory'
        db.create_table(u'services_servicescategory', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.ServicesOverviewPage'])),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=200, null=True)),
            ('subtitle', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=200, null=True, blank=True)),
            ('short_description', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(directory=u'services/', max_length=255, extensions=[u'.jpg', u'.jpeg', u'.gif', u'.png'])),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('subtitle_de', self.gf('django.db.models.fields.CharField')(u'Subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('subtitle_en', self.gf('django.db.models.fields.CharField')(u'Subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('short_description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Short Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('short_description_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('short_description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Short Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('short_description_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal(u'services', ['ServicesCategory'])

        # Adding model 'Service'
        db.create_table(u'services_service', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.ServicesCategory'])),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=200, null=True)),
            ('subtitle', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=200, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['locations.Location'])),
            ('short_description', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('external_link', self.gf('base_libs.models.fields.MultilingualURLField')(max_length=255, null=True)),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(directory=u'services/', max_length=255, extensions=[u'.jpg', u'.jpeg', u'.gif', u'.png'])),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
            ('subtitle_de', self.gf('django.db.models.fields.CharField')(u'Subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('subtitle_en', self.gf('django.db.models.fields.CharField')(u'Subtitle', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=200, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('short_description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Short Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('short_description_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('short_description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Short Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('short_description_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('external_link_de', self.gf('django.db.models.fields.CharField')(u'External Link', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('external_link_en', self.gf('django.db.models.fields.CharField')(u'External Link', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal(u'services', ['Service'])

        # Adding model 'LinksPage'
        db.create_table(u'services_linkspage', south_cleaned_fields((
            (u'servicepage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['services.ServicePage'], unique=True, primary_key=True)),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Placeholder'], null=True)),
        )))
        db.send_create_signal(u'services', ['LinksPage'])

        # Adding model 'LinkCategory'
        db.create_table(u'cmsplugin_linkcategory', south_cleaned_fields((
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        )))
        db.send_create_signal(u'services', ['LinkCategory'])

        # Adding model 'Link'
        db.create_table(u'services_link', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['services.LinkCategory'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('short_description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=None)),
        )))
        db.send_create_signal(u'services', ['Link'])

        # Adding model 'ArticlesPage'
        db.create_table(u'services_articlespage', south_cleaned_fields((
            (u'servicepage_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['services.ServicePage'], unique=True, primary_key=True)),
            ('content', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Placeholder'], null=True)),
        )))
        db.send_create_signal(u'services', ['ArticlesPage'])

        # Adding model 'TitleAndText'
        db.create_table(u'cmsplugin_titleandtext', south_cleaned_fields((
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('body', self.gf('base_libs.models.fields.ExtendedTextField')()),
            ('width', self.gf('django.db.models.fields.CharField')(default=u'full', max_length=20)),
            ('body_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal(u'services', ['TitleAndText'])

        # Adding model 'ImageAndText'
        db.create_table(u'cmsplugin_imageandtext', south_cleaned_fields((
            (u'cmsplugin_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['cms.CMSPlugin'], unique=True, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('body', self.gf('base_libs.models.fields.ExtendedTextField')()),
            ('image', self.gf('filebrowser.fields.FileBrowseField')(max_length=255, extensions=[u'.jpg', u'.jpeg', u'.gif', u'.png'])),
            ('alt', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('layout', self.gf('django.db.models.fields.CharField')(default=u'image-left', max_length=20)),
            ('body_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
        )))
        db.send_create_signal(u'services', ['ImageAndText'])
    
    
    def backwards(self, orm):
                # Deleting model 'ServicePage'
        db.delete_table(u'services_servicepage')

        # Deleting model 'IndexItem'
        db.delete_table(u'cmsplugin_indexitem')

        # Deleting model 'ServicesOverviewPage'
        db.delete_table(u'services_servicesoverviewpage')

        # Deleting model 'ServicesCategory'
        db.delete_table(u'services_servicescategory')

        # Deleting model 'Service'
        db.delete_table(u'services_service')

        # Deleting model 'LinksPage'
        db.delete_table(u'services_linkspage')

        # Deleting model 'LinkCategory'
        db.delete_table(u'cmsplugin_linkcategory')

        # Deleting model 'Link'
        db.delete_table(u'services_link')

        # Deleting model 'ArticlesPage'
        db.delete_table(u'services_articlespage')

        # Deleting model 'TitleAndText'
        db.delete_table(u'cmsplugin_titleandtext')

        # Deleting model 'ImageAndText'
        db.delete_table(u'cmsplugin_imageandtext')

    
    
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cms.cmsplugin': {
            'Meta': {'object_name': 'CMSPlugin'},
            'changed_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.CMSPlugin']", 'null': 'True', 'blank': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            'plugin_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'cms.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'default_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'locations.accessibilityoption': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'AccessibilityOption'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'accessibility/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png']", 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'locations.district': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'District'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'locations.location': {
            'Meta': {'ordering': "['title']", 'object_name': 'Location'},
            'accessibility_options': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['locations.AccessibilityOption']", 'symmetrical': 'False', 'blank': 'True'}),
            'categories': ('mptt.fields.TreeManyToManyField', [], {'to': u"orm['locations.LocationCategory']", 'symmetrical': 'False', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'Berlin'", 'max_length': '255'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'location_creator'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'districts': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['locations.District']", 'symmetrical': 'False', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'exceptions': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'exceptions_de': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'exceptions_en': ('base_libs.models.fields.ExtendedTextField', ["u'Exceptions for working hours'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'exceptions_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'fax_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'fax_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'fax_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'fri_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'fri_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_appointment_based': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'logo': ('filebrowser.fields.FileBrowseField', [], {'directory': "'locations/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png']", 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'location_modifier'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'mon_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'mon_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'phone_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'phone_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'press_contact_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'press_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'press_fax_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'press_fax_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'press_fax_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'press_phone_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'press_phone_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'press_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'press_website': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'sat_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sat_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['locations.Service']", 'symmetrical': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '20', 'blank': 'True'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'subtitle': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_en': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'sun_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'sun_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'teaser': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'teaser_de': ('base_libs.models.fields.ExtendedTextField', ["u'Teaser'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'teaser_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'teaser_en': ('base_libs.models.fields.ExtendedTextField', ["u'Teaser'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'teaser_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'thu_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'thu_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tickets_additional_info': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'tickets_additional_info_de': ('base_libs.models.fields.ExtendedTextField', ["u'Additional information'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'tickets_additional_info_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'tickets_additional_info_en': ('base_libs.models.fields.ExtendedTextField', ["u'Additional information'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'tickets_additional_info_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'tickets_calling_prices': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'tickets_calling_prices_de': ('base_libs.models.fields.ExtendedTextField', ["u'Phone calling prices'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'tickets_calling_prices_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'tickets_calling_prices_en': ('base_libs.models.fields.ExtendedTextField', ["u'Phone calling prices'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'tickets_calling_prices_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'tickets_city': ('django.db.models.fields.CharField', [], {'default': "'Berlin'", 'max_length': '255', 'blank': 'True'}),
            'tickets_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'tickets_fax_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'tickets_fax_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'tickets_fax_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'tickets_phone_area': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'tickets_phone_country': ('django.db.models.fields.CharField', [], {'default': "'49'", 'max_length': '4', 'blank': 'True'}),
            'tickets_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'tickets_postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tickets_street_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tickets_street_address2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tickets_website': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tue_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'tue_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('base_libs.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'wed_break_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_break_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_close': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'wed_open': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'locations.locationcategory': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'LocationCategory'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['locations.LocationCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'locations.service': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Service'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "'services/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png']", 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'permissions.rowlevelpermission': {
            'Meta': {'object_name': 'RowLevelPermission', 'db_table': "'auth_rowlevelpermission'"},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'owner_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owner'", 'to': u"orm['contenttypes.ContentType']"}),
            'owner_object_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'permission': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Permission']"})
        },
        u'services.articlespage': {
            'Meta': {'ordering': "[u'title_de']", 'object_name': 'ArticlesPage', '_ormbases': [u'services.ServicePage']},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            u'servicepage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['services.ServicePage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'services.imageandtext': {
            'Meta': {'object_name': 'ImageAndText', 'db_table': "u'cmsplugin_imageandtext'", '_ormbases': ['cms.CMSPlugin']},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'body': ('base_libs.models.fields.ExtendedTextField', [], {}),
            'body_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255', 'extensions': "[u'.jpg', u'.jpeg', u'.gif', u'.png']"}),
            'layout': ('django.db.models.fields.CharField', [], {'default': "u'image-left'", 'max_length': '20'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'services.indexitem': {
            'Meta': {'object_name': 'IndexItem', 'db_table': "u'cmsplugin_indexitem'", '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'service_page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.ServicePage']"}),
            'width': ('django.db.models.fields.CharField', [], {'default': "u'sigle'", 'max_length': '20'})
        },
        u'services.link': {
            'Meta': {'ordering': "[u'sort_order', u'title']", 'object_name': 'Link'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.LinkCategory']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'short_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'services.linkcategory': {
            'Meta': {'object_name': 'LinkCategory', 'db_table': "u'cmsplugin_linkcategory'", '_ormbases': ['cms.CMSPlugin']},
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'services.linkspage': {
            'Meta': {'ordering': "[u'title_de']", 'object_name': 'LinksPage', '_ormbases': [u'services.ServicePage']},
            'content': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Placeholder']", 'null': 'True'}),
            u'servicepage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['services.ServicePage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'services.service': {
            'Meta': {'ordering': "[u'sort_order', u'title_de']", 'object_name': 'Service'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.ServicesCategory']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'external_link': ('base_libs.models.fields.MultilingualURLField', [], {'max_length': '255', 'null': 'True'}),
            'external_link_de': ('django.db.models.fields.CharField', ["u'External Link'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'external_link_en': ('django.db.models.fields.CharField', ["u'External Link'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "u'services/'", 'max_length': '255', 'extensions': "[u'.jpg', u'.jpeg', u'.gif', u'.png']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['locations.Location']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'short_description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'short_description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Short Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'short_description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'short_description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Short Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'short_description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'subtitle': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_en': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'services.servicepage': {
            'Meta': {'ordering': "[u'title_de']", 'object_name': 'ServicePage'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'header_bg_color': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'header_icon': ('filebrowser.fields.FileBrowseField', [], {'directory': "u'services/'", 'max_length': '255', 'extensions': "[u'.jpg', u'.jpeg', u'.gif', u'.png']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'short_description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'short_description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Short Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'short_description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'short_description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Short Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'short_description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'draft'", 'max_length': '20', 'blank': 'True'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'services.servicescategory': {
            'Meta': {'ordering': "[u'title_de']", 'object_name': 'ServicesCategory'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('filebrowser.fields.FileBrowseField', [], {'directory': "u'services/'", 'max_length': '255', 'extensions': "[u'.jpg', u'.jpeg', u'.gif', u'.png']"}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['services.ServicesOverviewPage']"}),
            'short_description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'short_description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Short Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'short_description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'short_description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Short Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'short_description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': 'None'}),
            'subtitle': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'subtitle_de': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'subtitle_en': ('django.db.models.fields.CharField', ["u'Subtitle'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '200', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '200', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'services.servicesoverviewpage': {
            'Meta': {'ordering': "[u'title_de']", 'object_name': 'ServicesOverviewPage', '_ormbases': [u'services.ServicePage']},
            u'servicepage_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['services.ServicePage']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'services.titleandtext': {
            'Meta': {'object_name': 'TitleAndText', 'db_table': "u'cmsplugin_titleandtext'", '_ormbases': ['cms.CMSPlugin']},
            'body': ('base_libs.models.fields.ExtendedTextField', [], {}),
            'body_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            u'cmsplugin_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['cms.CMSPlugin']", 'unique': 'True', 'primary_key': 'True'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'width': ('django.db.models.fields.CharField', [], {'default': "u'full'", 'max_length': '20'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['services']
