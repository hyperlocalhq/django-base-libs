# -*- coding: UTF-8 -*-
import re
from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.utils.encoding import force_unicode, smart_str

SILENT, NORMAL, VERBOSE = 0, 1, 2

url_regex = re.compile(
    r"^(?#Protocol)(?:(?:ht|f)tp(?:s?)\:\/\/|~/|/)?"
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
        description.append("\nYou can fix the links here:")
        description.append(self.get_admin_link(obj))

        superuser = User.objects.filter(is_superuser=True)[0]
        t, created = Ticket.objects.get_or_create(
            concern=concern,
            description=u"\n".join(description),
            url=self.get_admin_link(obj),
            submitter=superuser,
            submitter_name=superuser.username,
            submitter_email=superuser.email,
        )
    
    def get_admin_link(self, obj):
        from base_libs.utils.misc import get_website_url
        if hasattr(obj, "get_admin_link"):
            return obj.get_admin_link()
        else:
            return "%sadmin/%s/%s/%s/" % (
                get_website_url(),
                obj._meta.app_label.lower(),
                type(obj).__name__.lower(),
                obj.pk,
            )

    def is_valid_link(self, url):
        import requests

        if url.startswith("mailto:"):
            return True
            
        if url in self._checked_links:
            return self._checked_links[url]

        self._checked_links[url] = False
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',  # User agent of Chrome
        }
        try:
            response = requests.head(url, allow_redirects=True, headers=headers, verify=False)
            if response.status_code == 200:
                self._checked_links[url] = True
        except requests.ConnectionError as err:
            pass
        except requests.TooManyRedirects as err:
            pass

        return self._checked_links[url]
    
    def handle_noargs(self, **options):
        self.verbosity = int(options.get('verbosity', NORMAL))
        self._checked_links = {}
        self.check_django_cms(**options)
        self.check_other_models(**options)
        if self.verbosity > NORMAL:
            print "Total unique links: %d" % len(self._checked_links)
        broken_links = [
            link
            for link in self._checked_links
            if not self._checked_links[link]
        ]
        if self.verbosity > NORMAL:
            print "Total broken unique links: %d" % len(broken_links)

    def check_django_cms(self, **options):
        from django.db import models
        from cms.models import Page

        if self.verbosity > NORMAL:
            print "Checking CMS pages..."

        for p in Page.objects.filter(publisher_is_draft=False):
            fields_with_broken_links = []
            for ph in p.placeholders.all():
                for pl in ph.get_plugins_list():
                    pl_instance = pl.get_plugin_instance()[0]

                    if not pl_instance:
                        continue

                    # traverse fields
                    for f in pl_instance._meta.fields:
                        broken_links_in_field = []
                        if isinstance(f, models.URLField):
                            # check the value of URLField
                            m = url_regex.match(getattr(pl_instance, f.name) or "")
                            if m:
                                is_valid = self.is_valid_link(m.group(0))
                                if not is_valid:
                                    broken_links_in_field.append(m.group(0))
                        elif isinstance(f, models.TextField) and not type(f).__name__.startswith("Multilingual"):
                            matches = a_link_regex.findall(getattr(pl_instance, f.name) or "")
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
                if self.verbosity > NORMAL:
                    print "  %s" % smart_str(p.get_title())
                    for f, links in fields_with_broken_links:
                        print "    %s:" % smart_str(force_unicode(f.verbose_name))
                        for link in links:
                            print "        %s" % link
                self.report_broken_links(
                    p,
                    fields_with_broken_links,
                )

    def check_other_models(self, **options):
        from django.db import models

        # 2-tuple of "app_name.model_name" and a callable returning the object to edit, if a link is broken
        models_to_check = (
            ("museums.Museum", (lambda o: o), {'status': 'published'}),
            ("exhibitions.Exhibition", (lambda o: o), {'status': 'published'}),
            ("events.Event", (lambda o: o), {'status': 'published'}),
            ("workshops.Workshop", (lambda o: o), {'status': 'published'}),
            ("shop.ShopProduct", (lambda o: o), {'status': 'published'}),
            #("institutions.InstitutionalContact", (lambda o: o.institution), {'status': 'published'}),
            #("blog.Post", (lambda o: o), {'status': 'published'}),
        )

        # traverse models
        for app_model, get_obj, filter_params in models_to_check:
            model = models.get_model(*app_model.split("."))
            if self.verbosity > NORMAL:
                print "Checking %s model..." % model.__name__
            # traverse instances
            for el in model._default_manager.filter(**filter_params):
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
                    if self.verbosity > NORMAL:
                        print "  %s" % smart_str(el)
                        for f, links in fields_with_broken_links:
                            print "    %s:" % smart_str(force_unicode(f.verbose_name))
                            for link in links:
                                print "        %s" % link
                    self.report_broken_links(
                        get_obj(el),
                        fields_with_broken_links,
                    )
