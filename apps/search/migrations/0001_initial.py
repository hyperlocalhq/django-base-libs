
from south.db import db
from django.db import models
from ccb.apps.search.models import *
from base_libs.utils.misc import south_clean_multilingual_fields

class Migration:
    
    def forwards(self, orm):
        "Write your forwards migration here"
    
    
    def backwards(self, orm):
        "Write your backwards migration here"
    
    
    models = {
        
    }
    south_clean_multilingual_fields(models)
    
    complete_apps = ['search']
