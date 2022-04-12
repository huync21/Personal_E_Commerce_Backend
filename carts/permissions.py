from rest_framework import permissions


class CartAPIPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated \
               and request.user.is_verified \
               and request.user.is_active
