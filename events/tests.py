from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import resolve, reverse
from django.utils import timezone

from .factories import EventFactory, UserFactory
from .views import event_detail, event_list


class UrlsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.event = EventFactory()

    def test_events_url_resolves(self):
        url = reverse('events:events')
        self.assertEqual(resolve(url).func, event_list)

    def test_event_url_resolves(self):
        url = reverse('events:event', args=[self.event.pk])
        self.assertEqual(resolve(url).func, event_detail)


class ViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.event = EventFactory()

    def setUp(self):
        self.client = Client()

    def test_event_list(self):
        url = reverse('events:events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/base.html', 'event_list.html')

    def test_event_detail(self):
        url = reverse('events:event', args=[self.event.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'core/base.html', 'event_detail.html')


class EventTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.past_datetime = timezone.now() - timedelta(days=1)
        cls.current_datetime = timezone.now()
        cls.future_datetime = timezone.now() + timedelta(days=1)
        cls.user_0 = UserFactory()

    def test_object_name_is_title(self):
        event = EventFactory()
        self.assertEqual(str(event), event.title)

    def test_clean_date_start_is_not_in_the_past(self):
        event_0 = EventFactory.build(
            added_by=self.user_0, date_start=self.past_datetime)
        self.assertRaises(ValidationError, event_0.full_clean)
        try:
            event_0.full_clean()
        except ValidationError as error:
            self.assertEqual(error.message_dict, {'date_start': [
                             'Czas rozpoczęcia nie może być w przeszłości!']})

    def test_clean_date_end_is_not_before_date_start(self):
        event_0 = EventFactory.build(
            added_by=self.user_0, date_start=self.future_datetime, date_end=self.current_datetime)
        self.assertRaises(ValidationError, event_0.full_clean)
        try:
            event_0.full_clean()
        except ValidationError as error:
            self.assertEqual(error.message_dict, {'date_end': [
                             'Czas zakończenia nie może być wcześniejszy niż czas rozpoczęcia.']})
