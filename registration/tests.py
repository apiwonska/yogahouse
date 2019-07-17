from django.test import Client, TestCase
from django.urls import resolve, reverse

from .forms import UserCreationFormExtended
from .views import SignUpView


class UrlTest(TestCase):

    def test_sign_up_url_resolves(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func.view_class, SignUpView)


class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_set_up_view_url_accessible_by_name(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_set_up_view_use_correct_template(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_set_up_view_uses_correct_form(self):
        '''The view schould use UserCreationFormExtended'''
        url = reverse('signup')
        response = self.client.get(url)
        self.assertTrue('form' in response.context)
        self.assertIsInstance(
            response.context['form'], UserCreationFormExtended)

    def test_set_up_view_success_url_redirects_to_login(self):
        '''After registering user schould be redirected to login'''
        form_data = {
            'username': 'test_username',
            'email': 'test@test.com',
            'first_name': 'First',
            'last_name': 'Last',
            'password1': 'Password123@',
            'password2': 'Password123@'
        }
        url = reverse('signup')
        response = self.client.post(url, form_data)
        self.assertRedirects(response, reverse('login') + '?register')


class UserCreationFormExtendedTest(TestCase):

    def setUp(self):
        self.form_data = {
            'username': 'test_username',
            'email': 'test@test.com',
            'first_name': 'First',
            'last_name': 'Last',
            'password1': 'Password123@',
            'password2': 'Password123@'
        }

    def test_form_has_all_necessary_fields(self):
        form = UserCreationFormExtended()
        # Fields that should be in the form
        necessary_fields = {"username", "email",
                            "first_name", "last_name", "password1", "password2"}
        self.assertEqual(set(form._meta.fields), necessary_fields)

    def test_form_valid(self):
        form = UserCreationFormExtended(self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_email_blank(self):
        self.form_data['email'] = ''
        form = UserCreationFormExtended(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.as_data())

    def test_form_invalid_first_name_blank(self):
        self.form_data['first_name'] = ''
        form = UserCreationFormExtended(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors.as_data())

    def test_form_invalid_last_name_blank(self):
        self.form_data['last_name'] = ''
        form = UserCreationFormExtended(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors.as_data())

    def test_email_field_is_required(self):
        form = UserCreationFormExtended(self.form_data)
        self.assertTrue(form.fields['email'].required)

    def test_email_has_to_be_unique(self):
        form = UserCreationFormExtended(self.form_data)
        form.save()
        form_1 = UserCreationFormExtended(self.form_data)
        error_dict = form_1.errors.as_data()
        self.assertFalse(form_1.is_valid())
        self.assertIn('email', error_dict)
        self.assertIn("Email jest już zarejestrowany. Podaj inny adres email.",
                      str(error_dict['email']))
