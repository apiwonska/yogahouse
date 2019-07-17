from datetime import datetime, time, timedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import factory

from .models import ClassOccurrence, ClassType, Course, Teacher


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user_{n}')
    password = make_password("password")


class ClassTypeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ClassType

    name = factory.Sequence(lambda n: f'class type {n}')


class TeacherFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Teacher

    name = factory.Faker('name')


class CourseFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Course

    class_type = factory.SubFactory(ClassTypeFactory)
    teacher = factory.SubFactory(TeacherFactory)
    weekday = Course.DAYS_OF_WEEK[0][0]
    start_time = time(hour=9)
    duration = 55


class ClassOccurrenceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ClassOccurrence

    course = factory.SubFactory(CourseFactory)
    date = (datetime.now() + timedelta(days=1)).date()
