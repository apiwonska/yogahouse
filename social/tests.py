from django.test import TestCase

from .models import Link


class LinkTest(TestCase):

    def setUp(self):
        self.link = Link.objects.create()

    def test_object_name(self):
        self.assertEqual(str(self.link), self.link.name)
