from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMessage
from .forms import ContactForm

# Create your views here.
def contact(request):
	contact_form = ContactForm()

	if request.method == "POST":
		contact_form = ContactForm(data=request.POST)
		if contact_form.is_valid():
			name = request.POST.get('name','')
			email = request.POST.get('email','')
			content = request.POST.get('content','')
			#sending an email
			message = EmailMessage(
				"YogaHouse: Nowa Wiadomość",
				f"{name}<{email}>\n Napisał(a):\n {content}",
				"no-contestar@inbox.mailtrap.io",
				["a.piwonska@poczta.onet.pl"],
				reply_to=[email]
				)

			try:
				message.send()
				return redirect(reverse('contact')+"?ok")
			except:
				return redirect(reverse('contact')+"?fail")					

	return render(request, "contact/contact.html", {'form':contact_form})