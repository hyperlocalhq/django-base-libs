# -*- coding: UTF-8 -*-
import re

from django.db import models
from django.conf import settings
from django import template

from kb.apps.people.app_settings import PREFIX_CI, PREFIX_BC, PREFIX_OT
from kb.apps.marketplace.forms import PREFIX_JS

Term = models.get_model("structure", "Term")
ContextCategory = models.get_model("structure", "ContextCategory")

register = template.Library()


### TAGS ###

def do_get_latest_published_objects(parser, token):
    """
    Gets a queryset of all objects of the model specified by app and model names

    Usage:
        
        {% get_published_objects app.name <amount> as <var_name> %}
        
    Example:
        
        {% get_published_objects people.Person 3 as people %}
        
    """
    try:
        tag_name, appmodel, amount, str_as, var_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "get_published_objects tag requires a following syntax: {% get_published_objects app.model <amount> as <var_name> %}"
    try:
        appname, modelname = appmodel.split(".")
    except ValueError:
        raise template.TemplateSyntaxError, "get_published_objects tag requires application name and model name separated by a dot"
    model = models.get_model(appname, modelname)
    return LatestPublishedObjectsNode(model, amount, var_name)


class LatestPublishedObjectsNode(template.Node):
    def __init__(self, model, amount, var_name):
        self.model = model
        self.amount = amount
        self.var_name = var_name

    def render(self, context):
        sector_slug = getattr(settings, "CREATIVE_SECTOR", "")
        path_re = re.compile('^/creative-sector/(?P<slug>[^/]+)/$')
        m = re.match(path_re, context["request"].path)
        if m:
            sector_slug = m.groupdict()["slug"]

        if hasattr(self.model.objects, "latest_published"):
            qs = self.model.objects.latest_published()
        else:
            qs = self.model.objects.all()
        if sector_slug:
            qs = qs.filter(creative_sectors__slug=sector_slug)
        # if qs.model.__name__ == "Event":
        #    qs = qs.order_by("start")
        amount = template.resolve_variable(self.amount, context)
        context[self.var_name] = qs[:amount]
        return ''


register.tag('get_latest_published_objects_cs', do_get_latest_published_objects)


class CreativeSectorsNode(template.Node):
    def __init__(self, var_name, cs_cleaned_data_lookup_var):

        self.var_name = var_name
        self.cs_cleaned_data_lookup_var = cs_cleaned_data_lookup_var

    def render(self, context):

        # try to resolve vars
        cleaned = None
        if self.cs_cleaned_data_lookup_var:
            try:
                cleaned = template.resolve_variable(self.cs_cleaned_data_lookup_var, context)
            except template.VariableDoesNotExist:
                return ''

        selected_cs = {}
        for item in Term.objects.filter(
            vocabulary__sysname='categories_creativesectors',
        ):
            if cleaned.get(PREFIX_CI + str(item.id), False):
                # remove all the parents
                for ancestor in item.get_ancestors():
                    if ancestor.id in selected_cs:
                        del (selected_cs[ancestor.id])
                # add current
                selected_cs[item.id] = item

        context[self.var_name] = selected_cs.values()
        return ''


class JobSectorsNode(template.Node):
    def __init__(self, var_name, js_cleaned_data_lookup_var):

        self.var_name = var_name
        self.js_cleaned_data_lookup_var = js_cleaned_data_lookup_var

    def render(self, context):

        # try to resolve vars
        cleaned = None
        if self.js_cleaned_data_lookup_var:
            try:
                cleaned = template.resolve_variable(self.js_cleaned_data_lookup_var, context)
            except template.VariableDoesNotExist:
                return ''

        selected_js = {}
        JobSector = models.get_model("marketplace", "JobSector")

        for item in JobSector.objects.all():
            if cleaned.get(PREFIX_JS + str(item.id), False):
                selected_js[item.id] = item

        context[self.var_name] = selected_js.values()
        return ''


class ContextCategoriesNode(template.Node):
    def __init__(self, var_name, cc_cleaned_data_lookup_var):

        self.var_name = var_name
        self.cc_cleaned_data_lookup_var = cc_cleaned_data_lookup_var

    def render(self, context):

        # try to resolve vars
        cleaned = None
        if self.cc_cleaned_data_lookup_var:
            try:
                cleaned = template.resolve_variable(self.cc_cleaned_data_lookup_var, context)
            except template.VariableDoesNotExist:
                return ''

        selected_cc = {}
        for item in ContextCategory.objects.filter(is_applied4person=True):
            if cleaned.get(PREFIX_BC + str(item.id), False):
                # remove all the parents
                for ancestor in item.get_ancestors():
                    if ancestor.id in selected_cc:
                        del (selected_cc[ancestor.id])
                # add current
                selected_cc[item.id] = item

        context[self.var_name] = selected_cc.values()
        return ''


