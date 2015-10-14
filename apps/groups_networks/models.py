# -*- coding: UTF-8 -*-

from django.utils.translation import ugettext_lazy as _

from jetson.apps.groups_networks.base import *

### PERSONGROUP MODIFICATION ###

class PersonGroup(PersonGroupBase):
    creative_sectors = TreeManyToManyField(
        Term,
        verbose_name=_("Creative sectors"),
        limit_choices_to={'vocabulary__sysname': 'categories_creativesectors'},
        related_name="creative_sectors_groups",
        blank=True,
    )

    def get_creative_sectors(self):
        return self.creative_sectors.all()


class GroupMembership(GroupMembershipBase):
    pass
