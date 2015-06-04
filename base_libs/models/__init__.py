from base_libs.models.models import *
from base_libs.models.admin import *
from base_libs.models.query import *
from base_libs.models.fields import *

"""
add templatetag path to base_libs folder here. As base is not 
part of apps (and is not added to the templatetags path 
by the initialization of django, we have to do that manually.
"""
from django.templatetags import __path__
__path__.extend(__import__('base_libs.templatetags', {}, {}, ['']).__path__)