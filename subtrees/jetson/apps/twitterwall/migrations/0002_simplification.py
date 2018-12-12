# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields


class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Removing M2M table for field sites on 'SearchSettings'
        db.delete_table('twitterwall_searchsettings_sites')

        # Removing M2M table for field sites on 'Tweet'
        db.delete_table('twitterwall_tweet_sites')

        # Deleting field 'UserTimelineSettings.exclude_replies'
        db.delete_column('twitterwall_usertimelinesettings', 'exclude_replies')

        # Deleting field 'UserTimelineSettings.include_rts'
        db.delete_column('twitterwall_usertimelinesettings', 'include_rts')

        # Removing M2M table for field sites on 'UserTimelineSettings'
        db.delete_table('twitterwall_usertimelinesettings_sites')
    
    def backwards(self, orm):
        
        # Adding M2M table for field sites on 'SearchSettings'
        db.create_table('twitterwall_searchsettings_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('searchsettings', models.ForeignKey(orm['twitterwall.searchsettings'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('twitterwall_searchsettings_sites', ['searchsettings_id', 'site_id'])

        # Adding M2M table for field sites on 'Tweet'
        db.create_table('twitterwall_tweet_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tweet', models.ForeignKey(orm['twitterwall.tweet'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('twitterwall_tweet_sites', ['tweet_id', 'site_id'])

        # Adding field 'UserTimelineSettings.exclude_replies'
        db.add_column('twitterwall_usertimelinesettings', 'exclude_replies', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding field 'UserTimelineSettings.include_rts'
        db.add_column('twitterwall_usertimelinesettings', 'include_rts', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Adding M2M table for field sites on 'UserTimelineSettings'
        db.create_table('twitterwall_usertimelinesettings_sites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('usertimelinesettings', models.ForeignKey(orm['twitterwall.usertimelinesettings'], null=False)),
            ('site', models.ForeignKey(orm['sites.site'], null=False))
        ))
        db.create_unique('twitterwall_usertimelinesettings_sites', ['usertimelinesettings_id', 'site_id'])
    
    
    models = {
        'twitterwall.searchsettings': {
            'Meta': {'object_name': 'SearchSettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '140'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'screen_name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['twitterwall']
