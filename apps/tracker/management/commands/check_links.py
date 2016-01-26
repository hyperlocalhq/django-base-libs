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

    def report_broken_links(self, obj, fields_with_broken_links):
        from django.db import models
        from base_libs.utils.misc import get_related_queryset

        Ticket = models.get_model("tracker", "Ticket")
        ContentType = models.get_model("contenttypes", "ContentType")
        User = models.get_model("auth", "User")
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
        if value.startswith("mailto:"):
            return True

        if value in self._checked_links:
            return self._checked_links[value]

        import urlparse
        import urllib2

        URL_VALIDATOR_USER_AGENT = 'Django (https://www.djangoproject.com/)'

        # If no URL path given, assume /
        if value and not urlparse.urlsplit(value)[2]:
            value += '/'
        headers = {
            "Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
            "Accept-Language": "en-us,en;q=0.5",
            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
            "Connection": "close",
            "User-Agent": URL_VALIDATOR_USER_AGENT,
        }
        try:
            req = urllib2.Request(value, None, headers)
            u = urllib2.urlopen(req)
            self._checked_links[value] = True
        except ValueError:
            self._checked_links[value] = False
        except Exception:  # urllib2.URLError, httplib.InvalidURL, etc.
            self._checked_links[value] = False
        return self._checked_links[value]

    def handle_noargs(self, **options):
        from django.db import models
        from django.apps import apps

        verbosity = int(options.get('verbosity', NORMAL))

        # 2-tuple of "app_name.model_name" and a callable returning the object to edit, if a link is broken
        models_to_check = (
            #("faqs.FaqCategory", (lambda o: o)),
            #("faqs.QuestionAnswer", (lambda o: o)),
            # ("articles.Article", (lambda o: o)),
            ("resources.Document", (lambda o: o)),
            # ("events.Event", (lambda o: o)),
            # ("people.IndividualContact", (lambda o: o.person)),
            # ("institutions.InstitutionalContact", (lambda o: o.institution)),
            # ("blog.Post", (lambda o: o)),
        )
        self._checked_links = {}

        # traverse models
        for app_model, get_obj in models_to_check:
            model = apps.get_model(*app_model.split("."))
            if verbosity > NORMAL:
                print "Checking %s model..." % model.__name__
            # traverse instances
            for el in model._default_manager.all():
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
                    if verbosity > NORMAL:
                        print "  %s" % el
                        for f, links in fields_with_broken_links:
                            print "    %s:" % force_unicode(f.verbose_name)
                            for link in links:
                                print "        %s" % link
                    self.report_broken_links(
                        get_obj(el),
                        fields_with_broken_links,
                    )
        if verbosity > NORMAL:
            print "Total unique links: %d" % len(self._checked_links)
        broken_links = [
            link
            for link in self._checked_links
            if not self._checked_links[link]
            ]
        if verbosity > NORMAL:
            print "Total broken unique links: %d" % len(broken_links)
