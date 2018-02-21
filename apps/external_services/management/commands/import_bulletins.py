# -*- coding: UTF-8 -*-
from optparse import make_option

from django.core.management.base import BaseCommand

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(BaseCommand):
    help = """Imports bulletins from the bulletin-import sources"""
    option_list = BaseCommand.option_list + (
        make_option(
            '--update-all',
            action='store_true',
            dest='update_all',
            default=False,
            help='Update all bulletins no matter what',
        ),
    )

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', NORMAL))
        update_all = options.get('update_all')

        import requests
        from datetime import datetime, timedelta

        from xml.dom.minidom import parseString
        from dateutil.parser import parse as parse_datetime

        from django.apps import apps
        from django.db import models
        from django.core.exceptions import MultipleObjectsReturned

        from base_libs.utils.misc import html_to_plain_text

        from jetson.apps.external_services.utils import get_value
        from jetson.apps.external_services.utils import date_de_to_en

        Bulletin = apps.get_model("bulletin_board", "Bulletin")
        BulletinCategory = apps.get_model("bulletin_board", "BulletinCategory")
        BulletinImportSource = apps.get_model("external_services", "BulletinImportSource")
        ObjectMapper = apps.get_model("external_services", "ObjectMapper")

        BULLETIN_CATEGORY_MAPPER = {
            'partner': BulletinCategory.objects.get(slug="partner"),
            'know how': BulletinCategory.objects.get(slug="know-how"),
            'material resources': BulletinCategory.objects.get(slug="material-resources"),
            'facilities': BulletinCategory.objects.get(slug="facilities"),
            'other': BulletinCategory.objects.get(slug="other"),
        }

        # default_bulletin_type = get_related_queryset(
        #     Bulletin,
        #     "bulletin_type",
        # ).get(slug="whatever")

        services_failed = []
        bulletins_failed = []

        for s in BulletinImportSource.objects.all():
            if verbosity > NORMAL:
                self.stdout.write(u"Importing from {}...\n".format(s.title))
                self.stdout.flush()
            try:
                response = requests.get(
                    s.url,
                    allow_redirects=True,
                    verify=False,
                    headers={
                        'User-Agent': 'Creative City Berlin',
                    }
                )
            except requests.exceptions.ConnectionError:
                services_failed.append(s)
                continue

            if response.status_code != 200:
                services_failed.append(s)
                continue
            data = response.content

            # quick fix of broken feeds
            data = data.replace("& ", "&amp; ")

            try:
                xml_doc = parseString(data)
            except Exception:
                services_failed.append(s)
                continue

            for node_bulletin in xml_doc.getElementsByTagName("item"):
                external_id = (
                    get_value(node_bulletin, "guid")  # if guid is not provided
                    or get_value(node_bulletin, "link")  # use link as external_id
                    or get_value(node_bulletin, "source_url") # use source_url as external_id
                    or get_value(node_bulletin, "url") # use url as external_id
                )
                published = date_de_to_en(
                    get_value(node_bulletin, "pubDate") or
                    get_value(node_bulletin, "dc:date") or
                    get_value(node_bulletin, "published")
                )
                change_date = parse_datetime(published, ignoretz=True)
                status = ""
                # get or create bulletin
                mapper = None
                try:
                    # get bulletin from saved mapper
                    mapper = s.objectmapper_set.get(
                        external_id=external_id,
                        content_type__app_label="bulletin_board",
                        content_type__model="bulletin",
                    )
                except models.ObjectDoesNotExist:
                    # or create a new bulletin and then create a mapper
                    bulletin = Bulletin()
                except MultipleObjectsReturned:
                    print u"Database integrity error with bulletin which external_id is %s." % external_id
                    continue
                else:
                    bulletin = mapper.content_object
                    if not bulletin:
                        # if bulletin was deleted after import,
                        # don't import it again
                        continue
                    status = bulletin.status
                    if status == "expired" or update_all:
                        status = s.default_status
                        bulletin.status = status
                    # update bulletin without changing the modified_date
                    Bulletin.objects.filter(id=bulletin.pk).update(
                        published_till=datetime.now() + timedelta(days=1),
                        status=status,
                    )
                    if bulletin.modified_date:
                        if not update_all and (bulletin.modified_date > change_date or bulletin.status == "published"):
                            continue

                bulletin.orig_published = change_date
                bulletin.published_from = change_date
                bulletin.published_till = datetime.now() + timedelta(days=1)

                bulletin.title = get_value(node_bulletin, "title")

                bulletin_type = get_value(node_bulletin, "type")
                if bulletin_type in ("suche", "search"):
                    bulletin_type = "searching"
                else:
                    bulletin_type = "offering"
                bulletin.bulletin_type = bulletin_type

                bulletin_category_str = get_value(node_bulletin, "category")
                bulletin.bulletin_category = BULLETIN_CATEGORY_MAPPER.get(
                    bulletin_category_str.lower(),
                    s.default_bulletin_category
                )

                content = (
                    get_value(node_bulletin, "content:encoded") or
                    get_value(node_bulletin, "description") or
                    get_value(node_bulletin, "details")
                )
                bulletin.description = html_to_plain_text(content)

                # bulletin.language = bulletin.guess_language()

                bulletin.contact_person = get_value(node_bulletin, "dc:creator")
                bulletin.institution_title = get_value(node_bulletin, "company")

                bulletin.external_url = (
                    get_value(node_bulletin, "link") or
                    get_value(node_bulletin, "source_url") or
                    get_value(node_bulletin, "url")
                )

                # bulletin.bulletin_type = default_bulletin_type

                # set status
                bulletin.status = status or s.default_status

                # set content provider
                bulletin.content_provider = s.content_provider

                # TODO: save image
                image_url = get_value(node_bulletin, "image_url")

                try:
                    bulletin.save()
                except Exception:
                    bulletins_failed.append(bulletin)
                    continue

                # set categories
                bulletin.categories.clear()
                for cs in s.default_categories.all():
                    bulletin.categories.add(cs)

                if verbosity > NORMAL:
                    self.stdout.write(u" - {} (PK={})\n".format(bulletin.title, bulletin.pk))
                    self.stdout.flush()

                if not mapper:
                    mapper = ObjectMapper(
                        service=s,
                        external_id=external_id,
                    )
                    mapper.content_object = bulletin
                    mapper.save()

        if update_all:
            # make sure that expired bulletins don't show up
            Bulletin.expired_objects.update_status()

        if verbosity > NORMAL:
            print "Services failed: %d" % len(services_failed)
            for s in services_failed:
                print "    %s" % s.url
            print "Bulletins failed: %d" % len(bulletins_failed)
            for a in bulletins_failed:
                print "    %s" % a.external_url
