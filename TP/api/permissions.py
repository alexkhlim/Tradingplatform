from rest_framework.permissions import BasePermission


class ProductPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='product').exists()


class HrPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='hr').exists()
