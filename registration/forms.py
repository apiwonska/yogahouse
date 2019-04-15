from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreationFormExtended(UserCreationForm):
	email = forms.EmailField(required=True, help_text="Maksymalnie 254 znaków.")
	first_name = forms.CharField(label="Imię", required=True)
	last_name = forms.CharField(label="Nazwisko", required=True,)

	class Meta:
		model = User
		fields = ("username", "email", "first_name", "last_name", "password1", "password2")

	def clean_email(self):
		email = self.cleaned_data.get("email")
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("Email jest już zarejestrowany. Podaj inny adres email.")
		else:
			return email

