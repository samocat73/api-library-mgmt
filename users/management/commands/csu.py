from django.core.management.base import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = CustomUser.objects.create_user(username="admin", password="1234")
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
