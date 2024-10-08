# coding=utf-8
"""
overriding admin views for tree items
"""
from django.contrib.admin.templatetags.admin_list import result_headers, _boolean_icon
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.template import Library
from django.utils import dateformat
try:
    from django.utils.encoding import force_text
except:
    from django.utils.encoding import force_unicode as force_text
from django.utils.formats import get_format
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.utils.text import capfirst

register = Library()


def get_empty_value_display(cl):
    if hasattr(cl.model_admin, 'get_empty_value_display'):
        return cl.model_admin.get_empty_value_display()
    else:
        # Django < 1.9
        from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE
        return EMPTY_CHANGELIST_VALUE


def tree_items_for_result(cl, result):
    first = True
    pk = cl.lookup_opts.pk.attname
    for field_name in cl.list_display:
        row_class = ""
        try:
            f = cl.lookup_opts.get_field(field_name)
        except models.FieldDoesNotExist:
            # For non-field list_display values, the value is either a method,
            # property or returned via a callable.
            try:
                if callable(field_name):
                    attr = field_name
                    value = attr(result)
                elif (
                    hasattr(cl.model_admin, field_name)
                    and not field_name == "__str__"
                    and not field_name == "__unicode__"
                ):
                    attr = getattr(cl.model_admin, field_name)
                    value = attr(result)
                else:
                    attr = getattr(result, field_name)
                    if callable(attr):
                        value = attr()
                    else:
                        value = attr
                allow_tags = getattr(attr, "allow_tags", False)
                boolean = getattr(attr, "boolean", False)
                if boolean:
                    allow_tags = True
                    result_repr = _boolean_icon(value)
                else:
                    result_repr = force_text(value)
            except (AttributeError, ObjectDoesNotExist):
                result_repr = get_empty_value_display(cl)
            else:
                # Strip HTML tags in the resulting text, except if the
                # function has an "allow_tags" attribute set to True.
                if not allow_tags:
                    result_repr = escape(result_repr)
                else:
                    result_repr = mark_safe(result_repr)
        else:
            field_val = getattr(result, f.attname)

            if isinstance(f.rel, models.ManyToOneRel):
                if field_val is not None:
                    result_repr = escape(getattr(result, f.name))
                else:
                    result_repr = get_empty_value_display(cl)
            # Dates and times are special: They're formatted in a certain way.
            elif isinstance(f, models.DateField) or isinstance(f, models.TimeField):
                if field_val:
                    date_format = get_format("DATE_FORMAT")
                    datetime_format = get_format("DATETIME_FORMAT")
                    time_format = get_format("TIME_FORMAT")
                    if isinstance(f, models.DateTimeField):
                        result_repr = capfirst(
                            dateformat.format(field_val, datetime_format)
                        )
                    elif isinstance(f, models.TimeField):
                        result_repr = capfirst(
                            dateformat.time_format(field_val, time_format)
                        )
                    else:
                        result_repr = capfirst(
                            dateformat.format(field_val, date_format)
                        )
                else:
                    result_repr = get_empty_value_display(cl)
                row_class = ' class="nowrap"'
            # Booleans are special: We use images.
            elif isinstance(f, models.BooleanField) or isinstance(
                f, models.NullBooleanField
            ):
                result_repr = _boolean_icon(field_val)
            # DecimalFields are special: Zero-pad the decimals.
            elif isinstance(f, models.DecimalField):
                if field_val is not None:
                    result_repr = ("%%.%sf" % f.decimal_places) % field_val
                else:
                    result_repr = get_empty_value_display(cl)
            # Fields with choices are special: Use the representation
            # of the choice.
            elif f.choices:
                result_repr = dict(f.choices).get(field_val, get_empty_value_display(cl))
            else:
                result_repr = escape(field_val)
        if force_text(result_repr) == "":
            result_repr = mark_safe("&nbsp;")
        # If list_display_links not defined, add the link tag to the first field
        if (first and not cl.list_display_links) or field_name in cl.list_display_links:
            table_tag = {True: "th", False: "td"}[first]
            first = False
            url = cl.url_for_result(result)
            # Convert the pk to something that can be used in Javascript.
            # Problem cases are long ints (23L) and non-ASCII strings.
            if cl.to_field:
                attr = str(cl.to_field)
            else:
                attr = pk
            result_id = repr(force_text(getattr(result, attr)))[1:]
            if result.pk in cl.filtered_out:
                yield mark_safe(
                    u'<%s%s><span class="filtered_out">%s</span></%s>'
                    % (table_tag, row_class, conditional_escape(result_repr), table_tag)
                )
            else:
                yield mark_safe(
                    u'<%s%s><a href="%s"%s>%s</a></%s>'
                    % (
                        table_tag,
                        row_class,
                        url,
                        (
                            cl.is_popup
                            and ' onclick="opener.dismissRelatedLookupPopup(window, %s); return false;"'
                            % result_id
                            or ""
                        ),
                        conditional_escape(result_repr),
                        table_tag,
                    )
                )
        else:
            yield mark_safe(
                u"<td%s>%s</td>" % (row_class, conditional_escape(result_repr))
            )


def tree_results(cl):
    for res in cl.result_list:
        yield [res] + list(tree_items_for_result(cl, res))


def tree_result_list(cl):
    return {
        "cl": cl,
        "result_headers": list(result_headers(cl)),
        "results": list(tree_results(cl)),
    }


tree_result_list = register.inclusion_tag("admin/tree_change_list_results.html")(
    tree_result_list
)


def tree_admin_list_filter(cl, spec):
    # we use the unique contenttype to make ids for html-elements unique for the tree filter
    ct = ContentType.objects.get_for_model(spec.field.rel.to)
    return {"ct": ct, "title": spec.title(), "choices": list(spec.choices(cl))}


tree_admin_list_filter = register.inclusion_tag("admin/tree_filter.html")(
    tree_admin_list_filter
)
