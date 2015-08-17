# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Advertiser'
        db.create_table(u'advertising_advertiser', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        )))
        db.send_create_signal(u'advertising', ['Advertiser'])

        # Adding model 'AdCategory'
        db.create_table(u'advertising_adcategory', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sysname', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True)),
            ('description', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('description_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('description_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal(u'advertising', ['AdCategory'])

        # Adding model 'AdZone'
        db.create_table(u'advertising_adzone', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sysname', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255)),
            ('title', self.gf('base_libs.models.fields.MultilingualCharField')(max_length=255, null=True)),
            ('description', self.gf('base_libs.models.fields.MultilingualTextField')(default='', null=True, blank=True)),
            ('description_de', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('description_de_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('description_en', self.gf('base_libs.models.fields.ExtendedTextField')(u'Description', unique_for_month=None, unique_for_date=None, primary_key=False, db_column=None, max_length=None, unique_for_year=None, rel=None, blank=True, unique=False, db_tablespace='', db_index=False)),
            ('description_en_markup_type', self.gf('django.db.models.fields.CharField')('Markup type', default='pt', max_length=10, blank=False)),
            ('title_de', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
            ('title_en', self.gf('django.db.models.fields.CharField')(u'Title', null=False, primary_key=False, db_column=None, default='', editable=True, max_length=255, db_tablespace='', blank=True, unique=False, db_index=False)),
        )))
        db.send_create_signal(u'advertising', ['AdZone'])

        # Adding model 'AdBase'
        db.create_table(u'advertising_adbase', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='adbase_creator', null=True, to=orm['auth.User'])),
            ('modifier', self.gf('django.db.models.fields.related.ForeignKey')(related_name='adbase_modifier', null=True, to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('language', self.gf('django.db.models.fields.CharField')(default='', max_length=5, blank=True)),
            ('start_showing', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('stop_showing', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(9999, 12, 30, 0, 0))),
            ('advertiser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['advertising.Advertiser'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['advertising.AdCategory'], null=True, blank=True)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['advertising.AdZone'])),
            ('show_ad_label', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('impressions_stats', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('clicks_stats', self.gf('django.db.models.fields.TextField')(blank=True)),
        )))
        db.send_create_signal(u'advertising', ['AdBase'])

        # Adding model 'AdImpression'
        db.create_table(u'advertising_adimpression', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('impression_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('source_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('ad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['advertising.AdBase'])),
        )))
        db.send_create_signal(u'advertising', ['AdImpression'])

        # Adding model 'AdClick'
        db.create_table(u'advertising_adclick', south_cleaned_fields((
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('click_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('source_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('ad', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['advertising.AdBase'])),
        )))
        db.send_create_signal(u'advertising', ['AdClick'])

        # Adding model 'TextAd'
        db.create_table(u'advertising_textad', south_cleaned_fields((
            (u'adbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['advertising.AdBase'], unique=True, primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        )))
        db.send_create_signal(u'advertising', ['TextAd'])

        # Adding model 'BannerAd'
        db.create_table(u'advertising_bannerad', south_cleaned_fields((
            (u'adbase_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['advertising.AdBase'], unique=True, primary_key=True)),
            ('content', self.gf('filebrowser.fields.FileBrowseField')(directory='advertising/', max_length=255, extensions=['.jpg', '.jpeg', '.gif', '.png'])),
        )))
        db.send_create_signal(u'advertising', ['BannerAd'])
    
    
    def backwards(self, orm):
                # Deleting model 'Advertiser'
        db.delete_table(u'advertising_advertiser')

        # Deleting model 'AdCategory'
        db.delete_table(u'advertising_adcategory')

        # Deleting model 'AdZone'
        db.delete_table(u'advertising_adzone')

        # Deleting model 'AdBase'
        db.delete_table(u'advertising_adbase')

        # Deleting model 'AdImpression'
        db.delete_table(u'advertising_adimpression')

        # Deleting model 'AdClick'
        db.delete_table(u'advertising_adclick')

        # Deleting model 'TextAd'
        db.delete_table(u'advertising_textad')

        # Deleting model 'BannerAd'
        db.delete_table(u'advertising_bannerad')

    
    
    models = {
        u'advertising.adbase': {
            'Meta': {'object_name': 'AdBase'},
            'advertiser': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['advertising.Advertiser']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['advertising.AdCategory']", 'null': 'True', 'blank': 'True'}),
            'clicks_stats': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adbase_creator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impressions_stats': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modifier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'adbase_modifier'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'show_ad_label': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'start_showing': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'stop_showing': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(9999, 12, 30, 0, 0)'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['advertising.AdZone']"})
        },
        u'advertising.adcategory': {
            'Meta': {'ordering': "('title',)", 'object_name': 'AdCategory'},
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'advertising.adclick': {
            'Meta': {'object_name': 'AdClick'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['advertising.AdBase']"}),
            'click_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        u'advertising.adimpression': {
            'Meta': {'object_name': 'AdImpression'},
            'ad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['advertising.AdBase']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'impression_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'source_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        u'advertising.advertiser': {
            'Meta': {'ordering': "('company_name',)", 'object_name': 'Advertiser'},
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'advertising.adzone': {
            'Meta': {'ordering': "('title',)", 'object_name': 'AdZone'},
            'description': ('base_libs.models.fields.MultilingualTextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'description_de': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_de_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            'description_en': ('base_libs.models.fields.ExtendedTextField', ["u'Description'"], {'unique_for_month': 'None', 'unique_for_date': 'None', 'primary_key': 'False', 'db_column': 'None', 'max_length': 'None', 'unique_for_year': 'None', 'rel': 'None', 'blank': 'True', 'unique': 'False', 'db_tablespace': "''", 'db_index': 'False'}),
            'description_en_markup_type': ('django.db.models.fields.CharField', ["'Markup type'"], {'default': "'pt'", 'max_length': '10', 'blank': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sysname': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'title': ('base_libs.models.fields.MultilingualCharField', [], {'max_length': '255', 'null': 'True'}),
            'title_de': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'}),
            'title_en': ('django.db.models.fields.CharField', ["u'Title'"], {'null': 'False', 'primary_key': 'False', 'db_column': 'None', 'default': "''", 'editable': 'True', 'max_length': '255', 'db_tablespace': "''", 'blank': 'True', 'unique': 'False', 'db_index': 'False'})
        },
        u'advertising.bannerad': {
            'Meta': {'object_name': 'BannerAd', '_ormbases': [u'advertising.AdBase']},
            u'adbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['advertising.AdBase']", 'unique': 'True', 'primary_key': 'True'}),
            'content': ('filebrowser.fields.FileBrowseField', [], {'directory': "'advertising/'", 'max_length': '255', 'extensions': "['.jpg', '.jpeg', '.gif', '.png']"})
        },
        u'advertising.textad': {
            'Meta': {'object_name': 'TextAd', '_ormbases': [u'advertising.AdBase']},
            u'adbase_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['advertising.AdBase']", 'unique': 'True', 'primary_key': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {})
        },
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('app_label', 'name')", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['advertising']
