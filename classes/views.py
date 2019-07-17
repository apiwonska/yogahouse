from django.shortcuts import render

from .models import ClassOffer, Conditions, PriceCategory, PriceOption


def class_offer_list(request):
    class_offer = ClassOffer.objects.all()
    return render(request, "classes/class_offer_list.html", {"class_offer": class_offer})


def price_option_list(request):
    prices = PriceOption.objects.all()
    categories = PriceCategory.objects.all()
    return render(request, "classes/price_option_list.html", {'prices': prices, 'categories': categories})


def conditions(request):
    conditions = Conditions.objects.first()
    return render(request, "classes/conditions.html", {'conditions': conditions})
