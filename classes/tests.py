from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import resolve, reverse

from .models import (
    ClassOffer,
    Conditions,
    PriceCategory,
    PriceDetail,
    PriceOption,
)
from .views import class_offer_list, conditions, price_option_list


class UrlTest(TestCase):

    def test_classes_url_resolves(self):
        url = reverse('classes:classes')
        self.assertEqual(resolve(url).func, class_offer_list)

    def test_prices_url_resolves(self):
        url = reverse('classes:prices')
        self.assertEqual(resolve(url).func, price_option_list)

    def test_conditions_url_resolves(self):
        url = reverse('classes:conditions')
        self.assertEqual(resolve(url).func, conditions)


class ViewsTest(TestCase):

    def test_class_offer_list(self):
        client = Client()
        url = reverse('classes:classes')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classes/class_offer_list.html')

    def test_price_option_list(self):
        client = Client()
        url = reverse('classes:prices')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classes/price_option_list.html')

    def test_conditions(self):
        client = Client()
        url = reverse('classes:conditions')
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'classes/conditions.html')


class ClassOfferTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.class_offer = ClassOffer.objects.create()

    def test_order_blank_true(self):
        field_option = self.class_offer._meta.get_field('order').blank
        self.assertTrue(field_option)

    def test_order_null_true(self):
        field_option = self.class_offer._meta.get_field('order').null
        self.assertTrue(field_option)

    def test_created_auto_now_add(self):
        field_option = self.class_offer._meta.get_field('created').auto_now_add
        self.assertTrue(field_option)

    def test_updated_auto_now(self):
        field_option = self.class_offer._meta.get_field('updated').auto_now
        self.assertTrue(field_option)

    def test_object_name_is_title(self):
        object_name = self.class_offer.title
        self.assertEqual(str(self.class_offer), object_name)


class PriceCategoryTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.price_category = PriceCategory.objects.create(
            name='price category name', class_duration=30)

    def test_order_blank_true(self):
        field_option = self.price_category._meta.get_field('order').blank
        self.assertTrue(field_option)

    def test_order_null_true(self):
        field_option = self.price_category._meta.get_field('order').null
        self.assertTrue(field_option)

    def test_created_auto_now_add(self):
        field_option = self.price_category._meta.get_field(
            'created').auto_now_add
        self.assertTrue(field_option)

    def test_updated_auto_now(self):
        field_option = self.price_category._meta.get_field('updated').auto_now
        self.assertTrue(field_option)

    def test_object_name_is_name(self):
        object_name = self.price_category.name
        self.assertEqual(str(self.price_category), object_name)


class PriceDetailTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.price_detail = PriceDetail.objects.create(
            description='price detail description', order=1)

    def test_object_name_is_description(self):
        object_name = self.price_detail.description
        self.assertEqual(str(self.price_detail), object_name)


class PriceOptionTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.price_category = PriceCategory.objects.create(
            name='price category name', class_duration=30)
        cls.price_option = PriceOption.objects.create(
            name='price option test', price=20, price_category=cls.price_category)

    def test_order_blank_true(self):
        field_option = self.price_option._meta.get_field('order').blank
        self.assertTrue(field_option)

    def test_order_null_true(self):
        field_option = self.price_option._meta.get_field('order').null
        self.assertTrue(field_option)

    def test_details_blank_true(self):
        field_option = self.price_option._meta.get_field('details').blank
        self.assertTrue(field_option)

    def test_created_auto_now_add(self):
        field_option = self.price_option._meta.get_field(
            'created').auto_now_add
        self.assertTrue(field_option)

    def test_updated_auto_now(self):
        field_option = self.price_option._meta.get_field('updated').auto_now
        self.assertTrue(field_option)

    def test_object_name_is_name(self):
        object_name = self.price_option.name
        self.assertEqual(str(self.price_option), object_name)


class ConditionsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.conditions = Conditions.objects.create(title='conditions')

    def test_created_auto_now_add(self):
        field_option = self.conditions._meta.get_field('created').auto_now_add
        self.assertTrue(field_option)

    def test_updated_auto_now(self):
        field_option = self.conditions._meta.get_field('updated').auto_now
        self.assertTrue(field_option)

    def test_object_name_is_title(self):
        object_name = self.conditions.title
        self.assertEqual(str(self.conditions), object_name)

    def test_only_one_object_can_exist(self):
        conditions_2 = Conditions(title='test title', content='test content')
        self.assertRaises(ValidationError, conditions_2.full_clean)
        try:
            conditions_2.full_clean()
        except ValidationError as error:
            self.assertEqual(
                error.message_dict,
                {'__all__': ['Może być tylko jeden obiekt "Regulamin". '
                             'Usuń istniejący obiekt, jeśli chcesz dodać nowy.']}
            )
