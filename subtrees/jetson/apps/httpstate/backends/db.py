from datetime import datetime

from django.core.exceptions import SuspiciousOperation
from django.db import IntegrityError, transaction, router
try:
    from django.utils.timezone import now as tz_now
except:
    tz_now = datetime.now

from jetson.apps.httpstate.backends.base import HttpStateBase, CreateError

class HttpStateStore(HttpStateBase):
    """
    Implements database httpstate store.
    """
    def __init__(self, httpstate_key=None):
        super(HttpStateStore, self).__init__(httpstate_key)

    def load(self):
        try:
            s = HttpState.objects.get(
                httpstate_key = self.httpstate_key,
                expire_date__gt=tz_now()
            )
            return self.decode(s.httpstate_data)
        except (HttpState.DoesNotExist, SuspiciousOperation):
            self.create()
            return {}

    def exists(self, httpstate_key):
        HttpState.objects.filter(httpstate_key=httpstate_key).exists()

    def create(self):
        while True:
            self._httpstate_key = self._get_new_httpstate_key()
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
            httpstate_key = self._get_or_create_httpstate_key(),
            httpstate_data = self.encode(self._get_httpstate(no_load=must_create)),
            expire_date = self.get_expiry_date()
        )
        using = router.db_for_write(HttpState, instance=obj)
        sid = transaction.savepoint(using=using)
        try:
            obj.save(force_insert=must_create, using=using)
        except IntegrityError:
            if must_create:
                transaction.savepoint_rollback(sid, using=using)
                raise CreateError
            raise

    def delete(self, httpstate_key=None):
        if httpstate_key is None:
            if self.httpstate_key is None:
                return
            httpstate_key = self.httpstate_key
        try:
            HttpState.objects.get(httpstate_key=httpstate_key).delete()
        except HttpState.DoesNotExist:
            pass

    @classmethod
    def clear_expired(cls):
        HttpState.objects.filter(expire_date__lt=tz_now()).delete()
        transaction.commit_unless_managed()

# At bottom to avoid circular import        
from jetson.apps.httpstate.models import HttpState
