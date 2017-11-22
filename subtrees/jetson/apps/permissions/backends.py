# -*- coding: UTF-8 -*-
from django.db import connection
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, AnonymousUser, Group, Permission
from django.contrib.auth.backends import ModelBackend
from django.db import models
from django.conf import settings
from django.utils.encoding import force_text

RowLevelPermission = models.get_model("permissions", "RowLevelPermission")
PerObjectGroup = models.get_model("permissions", "PerObjectGroup")


def cast_to_int(field):
    # utility function for the database queries
    if "postgresql" in settings.DATABASES['default']['ENGINE']:
        return field + '::integer'
    return field


class RowLevelPermissionsBackend(ModelBackend):
    """
    Supplies per-object permission checking for django.contrib.auth.models.User
    """
    supports_object_permissions = True
    supports_anonymous_user = False
    
    def get_group_permissions(self, user_obj, obj=None):
        """
        Returns a set of permission strings that this user has through his/her
        groups.
        """
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
                quote_name('app_label'), quote_name('codename'),
                quote_name('auth_permission'), quote_name('auth_group_permissions'),
                quote_name('auth_user_groups'), quote_name('django_content_type'),
                quote_name('id'), quote_name('permission_id'),
                quote_name('group_id'), quote_name('group_id'),
                quote_name('id'), quote_name('content_type_id'),
                quote_name('user_id'),)
            cursor.execute(sql, [user_obj.id])
            user_obj._group_perm_cache = set(["%s.%s" % (row[0], row[1]) for row in cursor.fetchall()])
        return user_obj._group_perm_cache

    def get_all_permissions(self, user_obj, obj=None):
        if user_obj.is_anonymous():
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = set([u"%s.%s" % (p.content_type.app_label, p.codename) for p in user_obj.user_permissions.select_related()])
            user_obj._perm_cache.update(self.get_group_permissions(user_obj))
        return user_obj._perm_cache
        
    def has_perm(self, user_obj, perm, obj=None):
        """Returns True if the user has the specified permission."""
        if isinstance(user_obj, AnonymousUser):
            return False
        if obj and getattr(obj, "row_level_permissions", False):
            # Since we use the content type for row level perms, we don't need the application name.
            permission_str = perm[perm.index('.')+1:]
            row_level_permission = self.check_row_level_permission(user_obj, permission_str, obj)
            if row_level_permission is not None:
                return row_level_permission
        return perm in user_obj.get_all_permissions(obj)

    def has_module_perms(self, user_obj, app_label):
        """Returns True if the user has any permissions in the given app label."""
        if not user_obj.is_active:
            return False
        if user_obj.is_superuser:
            return True
        if [p for p in user_obj.get_all_permissions() if p[:p.index('.')] == app_label]:
            return True
        return self.has_module_row_level_perms(user_obj, app_label)
        
    def check_row_level_permission(self, user_obj, permission, obj):
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
            row_level_perm = user_obj.row_level_permissions_owned.get(
                object_id=object_id,
                content_type=object_ct.id,
                permission=permission.id,
                )
        except (RowLevelPermission.DoesNotExist, RowLevelPermission.MultipleObjectsReturned):
            perms = self.check_per_object_group_permissions(user_obj, permission, obj)
            if perms is not None:
                return perms
            else:
                return self.check_group_row_level_permissions(user_obj, permission, obj)
        return not row_level_perm.negative
    
    def check_group_row_level_permissions(self, user_obj, permission, obj):
        object_id = obj._get_pk_val()
        cursor = connection.cursor()
        quote_name = connection.ops.quote_name
        if "postgresql" in settings.DATABASES['default']['ENGINE']:
            sql = """
                SELECT rlp.%s
                FROM %s ug, %s rlp
                WHERE rlp.%s = ug.%s::text
                    AND ug.%s=%%s
                    AND rlp.%s=%%s
                    AND rlp.%s=%%s
                    AND rlp.%s=%%s
                    AND rlp.%s=%%s
                    ORDER BY rlp.%s""" % (
                quote_name('negative'), quote_name('auth_user_groups'),
                quote_name('auth_rowlevelpermission'), cast_to_int(quote_name('owner_object_id')),
                quote_name('group_id'), quote_name('user_id'),
                quote_name('owner_content_type_id'), cast_to_int(quote_name('object_id')),
                quote_name('content_type_id'), quote_name('permission_id'),
                quote_name('negative'))
        else:
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
                quote_name('auth_rowlevelpermission'), cast_to_int(quote_name('owner_object_id')),
                quote_name('group_id'), quote_name('user_id'),
                quote_name('owner_content_type_id'), cast_to_int(quote_name('object_id')),
                quote_name('content_type_id'), quote_name('permission_id'),
                quote_name('negative'))
        cursor.execute(sql, [
            user_obj.id,
            ContentType.objects.get_for_model(Group).id,
            force_text(object_id),
            ContentType.objects.get_for_model(obj).id,
            permission.id,])
        row = cursor.fetchone()
        if row is None:
            return None
        return not row[0]
    
    def check_per_object_group_permissions(self, user_obj, permission, obj):
        object_id = obj._get_pk_val()
        cursor = connection.cursor()
        quote_name = connection.ops.quote_name
        if "postgresql" in settings.DATABASES['default']['ENGINE']:
            sql = """
                SELECT rlp.negative 
                FROM auth_rowlevelpermission rlp, auth_perobjectgroup_users gu
                WHERE rlp.owner_object_id = gu.perobjectgroup_id::text
                    AND gu.user_id=%s
                    AND rlp.owner_content_type_id=%s
                    AND rlp.object_id=%s
                    AND rlp.content_type_id=%s
                    AND rlp.permission_id=%s
                    ORDER BY rlp.negative"""
        else:
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
        cursor.execute(sql, [
            user_obj.id,
            ContentType.objects.get_for_model(PerObjectGroup).id,
            force_text(object_id),
            ContentType.objects.get_for_model(obj).id,
            permission.id,])
        row = cursor.fetchone()
        if row is None:
            return None
        return not row[0]

    def has_module_row_level_perms(self, user_obj, app_label):
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
            quote_name('django_content_type'), quote_name('auth_rowlevelpermission'),
            quote_name('content_type_id'), quote_name('id'),
            quote_name('app_label'),
            quote_name('owner_content_type_id'),
            cast_to_int(quote_name('owner_object_id')),quote_name('negative'), )
        cursor.execute(sql, [app_label, ContentType.objects.get_for_model(User).id, user_obj.id, False])
        count = int(cursor.fetchone()[0])
        if count > 0:
            return True
        return self.has_module_group_row_level_perms(user_obj, app_label)

    def has_module_group_row_level_perms(self, user_obj, app_label):
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
            quote_name('auth_user_groups'), quote_name('auth_rowlevelpermission'),
            quote_name('django_content_type'), cast_to_int(quote_name('owner_object_id')),
            quote_name('group_id'), quote_name('user_id'),
            quote_name('content_type_id'), quote_name('id'),
            quote_name('app_label'), quote_name('negative'),
            quote_name('owner_content_type_id'))
        cursor.execute(sql, [user_obj.id, app_label, False, ContentType.objects.get_for_model(Group).id])
        count = int(cursor.fetchone()[0])
        return count>0
