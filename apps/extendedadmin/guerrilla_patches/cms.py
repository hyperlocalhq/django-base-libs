# Let's guerrilla-patch the UserSelectAdminWidget which lacks of closing </a> tag
from cms.models import PageUser, get_permission_codename, admin_reverse, mark_safe
from cms.forms.widgets import UserSelectAdminWidget

def userselectadminwidget_render(self, name, value, attrs=None, choices=()):
    output = [super(UserSelectAdminWidget, self).render(name, value, attrs)]
    if hasattr(self, 'user') and (self.user.is_superuser or
        self.user.has_perm(PageUser._meta.app_label + '.' + get_permission_codename('add', PageUser._meta))):
        # append + icon
        add_url = admin_reverse('cms_pageuser_add')
        output.append(u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"></a>' % \
                (add_url, name))
    return mark_safe(u''.join(output))

UserSelectAdminWidget.render = userselectadminwidget_render