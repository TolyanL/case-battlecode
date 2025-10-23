from django.core.management.base import BaseCommand

from battlecode.defaults import DefaultBadges

from badges.models import Badge


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Creating Badges
        badge_items = [Badge(**b) for b in DefaultBadges().ALL_BADGES]
        Badge.objects.bulk_create(badge_items, ignore_conflicts=True)
