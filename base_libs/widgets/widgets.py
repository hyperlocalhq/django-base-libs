from copy import deepcopy
from itertools import chain
from json import JSONEncoder

from babel.dates import format_date, format_time, parse_date, parse_time

from django import forms
from django.conf import settings
from django.contrib.admin import widgets as admin_widgets
from django.forms.utils import flatatt
from django.forms.widgets import Widget
from django.utils.encoding import force_str
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe

from base_libs.middleware.threadlocals import get_current_language
from base_libs.utils.misc import XChoiceList
from base_libs.utils.misc import get_installed


ADMIN_MEDIA_URL = getattr(settings, "JETSON_MEDIA_URL", settings.ADMIN_MEDIA_PREFIX, )


class IntegerWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        from babel.numbers import parse_number
        from babel.numbers import format_number
        from babel.numbers import NumberFormatError

        locale = get_current_language()
        if value is None:
            value = ""
        if value and isinstance(value, str):
            try:
                value = parse_number(value, locale=locale)
            except NumberFormatError:
                pass
        if not isinstance(value, str):
            value = format_number(value, locale=locale)
        return super(IntegerWidget, self).render(name, value, attrs)


class DecimalWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        from babel.numbers import parse_decimal
        from babel.numbers import format_decimal
        from babel.numbers import NumberFormatError

        locale = get_current_language()
        if value is None:
            value = ""
        if value and isinstance(value, str):
            try:
                value = parse_decimal(value, locale=locale)
            except NumberFormatError:
                pass
        if not isinstance(value, str):
            value = format_decimal(value, self.format, locale=locale)
        return super(DecimalWidget, self).render(name, value, attrs)


class DateWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        locale = get_current_language()
        if value is None:
            value = ""
        if value and isinstance(value, str):
            try:
                value = parse_date(value, locale=locale)
            except:
                pass
        if not isinstance(value, str):
            value = format_date(value, locale=locale)
        return super(DateWidget, self).render(name, value, attrs)


