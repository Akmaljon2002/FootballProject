from rest_framework.permissions import BasePermission


class RoleBasedPermission(BasePermission):
    allowed_roles = ["admin"]

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in self.allowed_roles