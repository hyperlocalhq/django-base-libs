# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig, apps

from base_libs.middleware import get_current_user


def create_notice_types(app, created_models, verbosity, **kwargs):
    from jetson.apps.notification import models as notification
    notification.create_notice_type(
        "institution_claimed",
        "Institution Claimed",
        "someone has claimed an institution/company as his own",
        default=0,
    )
    notification.create_notice_type(
        "institution_ownership_confirmed",
        "Institution Ownership Confirmed",
        "someone has been confirmed as the owner of an institution/company",
        default=2,
    )


def add_methods_to_institution():
    """Additional methods to Institution model"""
    Institution = apps.get_model("institutions", "Institution")

    def is_addable_to_favorites(self, user=None):
        if not hasattr(self, "_is_addable_to_favorites_cache"):
            from ccb.apps.site_specific.templatetags.browsing import get_context_item

            Favorite = apps.get_model("favorites", "Favorite")
            user = get_current_user(user)
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
            user = get_current_user(user)
            self._is_removable_from_favorites_cache = Favorite.objects.is_favorite(get_context_item(self), user)
        return self._is_removable_from_favorites_cache

    def is_addable_to_memos(self, user=None):
        if not hasattr(self, "_is_addable_to_memos_cache"):
            user = get_current_user(user)
            group = self._get_related_group()
            self._is_addable_to_memos_cache = not (
                group
                and group.get_owners().filter(user=user)
            )
        return self._is_addable_to_memos_cache

    def is_claimable(self, user=None):
        if not hasattr(self, "_is_claimable_cache"):
            user = get_current_user(user)
            group = self._get_related_group()
            self._is_claimable_cache = user and not (group and group.get_owners())
        return self._is_claimable_cache

    Institution.is_addable_to_favorites = is_addable_to_favorites
    Institution.is_removable_from_favorites = is_removable_from_favorites
    Institution.is_addable_to_memos = is_addable_to_memos
    Institution.is_claimable = is_claimable


class SiteSpecificConfig(AppConfig):
    name = "ccb.apps.site_specific"

    def ready(self):
        from django.db.models import signals
        from jetson.apps.notification import models as notification

        add_methods_to_institution()
        signals.post_migrate.connect(create_notice_types, sender=notification)
