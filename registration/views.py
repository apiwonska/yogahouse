from django import forms
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserCreationFormExtended


class SignUpView(CreateView):

    form_class = UserCreationFormExtended
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        form.fields['username'].widget = forms.TextInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Wpisz nazwę użytkownika'})
        form.fields['email'].widget = forms.EmailInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Wpisz email'})
        form.fields['first_name'].widget = forms.TextInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Wpisz imię'})
        form.fields['last_name'].widget = forms.TextInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Wpisz nazwisko'})
        form.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Wpisz hasło'})
        form.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control mb-2', 'placeholder': 'Powtórz hasło'})
        return form
