from rest_framework import permissions
from django.contrib.auth.models import Group


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir que solo los propietarios de un objeto lo editen.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner.
        return obj.owner == request.user


def _is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


def _has_group_permission(user, required_groups):
    return any([_is_in_group(user, group_name) for group_name in required_groups])


class IsAdmin(permissions.BasePermission):
    # group_name for super admin
    required_groups = ['admin']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(
            request.user, self.required_groups)
        return request.user and has_group_permission


class IsAdminOrUser(permissions.BasePermission):
    required_groups = ['admin', 'user', 'anonymous']

    def has_permission(self, request, view):
        is_anonymous = _is_in_group(request.user, 'anonymous')
        if is_anonymous and request.method not in permissions.SAFE_METHODS:
            return False

        has_group_permission = _has_group_permission(
            request.user, self.required_groups)
        return request.user and has_group_permission


class IsUser(permissions.BasePermission):
    required_groups = ['user']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(
            request.user, self.required_groups)
        return request.user and has_group_permission
