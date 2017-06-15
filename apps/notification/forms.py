# -*- coding: UTF-8 -*-
from collections import OrderedDict
from django import forms
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.translation import string_concat
from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap
from base_libs.middleware.threadlocals import get_current_language
from .models import NoticeType, NOTICE_MEDIA, NOTICE_FREQUENCY
from .tasks import get_notification_setting


class NoticeSettingsForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(NoticeSettingsForm, self).__init__(*args, **kwargs)
        self.user = user

        if self.user.is_staff:
            queryset = NoticeType.objects.all().order_by(
                "sort_order",
                "category__title_%s" % get_current_language(),
                "display",
            )
        else:
            queryset = NoticeType.objects.filter(is_public=True).order_by(
                "sort_order",
                "category__title_%s" % get_current_language(),
                "display",
            )

        fields_for_fieldsets = OrderedDict()

        for notice_type in queryset:
            for medium_id, medium_display in NOTICE_MEDIA:
                field_name = "%s_%s_frequency" % (notice_type.sysname, medium_id)
                setting = get_notification_setting(self.user, notice_type, medium_id)

                label = notice_type.get_display()
                if not notice_type.is_public:
                    label = string_concat(label, ' (', _("Staff"), ')')

                self.fields[field_name] = forms.ChoiceField(
                    label=label,
                    choices=NOTICE_FREQUENCY,
                    help_text=notice_type.get_description(),
                    initial=setting.frequency,
                )

                category_title = ugettext("Unspecified")
                if notice_type.category:
                    category_title = notice_type.category.title

                fields_for_fieldsets.setdefault(category_title, []).append(field_name)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.attrs = {
            'enctype': "multipart/form-data",
        }

        elements = [
            layout.Fieldset(fieldset_name, *field_names)
            for fieldset_name, field_names in fields_for_fieldsets.items()
        ]
        elements.append(
            bootstrap.FormActions(layout.Submit('submit', _('Save')))
        )
        self.helper.layout = layout.Layout(*elements)

    def save(self):
        cleaned_data = self.cleaned_data
        if self.user.is_staff:
            queryset = NoticeType.objects.all().order_by("category__title_%s" % get_current_language(), "display")
        else:
            queryset = NoticeType.objects.filter(is_public=True).order_by("category__title_%s" % get_current_language(), "display")

        for notice_type in queryset:
            for medium_id, medium_display in NOTICE_MEDIA:
                field_name = "%s_%s_frequency" % (notice_type.sysname, medium_id)
                setting = get_notification_setting(self.user, notice_type, medium_id)
                setting.frequency = cleaned_data[field_name]
                setting.save()
