# -*- coding: UTF-8 -*-
from django.apps import apps
from django.db import connection, models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, AnonymousUser, Group, Permission
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
from django.db.models import signals

from base_libs.models.models import SysnameMixin
from base_libs.models.models import ObjectRelationMixin
from base_libs.models.fields import MultilingualCharField

verbose_name = _("Permissions")


class RowLevelPermissionManager(models.Manager):
    def create_row_level_permission(self, model_instance, owner, permission, negative=False):
        content_type = ContentType.objects.get_for_model(model_instance)
        if isinstance(permission, basestring):
            try:
                permission = Permission.objects.get(
                    codename=permission,
                    content_type=content_type,
                    )
            except Permission.DoesNotExist:
                from django.contrib.auth.management import create_permissions
                create_permissions(
                    apps.get_app(model_instance._meta.app_label),
                    created_models=None,
                    verbosity=0,
                    )
                permission = Permission.objects.get(
                    codename=permission,
                    content_type=content_type,
                    )
        if content_type != permission.content_type:
            raise TypeError, "Permission content type (%s) and object content type (%s) do not match" % (permission.content_type, content_type)
        object_id = model_instance._get_pk_val()
        row_lvl_perm = self.model(
            object_id=object_id,
            content_type=content_type,
            owner_object_id=owner._get_pk_val(),
            owner_content_type=ContentType.objects.get_for_model(owner),
            permission=permission,
            negative=negative,
            )
        row_lvl_perm.save()
        return row_lvl_perm

    def delete_row_level_permission(self, model_instance, owner, permission):
        content_type = ContentType.objects.get_for_model(model_instance)
        if isinstance(permission, basestring):
            permission = Permission.objects.get(
                codename=permission,
                content_type=content_type,
                )
        if content_type != permission.content_type:
            raise TypeError, "Permission content type (%s) and object content type (%s) do not match" % (permission.content_type, content_type)
        object_id = model_instance._get_pk_val()
        row_lvl_perm = self.get(
            object_id=object_id,
            content_type=content_type,
            owner_object_id=owner._get_pk_val(),
            owner_content_type=ContentType.objects.get_for_model(owner),
            permission=permission,
            )
        row_lvl_perm.delete()

    def create_default_row_permissions(self, model_instance, owner, change=True, delete=True, negChange=False, negDel=False):
        ret_dict = {}
        content_type = ContentType.objects.get_for_model(model_instance)
        if change:
            change_str = "change_%s" % (content_type.model)
            ret_dict[change_str] = self.create_row_level_permission(
                model_instance,
                owner,
                change_str,
                negative=negChange,
                )
        if delete:
            delete_str = "delete_%s" % (content_type.model)
            ret_dict[delete_str] = self.create_row_level_permission(
                model_instance,
                owner,
                delete_str,
                negative=negDel,
                )
        return ret_dict

    def get_model_list(self, user, model, perm):
        content_type = ContentType.objects.get_for_model(model)
        if isinstance(perm, basestring):
            perm = Permission.objects.get(
                codename__exact=perm,
                content_type=content_type,
                )
        user_model_ids = RowLevelPermission.objects.filter(
            owner_content_type=ContentType.objects.get_for_model(User),
            owner_object_id=user.id,
            permission=perm.id,
            content_type=content_type,
            ).values('object_id')
        id_list = [o['object_id'] for o in user_model_ids]
        user_group_list = [
            g['id']
            for g in user.groups.select_related().values('id')
            ]
        if user_group_list:
            group_model_ids = RowLevelPermission.objects.filter(
                owner_content_type=ContentType.objects.get_for_model(Group),
                owner_object_id__in=user_group_list,
                content_type=content_type,
                ).values('object_id')
            id_list = id_list + [o['object_id'] for o in group_model_ids]
        return id_list

RowLevelPermissionOwner = ObjectRelationMixin(
    is_required=True,
    prefix="owner",
    prefix_verbose=_("Owner"),
    add_related_name=True,
    )

