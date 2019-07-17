from django.test import Client, TestCase
from django.urls import resolve, reverse

from .views import home


class UrlsTest(TestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)


class ViewsTest(TestCase):

    def test_home(self):
        client = Client()
        url = reverse('home')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/base.html', 'core/home.html')
