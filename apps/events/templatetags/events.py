# -*- coding: UTF-8 -*-
import math
from datetime import datetime, timedelta

from django import template
from django.utils import dateformat
from django.utils.formats import get_format
from django.db import models

DATE_FORMAT = get_format('DATE_FORMAT')
DATETIME_FORMAT = get_format('DATETIME_FORMAT')
TIME_FORMAT = get_format('TIME_FORMAT')
MONTH_DAY_FORMAT = get_format('MONTH_DAY_FORMAT')
YEAR_MONTH_FORMAT = get_format('YEAR_MONTH_FORMAT')

Institution = models.get_model("institutions", "Institution")

register = template.Library()

### TAGS ###

class DatePeriodNode(template.Node):
    def __init__(
        self, var_name, start_yyyy_lookup_var,
        start_mm_lookup_var, start_dd_lookup_var,
        end_yyyy_lookup_var=None, end_mm_lookup_var=None,
        end_dd_lookup_var=None
    ):

        self.var_name = var_name
        self.start_yyyy_lookup_var = start_yyyy_lookup_var
        self.start_mm_lookup_var = start_mm_lookup_var
        self.start_dd_lookup_var = start_dd_lookup_var
        self.end_yyyy_lookup_var = end_yyyy_lookup_var
        self.end_mm_lookup_var = end_mm_lookup_var
        self.end_dd_lookup_var = end_dd_lookup_var

    def _get_start_date_formatted(self):

        start_date_format = DATE_FORMAT

        if self.start_dd and self.start_mm and self.start_yyyy:
            start_date_format = DATE_FORMAT
        elif self.start_dd and self.start_mm:
            start_date_format = MONTH_DAY_FORMAT
        elif self.start_mm and self.start_yyyy:
            start_date_format = YEAR_MONTH_FORMAT
        elif self.start_yyyy:
            start_date_format = "Y"

        if self.start_yyyy and self.end_yyyy == self.start_yyyy:
            start_date_format = "Y"
            if self.start_mm:
                start_date_format = "F"
                if self.start_dd:
                    start_date_format = MONTH_DAY_FORMAT

            if self.start_mm and self.end_mm == self.start_mm:
                start_date_format = YEAR_MONTH_FORMAT
                if self.start_dd and self.end_dd == self.start_dd:
                    start_date_format = DATE_FORMAT
                elif self.start_dd and self.end_dd != self.start_dd:
                    start_date_format = "j."

        start_date = datetime(
            int(self.start_yyyy or datetime.now().year),
            int(self.start_mm or 1),
            int(self.start_dd or 1),
        )

        return dateformat.format(start_date, start_date_format)

    def _get_end_date_formatted(self):

        end_date_format = None
        if self.end_dd and self.end_mm and self.end_yyyy:
            end_date_format = DATE_FORMAT
        elif self.end_dd and self.end_mm:
            end_date_format = MONTH_DAY_FORMAT
        elif self.end_mm and self.end_yyyy:
            end_date_format = YEAR_MONTH_FORMAT
        elif self.end_yyyy:
            start_date_format = "Y"
        else:
            return None

        try:
            end_date = datetime(
                int(self.end_yyyy or datetime.now().year),
                int(self.end_mm or 1),
                int(self.end_dd or 1),
            )
        except Exception:
            end_date = None

        return dateformat.format(end_date, end_date_format)

    def render(self, context):
        # from django.conf import settings

        # try to resolve vars
        if self.start_yyyy_lookup_var:
            try:
                self.start_yyyy = template.resolve_variable(self.start_yyyy_lookup_var, context)
            except template.VariableDoesNotExist:
                return ''

        if self.start_mm_lookup_var:
            try:
                self.start_mm = template.resolve_variable(self.start_mm_lookup_var, context)
            except template.VariableDoesNotExist:
                return ''

        if self.start_dd_lookup_var:
            try:
                self.start_dd = template.resolve_variable(self.start_dd_lookup_var, context)
            except template.VariableDoesNotExist:
                return ''

        if self.end_yyyy_lookup_var:
            try:
                self.end_yyyy = template.resolve_variable(self.end_yyyy_lookup_var, context)
            except template.VariableDoesNotExist:
                return ''

        if self.end_mm_lookup_var:
            try:
                self.end_mm = template.resolve_variable(self.end_mm_lookup_var, context)
            except template.VariableDoesNotExist:
                return ''

        if self.end_dd_lookup_var:
            try:
                self.end_dd = template.resolve_variable(self.end_dd_lookup_var, context)
            except template.VariableDoesNotExist:
                return ''

        start_date_formatted = self._get_start_date_formatted()
        end_date_formatted = self._get_end_date_formatted()

        context[self.var_name] = start_date_formatted
        if end_date_formatted and end_date_formatted != start_date_formatted:
            context[self.var_name] += "-" + end_date_formatted

        return ''


