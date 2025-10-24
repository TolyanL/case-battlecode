from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

from battlecode.groups import GROUPS


class Command(BaseCommand):
    def handle(self, *args, **options):
        created = 0

        for g in GROUPS:
            group, created = Group.objects.get_or_create(name=g.name)
            g.get_permissions()
            if not created:
                self.stdout.write(self.style.WARNING(f"Group {g.name} already exists"))
                continue

            group._meta.verbose_name = g.verbose_name
            group._meta.verbose_name_plural = g.verbose_name_plural

            group.permissions.set(g.get_permissions())

            group.save()
            created += 1

        if created > 0:
            self.stdout.write(self.style.SUCCESS(f"Created {created} groups"))
            return

        self.stdout.write(self.style.SUCCESS("No groups created"))
