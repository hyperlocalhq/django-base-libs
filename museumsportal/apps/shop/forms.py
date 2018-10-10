# -*- coding: UTF-8 -*-

from django.db import models
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils import timezone

import autocomplete_light

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from jetson.apps.image_mods.models import FileManager

from museumsportal.utils.forms import PrimarySubmit
from museumsportal.utils.forms import SecondarySubmit
from museumsportal.utils.forms import ModelMultipleChoiceTreeField

FRONTEND_LANGUAGES = getattr(settings, "FRONTEND_LANGUAGES", settings.LANGUAGES)

ShopProduct = models.get_model("shop", "ShopProduct")
ShopProductType = models.get_model("shop", "ShopProductType")


class ShopProductForm(autocomplete_light.ModelForm):

    image_path = forms.CharField(
        label="Product Image",
        max_length=255,
        widget=forms.TextInput(),
        required=True,
    )

    product_types = ModelMultipleChoiceTreeField(
        label=_("Types"),
        required=False,
        queryset=ShopProductType.objects.all(),
    )

    image_title_de = forms.CharField(
        label=_('Caption')+' DE',
        required=False,
        max_length=255,
    )

    image_title_en = forms.CharField(
        label=_('Caption')+' EN',
        required=False,
        max_length=255,
    )

    image_description_de = forms.CharField(
        label=_('Description (will be used as alt attribute)')+' DE',
        required=False,
        max_length=255,
    )

    image_description_en = forms.CharField(
        label=_('Description (will be used as alt attribute)')+' EN',
        required=False,
        max_length=255,
    )

    image_author = forms.CharField(
        label=_('Copyright / Photographer'),
        required=False,
        max_length=255,
    )

    class Meta:
        model = ShopProduct

        fields = [
            'price', 'link', 'languages',
            'product_types',
            #'is_new',
            #'is_featured',
            #'is_for_children',
            'museums', 'exhibitions', 'events', 'workshops',
        ]
        autocomplete_fields = ('museums', 'exhibitions', 'events', 'workshops')
        autocomplete_names = {
            'museums': 'OwnMuseumAutocomplete',
            'exhibitions': 'OwnExhibitionAutocomplete',
            'events': 'OwnEventAutocomplete',
            'workshops': 'OwnWorkshopAutocomplete',
        }

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            fields += [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'description_%s' % lang_code,
            ]

    def __init__(self, *args, **kwargs):
        super(ShopProductForm, self).__init__(*args, **kwargs)

        self.fields['link'] = forms.URLField(
            label=_("Shop Link"),
        )

        self.fields['price'].label = _("Price")

        self.fields['languages'].widget = forms.CheckboxSelectMultiple()
        self.fields['languages'].help_text = ""
        self.fields['languages'].empty_label = None

        #self.fields['product_categories'].widget = forms.CheckboxSelectMultiple()
        #self.fields['product_categories'].help_text = ""
        #self.fields['product_categories'].empty_label = None

        self.fields['product_types'].help_text = ""
        self.fields['product_types'].empty_label = None
        self.fields['product_types'].level_indicator = "/ "

        for lang_code, lang_name in FRONTEND_LANGUAGES:
            for f in [
                'title_%s' % lang_code,
                'subtitle_%s' % lang_code,
                'description_%s' % lang_code,
            ]:
                self.fields[f].label += """ <span class="lang">%s</span>""" % lang_code.upper()

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        layout_blocks = []

        fieldset_content = []  # collect multilingual divs into one list...
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('title_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('subtitle_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('description_%s' % lang_code, css_class="tinymce"),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(
            bootstrap.AppendedText("price", "€")
        )
        fieldset_content.append(
            layout.Field("link", placeholder="http://")
        )

        layout_blocks.append(layout.Fieldset(
            _("Basic Info"),
            css_class="fieldset-basic-info",
            *fieldset_content
        ))


        fieldset_content = []
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('image_title_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(layout.Row(
            css_class="row-md",
            *[layout.Div(
                layout.Field('image_description_%s' % lang_code),
                css_class="col-xs-6 col-sm-6 col-md-6 col-lg-6",
            ) for lang_code, lang_name in FRONTEND_LANGUAGES]
        ))
        fieldset_content.append(
            "image_author"
        )
        layout_blocks.append(layout.Fieldset(
            _("Image"),
            layout.Field("image_path"),
            layout.HTML(u"""{% load i18n image_modifications %}
                <div id="image_preview">
                    {% if object.image %}
                        <img src="{{ MEDIA_URL }}{{ object.image|modified_path:"shop_small" }}" alt="" />
                        <script>
                            $('#id_image_path').val('preset');
                        </script>
                    {% endif %}
                </div>
                <div id="image_uploader">
                    <noscript>
                        <p>{% trans "Please enable JavaScript to use file uploader." %}</p>
                    </noscript>
                </div>
                <p id="image_help_text" class="help-block">{% trans "Available formats are JPG, GIF, and PNG." %}</p>
                <div class="control-group error"><div class="messages help-block"></div></div>
                <style>
                    #div_id_image_path input {display:none;}
                </style>
            """),
            css_id="profile_image_upload",
            css_class="fieldset-pdf-files",
            *fieldset_content
        ))

        fieldset_content = []
        fieldset_content.append(
            "languages"
        )
        #fieldset_content.append(
        #    "product_categories"
        #)
        fieldset_content.append(
            layout.Div(
                layout.HTML("""{% load i18n %} <label>{% trans "Product Types" %}</label>"""),
                layout.Field("product_types", template="utils/checkboxselectmultipletree.html")
            ),
        )
        #fieldset_content.append(
        #    "is_new"
        #)
        #fieldset_content.append(
        #    "is_featured"
        #)
        #fieldset_content.append(
        #    "is_for_children"
        #)

        layout_blocks.append(layout.Fieldset(
            _("Categories and Tags"),
            css_class="fieldset-categories-tags",
            *fieldset_content
        ))

        layout_blocks.append(layout.Fieldset(
            _("Related museums, exhibitions, events, and guided tours"),
            layout.Field("museums", placeholder=_("Type some text to search in your museums")),
            layout.Field("exhibitions", placeholder=_("Type some text to search in your exhibitions")),
            layout.Field("events", placeholder=_("Type some text to search in your events")),
            layout.Field("workshops", placeholder=_("Type some text to search in your workshops")),
            css_class="fieldset-related-objects"
        ))

        layout_blocks.append(bootstrap.FormActions(
            PrimarySubmit('submit', _('Save')),
            SecondarySubmit('reset', _('Cancel')),
        ))

        self.helper.layout = layout.Layout(
            *layout_blocks
        )

    def clean_image_path(self):
        data = self.cleaned_data['image_path']
        if ".." in data:
            raise forms.ValidationError(_("Double dots are not allowed in the file name."))
        return data
