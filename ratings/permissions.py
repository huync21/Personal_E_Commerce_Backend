from rest_framework import permissions


class RatingApiPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == "create":
            return request.user.is_authenticated \
                   and request.user.is_verified \
                   and request.user.is_active
        else:
            return True
