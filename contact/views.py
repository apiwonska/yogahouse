from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ContactForm


def contact(request):
    contact_form = ContactForm()

    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            content = request.POST.get('content', '')
            # sending an email
            message = EmailMessage(
                "YogaHouse: Nowa Wiadomość",
                f"{name}<{email}>\n Napisał(a):\n {content}",
                "no-contestar@inbox.mailtrap.io",
                ["ann_piv04@gmail.com"],
                reply_to=[email]
            )
            try:
                message.send()
                return redirect(reverse('contact:contact') + "?ok")
            except:
                return redirect(reverse('contact:contact') + "?fail")

    return render(request, "contact/contact.html", {'form': contact_form})
