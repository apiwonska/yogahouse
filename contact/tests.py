from django.core import mail
from django.test import Client, TestCase
from django.urls import resolve, reverse

from .forms import ContactForm
from .views import contact


class UrlTest(TestCase):

    def test_coltact_url_resolves(self):
        url = reverse('contact:contact')
        self.assertEqual(resolve(url).func, contact)


class ViewTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_view_contact_accessible_by_name(self):
        url = reverse('contact:contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_view_contact_uses_correct_template(self):
        url = reverse('contact:contact')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/base.html', 'contact.html')

    def test_view_contact_contact_form_in_context(self):
        url = reverse('contact:contact')
        response = self.client.get(url)
        self.assertTrue(response.context['form'])
        self.assertTrue(isinstance(response.context['form'], ContactForm))

    def test_view_contact_sends_message_if_form_is_valid(self):
        url = reverse('contact:contact')
        data = {'name': 'test name', 'email': 'test@email.com',
                'content': 'test content'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse(
            'contact:contact') + "?ok", status_code=302, target_status_code=200)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'YogaHouse: Nowa Wiadomość')
        self.assertEqual(mail.outbox[0].body, f"{data['name']}<{data['email']}>\n Napisał(a):\n {data['content']}")
        self.assertEqual(mail.outbox[0].reply_to, [data['email']])

    def test_view_contact_does_not_send_message_if_form_invalid(self):
        url = reverse('contact:contact')
        data = {'name': 'test name', 'email': 'test email.com',
                'content': 'test content'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 0)


class ConactFormTest(TestCase):

    def test_name_required_true(self):
        '''Name field should be required'''
        form = ContactForm()
        self.assertEqual(form.fields['name'].required, True)

    def test_name_placeholder(self):
        form = ContactForm()
        self.assertEqual(form.fields['name'].widget.attrs[
                         'placeholder'], 'Imię i Nazwisko')

    def test_name_min_length(self):
        '''min_length should be 2'''
        form = ContactForm()
        self.assertEqual(form.fields['name'].min_length, 2)

    def test_name_max_length(self):
        '''max_length should be 200'''
        form = ContactForm()
        self.assertEqual(form.fields['name'].max_length, 200)

    def test_email_required_true(self):
        '''Email field should be required'''
        form = ContactForm()
        self.assertEqual(form.fields['email'].required, True)

    def test_email_placeholder(self):
        form = ContactForm()
        self.assertEqual(form.fields['email'].widget.attrs[
                         'placeholder'], 'Email')

    def test_email_min_length(self):
        '''min_length should be 3'''
        form = ContactForm()
        self.assertEqual(form.fields['email'].min_length, 3)

    def test_email_max_length(self):
        '''max_length should be 200'''
        form = ContactForm()
        self.assertEqual(form.fields['email'].max_length, 200)

    def test_content_required_true(self):
        '''content field should be required'''
        form = ContactForm()
        self.assertEqual(form.fields['content'].required, True)

    def test_content_placeholder(self):
        form = ContactForm()
        self.assertEqual(form.fields['content'].widget.attrs[
                         'placeholder'], 'Twoja Wiadomość')

    def test_content_min_length(self):
        '''min_length should be 2'''
        form = ContactForm()
        self.assertEqual(form.fields['content'].min_length, 2)

    def test_content_max_length(self):
        '''max_length should be 1000'''
        form = ContactForm()
        self.assertEqual(form.fields['content'].max_length, 1000)
