# -*- coding: UTF-8 -*-
import re

from django.core.management.base import NoArgsCommand
from django.utils.encoding import force_unicode

SILENT, NORMAL, VERBOSE = 0, 1, 2

url_regex = re.compile(
    r"^(?#Protocol)(?:(?:ht|f)tp(?:s?)://|~/|/)?"
    r"(?#Username:Password)(?:\w+:\w+@)?"
    r"(?#Subdomains)(?:"
    r"(?:[-\w]+\.)+(?#TopLevel Domains)"
    r"(?:com|org|net|gov|mil|biz|info|mobi|name|aero|jobs|museum|travel|[a-z]{2})"
    r")"
    r"(?#Port)(?::[\d]{1,5})?"
    r"(?#Directories)(?:(?:(?:/(?:[-\w~!$+|.,=]|%[a-f\d]{2})+)+|/)+|\?|#)?"
    r"(?#Query)(?:"
    r"(?:\?(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)"
    r"(?:&(?:[-\w~!$+|.,*:]|%[a-f\d{2}])+=(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)*"
    r")*"
    r"(?#Anchor)(?:#(?:[-\w~!$+|.,*:=]|%[a-f\d]{2})*)?$"
)

a_link_regex = re.compile("<a[^>]+?href=([\"'])([^\"']+?)\\1[^>]*>", re.IGNORECASE | re.MULTILINE)


