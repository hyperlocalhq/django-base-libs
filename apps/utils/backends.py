from django.conf import settings
from django.contrib.auth.models import User, check_password

class EmailBackend:
    """
    Authenticate against email and password or email only (from hash)
    """

    def __init__(self):
        pass

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False
    
    def authenticate(self, email=None, password=None):
        user = None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            if password is not None:
                if not check_password(password, user.password):
                    user = None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

