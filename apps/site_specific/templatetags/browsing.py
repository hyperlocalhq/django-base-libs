# -*- coding: UTF-8 -*-
from django.apps import apps
from django.template import loader
from django import template

from jetson.apps.structure.models import Term, ContextCategory
from kb.apps.site_specific.models import ContextItem

register = template.Library()

### HELPERS ###

def is_active_browsed_category(criterion, category, request):
    """
    Function checking whether the current category is selected in the path.
    """
    browsing_filters = request.httpstate.get("browsing_filters", {})
    selection = browsing_filters.get(criterion, {})
    # selection_path = getattr(selection, "path_search", "")
    selection_id = getattr(selection, "id", 0)
    is_in_path = False  # selection_path.startswith(category.path_search)
    is_child = category.parent_id == selection_id
    return (not criterion in browsing_filters and not category.parent_id) or is_in_path or is_child


def is_active_object_category(method, category, current_object):
    """
    Function checking whether the current category is selected for an object.
    """
    current_path = category.path_search
    selections = getattr(current_object, method)()
    if hasattr(selections, "__iter__") or hasattr(selections, "__getitem__"):
        for selection in selections:
            if selection.path_search.startswith(current_path):
                return True
    elif selections:
        if selections.path_search.startswith(current_path):
            return True
    return False


def context_categories_under(sysname, request, is_for_browsing=False, is_for_creating=False):
    browsing_filters = request.httpstate.get("browsing_filters", {})
    additional_joins = []
    additional_conditions = ["1"]
    if is_for_browsing:
        pass
        # if "creative-sector" in browsing_filters:
        #    selected = browsing_filters["creative-sector"]
        #    additional_joins.append('INNER JOIN system_contextitem_creative_sectors AS scci ON sc.id=scci.contextitem_id INNER JOIN structure_term AS st ON scci.term_id=st.id')
        #    additional_conditions.append('st.path_search LIKE "' + selected.path_search + '%%"')
        # if "location-type" in browsing_filters:
        #    selected = browsing_filters["location-type"]
        #    additional_joins.append('INNER JOIN structure_term AS st3 ON sc.location_type_id=st3.id')
        #    additional_conditions.append('st3.path_search LIKE "' + selected.path_search + '%%"')
    if sysname:
        filter_params = {'parent__sysname': sysname}
    else:
        filter_params = {'parent__isnull': True}
    # if is_for_creating:
    return ContextCategory.objects.filter(**filter_params)
    # else:
    #    return ContextCategory.objects.filter(**filter_params).extra(select={'item_count': 'SELECT COUNT(DISTINCT sc.id) FROM system_contextitem AS sc INNER JOIN system_contextitem_context_categories AS scbc ON sc.id=scbc.contextitem_id INNER JOIN structure_contextcategory AS sbc2 ON scbc.contextcategory_id=sbc2.id ' + ' '.join(additional_joins) + ' WHERE sbc2.path_search LIKE CONCAT(structure_contextcategory.path_search, "%%") AND ' + ' AND '.join(additional_conditions) + ' AND sc.status IN ("published", "published_commercial")'})


def creative_sectors_under(sysname, request, is_for_browsing=False, is_for_creating=False):
    browsing_filters = request.httpstate.get("browsing_filters", {})
    additional_joins = []
    additional_conditions = ["1"]
    if is_for_browsing:
        pass
        # if "context-category" in browsing_filters:
        #    selected = browsing_filters["context-category"]
        #    additional_joins.append('INNER JOIN system_contextitem_context_categories AS scbc ON sc.id=scbc.contextitem_id INNER JOIN structure_contextcategory AS sb ON scbc.contextcategory_id=sb.id')
        #    additional_conditions.append('sb.path_search LIKE "' + selected.path_search + '%%"')
        # if "location-type" in browsing_filters:
        #    selected = browsing_filters["location-type"]
        #    additional_joins.append('INNER JOIN structure_term AS st3 ON sc.location_type_id=st3.id')
        #    additional_conditions.append('st3.path_search LIKE "' + selected.path_search + '%%"')
    if sysname:
        filter_params = {'parent__sysname': sysname}
    else:
        filter_params = {'parent__isnull': True}
    # if is_for_creating:
    return Term.objects.filter(
        **dict(filter_params, vocabulary__sysname="categories_creativesectors")
    )
    # else:
    #    return Term.objects.filter(
    #        **dict(filter_params, vocabulary__sysname="categories_creativesectors")
    #        ).extra(select={'item_count': 'SELECT COUNT(DISTINCT sc.id) FROM system_contextitem AS sc INNER JOIN system_contextitem_creative_sectors AS scci ON sc.id=scci.contextitem_id INNER JOIN structure_term AS ci2 ON scci.term_id=ci2.id ' + ' '.join(additional_joins) + ' WHERE ci2.path_search LIKE CONCAT(structure_term.path_search, "%%") AND ' + ' AND '.join(additional_conditions) + ' AND sc.status IN ("published", "published_commercial")'})


