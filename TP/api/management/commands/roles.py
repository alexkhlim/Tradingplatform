import os

from django.core.management.base import BaseCommand
from app.models import Office, Roles, PermissionType
from data_for_base_command_django import ROLES


class Command(BaseCommand):

    def handle(self, *args, **options):
        data_role_name_dict = ROLES
        offices = Office.objects.all()
        for key in data_role_name_dict:
            role_name = key
            permission_types = data_role_name_dict[role_name].split(',')
            for permission_type in permission_types:
                PermissionType.objects.get_or_create(name=permission_type)
            for office in offices:
                roles = Roles.objects.get_or_create(
                    role_name=role_name,
                    unit=office
                )
                for permission_type in permission_types:
                    roles[0].permission_types.add(PermissionType.objects.get(name=permission_type))
