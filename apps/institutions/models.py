# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType

from actstream import action

from base_libs.utils.misc import get_related_queryset

from jetson.apps.institutions.base import *


### SITE-SPECIFIC INSTITUTION ###

class InstitutionManagerExtended(InstitutionManager):
    def latest_published_with_avatars(self):
        return self.latest_published().exclude(image="")


class Institution(InstitutionBase):
    creative_sectors = TreeManyToManyField(
        Term,
        verbose_name=_("Creative sectors"),
        limit_choices_to={'vocabulary__sysname': 'categories_creativesectors'},
        related_name="creative_sector_institutions",
        blank=True,
    )
    categories = TreeManyToManyField(
        Category,
        verbose_name=_("categories"),
        blank=True
    )

    objects = InstitutionManagerExtended()

    def create_default_group(self):
        PersonGroup = models.get_model("groups_networks", "PersonGroup")
        group = PersonGroup(
            title=self.title,
            slug=self.slug,
            group_type=get_related_queryset(PersonGroup, "group_type").get(
                sysname='institutional',
            ),
            access_type=get_related_queryset(PersonGroup, "access_type").get(
                sysname='secret_access',
            ),
        )
        group.content_object = self
        group.save()
        return group

    create_default_group.alters_data = True

    def get_representatives(self):
        """
        Returns the default owners of this object for permission manipulation
        """
        groups = self.get_groups()
        if not groups:
            groups = [self.create_default_group()]
        allowed_groups = []
        for person_group in groups:
            allowed_groups.append(
                person_group.perobjectgroup_set.get(sysname__startswith="owners")
            )
            allowed_groups.append(
                person_group.perobjectgroup_set.get(sysname__startswith="moderators")
            )
        return allowed_groups

    def get_owners(self):
        group = self._get_related_group()
        if group:
            return group.get_owners()
        return []

    def get_admin_links_to_owners(self):
        links = []
        for owner in self.get_owners():
            links.append("""<a href="/admin/people/person/%s/">%s</a>""" % (owner.id, owner.get_title()))
        return "<br /> ".join(links)

    get_admin_links_to_owners.allow_tags = True
    get_admin_links_to_owners.short_description = _("Owners")

    def get_groups(self):
        if not hasattr(self, "_groups_cache"):
            PersonGroup = models.get_model("groups_networks", "PersonGroup")
            ct = ContentType.objects.get_for_model(self)
            self._groups_cache = list(PersonGroup.objects.filter(
                content_type__pk=ct.id,
                object_id=self.id,
            ))
        return self._groups_cache

    def get_creative_sectors(self):
        return self.creative_sectors.all()

    def get_categories(self):
        return self.categories.all()

    def _get_current_user(self, user=None):
        if not user:
            from base_libs.middleware import get_current_user

            user = get_current_user()
        return user

    def _get_related_group(self):
        groups = self.get_groups()
        if groups:
            return groups[0]
        else:
            return None

    def is_addable_to_favorites(self, user=None):
        if not hasattr(self, "_is_addable_to_favorites_cache"):
            from ccb.apps.site_specific.templatetags.browsing import get_context_item

            Favorite = models.get_model("favorites", "Favorite")
            user = self._get_current_user(user)
            group = self._get_related_group()
            self._is_addable_to_favorites_cache = not (
                group
                and group.get_owners().filter(user=user)
            ) and not Favorite.objects.is_favorite(get_context_item(self), user)
        return self._is_addable_to_favorites_cache

    def is_removable_from_favorites(self, user=None):
        if not hasattr(self, "_is_removable_from_favorites_cache"):
            from ccb.apps.site_specific.templatetags.browsing import get_context_item

            Favorite = models.get_model("favorites", "Favorite")
            user = self._get_current_user(user)
            self._is_removable_from_favorites_cache = Favorite.objects.is_favorite(get_context_item(self), user)
        return self._is_removable_from_favorites_cache

    def is_addable_to_memos(self, user=None):
        if not hasattr(self, "_is_addable_to_memos_cache"):
            user = self._get_current_user(user)
            group = self._get_related_group()
            self._is_addable_to_memos_cache = not (
                group
                and group.get_owners().filter(user=user)
            )
        return self._is_addable_to_memos_cache

    def is_claimable(self, user=None):
        if not hasattr(self, "_is_claimable_cache"):
            user = self._get_current_user(user)
            group = self._get_related_group()
            self._is_claimable_cache = not group
        return self._is_claimable_cache

    def is_contactable(self, user=None):
        if not hasattr(self, "_is_contactable_cache"):
            user = self._get_current_user(user)
            group = self._get_related_group()
            contact_dict = self.get_primary_contact()
            self._is_contactable_cache = bool(not (
                group
                and group.get_owners().filter(user=user)
            ) and contact_dict.get("email0_address", False))
        return self._is_contactable_cache

    def is_email_displayed(self, user=None):
        if not hasattr(self, "_is_email_displayed_cache"):
            user = self._get_current_user(user)
            # group = self._get_related_group()
            self._is_email_displayed_cache = False
        return self._is_email_displayed_cache

    def is_phone_displayed(self, user=None):
        if not hasattr(self, "_is_phone_displayed_cache"):
            user = self._get_current_user(user)
            group = self._get_related_group()
            self._is_phone_displayed_cache = True
        return self._is_phone_displayed_cache

    def is_fax_displayed(self, user=None):
        if not hasattr(self, "_is_fax_displayed_cache"):
            user = self._get_current_user(user)
            group = self._get_related_group()
            self._is_fax_displayed_cache = True
        return self._is_fax_displayed_cache

    def is_mobile_displayed(self, user=None):
        if not hasattr(self, "_is_mobile_displayed_cache"):
            user = self._get_current_user(user)
            group = self._get_related_group()
            self._is_mobile_displayed_cache = True
        return self._is_mobile_displayed_cache

    def is_deletable(self, user=None):
        if not hasattr(self, "_is_deletable_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_deletable_cache = user.has_perm("institutions.delete_institution", self)
        return self._is_deletable_cache

    def save(self, *args, **kwargs):
        is_new = not self.id
        super(Institution, self).save(*args, **kwargs)
        if is_new:
            institution_added(Institution, self)

    save.alters_data = True


class InstitutionalContact(InstitutionalContactBase):
    def is_public(self):
        return self.institution.status in ("published", "published_commercial")


# Notify appropriate users about new institutions
def institution_added(sender, instance, **kwargs):
    from django.contrib.auth.models import User
    from base_libs.middleware import get_current_user
    from jetson.apps.notification import models as notification

    user = get_current_user()

    if user:
        action.send(user, verb="added institution", action_object=instance)
    else:
        action.send(instance, verb="was added")

    # TODO: fix this when re-enabling celery
    return

    creator_url = user.profile.get_url() if user else get_website_url() + "admin/"
    creator_title = user.profile.get_title() if user else ugettext("System")

    recipients = User.objects.all()

    notification.send(
        recipients,
        "institution_added",
        {
            "object_creator_url": creator_url,
            "object_creator_title": creator_title,
        },
        instance=instance,
        on_site=False,
    )

