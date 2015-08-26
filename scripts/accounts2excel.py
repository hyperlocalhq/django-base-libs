import os
import sys


def configure_django_project():
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    EXTERNAL_LIBS_PATH = os.path.join(PROJECT_PATH, "jetson", "externals", "libs")
    EXTERNAL_APPS_PATH = os.path.join(PROJECT_PATH, "jetson", "externals", "apps")

    sys.path = ["", EXTERNAL_LIBS_PATH, EXTERNAL_APPS_PATH, PROJECT_PATH] + sys.path
    os.environ["DJANGO_SETTINGS_MODULE"] = "ccb.settings"
    os.environ["PYTHON_EGG_CACHE"] = os.path.abspath(os.path.join(PROJECT_PATH, "ccb", "tmp", "python_cache"))


def export_accounts(filename_postfix="", **filters):
    from django.utils.encoding import force_unicode
    from django.conf import settings
    from django.contrib.auth.models import User

    from base_libs.middleware.threadlocals import set_current_user
    from pyExcelerator import Workbook, Font, XFStyle, UnicodeUtils

    from ccb.apps.people.models import Person
    from ccb.apps.institutions.models import Institution

    set_current_user(User.objects.filter(is_superuser=True)[0])

    w = Workbook()
    font = Font()
    font.bold = True
    header_style = XFStyle()
    header_style.font = font
    UnicodeUtils.DEFAULT_ENCODING = 'utf8'

    ws_0 = w.add_sheet('People')
    row = 0
    # width in 1/256th of zero character
    col_widths = [
        256 * 20,
        256 * 20,
        256 * 20,
        256 * 40,
        256 * 20,
        256 * 20,
        256 * 20,
        256 * 20,
        256 * 20,
        256 * 20,
        256 * 20,
        256 * 20,
        256 * 60,
        256 * 20,
    ]
    row_content = [
        "Username",
        "First Name",
        "Last Name",
        "Email",
        "Phone",
        "Fax",
        "Mobile",
        "Street Address",
        "Street Address (line 2)",
        "Postal Code",
        "City",
        "Country",
        "Creative Sectors",
        "Status",
    ]
    col = 0
    for val in row_content:
        ws_0.write(row, col, val, header_style)
        ws_0.col(col).width = col_widths[col]
        col += 1
    for p in Person.objects.filter(**filters).distinct():
        row += 1
        try:
            contact = p.get_primary_contact()
        except Exception:
            contact = {}
        row_content = [
            p.user.username,
            p.user.first_name,
            p.user.last_name,
            p.user.email,
            contact.get("phone_country", "") + " " + contact.get("phone_area", "") + " " + contact.get("phone_number",
                                                                                                       ""),
            contact.get("fax_country", "") + " " + contact.get("fax_area", "") + " " + contact.get("fax_number", ""),
            contact.get("mobile_country", "") + " " + contact.get("mobile_area", "") + " " + contact.get(
                "mobile_number", ""),
            contact.get("street_address", ""),
            contact.get("street_address2", ""),
            contact.get("postal_code", ""),
            contact.get("city", ""),
            contact.get("country_name", ""),
            ", ".join([force_unicode(sector) for sector in p.creative_sectors.all()]),
            force_unicode(p.status),
        ]
        col = 0
        for val in row_content:
            ws_0.write(row, col, val)
            col += 1

    ws_1 = w.add_sheet('Institutions')
    row = 0
    # width in 1/256th of zero character
    col_widths = [
        256 * 20,
        256 * 40,
        256 * 40,
        256 * 40,
        256 * 20,
        256 * 20,
        256 * 20,
        256 * 20,
        256 * 20,
        256 * 20,
        256 * 20,
        256 * 20,
        256 * 60,
        256 * 20,
    ]
    row_content = [
        "Slug",
        "Title",
        "Website",
        "Email",
        "Phone",
        "Fax",
        "Mobile",
        "Street Address",
        "Street Address (line 2)",
        "Postal Code",
        "City",
        "Country",
        "Creative Sectors",
        "Status",
    ]
    col = 0
    for val in row_content:
        ws_1.write(row, col, val, header_style)
        ws_1.col(col).width = col_widths[col]
        col += 1
    for inst in Institution.objects.filter(**filters).distinct():
        row += 1
        try:
            contact = inst.get_primary_contact()
        except Exception:
            contact = {}
        row_content = [
            inst.slug,
            inst.get_title(),
            contact.get("url0_link", ""),
            contact.get("email0_address", ""),
            contact.get("phone_country", "") + " " + contact.get("phone_area", "") + " " + contact.get("phone_number",
                                                                                                       ""),
            contact.get("fax_country", "") + " " + contact.get("fax_area", "") + " " + contact.get("fax_number", ""),
            contact.get("mobile_country", "") + " " + contact.get("mobile_area", "") + " " + contact.get(
                "mobile_number", ""),
            contact.get("street_address", ""),
            contact.get("street_address2", ""),
            contact.get("postal_code", ""),
            contact.get("city", ""),
            contact.get("country_name", ""),
            ", ".join([force_unicode(sector) for sector in inst.creative_sectors.all()]),
            force_unicode(inst.status),
        ]
        col = 0
        for val in row_content:
            ws_1.write(row, col, val)
            col += 1

    w.save(os.path.join(
        settings.PROJECT_PATH,
        'ccb',
        'data',
        'accounts%s.xls' % filename_postfix,
    ))


def export_necessary():
    from jetson.apps.structure.models import Term

    sector = Term.objects.get(slug="games-and-interactive")
    export_accounts()
    export_accounts("_icb", creative_sectors__path_search__startswith=sector.path_search)


def main():
    configure_django_project()
    export_necessary()


if __name__ == '__main__':
    main()