def institution_types_under(sysname, request, is_for_browsing=False, is_for_creating=False):
    InstitutionType = apps.get_model("institutions", "InstitutionType")
    browsing_filters = request.httpstate.get("browsing_filters", {})
    additional_joins = []
    additional_conditions = ["1"]
    if is_for_browsing:
        pass
        # if "creative-sector" in browsing_filters:
        #    selected = browsing_filters["creative-sector"]
        #    additional_joins.append('INNER JOIN system_contextitem_creative_sectors AS scci ON sc.id=scci.contextitem_id INNER JOIN structure_term AS st ON scci.term_id=st.id')
        #    additional_conditions.append('st.path_search LIKE "' + selected.path_search + '%%"')
        # if "context-category" in browsing_filters:
        #    selected = browsing_filters["context-category"]
        #    additional_joins.append('INNER JOIN system_contextitem_context_categories AS scbc ON sc.id=scbc.contextitem_id INNER JOIN structure_contextcategory AS sb ON scbc.contextcategory_id=sb.id')
        #    additional_conditions.append('sb.path_search LIKE "' + selected.path_search + '%%"')
        # if "location-type" in browsing_filters:
        #    selected = browsing_filters["location-type"]
        #    additional_joins.append('INNER JOIN structure_term AS st3 ON sc.location_type_id=st3.id')
        #    additional_conditions.append('st3.path_search LIKE "' + selected.path_search + '%%"')
    if sysname:
        filter_params = {'parent__slug': sysname}
    else:
        filter_params = {'parent__isnull': True}
    # if is_for_creating:
    return InstitutionType.objects.filter(**filter_params)
    # else:
    #    return InstitutionType.objects.filter(**filter_params).extra(select={'item_count': 'SELECT COUNT(DISTINCT sc.id) FROM system_contextitem AS sc INNER JOIN system_contextitem_object_types AS scot ON sc.id=scot.contextitem_id INNER JOIN structure_term AS ot2 ON scot.term_id=ot2.id ' + ' '.join(additional_joins) + ' WHERE ot2.path_search LIKE CONCAT(structure_term.path_search, "%%") AND ' + ' AND '.join(additional_conditions) + ' AND sc.status IN ("published", "published_commercial")'})


def locality_type_under(sysname, request, is_for_browsing=False, is_for_creating=False):
    from jetson.apps.location.models import LocalityType
    browsing_filters = request.httpstate.get("browsing_filters", {})
    additional_joins = []
    additional_conditions = ["1"]
    if is_for_browsing:
        pass
        # if "context-category" in browsing_filters:
        #    selected = browsing_filters["context-category"]
        #    additional_joins.append('INNER JOIN system_contextitem_context_categories AS scbc ON sc.id=scbc.contextitem_id INNER JOIN structure_contextcategory AS sb ON scbc.contextcategory_id=sb.id')
        #    additional_conditions.append('sb.path_search LIKE "' + selected.path_search + '%%"')
        # if "creative-sector" in browsing_filters:
        #    selected = browsing_filters["creative-sector"]
        #    additional_joins.append('INNER JOIN system_contextitem_creative_sectors AS scci ON sc.id=scci.contextitem_id INNER JOIN structure_term AS st ON scci.term_id=st.id')
        #    additional_conditions.append('st.path_search LIKE "' + selected.path_search + '%%"')
    if sysname:
        filter_params = {'parent__slug': sysname}
    else:
        filter_params = {'parent__isnull': True}
    return LocalityType.objects.filter(**dict(filter_params))


