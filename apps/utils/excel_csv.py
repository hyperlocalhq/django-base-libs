# -*- coding: utf-8 -*-
"""
You can run this script from creativeberlin as the current directory:

    python jetson/utils/excel_csv.py

Or from the python shell:
    
    python manage.py shell
    >>> from utils.excel_csv import read_excel_csv, test
    >>> read_excel_csv(filepath="/absolute/path/to/spreadsheet.csv", function=test)
"""
import csv

import os, sys
import django.core.management, django.core
from os.path import isdir, isfile, join, dirname
import datetime

try:
    from dev_environment import *
except:
    is_dev_environment = False

if "PYTHONPATH" in os.environ:
    os.environ["PYTHONPATH"] += "."
else:
    os.environ["PYTHONPATH"] = "."
os.environ["DJANGO_SETTINGS_MODULE"] = "jetson.settings"

from django.conf import settings


def test(l):
    print l


def create_institution(l):
    from django.db import models
    app = models.get_app("institutions")
    Institution, InstitutionalContact = (
        app.Institution,
        app.InstitutionalContact,
    )
    from jetson.apps.optionset.models import PhoneType
    from jetson.apps.structure.models import Term
    from jetson.apps.location.models import Address
    title = l[0].strip()
    if not title:
        return
    street = l[1]
    postal_code = l[2]
    phone = l[3]
    website = l[4]
    try:
        description = l[5]
    except:
        description = ""
    if title == "NAME" and street == "STRASSE":
        return
    print title
    status = Term.objects.get(sysname="import")
    i = Institution(
        title=title,
        description_de=description,
        status=status,
    )
    i.save()
    try:
        phone0_area, phone0_number = phone.split("-", 1)
    except:
        phone0_area = "030"
        phone0_number = ""
    if phone0_area == "030":
        phone0_type = PhoneType.objects.get(slug="phone")
    else:
        phone0_type = PhoneType.objects.get(slug="mobile")
    if website:
        website = "http://" + website
    contact = i.institutionalcontact_set.create(
        is_temporary=False,
        phone0_type=phone0_type,
        phone0_country="49",
        phone0_area=phone0_area,
        phone0_number=phone0_number,
        url0_link=website,
    )
    Address.objects.set_for(
        contact,
        "postal_address",
        street_address=street,
        postal_code=postal_code,
        city="Berlin",
        country="DE",
    )


def latin1_to_utf8(text):
    return unicode(text, "iso-8859-2").encode("utf-8")


def create_institution2(l):
    from django.db import models
    app = models.get_app("institutions")
    Institution, InstitutionalContact = (
        app.Institution,
        app.InstitutionalContact,
    )
    from jetson.apps.optionset.models import PhoneType
    from jetson.apps.structure.models import Term
    from jetson.apps.location.models import Address
    branch = latin1_to_utf8(l[0].strip())
    if not branch or branch == "Branche":
        return
    title = latin1_to_utf8(l[1].strip())
    cat = latin1_to_utf8(l[2].strip())
    street = latin1_to_utf8(l[3].strip())
    postal_code = latin1_to_utf8(l[4].strip())
    city = latin1_to_utf8(l[5].strip())
    phone_country = latin1_to_utf8(l[6].strip())
    phone_area = latin1_to_utf8(l[7].strip())
    phone_number = latin1_to_utf8(l[8].strip())
    fax_country = latin1_to_utf8(l[9].strip())
    fax_area = latin1_to_utf8(l[10].strip())
    fax_number = latin1_to_utf8(l[11].strip())
    website = latin1_to_utf8(l[12].strip())
    email = latin1_to_utf8(l[13].strip())
    print title
    status = Term.objects.get(sysname="import")
    i = Institution(
        title=title,
        status=status,
    )
    i.save()

    contact = i.institutionalcontact_set.create(
        is_primary=True,
        is_temporary=False,
        phone0_country="49",
        phone0_area=phone_area,
        phone0_number=phone_number,
        phone1_country="49",
        phone1_area=fax_area,
        phone1_number=fax_number,
        url0_link=website,
        email0_address=email,
    )
    Address.objects.set_for(
        contact,
        "postal_address",
        street_address=street,
        postal_code=postal_code,
        city=city,
        country="DE",
    )


def read_excel_csv(filepath, function):
    f = open(filepath, "rb")
    line_list = "".join(f.readlines()).split("\r")
    reader = csv.reader(line_list, delimiter=";", doublequote=True)
    for value_list in reader:
        function(value_list)


def main():
    #read_excel_csv(filepath="data/BerlinYellowPages2007.csv", function=create_institution)
    read_excel_csv(
        filepath="data/ICB_Dataimport.csv",
        function=create_institution2,
    )


if __name__ == '__main__':
    main()
