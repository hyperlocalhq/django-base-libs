from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from jetson.apps.location.models import Address, Locality, Geoposition

class Locality_Inline(admin.StackedInline):
    model = Locality
    extra = 1

class Geoposition_Inline(admin.StackedInline):
    model = Geoposition
    extra = 1

class AddressOptions(admin.ModelAdmin):
    inlines = [Locality_Inline, Geoposition_Inline]
    save_on_top = True

admin.site.register(Address, AddressOptions)

