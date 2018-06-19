# -*- coding: UTF-8 -*-
from django.conf import settings

# Institution = models.get_model("institutions", "Institution")
# LEGAL_FORM_CHOICES = ESTABLISHMENT_YYYY_CHOICES = ESTABLISHMENT_MM_CHOICES = INSTITUTION_LOCATION_TYPE_CHOICES = ()
# InstitutionalContact = URL_ID_INSTITUTION = URL_ID_INSTITUTIONS = None
# if Institution:
#     app = models.get_app("institutions")
#     InstitutionalContact, URL_ID_INSTITUTION, URL_ID_INSTITUTIONS = (
#         app.InstitutionalContact, app.URL_ID_INSTITUTION, app.URL_ID_INSTITUTIONS,
#     )
#     LEGAL_FORM_CHOICES = XChoiceList(get_related_queryset(Institution, 'legal_form'))
#     ESTABLISHMENT_YYYY_CHOICES = Institution._meta.get_field('establishment_yyyy').get_choices()
#     ESTABLISHMENT_YYYY_CHOICES[0] = ("", _("Year"))
#     ESTABLISHMENT_MM_CHOICES = Institution._meta.get_field('establishment_mm').get_choices()
#     ESTABLISHMENT_MM_CHOICES[0] = ("", _("Month"))
#     INSTITUTION_LOCATION_TYPE_CHOICES = XChoiceList(get_related_queryset(InstitutionalContact, 'location_type'))
#
# WEEK_DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
#

# BIRTHDAY_DD_CHOICES = Person._meta.get_field('birthday_dd').get_choices()
# BIRTHDAY_DD_CHOICES[0] = ("", _("Day"))
# BIRTHDAY_MM_CHOICES = Person._meta.get_field('birthday_mm').get_choices()
# BIRTHDAY_MM_CHOICES[0] = ("", _("Month"))
# BIRTHDAY_YYYY_CHOICES = Person._meta.get_field('birthday_yyyy').get_choices()
# BIRTHDAY_YYYY_CHOICES[0] = ("", _("Year"))
#
# NATIONALITY_CHOICES = XChoiceList(get_related_queryset(Person, 'nationality'))
# SALUTATION_CHOICES = XChoiceList(get_related_queryset(Person, 'salutation'))
#
# URL_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, 'url0_type'))
# IM_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, 'im0_type'))
# LOCATION_TYPE_CHOICES = XChoiceList(get_related_queryset(IndividualContact, 'location_type'))

# prexixes of fields to guarantee uniqueness
PREFIX_CI = 'CI_'  # Creative Sector aka Creative Industry
PREFIX_BC = 'BC_'  # Context Category aka Business Category
PREFIX_OT = 'OT_'  # Object Type
PREFIX_LT = 'LT_'  # Location Type

LOGO_SIZE = getattr(settings, "LOGO_SIZE", (100, 100))
STR_LOGO_SIZE = "%sx%s" % LOGO_SIZE
