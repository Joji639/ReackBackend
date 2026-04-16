from rest_framework.permissions import BasePermission

class IsNotBlocked(BasePermission):
    def has_permission(self, request, view):
        return request.user.status != "blocked"