class InstitutionNode(template.Node):
    def __init__(self, var_name, institution_id_lookup_var):

        self.var_name = var_name
        self.institution_id_lookup_var = institution_id_lookup_var

    def render(self, context):

        # try to resolve vars
        if self.institution_id_lookup_var:
            try:
                self.institution_id = template.resolve_variable(self.institution_id_lookup_var, context)
            except template.VariableDoesNotExist:
                return ''
        institution = Institution.objects.get(id=self.institution_id)
        context[self.var_name] = institution
        return ''


class DoGetDatePeriodFormatted:
    """
    Formats date periods nicely

    Syntax::

        {% get_date_period_formatted from [start_yyy] [start_mm] [start_dd] (to [end_yyyy] [end_mm] [end_dd]) as [varname] %}
        
        end_date is optional

    Example usage::

        {% get_date_period_formatted start_date end_date as event_dates %}
    """

    def __init__(self):
        pass

    def __call__(self, parser, token):

        tokens = token.contents.split()
        """
        Now tokens is a list like this:
        0 :'get_event_dates_formatted',
        1: 'from' 
        2: 'start_yyyy', 
        3: 'start_mm',
        4: 'start_dd',
        5: 'to',
        6: 'end_yyyy', 
        7: 'end_mm',
        8: 'end_dd',
        9: 'as'
        10:'var_name'
        """
        if not len(tokens) in (11, 7):
            raise template.TemplateSyntaxError, "%r tag requires 6 or 10 arguments" % tokens[0]
        if tokens[1] != 'from':
            raise template.TemplateSyntaxError, "first argument in %r tag must be 'from'" % tokens[0]

        if len(tokens) == 7:
            if tokens[6] != 'as':
                raise template.TemplateSyntaxError, "sixth argument in %r tag must be 'as'" % tokens[0]
            else:
                return DatePeriodNode(tokens[6], tokens[3], tokens[4])

        if len(tokens) == 11:
            if tokens[9] != 'as':
                raise template.TemplateSyntaxError, "10th argument in %r tag must be 'as'" % tokens[0]
            elif tokens[5] != 'to':
                raise template.TemplateSyntaxError, "fifth argument in %r tag must be 'to'" % tokens[0]
            else:
                return DatePeriodNode(
                    tokens[10], tokens[2], tokens[3],
                    tokens[4], tokens[6], tokens[7], tokens[8]
                )


class DoGetInstitution:
    """
    Gets data from an institution

    Syntax::

        {% get_institution_data [institution_id] as [varname] %}
        
    """

    def __init__(self):
        pass

    def __call__(self, parser, token):

        tokens = token.contents.split()
        """
        Now tokens is a list like this:
        0 :'get_institution_data',
        1: 'institution_id' 
        2: 'as'
        3:'var_name'
        """
        if len(tokens) != 4:
            raise template.TemplateSyntaxError, "%r tag requires 3 arguments" % tokens[0]
        if tokens[2] != 'as':
            raise template.TemplateSyntaxError, "second argument in %r tag must be 'as'" % tokens[0]

        return InstitutionNode(tokens[3], tokens[1])


register.tag('get_date_period_formatted', DoGetDatePeriodFormatted())
register.tag('get_institution', DoGetInstitution())


### FILTERS ###

def to_currency(value, arg=None):
    """
    formats a currency value nicely.

    arg:
      Currency Symbol
    """
    int_amount = math.floor(value)
    dec_amount = math.floor((value - int_amount) * 100)

    if dec_amount == 0.0:
        return "%d %s" % (int(int_amount), arg or "€")
    else:
        return "%d,%d %s" % (int(int_amount), int(dec_amount), arg or "€")


to_currency = register.filter(to_currency)


def add_days(value, days):
    """
    adds an amount of days to a given datetime object and returns the result
    """
    return value + timedelta(days=days)


add_days = register.filter(add_days)
