from django.utils.encoding import force_str


def get_user_title(user):
    """ Returns user's first and last name or username or nickname """
    profile = getattr(user, "profile", None)
    if profile:
        return force_str(profile)
    return user.get_full_name() or user.username
