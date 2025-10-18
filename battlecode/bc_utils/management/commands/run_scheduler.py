from django.core.management.base import BaseCommand
from utils.start_scheduler import start_jobs


class Command(BaseCommand):
    help = "Starts the scheduler"

    def handle(self, *args, **options):
        start_jobs()
