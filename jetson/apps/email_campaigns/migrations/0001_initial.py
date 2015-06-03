# -*- coding: UTF-8 -*-

from south.db import db
from django.db import models
from jetson.apps.email_campaigns.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'InfoSubscription'
        db.create_table('email_campaigns_infosubscription', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('site', models.ForeignKey(orm['sites.Site'], null=True, blank=True)),
            ('subscriber', models.ForeignKey(orm['auth.User'], null=True, blank=True)),
            ('subscriber_name', models.CharField(_("Subscriber's name"), max_length=200)),
            ('email', models.EmailField(_("Email address"))),
            ('ip', models.IPAddressField(_("IP Address"))),
            ('timestamp', models.DateTimeField(_("Timestamp"), auto_now_add=True)),
        )))
        db.send_create_signal('email_campaigns', ['InfoSubscription'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'InfoSubscription'
        db.delete_table('email_campaigns_infosubscription')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'db_table': "'django_site'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'email_campaigns.infosubscription': {
            'Meta': {'ordering': "['email']"},
            'email': ('models.EmailField', ['_("Email address")'], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'ip': ('models.IPAddressField', ['_("IP Address")'], {}),
            'site': ('models.ForeignKey', ["orm['sites.Site']"], {'null': 'True', 'blank': 'True'}),
            'subscriber': ('models.ForeignKey', ["orm['auth.User']"], {'null': 'True', 'blank': 'True'}),
            'subscriber_name': ('models.CharField', ['_("Subscriber\'s name")'], {'max_length': '200'}),
            'timestamp': ('models.DateTimeField', ['_("Timestamp")'], {'auto_now_add': 'True'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['email_campaigns']