class TimeWidget(forms.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        locale = get_current_language()
        if value is None:
            value = ""
        if value and isinstance(value, str):
            try:
                value = parse_time(value, locale=locale)
            except:
                pass
        if not isinstance(value, str):
            value = format_time(value, locale=locale)
        return super(TimeWidget, self).render(name, value, attrs)


class AutocompleteWidget(Widget):
    """ widget for forms autocomplete field """

    options = None
    js_template = """
        if (self.AutocompleteManager) {
            self.AutocompleteManager.register("#%s", %s, %s);
        }"""

    def __init__(
            self,
            app,
            qs_function,
            display_attr,
            add_display_attr=None,
            options=None,
            attrs=None,
    ):
        super(AutocompleteWidget, self).__init__()
        if not attrs:
            attrs = {}
        if not options:
            options = {}
        self.app = app
        self.qs_function = qs_function
        self.display_attr = display_attr
        self.add_display_attr = add_display_attr

        self.options = options

        self.attrs = attrs

    def render_js(self, hidden_field_id, field_id, text_field_value):
        source = "'/helper/autocomplete/%s/%s/%s/%s/'" % (
            self.app,
            self.qs_function,
            self.display_attr,
            self.add_display_attr,
        )

        if self.options:
            options = JSONEncoder().encode(self.options)

            # apply the required functions at the end of options! (without "")!!!!
            # TODO maybe there is a more elegant way!

            options = "%(options)s, %(events)s}" % {
                "options": options[:-1],
                "events": """
                    'formatItem': self.AutocompleteManager.formatItem
                """,
            }
        else:
            options = """{
                'formatItem': self.AutocompleteManager.formatItem
            }"""

        # $j("#%s").autocomplete(%s,%s).result(AutocompleteManager.result).next().click(function(){$j(this).prev().search();});""" % (
        js = self.js_template % (field_id, source, options)

        return js

    def render(self, name, value=None, attrs=None, renderer=None):
        """
        The widget consists of two text fields:
        1. Field with id = "id_<field_name>_text", which holds the text values
        2. Field with id = "id_<field_name>", which is hidden and holds the pk
            of a selected item.
        """
        if attrs is None:
            attrs = {}
        attrs["name"] = name + "_text"
        text_field_attrs = self.build_attrs(attrs)

        # if there is any initial value available, fill the text field from the queryset
        text_field_value = ""
        if value:
            func = get_installed(
                "%(app)s.ajax.%(func)s" % {"app": self.app, "func": self.qs_function, }
            )
            queryset = func("all")
            try:
                obj = queryset.get(pk=value)
                text_field_value = getattr(obj, self.display_attr)
                if callable(text_field_value) and not getattr(
                        text_field_value, "alters_data", False
                ):
                    text_field_value = text_field_value()
            except:
                pass

        text_field_attrs["value"] = text_field_value
        text_field_attrs["class"] = "autocomplete textinput textInput form-control"

        if "id" not in self.attrs:
            text_field_attrs["id"] = "id_%s_text" % name

        # hidden field for key value
        hidden_field_attrs = {
            "id": "id_%s" % name,
            "name": "%s" % name,
            "value": value or "",
            "class": "form_hidden",
        }

        return mark_safe(
            """
            <input type="text" %(text_field_attrs)s/>
            <input type="hidden" %(hidden_field_attrs)s />
            <script type="text/javascript">
            /* <![CDATA[ */
            %(js)s
            /* ]]> */
            </script>"""
            % {
                "text_field_attrs": flatatt(text_field_attrs),
                "js": self.render_js(
                    hidden_field_attrs["id"], text_field_attrs["id"], text_field_value,
                ),
                "hidden_field_attrs": flatatt(hidden_field_attrs),
            }
        )


class AutocompleteMultipleWidget(AutocompleteWidget):
    js_template = """
        if (self.AutocompleteMultipleManager) {
            self.AutocompleteMultipleManager.register("#%s", %s, %s);
        }"""

    def render(self, name, value=None, attrs=None, renderer=None):
        """
        The widget consists of two text fields:
        1. Field with id = "id_<field_name>_text", which is used for entering text values
        2. Field with id = "id_<field_name>", which is hidden and holds
            comma-separated pks of selected items
        3. List of selected text values with id = "id_<field_name>_value_pk-<pk>"
        """
        attrs["name"] = name + "_text"
        text_field_attrs = self.build_attrs(attrs)

        value = value or []

        # if there is any initial value available, fill the text field from the queryset
        value_list = []
        if value:
            func = get_installed(
                "%(app)s.ajax.%(func)s" % {"app": self.app, "func": self.qs_function, }
            )
            queryset = func("all")
            for obj in queryset.filter(pk__in=value):
                text_value = getattr(obj, self.display_attr)
                if callable(text_value) and not getattr(
                        text_value, "alters_data", False
                ):
                    text_value = text_value()
                    value_list.append(
                        """<li id="id_%(name)s_value_pk-%(pk)s">
                        <span>%(text_value)s</span>
                        </li>"""
                        % {
                            "name": name,
                            "pk": obj.pk,
                            "text_value": force_str(text_value),
                        }
                    )

        html_value_list = ""
        if value_list:
            html_value_list = """<ul id="id_%(name)s_value_list" class="ac_value_list">
            %(value_list)s
            </ul>""" % {
                "name": name,
                "value_list": "".join(value_list),
            }

        text_field_attrs["value"] = ""
        text_field_attrs["class"] = "autocomplete textinput textInput"

        if "id" not in self.attrs:
            text_field_attrs["id"] = "id_%s_text" % name

        # hidden field for key value
        hidden_field_attrs = {
            "id": "id_%s" % name,
            "name": "%s" % name,
            "value": ",".join([force_str(pk) for pk in value]),
            "class": "form_hidden",
        }

        return mark_safe(
            """
            <input type="hidden" %(hidden_field_attrs)s />
            %(html_value_list)s
            <input type="text" %(text_field_attrs)s/>
            <script type="text/javascript">
            /* <![CDATA[ */
            %(js)s
            /* ]]> */
            </script>"""
            % {
                "text_field_attrs": flatatt(text_field_attrs),
                "js": self.render_js(
                    hidden_field_attrs["id"], text_field_attrs["id"], "",
                ),
                "hidden_field_attrs": flatatt(hidden_field_attrs),
                "html_value_list": html_value_list,
            }
        )


class SelectToAutocompleteWidget(AutocompleteWidget):
    def __init__(
            self,
            app,
            qs_function,
            display_attr,
            add_display_attr=None,
            options=None,
            attrs=None,
    ):
        super(SelectToAutocompleteWidget, self).__init__(app, qs_function, display_attr)
        if not attrs:
            attrs = {}
        if not options:
            options = {}
        self.app = app
        self.qs_function = qs_function
        self.display_attr = display_attr
        self.add_display_attr = add_display_attr

        self.options = options

        self.attrs = attrs
        self.func = get_installed(
            "%(app)s.ajax.%(func)s" % {"app": self.app, "func": self.qs_function, }
        )
        self.queryset = self.func("all")
        # self.choices = list(XChoiceList(self.queryset))
        self.choices = XChoiceList(self.queryset)

    def render_js(self, select_field_id, field_id, text_field_value):
        source = "'/helper/autocomplete/%s/%s/%s/%s/'" % (
            self.app,
            self.qs_function,
            self.display_attr,
            self.add_display_attr,
        )

        options = JSONEncoder().encode(self.options)

        # apply the required functions at the end of options! (without "")!!!!
        # TODO maybe there is a more elegant way!

        options = "%(options)s, %(events)s}" % {
            "options": options[:-1],
            "events": """
                'formatItem': AutocompleteManager.formatItem
            """,
        }

        # $j("#%s").autocomplete(%s,%s).result(AutocompleteManager.result).next().click(function(){$j(this).prev().search();});""" % (
        js = """
        if (window.$j && window.AutocompleteManager) {
            $j("#%s")[0].lastSelected = %s;
            $j("#%s").autocomplete(%s,%s).result(AutocompleteManager.result).search();
        }""" % (
            field_id,
            JSONEncoder().encode(text_field_value),
            field_id,
            source,
            options,
        )

        return js

    def render(self, name, value=None, attrs=None, renderer=None, choices=()):
        """
        The widget consists of two text fields:
        1. Field with id = "id_<field_name>_text", which holds the text values
        2. Field with id = "id_<field_name>", which is hidden and holds the id
            of a selected item.
        """
        if value is None:
            value = ""
        attrs.setdefault("class", "")
        text_field_attrs = deepcopy(attrs)
        select_field_attrs = deepcopy(attrs)

        select_field_attrs["class"] = (select_field_attrs["class"] + " to_hide").strip()
        select_field_attrs["name"] = name
        final_attrs = self.build_attrs(select_field_attrs)
        output = ["<select%s>" % flatatt(final_attrs)]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append("</select>")
        select_field = "\n".join(output)

        text_field_attrs["class"] = (
                text_field_attrs["class"] + " to_show autocomplete"
        ).strip()
        text_field_attrs["name"] = name + "_text"
        text_field_attrs = self.build_attrs(text_field_attrs)

        # if there is any initial value available, fill the text field from the queryset
        text_field_value = ""

        if value:
            try:
                obj = self.queryset.get(pk=value)
                text_field_value = getattr(obj, self.display_attr)
                if callable(text_field_value):
                    text_field_value = text_field_value()
            except:
                pass

        text_field_attrs["value"] = text_field_value

        if "id" not in self.attrs:
            text_field_attrs["id"] = "id_%s_text" % name

        return mark_safe(
            """
            %(select_field)s
            <input type="text" %(text_field_attrs)s/>
            <script type="text/javascript">
            /* <![CDATA[ */
            %(js)s
            /* ]]> */
            </script>"""
            % {
                "select_field": select_field,
                "text_field_attrs": flatatt(text_field_attrs),
                "js": self.render_js(
                    select_field_attrs["id"], text_field_attrs["id"], text_field_value,
                ),
            }
        )

    def render_options(self, choices, selected_choices):
        def render_option(option_value, option_label):
            option_value = force_str(option_value)
            selected_html = (
                    (option_value in selected_choices) and ' selected="selected"' or ""
            )
            return '<option value="%s"%s>%s</option>' % (
                escape(option_value),
                selected_html,
                conditional_escape(force_str(option_label)),
            )

        # Normalize to strings.
        selected_choices = set([force_str(v) for v in selected_choices])
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(
                    '<optgroup label="%s">' % escape(force_str(option_value))
                )
                for option in option_label:
                    output.append(render_option(*option))
                output.append("</optgroup>")
            else:
                output.append(render_option(option_value, option_label))
        return "\n".join(output)


class ObjectSelect(forms.Widget):
    """ widget for selecting objects for use in generic relations """

    def __init__(self, attrs=None, choices=()):
        super(ObjectSelect, self).__init__(attrs)
        # choices can be any iterable, but we may need to render this widget
        # multiple times. Thus, collapse it into a list so it can be consumed
        # more than once.
        self.choices = list(choices)

    def render(self, name, value, attrs=None, renderer=None, choices=()):
        if value is None:
            value = ""
        if not isinstance(value, str):
            from base_libs.forms import fields

            value = fields.ObjectChoiceField.returnKey(value)
        attrs["name"] = name
        final_attrs = self.build_attrs(attrs)
        output = ["<select%s>" % flatatt(final_attrs)]
        if getattr(self, "default_text", False):
            output.append('<option value="">%s</option>' % self.default_text)
        str_value = force_str(value)  # Normalize to string.
        for group_name, obj_choices in self.choices:
            output.append('<optgroup label="%s">' % group_name)
            for option_value, option_label in obj_choices:
                option_value = force_str(option_value)
                selected_html = (
                        (option_value == str_value) and ' selected="selected"' or ""
                )
                output.append(
                    '<option value="%s"%s>%s</option>'
                    % (
                        escape(option_value),
                        selected_html,
                        escape(force_str(option_label)),
                    )
                )
            output.append("</optgroup>")
        output.append("</select>")
        return mark_safe("\n".join(output))


class TreeSelectWidget(forms.Select):
    """
    Widget to select from tree structures
    """

    def __init__(self, model, attrs=None, choices=()):
        if not attrs:
            attrs = {}
        self.model = model
        super(TreeSelectWidget, self).__init__(attrs, choices)

    def render_options(self, choices, selected_choices):
        def render_option(option_value, option_label):
            option_value = force_str(option_value)
            try:
                indentation = self.model._default_manager.get(
                    pk=option_value,
                ).get_level()
            except:
                indentation = 0

            selected_html = (
                    (option_value in selected_choices) and ' selected="selected"' or ""
            )
            return '<option value="%s"%s>%s</option>' % (
                escape(option_value),
                selected_html,
                ("-" * indentation)
                + " "
                + conditional_escape(force_str(option_label)),
            )

        # Normalize to strings.
        selected_choices = set([force_str(v) for v in selected_choices])
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(
                    '<optgroup label="%s">' % escape(force_str(option_value))
                )
                for option in option_label:
                    output.append(render_option(*option))
                output.append("</optgroup>")
            else:
                output.append(render_option(option_value, option_label))
        return "\n".join(output)


class TreeSelectMultipleWidget(forms.SelectMultiple):
    """
    Widget to select from tree structures
    """

    def __init__(self, model, attrs=None, choices=()):
        if not attrs:
            attrs = {}
        self.model = model
        super(TreeSelectMultipleWidget, self).__init__(attrs, choices)

    def render_options(self, choices, selected_choices):
        def render_option(option_value, option_label):
            option_value = force_str(option_value)
            try:
                indentation = self.model._default_manager.get(
                    pk=option_value,
                ).get_level()
            except:
                indentation = 0

            selected_html = (
                    (option_value in selected_choices) and ' selected="selected"' or ""
            )
            return '<option value="%s"%s>%s</option>' % (
                escape(option_value),
                selected_html,
                ("-" * indentation)
                + " "
                + conditional_escape(force_str(option_label)),
            )

        # Normalize to strings.
        selected_choices = set([force_str(v) for v in selected_choices])
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(
                    '<optgroup label="%s">' % escape(force_str(option_value))
                )
                for option in option_label:
                    output.append(render_option(*option))
                output.append("</optgroup>")
            else:
                output.append(render_option(option_value, option_label))
        return "\n".join(output)


class URLWidget(admin_widgets.AdminURLFieldWidget):
    class Media:
        extend = True
        js = ("%sjs/admin/URLField.js" % ADMIN_MEDIA_URL,)
