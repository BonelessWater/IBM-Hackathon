from django.core.management.base import BaseCommand
from playground.utils import fetch_and_log_emails

class Command(BaseCommand):
    help = 'Fetch and log emails every 5 minutes'

    def handle(self, *args, **kwargs):
        fetch_and_log_emails()
        self.stdout.write(self.style.SUCCESS('Successfully logged emails'))
