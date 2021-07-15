from django import forms


class ContactForm(forms.Form):

    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Imię i Nazwisko',
               'aria-label': 'imię i nazwisko'}), min_length=2, max_length=200)
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email', 
               'aria-label': 'email'}), min_length=3, max_length=200)
    content = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Twoja Wiadomość', 
               'aria-label': 'Wiadomość'}), min_length=2, max_length=1000)
