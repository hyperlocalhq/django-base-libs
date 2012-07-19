# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'SearchSettings'
        db.create_table('twitterwall_searchsettings', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('query', self.gf('django.db.models.fields.CharField')(max_length=140)),
        )))
        db.send_create_signal('twitterwall', ['SearchSettings'])

        # Adding M2M table for field sites on 'SearchSettings'
        db.create_table('twitterwall_searchsettings_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('searchsettings', models.ForeignKey(orm['twitterwall.searchsettings'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('twitterwall_searchsettings_sites', ['searchsettings_id', 'site_id'])

        # Adding model 'UserTimelineSettings'
        db.create_table('twitterwall_usertimelinesettings', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('include_rts', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('exclude_replies', self.gf('django.db.models.fields.BooleanField')(default=True)),
        )))
        db.send_create_signal('twitterwall', ['UserTimelineSettings'])

        # Adding M2M table for field sites on 'UserTimelineSettings'
        db.create_table('twitterwall_usertimelinesettings_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usertimelinesettings', models.ForeignKey(orm['twitterwall.usertimelinesettings'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('twitterwall_usertimelinesettings_sites', ['usertimelinesettings_id', 'site_id'])

        # Adding model 'TwitterUser'
        db.create_table('twitterwall_twitteruser', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('id_str', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('screen_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('profile_image_url', self.gf('base_libs.models.fields.URLField')(max_length=255)),
            ('url', self.gf('base_libs.models.fields.URLField')(max_length=255, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5, blank=True)),
        )))
        db.send_create_signal('twitterwall', ['TwitterUser'])

        # Adding model 'Tweet'
        db.create_table('twitterwall_tweet', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('id_str', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitterwall.TwitterUser'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('html', self.gf('django.db.models.fields.TextField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('from_search', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('by_user', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.CharField')(default='published', max_length=20, blank=True)),
        )))
        db.send_create_signal('twitterwall', ['Tweet'])

        # Adding M2M table for field sites on 'Tweet'
        db.create_table('twitterwall_tweet_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tweet', models.ForeignKey(orm['twitterwall.tweet'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('twitterwall_tweet_sites', ['tweet_id', 'site_id'])

        # Adding model 'TweetMedia'
        db.create_table('twitterwall_tweetmedia', south_cleaned_fields((
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tweet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['twitterwall.Tweet'])),
            ('media_url', self.gf('base_libs.models.fields.URLField')(max_length=200)),
            ('media_type', self.gf('django.db.models.fields.CharField')(default='photo', max_length=20)),
        )))
        db.send_create_signal('twitterwall', ['TweetMedia'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'SearchSettings'
        db.delete_table('twitterwall_searchsettings')

        # Removing M2M table for field sites on 'SearchSettings'
        db.delete_table('twitterwall_searchsettings_sites')

        # Deleting model 'UserTimelineSettings'
        db.delete_table('twitterwall_usertimelinesettings')

        # Removing M2M table for field sites on 'UserTimelineSettings'
        db.delete_table('twitterwall_usertimelinesettings_sites')

        # Deleting model 'TwitterUser'
        db.delete_table('twitterwall_twitteruser')

        # Deleting model 'Tweet'
        db.delete_table('twitterwall_tweet')

        # Removing M2M table for field sites on 'Tweet'
        db.delete_table('twitterwall_tweet_sites')

        # Deleting model 'TweetMedia'
        db.delete_table('twitterwall_tweetmedia')
    
    
    models = {
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'twitterwall.searchsettings': {
            'Meta': {'object_name': 'SearchSettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'})
        },
        'twitterwall.tweet': {
            'Meta': {'ordering': "('-creation_date',)", 'object_name': 'Tweet'},
            'by_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'from_search': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'html': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'id_str': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'published'", 'max_length': '20', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitterwall.TwitterUser']"})
        },
        'twitterwall.tweetmedia': {
            'Meta': {'ordering': "('id',)", 'object_name': 'TweetMedia'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media_type': ('django.db.models.fields.CharField', [], {'default': "'photo'", 'max_length': '20'}),
            'media_url': ('base_libs.models.fields.URLField', [], {'max_length': '200'}),
            'tweet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twitterwall.Tweet']"})
        },
        'twitterwall.twitteruser': {
            'Meta': {'ordering': "('screen_name',)", 'object_name': 'TwitterUser'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'id_str': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'profile_image_url': ('base_libs.models.fields.URLField', [], {'max_length': '255'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'url': ('base_libs.models.fields.URLField', [], {'max_length': '255', 'blank': 'True'})
        },
        'twitterwall.usertimelinesettings': {
            'Meta': {'object_name': 'UserTimelineSettings'},
            'exclude_replies': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_rts': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['twitterwall']
