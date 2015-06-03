import base64
import cPickle as pickle

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils.hashcompat import md5_constructor

verbose_name = _("HTTP State")

class HttpStateManager(models.Manager):
    def encode(self, httpstate_dict):
        """
        Returns the given httpstate dictionary pickled and encoded as a string.
        """
        pickled = pickle.dumps(httpstate_dict)
        pickled_md5 = md5_constructor(pickled + settings.SECRET_KEY).hexdigest()
        return base64.encodestring(pickled + pickled_md5)

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
        encoded_data = base64.decodestring(self.httpstate_data)
        pickled, tamper_check = encoded_data[:-32], encoded_data[-32:]
        if md5_constructor(pickled + settings.SECRET_KEY).hexdigest() != tamper_check:
            from django.core.exceptions import SuspiciousOperation
            raise SuspiciousOperation, "User tampered with httpstate cookie."
        try:
            return pickle.loads(pickled)
        # Unpickling can cause a variety of exceptions. If something happens,
        # just return an empty dictionary (an empty httpstate).
        except:
            return {}