### TAGS ###

def do_categories_under(parser, token):
    """
    This will output the categories under the one with the specified sysname.
    If the sysname is not specified, the top-level categories will be displayed.
    By default it uses the template site_specific/children.html, but optionally you can set some custom template.

    Usage::

        {% context_categories_under <sysname> [using <template_path>] [browsing|creating|selecting] %}
        {% creative_sectors_under <sysname> [using <template_path>] [browsing|creating|selecting] %}
        {% institution_types_under <sysname> [using <template_path>] [browsing|creating|selecting] %}
        {% locality_types_under <sysname> [using <template_path>] [browsing|creating|selecting] %}
    
    Examples::

        {% context_categories_under "" %}
        {% creative_sectors_under slug browsing %}
        {% institution_types_under "Institution" using "site_specific/children_of_institution.html" %}

    """
    bits = token.split_contents()
    try:
        tag_name = bits[0]
        sysname = bits[1]
        template_path = ""
        if "using" in bits:
            template_path = bits[3]
        is_for_browsing = "browsing" in bits
        is_for_creating = ("creating" in bits) or ("selecting" in bits)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a following syntax: {%% %r <sysname> [using <template_path>] [browsing] %%}" % \
                                            token.contents[0]
    return CategoriesUnder(tag_name, sysname, template_path, is_for_browsing, is_for_creating)


class CategoriesUnder(template.Node):
    def __init__(self, func_name, sysname, template_path, is_for_browsing=False, is_for_creating=False):
        self.func_name = func_name
        self.sysname = sysname
        self.template_path = template_path
        self.is_for_browsing = is_for_browsing
        self.is_for_creating = is_for_creating

    def render(self, context):
        sysname = None
        try:
            sysname = template.resolve_variable(self.sysname, context)
        except Exception:
            pass
        show_4_current_object = False
        current_object = None
        try:
            current_object = template.resolve_variable("object", context)
        except Exception:
            pass
        else:
            if is_context_item(current_object):
                show_4_current_object = True

        categories = eval(self.func_name)(
            sysname,
            context['request'],
            self.is_for_browsing and not show_4_current_object,
            self.is_for_creating,
        )
        if show_4_current_object:
            funcname2methodname = {
                "context_categories_under": "get_context_categories",
                "creative_sectors_under": "get_creative_sectors",
                "institution_types_under": "get_object_types",
                "locality_type_under": "get_locality_type",
            }
            categories = [cat for cat in categories
                          if self.is_for_creating or (cat.item_count and is_active_object_category(
                    funcname2methodname[self.func_name],
                    cat,
                    current_object,
                ))]
        elif self.is_for_browsing:
            funcname2criterion = {
                "context_categories_under": "context-category",
                "creative_sectors_under": "creative-sector",
                "institution_types_under": "object-type",
                "locality_type_under": "location-type",
            }
            categories = [cat for cat in categories
                          if cat.item_count and is_active_browsed_category(
                    funcname2criterion[self.func_name],
                    cat,
                    context["request"],
                )]
        try:
            template_path = template.resolve_variable(self.template_path, context)
        except Exception:
            template_path = ""
        context_vars = context
        context_vars.push()
        context_vars['categories'] = categories
        output = loader.render_to_string(template_path or "site_specific/categories.html", context_vars)
        context_vars.pop()
        return output


register.tag('context_categories_under', do_categories_under)
register.tag('creative_sectors_under', do_categories_under)
register.tag('institution_types_under', do_categories_under)
register.tag('locality_type_under', do_categories_under)

### FILTERS ###

def is_context_item(instance):
    return type(instance).__name__ in ("Person", "Institution", "Document", "Event", "PersonGroup", "ContextItem")


def get_context_item(instance):
    return ContextItem.objects.get_for(instance)


register.filter('is_context_item', is_context_item)
register.filter('get_context_item', get_context_item)
