# -*- coding: UTF-8 -*-

from django.apps import apps
from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

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
        "structure.Category",
        verbose_name=_("categories"),
        blank=True
    )
    completeness = models.SmallIntegerField(_("Completeness in %"), default=0)

    photo_author = models.CharField(_("Photo"), max_length=100, blank=True)

    objects = InstitutionManagerExtended()

    def get_url_path(self):
        try:
            path = reverse("member_detail", kwargs={'slug': self.slug})
        except:
            # the apphook is not attached yet
            return ""
        else:
            return path

    def ensure_default_person_group(self, lang_code=settings.LANGUAGE_CODE):
        PersonGroup = apps.get_model("groups_networks", "PersonGroup")
        GroupType = apps.get_model("groups_networks", "GroupType")
        Language = apps.get_model("i18n", "Language")
        ct = ContentType.objects.get_for_model(self)
        group_type, group_type_created = GroupType.objects.get_or_create(
            slug="institutional",
            defaults={
                'title_de': "Institutional",
                'title_en': "Institutional",
            },
        )
        group, group_created = PersonGroup.objects.get_or_create(
            content_type=ct,
            object_id=self.pk,
            group_type=group_type,
            access_type="secret",
            defaults={
                'title': self.title,
                'slug': self.slug,
                'is_by_confirmation': True,
            },
        )
        if group_created:
            language, _language_created = Language.objects.get_or_create(
                iso2_code=lang_code,
            )
            group.preferred_language = language
            group.save()
        elif group.title != self.title:  # update group title, if institution's title has changed
            group.title = self.title
            group.slug = self.slug
            group.save()

        return group

    ensure_default_person_group.alters_data = True

    def get_object_permission_roles(self):
        """
        Returns the default permission owners of this object for permission manipulation
        """
        groups = self.get_groups()
        if not groups:
            groups = [self.ensure_default_person_group()]
        allowed_groups = []
        for person_group in groups:
            allowed_groups.append(
                person_group.perobjectgroup_set.get(sysname__startswith="owners")
            )
            allowed_groups.append(
                person_group.perobjectgroup_set.get(sysname__startswith="moderators")
            )
        return allowed_groups

    get_object_permission_roles.alters_data = True

    def set_owner(self, person):
        GroupMembership = apps.get_model("groups_networks", "GroupMembership")
        if person.preferred_language:
            lang_code = person.preferred_language.iso2_code
        else:
            lang_code = get_current_language()
        group = self.ensure_default_person_group(lang_code=lang_code)

        current_user = get_current_user()
        GroupMembership.objects.get_or_create(
            user=person.user,
            person_group=group,
            role="owners",
            is_accepted=True,
            defaults={
                'inviter': current_user,
                'confirmer': current_user,
            },
        )
        return True

    set_owner.alters_data = True

    def remove_owner(self, person):
        from django.apps import apps
        GroupMembership = apps.get_model("groups_networks", "GroupMembership")
        group = self.ensure_default_person_group()

        memberships = GroupMembership.objects.filter(
            user=person.user,
            person_group=group,
            role="owners",
        )

        if memberships.count():
            memberships.delete()
            return True
        return False

    remove_owner.alters_data = True

    def get_owners(self):
        group = self.ensure_default_person_group()
        if group:
            return group.get_owners()
        return []

    def get_groups(self):
        if not hasattr(self, "_groups_cache"):
            PersonGroup = apps.get_model("groups_networks", "PersonGroup")
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

            Favorite = apps.get_model("favorites", "Favorite")
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

            Favorite = apps.get_model("favorites", "Favorite")
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

    def is_editable(self, user=None):
        if not hasattr(self, "_is_editable_cache"):
            user = get_current_user(user) or AnonymousUser()
            self._is_editable_cache = user.has_perm("institutions.change_institution", self)
        return self._is_editable_cache

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

    def calculate_completeness(self):
        progress = 0
        if self.title:
            progress += 25
        if self.image:
            progress += 25
        if self.description:
            progress += 25
        if self.institutionalcontact_set.count():
            progress += 25
        self.completeness = progress

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains",)


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

    creator_url = user.profile.get_url() if user else get_website_url() + "admin/"
    creator_title = user.profile.get_title() if user else ugettext("System")

    recipients = User.objects.filter(is_staff=True, is_active=True)

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
