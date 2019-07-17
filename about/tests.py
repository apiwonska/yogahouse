from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import resolve, reverse

from .models import AboutInfo, Teacher
from .views import about


class UrlsTest(TestCase):

    def test_about_url_resolves(self):
        url = reverse('about:about')
        self.assertEqual(resolve(url).func, about)


class ViewsTest(TestCase):

    def test_about(self):
        client = Client()
        url = reverse('about:about')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about/about.html')


class AboutInfoTest(TestCase):

    def test_about_info_one_instance_allowed(self):
        '''It should not be possible to save second instance'''
        about_info_0 = AboutInfo.objects.create()
        about_info_1 = AboutInfo()
        self.assertRaises(ValidationError, about_info_1.full_clean)

    def test_object_name(self):
        '''Object name should be "Prezentacja"'''
        about_info = AboutInfo.objects.create()
        self.assertEqual(str(about_info), "Prezentacja")


class TeacherTest(TestCase):

    def test_object_name_is_name(self):
        teacher = Teacher.objects.create()
        self.assertEqual(str(teacher), teacher.name)
