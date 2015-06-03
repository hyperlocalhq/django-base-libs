import datetime

from django.core.exceptions import SuspiciousOperation
from django.db import IntegrityError, transaction
from django.utils.encoding import force_unicode

from jetson.apps.httpstate.models import HttpState
from jetson.apps.httpstate.backends.base import HttpStateBase, CreateError

class HttpStateStore(HttpStateBase):
    """
    Implements database httpstate store.
    """
    def load(self):
        try:
            s = HttpState.objects.get(
                httpstate_key = self.httpstate_key,
                expire_date__gt=datetime.datetime.now()
            )
            return self.decode(force_unicode(s.httpstate_data))
        except (HttpState.DoesNotExist, SuspiciousOperation):
            self.create()
            return {}

    def exists(self, httpstate_key):
        try:
            HttpState.objects.get(httpstate_key=httpstate_key)
        except HttpState.DoesNotExist:
            return False
        return True

    def create(self):
        while True:
            self.httpstate_key = self._get_new_httpstate_key()
            try:
                # Save immediately to ensure we have a unique entry in the
                # database.
                self.save(must_create=True)
            except CreateError:
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            self._httpstate_cache = {}
            return

    def save(self, must_create=False):
        """
        Saves the current httpstate data to the database. If 'must_create' is
        True, a database error will be raised if the saving operation doesn't
        create a *new* entry (as opposed to possibly updating an existing
        entry).
        """
        obj = HttpState(
            httpstate_key = self.httpstate_key,
            httpstate_data = self.encode(self._get_httpstate(no_load=must_create)),
            expire_date = self.get_expiry_date()
        )
        sid = transaction.savepoint()
        try:
            obj.save(force_insert=must_create)
        except IntegrityError:
            if must_create:
                transaction.savepoint_rollback(sid)
                raise CreateError
            raise

    def delete(self, httpstate_key=None):
        if httpstate_key is None:
            if self._httpstate_key is None:
                return
            httpstate_key = self._httpstate_key
        try:
            HttpState.objects.get(httpstate_key=httpstate_key).delete()
        except HttpState.DoesNotExist:
            pass
