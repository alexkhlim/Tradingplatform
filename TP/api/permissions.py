from rest_framework.permissions import BasePermission

from rest_framework import serializers
from app.models import *


class ProductPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='product').exists()


class HrPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.groups.filter(name='hr').exists()


class HasAction(BasePermission):
    def has_object_permission(self, request, view, obj):
        pass


def has_action_hr(user, office, item, role='hr', permission_type='can_update'):
    role = Roles.objects.get(role_name=role)
    if role.users.filter(username=user.username).exists() and office.item.filter(name=item.name).exists() \
            and role.permission_types.filter(name=permission_type).exists():
        return True
    elif user.is_superuser:
        return True
    return False


def has_action_product(user, role='product', permission_type='can_create'):
    role = Roles.objects.get(role_name=role)
    if role.users.filter(username=user.username).exists() and role.permission_types.filter(
            name=permission_type).exists():
        return True
    elif user.is_superuser:
        return True
    return False


def has_action(user, office='', item='', model_name='', permission_type=''):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if item and not office.item.filter(id=item.id).exists():
        return False

    if office:
        roles = user.user_roles.filter(
            unit=office,
            permission_types__in=PermissionType.objects.filter(
                name=permission_type,
                model_name=model_name
            )
        )
    else:
        roles = user.user_roles.filter(
            permission_types__in=PermissionType.objects.filter(
                name=permission_type,
                model_name=model_name
            )
        )

    return roles.exists()


class OfferValidation:
    @staticmethod
    def checking_number_items(quantity, entry_quantity, offer_type):
        if quantity < entry_quantity and offer_type == Offer.SALE:
            raise serializers.ValidationError('Not enough item')

    @staticmethod
    def decrease_items(offer_type, user_inventory, entry_quantity):
        if offer_type == Offer.SALE:
            user_inventory.quantity -= entry_quantity
            user_inventory.save(update_fields=('quantity',))
