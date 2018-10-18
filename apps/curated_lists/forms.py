# -*- coding: UTF-8 -*-
import operator
from functools import reduce

from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext
from django.db import models
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms import layout, bootstrap

from ccb.apps.curated_lists.models import ListOwner
from ccb.apps.site_specific.models import ContextItem
from jetson.apps.structure.models import Category

from base_libs.forms.fields import ImageField

from .models import CuratedList, ListItem


MIN_LOGO_SIZE = getattr(settings, "LOGO_SIZE", (850, 400))
STR_MIN_LOGO_SIZE = "%sx%s" % MIN_LOGO_SIZE


class CuratedListForm(forms.Form):
    title = forms.CharField(
        label=_("Title"),
        required=True,
    )
    description = forms.CharField(
        label=_("Description"),
        required=False,
        widget=forms.Textarea(),
    )
    image = ImageField(
        label=_("Main Photo"),
        help_text=_(
            "You can upload GIF, JPG, and PNG images. The minimal dimensions are %s px.") % STR_MIN_LOGO_SIZE,
        required=False,
        min_dimensions=MIN_LOGO_SIZE,
    )
    tmp_image_filename = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.HiddenInput(),
    )
    image_author = forms.CharField(
        label=_("Photo Credits"),
        required=False,
        max_length=100,
    )

    def __init__(self, request, curated_list, *args, **kwargs):
        super(CuratedListForm, self).__init__(*args, **kwargs)
        self.request = request
        self.curated_list = curated_list

        if not self.curated_list:
            choices = [
                ('people.person.{}'.format(request.user.pk), request.user.profile.get_title())
            ]
            for contact in request.user.profile.individualcontact_set.exclude(institution=None).only("institution"):
                choices.append(('institutions.institution.{}'.format(contact.institution.pk), contact.institution.title))
            self.field['owner'] = forms.ChoiceField(
                label=_("Owner"),
                choices=choices,
            )

        if not self.initial:
            self.initial = {
                'title': getattr(curated_list, "title_{}".format(settings.LANGUAGE_CODE), ""),
                'description': getattr(curated_list, "description_{}".format(settings.LANGUAGE_CODE), ""),
                'image_author': getattr(curated_list, "image_author"),
            }

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Edit Curated List Description"),
                layout.Field("title"),
                layout.Field("description", rows=5),
                layout.Field("image"),
                layout.HTML("""{% load image_modifications %}
                <dl>
                {% if form.tmp_image_filename.data %}
                    <dt>&nbsp;</dt>
                    <dd>
                        <img src="/{{ LANGUAGE_CODE }}/helper/tmpimage/{{ form.tmp_image_filename.data }}/800x600/" alt="" />
                    </dd>
                {% elif curated_list.image %}
                    <dt>&nbsp;</dt>
                    <dd>
                        <img src="{{ UPLOADS_URL }}{{ form.curated_list.image|modified_path:'article' }}" alt="" />
                    </dd>
                {% else %}
                    <dt>&nbsp;</dt>
                    <dd>
                        <img src="{{ STATIC_URL }}site/img/placeholder/gallery_square.png" alt="" />
                    </dd>
                {% endif %}
                </dl>
                """),
                layout.Field("tmp_image_filename"),
                layout.Field("image_author"),
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Save')),
            )
        )

    def clean_tmp_image_filename(self):
        value = self.cleaned_data['tmp_image_filename']
        if "/" in value:
            # quick security check ensuring that there are no relative paths instead of just a filename
            raise forms.ValidationError(_("Temporary image filename is invalid"))
        return value

    def save(self, commit=True):
        cleaned = self.cleaned_data
        if not self.curated_list:
            self.curated_list = CuratedList
        for lang_code, lang_name in settings.LANGUAGES:
            setattr(self.curated_list, "title_{}".format(lang_code), cleaned['title'])
            setattr(self.curated_list, "description_{}".format(lang_code), cleaned['description'])
            if not getattr(self.curated_list, "description_{}_markup_type".format(lang_code)):
                setattr(self.curated_list, "description_{}_markup_type".format(lang_code), "pt")
        self.curated_list.image_author = cleaned['image_author']
        if commit:
            self.curated_list.save()
        return self.curated_list


class CuratedListItemForm(forms.Form):
    title = forms.CharField(
        label=_("Title"),
        required=True,
    )
    description = forms.CharField(
        label=_("Description"),
        required=False,
        widget=forms.Textarea(attrs={'rows': 5}),
    )

    def __init__(self, curated_list, item, *args, **kwargs):
        super(CuratedListItemForm, self).__init__(*args, **kwargs)

        self.curated_list = curated_list
        self.item = item

        if not self.initial:
            self.initial = {
                'title': getattr(item, "title_{}".format(settings.LANGUAGE_CODE), ""),
                'description': getattr(item, "description_{}".format(settings.LANGUAGE_CODE), ""),
            }

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Edit Curated List Description"),
                "title",
                layout.Field("description", rows=5),
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Save')),
            )
        )

    def save(self, commit=True):
        cleaned = self.cleaned_data
        if not self.item:
            self.item = ListItem(curated_list=self.curated_list)
        for lang_code, lang_name in settings.LANGUAGES:
            setattr(self.item, "title_{}".format(lang_code), cleaned['title'])
            setattr(self.item, "description_{}".format(lang_code), cleaned['description'])
            if not getattr(self.item, "description_{}_markup_type".format(lang_code)):
                setattr(self.item, "description_{}_markup_type".format(lang_code), "pt")
        if commit:
            self.item.save()
        return self.item


class CuratedListFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        label=_("Category"),
        empty_label=_("All"),
        queryset=Category.objects.filter(level=0),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(CuratedListFilterForm, self).__init__(*args, **kwargs)

        # Get all unique Person and Institution instances
        # that apply for owners of published and featured curated lists
        unique_owners = ListOwner.objects.filter(
            curated_list__privacy="public",
            curated_list__is_featured=True,
        ).values(
            "owner_content_type", "owner_object_id"
        ).order_by("owner_content_type", "owner_object_id").distinct()

        if unique_owners:
            # Create an owner ModelChoiceField with ContextItem instances matching unique owners
            context_item_qs = ContextItem.objects.filter(
                reduce(operator.ior, [
                    models.Q(content_type__id=owner['owner_content_type']) &
                    models.Q(object_id=owner['owner_object_id'])
                    for owner in unique_owners
                ])
            ).order_by("title")
        else:
            context_item_qs = ContextItem.objects.none()

        self.fields['owner'] = forms.ModelChoiceField(
            label=_("Curator"),
            empty_label=_("All"),
            queryset=context_item_qs,
            required=False,
        )


        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "GET"
        self.helper.form_id = "filter_form"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Filter"),
                layout.Field("owner", template="ccb_form/custom_widgets/filter_field.html"),
                layout.Field("category", template="ccb_form/custom_widgets/category_filter_field.html"),
                template="ccb_form/custom_widgets/filter.html"
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Search')),
            )
        )


class OwnerInvitationForm(forms.Form):
    first_name = forms.CharField(
        label=_("First name"),
        required=True,
    )
    last_name = forms.CharField(
        label=_("Last name"),
        required=True,
    )
    email = forms.EmailField(
        label=_("Email"),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(OwnerInvitationForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"

        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Invite another owner of the curated list"),
                layout.Field("first_name"),
                layout.Field("last_name"),
                layout.Field("email"),
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Send invitation')),
            )
        )


class CuratedListDeletionForm(forms.Form):
    def __init__(self, curated_list, *args, **kwargs):
        super(CuratedListDeletionForm, self).__init__(*args, **kwargs)
        self.curated_list = curated_list

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Confirm deletion"),
                layout.HTML("""{% load i18n %}
                <p>{% blocktrans with curated_list_title=form.curated_list.title trimmed %}
                    Do you realy want to delete the curated list "{{ curated_list_title }}"?
                {% endblocktrans %}</p>
                """)
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Delete')),
            )
        )

    def delete(self):
        self.curated_list.delete()


class CuratedListItemRemovalForm(forms.Form):
    def __init__(self, curated_list, item, *args, **kwargs):
        super(CuratedListItemRemovalForm, self).__init__(*args, **kwargs)
        self.curated_list = curated_list
        self.item = item

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Confirm deletion"),
                layout.HTML("""{% load i18n %}
                <p>{% blocktrans with curated_list_title=form.curated_list.title item_title=form.item.title trimmed %}
                    Do you realy want to remove "{{ item_title }}" from the curated list "{{ curated_list_title }}"?
                {% endblocktrans %}</p>
                """)
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Remove')),
            )
        )

    def remove(self):
        self.item.delete()


class CuratedListOwnerRemovalForm(forms.Form):
    def __init__(self, curated_list, owner, *args, **kwargs):
        super(CuratedListOwnerRemovalForm, self).__init__(*args, **kwargs)
        self.curated_list = curated_list
        self.owner = owner

        self.helper = FormHelper()
        self.helper.form_action = ""
        self.helper.form_method = "POST"
        self.helper.layout = layout.Layout(
            layout.Fieldset(
                _("Confirm deletion"),
                layout.HTML("""{% load i18n %}
                <p>{% blocktrans with curated_list_title=form.curated_list.title owner_title=form.owner.representation trimmed %}
                    Do you realy want to remove {{ owner_title }} from the owners of the curated list "{{ curated_list_title }}"?
                {% endblocktrans %}</p>
                """)
            ),
            bootstrap.FormActions(
                layout.Submit('submit', _('Remove')),
            )
        )

    def remove(self):
        self.owner.delete()


### Forms for JSON views ###

class AddItemToNewCuratedListForm(forms.Form):
    """Form used for creating a new curated list by Ajax and adding an item to it"""
    owner_app_model = forms.ChoiceField(
        choices=(
            ('people.person', 'Person'),
            ('institutions.institution', 'Institution'),
        )
    )
    owner_pk = forms.CharField()
    title = forms.CharField()
    item_content_type_id = forms.IntegerField()
    item_object_id = forms.CharField()


class ItemAtCuratedListForm(forms.Form):
    """Form used for adding or removing items by Ajax to and from an existing curated list"""
    curated_list_token = forms.CharField()
    item_content_type_id = forms.IntegerField()
    item_object_id = forms.CharField()
