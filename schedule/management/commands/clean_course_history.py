"""
    Delete course history older than 90 days
"""

from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from schedule.models import ClassOccurrence


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            reference_date = datetime.now() - timedelta(days=90)
            ClassOccurrence.objects.filter(date__lt=reference_date.date()).delete()
        except Exception as err:
            self.stdout.write(self.style.ERROR('An Error occured'))
            self.stdout.write(self.style.ERROR(str(err)))
            return

        self.stdout.write(self.style.SUCCESS('Successfully deleted old courses'))
        return
