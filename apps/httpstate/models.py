from django.db import models
from django.utils.translation import ugettext_lazy as _

verbose_name = _("HTTP State")

class HttpStateManager(models.Manager):
    def encode(self, httpstate_dict):
        """
        Returns the given httpstate dictionary pickled and encoded as a string.
        """
        return HttpStateStore().encode(httpstate_dict)

    def save(self, httpstate_key, httpstate_dict, expire_date):
        s = self.model(httpstate_key, self.encode(httpstate_dict), expire_date)
        if httpstate_dict:
            s.save()
        else:
            s.delete() # Clear httpstates with no data.
        return s


class HttpState(models.Model):
    """
    Django provides full support for anonymous httpstates. The httpstate
    framework lets you store and retrieve arbitrary data on a
    per-site-visitor basis. It stores data on the server side and
    abstracts the sending and receiving of cookies. Cookies contain a
    httpstate ID -- not the data itself.

    The Django httpstates framework is entirely cookie-based. It does
    not fall back to putting httpstate IDs in URLs. This is an intentional
    design decision. Not only does that behavior make URLs ugly, it makes
    your site vulnerable to httpstate-ID theft via the "Referer" header.

    For complete documentation on using HttpStates in your code, consult
    the httpstates documentation that is shipped with Django (also available
    on the Django website).
    """
    httpstate_key = models.CharField(_('httpstate key'), max_length=40,
                                   primary_key=True)
    httpstate_data = models.TextField(_('httpstate data'))
    expire_date = models.DateTimeField(_('expire date'))
    objects = HttpStateManager()

    class Meta:
        verbose_name = _('httpstate')
        verbose_name_plural = _('httpstates')

    def get_decoded(self):
        return HttpStateStore().decode(self.httpstate_data)
            
# At bottom to avoid circular import
from jetson.apps.httpstate.backends.db import HttpStateStore
