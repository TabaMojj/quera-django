from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        elif request.user.is_superuser or request.user == obj.owner:
            return True
        return False