class RowLevelPermission(ObjectRelationMixin(is_required=True), RowLevelPermissionOwner):
    """
    Similar to permissions but works on instances of objects instead of types.
    This uses generic relations to minimize the number of tables, and connects to the
    permissions table using a many to one relation.
    """
    negative = models.BooleanField(default=False)
    permission = models.ForeignKey(Permission)
    objects = RowLevelPermissionManager()

    class Meta:
        verbose_name = _('row level permission')
        verbose_name_plural = _('row level permissions')
        #unique_together = (('content_type', 'object_id', 'owner_object_id', 'owner_content_type', 'permission'),)
        db_table = "auth_rowlevelpermission"

    def __unicode__(self):
        return force_unicode("%s | %s:%s | %s:%s" % (
            self.permission,
            self.owner_content_type,
            self.owner_content_object,
            self.content_type,
            self.content_object,
            ))

    def delete(self):
        """
        print "row level perm is deleted:"
        print "-----------------"
        print "self.id = %s" % self.id
        print "-----------------"
        """ 
        super(RowLevelPermission, self).delete()
    delete.alters_data = True
        
class PerObjectGroup(ObjectRelationMixin(is_required=True), SysnameMixin(max_length=80)):
    """
    Similiar to auth.Group but works on instances of objects.
    This uses generic relations to minimize the number of tables, and connects
    to the permissions table using a many to many relation.
    """
    title = MultilingualCharField(_('title'), max_length=80)
    users = models.ManyToManyField(User, verbose_name=_('Users'), blank=True,
        help_text=_("In addition to the permissions manually assigned, these users will also get all row level permissions granted to this group."))
    
    class Meta:
        verbose_name = _('object-specific group')
        verbose_name_plural = _('object-specific groups')
        ordering = ('object_id', 'content_type')
        db_table = "auth_perobjectgroup"

    def get_title(self):
        return self.title
        
    def __unicode__(self):
        try:
            return u"%s | %s \"%s\"" % (force_unicode(self.get_title()), force_unicode(type(self.content_object)._meta.verbose_name), self.content_object)
        except:
            return self.title

### Additional functionality to all models
def add_functionality_to_models(sender, **kwargs):
    if getattr(sender, 'row_level_permissions', False):
        gen_rel = generic.GenericRelation(RowLevelPermission)
        sender.add_to_class("row_level_permissions", gen_rel)