class Command(NoArgsCommand):
    help = """Checks the database for broken links"""
    _checked_links = {}

    def handle_noargs(self, **options):
        self.verbosity = int(options.get('verbosity', NORMAL))

        self.initialize()
        self.main()
        self.finalize()

    def report_broken_links(self, obj, fields_with_broken_links):
        from django.apps import apps
        from base_libs.utils.misc import get_related_queryset

        Ticket = apps.get_model("tracker", "Ticket")
        ContentType = apps.get_model("contenttypes", "ContentType")
        User = apps.get_model("auth", "User")
        concern = get_related_queryset(Ticket, "concern").get(
            slug="broken-links",
        )
        description = [u'%s "%s" has broken links.\n' % (
            type(obj).__name__,
            force_unicode(obj),
        )]
        for f, links in fields_with_broken_links:
            description.append("%s:" % force_unicode(f.verbose_name))
            for link in links:
                description.append("    %s" % force_unicode(link))
        description.append(u"\nYou can fix the links here:")
        description.append(self.get_admin_link(obj))

        superuser = User.objects.filter(is_superuser=True)[0]
        t, created = Ticket.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
            concern=concern,
            description=u"\n".join(description),
            url=self.get_admin_link(obj),
            submitter=superuser,
            submitter_name=superuser.username,
            submitter_email=superuser.email,
        )

    def get_admin_link(self, obj):
        if hasattr(obj, "get_admin_link"):
            return obj.get_admin_link()
        else:
            from base_libs.utils.misc import get_website_url

            return "%sadmin/%s/%s/%s/" % (
                get_website_url(),
                obj._meta.app_label.lower(),
                type(obj).__name__.lower(),
                obj.pk,
            )

    def is_valid_link(self, value):
        import requests
        from django.utils.six.moves.urllib.parse import urlsplit

        if value.startswith("mailto:"):
            return True

        if value in self._checked_links:
            return self._checked_links[value]

        URL_VALIDATOR_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0'

        # If no URL path given, assume /
        if value and not urlsplit(value)[2]:
            value += '/'
        headers = {
            "Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
            "Accept-Language": "en-us,en;q=0.5",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
            "Connection": "close",
            "User-Agent": URL_VALIDATOR_USER_AGENT,
        }
        success = False
        try:
            # try HEAD request, because it is faster than GET
            response = requests.head(value, headers=headers, allow_redirects=True)
            if response.status_code == requests.codes.ok:
                success = True
            else:
                success = False
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.TooManyRedirects,
            requests.exceptions.MissingSchema,
        ) as exception:
            success = False
        except requests.exceptions.SSLError as exception:
            self.stderr.write("OpenSSL, pyOpenSSL, and virtual environment need to be upgraded.\n")
            self.stderr.flush()
            raise

        if not success:
            try:
                # try GET request
                response = requests.get(value, headers=headers, allow_redirects=True)
                if response.status_code == requests.codes.ok:
                    success = True
                else:
                    success = False
            except (
                requests.exceptions.ConnectionError,
                requests.exceptions.TooManyRedirects,
                requests.exceptions.MissingSchema,
            ) as exception:
                success = False
            except requests.exceptions.SSLError as exception:
                self.stderr.write("OpenSSL, pyOpenSSL, and virtual environment need to be upgraded.\n")
                self.stderr.flush()
                raise

        self._checked_links[value] = success
        return success

    def initialize(self):
        from django.db.models.query import Q
        # 3-tuple of "app_name.model_name", queryset filter, and a callable returning the object to edit, if a link is broken
        self.MODELS_TO_CHECK = (
            ("richtext.RichText", Q(placeholder__page__title_set__published=True), (lambda o: o.placeholder.page)),
            ("editorial.QuestionAnswer", Q(placeholder__page__title_set__published=True), (lambda o: o.placeholder.page)),
            ("editorial.Document", Q(placeholder__page__title_set__published=True), (lambda o: o.placeholder.page)),
            ("events.Event", Q(status="published"), (lambda o: o)),
            ("people.IndividualContact", Q(person__status="published"), (lambda o: o.person)),
            ("institutions.InstitutionalContact", Q(institution__status="published"), (lambda o: o.institution)),
            ("blog.Post", Q(status=1), (lambda o: o)),
            ("articles.Article", Q(status=1), (lambda o: o)),
        )
        self._checked_links = {}
        
    def main(self):
        from django.apps import apps
        from django.db import models

        # traverse models
        for app_model, filter, get_obj in self.MODELS_TO_CHECK:
            model = apps.get_model(*app_model.split("."))
            if self.verbosity >= NORMAL:
                self.stdout.write(u"Checking the {} model...\n".format(model.__name__))
                self.stdout.flush()
            # traverse instances
            for el in model._default_manager.filter(filter):
                fields_with_broken_links = []
                # traverse fields
                for f in model._meta.fields:
                    broken_links_in_field = []
                    if isinstance(f, models.URLField):
                        # check the value of URLField
                        m = url_regex.match(getattr(el, f.name) or "")
                        if m:
                            is_valid = self.is_valid_link(m.group(0))
                            if not is_valid:
                                broken_links_in_field.append(m.group(0))
                    elif isinstance(f, models.TextField) and not type(f).__name__.startswith("Multilingual"):
                        matches = a_link_regex.findall(getattr(el, f.name) or "")
                        # traverse <a href=""> links
                        for link_m in matches:
                            m = url_regex.match(link_m[1])
                            if m:
                                is_valid = self.is_valid_link(m.group(0))
                                if not is_valid:
                                    broken_links_in_field.append(m.group(0))
                    if broken_links_in_field:
                        fields_with_broken_links.append(
                            (f, broken_links_in_field),
                        )
                if fields_with_broken_links:
                    if self.verbosity >= NORMAL:
                        self.stdout.write(u"  {}\n".format(el))
                        self.stdout.flush()
                        for f, links in fields_with_broken_links:
                            self.stdout.write(u"    {}\n".format(f.verbose_name))
                            self.stdout.flush()
                            for link in links:
                                self.stdout.write(u"      {}\n".format(link))
                                self.stdout.flush()
                    self.report_broken_links(
                        get_obj(el),
                        fields_with_broken_links,
                    )
                    
    def finalize(self):
        if self.verbosity >= NORMAL:
            self.stdout.write(u"Total unique links: {}\n".format(len(self._checked_links)))
            self.stdout.flush()
        broken_links = [
            link
            for link, is_valid in self._checked_links.items()
            if not is_valid
        ]
        if self.verbosity >= NORMAL:
            self.stdout.write(u"Total broken unique links: {}\n".format(len(broken_links)))
            self.stdout.flush()

