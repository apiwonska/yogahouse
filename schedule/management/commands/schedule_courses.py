"""
    Schedule creation of courses. Courses will be added to schedule two weeks in advance
"""
from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand
from schedule.models import ClassOccurrence, Course


class Command(BaseCommand):

    def handle(self, *args, **options):
        weekdays = {
            1: "1_Poniedziałek",
            2: "2_Wtorek",
            3: "3_Środa",
            4: "4_Czwartek",
            5: "5_Piątek",
            6: "6_Sobota",
            7: "7_Niedziela"
        }

        try:
            weekday = weekdays[date.today().isoweekday()]
            date_today = datetime.now()
            time_delta = timedelta(days=14)
            date_scheduled = date_today + time_delta

            courses = Course.objects.filter(weekday=weekday)

            for course in courses:
                ClassOccurrence.objects.create(course=course, date=date_scheduled.date())

        except Exception as err:
            self.stdout.write(self.style.ERROR('An Error occured'))
            self.stdout.write(self.style.ERROR(str(err)))
            return

        self.stdout.write(self.style.SUCCESS('Successfully created courses'))
        return
