import os

from django.core.management.base import BaseCommand
from app.models import Office, Roles, PermissionType
from data_for_base_command_django import ROLES


class Command(BaseCommand):

    def handle(self, *args, **options):
        data_role_name_dict = ROLES
        offices = Office.objects.all()
        for key_role_name in data_role_name_dict:
            role_name = key_role_name
            model_name_permission_types = data_role_name_dict[role_name]
            for key_model_name in model_name_permission_types:
                model_name = key_model_name
                permission_types = model_name_permission_types[model_name]
                for permission_type in permission_types:
                    PermissionType.objects.get_or_create(name=permission_type, model_name=model_name)
                for office in offices:
                    roles = Roles.objects.get_or_create(
                        role_name=role_name,
                        unit=office
                    )
                    for permission_type in permission_types:
                        roles[0].permission_types.add(PermissionType.objects.get(name=permission_type, model_name=key_model_name))
