# -*- coding: UTF-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group

def patch_auth():
    # Patch User model
    def auth_user_get_verbose(self):
        """
        this is used as a callback for admin list_filters.
        the returned value is used as the textual 
        representation in the Admin list_filters  
        """
        return "%s %s" % (self.last_name, self.first_name) 

    def related_label(self):
        # used by grappelli's autocomplete widget
        return (u"%s %s (%s)" % (self.first_name, self.last_name, self.username)).strip()

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "first_name__icontains", "last_name__icontains", "username__icontains",)

    User.get_verbose = auth_user_get_verbose
    User.related_label = related_label
    User._meta.one_to_one_field = None # why?
    User._meta.ordering = ('username',)
    
    # Patch Group model
    Group._meta.verbose_name = _("Role")
    Group._meta.verbose_name_plural = _("Roles")
    def display_users(group):
        links = []
        for user in group.user_set.all():
            links.append(
                """<a href="/admin/auth/user/%d">%s</a>""" % (
                    user.id,
                    ("%s %s" % (
                        user.first_name,
                        user.last_name,
                        )
                        ).strip() or user.username,
                    )
                )
        return "<br />".join(links)
    display_users.allow_tags = True
    display_users.short_description = _("Users")
    Group.display_users = display_users
   
patch_auth()