class InstitutionTypesNode(template.Node):
    def __init__(self, var_name, ot_cleaned_data_lookup_var):

        self.var_name = var_name
        self.ot_cleaned_data_lookup_var = ot_cleaned_data_lookup_var

    def render(self, context):

        # try to resolve vars
        cleaned = None
        if self.ot_cleaned_data_lookup_var:
            try:
                cleaned = template.resolve_variable(self.ot_cleaned_data_lookup_var, context)
            except template.VariableDoesNotExist:
                return ''

        selected_ot = {}
        InstitutionType = models.get_model("institutions", "InstitutionType")
        for item in InstitutionType.objects.all():
            if cleaned.get(PREFIX_OT + str(item.id), False):
                # remove all the parents
                for ancestor in item.get_ancestors():
                    if ancestor.id in selected_ot:
                        del (selected_ot[ancestor.id])
                # add current
                selected_ot[item.id] = item
        context[self.var_name] = selected_ot.values()
        return ''


class DoGetCreativeSectors:
    """
    Gets selected creative sectors from form data

    Syntax::

        {% get_creative_sectors [cleaned_form_data] as [varname] %}
        
    """

    def __init__(self):
        pass

    def __call__(self, parser, token):

        tokens = token.contents.split()
        """
        Now tokens is a list like this:
        0: 'get_creative_sectors',
        1: 'cleaned_form_data' 
        2: 'as'
        3: 'var_name'
        """
        if len(tokens) != 4:
            raise template.TemplateSyntaxError, "%r tag requires 3 arguments" % tokens[0]
        if tokens[2] != 'as':
            raise template.TemplateSyntaxError, "second argument in %r tag must be 'as'" % tokens[0]

        return CreativeSectorsNode(tokens[3], tokens[1])


class DoGetJobSectors:
    """
    Gets job sectors from form data

    Syntax::

        {% get_job_sectors [cleaned_form_data] as [varname] %}
        
    """

    def __init__(self):
        pass

    def __call__(self, parser, token):

        tokens = token.contents.split()
        """
        Now tokens is a list like this:
        0: 'get_creative_sectors_for_jobs',
        1: 'cleaned_form_data' 
        2: 'as'
        3: 'var_name'
        """
        if len(tokens) != 4:
            raise template.TemplateSyntaxError, "%r tag requires 3 arguments" % tokens[0]
        if tokens[2] != 'as':
            raise template.TemplateSyntaxError, "second argument in %r tag must be 'as'" % tokens[0]

        return JobSectorsNode(tokens[3], tokens[1])


class DoGetContextCategories:
    """
    Gets selected context categories from form data

    Syntax::

        {% get_context_categories [cleaned_form_data] as [varname] %}
        
    """

    def __init__(self):
        pass

    def __call__(self, parser, token):

        tokens = token.contents.split()
        """
        Now tokens is a list like this:
        0: 'get_context_categories',
        1: 'cleaned_form_data' 
        2: 'as'
        3: 'var_name'
        """
        if len(tokens) != 4:
            raise template.TemplateSyntaxError, "%r tag requires 3 arguments" % tokens[0]
        if tokens[2] != 'as':
            raise template.TemplateSyntaxError, "second argument in %r tag must be 'as'" % tokens[0]

        return ContextCategoriesNode(tokens[3], tokens[1])


class DoGetInstitutionTypes:
    """
    Gets selected object types from form data

    Syntax::

        {% get_institution_types [cleaned_form_data] as [varname] %}
        
    """

    def __init__(self):
        pass

    def __call__(self, parser, token):

        tokens = token.contents.split()
        """
        Now tokens is a list like this:
        0: 'get_institution_types',
        1: 'cleaned_form_data' 
        2: 'as'
        3: 'var_name'
        """
        if len(tokens) != 4:
            raise template.TemplateSyntaxError, "%r tag requires 3 arguments" % tokens[0]
        if tokens[2] != 'as':
            raise template.TemplateSyntaxError, "second argument in %r tag must be 'as'" % tokens[0]

        return InstitutionTypesNode(tokens[3], tokens[1])


register.tag('get_creative_sectors', DoGetCreativeSectors())
register.tag('get_job_sectors', DoGetJobSectors())
register.tag('get_context_categories', DoGetContextCategories())
register.tag('get_institution_types', DoGetInstitutionTypes())
