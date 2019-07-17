from datetime import datetime, timedelta

from django.contrib.auth.models import User
import factory
import pytz

from .models import Event


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User
    username = factory.Sequence(lambda n: f"user {n}")


class EventFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Event
    title = 'test title'
    place = 'test place'
    description = 'test description'
    added_by = factory.SubFactory(UserFactory)
    date_start = pytz.timezone(
        'Europe/Warsaw').localize(datetime.now() + timedelta(hours=1))
    date_end = pytz.timezone(
        'Europe/Warsaw').localize(datetime.now() + timedelta(days=1))
