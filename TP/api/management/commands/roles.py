from django.core.management.base import BaseCommand
from app.models import Office, Roles, PermissionType
from role_configuration import ROLES


class Command(BaseCommand):

    def handle(self, *args, **options):
        offices = Office.objects.all()
        for key_role_name in ROLES:
            model_name_permission_types = ROLES[key_role_name]
            for key_model_name in model_name_permission_types:
                permission_types = model_name_permission_types[key_model_name]
                for permission_type in permission_types:
                    PermissionType.objects.get_or_create(name=permission_type, model_name=key_model_name)
                for office in offices.iterator():
                    roles, created = Roles.objects.get_or_create(
                        role_name=key_role_name,
                        unit=office,
                    )
                    for permission_type in permission_types:
                        roles.permission_types.add(PermissionType.objects.get(name=permission_type, model_name=key_model_name))