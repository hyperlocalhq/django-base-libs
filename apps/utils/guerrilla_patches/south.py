# -*- coding: UTF-8 -*-

from django.utils import importlib
from django.contrib.contenttypes import generic

from south.creator.actions import AddModel
AddModel.FORWARDS_TEMPLATE = '''
        # Adding model '%(model_name)s'
        db.create_table(%(table_name)r, south_cleaned_fields((
            %(field_defs)s
        )))
        db.send_create_signal(%(app_label)r, [%(model_name)r])'''

from south.management.commands import schemamigration
schemamigration.MIGRATION_TEMPLATE = """# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        %(forwards)s
    
    
    def backwards(self, orm):
        %(backwards)s
    
    
    models = %(frozen_models)s
    south_clean_multilingual_fields(models)
    
    %(complete_apps)s
"""

from south.management.commands import datamigration
datamigration.MIGRATION_TEMPLATE = """# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from base_libs.utils.misc import south_clean_multilingual_fields
from base_libs.utils.misc import south_cleaned_fields

class Migration(DataMigration):
    
    def forwards(self, orm):
        "Write your forwards methods here."
    
    
    def backwards(self, orm):
        "Write your backwards methods here."
    
    models = %(frozen_models)s
    south_clean_multilingual_fields(models)
    
    %(complete_apps)s
"""