### Additional methods to the User model
def add_methods_to_user():
    def get_group_permissions(self):
        """Returns a list of permission strings that this user has through his/her groups."""
        if not hasattr(self, '_group_perm_cache'):
            cursor = connection.cursor()
            # The SQL below works out to the following, after DB quoting:
            # cursor.execute("""
            #     SELECT ct."app_label", p."codename"
            #     FROM "auth_permission" p, "auth_group_permissions" gp, "auth_user_groups" ug, "django_content_type" ct
            #     WHERE p."id" = gp."permission_id"
            #         AND gp."group_id" = ug."group_id"
            #         AND ct."id" = p."content_type_id"
            #         AND ug."user_id" = %s, [self.id])
            quote_name = connection.ops.quote_name
            sql = """
                SELECT ct.%s, p.%s
                FROM %s p, %s gp, %s ug, %s ct
                WHERE p.%s = gp.%s
                    AND gp.%s = ug.%s
                    AND ct.%s = p.%s
                    AND ug.%s = %%s""" % (
                quote_name('app_label'),
                quote_name('codename'),
                quote_name('auth_permission'),
                quote_name('auth_group_permissions'),
                quote_name('auth_user_groups'),
                quote_name('django_content_type'),
                quote_name('id'),
                quote_name('permission_id'),
                quote_name('group_id'),
                quote_name('group_id'),
                quote_name('id'),
                quote_name('content_type_id'),
                quote_name('user_id'),
            )
            cursor.execute(sql, [self.id])
            self._group_perm_cache = set(
                ["%s.%s" % (row[0], row[1]) for row in cursor.fetchall()]
            )
        return self._group_perm_cache

    def get_all_permissions(self):
        if not hasattr(self, '_perm_cache'):
            self._perm_cache = set(
                [
                    "%s.%s" % (p.content_type.app_label, p.codename)
                    for p in self.user_permissions.select_related()
                ]
            )
            self._perm_cache.update(self.get_group_permissions())
        return self._perm_cache

    def check_row_level_permission(self, permission, obj):
        object_ct = ContentType.objects.get_for_model(obj)
        if type(permission).__name__ in ("str", "unicode"):
            try:
                permission = Permission.objects.get(
                    codename=permission,
                    content_type=object_ct.id,
                )
            except Permission.DoesNotExist:
                return False
        try:
            object_id = obj._get_pk_val()
            row_level_perm = self.row_level_permissions_owned.get(
                object_id=object_id,
                content_type=object_ct.id,
                permission=permission.id,
            )
        except RowLevelPermission.DoesNotExist:
            perms = self.check_per_object_group_permissions(permission, obj)
            if perms is not None:
                return perms
            else:
                return self.check_group_row_level_permissions(permission, obj)
        return not row_level_perm.negative

    def check_group_row_level_permissions(self, permission, obj):
        object_id = obj._get_pk_val()
        cursor = connection.cursor()
        quote_name = connection.ops.quote_name
        sql = """
            SELECT rlp.%s
            FROM %s ug, %s rlp
            WHERE rlp.%s = ug.%s
                AND ug.%s=%%s
                AND rlp.%s=%%s
                AND rlp.%s=%%s
                AND rlp.%s=%%s
                AND rlp.%s=%%s
                ORDER BY rlp.%s""" % (
            quote_name('negative'), quote_name('auth_user_groups'),
            quote_name('auth_rowlevelpermission'),
            quote_name('owner_object_id'), quote_name('group_id'),
            quote_name('user_id'), quote_name('owner_content_type_id'),
            quote_name('object_id'), quote_name('content_type_id'),
            quote_name('permission_id'), quote_name('negative')
        )
        cursor.execute(
            sql, [
                self.id,
                ContentType.objects.get_for_model(Group).id,
                object_id,
                ContentType.objects.get_for_model(obj).id,
                permission.id,
            ]
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return not row[0]

    def check_per_object_group_permissions(self, permission, obj):
        object_id = obj._get_pk_val()
        cursor = connection.cursor()
        quote_name = connection.ops.quote_name
        sql = """
            SELECT rlp.negative 
            FROM auth_rowlevelpermission rlp, auth_perobjectgroup_users gu
            WHERE rlp.owner_object_id = gu.perobjectgroup_id
                AND gu.user_id=%s
                AND rlp.owner_content_type_id=%s
                AND rlp.object_id=%s
                AND rlp.content_type_id=%s
                AND rlp.permission_id=%s
                ORDER BY rlp.negative"""
        cursor.execute(
            sql, [
                self.id,
                ContentType.objects.get_for_model(PerObjectGroup).id,
                object_id,
                ContentType.objects.get_for_model(obj).id,
                permission.id,
            ]
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return not row[0]

    def has_perm(self, perm, obj=None):
        """Returns True if the user has the specified permission."""
        if not self.is_active:
            return False
        if self.is_superuser:
            return True
        if obj and getattr(obj, "row_level_permissions", False):
            # Since we use the content type for row level perms, we don't need the application name.
            permission_str = perm[perm.index('.') + 1:]
            row_level_permission = self.check_row_level_permission(
                permission_str, obj
            )
            if row_level_permission is not None:
                return row_level_permission
        return perm in self.get_all_permissions()

    def contains_permission(self, perm, model=None):
        """
        This checks if the user has the given permission for any instance
        of the given model.
        """
        if self.has_perm(perm):
            return True
        if model and model._meta.row_level_permissions:
            perm = perm[perm.index('.') + 1:]
            return self.contains_row_level_perm(perm, model)
        return False

    def contains_row_level_perm(self, perm, model):
        content_type = ContentType.objects.get_for_model(model)
        if isinstance(perm, basestring):
            permission = Permission.objects.get(
                codename__exact=perm,
                content_type=content_type,
            )
        else:
            permission = perm
        count = self.row_level_permissions_owned.filter(
            content_type=content_type.id,
            permission=permission.id,
        ).count()
        if count > 0:
            return True
        return self.contains_group_row_level_perms(permission, content_type)

    def contains_group_row_level_perms(self, perm, ct):
        cursor = connection.cursor()
        quote_name = connection.ops.quote_name
        sql = """
            SELECT COUNT(*)
            FROM %s ug, %s rlp, %s ct
            WHERE rlp.%s = ug.%s
                AND ug.%s=%%s
                AND rlp.%s = %%s
                AND rlp.%s = %%s
                AND rlp.%s = %%s
                AND rlp.%s = %%s""" % (
            quote_name('auth_user_groups'),
            quote_name('auth_rowlevelpermission'),
            quote_name('django_content_type'), quote_name('owner_object_id'),
            quote_name('group_id'), quote_name('user_id'),
            quote_name('negative'), quote_name('owner_content_type_id'),
            quote_name('content_type_id'), quote_name('permission_id')
        )
        cursor.execute(
            sql, [
                self.id, False,
                ContentType.objects.get_for_model(Group).id, ct.id, perm.id
            ]
        )
        count = int(cursor.fetchone()[0])
        return count > 0

    def has_module_perms(self, app_label):
        """Returns True if the user has any permissions in the given app label."""
        if not self.is_active:
            return False
        if self.is_superuser:
            return True
        if [
            p
            for p in self.get_all_permissions() if p[:p.index('.')] == app_label
        ]:
            return True
        return self.has_module_row_level_perms(app_label)

    def has_module_row_level_perms(self, app_label):
        cursor = connection.cursor()
        quote_name = connection.ops.quote_name
        sql = """
            SELECT COUNT(*)
            FROM %s ct, %s rlp
            WHERE rlp.%s = ct.%s
                AND ct.%s=%%s
                AND rlp.%s = %%s
                AND rlp.%s = %%s
                AND rlp.%s = %%s
                """ % (
            quote_name('django_content_type'),
            quote_name('auth_rowlevelpermission'),
            quote_name('content_type_id'),
            quote_name('id'),
            quote_name('app_label'),
            quote_name('owner_content_type_id'),
            quote_name('owner_object_id'),
            quote_name('negative'),
        )
        cursor.execute(
            sql, [
                app_label,
                ContentType.objects.get_for_model(User).id, self.id, False
            ]
        )
        count = int(cursor.fetchone()[0])
        if count > 0:
            return True
        return self.has_module_group_row_level_perms(app_label)

    def has_module_group_row_level_perms(self, app_label):
        cursor = connection.cursor()
        quote_name = connection.ops.quote_name
        sql = """
            SELECT COUNT(*)
            FROM %s ug, %s rlp, %s ct
            WHERE rlp.%s = ug.%s
                AND ug.%s=%%s
                AND rlp.%s = ct.%s
                AND ct.%s=%%s
                AND rlp.%s = %%s
                AND rlp.%s = %%s""" % (
            quote_name('auth_user_groups'),
            quote_name('auth_rowlevelpermission'),
            quote_name('django_content_type'), quote_name('owner_object_id'),
            quote_name('group_id'), quote_name('user_id'),
            quote_name('content_type_id'), quote_name('id'),
            quote_name('app_label'), quote_name('negative'),
            quote_name('owner_content_type_id')
        )
        cursor.execute(
            sql, [
                self.id, app_label, False,
                ContentType.objects.get_for_model(Group).id
            ]
        )
        count = int(cursor.fetchone()[0])
        return count > 0

    User.contains_permission = contains_permission
    User.contains_row_level_perm = contains_row_level_perm
    User.contains_group_row_level_perms = contains_group_row_level_perms

    AnonymousUser.contains_permission = lambda perm, model=None: False
    AnonymousUser.contains_row_level_perm = lambda perm, model: False
    AnonymousUser.contains_group_row_level_perms = lambda perm, ct: False

    gen_rel = generic.GenericRelation(
        RowLevelPermission,
        object_id_field="owner_object_id",
        content_type_field="owner_content_type",
        #related_name="owner"
    )
    User.add_to_class("row_level_permissions_owned", gen_rel)


add_methods_to_user()

signals.class_prepared.connect(add_functionality_to_models)
