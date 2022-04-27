from rest_framework import permissions


class OrderAPIPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated \
               and request.user.is_active \
               and request.user.is_verified


class ShipmentAPIPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return True
