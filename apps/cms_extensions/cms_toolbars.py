# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from cms.toolbar_pool import toolbar_pool
from cms.extensions.toolbar import ExtensionToolbar

from .models import OpenGraph


@toolbar_pool.register
class OpenGraphToolbar(ExtensionToolbar):
    # defines the model for the current toolbar
    model = OpenGraph

    def populate(self):
        # setup the extension toolbar with permissions and sanity checks
        current_page_menu = self._setup_extension_toolbar()
        # if it's all ok
        if current_page_menu and self.toolbar.edit_mode:
            # create a sub menu
            position = 0
            sub_menu = self._get_sub_menu(current_page_menu, 'submenu_label', _('Open Graph for Social Sharing'), position)
            # retrieves the instances of the current title extension (if any) and the toolbar item URL
            for lang_code, lang_name in settings.LANGUAGES:
                # cycle through the title list
                for title_extension, url in self.get_title_extension_admin(language=lang_code):
                    # this should be executed once for each language
                    # adds toolbar items
                    sub_menu.add_modal_item(lang_code, url=url, disabled=not self.toolbar.edit_mode)