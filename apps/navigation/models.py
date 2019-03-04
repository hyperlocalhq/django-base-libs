# -*- coding: UTF-8 -*-
import re
import operator

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.utils.functional import lazy
from django.utils.encoding import force_unicode
from django.conf import settings

from base_libs.models.models import ObjectRelationMixin
from base_libs.models.models import SingleSiteMixin
from base_libs.models.models import HierarchyMixin
from base_libs.models.models import SysnameMixin
from base_libs.models.fields import MultilingualCharField
from base_libs.models.fields import MultilingualTextField

from base_libs.models.fields import PlainTextModelField
from base_libs.middleware import get_current_user

from mptt.models import MPTTModel
from mptt.managers import TreeManager
from mptt.fields import TreeForeignKey

verbose_name = _("Navigation")

LINKABLE_MODELS = getattr(settings, "LINKABLE_MODELS", (
    "flatpages.Flatpage",
    ))

def get_ct_filtering(LINKABLE_MODELS):
    filtering = []
    for el in LINKABLE_MODELS:
        app_label, model = el.lower().split(".")
        filtering.append(models.Q(app_label=app_label, model=model))
    return reduce(operator.or_, filtering)
    
LinkedObjectMixin = ObjectRelationMixin(
    is_required=False,
    limit_content_type_choices_to=get_ct_filtering(LINKABLE_MODELS), 
    prefix_verbose=_("Linked object"), 
    )

class NavigationLink(MPTTModel, SingleSiteMixin, LinkedObjectMixin, SysnameMixin(help_text=_("Do not change this value! Sysnames are used to display tree branches of navigation links in templates. Also they are used for binding specific styling or scripts to specific navigation items."))):
    sort_order = models.IntegerField(
        _("sort order"), 
        blank=True,
        editable=False,
        default=0,
    )
    parent = TreeForeignKey(
       'self',
       #related_name="%(class)s_children",
       related_name="child_set",
       blank=True,
       null=True,
    )
    
    title = MultilingualCharField(_('title'), max_length=255)
    link_url = models.CharField(_("Link URL"), max_length=255, blank=True, help_text=_("It can contain template tags and variables. The link is shown in the navigation menu only if it returns a non-empty string."))
    related_urls = PlainTextModelField(_("Related URLs"), blank=True, help_text=_("Other URLs for which this link should be highlighted, one per line. It can contain template tags and variables."))
    is_group = models.BooleanField(_("Group of links"), default=False)
    is_group_name_shown = models.BooleanField(_("Show group name"), default=True)
    is_shown_for_visitors = models.BooleanField(_("Shown for visitors"), default=True)
    is_shown_for_users = models.BooleanField(_("Shown for users"), default=True)
    is_login_required = models.BooleanField(_("Require login"), default=False)
    is_promoted = models.BooleanField(_("Promoted"), default=False)
    description = MultilingualTextField(_('description'), blank=True)
    
    objects = TreeManager()
    
    class Meta:
        verbose_name = _("navigational menu item")
        verbose_name_plural = _("navigational menu items")
        ordering = ["tree_id", "lft"]

    class MPTTMeta:
        order_insertion_by = ['sort_order']
        
    def __unicode__(self):
        return self.title
    __unicode__.admin_order_field = 'lft'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            NavigationLink.objects.insert_node(self, self.parent)
        super(NavigationLink, self).save(*args, **kwargs)
    
    def get_title(self):
        return self.title
        
    def get_description(self, language=None):
        return self.description
        
    def get_related_urls(self):
        related_urls = re.sub(r"\s*\n\s*", "\n", self.related_urls).strip()
        if related_urls:
            return related_urls.split("\n")
        else:
            return []
        
    def get_children_for_current_user(self):
        user = get_current_user()
        if user:
            return self.get_children_for_authenticated_user()
        return self.get_children_for_anonymous_user()

    def get_children_for_authenticated_user(self):
        if not hasattr(self, "_children_for_authenticated_user"):
            self._children_for_authenticated_user = self.get_children().filter(
                models.Q(site__isnull=True) | models.Q(site__pk=settings.SITE_ID),
                is_shown_for_users=True,
                )
        return self._children_for_authenticated_user
        
    def get_children_for_anonymous_user(self):
        if not hasattr(self, "_children_for_anonymous_user"):
            self._children_for_anonymous_user = self.get_children().filter(
                models.Q(site__isnull=True) | models.Q(site__pk=settings.SITE_ID),
                is_shown_for_visitors=True,
                )
        return self._children_for_anonymous_user        

