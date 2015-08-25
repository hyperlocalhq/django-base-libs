# -*- coding: UTF-8 -*-
import re

from django import forms
from django.db import models
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _

import haystack
from haystack.backends import SQ
from haystack.forms import SearchForm as _SearchForm

def get_dictionaries( site=None ):
    if site is None:
        site = haystack.site

    models = {}
    indexes = {}
    for model, index in site.get_indexes().items():
        model = "%s.%s" % ( model._meta.app_label, model._meta.module_name )
        models[ model ] = index.short_name
        indexes[ index.short_name ] = model
    return models, indexes

def get_model_short_name( name ):
    short_model_names, indexes = get_dictionaries()
    return short_model_names[ name ]

def get_model_from_short_name( name ):
    short_model_names, indexes = get_dictionaries()
    return indexes[ name ]

def model_choices(site=None):
    if site is None:
        site = haystack.site
    
    models = sorted( [ ( m, k.verbose_name, k.order ) for m, k in site.get_indexes().items() ], key=lambda x: x[2] )
    return [ ("%s" % get_model_short_name( "%s.%s" % ( m[0]._meta.app_label, m[0]._meta.module_name ) ), 
              capfirst( unicode( m[1] ) ) ) for m in models ]

class ModelSearchForm( _SearchForm ):
    QUERY_PARAM_NAME='q'
    MODELS_PARAM_NAME='t'

    #selected_facets = forms.CharField( required=False, widget=forms.HiddenInput )

    def __init__( self, *args, **kwargs ):
        super( ModelSearchForm, self ).__init__( *args, **kwargs )
        self.fields[ self.MODELS_PARAM_NAME ] = forms.MultipleChoiceField(
            choices=model_choices(),
            required=False,
            label=_('Search In'),
            widget=forms.CheckboxSelectMultiple
            )

    def get_models(self):
        """Return list of model classes in the index."""
        search_models = []
        
        if self.is_valid():
            for model in self.cleaned_data[ self.MODELS_PARAM_NAME ]:
                model = get_model_from_short_name( model )
                search_models.append( models.get_model( *model.split( '.' ) ) )
        
        return search_models

    
    def search( self ):
        if not self.is_valid():
            return self.no_query_found()
        
        if not self.cleaned_data[ self.QUERY_PARAM_NAME ]:
            return self.no_query_found()

        self.clean()

        q = self.cleaned_data[ self.QUERY_PARAM_NAME ]
        models = self.get_models()
        
        # add models
        #sqs = self.searchqueryset.models( *models )
        from haystack.query import SearchQuerySet
        sqs = SearchQuerySet().models( *models )
        
        
        sqs = sqs.auto_query(sqs.query.clean(q))

        # add highlight
        sqs = sqs.highlight()
        
        # add faceting by django_ct
        sqs = sqs.facet( 'django_ct' )

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
