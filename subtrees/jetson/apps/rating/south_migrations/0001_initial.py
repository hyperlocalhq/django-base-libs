
from south.db import db
from django.db import models
from jetson.apps.rating.models import *
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'UserRating'
        db.create_table('rating_userrating', south_cleaned_fields((
            ('id', models.AutoField(primary_key=True)),
            ('creation_date', models.DateTimeField(_("creation date"), editable=False)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'], related_name=None, null=True, blank=True)),
            ('object_id', models.CharField(u'Related object', max_length=255, null=False, blank=True)),
            ('user', models.ForeignKey(orm['auth.User'], related_name="rating_userrating_user")),
            ('key', models.CharField(_('key'), default='RATING', max_length=32)),
            ('score', models.IntegerField()),
            ('is_aggregated', models.BooleanField(_('is aggregated'), default=False)),
        )))
        db.send_create_signal('rating', ['UserRating'])
        
        # Creating unique_together for [content_type, object_id, user, key] on UserRating.
        db.create_unique('rating_userrating', ['content_type_id', 'object_id', 'user_id', 'key'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'UserRating'
        db.delete_table('rating_userrating')
        
        # Deleting unique_together for [content_type, object_id, user, key] on UserRating.
        db.delete_unique('rating_userrating', ['content_type_id', 'object_id', 'user_id', 'key'])
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'rating.userrating': {
            'Meta': {'unique_together': "(('content_type','object_id','user','key'))"},
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {'related_name': 'None', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('models.DateTimeField', ['_("creation date")'], {'editable': 'False'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_aggregated': ('models.BooleanField', ["_('is aggregated')"], {'default': 'False'}),
            'key': ('models.CharField', ["_('key')"], {'default': "'RATING'", 'max_length': '32'}),
            'object_id': ('models.CharField', ["u'Related object'"], {'max_length': '255', 'null': 'False', 'blank': 'True'}),
            'score': ('models.IntegerField', [], {}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {'related_name': '"rating_userrating_user"'})
        }
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['rating']
