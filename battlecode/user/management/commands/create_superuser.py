import os

from dotenv import load_dotenv

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, User

from battlecode.groups import ADMIN_GROUP


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_dotenv()

        try:
            group = Group.objects.get(name=ADMIN_GROUP)
        except Group.DoesNotExist:
            raise CommandError("admin group does not exist. Run create_user_groups first")
        except Exception as e:
            raise CommandError(e)

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not all([username, email, password]):
            raise CommandError("Error: missing environment variables for superuser creation.")

        if not User.objects.filter(username=username, email=email).exists():
            u = User.objects.create_superuser(username=username, email=email, password=password)
            u.groups.add(group)
            self.stdout.write(self.style.SUCCESS("Superuser created successfully."))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser {username} already exists."))
