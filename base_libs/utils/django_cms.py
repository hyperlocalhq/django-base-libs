try:
    from cms.cms_toolbars import PageToolbar
    from cms.utils import page_permissions
except ModuleNotFoundError:
    pass
else:
    def guerilla_patch_has_publish_permission():
        """
        Up until March 2021, django-cms 3.7.4, this is still an issue.
        https://github.com/django-cms/django-cms/issues/6433
        This patch fixes the dissapearance of the "Publish page changes"
        blue button in the upper right corner.
        """

        def has_publish_permission(self):
            is_has_publish_permission = False

            is_page_model_available = self.page is not None
            if is_page_model_available:
                is_has_publish_permission = (
                    page_permissions.user_can_publish_page(
                        self.request.user,
                        page=self.page,
                        site=self.current_site,
                    )
                )

            is_need_to_check_dirty_static_placeholders_perms = (
                is_has_publish_permission or not is_page_model_available
            ) and self.statics
            if is_need_to_check_dirty_static_placeholders_perms:
                is_has_publish_permission = all(
                    sp.has_publish_permission(self.request)
                    for sp in self.dirty_statics
                )

            return is_has_publish_permission

        return has_publish_permission

    PageToolbar.has_publish_permission = (
        guerilla_patch_has_publish_permission()
    )
